r'''
# `aws_ec2_allowed_images_settings`

Refer to the Terraform Registry for docs: [`aws_ec2_allowed_images_settings`](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings).
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


class Ec2AllowedImagesSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings aws_ec2_allowed_images_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        state: builtins.str,
        image_criterion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Ec2AllowedImagesSettingsImageCriterion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings aws_ec2_allowed_images_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#state Ec2AllowedImagesSettings#state}.
        :param image_criterion: image_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#image_criterion Ec2AllowedImagesSettings#image_criterion}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#region Ec2AllowedImagesSettings#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2b7c53648c6703e8bc8d35d12d196bff5345afe22035ca833a9bb1c7597466)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = Ec2AllowedImagesSettingsConfig(
            state=state,
            image_criterion=image_criterion,
            region=region,
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
        '''Generates CDKTF code for importing a Ec2AllowedImagesSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Ec2AllowedImagesSettings to import.
        :param import_from_id: The id of the existing Ec2AllowedImagesSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Ec2AllowedImagesSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2920754ced93ad38399a9efd0ccb1a2a2cdb9638be02c0b539a87cf90589402)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putImageCriterion")
    def put_image_criterion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Ec2AllowedImagesSettingsImageCriterion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63197294cea28962902f1675a22584fd5a7bf158cf929f8a0f8b8548bb8cacc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putImageCriterion", [value]))

    @jsii.member(jsii_name="resetImageCriterion")
    def reset_image_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageCriterion", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="imageCriterion")
    def image_criterion(self) -> "Ec2AllowedImagesSettingsImageCriterionList":
        return typing.cast("Ec2AllowedImagesSettingsImageCriterionList", jsii.get(self, "imageCriterion"))

    @builtins.property
    @jsii.member(jsii_name="imageCriterionInput")
    def image_criterion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterion"]]], jsii.get(self, "imageCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e1aa948d93e1bae337425027f7beaad3a4e684baa08fac44b46a908bde969c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415b5dfa3add37d7c7c02686c8591472e470a4936a5e1b29adc800cb195009f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "state": "state",
        "image_criterion": "imageCriterion",
        "region": "region",
    },
)
class Ec2AllowedImagesSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        state: builtins.str,
        image_criterion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Ec2AllowedImagesSettingsImageCriterion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#state Ec2AllowedImagesSettings#state}.
        :param image_criterion: image_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#image_criterion Ec2AllowedImagesSettings#image_criterion}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#region Ec2AllowedImagesSettings#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d0d16dea5b4cca2aaef3786b31147bc72d2ea147ea70df0dc580b2f21f5623)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument image_criterion", value=image_criterion, expected_type=type_hints["image_criterion"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "state": state,
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
        if image_criterion is not None:
            self._values["image_criterion"] = image_criterion
        if region is not None:
            self._values["region"] = region

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
    def state(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#state Ec2AllowedImagesSettings#state}.'''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_criterion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterion"]]]:
        '''image_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#image_criterion Ec2AllowedImagesSettings#image_criterion}
        '''
        result = self._values.get("image_criterion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterion"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#region Ec2AllowedImagesSettings#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2AllowedImagesSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterion",
    jsii_struct_bases=[],
    name_mapping={
        "creation_date_condition": "creationDateCondition",
        "deprecation_time_condition": "deprecationTimeCondition",
        "image_names": "imageNames",
        "image_providers": "imageProviders",
        "marketplace_product_codes": "marketplaceProductCodes",
    },
)
class Ec2AllowedImagesSettingsImageCriterion:
    def __init__(
        self,
        *,
        creation_date_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Ec2AllowedImagesSettingsImageCriterionCreationDateCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        deprecation_time_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        marketplace_product_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param creation_date_condition: creation_date_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#creation_date_condition Ec2AllowedImagesSettings#creation_date_condition}
        :param deprecation_time_condition: deprecation_time_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#deprecation_time_condition Ec2AllowedImagesSettings#deprecation_time_condition}
        :param image_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#image_names Ec2AllowedImagesSettings#image_names}.
        :param image_providers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#image_providers Ec2AllowedImagesSettings#image_providers}.
        :param marketplace_product_codes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#marketplace_product_codes Ec2AllowedImagesSettings#marketplace_product_codes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc6d83ebcd52d98b0617cbbf7fd769852f5d749c5d7c9036ac030e84740b97b)
            check_type(argname="argument creation_date_condition", value=creation_date_condition, expected_type=type_hints["creation_date_condition"])
            check_type(argname="argument deprecation_time_condition", value=deprecation_time_condition, expected_type=type_hints["deprecation_time_condition"])
            check_type(argname="argument image_names", value=image_names, expected_type=type_hints["image_names"])
            check_type(argname="argument image_providers", value=image_providers, expected_type=type_hints["image_providers"])
            check_type(argname="argument marketplace_product_codes", value=marketplace_product_codes, expected_type=type_hints["marketplace_product_codes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if creation_date_condition is not None:
            self._values["creation_date_condition"] = creation_date_condition
        if deprecation_time_condition is not None:
            self._values["deprecation_time_condition"] = deprecation_time_condition
        if image_names is not None:
            self._values["image_names"] = image_names
        if image_providers is not None:
            self._values["image_providers"] = image_providers
        if marketplace_product_codes is not None:
            self._values["marketplace_product_codes"] = marketplace_product_codes

    @builtins.property
    def creation_date_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterionCreationDateCondition"]]]:
        '''creation_date_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#creation_date_condition Ec2AllowedImagesSettings#creation_date_condition}
        '''
        result = self._values.get("creation_date_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterionCreationDateCondition"]]], result)

    @builtins.property
    def deprecation_time_condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition"]]]:
        '''deprecation_time_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#deprecation_time_condition Ec2AllowedImagesSettings#deprecation_time_condition}
        '''
        result = self._values.get("deprecation_time_condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition"]]], result)

    @builtins.property
    def image_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#image_names Ec2AllowedImagesSettings#image_names}.'''
        result = self._values.get("image_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def image_providers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#image_providers Ec2AllowedImagesSettings#image_providers}.'''
        result = self._values.get("image_providers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def marketplace_product_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#marketplace_product_codes Ec2AllowedImagesSettings#marketplace_product_codes}.'''
        result = self._values.get("marketplace_product_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2AllowedImagesSettingsImageCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionCreationDateCondition",
    jsii_struct_bases=[],
    name_mapping={"maximum_days_since_created": "maximumDaysSinceCreated"},
)
class Ec2AllowedImagesSettingsImageCriterionCreationDateCondition:
    def __init__(
        self,
        *,
        maximum_days_since_created: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_days_since_created: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#maximum_days_since_created Ec2AllowedImagesSettings#maximum_days_since_created}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9593839ee27ca63aff5e106f4aaf2e7c61801ef9b2aa7c9e483354193f3ff57)
            check_type(argname="argument maximum_days_since_created", value=maximum_days_since_created, expected_type=type_hints["maximum_days_since_created"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_days_since_created is not None:
            self._values["maximum_days_since_created"] = maximum_days_since_created

    @builtins.property
    def maximum_days_since_created(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#maximum_days_since_created Ec2AllowedImagesSettings#maximum_days_since_created}.'''
        result = self._values.get("maximum_days_since_created")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2AllowedImagesSettingsImageCriterionCreationDateCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2AllowedImagesSettingsImageCriterionCreationDateConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionCreationDateConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c7229de6a592d95d58661f689e3b005ab9145594e421a2cb00a59e5d8c9c32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Ec2AllowedImagesSettingsImageCriterionCreationDateConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1b52f78820a74162323821b113b5829bfe4ac933c8c6ba54aaf232a66fd54f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Ec2AllowedImagesSettingsImageCriterionCreationDateConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ad6f721a624ceafcdd156740d763495605f4526b3bbd69e6faa2706954f15d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd38a512e54dbb5c97044d8b5333988618ef30cab2ea84deef998fc83a10ec4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1954bbbc2d8fa78f386a1d64beec1ee41d7928bd2ee4300a2f6c715f84f18772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7c32ac8dfdc1393a274481d7832f92cf9d2e41dacf32de57a0c514bbf234ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Ec2AllowedImagesSettingsImageCriterionCreationDateConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionCreationDateConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ecb66fcbb4d1300b0d8a904b8b3c157c1fd541d17e77c72bc3a7b9e9303dabd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaximumDaysSinceCreated")
    def reset_maximum_days_since_created(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumDaysSinceCreated", []))

    @builtins.property
    @jsii.member(jsii_name="maximumDaysSinceCreatedInput")
    def maximum_days_since_created_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumDaysSinceCreatedInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumDaysSinceCreated")
    def maximum_days_since_created(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumDaysSinceCreated"))

    @maximum_days_since_created.setter
    def maximum_days_since_created(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f8ea99bd6d55bcb7971d3e05e02d540a0854dbce25e4158eb05f00d5aec5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumDaysSinceCreated", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efd833c4dcc7773aa342f72eb555fe8432325c617d04d4984479f6099b39a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition",
    jsii_struct_bases=[],
    name_mapping={"maximum_days_since_deprecated": "maximumDaysSinceDeprecated"},
)
class Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition:
    def __init__(
        self,
        *,
        maximum_days_since_deprecated: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_days_since_deprecated: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#maximum_days_since_deprecated Ec2AllowedImagesSettings#maximum_days_since_deprecated}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e81f9e435a0ff4428f6eae5cbbb96f0d827fac0a669484d932be3e7c81ed3c)
            check_type(argname="argument maximum_days_since_deprecated", value=maximum_days_since_deprecated, expected_type=type_hints["maximum_days_since_deprecated"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_days_since_deprecated is not None:
            self._values["maximum_days_since_deprecated"] = maximum_days_since_deprecated

    @builtins.property
    def maximum_days_since_deprecated(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ec2_allowed_images_settings#maximum_days_since_deprecated Ec2AllowedImagesSettings#maximum_days_since_deprecated}.'''
        result = self._values.get("maximum_days_since_deprecated")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d91e5f45f65950051df2a553a9673a383956b231ecf8ea99d514e0dafa8fa83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae629b1343f6d435430e6553218ac2ce5297763ae27b4375b448550161a6fa6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b29a94cdf57093f62c7c611bf51f3a2d41ecb6ae58f4e4e3e05da89aecd1fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb37975ca2808a2cdd5de75f9191034fbfc532c41f8f58665330fc56fc162e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd802329aa96cdc68cafc19ade740526535d6b248d44e4ba2c95f3d03cc8350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7578a2ff72eca936bc2ae96ee1c473545467b52cedacfbd0aa5373df4885cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__295af574a25c5f4a5459e3a87bd6d787fa255cfdb8da86497f709961c5502f38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaximumDaysSinceDeprecated")
    def reset_maximum_days_since_deprecated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumDaysSinceDeprecated", []))

    @builtins.property
    @jsii.member(jsii_name="maximumDaysSinceDeprecatedInput")
    def maximum_days_since_deprecated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumDaysSinceDeprecatedInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumDaysSinceDeprecated")
    def maximum_days_since_deprecated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumDaysSinceDeprecated"))

    @maximum_days_since_deprecated.setter
    def maximum_days_since_deprecated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228b04f02d48855d2f7df63d1f2eafced125dc2b557683392194faf0288efbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumDaysSinceDeprecated", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29dc2da6e893cc11f0437945d15d33315bf117c4a2e4fc3890b328405f848328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Ec2AllowedImagesSettingsImageCriterionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__922a7a43362b864d0a4b4c84d67937d5af9a36348b4c0ad05e1f2c6cec6e4f06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Ec2AllowedImagesSettingsImageCriterionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6b125baaaea067007ba7c37b0b9fbdfcd9facc1e81c3442d9684deccece67b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Ec2AllowedImagesSettingsImageCriterionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604a96a69bd65eb189e66a4f7677ec144783012ab8557984a25026d79d3bc50c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd8055a7d6da7b90feb69c7ea1f1e7b9be6fb351b7ed0f58bc9c8d3c1e3c6365)
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
            type_hints = typing.get_type_hints(_typecheckingstub__984c58ca545e668e602166fc9a3b69fc0418278a2507a5eb2f199d45a9bbf73b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369a492060070096cdd08acfaab51d763245369b67d772e259aa33e2dbe6a2fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Ec2AllowedImagesSettingsImageCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2AllowedImagesSettings.Ec2AllowedImagesSettingsImageCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4f538a906b8a3e8fac94b739ccf9ecd7b304b9078f774640dcefede95d0e0ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCreationDateCondition")
    def put_creation_date_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eebfa506b2903d7e1829f822cc6f6f2338c85dfe9055d58b9c68b975a55b840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCreationDateCondition", [value]))

    @jsii.member(jsii_name="putDeprecationTimeCondition")
    def put_deprecation_time_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6393d820d0664d6ed07e8c4fb06b852e27b26a8d9a5bd859ee63266916e4e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeprecationTimeCondition", [value]))

    @jsii.member(jsii_name="resetCreationDateCondition")
    def reset_creation_date_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreationDateCondition", []))

    @jsii.member(jsii_name="resetDeprecationTimeCondition")
    def reset_deprecation_time_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprecationTimeCondition", []))

    @jsii.member(jsii_name="resetImageNames")
    def reset_image_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageNames", []))

    @jsii.member(jsii_name="resetImageProviders")
    def reset_image_providers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageProviders", []))

    @jsii.member(jsii_name="resetMarketplaceProductCodes")
    def reset_marketplace_product_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketplaceProductCodes", []))

    @builtins.property
    @jsii.member(jsii_name="creationDateCondition")
    def creation_date_condition(
        self,
    ) -> Ec2AllowedImagesSettingsImageCriterionCreationDateConditionList:
        return typing.cast(Ec2AllowedImagesSettingsImageCriterionCreationDateConditionList, jsii.get(self, "creationDateCondition"))

    @builtins.property
    @jsii.member(jsii_name="deprecationTimeCondition")
    def deprecation_time_condition(
        self,
    ) -> Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionList:
        return typing.cast(Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionList, jsii.get(self, "deprecationTimeCondition"))

    @builtins.property
    @jsii.member(jsii_name="creationDateConditionInput")
    def creation_date_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]]], jsii.get(self, "creationDateConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="deprecationTimeConditionInput")
    def deprecation_time_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]]], jsii.get(self, "deprecationTimeConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNamesInput")
    def image_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "imageNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageProvidersInput")
    def image_providers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "imageProvidersInput"))

    @builtins.property
    @jsii.member(jsii_name="marketplaceProductCodesInput")
    def marketplace_product_codes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "marketplaceProductCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNames")
    def image_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "imageNames"))

    @image_names.setter
    def image_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2702d7fa8c8d5d072b85488b34063b430625d19e5821f44f3ff8eeee64488301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageProviders")
    def image_providers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "imageProviders"))

    @image_providers.setter
    def image_providers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89b8331c51d10d9af8d38b14db0caabbb157cdfbab7723e1e9e3e646572ea0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageProviders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketplaceProductCodes")
    def marketplace_product_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "marketplaceProductCodes"))

    @marketplace_product_codes.setter
    def marketplace_product_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2682990bd93e45c58c3466eb1b337a9259847ae6df7d0f0f05bc7df1dc431f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketplaceProductCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650df87e8bdbef142c247bc3c1546a4c6db09be526afbe8f77002abf47283a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Ec2AllowedImagesSettings",
    "Ec2AllowedImagesSettingsConfig",
    "Ec2AllowedImagesSettingsImageCriterion",
    "Ec2AllowedImagesSettingsImageCriterionCreationDateCondition",
    "Ec2AllowedImagesSettingsImageCriterionCreationDateConditionList",
    "Ec2AllowedImagesSettingsImageCriterionCreationDateConditionOutputReference",
    "Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition",
    "Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionList",
    "Ec2AllowedImagesSettingsImageCriterionDeprecationTimeConditionOutputReference",
    "Ec2AllowedImagesSettingsImageCriterionList",
    "Ec2AllowedImagesSettingsImageCriterionOutputReference",
]

