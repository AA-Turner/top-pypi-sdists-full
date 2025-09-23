r'''
# `aws_bedrockagent_prompt`

Refer to the Terraform Registry for docs: [`aws_bedrockagent_prompt`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt).
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


class BedrockagentPrompt(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPrompt",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt aws_bedrockagent_prompt}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        customer_encryption_key_arn: typing.Optional[builtins.str] = None,
        default_variant: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariant", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt aws_bedrockagent_prompt} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.
        :param customer_encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#customer_encryption_key_arn BedrockagentPrompt#customer_encryption_key_arn}.
        :param default_variant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#default_variant BedrockagentPrompt#default_variant}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#description BedrockagentPrompt#description}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#region BedrockagentPrompt#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tags BedrockagentPrompt#tags}.
        :param variant: variant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#variant BedrockagentPrompt#variant}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba34194330bd0e4bbe192694d544e555f049d349b2210bd616fd089192f2545)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BedrockagentPromptConfig(
            name=name,
            customer_encryption_key_arn=customer_encryption_key_arn,
            default_variant=default_variant,
            description=description,
            region=region,
            tags=tags,
            variant=variant,
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
        '''Generates CDKTF code for importing a BedrockagentPrompt resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BedrockagentPrompt to import.
        :param import_from_id: The id of the existing BedrockagentPrompt that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BedrockagentPrompt to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39ab4b3c202783b9e7180a1899007d3a6bdf7582790223bff7b40a113fdf6bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putVariant")
    def put_variant(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariant", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45cbb043d08cd52a051446be3cb4a661e482482b5bfb9ff837bedf84968eada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariant", [value]))

    @jsii.member(jsii_name="resetCustomerEncryptionKeyArn")
    def reset_customer_encryption_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerEncryptionKeyArn", []))

    @jsii.member(jsii_name="resetDefaultVariant")
    def reset_default_variant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultVariant", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVariant")
    def reset_variant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariant", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="variant")
    def variant(self) -> "BedrockagentPromptVariantList":
        return typing.cast("BedrockagentPromptVariantList", jsii.get(self, "variant"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="customerEncryptionKeyArnInput")
    def customer_encryption_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerEncryptionKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultVariantInput")
    def default_variant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultVariantInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="variantInput")
    def variant_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariant"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariant"]]], jsii.get(self, "variantInput"))

    @builtins.property
    @jsii.member(jsii_name="customerEncryptionKeyArn")
    def customer_encryption_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerEncryptionKeyArn"))

    @customer_encryption_key_arn.setter
    def customer_encryption_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65ead866712144c45ecdf7241aaa1487564ffdc761add9e8d298b18d9198063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerEncryptionKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultVariant")
    def default_variant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultVariant"))

    @default_variant.setter
    def default_variant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4679ca035c20903a0d265ede3b2d5cab3ea5fda1bc5d8294cc0992e22bdd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultVariant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcae81fb0d1c0476e7830b2b6daf84b774b23f9e38d5ac89fae3e0d5d5b82017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75865402162fe8ff86822bfbc5cc3630e6c43eb658638c0737ddd6f3d22162b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7f5e9c46732cdf58c92adbe25dc1cec9a9c8c8c41ea3db8a3ccda17636901c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8f91ec64560b0fb052ee997cc8561ecec560635e3119a01d2ad9c1993d7ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptConfig",
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
        "customer_encryption_key_arn": "customerEncryptionKeyArn",
        "default_variant": "defaultVariant",
        "description": "description",
        "region": "region",
        "tags": "tags",
        "variant": "variant",
    },
)
class BedrockagentPromptConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        customer_encryption_key_arn: typing.Optional[builtins.str] = None,
        default_variant: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariant", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.
        :param customer_encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#customer_encryption_key_arn BedrockagentPrompt#customer_encryption_key_arn}.
        :param default_variant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#default_variant BedrockagentPrompt#default_variant}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#description BedrockagentPrompt#description}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#region BedrockagentPrompt#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tags BedrockagentPrompt#tags}.
        :param variant: variant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#variant BedrockagentPrompt#variant}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec42db6c4c8848e5e937a9e31cb42221c0e63ba0b63736f45e8e868a3870973)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument customer_encryption_key_arn", value=customer_encryption_key_arn, expected_type=type_hints["customer_encryption_key_arn"])
            check_type(argname="argument default_variant", value=default_variant, expected_type=type_hints["default_variant"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variant", value=variant, expected_type=type_hints["variant"])
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
        if customer_encryption_key_arn is not None:
            self._values["customer_encryption_key_arn"] = customer_encryption_key_arn
        if default_variant is not None:
            self._values["default_variant"] = default_variant
        if description is not None:
            self._values["description"] = description
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if variant is not None:
            self._values["variant"] = variant

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#customer_encryption_key_arn BedrockagentPrompt#customer_encryption_key_arn}.'''
        result = self._values.get("customer_encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_variant(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#default_variant BedrockagentPrompt#default_variant}.'''
        result = self._values.get("default_variant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#description BedrockagentPrompt#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#region BedrockagentPrompt#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tags BedrockagentPrompt#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def variant(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariant"]]]:
        '''variant block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#variant BedrockagentPrompt#variant}
        '''
        result = self._values.get("variant")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariant"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariant",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "template_type": "templateType",
        "additional_model_request_fields": "additionalModelRequestFields",
        "gen_ai_resource": "genAiResource",
        "inference_configuration": "inferenceConfiguration",
        "metadata": "metadata",
        "model_id": "modelId",
        "template_configuration": "templateConfiguration",
    },
)
class BedrockagentPromptVariant:
    def __init__(
        self,
        *,
        name: builtins.str,
        template_type: builtins.str,
        additional_model_request_fields: typing.Optional[builtins.str] = None,
        gen_ai_resource: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantGenAiResource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inference_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantInferenceConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantMetadata", typing.Dict[builtins.str, typing.Any]]]]] = None,
        model_id: typing.Optional[builtins.str] = None,
        template_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.
        :param template_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#template_type BedrockagentPrompt#template_type}.
        :param additional_model_request_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#additional_model_request_fields BedrockagentPrompt#additional_model_request_fields}.
        :param gen_ai_resource: gen_ai_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#gen_ai_resource BedrockagentPrompt#gen_ai_resource}
        :param inference_configuration: inference_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#inference_configuration BedrockagentPrompt#inference_configuration}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#metadata BedrockagentPrompt#metadata}
        :param model_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#model_id BedrockagentPrompt#model_id}.
        :param template_configuration: template_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#template_configuration BedrockagentPrompt#template_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad98a70424ab275d5e684a1414bd5638bf007508b55be168b3a4d8a5dfd129c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument template_type", value=template_type, expected_type=type_hints["template_type"])
            check_type(argname="argument additional_model_request_fields", value=additional_model_request_fields, expected_type=type_hints["additional_model_request_fields"])
            check_type(argname="argument gen_ai_resource", value=gen_ai_resource, expected_type=type_hints["gen_ai_resource"])
            check_type(argname="argument inference_configuration", value=inference_configuration, expected_type=type_hints["inference_configuration"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "template_type": template_type,
        }
        if additional_model_request_fields is not None:
            self._values["additional_model_request_fields"] = additional_model_request_fields
        if gen_ai_resource is not None:
            self._values["gen_ai_resource"] = gen_ai_resource
        if inference_configuration is not None:
            self._values["inference_configuration"] = inference_configuration
        if metadata is not None:
            self._values["metadata"] = metadata
        if model_id is not None:
            self._values["model_id"] = model_id
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#template_type BedrockagentPrompt#template_type}.'''
        result = self._values.get("template_type")
        assert result is not None, "Required property 'template_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_model_request_fields(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#additional_model_request_fields BedrockagentPrompt#additional_model_request_fields}.'''
        result = self._values.get("additional_model_request_fields")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gen_ai_resource(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantGenAiResource"]]]:
        '''gen_ai_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#gen_ai_resource BedrockagentPrompt#gen_ai_resource}
        '''
        result = self._values.get("gen_ai_resource")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantGenAiResource"]]], result)

    @builtins.property
    def inference_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantInferenceConfiguration"]]]:
        '''inference_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#inference_configuration BedrockagentPrompt#inference_configuration}
        '''
        result = self._values.get("inference_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantInferenceConfiguration"]]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantMetadata"]]]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#metadata BedrockagentPrompt#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantMetadata"]]], result)

    @builtins.property
    def model_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#model_id BedrockagentPrompt#model_id}.'''
        result = self._values.get("model_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfiguration"]]]:
        '''template_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#template_configuration BedrockagentPrompt#template_configuration}
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantGenAiResource",
    jsii_struct_bases=[],
    name_mapping={"agent": "agent"},
)
class BedrockagentPromptVariantGenAiResource:
    def __init__(
        self,
        *,
        agent: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantGenAiResourceAgent", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param agent: agent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#agent BedrockagentPrompt#agent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a8c23ed677f0d22b56914f08e91974825ac19e02684f8d4802344a5e79ff1f)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent is not None:
            self._values["agent"] = agent

    @builtins.property
    def agent(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantGenAiResourceAgent"]]]:
        '''agent block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#agent BedrockagentPrompt#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantGenAiResourceAgent"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantGenAiResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantGenAiResourceAgent",
    jsii_struct_bases=[],
    name_mapping={"agent_identifier": "agentIdentifier"},
)
class BedrockagentPromptVariantGenAiResourceAgent:
    def __init__(self, *, agent_identifier: builtins.str) -> None:
        '''
        :param agent_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#agent_identifier BedrockagentPrompt#agent_identifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d63f3c994f49299005fafbbda05c3cb21786960250edf96f3e3a73b649c5a9)
            check_type(argname="argument agent_identifier", value=agent_identifier, expected_type=type_hints["agent_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_identifier": agent_identifier,
        }

    @builtins.property
    def agent_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#agent_identifier BedrockagentPrompt#agent_identifier}.'''
        result = self._values.get("agent_identifier")
        assert result is not None, "Required property 'agent_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantGenAiResourceAgent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantGenAiResourceAgentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantGenAiResourceAgentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b814a7ef7ccb08974b004fc6de0c004aedf5f01bcdc866a5f1ecaa5b54e9ef3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantGenAiResourceAgentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafdd6dbaebf7f8493213a0fa26bd59cc151500fa28ec13e2a64227ac7cc7bc7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantGenAiResourceAgentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a7d3a6773da8ddaab9ca0a7c03fb0777d81b705414566310bffdd0ab019765)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b35b466e5ae34d53cde97d7a50961a995da71963abf7e0409d3fb867bda35d8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58ab534d70c4da5f3268af87ac66db467b9a7313e7cec3b726a4f366a8ec6df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResourceAgent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResourceAgent]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResourceAgent]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf7bf1d5ae8efc753402bc487066b40a63c8772dfdb42539dcf68ed11069615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantGenAiResourceAgentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantGenAiResourceAgentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09ae40ff6c5833f5d09aeabc983e454bf2fc4ec30b5e62d4c304484b3f3579d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="agentIdentifierInput")
    def agent_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="agentIdentifier")
    def agent_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentIdentifier"))

    @agent_identifier.setter
    def agent_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea9e2e290a829631c2d738d9bd4672a14ba0fbcf1bda84366abbb5557f2d201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResourceAgent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResourceAgent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResourceAgent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b041c386a1efd27e9b4e32a0e196616a279d7a879938f9c4fc06816b08133b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantGenAiResourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantGenAiResourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66426db7b27197a6b54f58ff173b09bc113ab74c6e2c667c029758033e8b56ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantGenAiResourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c735c101380e00d6434d0ea218ed4941299d7375c45068512a20533c5c15f9d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantGenAiResourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a469e53014c908817dac4a45e11a6fdc4aa1ed56e737170812595607ccf36b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d15dc855678f8457d55b4492b3981d92e564685635e757ff32c5f6e9770404d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d47ac05a145a006eefc4c25c20b65180b9601220fb32bc550c0fa93fdfbc2aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea5f0e00e7084e53f9d5586661764e3bd1731378751fe190c3e0e09a1c82a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantGenAiResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantGenAiResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2249dfaa8d719503e1a958205b044718c4149f055b8218c2a73f09aca41efde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAgent")
    def put_agent(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantGenAiResourceAgent, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9edc09758d12359951522bc7d4f008e3a7ccd47272eda2bb74c702ec7299d441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAgent", [value]))

    @jsii.member(jsii_name="resetAgent")
    def reset_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgent", []))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> BedrockagentPromptVariantGenAiResourceAgentList:
        return typing.cast(BedrockagentPromptVariantGenAiResourceAgentList, jsii.get(self, "agent"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResourceAgent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResourceAgent]]], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2e5bf34544cfe2c317b8635e480a0ce7109af7c065c1d450bc3261addaf979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantInferenceConfiguration",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class BedrockagentPromptVariantInferenceConfiguration:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantInferenceConfigurationText", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b5f39e3d2974ff9e58a549fce8ac7584adaca13145e25e28634ad3284535e5)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantInferenceConfigurationText"]]]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantInferenceConfigurationText"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantInferenceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantInferenceConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantInferenceConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df98c8b472056e8d4e5f0c2d1c9b558c378092bf638bcec95a2ab02ad97af7dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantInferenceConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18000becc0e2dc5467373d2cf01a6f4e71ceebdb680f0cdd9827a33f28a4e93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantInferenceConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea8f003adfc97d46f1afb300f93924985302c230c1c3fcef5fe3edd11741672)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad60d6e4baeb7cf21cec8f045c0ec90183bde3a725fb7365c9a0eb0882c47371)
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
            type_hints = typing.get_type_hints(_typecheckingstub__703b95023211803ba2d9964e224847ffbc671bc789f91794f112ec57806ee975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b066bd5ee9af142a7cd5333338757dcf523e08a65e3339988d498b6d23ebaf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantInferenceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantInferenceConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69ff2ad2c7894da87565d3a35558de050783d7ef56fc8764d942dae7c9caecc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putText")
    def put_text(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantInferenceConfigurationText", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc67da7c193a6ec109cd3858fe83a34c29737c2d961d30319899c5e56ccf250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> "BedrockagentPromptVariantInferenceConfigurationTextList":
        return typing.cast("BedrockagentPromptVariantInferenceConfigurationTextList", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantInferenceConfigurationText"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantInferenceConfigurationText"]]], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649c61fe2ddd0976006ad67f62abe646cc6b251917067b5fbd1be79142c81f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantInferenceConfigurationText",
    jsii_struct_bases=[],
    name_mapping={
        "max_tokens": "maxTokens",
        "stop_sequences": "stopSequences",
        "temperature": "temperature",
        "top_p": "topP",
    },
)
class BedrockagentPromptVariantInferenceConfigurationText:
    def __init__(
        self,
        *,
        max_tokens: typing.Optional[jsii.Number] = None,
        stop_sequences: typing.Optional[typing.Sequence[builtins.str]] = None,
        temperature: typing.Optional[jsii.Number] = None,
        top_p: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_tokens: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#max_tokens BedrockagentPrompt#max_tokens}.
        :param stop_sequences: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#stop_sequences BedrockagentPrompt#stop_sequences}.
        :param temperature: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#temperature BedrockagentPrompt#temperature}.
        :param top_p: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#top_p BedrockagentPrompt#top_p}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef9d4ef42161a2745a2a05d7aa7ca3fb742112606b7b5f1ff77a5b8af8e98e6)
            check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
            check_type(argname="argument stop_sequences", value=stop_sequences, expected_type=type_hints["stop_sequences"])
            check_type(argname="argument temperature", value=temperature, expected_type=type_hints["temperature"])
            check_type(argname="argument top_p", value=top_p, expected_type=type_hints["top_p"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_tokens is not None:
            self._values["max_tokens"] = max_tokens
        if stop_sequences is not None:
            self._values["stop_sequences"] = stop_sequences
        if temperature is not None:
            self._values["temperature"] = temperature
        if top_p is not None:
            self._values["top_p"] = top_p

    @builtins.property
    def max_tokens(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#max_tokens BedrockagentPrompt#max_tokens}.'''
        result = self._values.get("max_tokens")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stop_sequences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#stop_sequences BedrockagentPrompt#stop_sequences}.'''
        result = self._values.get("stop_sequences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def temperature(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#temperature BedrockagentPrompt#temperature}.'''
        result = self._values.get("temperature")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def top_p(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#top_p BedrockagentPrompt#top_p}.'''
        result = self._values.get("top_p")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantInferenceConfigurationText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantInferenceConfigurationTextList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantInferenceConfigurationTextList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a1b893aec81d34cf31a8c8e16039539df9307208985fda5b5dca26c7fa37fdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantInferenceConfigurationTextOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db2bca54e7cc2ae55f284d923d037f5a4598a934025c153d8ce026a8f4cd46e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantInferenceConfigurationTextOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee7e5b1cadf061ff1b308e43f78fe62a75ec5812a6e41eeac7c28bc248fea27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__834e74b4c8b6c1986a1c161db7d79aaf5b33e29fca0f1ea1416bc52b42d477ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f82827480e747a4302305f827ba221caf597b5484d27a0a1eea297a9ce43890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfigurationText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfigurationText]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfigurationText]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35bc62aeb8513d62feaef424481cab3a19a011a61ffeff73e1a7ad79ccc5ecc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantInferenceConfigurationTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantInferenceConfigurationTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__644bbc7903cfc9304672624da4da8d26167c856d88b582a2ab020c2049f37b73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaxTokens")
    def reset_max_tokens(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTokens", []))

    @jsii.member(jsii_name="resetStopSequences")
    def reset_stop_sequences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopSequences", []))

    @jsii.member(jsii_name="resetTemperature")
    def reset_temperature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemperature", []))

    @jsii.member(jsii_name="resetTopP")
    def reset_top_p(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopP", []))

    @builtins.property
    @jsii.member(jsii_name="maxTokensInput")
    def max_tokens_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTokensInput"))

    @builtins.property
    @jsii.member(jsii_name="stopSequencesInput")
    def stop_sequences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stopSequencesInput"))

    @builtins.property
    @jsii.member(jsii_name="temperatureInput")
    def temperature_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "temperatureInput"))

    @builtins.property
    @jsii.member(jsii_name="topPInput")
    def top_p_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "topPInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTokens")
    def max_tokens(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTokens"))

    @max_tokens.setter
    def max_tokens(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69e1f2cea1fee291b53d3026126b63390c8a6bc5a2d7e2a9ccc53d10bbc93f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopSequences")
    def stop_sequences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stopSequences"))

    @stop_sequences.setter
    def stop_sequences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa06d34bf6eb5ca141fa6e90f3c8f9972b12f0fd13b888d5aa2ea1af06572176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopSequences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temperature")
    def temperature(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "temperature"))

    @temperature.setter
    def temperature(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad7485843df595d8ddbf4c1f66d468c3407cff201b2435dc8cb6957db6ed663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temperature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topP")
    def top_p(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "topP"))

    @top_p.setter
    def top_p(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dddb59b900ad6ef90b20c215d4e9e293caf83b2698d5ba849d738b6a35f8440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topP", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfigurationText]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfigurationText]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfigurationText]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbf93943a7da61707aa94749c0be55a515037b1db2a2b709601e138d1017723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd70288b9aca7ae69f09f8e28915702e208c6d33df3b4cf18f4439a41c89306e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BedrockagentPromptVariantOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a69744ed909e068ca30f58872f4361b9062e0b523b3e8a2ac62b2428ece2f8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f26746d855aee716dd700b7c8795e4fc6d995139d810133dec649ab0fb41bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31747ccd51d51aa21f926e5d4ed0fa5bf2877938c6dd8eed693f133ffe98dbad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35758bd366849a252825dea7b6abe8cc9ac9cd9a331bd8b38af60f32e3bd728c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariant]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariant]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariant]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4721f0f051d924d1d7c0cf656e314885360e721615e73e7808b254f74b7c797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantMetadata",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class BedrockagentPromptVariantMetadata:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#key BedrockagentPrompt#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#value BedrockagentPrompt#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d34764fd1e65eb50c241750ecb1f58008694e427a3ffc77730a897cc2850417)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#key BedrockagentPrompt#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#value BedrockagentPrompt#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bd0acd1d6de481c724a2c520a1a398f33721e9f6b11794a33233ada0023ab79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58930050641f5e6b04423d6123e1015cbce46deadf92af4ee7d102de9872b30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05d5105acba7bcd3fe884932bc147e2ac5d8f2d5069e6c8a58039a2a4b0c408)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34540f7eb3c82d0c29d8d5a89f3ed76f3cfa91db28b028d7ba149107b43dbcab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9385e025f395bdf2fe50f100d08554b6d36556dbbaf258a05e36927effee1da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantMetadata]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantMetadata]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantMetadata]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785d88fe248744db47e1b9dc4e692e0405a91ec80de79e1f38e363f96c8ad875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbd18505f78292293e1fc26f7c043c3021ade8c7a7f1831a345de90356d311b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897a59a6ccce482a52a9efbcd5ebab0c1a91de9f90e46e3012ef3b4e6736387e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074dd90f3ee522b9b7fc42a60ef580ee6b1c1abb66e63a3aac5677bc8c9aa16b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantMetadata]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantMetadata]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantMetadata]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8c291ad5db6b6f6c438cbfcada4147c0cfaba7e42e07bb42fa88b1981ed718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bac6aaf4e2e0a8bbd3d4064d9c981c01c06253c127ac8e18d687077f2f58e59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGenAiResource")
    def put_gen_ai_resource(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantGenAiResource, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fa84eb4ef6b313471997079d09d7e56b78075679950346bc7c38aa4aa774cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGenAiResource", [value]))

    @jsii.member(jsii_name="putInferenceConfiguration")
    def put_inference_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantInferenceConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73df22b7bfddb9ae696f5a2f7a0f4f67984eb6a981e0d245b233bb0a7a424802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInferenceConfiguration", [value]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantMetadata, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6510d55155e1708d070b599931cc7a2d180083f35edf0666d49fbc425cbc05aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putTemplateConfiguration")
    def put_template_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353c5d56e59fb63ca6e0afb94718f30b0e3cb3255c60f0e6cbbfb03fc8e3c330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTemplateConfiguration", [value]))

    @jsii.member(jsii_name="resetAdditionalModelRequestFields")
    def reset_additional_model_request_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalModelRequestFields", []))

    @jsii.member(jsii_name="resetGenAiResource")
    def reset_gen_ai_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenAiResource", []))

    @jsii.member(jsii_name="resetInferenceConfiguration")
    def reset_inference_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceConfiguration", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetModelId")
    def reset_model_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelId", []))

    @jsii.member(jsii_name="resetTemplateConfiguration")
    def reset_template_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="genAiResource")
    def gen_ai_resource(self) -> BedrockagentPromptVariantGenAiResourceList:
        return typing.cast(BedrockagentPromptVariantGenAiResourceList, jsii.get(self, "genAiResource"))

    @builtins.property
    @jsii.member(jsii_name="inferenceConfiguration")
    def inference_configuration(
        self,
    ) -> BedrockagentPromptVariantInferenceConfigurationList:
        return typing.cast(BedrockagentPromptVariantInferenceConfigurationList, jsii.get(self, "inferenceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> BedrockagentPromptVariantMetadataList:
        return typing.cast(BedrockagentPromptVariantMetadataList, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    def template_configuration(
        self,
    ) -> "BedrockagentPromptVariantTemplateConfigurationList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationList", jsii.get(self, "templateConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="additionalModelRequestFieldsInput")
    def additional_model_request_fields_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "additionalModelRequestFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="genAiResourceInput")
    def gen_ai_resource_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResource]]], jsii.get(self, "genAiResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceConfigurationInput")
    def inference_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfiguration]]], jsii.get(self, "inferenceConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantMetadata]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantMetadata]]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="modelIdInput")
    def model_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="templateConfigurationInput")
    def template_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfiguration"]]], jsii.get(self, "templateConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="templateTypeInput")
    def template_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalModelRequestFields")
    def additional_model_request_fields(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "additionalModelRequestFields"))

    @additional_model_request_fields.setter
    def additional_model_request_fields(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7be99120932789a3fd78be4c00ecbcec791c116c613de56d299d4e622ddf9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalModelRequestFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelId"))

    @model_id.setter
    def model_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acc64c385728c4549ad308d96f9a986516e00e1b2e75b7befa578e19413fdbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7c684c4810552ac987299814d1d2af41964c5a580babe530c57315420b30a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateType")
    def template_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateType"))

    @template_type.setter
    def template_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0182213082308d4eacdd4aefa248e63d62c2e49f06aa6837633ea95715dab1d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariant]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariant]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariant]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f66480491bd7e4beee9b2f045392a78f7ebd97a44def09cc526676e67ca8d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfiguration",
    jsii_struct_bases=[],
    name_mapping={"chat": "chat", "text": "text"},
)
class BedrockagentPromptVariantTemplateConfiguration:
    def __init__(
        self,
        *,
        chat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationText", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param chat: chat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#chat BedrockagentPrompt#chat}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25216f596a10d7af3a469ee20cc6728b25e3392e442e9fbb853bf9f4f683fb5)
            check_type(argname="argument chat", value=chat, expected_type=type_hints["chat"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chat is not None:
            self._values["chat"] = chat
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def chat(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChat"]]]:
        '''chat block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#chat BedrockagentPrompt#chat}
        '''
        result = self._values.get("chat")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChat"]]], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationText"]]]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationText"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChat",
    jsii_struct_bases=[],
    name_mapping={
        "input_variable": "inputVariable",
        "message": "message",
        "system_attribute": "systemAttribute",
        "tool_configuration": "toolConfiguration",
    },
)
class BedrockagentPromptVariantTemplateConfigurationChat:
    def __init__(
        self,
        *,
        input_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatInputVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        message: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatMessage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        system_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatSystem", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tool_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param input_variable: input_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#input_variable BedrockagentPrompt#input_variable}
        :param message: message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#message BedrockagentPrompt#message}
        :param system_attribute: system block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#system BedrockagentPrompt#system}
        :param tool_configuration: tool_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool_configuration BedrockagentPrompt#tool_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f9c3ee2548cb4a0be20837b82f45ee2c5b3805a58577f0e2d34c67defc37f7)
            check_type(argname="argument input_variable", value=input_variable, expected_type=type_hints["input_variable"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument system_attribute", value=system_attribute, expected_type=type_hints["system_attribute"])
            check_type(argname="argument tool_configuration", value=tool_configuration, expected_type=type_hints["tool_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_variable is not None:
            self._values["input_variable"] = input_variable
        if message is not None:
            self._values["message"] = message
        if system_attribute is not None:
            self._values["system_attribute"] = system_attribute
        if tool_configuration is not None:
            self._values["tool_configuration"] = tool_configuration

    @builtins.property
    def input_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatInputVariable"]]]:
        '''input_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#input_variable BedrockagentPrompt#input_variable}
        '''
        result = self._values.get("input_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatInputVariable"]]], result)

    @builtins.property
    def message(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatMessage"]]]:
        '''message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#message BedrockagentPrompt#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatMessage"]]], result)

    @builtins.property
    def system_attribute(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatSystem"]]]:
        '''system block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#system BedrockagentPrompt#system}
        '''
        result = self._values.get("system_attribute")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatSystem"]]], result)

    @builtins.property
    def tool_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration"]]]:
        '''tool_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool_configuration BedrockagentPrompt#tool_configuration}
        '''
        result = self._values.get("tool_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatInputVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class BedrockagentPromptVariantTemplateConfigurationChatInputVariable:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283c319aeeedc1dbc477af948c66b9652bde09484b484c6078ac8915f5e39a88)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatInputVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatInputVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatInputVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53f02fa69fe7284d9a78bde90c2e9b2f937ac8567b8405343135216319c8315c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatInputVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f237b918828fc2932ae3e5a84b18351a5077deb3c324472a8a2bde869c9ccd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatInputVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b37671f5e25c3b73fc6a0402c711acb00334f6a45d14935561b589a5c2d8a5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4753cda7b510a1c2bc7181d5ff6797f788eb6308b458e06003076824a6afe9ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ab1d1ded0d04a350f4ac6d331442bebe1618f2e79d37f311e16d4321b0ac90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatInputVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatInputVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatInputVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0b644e6d35dbdab44fe75efa5d4856aed29778407216d413db6e16be9823e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatInputVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatInputVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__567c93a2568c21ecbf48ec3a280cba430f1d98efbb7f2f43dc4a0380869ae425)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb7c454672fd044c10a40804bf12803125b5b356236b191fa8cbd51c0d90bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatInputVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatInputVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatInputVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce075c742e8a107713c265fb81c8bdfade4de94d6cefa446d7171788c61af4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3185be2b6b7f2214c2bf29c5c6e432b238b814f1964145e0d9afe3a3d3ea018)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa74605d236c0b0955c8bd452503c9cb2d3c0bff7cbbb73d7966748f2cdf588)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1b72aa0f715289883481a69923c3596e1f9a4eb4c88cb4c02ea524888f9397)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6cb1cd430948a995f0bae4ee38511cfb22201a8aaaab1f9e4dae2da476e8d94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cb41221681e1d41272480ec75f22747d1cabcc2db3e4493bee8636840ba6f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChat]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChat]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChat]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7f55d220fb006249a1786bc85d0f69c730bfabe452fd96a436a6560940b6d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessage",
    jsii_struct_bases=[],
    name_mapping={"role": "role", "content": "content"},
)
class BedrockagentPromptVariantTemplateConfigurationChatMessage:
    def __init__(
        self,
        *,
        role: builtins.str,
        content: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatMessageContent", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#role BedrockagentPrompt#role}.
        :param content: content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#content BedrockagentPrompt#content}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e782bde952cdaf114ec26e07bf821071275a68909c118a8cae4572d6403963)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
        }
        if content is not None:
            self._values["content"] = content

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#role BedrockagentPrompt#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatMessageContent"]]]:
        '''content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#content BedrockagentPrompt#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatMessageContent"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageContent",
    jsii_struct_bases=[],
    name_mapping={"cache_point": "cachePoint", "text": "text"},
)
class BedrockagentPromptVariantTemplateConfigurationChatMessageContent:
    def __init__(
        self,
        *,
        cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_point: cache_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423a98636b8b7956db22c29cefdc52d8447c88e39846b7bb5d8e3af9b3a662d1)
            check_type(argname="argument cache_point", value=cache_point, expected_type=type_hints["cache_point"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_point is not None:
            self._values["cache_point"] = cache_point
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def cache_point(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint"]]]:
        '''cache_point block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        '''
        result = self._values.get("cache_point")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint"]]], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}.'''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatMessageContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713bcbf03f3770d03ff1d2ea1bf8f62800101f15e5b0db31d81f14d1829268b9)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0280f9d2b155483fd3149b15d4a4c09096d223a9fa9a2ad93a7624afd8bc13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00308cc585b094de9e70dcb82a22e819f36ae6c3317d1f496059bd2ab195eff8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14b2445e7aec93a34ff53f2ea51a650bb690a7552596856bbf38fe8cd29f41f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b4f8d3c346480b83287294722571314299ac8207df4ac2cc4129e33427d3c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7d04679c900e45f8d4066af66edaae8cf82b04738e5bb835550133decc59801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa39c745a0cf371e1bbf33b171137e363ec8579be2ba2a3d274f73c3ffe7c0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a3f09e0066e1d651ce7c2ed80420f310bc38acefddc8e1f4d97afbf74503ab6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c3f82faaca2a7172d681b907a657b3413f57a9412be925378030028ffb3f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbac14e310923c5795af022eb1924656ae666bdd2a295004918578d7ad3d9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatMessageContentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageContentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__529ab5455ae1f0ded7dedd29ce64ac06f01dcaa7d628ff6d1099b958f9e955ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatMessageContentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c556f4ca02cfacb5087408cf4ff91e25d879f9e1439db475378bcfb86346a1ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatMessageContentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd6dcef4abcaaf55e90dcac80a218bbd2b4c0d58e2d8e9c023b1fa186149eea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c6f4810cb3875663ee7ef8f9329531f53be3d22d30b570cc220fb1fcef48abf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0adc3b34c421a46d3999bac2e8554cd86efcfa00ef4ec172bb7ecf010f14ed8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContent]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContent]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bf4455c87fbd1595328fd917e86cd085d2d55c0fa85f8a92d85edab8448a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatMessageContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageContentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d56229a21e38a555602d2592fb4bdad846d4b3beeb18061cf2c1c06d64934ea1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCachePoint")
    def put_cache_point(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15d1e2d210a4d7cedd9a272538505228d8243f3210c56d165285922cac1727e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCachePoint", [value]))

    @jsii.member(jsii_name="resetCachePoint")
    def reset_cache_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePoint", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="cachePoint")
    def cache_point(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointList, jsii.get(self, "cachePoint"))

    @builtins.property
    @jsii.member(jsii_name="cachePointInput")
    def cache_point_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]]], jsii.get(self, "cachePointInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e21820b0d53ac7920cb02abf7267adcea7fc8945814198073787bd2d078d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025f1e3e6a76eddf94236f2dbee58e04785b7ddb2d137806dc98a761d8192f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c289b92b807971ee35eeb65ca5dd3c4f93110f9ad3537e0207709e90473fc32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cedb1e4e052718bcbf58e88cf1ba4c63527b8082e7f3b2fbfea59a263dc426e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46e59bdd3014a07b149c64ce20aa321edbe8fac80eb80ba7cd13bdded334f4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__778d7f856ef8a2fc5f3ecb6075b55ff46d0a7ee229dec1ec71215154137e1caa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a265e45e91ca9366b06bf8272162af44b5940477449f2555dfd9ca370950a0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79cbf140bede2483bb36bbb4685fda4861f15558b9f7ef8381ddf708052638f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad1efc3ea92a2afa0b33106bf62e69a4d4156dd97f5e4e5ab0bdcf826da413ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContent")
    def put_content(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessageContent, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48f343a7abae27c150d6e563c68a4879f18427f21b30a74472c9f06f15cae54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContent", [value]))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatMessageContentList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatMessageContentList, jsii.get(self, "content"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContent]]], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3d0d7e0489182a8db8961f8d8c0128119ab076ab2214933951687aa3956f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32897f47139547cd2d836125a04d4ce4c6e18f4ce204d89d29fe669d3d64bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d69eb3af9f3c3f269a4a6c32497f5e5cb88eea409650260fdd4053619220706b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInputVariable")
    def put_input_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatInputVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6dff4a63f57bb885e42d73e06b3c62372aaa1a86ca3c8ff20f38898e7d9983b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputVariable", [value]))

    @jsii.member(jsii_name="putMessage")
    def put_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e3bfd9d87663a3a30972ebdd82b77271bd9a3c43f9f37add2783aef95e5756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessage", [value]))

    @jsii.member(jsii_name="putSystemAttribute")
    def put_system_attribute(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatSystem", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b927c7e511a03a8845eec47bee4d6b10389a367c409b13bb3fafbf6bab5b4a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSystemAttribute", [value]))

    @jsii.member(jsii_name="putToolConfiguration")
    def put_tool_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8898e797ff65f5b75afad4ab9556129dd01dc390bb837e5c2c594e430d4b202b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putToolConfiguration", [value]))

    @jsii.member(jsii_name="resetInputVariable")
    def reset_input_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputVariable", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetSystemAttribute")
    def reset_system_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemAttribute", []))

    @jsii.member(jsii_name="resetToolConfiguration")
    def reset_tool_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToolConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="inputVariable")
    def input_variable(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatInputVariableList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatInputVariableList, jsii.get(self, "inputVariable"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> BedrockagentPromptVariantTemplateConfigurationChatMessageList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatMessageList, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="systemAttribute")
    def system_attribute(
        self,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatSystemList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatSystemList", jsii.get(self, "systemAttribute"))

    @builtins.property
    @jsii.member(jsii_name="toolConfiguration")
    def tool_configuration(
        self,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationList", jsii.get(self, "toolConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="inputVariableInput")
    def input_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatInputVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatInputVariable]]], jsii.get(self, "inputVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessage]]], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="systemAttributeInput")
    def system_attribute_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatSystem"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatSystem"]]], jsii.get(self, "systemAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="toolConfigurationInput")
    def tool_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration"]]], jsii.get(self, "toolConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChat]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChat]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChat]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4022dd64a0b89bacf1c7e3d3da664455b981f8ac025c7299ff9f4ff65471176a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatSystem",
    jsii_struct_bases=[],
    name_mapping={"cache_point": "cachePoint", "text": "text"},
)
class BedrockagentPromptVariantTemplateConfigurationChatSystem:
    def __init__(
        self,
        *,
        cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_point: cache_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2998028f32766775d6d53c0bff9b61330ebe7863d9a265028359bbf1baa8b14e)
            check_type(argname="argument cache_point", value=cache_point, expected_type=type_hints["cache_point"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_point is not None:
            self._values["cache_point"] = cache_point
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def cache_point(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint"]]]:
        '''cache_point block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        '''
        result = self._values.get("cache_point")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint"]]], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}.'''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatSystem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afcd12fe5183c705958aaf6daa05e27f035c1fe7ae961d774978f23023c0fb0)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a027dd9ab149b472d1c65f332683b995cd66772a1edfb0a0bdd5e292338eb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a4ce1c3b92e8bac4673c022acfda3a568a873f2bdd4ae2a6cf2153d87eb7df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c80da34159b496bda579fa8d3010fe1fddbcc04f6d846778b7af3b7d6f8ebe9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be46b7192023830e0bbeb03d6800d15f171e2796de8f7a203f774126b2535a5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91b1149a2afb2f347da77bb8840fc364978ae2e5830a2bdfa9a893c504f02c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d81cf0a529bb75570932308b2137ce66406c394310b208200899dd716a6dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__427102db16aa33ee1c9fbdfaeab5a36c314c4aa461e6d95bc013deea96321755)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465f996152d1cf041c604157934fca9355f15e2a72e455a8d1ff3ecbf5ab5710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd29aa7f00cf135501aec6dccd1b913f90a58676d05793b7b792228fd92b0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatSystemList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatSystemList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05fb177d3982fb798c1ef6acf31aebb29a23a43f4165e58aefabc821edbc84d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatSystemOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b43fff10af12c9d450922f0e07e648be185fd7b17810c10f041a75669aad0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatSystemOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051775a26b35c4785cd6f05016fed750637920e8af052be01517471fe5246c5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be81671e804aece8953757800d324d98bdf3a0c96d62c50e99fc3b5c1798087)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d520f9b9d83234d90fbc63236e1ab901d881765fff22aae117e7d8e3de230188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystem]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystem]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystem]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9df1d7fd0c613494c9e5578f73dad6df56a57a40156f2abfabd3efee2430d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatSystemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatSystemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28a003ef962186c770c854585fdea5e907376b0db1f867948bde6cbcd47c0a18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCachePoint")
    def put_cache_point(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225ad6e9c23b7fad3dcbbdf98d79b4a3ce0a0ef614a77aa1a12d53970b0c11a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCachePoint", [value]))

    @jsii.member(jsii_name="resetCachePoint")
    def reset_cache_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePoint", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="cachePoint")
    def cache_point(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointList, jsii.get(self, "cachePoint"))

    @builtins.property
    @jsii.member(jsii_name="cachePointInput")
    def cache_point_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]]], jsii.get(self, "cachePointInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4164042e9f1ee1c50c90a66c974a7e3a2cfc166c0a743d312a572d3e7d5002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystem]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystem]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystem]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98928c9d297cc840280af891172947a7bae8c77986780e219e0735a0a5679198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration",
    jsii_struct_bases=[],
    name_mapping={"tool": "tool", "tool_choice": "toolChoice"},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration:
    def __init__(
        self,
        *,
        tool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tool_choice: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param tool: tool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool BedrockagentPrompt#tool}
        :param tool_choice: tool_choice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool_choice BedrockagentPrompt#tool_choice}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9592704dbfc5b45a46114711aa0f41df7e572fc42315d4a4b96106bc392b2e)
            check_type(argname="argument tool", value=tool, expected_type=type_hints["tool"])
            check_type(argname="argument tool_choice", value=tool_choice, expected_type=type_hints["tool_choice"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tool is not None:
            self._values["tool"] = tool
        if tool_choice is not None:
            self._values["tool_choice"] = tool_choice

    @builtins.property
    def tool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool"]]]:
        '''tool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool BedrockagentPrompt#tool}
        '''
        result = self._values.get("tool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool"]]], result)

    @builtins.property
    def tool_choice(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice"]]]:
        '''tool_choice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool_choice BedrockagentPrompt#tool_choice}
        '''
        result = self._values.get("tool_choice")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c34ae9d3c1ded6e2f6da213e0798cbaf08b328130a26cdbdcd10e9b3184d02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40ac1f3bd89589aba226139a6b7258d9225e9e88b0c3147d83580a55a99b07e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5009d7a3c7a19034295ad30e5739bb0a723a3cb982175eef5a3d5608d2cf94c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5598e97e7a1ef785f6561cd07e0ed92582b7802e71cfc66ab058145aa285849)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7743cc25e54ce9b3043bb8b0e6ecd47d9695e65b95feb565dcafebc97e3d66bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55c120fa1036d188e899358e93ddcf5775faa8f632475b8a50236b0ca82f1d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebdf996ea9ca7e52e5b403912a355afb4774077c20ee62e38a15e16c488a9f84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTool")
    def put_tool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8e9c82b66eeaa580c847baae7087d6636da228e1f03c43efa5f65497d7be6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTool", [value]))

    @jsii.member(jsii_name="putToolChoice")
    def put_tool_choice(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b57cdf7f2edb248dc0a57cc9213359837baa4c23e6b48ea1ffc7261e2d1139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putToolChoice", [value]))

    @jsii.member(jsii_name="resetTool")
    def reset_tool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTool", []))

    @jsii.member(jsii_name="resetToolChoice")
    def reset_tool_choice(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToolChoice", []))

    @builtins.property
    @jsii.member(jsii_name="tool")
    def tool(
        self,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolList", jsii.get(self, "tool"))

    @builtins.property
    @jsii.member(jsii_name="toolChoice")
    def tool_choice(
        self,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceList", jsii.get(self, "toolChoice"))

    @builtins.property
    @jsii.member(jsii_name="toolChoiceInput")
    def tool_choice_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice"]]], jsii.get(self, "toolChoiceInput"))

    @builtins.property
    @jsii.member(jsii_name="toolInput")
    def tool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool"]]], jsii.get(self, "toolInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e20067b9e209b64eb99836093e77497f2204ecf5fdfcc2ee1e8635da84e22f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool",
    jsii_struct_bases=[],
    name_mapping={"cache_point": "cachePoint", "tool_spec": "toolSpec"},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool:
    def __init__(
        self,
        *,
        cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tool_spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cache_point: cache_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        :param tool_spec: tool_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool_spec BedrockagentPrompt#tool_spec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132827f04a9cbfc4792cd1e62a5a7fc05796d98c2231eca938a8e71b29c7c37b)
            check_type(argname="argument cache_point", value=cache_point, expected_type=type_hints["cache_point"])
            check_type(argname="argument tool_spec", value=tool_spec, expected_type=type_hints["tool_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_point is not None:
            self._values["cache_point"] = cache_point
        if tool_spec is not None:
            self._values["tool_spec"] = tool_spec

    @builtins.property
    def cache_point(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint"]]]:
        '''cache_point block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        '''
        result = self._values.get("cache_point")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint"]]], result)

    @builtins.property
    def tool_spec(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec"]]]:
        '''tool_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool_spec BedrockagentPrompt#tool_spec}
        '''
        result = self._values.get("tool_spec")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bee307ca85b7eeaa56ce0a5a29847ebb35d45042727a6d71dbaf67b5d6e2438)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6dff2f855f77bcc10622163d6512d2ceec2ad6f761827f899532a37ab1ff2db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f422c75b5411666183621c62dbe30c5620f36577c4ab41eea5afc7a8ec92b58)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87f62665c824ebfd110b8bed98a4ac2ed9a9f2547fd5b270a887176ed3d2f3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a36bd51d85694b22015fd7187ca3a60b45459f60dc7c7c934bbd13e8b69bbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49cdec0810fff8a8d77ac0bdc24cb2854fdfc43b422fbbc2efb34692e248dbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e9bd0fea956367aeb3e321aa61ade0134dc5935d074d1263440a7cf9c2d390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dc726eec67ba593283160fcf9a63fed6dae1d13fc7797084dcd57cc30dca2f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e9e5260d5857fd8d165f5464a018b7e85fb3dee692f32000c3236a854e5182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ffcd3b5b9ac559f210ec205b478f9972ae5670a5f29c4113d6fcb73dc064f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice",
    jsii_struct_bases=[],
    name_mapping={"any": "any", "auto": "auto", "tool": "tool"},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice:
    def __init__(
        self,
        *,
        any: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auto: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param any: any block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#any BedrockagentPrompt#any}
        :param auto: auto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#auto BedrockagentPrompt#auto}
        :param tool: tool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool BedrockagentPrompt#tool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdee216e0439011e63b156b3315e4ee7d8a00069c94b6dcf2c7d363bd7413860)
            check_type(argname="argument any", value=any, expected_type=type_hints["any"])
            check_type(argname="argument auto", value=auto, expected_type=type_hints["auto"])
            check_type(argname="argument tool", value=tool, expected_type=type_hints["tool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if any is not None:
            self._values["any"] = any
        if auto is not None:
            self._values["auto"] = auto
        if tool is not None:
            self._values["tool"] = tool

    @builtins.property
    def any(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny"]]]:
        '''any block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#any BedrockagentPrompt#any}
        '''
        result = self._values.get("any")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny"]]], result)

    @builtins.property
    def auto(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto"]]]:
        '''auto block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#auto BedrockagentPrompt#auto}
        '''
        result = self._values.get("auto")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto"]]], result)

    @builtins.property
    def tool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool"]]]:
        '''tool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#tool BedrockagentPrompt#tool}
        '''
        result = self._values.get("tool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny",
    jsii_struct_bases=[],
    name_mapping={},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e69c5059a888e44199314a3f8a9a28e36a365c4dee41e8a0f2ea33bb92b31c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15cb8c6401b9e9e202d24b7dd9606d824bba92f9618b4d2f37ff51d4a1174598)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c795e7b24c2ed5aa1200d7521e97758034edf3a052e13669f019363c153884)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a82c4a224ebf879763204a0ae5327d1fd4c4afc9920723a528cc0e5cda2ca8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26881412b0103829c0641f1714f3c0699d8a1a89af4bf93a7027a3bac53b92a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a820d89e83b6b22e27c3b1b9ca7bcfab07f3e368e8b26c94fbfa460ce1b61a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3472ee9c7d24a926925365b91904c624080226c74dc1c9c4e9c404a6130fca9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7393ade6cf2c8547279c0074465a70fc928e22a4bdf2feb7ffdb364e20610e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto",
    jsii_struct_bases=[],
    name_mapping={},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5e39c74f8e25231e44bc02e19624d6e8db42a246b7b78693f46cfc2f67a1a2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c516b3b738a8004db244dc5aab5fc8febd29c6b30215faa02a7115009fcfe16a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad0de890b93c643b200e1b0f44e11637aecdc42759726525a002c678b6f9f94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a39d6b5fa4946855974ed198fce88510d38e84b567b9ff4db3b1835a0a798f3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec9a35724b32574daf8257fd4962d29909b53aeade148fc62ed1e97b4bb15b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbcbd3cc52facd5368b31fa160ae608ef216b0e20fbdc5440fffcf348059e23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4df843b73702a652c538923574af5abc4b67c6f926922940d53877ed0a3c8fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916ee5f37cc5c6c99f733ed40899d86b6f2c7a8c86d60bf4a7833379cd610622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb786633d262aba5449518c3d6b8eb4660dc5fce8e2cd6eb75bd3292bdddc0a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af45c9b18ce22ed230746a8183b7900b6047537fc6064c24bd7338bf88c6ed5f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b88228d558e44ee0d347acfa8a702176571974d542fcd510007dfef4b18959)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d99212b4a20d64200c1688b836221451b9ec053a9742db7a7debb9c466f066f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cebf96dea49a9d12acb63ddbb348b9bccc3b4cde76c967c59d803a0037cfd74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed9175b2d39601accea3ada902f1c73fb47aa12593a7e6de69d3cf5519e18da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5de85df95fc07f022dcc58bf50ae8c33dd8d6c8ab0c8d2948e4fc6b23226d69f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAny")
    def put_any(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea48af7c5b606f017ab249299bcd22d7c9607e8061e04b66cde3070a7e69fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAny", [value]))

    @jsii.member(jsii_name="putAuto")
    def put_auto(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2d99a3a92796b332f7900b40188c41080a8813d81d057d11fc33b4f89022ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuto", [value]))

    @jsii.member(jsii_name="putTool")
    def put_tool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7843f646f65f7b8fa719de5fef1d06ba9f7bbf4e716ea69954fff44a66ea9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTool", [value]))

    @jsii.member(jsii_name="resetAny")
    def reset_any(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAny", []))

    @jsii.member(jsii_name="resetAuto")
    def reset_auto(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuto", []))

    @jsii.member(jsii_name="resetTool")
    def reset_tool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTool", []))

    @builtins.property
    @jsii.member(jsii_name="any")
    def any(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyList, jsii.get(self, "any"))

    @builtins.property
    @jsii.member(jsii_name="auto")
    def auto(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoList, jsii.get(self, "auto"))

    @builtins.property
    @jsii.member(jsii_name="tool")
    def tool(
        self,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolList", jsii.get(self, "tool"))

    @builtins.property
    @jsii.member(jsii_name="anyInput")
    def any_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]]], jsii.get(self, "anyInput"))

    @builtins.property
    @jsii.member(jsii_name="autoInput")
    def auto_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]]], jsii.get(self, "autoInput"))

    @builtins.property
    @jsii.member(jsii_name="toolInput")
    def tool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool"]]], jsii.get(self, "toolInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221881ae34be6284a56021ce3d75eb983da6da26b34cdb370cebf2aa457cfffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b75b33d48f609f80a859920a63fcb1f15731a80f07e16e07ad455a677fc9e9b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1800cb851300474641bb95747348aa2e985695fad957fece03765cb33db2fdfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54522665acfc69b5e21e10805d9ab19642230e4d727267495ef60aef570ed2f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7df0e0bfd5ee54b59d03e6cdf1cdb3ed355ce5338878cf540eab15221a9d6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74d18bfbb4ed9d6142d5e794e9f48037b8430f8f3ae9ad4f094685d8167b558d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__903d22f94989c06fb62198d14ed7b94a29d4371a15b7c866977fae41c2799a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b124fa3bceacdb05f8d02ea11005558c79b498126c84c160815f7afe0caa6516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3553ecab19cdb1bcefb9331a8a7ed9ece4fcaf13ab731263e560d059f99b3447)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1eab6884ffb6b97b2851d814c0c48ae8f53c0f66351189243a0dc2c715f1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415ebcc0c49e4321ad1d4426c105092803ad535148deb5b38fd854bd720b347e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30652406289b3026f672d6d01fc96f14552e99c2de3d6deeddcf77992561abf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ae7f84a9abd7979ff23e7a5ef42601d00f81497466683bc673b80121377ab7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c56e92c1dc6f20ae46b0f26645657723ce8d04f6ad63be1226eb45c57cdac8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b21272bda85d235e0020b75b3be0417187f4a8d65e987ee52262bf7b3fa131d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63e21c67e1156d23878a3e3a78edfce737be23d7547cc9604c416c80151006e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0b97c5bf0c9d07a8777b4c70bf42840eb660716f363f82e6a787bc1c640bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0498e3a0fe479ca196ef030756b0c15ce0caa4925161ccf3e7f410a99a4a5c48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCachePoint")
    def put_cache_point(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c487eb8ae9ec1aafdcdeb504d30ada9f5b367082c1ecd503041261b8d153cd26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCachePoint", [value]))

    @jsii.member(jsii_name="putToolSpec")
    def put_tool_spec(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19f2ad45775d34618f425124a5898cd9ebc26393e95f2dcd6715e5e5972b127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putToolSpec", [value]))

    @jsii.member(jsii_name="resetCachePoint")
    def reset_cache_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePoint", []))

    @jsii.member(jsii_name="resetToolSpec")
    def reset_tool_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToolSpec", []))

    @builtins.property
    @jsii.member(jsii_name="cachePoint")
    def cache_point(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointList, jsii.get(self, "cachePoint"))

    @builtins.property
    @jsii.member(jsii_name="toolSpec")
    def tool_spec(
        self,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecList", jsii.get(self, "toolSpec"))

    @builtins.property
    @jsii.member(jsii_name="cachePointInput")
    def cache_point_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]]], jsii.get(self, "cachePointInput"))

    @builtins.property
    @jsii.member(jsii_name="toolSpecInput")
    def tool_spec_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec"]]], jsii.get(self, "toolSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb767c3a0c0dcdba11a31fe1534268f3ad2ac1e986fbba233f0f6888660d808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "input_schema": "inputSchema",
    },
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        input_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#description BedrockagentPrompt#description}.
        :param input_schema: input_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#input_schema BedrockagentPrompt#input_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b6739ffdd73767949fd606a355af3d71021a60a26a7e74214aa9491932c31a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument input_schema", value=input_schema, expected_type=type_hints["input_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if input_schema is not None:
            self._values["input_schema"] = input_schema

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#description BedrockagentPrompt#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_schema(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema"]]]:
        '''input_schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#input_schema BedrockagentPrompt#input_schema}
        '''
        result = self._values.get("input_schema")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema",
    jsii_struct_bases=[],
    name_mapping={"json": "json"},
)
class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema:
    def __init__(self, *, json: typing.Optional[builtins.str] = None) -> None:
        '''
        :param json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#json BedrockagentPrompt#json}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc77b5ef9229a21262ddcc4e8dbb3345743371c0cddd6da417b356db21b6b5b5)
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if json is not None:
            self._values["json"] = json

    @builtins.property
    def json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#json BedrockagentPrompt#json}.'''
        result = self._values.get("json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98719572f873e249cc9d84f14b8890f2c03922256905322a2dbfca3a4460eb44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28be0e999605e14d2c63459caab4235b076d6eed51516f6dcd356fa5fa16b606)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbff20c919454a60052e9ecc409810ac82163ebda49397f94abbb4eeb9f8928a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbb8eef9a26fa56b873df1a4e19f60c64f3eed762bf49d36fac072690d1301fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2695e8a254efd54733740f2e16a1f626f86f214178d544e7c7cc942e7a15122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f12440b7df0ed2ea1ff1a6ed8f74813533ba91394f9d18caa15bcb49a709e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7779f762266f17896f0cc553d09b0f9e14e1a55cb7710bc04de23e49adc6d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "json"))

    @json.setter
    def json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12497ba0ab381e0388012f538789cc895668942915191b5d2bf6bb684aa78a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "json", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__919dccd59d94fc3ddcb69d868bb75b4f6f28372571f233bb0453c7bb290d7210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b72610ba80fb5fbab9ee2321c28a46fc4d7636235fc83e185f4c6055d4a0eca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4543284be4ebcf3d1e71e25421a1146576652a2ec591008e4538a9c7c4c28e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7a6e08d7b64ea4c24f73ed7d43bc5566f2e171246e490ec2938efe52612ec9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4db78ee8e213d19da091f495fb72fb7b3ada8c2e1a5e691384eec9e4a7dbbff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77234c675761b7cd03315a14ba817e1aec912f49d137053b8bd95495a80d6aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1cac655595e9aaea945db31a2072431b7ef51465f62834387512cce90404af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083c560b2ac4855e7e269bfe9d791c5689b4408d665492e30a9cbe59382fd7ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInputSchema")
    def put_input_schema(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fac780d723e9fd9307da529c90db61c972af0134bed0a14c75765758dec8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputSchema", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetInputSchema")
    def reset_input_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputSchema", []))

    @builtins.property
    @jsii.member(jsii_name="inputSchema")
    def input_schema(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaList, jsii.get(self, "inputSchema"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputSchemaInput")
    def input_schema_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]]], jsii.get(self, "inputSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbac754b8e7ffe8313efcc3f24760ab8c5b901ed0834b19533c1e7ecaf199ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26cad1d69fed45ce267d95e5986a7348e77acd9c5fdd0907777c2a2df2d07d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c81116ec3e4559e649de2fee6d6a5edf508a7951be2d74ec103699b1b0c738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__315050113583c4cbadcc7d237570baf1420722a2a5497a816a3e2b1f68e9e597)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fc178809cb365fa1878e7669a5deb1f05174ba9432f6c5ffa716343b6283f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fed3942f50482b761b0354d20a82c81516106e946e78e16989b8350fcc3d28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e235852c34588270c2dc5a659dfe8870ffeffead2a1f06b1db99073fcf2eef1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f42fbb48b925d981075a4d680c8f9fee0b8adf2816c098f8bca7b8067e0cd5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc2cfa77ce594f43b405ec51ba204ea242a171138d3889e129c20b8e1340c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a973c19bf7672bd0059cc030c41563fbab99f08245c65c7dd13c0a79dd232489)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putChat")
    def put_chat(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChat, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e884769afaf8bffa89ccc1c5ebee5aa8a766127e01185d4af96f6557d17191e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putChat", [value]))

    @jsii.member(jsii_name="putText")
    def put_text(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationText", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a289ad1421af1ccace2b9fba89b0bf1fb8dbbccfc5f2e69bc9f7da10ba09b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @jsii.member(jsii_name="resetChat")
    def reset_chat(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChat", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="chat")
    def chat(self) -> BedrockagentPromptVariantTemplateConfigurationChatList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationChatList, jsii.get(self, "chat"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> "BedrockagentPromptVariantTemplateConfigurationTextList":
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationTextList", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="chatInput")
    def chat_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChat]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChat]]], jsii.get(self, "chatInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationText"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationText"]]], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb27ad89881884fd37a8b872e45e7bf32d899c60d888864e89574fba97e7a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationText",
    jsii_struct_bases=[],
    name_mapping={
        "text": "text",
        "cache_point": "cachePoint",
        "input_variable": "inputVariable",
    },
)
class BedrockagentPromptVariantTemplateConfigurationText:
    def __init__(
        self,
        *,
        text: builtins.str,
        cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationTextCachePoint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        input_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentPromptVariantTemplateConfigurationTextInputVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}.
        :param cache_point: cache_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        :param input_variable: input_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#input_variable BedrockagentPrompt#input_variable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77148f6ecc2cc4f63a8a90764d3a41f3d6f8685528f16c8c3b2757fc7272705c)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument cache_point", value=cache_point, expected_type=type_hints["cache_point"])
            check_type(argname="argument input_variable", value=input_variable, expected_type=type_hints["input_variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
        }
        if cache_point is not None:
            self._values["cache_point"] = cache_point
        if input_variable is not None:
            self._values["input_variable"] = input_variable

    @builtins.property
    def text(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#text BedrockagentPrompt#text}.'''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cache_point(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationTextCachePoint"]]]:
        '''cache_point block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#cache_point BedrockagentPrompt#cache_point}
        '''
        result = self._values.get("cache_point")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationTextCachePoint"]]], result)

    @builtins.property
    def input_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationTextInputVariable"]]]:
        '''input_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#input_variable BedrockagentPrompt#input_variable}
        '''
        result = self._values.get("input_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentPromptVariantTemplateConfigurationTextInputVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextCachePoint",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class BedrockagentPromptVariantTemplateConfigurationTextCachePoint:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197b1bab9644bda89aeae91c70bf12afdde0f4a73dcea3ab5ef1d70c4c7f1cec)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#type BedrockagentPrompt#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationTextCachePoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationTextCachePointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextCachePointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fbc180ef7eedc23ef72e588dabcdfb220dfae4751523be1682d6d7c06243c61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationTextCachePointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016124e230d6d59a3824281f55ae71ff6b382ebe7c78f361a8edcdf0cffa1c32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationTextCachePointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6685b13cd9ad4bc6f6cdb7cc285e754e8feb48379575fc1360f8a5a68fce7491)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e94bdbc9ebe75b1ecfa44d003a40d16258c615556b779c7216a6d335e6baba9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac4c78d9b704d2ce6310dbd3ea8f43a896149f10a2d190ef512897b0db77785a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextCachePoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextCachePoint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e2f3e38ade562f482393a40873b85573627770a2dce810e49c1ed644d6afc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationTextCachePointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextCachePointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1148d52684e4826fc4cba39e0c9b995fa0ac4eda508af11ef6a0d0ab07cd3340)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d624c34427003fdb838f6e11acff7bd99fa7a9832768c06ef17ead7724212f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextCachePoint]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextCachePoint]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextCachePoint]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377411c40bc796a16048657eecc2ae0dca61d7754a106e3e91f509243b21fda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextInputVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class BedrockagentPromptVariantTemplateConfigurationTextInputVariable:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7ad64535534ed02948b39a4579c2d9fb6cee88b90de908ccbc66103bfb92ae)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/bedrockagent_prompt#name BedrockagentPrompt#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentPromptVariantTemplateConfigurationTextInputVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentPromptVariantTemplateConfigurationTextInputVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextInputVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ae865070f55effebecb0ab1ab7ec70d64a496228223cc7a78273df7f627d777)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationTextInputVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3f0db75515e7ff837d605d8bb50c59978abe98e52451c39063a699b5da0d00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationTextInputVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea15c036f35fc24de9d334a9255edc5af4222f0a90840f1e9f3db38319fa5b42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13cc81e8f3457c12e36075a102085e54354509553b5dc7d053cc67f7db72974b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceb23ff5e55745dd114043b9ae214c403261445509652a5cc8a30cabab65c0a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextInputVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextInputVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextInputVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bacbccaa9c3b0ca136dd7de4319739d2952d0e3e478588c82d44f1cf2e5bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationTextInputVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextInputVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dd1118d2f329add290635b0ad156547d6c0a74f8675b1fbc0dd60473b23e29a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29950d12464ff6d557029555d337d3b36b56cd4cc8f7dceffe537f52abadc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextInputVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextInputVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextInputVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4f3f8ca2783df8219c1c688e4fef80438720883701c97aa9a8ba95b0f04696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationTextList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0a45cea8b7ecd985d405e5ea3e15688108d7ed123af0c66514146a71499908)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentPromptVariantTemplateConfigurationTextOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8f8107482682d0ff831325718aa13d4f8109d29346aa71f3eeaf6902d50752)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentPromptVariantTemplateConfigurationTextOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f26a9149e94a081ddb9481241ed3f4ef0e2fd2b5c925834585625489514ce4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b855da5421530e6de16c39a2a862b48965b9dfc20d50fbf1c5808fed9b1fd042)
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
            type_hints = typing.get_type_hints(_typecheckingstub__926489b52af64b61a870d1a56664a1238dbd28e040ac32270de114c2c5f3ee68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationText]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationText]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce03fd294281bf6bebc6c52a2efcfad181dbb8395758b47ec3cb3c1cc37a376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentPromptVariantTemplateConfigurationTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentPrompt.BedrockagentPromptVariantTemplateConfigurationTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8078c9f4851348cf6b66f6e936c651330e0511c091b019e4d8f208cff5d1339)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCachePoint")
    def put_cache_point(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationTextCachePoint, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b358e7170488ca1dc30e9fdf53d8d316b59b20d27443d6fb9fa2615568fa424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCachePoint", [value]))

    @jsii.member(jsii_name="putInputVariable")
    def put_input_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationTextInputVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4babaa04f7255d7e86106989ffcdc11914c0e21447bf5a2e1cdc0f85e99be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputVariable", [value]))

    @jsii.member(jsii_name="resetCachePoint")
    def reset_cache_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePoint", []))

    @jsii.member(jsii_name="resetInputVariable")
    def reset_input_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputVariable", []))

    @builtins.property
    @jsii.member(jsii_name="cachePoint")
    def cache_point(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationTextCachePointList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationTextCachePointList, jsii.get(self, "cachePoint"))

    @builtins.property
    @jsii.member(jsii_name="inputVariable")
    def input_variable(
        self,
    ) -> BedrockagentPromptVariantTemplateConfigurationTextInputVariableList:
        return typing.cast(BedrockagentPromptVariantTemplateConfigurationTextInputVariableList, jsii.get(self, "inputVariable"))

    @builtins.property
    @jsii.member(jsii_name="cachePointInput")
    def cache_point_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextCachePoint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextCachePoint]]], jsii.get(self, "cachePointInput"))

    @builtins.property
    @jsii.member(jsii_name="inputVariableInput")
    def input_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextInputVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextInputVariable]]], jsii.get(self, "inputVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6fbcdfead8aa58346dcada4f9774a2347c99f3742944d3225167fb4821e999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationText]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationText]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationText]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8c491a4a8c880827bec6272c921e432bcceddd35f41ee89cbe08b2b94d4682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BedrockagentPrompt",
    "BedrockagentPromptConfig",
    "BedrockagentPromptVariant",
    "BedrockagentPromptVariantGenAiResource",
    "BedrockagentPromptVariantGenAiResourceAgent",
    "BedrockagentPromptVariantGenAiResourceAgentList",
    "BedrockagentPromptVariantGenAiResourceAgentOutputReference",
    "BedrockagentPromptVariantGenAiResourceList",
    "BedrockagentPromptVariantGenAiResourceOutputReference",
    "BedrockagentPromptVariantInferenceConfiguration",
    "BedrockagentPromptVariantInferenceConfigurationList",
    "BedrockagentPromptVariantInferenceConfigurationOutputReference",
    "BedrockagentPromptVariantInferenceConfigurationText",
    "BedrockagentPromptVariantInferenceConfigurationTextList",
    "BedrockagentPromptVariantInferenceConfigurationTextOutputReference",
    "BedrockagentPromptVariantList",
    "BedrockagentPromptVariantMetadata",
    "BedrockagentPromptVariantMetadataList",
    "BedrockagentPromptVariantMetadataOutputReference",
    "BedrockagentPromptVariantOutputReference",
    "BedrockagentPromptVariantTemplateConfiguration",
    "BedrockagentPromptVariantTemplateConfigurationChat",
    "BedrockagentPromptVariantTemplateConfigurationChatInputVariable",
    "BedrockagentPromptVariantTemplateConfigurationChatInputVariableList",
    "BedrockagentPromptVariantTemplateConfigurationChatInputVariableOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatList",
    "BedrockagentPromptVariantTemplateConfigurationChatMessage",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageContent",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointList",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePointOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageContentList",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageContentOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageList",
    "BedrockagentPromptVariantTemplateConfigurationChatMessageOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatSystem",
    "BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint",
    "BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointList",
    "BedrockagentPromptVariantTemplateConfigurationChatSystemCachePointOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatSystemList",
    "BedrockagentPromptVariantTemplateConfigurationChatSystemOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePointOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAnyOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAutoOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceToolOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchemaOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecList",
    "BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationList",
    "BedrockagentPromptVariantTemplateConfigurationOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationText",
    "BedrockagentPromptVariantTemplateConfigurationTextCachePoint",
    "BedrockagentPromptVariantTemplateConfigurationTextCachePointList",
    "BedrockagentPromptVariantTemplateConfigurationTextCachePointOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationTextInputVariable",
    "BedrockagentPromptVariantTemplateConfigurationTextInputVariableList",
    "BedrockagentPromptVariantTemplateConfigurationTextInputVariableOutputReference",
    "BedrockagentPromptVariantTemplateConfigurationTextList",
    "BedrockagentPromptVariantTemplateConfigurationTextOutputReference",
]

