r'''
# `aws_sagemaker_endpoint_configuration`

Refer to the Terraform Registry for docs: [`aws_sagemaker_endpoint_configuration`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration).
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


class SagemakerEndpointConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration aws_sagemaker_endpoint_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
        async_inference_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_capture_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariants", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration aws_sagemaker_endpoint_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param production_variants: production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#production_variants SagemakerEndpointConfiguration#production_variants}
        :param async_inference_config: async_inference_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#async_inference_config SagemakerEndpointConfiguration#async_inference_config}
        :param data_capture_config: data_capture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#data_capture_config SagemakerEndpointConfiguration#data_capture_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#id SagemakerEndpointConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_arn SagemakerEndpointConfiguration#kms_key_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#name SagemakerEndpointConfiguration#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#name_prefix SagemakerEndpointConfiguration#name_prefix}.
        :param shadow_production_variants: shadow_production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#shadow_production_variants SagemakerEndpointConfiguration#shadow_production_variants}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#tags SagemakerEndpointConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#tags_all SagemakerEndpointConfiguration#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400ab2f4777265a946b6b8276b052755086c5de235865af9ee8aab00f21da3e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerEndpointConfigurationConfig(
            production_variants=production_variants,
            async_inference_config=async_inference_config,
            data_capture_config=data_capture_config,
            id=id,
            kms_key_arn=kms_key_arn,
            name=name,
            name_prefix=name_prefix,
            shadow_production_variants=shadow_production_variants,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a SagemakerEndpointConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerEndpointConfiguration to import.
        :param import_from_id: The id of the existing SagemakerEndpointConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerEndpointConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c119146cf009e7d5862bb5a12e6f71424c6c8ec40e93de2cb2fb5418105db8dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAsyncInferenceConfig")
    def put_async_inference_config(
        self,
        *,
        output_config: typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig", typing.Dict[builtins.str, typing.Any]],
        client_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#output_config SagemakerEndpointConfiguration#output_config}
        :param client_config: client_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#client_config SagemakerEndpointConfiguration#client_config}
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfig(
            output_config=output_config, client_config=client_config
        )

        return typing.cast(None, jsii.invoke(self, "putAsyncInferenceConfig", [value]))

    @jsii.member(jsii_name="putDataCaptureConfig")
    def put_data_capture_config(
        self,
        *,
        capture_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions", typing.Dict[builtins.str, typing.Any]]]],
        destination_s3_uri: builtins.str,
        initial_sampling_percentage: jsii.Number,
        capture_content_type_header: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_capture: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capture_options: capture_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_options SagemakerEndpointConfiguration#capture_options}
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param initial_sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_sampling_percentage SagemakerEndpointConfiguration#initial_sampling_percentage}.
        :param capture_content_type_header: capture_content_type_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_content_type_header SagemakerEndpointConfiguration#capture_content_type_header}
        :param enable_capture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#enable_capture SagemakerEndpointConfiguration#enable_capture}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        value = SagemakerEndpointConfigurationDataCaptureConfig(
            capture_options=capture_options,
            destination_s3_uri=destination_s3_uri,
            initial_sampling_percentage=initial_sampling_percentage,
            capture_content_type_header=capture_content_type_header,
            enable_capture=enable_capture,
            kms_key_id=kms_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDataCaptureConfig", [value]))

    @jsii.member(jsii_name="putProductionVariants")
    def put_production_variants(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8802dbe0982b4f40b7e562c738d89c0f9fffac7c5e654624f677a09af78d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProductionVariants", [value]))

    @jsii.member(jsii_name="putShadowProductionVariants")
    def put_shadow_production_variants(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3928d439f0992d35785ab0ce88003b92b0dc06b075a1b993cd6207e9ee6a150d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putShadowProductionVariants", [value]))

    @jsii.member(jsii_name="resetAsyncInferenceConfig")
    def reset_async_inference_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsyncInferenceConfig", []))

    @jsii.member(jsii_name="resetDataCaptureConfig")
    def reset_data_capture_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCaptureConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetShadowProductionVariants")
    def reset_shadow_production_variants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShadowProductionVariants", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="asyncInferenceConfig")
    def async_inference_config(
        self,
    ) -> "SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference", jsii.get(self, "asyncInferenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataCaptureConfig")
    def data_capture_config(
        self,
    ) -> "SagemakerEndpointConfigurationDataCaptureConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationDataCaptureConfigOutputReference", jsii.get(self, "dataCaptureConfig"))

    @builtins.property
    @jsii.member(jsii_name="productionVariants")
    def production_variants(
        self,
    ) -> "SagemakerEndpointConfigurationProductionVariantsList":
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsList", jsii.get(self, "productionVariants"))

    @builtins.property
    @jsii.member(jsii_name="shadowProductionVariants")
    def shadow_production_variants(
        self,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsList":
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsList", jsii.get(self, "shadowProductionVariants"))

    @builtins.property
    @jsii.member(jsii_name="asyncInferenceConfigInput")
    def async_inference_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfig"], jsii.get(self, "asyncInferenceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCaptureConfigInput")
    def data_capture_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"], jsii.get(self, "dataCaptureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="productionVariantsInput")
    def production_variants_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]]], jsii.get(self, "productionVariantsInput"))

    @builtins.property
    @jsii.member(jsii_name="shadowProductionVariantsInput")
    def shadow_production_variants_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]], jsii.get(self, "shadowProductionVariantsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6793aa42fd735bbcb9ab21b676b88cbf35b06301f6af1e6dbb4187360c4c271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b112001cbd47306082da082eddcb81f532d0c129efeac5b169631379c3885eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5dbac074b12dfdec031c2ade8a58926274741f40921c3fe15d6de17a9d9891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96003ecd8d1d8ccc47ef6cf4373de007321dd807337e8e8c96b75837ae9bcf3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6899621cd811d0d0e644aad4077aded9eeeda2bdcda191ca219cfeab5c82540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88fb26b73e193784bc9c17458fe5ae1c15ecc0887ec71a66d45257d807a3f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfig",
    jsii_struct_bases=[],
    name_mapping={"output_config": "outputConfig", "client_config": "clientConfig"},
)
class SagemakerEndpointConfigurationAsyncInferenceConfig:
    def __init__(
        self,
        *,
        output_config: typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig", typing.Dict[builtins.str, typing.Any]],
        client_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param output_config: output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#output_config SagemakerEndpointConfiguration#output_config}
        :param client_config: client_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#client_config SagemakerEndpointConfiguration#client_config}
        '''
        if isinstance(output_config, dict):
            output_config = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig(**output_config)
        if isinstance(client_config, dict):
            client_config = SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig(**client_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541333f3f17c0529299347be153f3621f2bc1e7ac2eea503741c3f7b9c14b2e6)
            check_type(argname="argument output_config", value=output_config, expected_type=type_hints["output_config"])
            check_type(argname="argument client_config", value=client_config, expected_type=type_hints["client_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_config": output_config,
        }
        if client_config is not None:
            self._values["client_config"] = client_config

    @builtins.property
    def output_config(
        self,
    ) -> "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig":
        '''output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#output_config SagemakerEndpointConfiguration#output_config}
        '''
        result = self._values.get("output_config")
        assert result is not None, "Required property 'output_config' is missing"
        return typing.cast("SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig", result)

    @builtins.property
    def client_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig"]:
        '''client_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#client_config SagemakerEndpointConfiguration#client_config}
        '''
        result = self._values.get("client_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_invocations_per_instance": "maxConcurrentInvocationsPerInstance",
    },
)
class SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig:
    def __init__(
        self,
        *,
        max_concurrent_invocations_per_instance: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_invocations_per_instance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrent_invocations_per_instance SagemakerEndpointConfiguration#max_concurrent_invocations_per_instance}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783605fe56ba8b2713e1157214d3797f8c0fcadce21cc398f2e043ac3d71ea5f)
            check_type(argname="argument max_concurrent_invocations_per_instance", value=max_concurrent_invocations_per_instance, expected_type=type_hints["max_concurrent_invocations_per_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_invocations_per_instance is not None:
            self._values["max_concurrent_invocations_per_instance"] = max_concurrent_invocations_per_instance

    @builtins.property
    def max_concurrent_invocations_per_instance(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrent_invocations_per_instance SagemakerEndpointConfiguration#max_concurrent_invocations_per_instance}.'''
        result = self._values.get("max_concurrent_invocations_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55e3d35b6c05ac5e62ca6d80a041710038ef0fd0c0d40ed3a141efa0035ef951)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxConcurrentInvocationsPerInstance")
    def reset_max_concurrent_invocations_per_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentInvocationsPerInstance", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentInvocationsPerInstanceInput")
    def max_concurrent_invocations_per_instance_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentInvocationsPerInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentInvocationsPerInstance")
    def max_concurrent_invocations_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentInvocationsPerInstance"))

    @max_concurrent_invocations_per_instance.setter
    def max_concurrent_invocations_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a6815e28ef0868d6c2e9bc5d44c3607a2be6c6fc0c65f26b6e4f13f75553a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentInvocationsPerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d3c24b548b6b2707c6c1165090ea14587896d61d40615d4c6ee2189ddc253d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_output_path": "s3OutputPath",
        "kms_key_id": "kmsKeyId",
        "notification_config": "notificationConfig",
        "s3_failure_path": "s3FailurePath",
    },
)
class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig:
    def __init__(
        self,
        *,
        s3_output_path: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_failure_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_output_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#s3_output_path SagemakerEndpointConfiguration#s3_output_path}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#notification_config SagemakerEndpointConfiguration#notification_config}
        :param s3_failure_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#s3_failure_path SagemakerEndpointConfiguration#s3_failure_path}.
        '''
        if isinstance(notification_config, dict):
            notification_config = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig(**notification_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d793e1f69c472ad192d35481e677327ba8b1ec7d9b35d9c0dfbf3500927914)
            check_type(argname="argument s3_output_path", value=s3_output_path, expected_type=type_hints["s3_output_path"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
            check_type(argname="argument s3_failure_path", value=s3_failure_path, expected_type=type_hints["s3_failure_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_output_path": s3_output_path,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if notification_config is not None:
            self._values["notification_config"] = notification_config
        if s3_failure_path is not None:
            self._values["s3_failure_path"] = s3_failure_path

    @builtins.property
    def s3_output_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#s3_output_path SagemakerEndpointConfiguration#s3_output_path}.'''
        result = self._values.get("s3_output_path")
        assert result is not None, "Required property 's3_output_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig"]:
        '''notification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#notification_config SagemakerEndpointConfiguration#notification_config}
        '''
        result = self._values.get("notification_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig"], result)

    @builtins.property
    def s3_failure_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#s3_failure_path SagemakerEndpointConfiguration#s3_failure_path}.'''
        result = self._values.get("s3_failure_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "error_topic": "errorTopic",
        "include_inference_response_in": "includeInferenceResponseIn",
        "success_topic": "successTopic",
    },
)
class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig:
    def __init__(
        self,
        *,
        error_topic: typing.Optional[builtins.str] = None,
        include_inference_response_in: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#error_topic SagemakerEndpointConfiguration#error_topic}.
        :param include_inference_response_in: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#include_inference_response_in SagemakerEndpointConfiguration#include_inference_response_in}.
        :param success_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#success_topic SagemakerEndpointConfiguration#success_topic}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d32fc8df0086d95be699e9c9ee144b21afd21163f8235e33d87ba17398f4674)
            check_type(argname="argument error_topic", value=error_topic, expected_type=type_hints["error_topic"])
            check_type(argname="argument include_inference_response_in", value=include_inference_response_in, expected_type=type_hints["include_inference_response_in"])
            check_type(argname="argument success_topic", value=success_topic, expected_type=type_hints["success_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if error_topic is not None:
            self._values["error_topic"] = error_topic
        if include_inference_response_in is not None:
            self._values["include_inference_response_in"] = include_inference_response_in
        if success_topic is not None:
            self._values["success_topic"] = success_topic

    @builtins.property
    def error_topic(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#error_topic SagemakerEndpointConfiguration#error_topic}.'''
        result = self._values.get("error_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_inference_response_in(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#include_inference_response_in SagemakerEndpointConfiguration#include_inference_response_in}.'''
        result = self._values.get("include_inference_response_in")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def success_topic(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#success_topic SagemakerEndpointConfiguration#success_topic}.'''
        result = self._values.get("success_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02e313cbbea936e34aca6fd959c0a96ef7ff029ab7b581711d5a34da5e5c29eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetErrorTopic")
    def reset_error_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorTopic", []))

    @jsii.member(jsii_name="resetIncludeInferenceResponseIn")
    def reset_include_inference_response_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeInferenceResponseIn", []))

    @jsii.member(jsii_name="resetSuccessTopic")
    def reset_success_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessTopic", []))

    @builtins.property
    @jsii.member(jsii_name="errorTopicInput")
    def error_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInferenceResponseInInput")
    def include_inference_response_in_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeInferenceResponseInInput"))

    @builtins.property
    @jsii.member(jsii_name="successTopicInput")
    def success_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="errorTopic")
    def error_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorTopic"))

    @error_topic.setter
    def error_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d8d34f22cb6b3038e675bdefdfa0ae65eb0f7c4fcb2f3f7d94de7c0d173424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeInferenceResponseIn")
    def include_inference_response_in(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeInferenceResponseIn"))

    @include_inference_response_in.setter
    def include_inference_response_in(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907c4f8786fb12b4c84a0c3e2b0719db9f21e311c047b94b082d18163a04fe6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeInferenceResponseIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successTopic")
    def success_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successTopic"))

    @success_topic.setter
    def success_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b55b569a6e40d673539b91394b290abe45ca61dc698beaaa687c6019994fa3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a737f164ba6e9fecdba481e5d4d84d92847cab535b39b30f896edaf19d3cc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27e1ae962545e83c29bd983799fa9ca3983b5dd003cbb8ceea392774517d19c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotificationConfig")
    def put_notification_config(
        self,
        *,
        error_topic: typing.Optional[builtins.str] = None,
        include_inference_response_in: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#error_topic SagemakerEndpointConfiguration#error_topic}.
        :param include_inference_response_in: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#include_inference_response_in SagemakerEndpointConfiguration#include_inference_response_in}.
        :param success_topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#success_topic SagemakerEndpointConfiguration#success_topic}.
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig(
            error_topic=error_topic,
            include_inference_response_in=include_inference_response_in,
            success_topic=success_topic,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationConfig", [value]))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetNotificationConfig")
    def reset_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationConfig", []))

    @jsii.member(jsii_name="resetS3FailurePath")
    def reset_s3_failure_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3FailurePath", []))

    @builtins.property
    @jsii.member(jsii_name="notificationConfig")
    def notification_config(
        self,
    ) -> SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference, jsii.get(self, "notificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationConfigInput")
    def notification_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig], jsii.get(self, "notificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="s3FailurePathInput")
    def s3_failure_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3FailurePathInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputPathInput")
    def s3_output_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3OutputPathInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81241a130d5f95f33250c4bb8b628de648e836d8b7715ad31789c3094889a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3FailurePath")
    def s3_failure_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3FailurePath"))

    @s3_failure_path.setter
    def s3_failure_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c50de6d3d25bb36a5f158ca6a00b3fa1cac632819330c0f47e0c3f2c83a7de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3FailurePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3OutputPath")
    def s3_output_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3OutputPath"))

    @s3_output_path.setter
    def s3_output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a911f81caff2636d0148980dbb50f0219a5798593d98626403fff4ee0190ddf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3OutputPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91d821bf21632803e7bfacf8be0706c7f48062eacbf5f0301780d591c6cbeb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2746889b420d793d9edea295b0619c77195f557985274e362ffb8a478da2b8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientConfig")
    def put_client_config(
        self,
        *,
        max_concurrent_invocations_per_instance: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_invocations_per_instance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrent_invocations_per_instance SagemakerEndpointConfiguration#max_concurrent_invocations_per_instance}.
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig(
            max_concurrent_invocations_per_instance=max_concurrent_invocations_per_instance,
        )

        return typing.cast(None, jsii.invoke(self, "putClientConfig", [value]))

    @jsii.member(jsii_name="putOutputConfig")
    def put_output_config(
        self,
        *,
        s3_output_path: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
        notification_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_failure_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_output_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#s3_output_path SagemakerEndpointConfiguration#s3_output_path}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        :param notification_config: notification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#notification_config SagemakerEndpointConfiguration#notification_config}
        :param s3_failure_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#s3_failure_path SagemakerEndpointConfiguration#s3_failure_path}.
        '''
        value = SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig(
            s3_output_path=s3_output_path,
            kms_key_id=kms_key_id,
            notification_config=notification_config,
            s3_failure_path=s3_failure_path,
        )

        return typing.cast(None, jsii.invoke(self, "putOutputConfig", [value]))

    @jsii.member(jsii_name="resetClientConfig")
    def reset_client_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientConfig", []))

    @builtins.property
    @jsii.member(jsii_name="clientConfig")
    def client_config(
        self,
    ) -> SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference, jsii.get(self, "clientConfig"))

    @builtins.property
    @jsii.member(jsii_name="outputConfig")
    def output_config(
        self,
    ) -> SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference, jsii.get(self, "outputConfig"))

    @builtins.property
    @jsii.member(jsii_name="clientConfigInput")
    def client_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig], jsii.get(self, "clientConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="outputConfigInput")
    def output_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig], jsii.get(self, "outputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492553ec3743af75a9b600557959767c915b12c3c92a68c95f426045f79fdf59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "production_variants": "productionVariants",
        "async_inference_config": "asyncInferenceConfig",
        "data_capture_config": "dataCaptureConfig",
        "id": "id",
        "kms_key_arn": "kmsKeyArn",
        "name": "name",
        "name_prefix": "namePrefix",
        "shadow_production_variants": "shadowProductionVariants",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerEndpointConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariants", typing.Dict[builtins.str, typing.Any]]]],
        async_inference_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        data_capture_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariants", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param production_variants: production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#production_variants SagemakerEndpointConfiguration#production_variants}
        :param async_inference_config: async_inference_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#async_inference_config SagemakerEndpointConfiguration#async_inference_config}
        :param data_capture_config: data_capture_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#data_capture_config SagemakerEndpointConfiguration#data_capture_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#id SagemakerEndpointConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_arn SagemakerEndpointConfiguration#kms_key_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#name SagemakerEndpointConfiguration#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#name_prefix SagemakerEndpointConfiguration#name_prefix}.
        :param shadow_production_variants: shadow_production_variants block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#shadow_production_variants SagemakerEndpointConfiguration#shadow_production_variants}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#tags SagemakerEndpointConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#tags_all SagemakerEndpointConfiguration#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(async_inference_config, dict):
            async_inference_config = SagemakerEndpointConfigurationAsyncInferenceConfig(**async_inference_config)
        if isinstance(data_capture_config, dict):
            data_capture_config = SagemakerEndpointConfigurationDataCaptureConfig(**data_capture_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef24afb957de9c40da6864604adacf6f822a5eefe8dc09dd46c7147fb23cdf40)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument production_variants", value=production_variants, expected_type=type_hints["production_variants"])
            check_type(argname="argument async_inference_config", value=async_inference_config, expected_type=type_hints["async_inference_config"])
            check_type(argname="argument data_capture_config", value=data_capture_config, expected_type=type_hints["data_capture_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument shadow_production_variants", value=shadow_production_variants, expected_type=type_hints["shadow_production_variants"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "production_variants": production_variants,
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
        if async_inference_config is not None:
            self._values["async_inference_config"] = async_inference_config
        if data_capture_config is not None:
            self._values["data_capture_config"] = data_capture_config
        if id is not None:
            self._values["id"] = id
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if shadow_production_variants is not None:
            self._values["shadow_production_variants"] = shadow_production_variants
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def production_variants(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]]:
        '''production_variants block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#production_variants SagemakerEndpointConfiguration#production_variants}
        '''
        result = self._values.get("production_variants")
        assert result is not None, "Required property 'production_variants' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariants"]], result)

    @builtins.property
    def async_inference_config(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig]:
        '''async_inference_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#async_inference_config SagemakerEndpointConfiguration#async_inference_config}
        '''
        result = self._values.get("async_inference_config")
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig], result)

    @builtins.property
    def data_capture_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"]:
        '''data_capture_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#data_capture_config SagemakerEndpointConfiguration#data_capture_config}
        '''
        result = self._values.get("data_capture_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationDataCaptureConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#id SagemakerEndpointConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_arn SagemakerEndpointConfiguration#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#name SagemakerEndpointConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#name_prefix SagemakerEndpointConfiguration#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shadow_production_variants(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]]:
        '''shadow_production_variants block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#shadow_production_variants SagemakerEndpointConfiguration#shadow_production_variants}
        '''
        result = self._values.get("shadow_production_variants")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariants"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#tags SagemakerEndpointConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#tags_all SagemakerEndpointConfiguration#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfig",
    jsii_struct_bases=[],
    name_mapping={
        "capture_options": "captureOptions",
        "destination_s3_uri": "destinationS3Uri",
        "initial_sampling_percentage": "initialSamplingPercentage",
        "capture_content_type_header": "captureContentTypeHeader",
        "enable_capture": "enableCapture",
        "kms_key_id": "kmsKeyId",
    },
)
class SagemakerEndpointConfigurationDataCaptureConfig:
    def __init__(
        self,
        *,
        capture_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions", typing.Dict[builtins.str, typing.Any]]]],
        destination_s3_uri: builtins.str,
        initial_sampling_percentage: jsii.Number,
        capture_content_type_header: typing.Optional[typing.Union["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_capture: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capture_options: capture_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_options SagemakerEndpointConfiguration#capture_options}
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param initial_sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_sampling_percentage SagemakerEndpointConfiguration#initial_sampling_percentage}.
        :param capture_content_type_header: capture_content_type_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_content_type_header SagemakerEndpointConfiguration#capture_content_type_header}
        :param enable_capture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#enable_capture SagemakerEndpointConfiguration#enable_capture}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        if isinstance(capture_content_type_header, dict):
            capture_content_type_header = SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader(**capture_content_type_header)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734bc0c9e881259aa2e8b6b019c29d47812de8ed8cdd0682d0397b15bbede200)
            check_type(argname="argument capture_options", value=capture_options, expected_type=type_hints["capture_options"])
            check_type(argname="argument destination_s3_uri", value=destination_s3_uri, expected_type=type_hints["destination_s3_uri"])
            check_type(argname="argument initial_sampling_percentage", value=initial_sampling_percentage, expected_type=type_hints["initial_sampling_percentage"])
            check_type(argname="argument capture_content_type_header", value=capture_content_type_header, expected_type=type_hints["capture_content_type_header"])
            check_type(argname="argument enable_capture", value=enable_capture, expected_type=type_hints["enable_capture"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capture_options": capture_options,
            "destination_s3_uri": destination_s3_uri,
            "initial_sampling_percentage": initial_sampling_percentage,
        }
        if capture_content_type_header is not None:
            self._values["capture_content_type_header"] = capture_content_type_header
        if enable_capture is not None:
            self._values["enable_capture"] = enable_capture
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def capture_options(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions"]]:
        '''capture_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_options SagemakerEndpointConfiguration#capture_options}
        '''
        result = self._values.get("capture_options")
        assert result is not None, "Required property 'capture_options' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions"]], result)

    @builtins.property
    def destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.'''
        result = self._values.get("destination_s3_uri")
        assert result is not None, "Required property 'destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_sampling_percentage(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_sampling_percentage SagemakerEndpointConfiguration#initial_sampling_percentage}.'''
        result = self._values.get("initial_sampling_percentage")
        assert result is not None, "Required property 'initial_sampling_percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def capture_content_type_header(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader"]:
        '''capture_content_type_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_content_type_header SagemakerEndpointConfiguration#capture_content_type_header}
        '''
        result = self._values.get("capture_content_type_header")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader"], result)

    @builtins.property
    def enable_capture(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#enable_capture SagemakerEndpointConfiguration#enable_capture}.'''
        result = self._values.get("enable_capture")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationDataCaptureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader",
    jsii_struct_bases=[],
    name_mapping={
        "csv_content_types": "csvContentTypes",
        "json_content_types": "jsonContentTypes",
    },
)
class SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader:
    def __init__(
        self,
        *,
        csv_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param csv_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#csv_content_types SagemakerEndpointConfiguration#csv_content_types}.
        :param json_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#json_content_types SagemakerEndpointConfiguration#json_content_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14fddbe6445dac48556f62969a5c092a3eacebebb68750eb1e1d4fc268acc52a)
            check_type(argname="argument csv_content_types", value=csv_content_types, expected_type=type_hints["csv_content_types"])
            check_type(argname="argument json_content_types", value=json_content_types, expected_type=type_hints["json_content_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv_content_types is not None:
            self._values["csv_content_types"] = csv_content_types
        if json_content_types is not None:
            self._values["json_content_types"] = json_content_types

    @builtins.property
    def csv_content_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#csv_content_types SagemakerEndpointConfiguration#csv_content_types}.'''
        result = self._values.get("csv_content_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def json_content_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#json_content_types SagemakerEndpointConfiguration#json_content_types}.'''
        result = self._values.get("json_content_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1054fb740e67b772a7ec6b676a3031c40d1ddba4d6ee4037f5ae0cce61b7f55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCsvContentTypes")
    def reset_csv_content_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvContentTypes", []))

    @jsii.member(jsii_name="resetJsonContentTypes")
    def reset_json_content_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonContentTypes", []))

    @builtins.property
    @jsii.member(jsii_name="csvContentTypesInput")
    def csv_content_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "csvContentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonContentTypesInput")
    def json_content_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jsonContentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="csvContentTypes")
    def csv_content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "csvContentTypes"))

    @csv_content_types.setter
    def csv_content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58e3f96238e746bcbaa9c4d3388f3e84cb8dd40e06288d90529cf69ee646f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "csvContentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonContentTypes")
    def json_content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jsonContentTypes"))

    @json_content_types.setter
    def json_content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb0220de442e7c96e7f561046b5bb6bc2243cc609c792f3034d38cc8e0e4392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonContentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259dff28d921e9333b2c704398a245eb7b56827819e4013ea0e6ea3a82e964f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions",
    jsii_struct_bases=[],
    name_mapping={"capture_mode": "captureMode"},
)
class SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions:
    def __init__(self, *, capture_mode: builtins.str) -> None:
        '''
        :param capture_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_mode SagemakerEndpointConfiguration#capture_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd21ea76fe37867a6dd7207eb5b15b1270736487ddcae38eb0835c1200364174)
            check_type(argname="argument capture_mode", value=capture_mode, expected_type=type_hints["capture_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capture_mode": capture_mode,
        }

    @builtins.property
    def capture_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#capture_mode SagemakerEndpointConfiguration#capture_mode}.'''
        result = self._values.get("capture_mode")
        assert result is not None, "Required property 'capture_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7693e4163672a262c660b52ae77a6755b2c919f693d835495282cdf92a88ca37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d09c2e0de3e7096a6493cbdbf76a528d967d1085af24f8980be9907a042b89)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e547ab958ab0a21b0a4719bf33230e5e47873b7ecd537203a53ed003402f58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61eddabeab928f7a6c3276adaf2d46d996f85ad33ddc06bb99ae74d9b3575fb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18f1d1dec673118a414c77f71b2c55f816eba070ba5e616a52d2a7a9a1fd3aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598d51ec3a091a7542729ba424dc7ea6dd1fce289534d334537bb0a774d91311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5a0e275f591b9abb74b2e0bf714a1033bf88c2f601173ff4de259d0660da95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="captureModeInput")
    def capture_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "captureModeInput"))

    @builtins.property
    @jsii.member(jsii_name="captureMode")
    def capture_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "captureMode"))

    @capture_mode.setter
    def capture_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf234fd2458211706496c1b2d313698fa9d6805d992fb4ced4f260911a244967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "captureMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a908812e073ae30a13f1b5a7d6d18f45563e38752654a6b7ac474c67b849526d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationDataCaptureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationDataCaptureConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c708d3f1fa0c7e0f0aed0699d95f2a6620a00541b914d2e2b3addbe45536463)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCaptureContentTypeHeader")
    def put_capture_content_type_header(
        self,
        *,
        csv_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        json_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param csv_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#csv_content_types SagemakerEndpointConfiguration#csv_content_types}.
        :param json_content_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#json_content_types SagemakerEndpointConfiguration#json_content_types}.
        '''
        value = SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader(
            csv_content_types=csv_content_types, json_content_types=json_content_types
        )

        return typing.cast(None, jsii.invoke(self, "putCaptureContentTypeHeader", [value]))

    @jsii.member(jsii_name="putCaptureOptions")
    def put_capture_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26249d86ca1c98502efe02db6764e465779a9b86035cea1f0858d94ed74ef7d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCaptureOptions", [value]))

    @jsii.member(jsii_name="resetCaptureContentTypeHeader")
    def reset_capture_content_type_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptureContentTypeHeader", []))

    @jsii.member(jsii_name="resetEnableCapture")
    def reset_enable_capture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableCapture", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="captureContentTypeHeader")
    def capture_content_type_header(
        self,
    ) -> SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference:
        return typing.cast(SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference, jsii.get(self, "captureContentTypeHeader"))

    @builtins.property
    @jsii.member(jsii_name="captureOptions")
    def capture_options(
        self,
    ) -> SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList:
        return typing.cast(SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList, jsii.get(self, "captureOptions"))

    @builtins.property
    @jsii.member(jsii_name="captureContentTypeHeaderInput")
    def capture_content_type_header_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader], jsii.get(self, "captureContentTypeHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="captureOptionsInput")
    def capture_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]], jsii.get(self, "captureOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3UriInput")
    def destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="enableCaptureInput")
    def enable_capture_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableCaptureInput"))

    @builtins.property
    @jsii.member(jsii_name="initialSamplingPercentageInput")
    def initial_sampling_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialSamplingPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3Uri")
    def destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationS3Uri"))

    @destination_s3_uri.setter
    def destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5f85becf11a201aa3367881da21637a005936f9fe48eaaa99d9b6f2d7cc6e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableCapture")
    def enable_capture(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableCapture"))

    @enable_capture.setter
    def enable_capture(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edca43fb4b9cb99979368f12b271c823f3ec18c6226e6d8063282a6cdf000df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCapture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialSamplingPercentage")
    def initial_sampling_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialSamplingPercentage"))

    @initial_sampling_percentage.setter
    def initial_sampling_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009b2ccc7c44b8c58827788e6917ef8dee2a593f2142ba57b35ff3d41f22b63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialSamplingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dab8a15393a07fe749cac62b99ced505b7c9e333bbf890c75d53e2a156f079e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55edf7c4ecbbea61f3edaff35308ff3ae9b20d4fdbb139243e578978bd63cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariants",
    jsii_struct_bases=[],
    name_mapping={
        "model_name": "modelName",
        "accelerator_type": "acceleratorType",
        "container_startup_health_check_timeout_in_seconds": "containerStartupHealthCheckTimeoutInSeconds",
        "core_dump_config": "coreDumpConfig",
        "enable_ssm_access": "enableSsmAccess",
        "inference_ami_version": "inferenceAmiVersion",
        "initial_instance_count": "initialInstanceCount",
        "initial_variant_weight": "initialVariantWeight",
        "instance_type": "instanceType",
        "managed_instance_scaling": "managedInstanceScaling",
        "model_data_download_timeout_in_seconds": "modelDataDownloadTimeoutInSeconds",
        "routing_config": "routingConfig",
        "serverless_config": "serverlessConfig",
        "variant_name": "variantName",
        "volume_size_in_gb": "volumeSizeInGb",
    },
)
class SagemakerEndpointConfigurationProductionVariants:
    def __init__(
        self,
        *,
        model_name: builtins.str,
        accelerator_type: typing.Optional[builtins.str] = None,
        container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        core_dump_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inference_ami_version: typing.Optional[builtins.str] = None,
        initial_instance_count: typing.Optional[jsii.Number] = None,
        initial_variant_weight: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[builtins.str] = None,
        managed_instance_scaling: typing.Optional[typing.Union["SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serverless_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationProductionVariantsServerlessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        variant_name: typing.Optional[builtins.str] = None,
        volume_size_in_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.
        :param accelerator_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.
        :param container_startup_health_check_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.
        :param core_dump_config: core_dump_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        :param enable_ssm_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.
        :param inference_ami_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.
        :param initial_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.
        :param initial_variant_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.
        :param managed_instance_scaling: managed_instance_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        :param model_data_download_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.
        :param routing_config: routing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        :param serverless_config: serverless_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        :param variant_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.
        '''
        if isinstance(core_dump_config, dict):
            core_dump_config = SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig(**core_dump_config)
        if isinstance(managed_instance_scaling, dict):
            managed_instance_scaling = SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling(**managed_instance_scaling)
        if isinstance(serverless_config, dict):
            serverless_config = SagemakerEndpointConfigurationProductionVariantsServerlessConfig(**serverless_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d0780f8f3c6a31b6ffc7228c7474b45c20464094621414fec68bb65b8174a1)
            check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument container_startup_health_check_timeout_in_seconds", value=container_startup_health_check_timeout_in_seconds, expected_type=type_hints["container_startup_health_check_timeout_in_seconds"])
            check_type(argname="argument core_dump_config", value=core_dump_config, expected_type=type_hints["core_dump_config"])
            check_type(argname="argument enable_ssm_access", value=enable_ssm_access, expected_type=type_hints["enable_ssm_access"])
            check_type(argname="argument inference_ami_version", value=inference_ami_version, expected_type=type_hints["inference_ami_version"])
            check_type(argname="argument initial_instance_count", value=initial_instance_count, expected_type=type_hints["initial_instance_count"])
            check_type(argname="argument initial_variant_weight", value=initial_variant_weight, expected_type=type_hints["initial_variant_weight"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument managed_instance_scaling", value=managed_instance_scaling, expected_type=type_hints["managed_instance_scaling"])
            check_type(argname="argument model_data_download_timeout_in_seconds", value=model_data_download_timeout_in_seconds, expected_type=type_hints["model_data_download_timeout_in_seconds"])
            check_type(argname="argument routing_config", value=routing_config, expected_type=type_hints["routing_config"])
            check_type(argname="argument serverless_config", value=serverless_config, expected_type=type_hints["serverless_config"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model_name": model_name,
        }
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if container_startup_health_check_timeout_in_seconds is not None:
            self._values["container_startup_health_check_timeout_in_seconds"] = container_startup_health_check_timeout_in_seconds
        if core_dump_config is not None:
            self._values["core_dump_config"] = core_dump_config
        if enable_ssm_access is not None:
            self._values["enable_ssm_access"] = enable_ssm_access
        if inference_ami_version is not None:
            self._values["inference_ami_version"] = inference_ami_version
        if initial_instance_count is not None:
            self._values["initial_instance_count"] = initial_instance_count
        if initial_variant_weight is not None:
            self._values["initial_variant_weight"] = initial_variant_weight
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if managed_instance_scaling is not None:
            self._values["managed_instance_scaling"] = managed_instance_scaling
        if model_data_download_timeout_in_seconds is not None:
            self._values["model_data_download_timeout_in_seconds"] = model_data_download_timeout_in_seconds
        if routing_config is not None:
            self._values["routing_config"] = routing_config
        if serverless_config is not None:
            self._values["serverless_config"] = serverless_config
        if variant_name is not None:
            self._values["variant_name"] = variant_name
        if volume_size_in_gb is not None:
            self._values["volume_size_in_gb"] = volume_size_in_gb

    @builtins.property
    def model_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.'''
        result = self._values.get("model_name")
        assert result is not None, "Required property 'model_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.'''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_startup_health_check_timeout_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.'''
        result = self._values.get("container_startup_health_check_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def core_dump_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig"]:
        '''core_dump_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        '''
        result = self._values.get("core_dump_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig"], result)

    @builtins.property
    def enable_ssm_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.'''
        result = self._values.get("enable_ssm_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inference_ami_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.'''
        result = self._values.get("inference_ami_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.'''
        result = self._values.get("initial_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def initial_variant_weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.'''
        result = self._values.get("initial_variant_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_instance_scaling(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling"]:
        '''managed_instance_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        '''
        result = self._values.get("managed_instance_scaling")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling"], result)

    @builtins.property
    def model_data_download_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.'''
        result = self._values.get("model_data_download_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def routing_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]]:
        '''routing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        '''
        result = self._values.get("routing_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]], result)

    @builtins.property
    def serverless_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"]:
        '''serverless_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        '''
        result = self._values.get("serverless_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"], result)

    @builtins.property
    def variant_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.'''
        result = self._values.get("variant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.'''
        result = self._values.get("volume_size_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariants(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig",
    jsii_struct_bases=[],
    name_mapping={"destination_s3_uri": "destinationS3Uri", "kms_key_id": "kmsKeyId"},
)
class SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig:
    def __init__(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d076aa9449b6dfab6d2b6377a6186f0a0f3a05ede9da2cd8ac0018aad5f768a7)
            check_type(argname="argument destination_s3_uri", value=destination_s3_uri, expected_type=type_hints["destination_s3_uri"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_s3_uri": destination_s3_uri,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.'''
        result = self._values.get("destination_s3_uri")
        assert result is not None, "Required property 'destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__756dea95ef85c12cc2b108690c94e29193aab84be02dd41d66f05966f19b2029)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="destinationS3UriInput")
    def destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3Uri")
    def destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationS3Uri"))

    @destination_s3_uri.setter
    def destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a9ad5cb74300bd120773468cfe3025fa94b0c99fbc412565c2fa07e5907ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7627ca9f730b30d23da6b719a22c16074502ad06153e242cae0adf157e6232f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b0c957d7e56a61321d5b7239441f1f3e31d81a4cb6662879e5f433907001d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationProductionVariantsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bf02daf220059865bfc99c83db124fb3bbe9ee8ce7f35e2e586122032206dc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationProductionVariantsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c90bc99ca2ce8e0b5c13ccad87a8e13f934b73e733296c40dadac4096396c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34a0bf317bcaadfc3ca0ebc0785779859250234fecac161d15af4c09c40207f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91454145ca0b67d7d766943bcb8b62af91f91609ee37ab76604f536f9cd0d500)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81d489665256be211488636aeb939235f147884174c7662cc4c6a7002d0f4aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3729606a811f71bcaee08636659a759926b2f9cd8b333f64f4dbfb3df29175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
        "status": "status",
    },
)
class SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling:
    def __init__(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ead371255661b36e9d2ffa4af6212901d6097b6fefd02427898fbf2b16f969)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.'''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.'''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__230c86111b1b6a3ad41c905626b77045c2b19810ef6c5008a670c00867df573b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0884854fb17c00cea1062e9fb285da6609694f62c023b37a0f60a83e3e7ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4011e28adf89521139a8f01ac48a1470bdbea06ccd5a13d36db19a70d4420911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057bd398dce9b25652f54c20fb6696ae86ad21b39fafa5ade65f8ae33deea778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b517c8e75cbd9fcd6aa93a58e50a5f1872fb52d8582d23a412029ea2cf3a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationProductionVariantsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0013d581f9aaf1b6f318e20b92a5ac0b9b6983f7b46e9ee20c27f4d291add4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCoreDumpConfig")
    def put_core_dump_config(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        value = SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig(
            destination_s3_uri=destination_s3_uri, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putCoreDumpConfig", [value]))

    @jsii.member(jsii_name="putManagedInstanceScaling")
    def put_managed_instance_scaling(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        value = SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedInstanceScaling", [value]))

    @jsii.member(jsii_name="putRoutingConfig")
    def put_routing_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e37caa3fc1e8b9a2b91e2a64a5beb1cfabd83858442f27438c3e90ff7d98664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoutingConfig", [value]))

    @jsii.member(jsii_name="putServerlessConfig")
    def put_serverless_config(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        value = SagemakerEndpointConfigurationProductionVariantsServerlessConfig(
            max_concurrency=max_concurrency,
            memory_size_in_mb=memory_size_in_mb,
            provisioned_concurrency=provisioned_concurrency,
        )

        return typing.cast(None, jsii.invoke(self, "putServerlessConfig", [value]))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetContainerStartupHealthCheckTimeoutInSeconds")
    def reset_container_startup_health_check_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerStartupHealthCheckTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetCoreDumpConfig")
    def reset_core_dump_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreDumpConfig", []))

    @jsii.member(jsii_name="resetEnableSsmAccess")
    def reset_enable_ssm_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSsmAccess", []))

    @jsii.member(jsii_name="resetInferenceAmiVersion")
    def reset_inference_ami_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceAmiVersion", []))

    @jsii.member(jsii_name="resetInitialInstanceCount")
    def reset_initial_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialInstanceCount", []))

    @jsii.member(jsii_name="resetInitialVariantWeight")
    def reset_initial_variant_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialVariantWeight", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetManagedInstanceScaling")
    def reset_managed_instance_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedInstanceScaling", []))

    @jsii.member(jsii_name="resetModelDataDownloadTimeoutInSeconds")
    def reset_model_data_download_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataDownloadTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetRoutingConfig")
    def reset_routing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingConfig", []))

    @jsii.member(jsii_name="resetServerlessConfig")
    def reset_serverless_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessConfig", []))

    @jsii.member(jsii_name="resetVariantName")
    def reset_variant_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariantName", []))

    @jsii.member(jsii_name="resetVolumeSizeInGb")
    def reset_volume_size_in_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSizeInGb", []))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfig")
    def core_dump_config(
        self,
    ) -> SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference, jsii.get(self, "coreDumpConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScaling")
    def managed_instance_scaling(
        self,
    ) -> SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference:
        return typing.cast(SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference, jsii.get(self, "managedInstanceScaling"))

    @builtins.property
    @jsii.member(jsii_name="routingConfig")
    def routing_config(
        self,
    ) -> "SagemakerEndpointConfigurationProductionVariantsRoutingConfigList":
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsRoutingConfigList", jsii.get(self, "routingConfig"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfig")
    def serverless_config(
        self,
    ) -> "SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference", jsii.get(self, "serverlessConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSecondsInput")
    def container_startup_health_check_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerStartupHealthCheckTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfigInput")
    def core_dump_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig], jsii.get(self, "coreDumpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccessInput")
    def enable_ssm_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSsmAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersionInput")
    def inference_ami_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inferenceAmiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCountInput")
    def initial_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeightInput")
    def initial_variant_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialVariantWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScalingInput")
    def managed_instance_scaling_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling], jsii.get(self, "managedInstanceScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSecondsInput")
    def model_data_download_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modelDataDownloadTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="modelNameInput")
    def model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingConfigInput")
    def routing_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationProductionVariantsRoutingConfig"]]], jsii.get(self, "routingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfigInput")
    def serverless_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationProductionVariantsServerlessConfig"], jsii.get(self, "serverlessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="variantNameInput")
    def variant_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGbInput")
    def volume_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7cf39cd8abae8df116edce08bdf7f91ba0d8a87865615a1c4d1de31e1cd26c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSeconds")
    def container_startup_health_check_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerStartupHealthCheckTimeoutInSeconds"))

    @container_startup_health_check_timeout_in_seconds.setter
    def container_startup_health_check_timeout_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe3f84b9fda0c01e9ed7d5b56ed1c8fb685fc95be9102918fe52aca49ef7dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerStartupHealthCheckTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccess")
    def enable_ssm_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSsmAccess"))

    @enable_ssm_access.setter
    def enable_ssm_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30a2f21a4ab8f34b5cc275ca72260b7f5c3bde30c57a7dc3eafbed7cdb1af0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSsmAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersion")
    def inference_ami_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inferenceAmiVersion"))

    @inference_ami_version.setter
    def inference_ami_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802a3f4dc9dd1eb0415c9018087244ddfa05905f8443de37052406d3e413a05d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceAmiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCount")
    def initial_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialInstanceCount"))

    @initial_instance_count.setter
    def initial_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b577907b9ab655dc72b5590834888c318e6d7c547e345427460a1783585bc5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeight")
    def initial_variant_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialVariantWeight"))

    @initial_variant_weight.setter
    def initial_variant_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca017976fe4b84725df70afe1e42abf64a0b219e31160ac536a72aec8c51463e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVariantWeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274830f1a0df265827c3cfb6a177b162496ea3e375a88e7bd9734bed46b70a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSeconds")
    def model_data_download_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "modelDataDownloadTimeoutInSeconds"))

    @model_data_download_timeout_in_seconds.setter
    def model_data_download_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86537127deebe57f54b9776092b7857718c6eb47478ded7348a140ebc8dcf981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataDownloadTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelName"))

    @model_name.setter
    def model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94765db5e4d080ba194d9e1ddb6a87103c5d07bb5a261e207ec8a300fe86d3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variantName")
    def variant_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variantName"))

    @variant_name.setter
    def variant_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88f02d1a7987dfd0dadd7b02f4e72a34a8f98e7f2c3c93e5407cf5b74cd4b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variantName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGb")
    def volume_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSizeInGb"))

    @volume_size_in_gb.setter
    def volume_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72882034d82ee8179711bc6feac177115d90a53df4a29b3b6de9c3c4ca3d5751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c5be31fd32f0ae0ee3f3f70f4e41d0d6c15db0e6045db5282e9ee8d80d7ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsRoutingConfig",
    jsii_struct_bases=[],
    name_mapping={"routing_strategy": "routingStrategy"},
)
class SagemakerEndpointConfigurationProductionVariantsRoutingConfig:
    def __init__(self, *, routing_strategy: builtins.str) -> None:
        '''
        :param routing_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353169f103c3c7c8ec3e939b016a4c29d0dcc9a1f825e45ea8579b2c7e20995a)
            check_type(argname="argument routing_strategy", value=routing_strategy, expected_type=type_hints["routing_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "routing_strategy": routing_strategy,
        }

    @builtins.property
    def routing_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.'''
        result = self._values.get("routing_strategy")
        assert result is not None, "Required property 'routing_strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsRoutingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsRoutingConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsRoutingConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__124b20644b49555b83f25e25764c4a237aed73ef5cd1eb1495fff7eddd5c7479)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a91120c46f9d2d6fc4273c5ba61d9e1b8dc2bdd5d6054e3aaaac7c78745ccd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e74841fb444fe7ca1d99320de947106c3eae7f046b725d4ce7741577d0c6c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bafb7e555ef097f295c3641450f0d055d352c1f6a6f88429b02e1fb1578b68af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21823e8dffed5a46bd28d2f1509a5aa7638c1285a6d7d24b21c8792fcfb54b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca55f9ae95e9aa8672f260d87ddad8b064a4e0f4dff57246be4be79fd63f77f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f26f51ee7ec79709eecda75c03734497878aa5d661d99f95325cb086556fade)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="routingStrategyInput")
    def routing_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="routingStrategy")
    def routing_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingStrategy"))

    @routing_strategy.setter
    def routing_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348de3f5f3f2d4aa031edc805b3379bd7f21232962103bcc1182da30c664885a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d79864a02a910ac8175828edb3e8c2ec41449222334dd9ce9a809c93ea8b92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsServerlessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrency": "maxConcurrency",
        "memory_size_in_mb": "memorySizeInMb",
        "provisioned_concurrency": "provisionedConcurrency",
    },
)
class SagemakerEndpointConfigurationProductionVariantsServerlessConfig:
    def __init__(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfe4354037be8b481f267a6f203076a98f02151679c69f77619e86510c1d9bc)
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument memory_size_in_mb", value=memory_size_in_mb, expected_type=type_hints["memory_size_in_mb"])
            check_type(argname="argument provisioned_concurrency", value=provisioned_concurrency, expected_type=type_hints["provisioned_concurrency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_concurrency": max_concurrency,
            "memory_size_in_mb": memory_size_in_mb,
        }
        if provisioned_concurrency is not None:
            self._values["provisioned_concurrency"] = provisioned_concurrency

    @builtins.property
    def max_concurrency(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.'''
        result = self._values.get("max_concurrency")
        assert result is not None, "Required property 'max_concurrency' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def memory_size_in_mb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.'''
        result = self._values.get("memory_size_in_mb")
        assert result is not None, "Required property 'memory_size_in_mb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def provisioned_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.'''
        result = self._values.get("provisioned_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationProductionVariantsServerlessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b06a9709d7da8372d5595c48701336df594760b36b9c67e5d53d1e89492eb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProvisionedConcurrency")
    def reset_provisioned_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedConcurrency", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyInput")
    def max_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMbInput")
    def memory_size_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyInput")
    def provisioned_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrency")
    def max_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrency"))

    @max_concurrency.setter
    def max_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2a7b6ff55840d4b075b47bfc24ac5fba88523044cafffff0722bba00555406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMb")
    def memory_size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInMb"))

    @memory_size_in_mb.setter
    def memory_size_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d41fc6a7eb2ab535f7378047f5163ea107d2c1dc715d09b7fbea575b295e5db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrency")
    def provisioned_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedConcurrency"))

    @provisioned_concurrency.setter
    def provisioned_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6869accca223885730e65c29a6819cca3d1df3d459d019bbfdf441e1811318df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37041801e08c53ac59d9289fbab25eb59ca3c620ec86da0130a55bfd57386b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariants",
    jsii_struct_bases=[],
    name_mapping={
        "model_name": "modelName",
        "accelerator_type": "acceleratorType",
        "container_startup_health_check_timeout_in_seconds": "containerStartupHealthCheckTimeoutInSeconds",
        "core_dump_config": "coreDumpConfig",
        "enable_ssm_access": "enableSsmAccess",
        "inference_ami_version": "inferenceAmiVersion",
        "initial_instance_count": "initialInstanceCount",
        "initial_variant_weight": "initialVariantWeight",
        "instance_type": "instanceType",
        "managed_instance_scaling": "managedInstanceScaling",
        "model_data_download_timeout_in_seconds": "modelDataDownloadTimeoutInSeconds",
        "routing_config": "routingConfig",
        "serverless_config": "serverlessConfig",
        "variant_name": "variantName",
        "volume_size_in_gb": "volumeSizeInGb",
    },
)
class SagemakerEndpointConfigurationShadowProductionVariants:
    def __init__(
        self,
        *,
        model_name: builtins.str,
        accelerator_type: typing.Optional[builtins.str] = None,
        container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        core_dump_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inference_ami_version: typing.Optional[builtins.str] = None,
        initial_instance_count: typing.Optional[jsii.Number] = None,
        initial_variant_weight: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[builtins.str] = None,
        managed_instance_scaling: typing.Optional[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serverless_config: typing.Optional[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        variant_name: typing.Optional[builtins.str] = None,
        volume_size_in_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.
        :param accelerator_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.
        :param container_startup_health_check_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.
        :param core_dump_config: core_dump_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        :param enable_ssm_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.
        :param inference_ami_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.
        :param initial_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.
        :param initial_variant_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.
        :param managed_instance_scaling: managed_instance_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        :param model_data_download_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.
        :param routing_config: routing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        :param serverless_config: serverless_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        :param variant_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.
        :param volume_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.
        '''
        if isinstance(core_dump_config, dict):
            core_dump_config = SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig(**core_dump_config)
        if isinstance(managed_instance_scaling, dict):
            managed_instance_scaling = SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling(**managed_instance_scaling)
        if isinstance(serverless_config, dict):
            serverless_config = SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig(**serverless_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01391016e396c324c4f94244d3c38ee88ee45365d696ae1a033340076fe2a1e7)
            check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument container_startup_health_check_timeout_in_seconds", value=container_startup_health_check_timeout_in_seconds, expected_type=type_hints["container_startup_health_check_timeout_in_seconds"])
            check_type(argname="argument core_dump_config", value=core_dump_config, expected_type=type_hints["core_dump_config"])
            check_type(argname="argument enable_ssm_access", value=enable_ssm_access, expected_type=type_hints["enable_ssm_access"])
            check_type(argname="argument inference_ami_version", value=inference_ami_version, expected_type=type_hints["inference_ami_version"])
            check_type(argname="argument initial_instance_count", value=initial_instance_count, expected_type=type_hints["initial_instance_count"])
            check_type(argname="argument initial_variant_weight", value=initial_variant_weight, expected_type=type_hints["initial_variant_weight"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument managed_instance_scaling", value=managed_instance_scaling, expected_type=type_hints["managed_instance_scaling"])
            check_type(argname="argument model_data_download_timeout_in_seconds", value=model_data_download_timeout_in_seconds, expected_type=type_hints["model_data_download_timeout_in_seconds"])
            check_type(argname="argument routing_config", value=routing_config, expected_type=type_hints["routing_config"])
            check_type(argname="argument serverless_config", value=serverless_config, expected_type=type_hints["serverless_config"])
            check_type(argname="argument variant_name", value=variant_name, expected_type=type_hints["variant_name"])
            check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model_name": model_name,
        }
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if container_startup_health_check_timeout_in_seconds is not None:
            self._values["container_startup_health_check_timeout_in_seconds"] = container_startup_health_check_timeout_in_seconds
        if core_dump_config is not None:
            self._values["core_dump_config"] = core_dump_config
        if enable_ssm_access is not None:
            self._values["enable_ssm_access"] = enable_ssm_access
        if inference_ami_version is not None:
            self._values["inference_ami_version"] = inference_ami_version
        if initial_instance_count is not None:
            self._values["initial_instance_count"] = initial_instance_count
        if initial_variant_weight is not None:
            self._values["initial_variant_weight"] = initial_variant_weight
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if managed_instance_scaling is not None:
            self._values["managed_instance_scaling"] = managed_instance_scaling
        if model_data_download_timeout_in_seconds is not None:
            self._values["model_data_download_timeout_in_seconds"] = model_data_download_timeout_in_seconds
        if routing_config is not None:
            self._values["routing_config"] = routing_config
        if serverless_config is not None:
            self._values["serverless_config"] = serverless_config
        if variant_name is not None:
            self._values["variant_name"] = variant_name
        if volume_size_in_gb is not None:
            self._values["volume_size_in_gb"] = volume_size_in_gb

    @builtins.property
    def model_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_name SagemakerEndpointConfiguration#model_name}.'''
        result = self._values.get("model_name")
        assert result is not None, "Required property 'model_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#accelerator_type SagemakerEndpointConfiguration#accelerator_type}.'''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_startup_health_check_timeout_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#container_startup_health_check_timeout_in_seconds SagemakerEndpointConfiguration#container_startup_health_check_timeout_in_seconds}.'''
        result = self._values.get("container_startup_health_check_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def core_dump_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig"]:
        '''core_dump_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#core_dump_config SagemakerEndpointConfiguration#core_dump_config}
        '''
        result = self._values.get("core_dump_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig"], result)

    @builtins.property
    def enable_ssm_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#enable_ssm_access SagemakerEndpointConfiguration#enable_ssm_access}.'''
        result = self._values.get("enable_ssm_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inference_ami_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#inference_ami_version SagemakerEndpointConfiguration#inference_ami_version}.'''
        result = self._values.get("inference_ami_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_instance_count SagemakerEndpointConfiguration#initial_instance_count}.'''
        result = self._values.get("initial_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def initial_variant_weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#initial_variant_weight SagemakerEndpointConfiguration#initial_variant_weight}.'''
        result = self._values.get("initial_variant_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#instance_type SagemakerEndpointConfiguration#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_instance_scaling(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling"]:
        '''managed_instance_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#managed_instance_scaling SagemakerEndpointConfiguration#managed_instance_scaling}
        '''
        result = self._values.get("managed_instance_scaling")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling"], result)

    @builtins.property
    def model_data_download_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#model_data_download_timeout_in_seconds SagemakerEndpointConfiguration#model_data_download_timeout_in_seconds}.'''
        result = self._values.get("model_data_download_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def routing_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]]:
        '''routing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_config SagemakerEndpointConfiguration#routing_config}
        '''
        result = self._values.get("routing_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]], result)

    @builtins.property
    def serverless_config(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"]:
        '''serverless_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#serverless_config SagemakerEndpointConfiguration#serverless_config}
        '''
        result = self._values.get("serverless_config")
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"], result)

    @builtins.property
    def variant_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#variant_name SagemakerEndpointConfiguration#variant_name}.'''
        result = self._values.get("variant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#volume_size_in_gb SagemakerEndpointConfiguration#volume_size_in_gb}.'''
        result = self._values.get("volume_size_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariants(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig",
    jsii_struct_bases=[],
    name_mapping={"destination_s3_uri": "destinationS3Uri", "kms_key_id": "kmsKeyId"},
)
class SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig:
    def __init__(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: builtins.str,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6dfd6cb4d35ec343ed42baae5d196c969e23bd96d7c66133b9671f51ce92f9d)
            check_type(argname="argument destination_s3_uri", value=destination_s3_uri, expected_type=type_hints["destination_s3_uri"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_s3_uri": destination_s3_uri,
            "kms_key_id": kms_key_id,
        }

    @builtins.property
    def destination_s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.'''
        result = self._values.get("destination_s3_uri")
        assert result is not None, "Required property 'destination_s3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        assert result is not None, "Required property 'kms_key_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab23a65ca3ff452ab32c97e00e2f6cbc13050007411df71a017fea4f6a8d11fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationS3UriInput")
    def destination_s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationS3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationS3Uri")
    def destination_s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationS3Uri"))

    @destination_s3_uri.setter
    def destination_s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42d8455bf249779fa95ebfeeeb07432e09d07359ab5b7d6556ed4efc62fb393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationS3Uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c3cd9d9c01b4df72065f0589aa406169a511bafac425e2e6fb5f69ce72a55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cd8b253f4088a94b9fe0293ff097b5596e08bc64c8e23c865e1ec0553cf433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationShadowProductionVariantsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__515b0f815c978f8648e9ecd589c4c4cdf571275e78a06a850282c8af5d95a16f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b0267ea00388c071b07c786e98b5cf2e68205ab56237d59d670b1ac47d75e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e8d030a069e6dedcd48e5bdaf9da4b55f57b20c45bfcec850c5cb8d793e8c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93a5e639f75bfe7bf6fb8d06ef4096f0c3e89c219c411debe83ad262c6f7de4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad930078ece8117197bd05dd8e727d8521e4110702c9d01c961116e93c21392e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d9b1b979f7d24a1c20bf558ffacb8bc3c97e1e02cafc8b5bc7724212ff8114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
        "status": "status",
    },
)
class SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling:
    def __init__(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af40dd4d0353f58c1f0d26f4289982fa3f3602a0f7c8e4293e563c9cbaf76a5)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.'''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.'''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__841934a64462b4b5cb753b9929c2f6ad7caa7bcac5ae83be063ad42e2aad5693)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55256a92854d1a548eb6c2914dd8826356ed0ad80face16de759d50734f508ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d9b94f9eefa1e0929d8cc817f14fd0adf410606ad6a4d4a81597980656415c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d8f21685ad920bf8b47b3c2c3ddfcf0ba94f4831b30cebd6b9719791f6dfc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5b698f194b8affd19a2c807da47ab9de8fc259bf601e1d748ca4f0eee98c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationShadowProductionVariantsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfb65ea03a1c37e9e67db70dd1cc7122aa0f23c614af20954b68cdd32f539361)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCoreDumpConfig")
    def put_core_dump_config(
        self,
        *,
        destination_s3_uri: builtins.str,
        kms_key_id: builtins.str,
    ) -> None:
        '''
        :param destination_s3_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#destination_s3_uri SagemakerEndpointConfiguration#destination_s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#kms_key_id SagemakerEndpointConfiguration#kms_key_id}.
        '''
        value = SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig(
            destination_s3_uri=destination_s3_uri, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putCoreDumpConfig", [value]))

    @jsii.member(jsii_name="putManagedInstanceScaling")
    def put_managed_instance_scaling(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_instance_count SagemakerEndpointConfiguration#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#min_instance_count SagemakerEndpointConfiguration#min_instance_count}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#status SagemakerEndpointConfiguration#status}.
        '''
        value = SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedInstanceScaling", [value]))

    @jsii.member(jsii_name="putRoutingConfig")
    def put_routing_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f8bf238e9e562ed6cd1ca99178f3344db5f2f088fb6428e8c583858cedf0d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoutingConfig", [value]))

    @jsii.member(jsii_name="putServerlessConfig")
    def put_serverless_config(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        value = SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig(
            max_concurrency=max_concurrency,
            memory_size_in_mb=memory_size_in_mb,
            provisioned_concurrency=provisioned_concurrency,
        )

        return typing.cast(None, jsii.invoke(self, "putServerlessConfig", [value]))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetContainerStartupHealthCheckTimeoutInSeconds")
    def reset_container_startup_health_check_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerStartupHealthCheckTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetCoreDumpConfig")
    def reset_core_dump_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreDumpConfig", []))

    @jsii.member(jsii_name="resetEnableSsmAccess")
    def reset_enable_ssm_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSsmAccess", []))

    @jsii.member(jsii_name="resetInferenceAmiVersion")
    def reset_inference_ami_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceAmiVersion", []))

    @jsii.member(jsii_name="resetInitialInstanceCount")
    def reset_initial_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialInstanceCount", []))

    @jsii.member(jsii_name="resetInitialVariantWeight")
    def reset_initial_variant_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialVariantWeight", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetManagedInstanceScaling")
    def reset_managed_instance_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedInstanceScaling", []))

    @jsii.member(jsii_name="resetModelDataDownloadTimeoutInSeconds")
    def reset_model_data_download_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataDownloadTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetRoutingConfig")
    def reset_routing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingConfig", []))

    @jsii.member(jsii_name="resetServerlessConfig")
    def reset_serverless_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessConfig", []))

    @jsii.member(jsii_name="resetVariantName")
    def reset_variant_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariantName", []))

    @jsii.member(jsii_name="resetVolumeSizeInGb")
    def reset_volume_size_in_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSizeInGb", []))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfig")
    def core_dump_config(
        self,
    ) -> SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference:
        return typing.cast(SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference, jsii.get(self, "coreDumpConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScaling")
    def managed_instance_scaling(
        self,
    ) -> SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference:
        return typing.cast(SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference, jsii.get(self, "managedInstanceScaling"))

    @builtins.property
    @jsii.member(jsii_name="routingConfig")
    def routing_config(
        self,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList":
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList", jsii.get(self, "routingConfig"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfig")
    def serverless_config(
        self,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference":
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference", jsii.get(self, "serverlessConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSecondsInput")
    def container_startup_health_check_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerStartupHealthCheckTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="coreDumpConfigInput")
    def core_dump_config_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig], jsii.get(self, "coreDumpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccessInput")
    def enable_ssm_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSsmAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersionInput")
    def inference_ami_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inferenceAmiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCountInput")
    def initial_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeightInput")
    def initial_variant_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialVariantWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceScalingInput")
    def managed_instance_scaling_input(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling], jsii.get(self, "managedInstanceScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSecondsInput")
    def model_data_download_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modelDataDownloadTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="modelNameInput")
    def model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingConfigInput")
    def routing_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig"]]], jsii.get(self, "routingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessConfigInput")
    def serverless_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig"], jsii.get(self, "serverlessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="variantNameInput")
    def variant_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGbInput")
    def volume_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3859701340fc904919146f7b9409934b000476613d3e3d2b02740835947b9f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerStartupHealthCheckTimeoutInSeconds")
    def container_startup_health_check_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerStartupHealthCheckTimeoutInSeconds"))

    @container_startup_health_check_timeout_in_seconds.setter
    def container_startup_health_check_timeout_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ba468c537f23ef0ec0e16a3c4de4ec041a6c2d8e5c0f80b228745d520f9479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerStartupHealthCheckTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSsmAccess")
    def enable_ssm_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSsmAccess"))

    @enable_ssm_access.setter
    def enable_ssm_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6278e258d48c09909d7abf48ec543383503fe73f106805562b4c572da3abd40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSsmAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inferenceAmiVersion")
    def inference_ami_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inferenceAmiVersion"))

    @inference_ami_version.setter
    def inference_ami_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d330d70e83bf5696de53bf06801f5c4986d2d8d444c307ecf96b5b574ec8f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceAmiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialInstanceCount")
    def initial_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialInstanceCount"))

    @initial_instance_count.setter
    def initial_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673c339c283e9f6a4b2bee987c7f5d63df3ea4114c51297fc4d1b9567f6c4701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialVariantWeight")
    def initial_variant_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialVariantWeight"))

    @initial_variant_weight.setter
    def initial_variant_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b079b21173a723d7129e1a2065babc0240603b09d69ce0305b29d65bb0755f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVariantWeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d066606a5e3fe3d90332bb41be4f303c59b486d6c6844a6b0d9fccba977b94e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDataDownloadTimeoutInSeconds")
    def model_data_download_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "modelDataDownloadTimeoutInSeconds"))

    @model_data_download_timeout_in_seconds.setter
    def model_data_download_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4fa079ebbaaab6d3dc555916e3b1332677b0f55e3f28b2f58b7764aafff88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataDownloadTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelName"))

    @model_name.setter
    def model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec33cae5869d80dc8dab8358211e69e42385be79b57581035ca21c6eb58be23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variantName")
    def variant_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variantName"))

    @variant_name.setter
    def variant_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec5c135375a8df80a7956653b2fcae544538a18a3602b4cd38d6c47b7a7a86b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variantName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInGb")
    def volume_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSizeInGb"))

    @volume_size_in_gb.setter
    def volume_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358eed37f0fbc0726f382dc2ee2776f1841dfb0bfb094f1bbd53f00aa4ee3711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc2a4cd5042c39ac7393e49d25d39eff4ef09fd2309952236ca50b3e7bdfe29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig",
    jsii_struct_bases=[],
    name_mapping={"routing_strategy": "routingStrategy"},
)
class SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig:
    def __init__(self, *, routing_strategy: builtins.str) -> None:
        '''
        :param routing_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45021756c826ffd6233c864ec16c0d07c4e69967aa3d2ce0b307ea1cdc616f0)
            check_type(argname="argument routing_strategy", value=routing_strategy, expected_type=type_hints["routing_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "routing_strategy": routing_strategy,
        }

    @builtins.property
    def routing_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#routing_strategy SagemakerEndpointConfiguration#routing_strategy}.'''
        result = self._values.get("routing_strategy")
        assert result is not None, "Required property 'routing_strategy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6474202133306cc0a53974cd6e2d36deea7dbbb7b9afd5a26b4acdadb4da8610)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5124366d6db31808b4ab147eb50ee4d62f7f8d76497f99c287048d2897891eec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1435fa79ab90b871ebf17ab556002ec9a788d5817a8e53a7040c6b847dae2f34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ead107b7b0ec2a0e4d65aeb530d83188c9a68699dc062511bc5ce8a96af9e3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__846a7aa7582d5d65e851c137c2fa6adb8e5b536e78b80b02b1669b1b666fcb7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c248e2cf48c2564511aa8d3e51df54f80eef81e059fd4204551e2f3ad63c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d7d2c210b54517b19071cede0374464b19103e5aa3c051e1890271e5be33ea9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="routingStrategyInput")
    def routing_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="routingStrategy")
    def routing_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingStrategy"))

    @routing_strategy.setter
    def routing_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4110d0fb8ea6a702d4c29d935a80e17e612ac37c8988a4131495f895abfd6597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e34e26336dcd07f7fa67d6d9001202b4404087dc4ece514f5a64fd7733b515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrency": "maxConcurrency",
        "memory_size_in_mb": "memorySizeInMb",
        "provisioned_concurrency": "provisionedConcurrency",
    },
)
class SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig:
    def __init__(
        self,
        *,
        max_concurrency: jsii.Number,
        memory_size_in_mb: jsii.Number,
        provisioned_concurrency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.
        :param memory_size_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.
        :param provisioned_concurrency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f4a8f984366965f3aa8f5838f8a9dd93300ff93e1449e86c5c5220f0ac42eb)
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument memory_size_in_mb", value=memory_size_in_mb, expected_type=type_hints["memory_size_in_mb"])
            check_type(argname="argument provisioned_concurrency", value=provisioned_concurrency, expected_type=type_hints["provisioned_concurrency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_concurrency": max_concurrency,
            "memory_size_in_mb": memory_size_in_mb,
        }
        if provisioned_concurrency is not None:
            self._values["provisioned_concurrency"] = provisioned_concurrency

    @builtins.property
    def max_concurrency(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#max_concurrency SagemakerEndpointConfiguration#max_concurrency}.'''
        result = self._values.get("max_concurrency")
        assert result is not None, "Required property 'max_concurrency' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def memory_size_in_mb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#memory_size_in_mb SagemakerEndpointConfiguration#memory_size_in_mb}.'''
        result = self._values.get("memory_size_in_mb")
        assert result is not None, "Required property 'memory_size_in_mb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def provisioned_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint_configuration#provisioned_concurrency SagemakerEndpointConfiguration#provisioned_concurrency}.'''
        result = self._values.get("provisioned_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpointConfiguration.SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17a94b88a2ecabe2198e3ffcd332b975169d3a7675a50e637be3c9012981e640)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProvisionedConcurrency")
    def reset_provisioned_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedConcurrency", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyInput")
    def max_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMbInput")
    def memory_size_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyInput")
    def provisioned_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrency")
    def max_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrency"))

    @max_concurrency.setter
    def max_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18242f5d69746aee8bb7c610bd3d9a4e72c5a965a662a2ff95e1453558ce0682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeInMb")
    def memory_size_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInMb"))

    @memory_size_in_mb.setter
    def memory_size_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af2cb36c9ad2c6068d5428a5d68c75130df597fd068ec42675fdfbacd91cc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrency")
    def provisioned_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedConcurrency"))

    @provisioned_concurrency.setter
    def provisioned_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b22a747fd6336a0400a1d6d2466537a3d61b3008f5b87538fe66b0ca37c58a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b9a5b6b93c614a0022bceb391a21ffbbbc32e209685d5b93cf29994c0f61ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerEndpointConfiguration",
    "SagemakerEndpointConfigurationAsyncInferenceConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigClientConfigOutputReference",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfigOutputReference",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigOutputReference",
    "SagemakerEndpointConfigurationAsyncInferenceConfigOutputReference",
    "SagemakerEndpointConfigurationConfig",
    "SagemakerEndpointConfigurationDataCaptureConfig",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeaderOutputReference",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsList",
    "SagemakerEndpointConfigurationDataCaptureConfigCaptureOptionsOutputReference",
    "SagemakerEndpointConfigurationDataCaptureConfigOutputReference",
    "SagemakerEndpointConfigurationProductionVariants",
    "SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig",
    "SagemakerEndpointConfigurationProductionVariantsCoreDumpConfigOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsList",
    "SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling",
    "SagemakerEndpointConfigurationProductionVariantsManagedInstanceScalingOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsRoutingConfig",
    "SagemakerEndpointConfigurationProductionVariantsRoutingConfigList",
    "SagemakerEndpointConfigurationProductionVariantsRoutingConfigOutputReference",
    "SagemakerEndpointConfigurationProductionVariantsServerlessConfig",
    "SagemakerEndpointConfigurationProductionVariantsServerlessConfigOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariants",
    "SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig",
    "SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfigOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsList",
    "SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling",
    "SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScalingOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig",
    "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigList",
    "SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfigOutputReference",
    "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig",
    "SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfigOutputReference",
]

publication.publish()

def _typecheckingstub__400ab2f4777265a946b6b8276b052755086c5de235865af9ee8aab00f21da3e1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
    async_inference_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    data_capture_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationDataCaptureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariants, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__c119146cf009e7d5862bb5a12e6f71424c6c8ec40e93de2cb2fb5418105db8dd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8802dbe0982b4f40b7e562c738d89c0f9fffac7c5e654624f677a09af78d2b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3928d439f0992d35785ab0ce88003b92b0dc06b075a1b993cd6207e9ee6a150d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6793aa42fd735bbcb9ab21b676b88cbf35b06301f6af1e6dbb4187360c4c271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b112001cbd47306082da082eddcb81f532d0c129efeac5b169631379c3885eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5dbac074b12dfdec031c2ade8a58926274741f40921c3fe15d6de17a9d9891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96003ecd8d1d8ccc47ef6cf4373de007321dd807337e8e8c96b75837ae9bcf3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6899621cd811d0d0e644aad4077aded9eeeda2bdcda191ca219cfeab5c82540(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88fb26b73e193784bc9c17458fe5ae1c15ecc0887ec71a66d45257d807a3f99(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541333f3f17c0529299347be153f3621f2bc1e7ac2eea503741c3f7b9c14b2e6(
    *,
    output_config: typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig, typing.Dict[builtins.str, typing.Any]],
    client_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783605fe56ba8b2713e1157214d3797f8c0fcadce21cc398f2e043ac3d71ea5f(
    *,
    max_concurrent_invocations_per_instance: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e3d35b6c05ac5e62ca6d80a041710038ef0fd0c0d40ed3a141efa0035ef951(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a6815e28ef0868d6c2e9bc5d44c3607a2be6c6fc0c65f26b6e4f13f75553a0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d3c24b548b6b2707c6c1165090ea14587896d61d40615d4c6ee2189ddc253d(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigClientConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d793e1f69c472ad192d35481e677327ba8b1ec7d9b35d9c0dfbf3500927914(
    *,
    s3_output_path: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_failure_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d32fc8df0086d95be699e9c9ee144b21afd21163f8235e33d87ba17398f4674(
    *,
    error_topic: typing.Optional[builtins.str] = None,
    include_inference_response_in: typing.Optional[typing.Sequence[builtins.str]] = None,
    success_topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e313cbbea936e34aca6fd959c0a96ef7ff029ab7b581711d5a34da5e5c29eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d8d34f22cb6b3038e675bdefdfa0ae65eb0f7c4fcb2f3f7d94de7c0d173424(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907c4f8786fb12b4c84a0c3e2b0719db9f21e311c047b94b082d18163a04fe6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b55b569a6e40d673539b91394b290abe45ca61dc698beaaa687c6019994fa3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a737f164ba6e9fecdba481e5d4d84d92847cab535b39b30f896edaf19d3cc45(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfigNotificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e1ae962545e83c29bd983799fa9ca3983b5dd003cbb8ceea392774517d19c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81241a130d5f95f33250c4bb8b628de648e836d8b7715ad31789c3094889a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c50de6d3d25bb36a5f158ca6a00b3fa1cac632819330c0f47e0c3f2c83a7de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a911f81caff2636d0148980dbb50f0219a5798593d98626403fff4ee0190ddf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91d821bf21632803e7bfacf8be0706c7f48062eacbf5f0301780d591c6cbeb0(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfigOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2746889b420d793d9edea295b0619c77195f557985274e362ffb8a478da2b8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492553ec3743af75a9b600557959767c915b12c3c92a68c95f426045f79fdf59(
    value: typing.Optional[SagemakerEndpointConfigurationAsyncInferenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef24afb957de9c40da6864604adacf6f822a5eefe8dc09dd46c7147fb23cdf40(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    production_variants: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariants, typing.Dict[builtins.str, typing.Any]]]],
    async_inference_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationAsyncInferenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    data_capture_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationDataCaptureConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    shadow_production_variants: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariants, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734bc0c9e881259aa2e8b6b019c29d47812de8ed8cdd0682d0397b15bbede200(
    *,
    capture_options: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions, typing.Dict[builtins.str, typing.Any]]]],
    destination_s3_uri: builtins.str,
    initial_sampling_percentage: jsii.Number,
    capture_content_type_header: typing.Optional[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_capture: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fddbe6445dac48556f62969a5c092a3eacebebb68750eb1e1d4fc268acc52a(
    *,
    csv_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1054fb740e67b772a7ec6b676a3031c40d1ddba4d6ee4037f5ae0cce61b7f55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58e3f96238e746bcbaa9c4d3388f3e84cb8dd40e06288d90529cf69ee646f56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb0220de442e7c96e7f561046b5bb6bc2243cc609c792f3034d38cc8e0e4392(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259dff28d921e9333b2c704398a245eb7b56827819e4013ea0e6ea3a82e964f9(
    value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfigCaptureContentTypeHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd21ea76fe37867a6dd7207eb5b15b1270736487ddcae38eb0835c1200364174(
    *,
    capture_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7693e4163672a262c660b52ae77a6755b2c919f693d835495282cdf92a88ca37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d09c2e0de3e7096a6493cbdbf76a528d967d1085af24f8980be9907a042b89(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e547ab958ab0a21b0a4719bf33230e5e47873b7ecd537203a53ed003402f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61eddabeab928f7a6c3276adaf2d46d996f85ad33ddc06bb99ae74d9b3575fb1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f1d1dec673118a414c77f71b2c55f816eba070ba5e616a52d2a7a9a1fd3aea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598d51ec3a091a7542729ba424dc7ea6dd1fce289534d334537bb0a774d91311(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5a0e275f591b9abb74b2e0bf714a1033bf88c2f601173ff4de259d0660da95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf234fd2458211706496c1b2d313698fa9d6805d992fb4ced4f260911a244967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a908812e073ae30a13f1b5a7d6d18f45563e38752654a6b7ac474c67b849526d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c708d3f1fa0c7e0f0aed0699d95f2a6620a00541b914d2e2b3addbe45536463(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26249d86ca1c98502efe02db6764e465779a9b86035cea1f0858d94ed74ef7d3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationDataCaptureConfigCaptureOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5f85becf11a201aa3367881da21637a005936f9fe48eaaa99d9b6f2d7cc6e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edca43fb4b9cb99979368f12b271c823f3ec18c6226e6d8063282a6cdf000df7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009b2ccc7c44b8c58827788e6917ef8dee2a593f2142ba57b35ff3d41f22b63c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dab8a15393a07fe749cac62b99ced505b7c9e333bbf890c75d53e2a156f079e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55edf7c4ecbbea61f3edaff35308ff3ae9b20d4fdbb139243e578978bd63cce(
    value: typing.Optional[SagemakerEndpointConfigurationDataCaptureConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d0780f8f3c6a31b6ffc7228c7474b45c20464094621414fec68bb65b8174a1(
    *,
    model_name: builtins.str,
    accelerator_type: typing.Optional[builtins.str] = None,
    container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    core_dump_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inference_ami_version: typing.Optional[builtins.str] = None,
    initial_instance_count: typing.Optional[jsii.Number] = None,
    initial_variant_weight: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    managed_instance_scaling: typing.Optional[typing.Union[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    serverless_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationProductionVariantsServerlessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    variant_name: typing.Optional[builtins.str] = None,
    volume_size_in_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d076aa9449b6dfab6d2b6377a6186f0a0f3a05ede9da2cd8ac0018aad5f768a7(
    *,
    destination_s3_uri: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756dea95ef85c12cc2b108690c94e29193aab84be02dd41d66f05966f19b2029(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a9ad5cb74300bd120773468cfe3025fa94b0c99fbc412565c2fa07e5907ad2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7627ca9f730b30d23da6b719a22c16074502ad06153e242cae0adf157e6232f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b0c957d7e56a61321d5b7239441f1f3e31d81a4cb6662879e5f433907001d9(
    value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsCoreDumpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf02daf220059865bfc99c83db124fb3bbe9ee8ce7f35e2e586122032206dc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c90bc99ca2ce8e0b5c13ccad87a8e13f934b73e733296c40dadac4096396c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34a0bf317bcaadfc3ca0ebc0785779859250234fecac161d15af4c09c40207f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91454145ca0b67d7d766943bcb8b62af91f91609ee37ab76604f536f9cd0d500(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d489665256be211488636aeb939235f147884174c7662cc4c6a7002d0f4aa0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3729606a811f71bcaee08636659a759926b2f9cd8b333f64f4dbfb3df29175(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariants]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ead371255661b36e9d2ffa4af6212901d6097b6fefd02427898fbf2b16f969(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230c86111b1b6a3ad41c905626b77045c2b19810ef6c5008a670c00867df573b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0884854fb17c00cea1062e9fb285da6609694f62c023b37a0f60a83e3e7ceb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4011e28adf89521139a8f01ac48a1470bdbea06ccd5a13d36db19a70d4420911(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057bd398dce9b25652f54c20fb6696ae86ad21b39fafa5ade65f8ae33deea778(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b517c8e75cbd9fcd6aa93a58e50a5f1872fb52d8582d23a412029ea2cf3a5f(
    value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsManagedInstanceScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0013d581f9aaf1b6f318e20b92a5ac0b9b6983f7b46e9ee20c27f4d291add4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e37caa3fc1e8b9a2b91e2a64a5beb1cfabd83858442f27438c3e90ff7d98664(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7cf39cd8abae8df116edce08bdf7f91ba0d8a87865615a1c4d1de31e1cd26c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe3f84b9fda0c01e9ed7d5b56ed1c8fb685fc95be9102918fe52aca49ef7dab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30a2f21a4ab8f34b5cc275ca72260b7f5c3bde30c57a7dc3eafbed7cdb1af0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802a3f4dc9dd1eb0415c9018087244ddfa05905f8443de37052406d3e413a05d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b577907b9ab655dc72b5590834888c318e6d7c547e345427460a1783585bc5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca017976fe4b84725df70afe1e42abf64a0b219e31160ac536a72aec8c51463e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274830f1a0df265827c3cfb6a177b162496ea3e375a88e7bd9734bed46b70a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86537127deebe57f54b9776092b7857718c6eb47478ded7348a140ebc8dcf981(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94765db5e4d080ba194d9e1ddb6a87103c5d07bb5a261e207ec8a300fe86d3c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88f02d1a7987dfd0dadd7b02f4e72a34a8f98e7f2c3c93e5407cf5b74cd4b86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72882034d82ee8179711bc6feac177115d90a53df4a29b3b6de9c3c4ca3d5751(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c5be31fd32f0ae0ee3f3f70f4e41d0d6c15db0e6045db5282e9ee8d80d7ea9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariants]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353169f103c3c7c8ec3e939b016a4c29d0dcc9a1f825e45ea8579b2c7e20995a(
    *,
    routing_strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124b20644b49555b83f25e25764c4a237aed73ef5cd1eb1495fff7eddd5c7479(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a91120c46f9d2d6fc4273c5ba61d9e1b8dc2bdd5d6054e3aaaac7c78745ccd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e74841fb444fe7ca1d99320de947106c3eae7f046b725d4ce7741577d0c6c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafb7e555ef097f295c3641450f0d055d352c1f6a6f88429b02e1fb1578b68af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21823e8dffed5a46bd28d2f1509a5aa7638c1285a6d7d24b21c8792fcfb54b4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca55f9ae95e9aa8672f260d87ddad8b064a4e0f4dff57246be4be79fd63f77f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationProductionVariantsRoutingConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f26f51ee7ec79709eecda75c03734497878aa5d661d99f95325cb086556fade(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348de3f5f3f2d4aa031edc805b3379bd7f21232962103bcc1182da30c664885a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d79864a02a910ac8175828edb3e8c2ec41449222334dd9ce9a809c93ea8b92f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationProductionVariantsRoutingConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfe4354037be8b481f267a6f203076a98f02151679c69f77619e86510c1d9bc(
    *,
    max_concurrency: jsii.Number,
    memory_size_in_mb: jsii.Number,
    provisioned_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b06a9709d7da8372d5595c48701336df594760b36b9c67e5d53d1e89492eb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2a7b6ff55840d4b075b47bfc24ac5fba88523044cafffff0722bba00555406(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d41fc6a7eb2ab535f7378047f5163ea107d2c1dc715d09b7fbea575b295e5db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6869accca223885730e65c29a6819cca3d1df3d459d019bbfdf441e1811318df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37041801e08c53ac59d9289fbab25eb59ca3c620ec86da0130a55bfd57386b2f(
    value: typing.Optional[SagemakerEndpointConfigurationProductionVariantsServerlessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01391016e396c324c4f94244d3c38ee88ee45365d696ae1a033340076fe2a1e7(
    *,
    model_name: builtins.str,
    accelerator_type: typing.Optional[builtins.str] = None,
    container_startup_health_check_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    core_dump_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_ssm_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inference_ami_version: typing.Optional[builtins.str] = None,
    initial_instance_count: typing.Optional[jsii.Number] = None,
    initial_variant_weight: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    managed_instance_scaling: typing.Optional[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    model_data_download_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    routing_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    serverless_config: typing.Optional[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    variant_name: typing.Optional[builtins.str] = None,
    volume_size_in_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6dfd6cb4d35ec343ed42baae5d196c969e23bd96d7c66133b9671f51ce92f9d(
    *,
    destination_s3_uri: builtins.str,
    kms_key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab23a65ca3ff452ab32c97e00e2f6cbc13050007411df71a017fea4f6a8d11fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42d8455bf249779fa95ebfeeeb07432e09d07359ab5b7d6556ed4efc62fb393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c3cd9d9c01b4df72065f0589aa406169a511bafac425e2e6fb5f69ce72a55f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cd8b253f4088a94b9fe0293ff097b5596e08bc64c8e23c865e1ec0553cf433(
    value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsCoreDumpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515b0f815c978f8648e9ecd589c4c4cdf571275e78a06a850282c8af5d95a16f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b0267ea00388c071b07c786e98b5cf2e68205ab56237d59d670b1ac47d75e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e8d030a069e6dedcd48e5bdaf9da4b55f57b20c45bfcec850c5cb8d793e8c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a5e639f75bfe7bf6fb8d06ef4096f0c3e89c219c411debe83ad262c6f7de4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad930078ece8117197bd05dd8e727d8521e4110702c9d01c961116e93c21392e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d9b1b979f7d24a1c20bf558ffacb8bc3c97e1e02cafc8b5bc7724212ff8114(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariants]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af40dd4d0353f58c1f0d26f4289982fa3f3602a0f7c8e4293e563c9cbaf76a5(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841934a64462b4b5cb753b9929c2f6ad7caa7bcac5ae83be063ad42e2aad5693(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55256a92854d1a548eb6c2914dd8826356ed0ad80face16de759d50734f508ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d9b94f9eefa1e0929d8cc817f14fd0adf410606ad6a4d4a81597980656415c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d8f21685ad920bf8b47b3c2c3ddfcf0ba94f4831b30cebd6b9719791f6dfc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5b698f194b8affd19a2c807da47ab9de8fc259bf601e1d748ca4f0eee98c9d(
    value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsManagedInstanceScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb65ea03a1c37e9e67db70dd1cc7122aa0f23c614af20954b68cdd32f539361(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f8bf238e9e562ed6cd1ca99178f3344db5f2f088fb6428e8c583858cedf0d1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3859701340fc904919146f7b9409934b000476613d3e3d2b02740835947b9f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ba468c537f23ef0ec0e16a3c4de4ec041a6c2d8e5c0f80b228745d520f9479(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6278e258d48c09909d7abf48ec543383503fe73f106805562b4c572da3abd40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d330d70e83bf5696de53bf06801f5c4986d2d8d444c307ecf96b5b574ec8f0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673c339c283e9f6a4b2bee987c7f5d63df3ea4114c51297fc4d1b9567f6c4701(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b079b21173a723d7129e1a2065babc0240603b09d69ce0305b29d65bb0755f5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d066606a5e3fe3d90332bb41be4f303c59b486d6c6844a6b0d9fccba977b94e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4fa079ebbaaab6d3dc555916e3b1332677b0f55e3f28b2f58b7764aafff88f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec33cae5869d80dc8dab8358211e69e42385be79b57581035ca21c6eb58be23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec5c135375a8df80a7956653b2fcae544538a18a3602b4cd38d6c47b7a7a86b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358eed37f0fbc0726f382dc2ee2776f1841dfb0bfb094f1bbd53f00aa4ee3711(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc2a4cd5042c39ac7393e49d25d39eff4ef09fd2309952236ca50b3e7bdfe29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariants]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45021756c826ffd6233c864ec16c0d07c4e69967aa3d2ce0b307ea1cdc616f0(
    *,
    routing_strategy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6474202133306cc0a53974cd6e2d36deea7dbbb7b9afd5a26b4acdadb4da8610(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5124366d6db31808b4ab147eb50ee4d62f7f8d76497f99c287048d2897891eec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1435fa79ab90b871ebf17ab556002ec9a788d5817a8e53a7040c6b847dae2f34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ead107b7b0ec2a0e4d65aeb530d83188c9a68699dc062511bc5ce8a96af9e3d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846a7aa7582d5d65e851c137c2fa6adb8e5b536e78b80b02b1669b1b666fcb7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c248e2cf48c2564511aa8d3e51df54f80eef81e059fd4204551e2f3ad63c9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7d2c210b54517b19071cede0374464b19103e5aa3c051e1890271e5be33ea9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4110d0fb8ea6a702d4c29d935a80e17e612ac37c8988a4131495f895abfd6597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e34e26336dcd07f7fa67d6d9001202b4404087dc4ece514f5a64fd7733b515(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointConfigurationShadowProductionVariantsRoutingConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f4a8f984366965f3aa8f5838f8a9dd93300ff93e1449e86c5c5220f0ac42eb(
    *,
    max_concurrency: jsii.Number,
    memory_size_in_mb: jsii.Number,
    provisioned_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a94b88a2ecabe2198e3ffcd332b975169d3a7675a50e637be3c9012981e640(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18242f5d69746aee8bb7c610bd3d9a4e72c5a965a662a2ff95e1453558ce0682(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af2cb36c9ad2c6068d5428a5d68c75130df597fd068ec42675fdfbacd91cc87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b22a747fd6336a0400a1d6d2466537a3d61b3008f5b87538fe66b0ca37c58a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b9a5b6b93c614a0022bceb391a21ffbbbc32e209685d5b93cf29994c0f61ba(
    value: typing.Optional[SagemakerEndpointConfigurationShadowProductionVariantsServerlessConfig],
) -> None:
    """Type checking stubs"""
    pass