publication.publish()

def _typecheckingstub__4d2b7c53648c6703e8bc8d35d12d196bff5345afe22035ca833a9bb1c7597466(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    state: builtins.str,
    image_criterion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b2920754ced93ad38399a9efd0ccb1a2a2cdb9638be02c0b539a87cf90589402(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63197294cea28962902f1675a22584fd5a7bf158cf929f8a0f8b8548bb8cacc8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e1aa948d93e1bae337425027f7beaad3a4e684baa08fac44b46a908bde969c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415b5dfa3add37d7c7c02686c8591472e470a4936a5e1b29adc800cb195009f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d0d16dea5b4cca2aaef3786b31147bc72d2ea147ea70df0dc580b2f21f5623(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    state: builtins.str,
    image_criterion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc6d83ebcd52d98b0617cbbf7fd769852f5d749c5d7c9036ac030e84740b97b(
    *,
    creation_date_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deprecation_time_condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    image_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    marketplace_product_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9593839ee27ca63aff5e106f4aaf2e7c61801ef9b2aa7c9e483354193f3ff57(
    *,
    maximum_days_since_created: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c7229de6a592d95d58661f689e3b005ab9145594e421a2cb00a59e5d8c9c32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1b52f78820a74162323821b113b5829bfe4ac933c8c6ba54aaf232a66fd54f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ad6f721a624ceafcdd156740d763495605f4526b3bbd69e6faa2706954f15d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd38a512e54dbb5c97044d8b5333988618ef30cab2ea84deef998fc83a10ec4e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1954bbbc2d8fa78f386a1d64beec1ee41d7928bd2ee4300a2f6c715f84f18772(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7c32ac8dfdc1393a274481d7832f92cf9d2e41dacf32de57a0c514bbf234ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecb66fcbb4d1300b0d8a904b8b3c157c1fd541d17e77c72bc3a7b9e9303dabd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f8ea99bd6d55bcb7971d3e05e02d540a0854dbce25e4158eb05f00d5aec5b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efd833c4dcc7773aa342f72eb555fe8432325c617d04d4984479f6099b39a37(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionCreationDateCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e81f9e435a0ff4428f6eae5cbbb96f0d827fac0a669484d932be3e7c81ed3c(
    *,
    maximum_days_since_deprecated: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d91e5f45f65950051df2a553a9673a383956b231ecf8ea99d514e0dafa8fa83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae629b1343f6d435430e6553218ac2ce5297763ae27b4375b448550161a6fa6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b29a94cdf57093f62c7c611bf51f3a2d41ecb6ae58f4e4e3e05da89aecd1fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb37975ca2808a2cdd5de75f9191034fbfc532c41f8f58665330fc56fc162e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd802329aa96cdc68cafc19ade740526535d6b248d44e4ba2c95f3d03cc8350(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7578a2ff72eca936bc2ae96ee1c473545467b52cedacfbd0aa5373df4885cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295af574a25c5f4a5459e3a87bd6d787fa255cfdb8da86497f709961c5502f38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228b04f02d48855d2f7df63d1f2eafced125dc2b557683392194faf0288efbc1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29dc2da6e893cc11f0437945d15d33315bf117c4a2e4fc3890b328405f848328(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922a7a43362b864d0a4b4c84d67937d5af9a36348b4c0ad05e1f2c6cec6e4f06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6b125baaaea067007ba7c37b0b9fbdfcd9facc1e81c3442d9684deccece67b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604a96a69bd65eb189e66a4f7677ec144783012ab8557984a25026d79d3bc50c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8055a7d6da7b90feb69c7ea1f1e7b9be6fb351b7ed0f58bc9c8d3c1e3c6365(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984c58ca545e668e602166fc9a3b69fc0418278a2507a5eb2f199d45a9bbf73b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369a492060070096cdd08acfaab51d763245369b67d772e259aa33e2dbe6a2fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Ec2AllowedImagesSettingsImageCriterion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f538a906b8a3e8fac94b739ccf9ecd7b304b9078f774640dcefede95d0e0ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eebfa506b2903d7e1829f822cc6f6f2338c85dfe9055d58b9c68b975a55b840(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterionCreationDateCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6393d820d0664d6ed07e8c4fb06b852e27b26a8d9a5bd859ee63266916e4e22(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Ec2AllowedImagesSettingsImageCriterionDeprecationTimeCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2702d7fa8c8d5d072b85488b34063b430625d19e5821f44f3ff8eeee64488301(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89b8331c51d10d9af8d38b14db0caabbb157cdfbab7723e1e9e3e646572ea0f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2682990bd93e45c58c3466eb1b337a9259847ae6df7d0f0f05bc7df1dc431f97(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650df87e8bdbef142c247bc3c1546a4c6db09be526afbe8f77002abf47283a7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Ec2AllowedImagesSettingsImageCriterion]],
) -> None:
    """Type checking stubs"""
    pass