publication.publish()

def _typecheckingstub__2ba34194330bd0e4bbe192694d544e555f049d349b2210bd616fd089192f2545(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    customer_encryption_key_arn: typing.Optional[builtins.str] = None,
    default_variant: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariant, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__b39ab4b3c202783b9e7180a1899007d3a6bdf7582790223bff7b40a113fdf6bd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45cbb043d08cd52a051446be3cb4a661e482482b5bfb9ff837bedf84968eada(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariant, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65ead866712144c45ecdf7241aaa1487564ffdc761add9e8d298b18d9198063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4679ca035c20903a0d265ede3b2d5cab3ea5fda1bc5d8294cc0992e22bdd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcae81fb0d1c0476e7830b2b6daf84b774b23f9e38d5ac89fae3e0d5d5b82017(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75865402162fe8ff86822bfbc5cc3630e6c43eb658638c0737ddd6f3d22162b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7f5e9c46732cdf58c92adbe25dc1cec9a9c8c8c41ea3db8a3ccda17636901c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8f91ec64560b0fb052ee997cc8561ecec560635e3119a01d2ad9c1993d7ee6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec42db6c4c8848e5e937a9e31cb42221c0e63ba0b63736f45e8e868a3870973(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    customer_encryption_key_arn: typing.Optional[builtins.str] = None,
    default_variant: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variant: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariant, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad98a70424ab275d5e684a1414bd5638bf007508b55be168b3a4d8a5dfd129c(
    *,
    name: builtins.str,
    template_type: builtins.str,
    additional_model_request_fields: typing.Optional[builtins.str] = None,
    gen_ai_resource: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantGenAiResource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inference_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantInferenceConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantMetadata, typing.Dict[builtins.str, typing.Any]]]]] = None,
    model_id: typing.Optional[builtins.str] = None,
    template_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a8c23ed677f0d22b56914f08e91974825ac19e02684f8d4802344a5e79ff1f(
    *,
    agent: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantGenAiResourceAgent, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d63f3c994f49299005fafbbda05c3cb21786960250edf96f3e3a73b649c5a9(
    *,
    agent_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b814a7ef7ccb08974b004fc6de0c004aedf5f01bcdc866a5f1ecaa5b54e9ef3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafdd6dbaebf7f8493213a0fa26bd59cc151500fa28ec13e2a64227ac7cc7bc7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a7d3a6773da8ddaab9ca0a7c03fb0777d81b705414566310bffdd0ab019765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35b466e5ae34d53cde97d7a50961a995da71963abf7e0409d3fb867bda35d8a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ab534d70c4da5f3268af87ac66db467b9a7313e7cec3b726a4f366a8ec6df2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf7bf1d5ae8efc753402bc487066b40a63c8772dfdb42539dcf68ed11069615(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResourceAgent]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ae40ff6c5833f5d09aeabc983e454bf2fc4ec30b5e62d4c304484b3f3579d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea9e2e290a829631c2d738d9bd4672a14ba0fbcf1bda84366abbb5557f2d201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b041c386a1efd27e9b4e32a0e196616a279d7a879938f9c4fc06816b08133b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResourceAgent]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66426db7b27197a6b54f58ff173b09bc113ab74c6e2c667c029758033e8b56ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c735c101380e00d6434d0ea218ed4941299d7375c45068512a20533c5c15f9d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a469e53014c908817dac4a45e11a6fdc4aa1ed56e737170812595607ccf36b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15dc855678f8457d55b4492b3981d92e564685635e757ff32c5f6e9770404d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47ac05a145a006eefc4c25c20b65180b9601220fb32bc550c0fa93fdfbc2aa2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea5f0e00e7084e53f9d5586661764e3bd1731378751fe190c3e0e09a1c82a1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantGenAiResource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2249dfaa8d719503e1a958205b044718c4149f055b8218c2a73f09aca41efde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edc09758d12359951522bc7d4f008e3a7ccd47272eda2bb74c702ec7299d441(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantGenAiResourceAgent, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2e5bf34544cfe2c317b8635e480a0ce7109af7c065c1d450bc3261addaf979(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantGenAiResource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b5f39e3d2974ff9e58a549fce8ac7584adaca13145e25e28634ad3284535e5(
    *,
    text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantInferenceConfigurationText, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df98c8b472056e8d4e5f0c2d1c9b558c378092bf638bcec95a2ab02ad97af7dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18000becc0e2dc5467373d2cf01a6f4e71ceebdb680f0cdd9827a33f28a4e93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea8f003adfc97d46f1afb300f93924985302c230c1c3fcef5fe3edd11741672(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad60d6e4baeb7cf21cec8f045c0ec90183bde3a725fb7365c9a0eb0882c47371(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703b95023211803ba2d9964e224847ffbc671bc789f91794f112ec57806ee975(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b066bd5ee9af142a7cd5333338757dcf523e08a65e3339988d498b6d23ebaf3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ff2ad2c7894da87565d3a35558de050783d7ef56fc8764d942dae7c9caecc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc67da7c193a6ec109cd3858fe83a34c29737c2d961d30319899c5e56ccf250(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantInferenceConfigurationText, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649c61fe2ddd0976006ad67f62abe646cc6b251917067b5fbd1be79142c81f45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef9d4ef42161a2745a2a05d7aa7ca3fb742112606b7b5f1ff77a5b8af8e98e6(
    *,
    max_tokens: typing.Optional[jsii.Number] = None,
    stop_sequences: typing.Optional[typing.Sequence[builtins.str]] = None,
    temperature: typing.Optional[jsii.Number] = None,
    top_p: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1b893aec81d34cf31a8c8e16039539df9307208985fda5b5dca26c7fa37fdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db2bca54e7cc2ae55f284d923d037f5a4598a934025c153d8ce026a8f4cd46e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee7e5b1cadf061ff1b308e43f78fe62a75ec5812a6e41eeac7c28bc248fea27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834e74b4c8b6c1986a1c161db7d79aaf5b33e29fca0f1ea1416bc52b42d477ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f82827480e747a4302305f827ba221caf597b5484d27a0a1eea297a9ce43890(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bc62aeb8513d62feaef424481cab3a19a011a61ffeff73e1a7ad79ccc5ecc7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantInferenceConfigurationText]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644bbc7903cfc9304672624da4da8d26167c856d88b582a2ab020c2049f37b73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69e1f2cea1fee291b53d3026126b63390c8a6bc5a2d7e2a9ccc53d10bbc93f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa06d34bf6eb5ca141fa6e90f3c8f9972b12f0fd13b888d5aa2ea1af06572176(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad7485843df595d8ddbf4c1f66d468c3407cff201b2435dc8cb6957db6ed663(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dddb59b900ad6ef90b20c215d4e9e293caf83b2698d5ba849d738b6a35f8440(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbf93943a7da61707aa94749c0be55a515037b1db2a2b709601e138d1017723(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantInferenceConfigurationText]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd70288b9aca7ae69f09f8e28915702e208c6d33df3b4cf18f4439a41c89306e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a69744ed909e068ca30f58872f4361b9062e0b523b3e8a2ac62b2428ece2f8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f26746d855aee716dd700b7c8795e4fc6d995139d810133dec649ab0fb41bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31747ccd51d51aa21f926e5d4ed0fa5bf2877938c6dd8eed693f133ffe98dbad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35758bd366849a252825dea7b6abe8cc9ac9cd9a331bd8b38af60f32e3bd728c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4721f0f051d924d1d7c0cf656e314885360e721615e73e7808b254f74b7c797(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariant]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d34764fd1e65eb50c241750ecb1f58008694e427a3ffc77730a897cc2850417(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd0acd1d6de481c724a2c520a1a398f33721e9f6b11794a33233ada0023ab79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58930050641f5e6b04423d6123e1015cbce46deadf92af4ee7d102de9872b30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05d5105acba7bcd3fe884932bc147e2ac5d8f2d5069e6c8a58039a2a4b0c408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34540f7eb3c82d0c29d8d5a89f3ed76f3cfa91db28b028d7ba149107b43dbcab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9385e025f395bdf2fe50f100d08554b6d36556dbbaf258a05e36927effee1da2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785d88fe248744db47e1b9dc4e692e0405a91ec80de79e1f38e363f96c8ad875(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantMetadata]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd18505f78292293e1fc26f7c043c3021ade8c7a7f1831a345de90356d311b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897a59a6ccce482a52a9efbcd5ebab0c1a91de9f90e46e3012ef3b4e6736387e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074dd90f3ee522b9b7fc42a60ef580ee6b1c1abb66e63a3aac5677bc8c9aa16b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8c291ad5db6b6f6c438cbfcada4147c0cfaba7e42e07bb42fa88b1981ed718(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantMetadata]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bac6aaf4e2e0a8bbd3d4064d9c981c01c06253c127ac8e18d687077f2f58e59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fa84eb4ef6b313471997079d09d7e56b78075679950346bc7c38aa4aa774cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantGenAiResource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73df22b7bfddb9ae696f5a2f7a0f4f67984eb6a981e0d245b233bb0a7a424802(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantInferenceConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6510d55155e1708d070b599931cc7a2d180083f35edf0666d49fbc425cbc05aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantMetadata, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353c5d56e59fb63ca6e0afb94718f30b0e3cb3255c60f0e6cbbfb03fc8e3c330(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7be99120932789a3fd78be4c00ecbcec791c116c613de56d299d4e622ddf9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acc64c385728c4549ad308d96f9a986516e00e1b2e75b7befa578e19413fdbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7c684c4810552ac987299814d1d2af41964c5a580babe530c57315420b30a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0182213082308d4eacdd4aefa248e63d62c2e49f06aa6837633ea95715dab1d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f66480491bd7e4beee9b2f045392a78f7ebd97a44def09cc526676e67ca8d6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariant]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25216f596a10d7af3a469ee20cc6728b25e3392e442e9fbb853bf9f4f683fb5(
    *,
    chat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationText, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f9c3ee2548cb4a0be20837b82f45ee2c5b3805a58577f0e2d34c67defc37f7(
    *,
    input_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatInputVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    message: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    system_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatSystem, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tool_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283c319aeeedc1dbc477af948c66b9652bde09484b484c6078ac8915f5e39a88(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f02fa69fe7284d9a78bde90c2e9b2f937ac8567b8405343135216319c8315c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f237b918828fc2932ae3e5a84b18351a5077deb3c324472a8a2bde869c9ccd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b37671f5e25c3b73fc6a0402c711acb00334f6a45d14935561b589a5c2d8a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4753cda7b510a1c2bc7181d5ff6797f788eb6308b458e06003076824a6afe9ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab1d1ded0d04a350f4ac6d331442bebe1618f2e79d37f311e16d4321b0ac90d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0b644e6d35dbdab44fe75efa5d4856aed29778407216d413db6e16be9823e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatInputVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567c93a2568c21ecbf48ec3a280cba430f1d98efbb7f2f43dc4a0380869ae425(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb7c454672fd044c10a40804bf12803125b5b356236b191fa8cbd51c0d90bcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce075c742e8a107713c265fb81c8bdfade4de94d6cefa446d7171788c61af4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatInputVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3185be2b6b7f2214c2bf29c5c6e432b238b814f1964145e0d9afe3a3d3ea018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa74605d236c0b0955c8bd452503c9cb2d3c0bff7cbbb73d7966748f2cdf588(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1b72aa0f715289883481a69923c3596e1f9a4eb4c88cb4c02ea524888f9397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cb1cd430948a995f0bae4ee38511cfb22201a8aaaab1f9e4dae2da476e8d94(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb41221681e1d41272480ec75f22747d1cabcc2db3e4493bee8636840ba6f7d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f55d220fb006249a1786bc85d0f69c730bfabe452fd96a436a6560940b6d53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChat]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e782bde952cdaf114ec26e07bf821071275a68909c118a8cae4572d6403963(
    *,
    role: builtins.str,
    content: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessageContent, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423a98636b8b7956db22c29cefdc52d8447c88e39846b7bb5d8e3af9b3a662d1(
    *,
    cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713bcbf03f3770d03ff1d2ea1bf8f62800101f15e5b0db31d81f14d1829268b9(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0280f9d2b155483fd3149b15d4a4c09096d223a9fa9a2ad93a7624afd8bc13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00308cc585b094de9e70dcb82a22e819f36ae6c3317d1f496059bd2ab195eff8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14b2445e7aec93a34ff53f2ea51a650bb690a7552596856bbf38fe8cd29f41f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b4f8d3c346480b83287294722571314299ac8207df4ac2cc4129e33427d3c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d04679c900e45f8d4066af66edaae8cf82b04738e5bb835550133decc59801(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa39c745a0cf371e1bbf33b171137e363ec8579be2ba2a3d274f73c3ffe7c0d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3f09e0066e1d651ce7c2ed80420f310bc38acefddc8e1f4d97afbf74503ab6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c3f82faaca2a7172d681b907a657b3413f57a9412be925378030028ffb3f16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbac14e310923c5795af022eb1924656ae666bdd2a295004918578d7ad3d9ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529ab5455ae1f0ded7dedd29ce64ac06f01dcaa7d628ff6d1099b958f9e955ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c556f4ca02cfacb5087408cf4ff91e25d879f9e1439db475378bcfb86346a1ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd6dcef4abcaaf55e90dcac80a218bbd2b4c0d58e2d8e9c023b1fa186149eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6f4810cb3875663ee7ef8f9329531f53be3d22d30b570cc220fb1fcef48abf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adc3b34c421a46d3999bac2e8554cd86efcfa00ef4ec172bb7ecf010f14ed8a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bf4455c87fbd1595328fd917e86cd085d2d55c0fa85f8a92d85edab8448a29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessageContent]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56229a21e38a555602d2592fb4bdad846d4b3beeb18061cf2c1c06d64934ea1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15d1e2d210a4d7cedd9a272538505228d8243f3210c56d165285922cac1727e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessageContentCachePoint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e21820b0d53ac7920cb02abf7267adcea7fc8945814198073787bd2d078d0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025f1e3e6a76eddf94236f2dbee58e04785b7ddb2d137806dc98a761d8192f3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessageContent]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c289b92b807971ee35eeb65ca5dd3c4f93110f9ad3537e0207709e90473fc32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cedb1e4e052718bcbf58e88cf1ba4c63527b8082e7f3b2fbfea59a263dc426e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46e59bdd3014a07b149c64ce20aa321edbe8fac80eb80ba7cd13bdded334f4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778d7f856ef8a2fc5f3ecb6075b55ff46d0a7ee229dec1ec71215154137e1caa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a265e45e91ca9366b06bf8272162af44b5940477449f2555dfd9ca370950a0f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79cbf140bede2483bb36bbb4685fda4861f15558b9f7ef8381ddf708052638f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1efc3ea92a2afa0b33106bf62e69a4d4156dd97f5e4e5ab0bdcf826da413ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48f343a7abae27c150d6e563c68a4879f18427f21b30a74472c9f06f15cae54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessageContent, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3d0d7e0489182a8db8961f8d8c0128119ab076ab2214933951687aa3956f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32897f47139547cd2d836125a04d4ce4c6e18f4ce204d89d29fe669d3d64bc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69eb3af9f3c3f269a4a6c32497f5e5cb88eea409650260fdd4053619220706b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6dff4a63f57bb885e42d73e06b3c62372aaa1a86ca3c8ff20f38898e7d9983b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatInputVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e3bfd9d87663a3a30972ebdd82b77271bd9a3c43f9f37add2783aef95e5756(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b927c7e511a03a8845eec47bee4d6b10389a367c409b13bb3fafbf6bab5b4a8e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatSystem, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8898e797ff65f5b75afad4ab9556129dd01dc390bb837e5c2c594e430d4b202b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4022dd64a0b89bacf1c7e3d3da664455b981f8ac025c7299ff9f4ff65471176a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChat]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2998028f32766775d6d53c0bff9b61330ebe7863d9a265028359bbf1baa8b14e(
    *,
    cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afcd12fe5183c705958aaf6daa05e27f035c1fe7ae961d774978f23023c0fb0(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a027dd9ab149b472d1c65f332683b995cd66772a1edfb0a0bdd5e292338eb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a4ce1c3b92e8bac4673c022acfda3a568a873f2bdd4ae2a6cf2153d87eb7df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c80da34159b496bda579fa8d3010fe1fddbcc04f6d846778b7af3b7d6f8ebe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be46b7192023830e0bbeb03d6800d15f171e2796de8f7a203f774126b2535a5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b1149a2afb2f347da77bb8840fc364978ae2e5830a2bdfa9a893c504f02c0e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d81cf0a529bb75570932308b2137ce66406c394310b208200899dd716a6dc9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427102db16aa33ee1c9fbdfaeab5a36c314c4aa461e6d95bc013deea96321755(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465f996152d1cf041c604157934fca9355f15e2a72e455a8d1ff3ecbf5ab5710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd29aa7f00cf135501aec6dccd1b913f90a58676d05793b7b792228fd92b0e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05fb177d3982fb798c1ef6acf31aebb29a23a43f4165e58aefabc821edbc84d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b43fff10af12c9d450922f0e07e648be185fd7b17810c10f041a75669aad0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051775a26b35c4785cd6f05016fed750637920e8af052be01517471fe5246c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be81671e804aece8953757800d324d98bdf3a0c96d62c50e99fc3b5c1798087(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d520f9b9d83234d90fbc63236e1ab901d881765fff22aae117e7d8e3de230188(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9df1d7fd0c613494c9e5578f73dad6df56a57a40156f2abfabd3efee2430d68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatSystem]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a003ef962186c770c854585fdea5e907376b0db1f867948bde6cbcd47c0a18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225ad6e9c23b7fad3dcbbdf98d79b4a3ce0a0ef614a77aa1a12d53970b0c11a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatSystemCachePoint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4164042e9f1ee1c50c90a66c974a7e3a2cfc166c0a743d312a572d3e7d5002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98928c9d297cc840280af891172947a7bae8c77986780e219e0735a0a5679198(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatSystem]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9592704dbfc5b45a46114711aa0f41df7e572fc42315d4a4b96106bc392b2e(
    *,
    tool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tool_choice: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c34ae9d3c1ded6e2f6da213e0798cbaf08b328130a26cdbdcd10e9b3184d02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40ac1f3bd89589aba226139a6b7258d9225e9e88b0c3147d83580a55a99b07e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5009d7a3c7a19034295ad30e5739bb0a723a3cb982175eef5a3d5608d2cf94c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5598e97e7a1ef785f6561cd07e0ed92582b7802e71cfc66ab058145aa285849(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7743cc25e54ce9b3043bb8b0e6ecd47d9695e65b95feb565dcafebc97e3d66bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55c120fa1036d188e899358e93ddcf5775faa8f632475b8a50236b0ca82f1d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdf996ea9ca7e52e5b403912a355afb4774077c20ee62e38a15e16c488a9f84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8e9c82b66eeaa580c847baae7087d6636da228e1f03c43efa5f65497d7be6c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b57cdf7f2edb248dc0a57cc9213359837baa4c23e6b48ea1ffc7261e2d1139(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e20067b9e209b64eb99836093e77497f2204ecf5fdfcc2ee1e8635da84e22f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132827f04a9cbfc4792cd1e62a5a7fc05796d98c2231eca938a8e71b29c7c37b(
    *,
    cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tool_spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bee307ca85b7eeaa56ce0a5a29847ebb35d45042727a6d71dbaf67b5d6e2438(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dff2f855f77bcc10622163d6512d2ceec2ad6f761827f899532a37ab1ff2db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f422c75b5411666183621c62dbe30c5620f36577c4ab41eea5afc7a8ec92b58(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87f62665c824ebfd110b8bed98a4ac2ed9a9f2547fd5b270a887176ed3d2f3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a36bd51d85694b22015fd7187ca3a60b45459f60dc7c7c934bbd13e8b69bbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cdec0810fff8a8d77ac0bdc24cb2854fdfc43b422fbbc2efb34692e248dbed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e9bd0fea956367aeb3e321aa61ade0134dc5935d074d1263440a7cf9c2d390(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc726eec67ba593283160fcf9a63fed6dae1d13fc7797084dcd57cc30dca2f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e9e5260d5857fd8d165f5464a018b7e85fb3dee692f32000c3236a854e5182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ffcd3b5b9ac559f210ec205b478f9972ae5670a5f29c4113d6fcb73dc064f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdee216e0439011e63b156b3315e4ee7d8a00069c94b6dcf2c7d363bd7413860(
    *,
    any: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auto: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e69c5059a888e44199314a3f8a9a28e36a365c4dee41e8a0f2ea33bb92b31c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cb8c6401b9e9e202d24b7dd9606d824bba92f9618b4d2f37ff51d4a1174598(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c795e7b24c2ed5aa1200d7521e97758034edf3a052e13669f019363c153884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a82c4a224ebf879763204a0ae5327d1fd4c4afc9920723a528cc0e5cda2ca8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26881412b0103829c0641f1714f3c0699d8a1a89af4bf93a7027a3bac53b92a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a820d89e83b6b22e27c3b1b9ca7bcfab07f3e368e8b26c94fbfa460ce1b61a5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3472ee9c7d24a926925365b91904c624080226c74dc1c9c4e9c404a6130fca9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7393ade6cf2c8547279c0074465a70fc928e22a4bdf2feb7ffdb364e20610e47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e39c74f8e25231e44bc02e19624d6e8db42a246b7b78693f46cfc2f67a1a2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c516b3b738a8004db244dc5aab5fc8febd29c6b30215faa02a7115009fcfe16a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad0de890b93c643b200e1b0f44e11637aecdc42759726525a002c678b6f9f94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39d6b5fa4946855974ed198fce88510d38e84b567b9ff4db3b1835a0a798f3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9a35724b32574daf8257fd4962d29909b53aeade148fc62ed1e97b4bb15b4d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbcbd3cc52facd5368b31fa160ae608ef216b0e20fbdc5440fffcf348059e23e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4df843b73702a652c538923574af5abc4b67c6f926922940d53877ed0a3c8fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916ee5f37cc5c6c99f733ed40899d86b6f2c7a8c86d60bf4a7833379cd610622(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb786633d262aba5449518c3d6b8eb4660dc5fce8e2cd6eb75bd3292bdddc0a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af45c9b18ce22ed230746a8183b7900b6047537fc6064c24bd7338bf88c6ed5f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b88228d558e44ee0d347acfa8a702176571974d542fcd510007dfef4b18959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99212b4a20d64200c1688b836221451b9ec053a9742db7a7debb9c466f066f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cebf96dea49a9d12acb63ddbb348b9bccc3b4cde76c967c59d803a0037cfd74(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed9175b2d39601accea3ada902f1c73fb47aa12593a7e6de69d3cf5519e18da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de85df95fc07f022dcc58bf50ae8c33dd8d6c8ab0c8d2948e4fc6b23226d69f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea48af7c5b606f017ab249299bcd22d7c9607e8061e04b66cde3070a7e69fd2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAny, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2d99a3a92796b332f7900b40188c41080a8813d81d057d11fc33b4f89022ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceAuto, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7843f646f65f7b8fa719de5fef1d06ba9f7bbf4e716ea69954fff44a66ea9c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221881ae34be6284a56021ce3d75eb983da6da26b34cdb370cebf2aa457cfffb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoice]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b75b33d48f609f80a859920a63fcb1f15731a80f07e16e07ad455a677fc9e9b(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1800cb851300474641bb95747348aa2e985695fad957fece03765cb33db2fdfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54522665acfc69b5e21e10805d9ab19642230e4d727267495ef60aef570ed2f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7df0e0bfd5ee54b59d03e6cdf1cdb3ed355ce5338878cf540eab15221a9d6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d18bfbb4ed9d6142d5e794e9f48037b8430f8f3ae9ad4f094685d8167b558d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903d22f94989c06fb62198d14ed7b94a29d4371a15b7c866977fae41c2799a86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b124fa3bceacdb05f8d02ea11005558c79b498126c84c160815f7afe0caa6516(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3553ecab19cdb1bcefb9331a8a7ed9ece4fcaf13ab731263e560d059f99b3447(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1eab6884ffb6b97b2851d814c0c48ae8f53c0f66351189243a0dc2c715f1c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415ebcc0c49e4321ad1d4426c105092803ad535148deb5b38fd854bd720b347e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolChoiceTool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30652406289b3026f672d6d01fc96f14552e99c2de3d6deeddcf77992561abf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ae7f84a9abd7979ff23e7a5ef42601d00f81497466683bc673b80121377ab7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c56e92c1dc6f20ae46b0f26645657723ce8d04f6ad63be1226eb45c57cdac8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b21272bda85d235e0020b75b3be0417187f4a8d65e987ee52262bf7b3fa131d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e21c67e1156d23878a3e3a78edfce737be23d7547cc9604c416c80151006e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0b97c5bf0c9d07a8777b4c70bf42840eb660716f363f82e6a787bc1c640bfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0498e3a0fe479ca196ef030756b0c15ce0caa4925161ccf3e7f410a99a4a5c48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c487eb8ae9ec1aafdcdeb504d30ada9f5b367082c1ecd503041261b8d153cd26(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolCachePoint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19f2ad45775d34618f425124a5898cd9ebc26393e95f2dcd6715e5e5972b127(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb767c3a0c0dcdba11a31fe1534268f3ad2ac1e986fbba233f0f6888660d808(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationTool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b6739ffdd73767949fd606a355af3d71021a60a26a7e74214aa9491932c31a(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    input_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc77b5ef9229a21262ddcc4e8dbb3345743371c0cddd6da417b356db21b6b5b5(
    *,
    json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98719572f873e249cc9d84f14b8890f2c03922256905322a2dbfca3a4460eb44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28be0e999605e14d2c63459caab4235b076d6eed51516f6dcd356fa5fa16b606(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbff20c919454a60052e9ecc409810ac82163ebda49397f94abbb4eeb9f8928a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb8eef9a26fa56b873df1a4e19f60c64f3eed762bf49d36fac072690d1301fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2695e8a254efd54733740f2e16a1f626f86f214178d544e7c7cc942e7a15122(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f12440b7df0ed2ea1ff1a6ed8f74813533ba91394f9d18caa15bcb49a709e4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7779f762266f17896f0cc553d09b0f9e14e1a55cb7710bc04de23e49adc6d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12497ba0ab381e0388012f538789cc895668942915191b5d2bf6bb684aa78a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919dccd59d94fc3ddcb69d868bb75b4f6f28372571f233bb0453c7bb290d7210(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b72610ba80fb5fbab9ee2321c28a46fc4d7636235fc83e185f4c6055d4a0eca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4543284be4ebcf3d1e71e25421a1146576652a2ec591008e4538a9c7c4c28e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7a6e08d7b64ea4c24f73ed7d43bc5566f2e171246e490ec2938efe52612ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4db78ee8e213d19da091f495fb72fb7b3ada8c2e1a5e691384eec9e4a7dbbff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77234c675761b7cd03315a14ba817e1aec912f49d137053b8bd95495a80d6aab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1cac655595e9aaea945db31a2072431b7ef51465f62834387512cce90404af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083c560b2ac4855e7e269bfe9d791c5689b4408d665492e30a9cbe59382fd7ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fac780d723e9fd9307da529c90db61c972af0134bed0a14c75765758dec8a1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpecInputSchema, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbac754b8e7ffe8313efcc3f24760ab8c5b901ed0834b19533c1e7ecaf199ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cad1d69fed45ce267d95e5986a7348e77acd9c5fdd0907777c2a2df2d07d9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c81116ec3e4559e649de2fee6d6a5edf508a7951be2d74ec103699b1b0c738(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationChatToolConfigurationToolToolSpec]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315050113583c4cbadcc7d237570baf1420722a2a5497a816a3e2b1f68e9e597(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fc178809cb365fa1878e7669a5deb1f05174ba9432f6c5ffa716343b6283f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fed3942f50482b761b0354d20a82c81516106e946e78e16989b8350fcc3d28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e235852c34588270c2dc5a659dfe8870ffeffead2a1f06b1db99073fcf2eef1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42fbb48b925d981075a4d680c8f9fee0b8adf2816c098f8bca7b8067e0cd5f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc2cfa77ce594f43b405ec51ba204ea242a171138d3889e129c20b8e1340c07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a973c19bf7672bd0059cc030c41563fbab99f08245c65c7dd13c0a79dd232489(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e884769afaf8bffa89ccc1c5ebee5aa8a766127e01185d4af96f6557d17191e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationChat, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a289ad1421af1ccace2b9fba89b0bf1fb8dbbccfc5f2e69bc9f7da10ba09b1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationText, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb27ad89881884fd37a8b872e45e7bf32d899c60d888864e89574fba97e7a85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77148f6ecc2cc4f63a8a90764d3a41f3d6f8685528f16c8c3b2757fc7272705c(
    *,
    text: builtins.str,
    cache_point: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationTextCachePoint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    input_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationTextInputVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197b1bab9644bda89aeae91c70bf12afdde0f4a73dcea3ab5ef1d70c4c7f1cec(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbc180ef7eedc23ef72e588dabcdfb220dfae4751523be1682d6d7c06243c61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016124e230d6d59a3824281f55ae71ff6b382ebe7c78f361a8edcdf0cffa1c32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6685b13cd9ad4bc6f6cdb7cc285e754e8feb48379575fc1360f8a5a68fce7491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e94bdbc9ebe75b1ecfa44d003a40d16258c615556b779c7216a6d335e6baba9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4c78d9b704d2ce6310dbd3ea8f43a896149f10a2d190ef512897b0db77785a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e2f3e38ade562f482393a40873b85573627770a2dce810e49c1ed644d6afc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextCachePoint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1148d52684e4826fc4cba39e0c9b995fa0ac4eda508af11ef6a0d0ab07cd3340(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d624c34427003fdb838f6e11acff7bd99fa7a9832768c06ef17ead7724212f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377411c40bc796a16048657eecc2ae0dca61d7754a106e3e91f509243b21fda4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextCachePoint]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7ad64535534ed02948b39a4579c2d9fb6cee88b90de908ccbc66103bfb92ae(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae865070f55effebecb0ab1ab7ec70d64a496228223cc7a78273df7f627d777(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3f0db75515e7ff837d605d8bb50c59978abe98e52451c39063a699b5da0d00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea15c036f35fc24de9d334a9255edc5af4222f0a90840f1e9f3db38319fa5b42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cc81e8f3457c12e36075a102085e54354509553b5dc7d053cc67f7db72974b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb23ff5e55745dd114043b9ae214c403261445509652a5cc8a30cabab65c0a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bacbccaa9c3b0ca136dd7de4319739d2952d0e3e478588c82d44f1cf2e5bc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationTextInputVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd1118d2f329add290635b0ad156547d6c0a74f8675b1fbc0dd60473b23e29a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29950d12464ff6d557029555d337d3b36b56cd4cc8f7dceffe537f52abadc67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4f3f8ca2783df8219c1c688e4fef80438720883701c97aa9a8ba95b0f04696(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationTextInputVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0a45cea8b7ecd985d405e5ea3e15688108d7ed123af0c66514146a71499908(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8f8107482682d0ff831325718aa13d4f8109d29346aa71f3eeaf6902d50752(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f26a9149e94a081ddb9481241ed3f4ef0e2fd2b5c925834585625489514ce4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b855da5421530e6de16c39a2a862b48965b9dfc20d50fbf1c5808fed9b1fd042(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926489b52af64b61a870d1a56664a1238dbd28e040ac32270de114c2c5f3ee68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce03fd294281bf6bebc6c52a2efcfad181dbb8395758b47ec3cb3c1cc37a376(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentPromptVariantTemplateConfigurationText]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8078c9f4851348cf6b66f6e936c651330e0511c091b019e4d8f208cff5d1339(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b358e7170488ca1dc30e9fdf53d8d316b59b20d27443d6fb9fa2615568fa424(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationTextCachePoint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4babaa04f7255d7e86106989ffcdc11914c0e21447bf5a2e1cdc0f85e99be9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentPromptVariantTemplateConfigurationTextInputVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6fbcdfead8aa58346dcada4f9774a2347c99f3742944d3225167fb4821e999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8c491a4a8c880827bec6272c921e432bcceddd35f41ee89cbe08b2b94d4682(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentPromptVariantTemplateConfigurationText]],
) -> None:
    """Type checking stubs"""
    pass
