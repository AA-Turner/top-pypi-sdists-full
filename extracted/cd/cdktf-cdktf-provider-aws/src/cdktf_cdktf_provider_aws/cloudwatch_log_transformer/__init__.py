r'''
# `aws_cloudwatch_log_transformer`

Refer to the Terraform Registry for docs: [`aws_cloudwatch_log_transformer`](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer).
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


class CloudwatchLogTransformer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer aws_cloudwatch_log_transformer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group_arn: builtins.str,
        region: typing.Optional[builtins.str] = None,
        transformer_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer aws_cloudwatch_log_transformer} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#log_group_arn CloudwatchLogTransformer#log_group_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#region CloudwatchLogTransformer#region}
        :param transformer_config: transformer_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#transformer_config CloudwatchLogTransformer#transformer_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c36969cc39a3712e08b49439f37abfaa97a91da915b31a7fc8675034b887755)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CloudwatchLogTransformerConfig(
            log_group_arn=log_group_arn,
            region=region,
            transformer_config=transformer_config,
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
        '''Generates CDKTF code for importing a CloudwatchLogTransformer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudwatchLogTransformer to import.
        :param import_from_id: The id of the existing CloudwatchLogTransformer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudwatchLogTransformer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6204bff60aa4592e2ded4ff755210de54ca1a587f42a658a199b8ee5df7367d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTransformerConfig")
    def put_transformer_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b89437e4d33e6db26a83bbb31cc4749dccbb3f4fc2d3832f5010293a375d809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransformerConfig", [value]))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTransformerConfig")
    def reset_transformer_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformerConfig", []))

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
    @jsii.member(jsii_name="transformerConfig")
    def transformer_config(self) -> "CloudwatchLogTransformerTransformerConfigList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigList", jsii.get(self, "transformerConfig"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="transformerConfigInput")
    def transformer_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfig"]]], jsii.get(self, "transformerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5067f04ce3c8f32cbcbac5aae47a5c10c4cb2ad4c19b5a22d4d24506c8176f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3042dc25f6d7cd2b6338039c0273c3dfa7a8a6ef8327b1dc1904165405ba0ff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "log_group_arn": "logGroupArn",
        "region": "region",
        "transformer_config": "transformerConfig",
    },
)
class CloudwatchLogTransformerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        log_group_arn: builtins.str,
        region: typing.Optional[builtins.str] = None,
        transformer_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#log_group_arn CloudwatchLogTransformer#log_group_arn}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#region CloudwatchLogTransformer#region}
        :param transformer_config: transformer_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#transformer_config CloudwatchLogTransformer#transformer_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1812fb2d38fd4c3d3860135319e49d0171a220eb97d89bafcc81455aa5f3493)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument transformer_config", value=transformer_config, expected_type=type_hints["transformer_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_arn": log_group_arn,
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
        if region is not None:
            self._values["region"] = region
        if transformer_config is not None:
            self._values["transformer_config"] = transformer_config

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
    def log_group_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#log_group_arn CloudwatchLogTransformer#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        assert result is not None, "Required property 'log_group_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#region CloudwatchLogTransformer#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transformer_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfig"]]]:
        '''transformer_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#transformer_config CloudwatchLogTransformer#transformer_config}
        '''
        result = self._values.get("transformer_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "add_keys": "addKeys",
        "copy_value": "copyValue",
        "csv": "csv",
        "date_time_converter": "dateTimeConverter",
        "delete_keys": "deleteKeys",
        "grok": "grok",
        "list_to_map": "listToMap",
        "lower_case_string": "lowerCaseString",
        "move_keys": "moveKeys",
        "parse_cloudfront": "parseCloudfront",
        "parse_json": "parseJson",
        "parse_key_value": "parseKeyValue",
        "parse_postgres": "parsePostgres",
        "parse_route53": "parseRoute53",
        "parse_to_ocsf": "parseToOcsf",
        "parse_vpc": "parseVpc",
        "parse_waf": "parseWaf",
        "rename_keys": "renameKeys",
        "split_string": "splitString",
        "substitute_string": "substituteString",
        "trim_string": "trimString",
        "type_converter": "typeConverter",
        "upper_case_string": "upperCaseString",
    },
)
class CloudwatchLogTransformerTransformerConfig:
    def __init__(
        self,
        *,
        add_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigAddKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        copy_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigCopyValue", typing.Dict[builtins.str, typing.Any]]]]] = None,
        csv: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigCsv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        date_time_converter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigDateTimeConverter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        delete_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigDeleteKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        grok: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigGrok", typing.Dict[builtins.str, typing.Any]]]]] = None,
        list_to_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigListToMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lower_case_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigLowerCaseString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        move_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigMoveKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_cloudfront: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseCloudfront", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseJson", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_key_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseKeyValue", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_postgres: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParsePostgres", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_route53: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseRoute53", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_to_ocsf: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseToOcsf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_vpc: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseVpc", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_waf: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseWaf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rename_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigRenameKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        split_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigSplitString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        substitute_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigSubstituteString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trim_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigTrimString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type_converter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigTypeConverter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        upper_case_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigUpperCaseString", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param add_keys: add_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#add_keys CloudwatchLogTransformer#add_keys}
        :param copy_value: copy_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#copy_value CloudwatchLogTransformer#copy_value}
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#csv CloudwatchLogTransformer#csv}
        :param date_time_converter: date_time_converter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#date_time_converter CloudwatchLogTransformer#date_time_converter}
        :param delete_keys: delete_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#delete_keys CloudwatchLogTransformer#delete_keys}
        :param grok: grok block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#grok CloudwatchLogTransformer#grok}
        :param list_to_map: list_to_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#list_to_map CloudwatchLogTransformer#list_to_map}
        :param lower_case_string: lower_case_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#lower_case_string CloudwatchLogTransformer#lower_case_string}
        :param move_keys: move_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#move_keys CloudwatchLogTransformer#move_keys}
        :param parse_cloudfront: parse_cloudfront block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_cloudfront CloudwatchLogTransformer#parse_cloudfront}
        :param parse_json: parse_json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_json CloudwatchLogTransformer#parse_json}
        :param parse_key_value: parse_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_key_value CloudwatchLogTransformer#parse_key_value}
        :param parse_postgres: parse_postgres block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_postgres CloudwatchLogTransformer#parse_postgres}
        :param parse_route53: parse_route53 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_route53 CloudwatchLogTransformer#parse_route53}
        :param parse_to_ocsf: parse_to_ocsf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_to_ocsf CloudwatchLogTransformer#parse_to_ocsf}
        :param parse_vpc: parse_vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_vpc CloudwatchLogTransformer#parse_vpc}
        :param parse_waf: parse_waf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_waf CloudwatchLogTransformer#parse_waf}
        :param rename_keys: rename_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#rename_keys CloudwatchLogTransformer#rename_keys}
        :param split_string: split_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#split_string CloudwatchLogTransformer#split_string}
        :param substitute_string: substitute_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#substitute_string CloudwatchLogTransformer#substitute_string}
        :param trim_string: trim_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#trim_string CloudwatchLogTransformer#trim_string}
        :param type_converter: type_converter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#type_converter CloudwatchLogTransformer#type_converter}
        :param upper_case_string: upper_case_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#upper_case_string CloudwatchLogTransformer#upper_case_string}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914d5b1e5db99c195fbc4e8ab2cf154404a9b541779bd303440e943aca27e17c)
            check_type(argname="argument add_keys", value=add_keys, expected_type=type_hints["add_keys"])
            check_type(argname="argument copy_value", value=copy_value, expected_type=type_hints["copy_value"])
            check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            check_type(argname="argument date_time_converter", value=date_time_converter, expected_type=type_hints["date_time_converter"])
            check_type(argname="argument delete_keys", value=delete_keys, expected_type=type_hints["delete_keys"])
            check_type(argname="argument grok", value=grok, expected_type=type_hints["grok"])
            check_type(argname="argument list_to_map", value=list_to_map, expected_type=type_hints["list_to_map"])
            check_type(argname="argument lower_case_string", value=lower_case_string, expected_type=type_hints["lower_case_string"])
            check_type(argname="argument move_keys", value=move_keys, expected_type=type_hints["move_keys"])
            check_type(argname="argument parse_cloudfront", value=parse_cloudfront, expected_type=type_hints["parse_cloudfront"])
            check_type(argname="argument parse_json", value=parse_json, expected_type=type_hints["parse_json"])
            check_type(argname="argument parse_key_value", value=parse_key_value, expected_type=type_hints["parse_key_value"])
            check_type(argname="argument parse_postgres", value=parse_postgres, expected_type=type_hints["parse_postgres"])
            check_type(argname="argument parse_route53", value=parse_route53, expected_type=type_hints["parse_route53"])
            check_type(argname="argument parse_to_ocsf", value=parse_to_ocsf, expected_type=type_hints["parse_to_ocsf"])
            check_type(argname="argument parse_vpc", value=parse_vpc, expected_type=type_hints["parse_vpc"])
            check_type(argname="argument parse_waf", value=parse_waf, expected_type=type_hints["parse_waf"])
            check_type(argname="argument rename_keys", value=rename_keys, expected_type=type_hints["rename_keys"])
            check_type(argname="argument split_string", value=split_string, expected_type=type_hints["split_string"])
            check_type(argname="argument substitute_string", value=substitute_string, expected_type=type_hints["substitute_string"])
            check_type(argname="argument trim_string", value=trim_string, expected_type=type_hints["trim_string"])
            check_type(argname="argument type_converter", value=type_converter, expected_type=type_hints["type_converter"])
            check_type(argname="argument upper_case_string", value=upper_case_string, expected_type=type_hints["upper_case_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_keys is not None:
            self._values["add_keys"] = add_keys
        if copy_value is not None:
            self._values["copy_value"] = copy_value
        if csv is not None:
            self._values["csv"] = csv
        if date_time_converter is not None:
            self._values["date_time_converter"] = date_time_converter
        if delete_keys is not None:
            self._values["delete_keys"] = delete_keys
        if grok is not None:
            self._values["grok"] = grok
        if list_to_map is not None:
            self._values["list_to_map"] = list_to_map
        if lower_case_string is not None:
            self._values["lower_case_string"] = lower_case_string
        if move_keys is not None:
            self._values["move_keys"] = move_keys
        if parse_cloudfront is not None:
            self._values["parse_cloudfront"] = parse_cloudfront
        if parse_json is not None:
            self._values["parse_json"] = parse_json
        if parse_key_value is not None:
            self._values["parse_key_value"] = parse_key_value
        if parse_postgres is not None:
            self._values["parse_postgres"] = parse_postgres
        if parse_route53 is not None:
            self._values["parse_route53"] = parse_route53
        if parse_to_ocsf is not None:
            self._values["parse_to_ocsf"] = parse_to_ocsf
        if parse_vpc is not None:
            self._values["parse_vpc"] = parse_vpc
        if parse_waf is not None:
            self._values["parse_waf"] = parse_waf
        if rename_keys is not None:
            self._values["rename_keys"] = rename_keys
        if split_string is not None:
            self._values["split_string"] = split_string
        if substitute_string is not None:
            self._values["substitute_string"] = substitute_string
        if trim_string is not None:
            self._values["trim_string"] = trim_string
        if type_converter is not None:
            self._values["type_converter"] = type_converter
        if upper_case_string is not None:
            self._values["upper_case_string"] = upper_case_string

    @builtins.property
    def add_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigAddKeys"]]]:
        '''add_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#add_keys CloudwatchLogTransformer#add_keys}
        '''
        result = self._values.get("add_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigAddKeys"]]], result)

    @builtins.property
    def copy_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigCopyValue"]]]:
        '''copy_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#copy_value CloudwatchLogTransformer#copy_value}
        '''
        result = self._values.get("copy_value")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigCopyValue"]]], result)

    @builtins.property
    def csv(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigCsv"]]]:
        '''csv block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#csv CloudwatchLogTransformer#csv}
        '''
        result = self._values.get("csv")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigCsv"]]], result)

    @builtins.property
    def date_time_converter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigDateTimeConverter"]]]:
        '''date_time_converter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#date_time_converter CloudwatchLogTransformer#date_time_converter}
        '''
        result = self._values.get("date_time_converter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigDateTimeConverter"]]], result)

    @builtins.property
    def delete_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigDeleteKeys"]]]:
        '''delete_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#delete_keys CloudwatchLogTransformer#delete_keys}
        '''
        result = self._values.get("delete_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigDeleteKeys"]]], result)

    @builtins.property
    def grok(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigGrok"]]]:
        '''grok block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#grok CloudwatchLogTransformer#grok}
        '''
        result = self._values.get("grok")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigGrok"]]], result)

    @builtins.property
    def list_to_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigListToMap"]]]:
        '''list_to_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#list_to_map CloudwatchLogTransformer#list_to_map}
        '''
        result = self._values.get("list_to_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigListToMap"]]], result)

    @builtins.property
    def lower_case_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigLowerCaseString"]]]:
        '''lower_case_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#lower_case_string CloudwatchLogTransformer#lower_case_string}
        '''
        result = self._values.get("lower_case_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigLowerCaseString"]]], result)

    @builtins.property
    def move_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigMoveKeys"]]]:
        '''move_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#move_keys CloudwatchLogTransformer#move_keys}
        '''
        result = self._values.get("move_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigMoveKeys"]]], result)

    @builtins.property
    def parse_cloudfront(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseCloudfront"]]]:
        '''parse_cloudfront block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_cloudfront CloudwatchLogTransformer#parse_cloudfront}
        '''
        result = self._values.get("parse_cloudfront")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseCloudfront"]]], result)

    @builtins.property
    def parse_json(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseJson"]]]:
        '''parse_json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_json CloudwatchLogTransformer#parse_json}
        '''
        result = self._values.get("parse_json")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseJson"]]], result)

    @builtins.property
    def parse_key_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseKeyValue"]]]:
        '''parse_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_key_value CloudwatchLogTransformer#parse_key_value}
        '''
        result = self._values.get("parse_key_value")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseKeyValue"]]], result)

    @builtins.property
    def parse_postgres(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParsePostgres"]]]:
        '''parse_postgres block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_postgres CloudwatchLogTransformer#parse_postgres}
        '''
        result = self._values.get("parse_postgres")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParsePostgres"]]], result)

    @builtins.property
    def parse_route53(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseRoute53"]]]:
        '''parse_route53 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_route53 CloudwatchLogTransformer#parse_route53}
        '''
        result = self._values.get("parse_route53")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseRoute53"]]], result)

    @builtins.property
    def parse_to_ocsf(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseToOcsf"]]]:
        '''parse_to_ocsf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_to_ocsf CloudwatchLogTransformer#parse_to_ocsf}
        '''
        result = self._values.get("parse_to_ocsf")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseToOcsf"]]], result)

    @builtins.property
    def parse_vpc(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseVpc"]]]:
        '''parse_vpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_vpc CloudwatchLogTransformer#parse_vpc}
        '''
        result = self._values.get("parse_vpc")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseVpc"]]], result)

    @builtins.property
    def parse_waf(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseWaf"]]]:
        '''parse_waf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#parse_waf CloudwatchLogTransformer#parse_waf}
        '''
        result = self._values.get("parse_waf")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseWaf"]]], result)

    @builtins.property
    def rename_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigRenameKeys"]]]:
        '''rename_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#rename_keys CloudwatchLogTransformer#rename_keys}
        '''
        result = self._values.get("rename_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigRenameKeys"]]], result)

    @builtins.property
    def split_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSplitString"]]]:
        '''split_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#split_string CloudwatchLogTransformer#split_string}
        '''
        result = self._values.get("split_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSplitString"]]], result)

    @builtins.property
    def substitute_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSubstituteString"]]]:
        '''substitute_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#substitute_string CloudwatchLogTransformer#substitute_string}
        '''
        result = self._values.get("substitute_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSubstituteString"]]], result)

    @builtins.property
    def trim_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTrimString"]]]:
        '''trim_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#trim_string CloudwatchLogTransformer#trim_string}
        '''
        result = self._values.get("trim_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTrimString"]]], result)

    @builtins.property
    def type_converter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTypeConverter"]]]:
        '''type_converter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#type_converter CloudwatchLogTransformer#type_converter}
        '''
        result = self._values.get("type_converter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTypeConverter"]]], result)

    @builtins.property
    def upper_case_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigUpperCaseString"]]]:
        '''upper_case_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#upper_case_string CloudwatchLogTransformer#upper_case_string}
        '''
        result = self._values.get("upper_case_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigUpperCaseString"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigAddKeys",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry"},
)
class CloudwatchLogTransformerTransformerConfigAddKeys:
    def __init__(
        self,
        *,
        entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigAddKeysEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entry: entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fed55d03c26775187137d06980797ee3ccccafb31dc48260c069e4932108daf)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry is not None:
            self._values["entry"] = entry

    @builtins.property
    def entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigAddKeysEntry"]]]:
        '''entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigAddKeysEntry"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigAddKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigAddKeysEntry",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "value": "value",
        "overwrite_if_exists": "overwriteIfExists",
    },
)
class CloudwatchLogTransformerTransformerConfigAddKeysEntry:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#value CloudwatchLogTransformer#value}.
        :param overwrite_if_exists: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae3b47fe61f71ff6c54247b4ddf3bb267bf33bff13b3bc4e6fc5b5436db7e0f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if overwrite_if_exists is not None:
            self._values["overwrite_if_exists"] = overwrite_if_exists

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#value CloudwatchLogTransformer#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overwrite_if_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.'''
        result = self._values.get("overwrite_if_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigAddKeysEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigAddKeysEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigAddKeysEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__542ad670ae56bfc3b52f62af263b621a38b5d740e1335fc4403a7b7e369f0d1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigAddKeysEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e894e20bb48ed2f72812a9df194994d8ba5f9ba84fed16f03d750ccc5137cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigAddKeysEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c52d8eb6f4aca11f1fcfc73f1e37ef242895a1f198060943c93393a95ce0e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd1affb74e796fd9afe5d37f6497a2ee19d57955113c2345707ec8856b559db8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4bbc4e861c67f30c1cc8540e7353bc85593b41367c52269b6a4bc46b6009028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeysEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeysEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeysEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d794f68027b3916c403070526e48c5305032f4818a410a33e166243b32055ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigAddKeysEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigAddKeysEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__405d48d8586614d8e4fdbc743f6365dd6c97bfcbdee112aca64b2548ac9a2065)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOverwriteIfExists")
    def reset_overwrite_if_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteIfExists", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExistsInput")
    def overwrite_if_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteIfExistsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ef35d304919b48635a1c30f784cc9ec0bf13f36c347d17f562cf8e55792c6080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExists")
    def overwrite_if_exists(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteIfExists"))

    @overwrite_if_exists.setter
    def overwrite_if_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d56cdbd27900e303d0cac18c91e17dcea20c340cb5eef14e958fe2319f4039a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteIfExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002568abd4c8d91c89dd41b566941279e01ed15e0480f7c60c21e08204d78b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeysEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeysEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeysEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506224493c62b90f96f8ba627815b30e2c33241ccdf7554353caecd18d9a80af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigAddKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigAddKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57577fcd721742e699a8af562664dd532c376721bc24c70fe546d4e0bbda5d48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigAddKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be6bb448584d3040a66ccd09323aa3c6f621629f229a41db444b16e73854a6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigAddKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba6e6dcde3a116b6aed2fa8464e1516910cb31792bce71254767ef6f9170794)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0399706d1460b043f54b8464ccdba84351bc48c79de4feb83175f0581a122ae0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc5026ca4c0404c4d3aee57eb67a32ff978a6e6c6f860ccd7c87535feb39c59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fda2c9b29fcd19f0ae2e7ec730044be209a16ea79cea474a3d833a84c136a7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigAddKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigAddKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1119c426f3738d7f9eebcec2a2f3d5588ee343c76b015af1aa03b09aea78442f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEntry")
    def put_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigAddKeysEntry, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1f7961a9962723a6088c072f6dfe067abbfb72860944dd859415cc9de4fd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntry", [value]))

    @jsii.member(jsii_name="resetEntry")
    def reset_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntry", []))

    @builtins.property
    @jsii.member(jsii_name="entry")
    def entry(self) -> CloudwatchLogTransformerTransformerConfigAddKeysEntryList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigAddKeysEntryList, jsii.get(self, "entry"))

    @builtins.property
    @jsii.member(jsii_name="entryInput")
    def entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeysEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeysEntry]]], jsii.get(self, "entryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de9cce377581421eeaf4d346efda68ace0a475fe815deb113297416749c4030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCopyValue",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry"},
)
class CloudwatchLogTransformerTransformerConfigCopyValue:
    def __init__(
        self,
        *,
        entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigCopyValueEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entry: entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0649b40eac7a06e1d2fd23286c029a612b131cbe9a9c6a02fea433f031c8c29e)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry is not None:
            self._values["entry"] = entry

    @builtins.property
    def entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigCopyValueEntry"]]]:
        '''entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigCopyValueEntry"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigCopyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCopyValueEntry",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "target": "target",
        "overwrite_if_exists": "overwriteIfExists",
    },
)
class CloudwatchLogTransformerTransformerConfigCopyValueEntry:
    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.
        :param overwrite_if_exists: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78989d51b605a65ec09e0f1665e21f8020a7f77039322f7437bcf9589ab85750)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }
        if overwrite_if_exists is not None:
            self._values["overwrite_if_exists"] = overwrite_if_exists

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overwrite_if_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.'''
        result = self._values.get("overwrite_if_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigCopyValueEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigCopyValueEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCopyValueEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a696db04289ea8b7fba15d69b18b6c3fa1abff64b1cc7a75d53f7d0f124e967b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigCopyValueEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7529a4a30a358d0eff845f9e641259316e7d058d54f165ff7ede57fc00e8d591)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigCopyValueEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2827130ba63ada66e9e8e2751bfeea4ec82954ab1789fa396b13c31a8767de8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1d8795d35cbbdde01078392ebe03e968b74967cda3de8dbefe361d25667ab6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__919535d1edacd5555f6978f440ef2c6af1c244f2c82baf7691a158b16d2e5dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValueEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValueEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValueEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076ae7cb4f0ff3dc1a14dc2a58dba92d8a8be2265881c7b65be683701fff75f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigCopyValueEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCopyValueEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__244985696f6348dc46878e42ba1eca03c29af77dace8dbc637a16577d9ecf717)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOverwriteIfExists")
    def reset_overwrite_if_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteIfExists", []))

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExistsInput")
    def overwrite_if_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteIfExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExists")
    def overwrite_if_exists(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteIfExists"))

    @overwrite_if_exists.setter
    def overwrite_if_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88456b787cd33a3658eefb746aee9e9ffee062dbf12413cae1dc156d43395ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteIfExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a7639ced8a817810ba3a75463c9ffb63ac460338a0fd8ff518c7edf0e329ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6d055fbdf4b1796a9a5bf7569d2c49919ca647d60b997a271aed1e4cc64733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValueEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValueEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValueEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496b5f50a2129b6814dd887130ac622dca4183be83b60270ca897989faee8feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigCopyValueList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCopyValueList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6d866877af6f5c727116fdefec29131f3eaf97fdd59d6de8a9bf7c0c74ce31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigCopyValueOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5433d3388eb1f9a55dca94eaee558048f71e5369665f1d2f5408eff5dca8fb28)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigCopyValueOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b48ab01f3b3118df166e891f481d876f6eb02f34a6cd3adcb96f3af2e597a5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99d73eb6ca2f78ab477f35cf853878115ed3197b9af5f631da4f02732fb4e143)
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
            type_hints = typing.get_type_hints(_typecheckingstub__543bab7ae042bffa8bae4817a6655f619c347f84c4c14980c0c5d6a7bc7da733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValue]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValue]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValue]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f001349d1a404b923ca5e932d7f5964a51244946e675ea3ec36abe3629e33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigCopyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCopyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3433715805a8bc26e0d2be67a06bdf3dffd91e99a90fa479e1cf6ce5c78bfc8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEntry")
    def put_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCopyValueEntry, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49555e49f42a20fbfa61faee360c2bb03784658a8e018ee995860f19ba2f919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntry", [value]))

    @jsii.member(jsii_name="resetEntry")
    def reset_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntry", []))

    @builtins.property
    @jsii.member(jsii_name="entry")
    def entry(self) -> CloudwatchLogTransformerTransformerConfigCopyValueEntryList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigCopyValueEntryList, jsii.get(self, "entry"))

    @builtins.property
    @jsii.member(jsii_name="entryInput")
    def entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValueEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValueEntry]]], jsii.get(self, "entryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValue]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValue]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValue]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7aca0c690c462224e0ffd69edd3dc1dbb67e5e27d9c3fa19f206f75361efdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCsv",
    jsii_struct_bases=[],
    name_mapping={
        "columns": "columns",
        "delimiter": "delimiter",
        "quote_character": "quoteCharacter",
        "source": "source",
    },
)
class CloudwatchLogTransformerTransformerConfigCsv:
    def __init__(
        self,
        *,
        columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        quote_character: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#columns CloudwatchLogTransformer#columns}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#delimiter CloudwatchLogTransformer#delimiter}.
        :param quote_character: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#quote_character CloudwatchLogTransformer#quote_character}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d554579a52894a9a10756bcccb6c6ed418248967e551759a7fa212be45f62f)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument quote_character", value=quote_character, expected_type=type_hints["quote_character"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if columns is not None:
            self._values["columns"] = columns
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if quote_character is not None:
            self._values["quote_character"] = quote_character
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def columns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#columns CloudwatchLogTransformer#columns}.'''
        result = self._values.get("columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#delimiter CloudwatchLogTransformer#delimiter}.'''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quote_character(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#quote_character CloudwatchLogTransformer#quote_character}.'''
        result = self._values.get("quote_character")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigCsv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigCsvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCsvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03f308640224fe44289ea17b3f90a61f6713780140ee3b49766b2aa30bc28fe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigCsvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39e46861460f2c679bca9d650684a00cf0b1de620128b82dd7b449f2b90cda9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigCsvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f122bfd7973e2f928923607e758b2a4b19d4bb174cb18795239a1aa4bb09021a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0514c28fd373fb9f977f6a912cd6ff3623184cb34f1417e64ac684418c7656dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db43d4311c9897829e562fe73cbd8e0145e44cb162917462985c646596101c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCsv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCsv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCsv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4849a105d7cab2d580761df870ca0dce130dc8ecda68755f96c66cbe0d05d312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigCsvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigCsvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f989b58720cb10ca0e0f61b69ce3823f26b3b40d9ef820cc4abcbd11d24fe73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumns")
    def reset_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumns", []))

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetQuoteCharacter")
    def reset_quote_character(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuoteCharacter", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteCharacterInput")
    def quote_character_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteCharacterInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce1c299eb6323947e19b542eac1d3c02e7c0d43884eacb31a790b68b0d6d7ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef016b4ee6866473817960972fadc92688e7c40c655d88cd75cdd7b14020dc97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteCharacter")
    def quote_character(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quoteCharacter"))

    @quote_character.setter
    def quote_character(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5e62aad385afbece00097bfca455a302972bf234e4822a658f33ee748c38ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteCharacter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5034f77994c2229d7f1c0b78817162c8eba9ccfd2be145524450717a64d6a606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCsv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCsv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCsv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0971ad0b386acfd2c137c73fbb69bd82f44439ddb7dbc2a5386dc68ba6db590c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigDateTimeConverter",
    jsii_struct_bases=[],
    name_mapping={
        "match_patterns": "matchPatterns",
        "source": "source",
        "target": "target",
        "locale": "locale",
        "source_timezone": "sourceTimezone",
        "target_format": "targetFormat",
        "target_timezone": "targetTimezone",
    },
)
class CloudwatchLogTransformerTransformerConfigDateTimeConverter:
    def __init__(
        self,
        *,
        match_patterns: typing.Sequence[builtins.str],
        source: builtins.str,
        target: builtins.str,
        locale: typing.Optional[builtins.str] = None,
        source_timezone: typing.Optional[builtins.str] = None,
        target_format: typing.Optional[builtins.str] = None,
        target_timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#match_patterns CloudwatchLogTransformer#match_patterns}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.
        :param locale: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#locale CloudwatchLogTransformer#locale}.
        :param source_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source_timezone CloudwatchLogTransformer#source_timezone}.
        :param target_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target_format CloudwatchLogTransformer#target_format}.
        :param target_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target_timezone CloudwatchLogTransformer#target_timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e863f4c091697276b2a71ad7abd84b9bf65506389b9dada7b3eae34e7f9301cf)
            check_type(argname="argument match_patterns", value=match_patterns, expected_type=type_hints["match_patterns"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
            check_type(argname="argument source_timezone", value=source_timezone, expected_type=type_hints["source_timezone"])
            check_type(argname="argument target_format", value=target_format, expected_type=type_hints["target_format"])
            check_type(argname="argument target_timezone", value=target_timezone, expected_type=type_hints["target_timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_patterns": match_patterns,
            "source": source,
            "target": target,
        }
        if locale is not None:
            self._values["locale"] = locale
        if source_timezone is not None:
            self._values["source_timezone"] = source_timezone
        if target_format is not None:
            self._values["target_format"] = target_format
        if target_timezone is not None:
            self._values["target_timezone"] = target_timezone

    @builtins.property
    def match_patterns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#match_patterns CloudwatchLogTransformer#match_patterns}.'''
        result = self._values.get("match_patterns")
        assert result is not None, "Required property 'match_patterns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def locale(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#locale CloudwatchLogTransformer#locale}.'''
        result = self._values.get("locale")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source_timezone CloudwatchLogTransformer#source_timezone}.'''
        result = self._values.get("source_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target_format CloudwatchLogTransformer#target_format}.'''
        result = self._values.get("target_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target_timezone CloudwatchLogTransformer#target_timezone}.'''
        result = self._values.get("target_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigDateTimeConverter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigDateTimeConverterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigDateTimeConverterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1798b67a13037ebe3b5d9f8c99b23c78664b1cf9bb7399c4f249ab4b24ddea7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigDateTimeConverterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d541459d88a8b505515a621e7846f3f92edbbf824f20201287fd4ec0bc8fff6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigDateTimeConverterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5dd8527d83bbc91cbdfa0dd3b9e2273b4b4cc9d730850fb5faebf98c179c6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17c25422e4a737d2035da4c0eb2b11dd05290dd598087053c65ad892d9d61de9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__381d99e7a6b69f9eab1171e5d02243287e0586bb4efbb9297325c2c0973e33fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDateTimeConverter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDateTimeConverter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDateTimeConverter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca2ea5cb3477259bef4c1228b8d50e428e5282a2f05d64706e23b6108557598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigDateTimeConverterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigDateTimeConverterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5e425aab2ad6598eb204faf8cb82adf3fc3cdf0deffe35e15728a0ad6b6169e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLocale")
    def reset_locale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocale", []))

    @jsii.member(jsii_name="resetSourceTimezone")
    def reset_source_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceTimezone", []))

    @jsii.member(jsii_name="resetTargetFormat")
    def reset_target_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFormat", []))

    @jsii.member(jsii_name="resetTargetTimezone")
    def reset_target_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="localeInput")
    def locale_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localeInput"))

    @builtins.property
    @jsii.member(jsii_name="matchPatternsInput")
    def match_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTimezoneInput")
    def source_timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFormatInput")
    def target_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTimezoneInput")
    def target_timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="locale")
    def locale(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locale"))

    @locale.setter
    def locale(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69501efecb8b7ad567ac494c70ee52ace60ed6b17a4687a97fce91c2e2461f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchPatterns")
    def match_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchPatterns"))

    @match_patterns.setter
    def match_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889d28fe35bee9dd68d605bb62ccd7390054d633317ce360f673db4c04d880c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c6812a845f3aa16b56399fa2f8bdcff70d7e0e2812547e338f66f7a16b4811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceTimezone")
    def source_timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceTimezone"))

    @source_timezone.setter
    def source_timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097c63e88617c040d58b1b1e71a620319693743b566e70ddb3dcc1fbc42b148d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1d28be2995321edb9e100fbd504b3ef5d5fc0a8b4275868132b16e842f1150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFormat")
    def target_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFormat"))

    @target_format.setter
    def target_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ecce82edbafa6e68bd807f5c8c772db86b7fedddd226c5838e741c493aab2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetTimezone")
    def target_timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetTimezone"))

    @target_timezone.setter
    def target_timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6ad5554161d64f781f3c8e1b6aaf4e650021a54d33a37f1024552f59357eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDateTimeConverter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDateTimeConverter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDateTimeConverter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d69849c04a742796e1e31af07e5db9d86de85513585ddf94e174b3213c9b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigDeleteKeys",
    jsii_struct_bases=[],
    name_mapping={"with_keys": "withKeys"},
)
class CloudwatchLogTransformerTransformerConfigDeleteKeys:
    def __init__(self, *, with_keys: typing.Sequence[builtins.str]) -> None:
        '''
        :param with_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd8406ab950b30fe2c2c7d9ef5186c586e8d343b1eeac1fb40e2d0cb6ff30ca)
            check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "with_keys": with_keys,
        }

    @builtins.property
    def with_keys(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.'''
        result = self._values.get("with_keys")
        assert result is not None, "Required property 'with_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigDeleteKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigDeleteKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigDeleteKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c11386b2297028334497a8fccde3a3521201831cacf92289f24e49c8eb2680cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigDeleteKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f48398865ddcb0d7b701b1156e58a3ea84d7ef4be9bd9e25a10b1e94ed226e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigDeleteKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdddf752ba658f943db2f3bc319c81234e151690828910cfdae1b88bd2c14273)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b025a869ee00d134e14f8ed89b9b31e62278b7cd28a03691858183d6928b32c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__275a4b144f83e2152bb0696b2d546f3853fe3cf7d7aad0953d619d5e6a74ec41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDeleteKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDeleteKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDeleteKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9f58bf661be7c5157c79b6c6e0aef5eaab8e8a8840737e41305ed23e335840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigDeleteKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigDeleteKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b86ef7e4128a91b892d637b310dd4c02e032fd51d2a8c0393f6c175eee9a2118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="withKeysInput")
    def with_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "withKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="withKeys")
    def with_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "withKeys"))

    @with_keys.setter
    def with_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f88f3a31d84986f8d23f609aef219414497d1626712cc65da0b54f53a34f449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDeleteKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDeleteKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDeleteKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6fb0d0bf2938124aebffd6dac2490401c251659b04aba6d8c5bf90f212ceda8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigGrok",
    jsii_struct_bases=[],
    name_mapping={"match": "match", "source": "source"},
)
class CloudwatchLogTransformerTransformerConfigGrok:
    def __init__(
        self,
        *,
        match: builtins.str,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#match CloudwatchLogTransformer#match}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5b9464f98c6680da4b938e88465973eed833e227f7847b35346e596019cf56)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match": match,
        }
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def match(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#match CloudwatchLogTransformer#match}.'''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigGrok(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigGrokList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigGrokList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__682e2a464e226285b49f7e750141051791483f389d23d929130d08378be2b62a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigGrokOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79aea2746c5f440b4127dd61a159e4c4daac32009d09c8e0af300f4345cb0b98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigGrokOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3281442c704817b7a58ba5b36c3edf7a152f7cda2b8c31cc55b35851956e6482)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0939ae76fec75367f1395313e4c35cc2615b4af4725677381b1c9ac0b745cb41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05f70da70970fa2a1bd26c5582e9b09b1c83d50a35f75acc39a49ec9c3dcc6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigGrok]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigGrok]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigGrok]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe7aed7abed8a418ba64c03503e550e353bf14e298a2a5b294a36ba8ff4eaac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigGrokOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigGrokOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eff3a88b7bc1888405a7062cddec4aeb23dd2ff248e44d8d8ad4966c02baf1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "match"))

    @match.setter
    def match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1805b9db89e7b9edabe4179195b59a086c107c1b1b7ca11daf54016e954f1c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb630f8a5aa44e27fe9fe698504c5ef8919ec513bae85dc14819d40095a620a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigGrok]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigGrok]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigGrok]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c119b9a46affde951245131cd87dc5902c0ae48ef2e2f399ca78149952378b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__916d2f8404a22976659e740238ff401b7d2197eb8417e989f97330ec0bc65442)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be25f60176a8b50708c713a1a132062e4e5684d65e51210b7bf7fd201270bbc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5908f19a6de81b1c0596353e83e2fee7296cc46cc19ea72c59ac046b5424c7f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4974b926ca7a141dd806c12b7104bcd3b4e112027691ed89ee9ebe7adf3965)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05a21c35674de48c79a301402d5fbd32307475266518ecc76b5081abd2395eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3887c6983d51c677af825175710e6985a37514024e7665860cf556c20cff65b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigListToMap",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "source": "source",
        "flatten": "flatten",
        "flattened_element": "flattenedElement",
        "target": "target",
        "value_key": "valueKey",
    },
)
class CloudwatchLogTransformerTransformerConfigListToMap:
    def __init__(
        self,
        *,
        key: builtins.str,
        source: builtins.str,
        flatten: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        flattened_element: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        value_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        :param flatten: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#flatten CloudwatchLogTransformer#flatten}.
        :param flattened_element: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#flattened_element CloudwatchLogTransformer#flattened_element}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.
        :param value_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#value_key CloudwatchLogTransformer#value_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc91ca19c40650791a56a639d3264be9ef47b55751d90e8204f4d2d63e5efed4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument flatten", value=flatten, expected_type=type_hints["flatten"])
            check_type(argname="argument flattened_element", value=flattened_element, expected_type=type_hints["flattened_element"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument value_key", value=value_key, expected_type=type_hints["value_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "source": source,
        }
        if flatten is not None:
            self._values["flatten"] = flatten
        if flattened_element is not None:
            self._values["flattened_element"] = flattened_element
        if target is not None:
            self._values["target"] = target
        if value_key is not None:
            self._values["value_key"] = value_key

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flatten(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#flatten CloudwatchLogTransformer#flatten}.'''
        result = self._values.get("flatten")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def flattened_element(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#flattened_element CloudwatchLogTransformer#flattened_element}.'''
        result = self._values.get("flattened_element")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#value_key CloudwatchLogTransformer#value_key}.'''
        result = self._values.get("value_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigListToMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigListToMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigListToMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2115d05b37e73dbf8b25181664a8841088db3d114fbca6c5a0a0161b779ba108)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigListToMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0deec93540d86ad9b8c38995d75376e7eed512bf1293a72ac16f1db365ee6821)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigListToMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f938acff6e41aff4a066e08a42b7a48838be7608274966fa3edec1966dc2fb61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ccffc10750c4c3203b919d4144c3ee07885932ddd6d8a8c10975df70caf8c0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a966fe6ab1e301d232b983b7d28bb91cfecebfec5fa8e0863480a3d68bef0885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigListToMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigListToMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigListToMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6ce31e0ed85922daa3c977ac11b3c3e9c0f20d4bbe3f83d4d79a1504cf9ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigListToMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigListToMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4d11464fc732b00e46bceb186be88eb045841948cdea81fca2177805648e0db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFlatten")
    def reset_flatten(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlatten", []))

    @jsii.member(jsii_name="resetFlattenedElement")
    def reset_flattened_element(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlattenedElement", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetValueKey")
    def reset_value_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueKey", []))

    @builtins.property
    @jsii.member(jsii_name="flattenedElementInput")
    def flattened_element_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flattenedElementInput"))

    @builtins.property
    @jsii.member(jsii_name="flattenInput")
    def flatten_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "flattenInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="valueKeyInput")
    def value_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="flatten")
    def flatten(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "flatten"))

    @flatten.setter
    def flatten(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9494793b805b043667119944b156fc9955cb5e38763aa746af674ddcd624e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flatten", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flattenedElement")
    def flattened_element(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flattenedElement"))

    @flattened_element.setter
    def flattened_element(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4979e3ae8aa4bf339e342dd6428c93a3cbdae2f7471cf7de9f6625a787b67fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flattenedElement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad7ae2d9753de7bf88ac29aba2af7f03b25e609efab9d72c31b508750a03e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73410b12680faca2189500c74e2a9855c40edde8771fc14a45f2b612ff53944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551d783e82fabfb55fb1bb910584dc78914803f3bdedb521c97bc6ad03b3a709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueKey")
    def value_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueKey"))

    @value_key.setter
    def value_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7023c732f9ff4a23a46bbcb80b7316b2c34942e1f84ff6f2e6d988635000af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigListToMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigListToMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigListToMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b257b3fb1320c8488351e38e9122cb6fc52d4979a722a4d85faf74d916f429a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigLowerCaseString",
    jsii_struct_bases=[],
    name_mapping={"with_keys": "withKeys"},
)
class CloudwatchLogTransformerTransformerConfigLowerCaseString:
    def __init__(self, *, with_keys: typing.Sequence[builtins.str]) -> None:
        '''
        :param with_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41374eb17c53962a8d76dbac51115e7eb3584cbdb8e2f355cfa0a1266b7de9dc)
            check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "with_keys": with_keys,
        }

    @builtins.property
    def with_keys(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.'''
        result = self._values.get("with_keys")
        assert result is not None, "Required property 'with_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigLowerCaseString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigLowerCaseStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigLowerCaseStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be5a68933394574570c0797cc2d42fb24db6680d3ddb7a7a33b9d353730383d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigLowerCaseStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5deb17d12bba7f17213f7caa2c9bd0e4f4e4bed536bcc3457ac0d9e1558d7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigLowerCaseStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f61e9b3010207e0df3ac821c7db33dae76a276ec8cb6cd33515e5732668fd10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9b53d49c77b120652e82084d0f5c4f11f76538708a1e63e9a38d5b00ea17bb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7f582719e402e7dd2ebebc06dfe6adc5dec2b1808c76b22a23f94c8f534b212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigLowerCaseString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigLowerCaseString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigLowerCaseString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5cda84c9ceef911ea783242ed0c485f8479848ff997cd5d8d4d4d86bcbdf1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigLowerCaseStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigLowerCaseStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa43d0287aef7cca3c28091152fd5b7dc685481ddade7311519e7eb79394e27d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="withKeysInput")
    def with_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "withKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="withKeys")
    def with_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "withKeys"))

    @with_keys.setter
    def with_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb63d546444121ee5ae7cd26e00aa6732cc37634977099648ce71bb57ee40dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigLowerCaseString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigLowerCaseString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigLowerCaseString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c70531ad522853867dd8ba13d619f6fb7fa335601bb445052415d86f87a4c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigMoveKeys",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry"},
)
class CloudwatchLogTransformerTransformerConfigMoveKeys:
    def __init__(
        self,
        *,
        entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigMoveKeysEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entry: entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedb7abb82e9364f66b643be5ae4c860a3ef034f9bb2fa90591b6c613fc4edaa)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry is not None:
            self._values["entry"] = entry

    @builtins.property
    def entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigMoveKeysEntry"]]]:
        '''entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigMoveKeysEntry"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigMoveKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigMoveKeysEntry",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "target": "target",
        "overwrite_if_exists": "overwriteIfExists",
    },
)
class CloudwatchLogTransformerTransformerConfigMoveKeysEntry:
    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.
        :param overwrite_if_exists: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692c7efad9e10ebcae250d9c2a4cd37566fcca89676f58d5a2da2c9fba1a5637)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }
        if overwrite_if_exists is not None:
            self._values["overwrite_if_exists"] = overwrite_if_exists

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#target CloudwatchLogTransformer#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overwrite_if_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.'''
        result = self._values.get("overwrite_if_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigMoveKeysEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigMoveKeysEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigMoveKeysEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__320e208907b1cf85c691b6e70ab5fd4ddaf1822218fa913dba22711e46fc7883)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigMoveKeysEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1a2a85af50cd36f6d04b4c9da6e0fc2e44b9b59eb60b6f8b13b94040154d83)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigMoveKeysEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779ad649353a08692c8a14033ef9979ed29d08494d701c70e5b060599b5a6963)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9911b0de42318cd59025f538742d3c77615b72827c5c8e7b1e0e510a6611b7c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ca49d80f933c333fec6eef47f256a6d1e06e952f363f98e2cb5c2c51cad5b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeysEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeysEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeysEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fe58e5814bf667f02deb99c9d66bdc2468071070fed45d23cadd218760a56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigMoveKeysEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigMoveKeysEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad356acd88340564ab3985eb5a8ee9c06f080c53ad6aa904c7f15be81c4ff51d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOverwriteIfExists")
    def reset_overwrite_if_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteIfExists", []))

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExistsInput")
    def overwrite_if_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteIfExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExists")
    def overwrite_if_exists(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteIfExists"))

    @overwrite_if_exists.setter
    def overwrite_if_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9fdc1e4b3c306da5df1d3eea1e4546ea3a99d393aadc4dddfbb46c91193fa11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteIfExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7634065105950284b1f32876d19964dfac87bd43a707bbdbf0acc8e8135bbde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db72fdafdb5635a39ca52c0d600f0208ced3f61625b83dc71159184d62efa6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeysEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeysEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeysEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441e6869c4524fc9ae4b73f46f6fa8eb391a95266d3fd862d852efcf8bb4503a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigMoveKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigMoveKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a64afe641c4ba2e11455a60686c1335dd28eb77188ffd69910e71857dde17f7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigMoveKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2975d76ae4fa935a0e8551a5fb61b5ade49f3a912c7c86fa42f1ed31102103)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigMoveKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8bd7196938fc9fb26a79f65dfa1eef0acbc20ac031201b5370b446135857dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__216dcf365ac6570af396fba01afeeb85e3af947d6179dd5105ddf4f5c0b26d6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62555cf2e15352e8f7c5df47b8652d25313a3186ac3c8118cd776b8befda3cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c957bdd9f29cbc13f8db41926c0dcf2cc33d8f09c11189a51a4732007403d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigMoveKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigMoveKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__617aa53a95c99b3f5be105c8734e40a995db2b4498cd8761373ec4c212f4994e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEntry")
    def put_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigMoveKeysEntry, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf5c63c71e0edffbc48f4fbd0a8301cc7f7372b2575abc9ebb80ca42451db6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntry", [value]))

    @jsii.member(jsii_name="resetEntry")
    def reset_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntry", []))

    @builtins.property
    @jsii.member(jsii_name="entry")
    def entry(self) -> CloudwatchLogTransformerTransformerConfigMoveKeysEntryList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigMoveKeysEntryList, jsii.get(self, "entry"))

    @builtins.property
    @jsii.member(jsii_name="entryInput")
    def entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeysEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeysEntry]]], jsii.get(self, "entryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647ba4e0c69a2b560270f6afb9086e06c56c8e2d63a36591a0508fdd4b8989f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c73c5e54961328b019d8805fb8358201256262be2d44f433e00932fb57b3957)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAddKeys")
    def put_add_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigAddKeys, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0543f88be8f37ee0cfe9011b7764eb4604cdc9181e60a68dde05331b41478a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddKeys", [value]))

    @jsii.member(jsii_name="putCopyValue")
    def put_copy_value(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCopyValue, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d6673023a65ce338e29d6771b1acaf96d01667b7db67163d1d0084977ad526c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCopyValue", [value]))

    @jsii.member(jsii_name="putCsv")
    def put_csv(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCsv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fa8553735b42f57ec2d3d64db1a81190c4b5a411b5ffbe9947658ac977482c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCsv", [value]))

    @jsii.member(jsii_name="putDateTimeConverter")
    def put_date_time_converter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigDateTimeConverter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4bfa5394ed5131f5ec2203874462c43ca17797585f815c83c2db69f0c8828f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateTimeConverter", [value]))

    @jsii.member(jsii_name="putDeleteKeys")
    def put_delete_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigDeleteKeys, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551798ef9a6e473beae54e9dbb159e6d6c859d78fbc9ced75440ba0346dde3b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeleteKeys", [value]))

    @jsii.member(jsii_name="putGrok")
    def put_grok(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigGrok, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8811c5361fa4ff53f424539ff55c4d7ff104250b9528e4449fb59978af6e087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGrok", [value]))

    @jsii.member(jsii_name="putListToMap")
    def put_list_to_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigListToMap, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e83a821ce301c0df9337f716fd1594eedca34db4f40c35c203ea1355c20b19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putListToMap", [value]))

    @jsii.member(jsii_name="putLowerCaseString")
    def put_lower_case_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigLowerCaseString, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec3eb2f865d0f5f5f33d20ea4ee28faee4d014e0cfdb9fc0fa7e7bef92591e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLowerCaseString", [value]))

    @jsii.member(jsii_name="putMoveKeys")
    def put_move_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigMoveKeys, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b768c4fcbe3662cc8eed48021baec45e4a62831d445c3164b3423345b1a9f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMoveKeys", [value]))

    @jsii.member(jsii_name="putParseCloudfront")
    def put_parse_cloudfront(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseCloudfront", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668ca5ef0d8d13ed25e244968e8b8f387bd058e062653ed01930312c08bbe7be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseCloudfront", [value]))

    @jsii.member(jsii_name="putParseJson")
    def put_parse_json(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseJson", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2a7fb776b5e9129ef99ec7e377ebb1050b077eadaa5dc646036519edd21e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseJson", [value]))

    @jsii.member(jsii_name="putParseKeyValue")
    def put_parse_key_value(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseKeyValue", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b566920b897a9255f06d85dad31576a639dcf35168635931f75f6eb223aacbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseKeyValue", [value]))

    @jsii.member(jsii_name="putParsePostgres")
    def put_parse_postgres(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParsePostgres", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a7bfdb6e1364b1e809290c3b2e7ac6c2f8d482969e9e7f2304fdaeb7085e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParsePostgres", [value]))

    @jsii.member(jsii_name="putParseRoute53")
    def put_parse_route53(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseRoute53", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb0193e72339390cf55b34790ddc3ffe798a5b729ea16f5478f4197beef8dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseRoute53", [value]))

    @jsii.member(jsii_name="putParseToOcsf")
    def put_parse_to_ocsf(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseToOcsf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c2ad83b5c71622e85ca635d2b97cbd8664c875fb9c07115e0308b891a8a620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseToOcsf", [value]))

    @jsii.member(jsii_name="putParseVpc")
    def put_parse_vpc(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseVpc", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87655561e40174eff6806e0a35ebf86a39690c747f8f044250e4b8b78cb2569d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseVpc", [value]))

    @jsii.member(jsii_name="putParseWaf")
    def put_parse_waf(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigParseWaf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80306cc7fc4197f90f2dd2b954ea6cc5d8ad4d76b3c0029b4806e791be420dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseWaf", [value]))

    @jsii.member(jsii_name="putRenameKeys")
    def put_rename_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigRenameKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658d407742f2cc736e9cffd089d67fd771f270002e11a91ac0be28e6c28894a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRenameKeys", [value]))

    @jsii.member(jsii_name="putSplitString")
    def put_split_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigSplitString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9be79bf3e156255126e4956b126fd3db6db3a9d79c8281dc843069d2914c186f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSplitString", [value]))

    @jsii.member(jsii_name="putSubstituteString")
    def put_substitute_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigSubstituteString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa7b0c1a78ffbaf9800cc755dddf998536aef6827e8f42bede45f19888dcdf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubstituteString", [value]))

    @jsii.member(jsii_name="putTrimString")
    def put_trim_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigTrimString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde505157e27f8f93a18c79005c84ac5479830fd4449f4d417fd8a50696656b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrimString", [value]))

    @jsii.member(jsii_name="putTypeConverter")
    def put_type_converter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigTypeConverter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fd5cbfb5870055db2f920d27cf94dc1e9d09f581129a831605bc728ed9cc92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTypeConverter", [value]))

    @jsii.member(jsii_name="putUpperCaseString")
    def put_upper_case_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigUpperCaseString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a57bd7503c5e0f2301d6d9d058eaf79f3a4420a73d5ff42b98dab7b384bac2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpperCaseString", [value]))

    @jsii.member(jsii_name="resetAddKeys")
    def reset_add_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddKeys", []))

    @jsii.member(jsii_name="resetCopyValue")
    def reset_copy_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyValue", []))

    @jsii.member(jsii_name="resetCsv")
    def reset_csv(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsv", []))

    @jsii.member(jsii_name="resetDateTimeConverter")
    def reset_date_time_converter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateTimeConverter", []))

    @jsii.member(jsii_name="resetDeleteKeys")
    def reset_delete_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteKeys", []))

    @jsii.member(jsii_name="resetGrok")
    def reset_grok(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrok", []))

    @jsii.member(jsii_name="resetListToMap")
    def reset_list_to_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetListToMap", []))

    @jsii.member(jsii_name="resetLowerCaseString")
    def reset_lower_case_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLowerCaseString", []))

    @jsii.member(jsii_name="resetMoveKeys")
    def reset_move_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMoveKeys", []))

    @jsii.member(jsii_name="resetParseCloudfront")
    def reset_parse_cloudfront(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseCloudfront", []))

    @jsii.member(jsii_name="resetParseJson")
    def reset_parse_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseJson", []))

    @jsii.member(jsii_name="resetParseKeyValue")
    def reset_parse_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseKeyValue", []))

    @jsii.member(jsii_name="resetParsePostgres")
    def reset_parse_postgres(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParsePostgres", []))

    @jsii.member(jsii_name="resetParseRoute53")
    def reset_parse_route53(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseRoute53", []))

    @jsii.member(jsii_name="resetParseToOcsf")
    def reset_parse_to_ocsf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseToOcsf", []))

    @jsii.member(jsii_name="resetParseVpc")
    def reset_parse_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseVpc", []))

    @jsii.member(jsii_name="resetParseWaf")
    def reset_parse_waf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseWaf", []))

    @jsii.member(jsii_name="resetRenameKeys")
    def reset_rename_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenameKeys", []))

    @jsii.member(jsii_name="resetSplitString")
    def reset_split_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplitString", []))

    @jsii.member(jsii_name="resetSubstituteString")
    def reset_substitute_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstituteString", []))

    @jsii.member(jsii_name="resetTrimString")
    def reset_trim_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrimString", []))

    @jsii.member(jsii_name="resetTypeConverter")
    def reset_type_converter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeConverter", []))

    @jsii.member(jsii_name="resetUpperCaseString")
    def reset_upper_case_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpperCaseString", []))

    @builtins.property
    @jsii.member(jsii_name="addKeys")
    def add_keys(self) -> CloudwatchLogTransformerTransformerConfigAddKeysList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigAddKeysList, jsii.get(self, "addKeys"))

    @builtins.property
    @jsii.member(jsii_name="copyValue")
    def copy_value(self) -> CloudwatchLogTransformerTransformerConfigCopyValueList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigCopyValueList, jsii.get(self, "copyValue"))

    @builtins.property
    @jsii.member(jsii_name="csv")
    def csv(self) -> CloudwatchLogTransformerTransformerConfigCsvList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigCsvList, jsii.get(self, "csv"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeConverter")
    def date_time_converter(
        self,
    ) -> CloudwatchLogTransformerTransformerConfigDateTimeConverterList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigDateTimeConverterList, jsii.get(self, "dateTimeConverter"))

    @builtins.property
    @jsii.member(jsii_name="deleteKeys")
    def delete_keys(self) -> CloudwatchLogTransformerTransformerConfigDeleteKeysList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigDeleteKeysList, jsii.get(self, "deleteKeys"))

    @builtins.property
    @jsii.member(jsii_name="grok")
    def grok(self) -> CloudwatchLogTransformerTransformerConfigGrokList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigGrokList, jsii.get(self, "grok"))

    @builtins.property
    @jsii.member(jsii_name="listToMap")
    def list_to_map(self) -> CloudwatchLogTransformerTransformerConfigListToMapList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigListToMapList, jsii.get(self, "listToMap"))

    @builtins.property
    @jsii.member(jsii_name="lowerCaseString")
    def lower_case_string(
        self,
    ) -> CloudwatchLogTransformerTransformerConfigLowerCaseStringList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigLowerCaseStringList, jsii.get(self, "lowerCaseString"))

    @builtins.property
    @jsii.member(jsii_name="moveKeys")
    def move_keys(self) -> CloudwatchLogTransformerTransformerConfigMoveKeysList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigMoveKeysList, jsii.get(self, "moveKeys"))

    @builtins.property
    @jsii.member(jsii_name="parseCloudfront")
    def parse_cloudfront(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigParseCloudfrontList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseCloudfrontList", jsii.get(self, "parseCloudfront"))

    @builtins.property
    @jsii.member(jsii_name="parseJson")
    def parse_json(self) -> "CloudwatchLogTransformerTransformerConfigParseJsonList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseJsonList", jsii.get(self, "parseJson"))

    @builtins.property
    @jsii.member(jsii_name="parseKeyValue")
    def parse_key_value(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigParseKeyValueList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseKeyValueList", jsii.get(self, "parseKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="parsePostgres")
    def parse_postgres(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigParsePostgresList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParsePostgresList", jsii.get(self, "parsePostgres"))

    @builtins.property
    @jsii.member(jsii_name="parseRoute53")
    def parse_route53(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigParseRoute53List":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseRoute53List", jsii.get(self, "parseRoute53"))

    @builtins.property
    @jsii.member(jsii_name="parseToOcsf")
    def parse_to_ocsf(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigParseToOcsfList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseToOcsfList", jsii.get(self, "parseToOcsf"))

    @builtins.property
    @jsii.member(jsii_name="parseVpc")
    def parse_vpc(self) -> "CloudwatchLogTransformerTransformerConfigParseVpcList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseVpcList", jsii.get(self, "parseVpc"))

    @builtins.property
    @jsii.member(jsii_name="parseWaf")
    def parse_waf(self) -> "CloudwatchLogTransformerTransformerConfigParseWafList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseWafList", jsii.get(self, "parseWaf"))

    @builtins.property
    @jsii.member(jsii_name="renameKeys")
    def rename_keys(self) -> "CloudwatchLogTransformerTransformerConfigRenameKeysList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigRenameKeysList", jsii.get(self, "renameKeys"))

    @builtins.property
    @jsii.member(jsii_name="splitString")
    def split_string(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigSplitStringList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigSplitStringList", jsii.get(self, "splitString"))

    @builtins.property
    @jsii.member(jsii_name="substituteString")
    def substitute_string(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigSubstituteStringList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigSubstituteStringList", jsii.get(self, "substituteString"))

    @builtins.property
    @jsii.member(jsii_name="trimString")
    def trim_string(self) -> "CloudwatchLogTransformerTransformerConfigTrimStringList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigTrimStringList", jsii.get(self, "trimString"))

    @builtins.property
    @jsii.member(jsii_name="typeConverter")
    def type_converter(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigTypeConverterList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigTypeConverterList", jsii.get(self, "typeConverter"))

    @builtins.property
    @jsii.member(jsii_name="upperCaseString")
    def upper_case_string(
        self,
    ) -> "CloudwatchLogTransformerTransformerConfigUpperCaseStringList":
        return typing.cast("CloudwatchLogTransformerTransformerConfigUpperCaseStringList", jsii.get(self, "upperCaseString"))

    @builtins.property
    @jsii.member(jsii_name="addKeysInput")
    def add_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeys]]], jsii.get(self, "addKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="copyValueInput")
    def copy_value_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValue]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValue]]], jsii.get(self, "copyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="csvInput")
    def csv_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCsv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCsv]]], jsii.get(self, "csvInput"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeConverterInput")
    def date_time_converter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDateTimeConverter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDateTimeConverter]]], jsii.get(self, "dateTimeConverterInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteKeysInput")
    def delete_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDeleteKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDeleteKeys]]], jsii.get(self, "deleteKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="grokInput")
    def grok_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigGrok]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigGrok]]], jsii.get(self, "grokInput"))

    @builtins.property
    @jsii.member(jsii_name="listToMapInput")
    def list_to_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigListToMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigListToMap]]], jsii.get(self, "listToMapInput"))

    @builtins.property
    @jsii.member(jsii_name="lowerCaseStringInput")
    def lower_case_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigLowerCaseString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigLowerCaseString]]], jsii.get(self, "lowerCaseStringInput"))

    @builtins.property
    @jsii.member(jsii_name="moveKeysInput")
    def move_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeys]]], jsii.get(self, "moveKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="parseCloudfrontInput")
    def parse_cloudfront_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseCloudfront"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseCloudfront"]]], jsii.get(self, "parseCloudfrontInput"))

    @builtins.property
    @jsii.member(jsii_name="parseJsonInput")
    def parse_json_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseJson"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseJson"]]], jsii.get(self, "parseJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="parseKeyValueInput")
    def parse_key_value_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseKeyValue"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseKeyValue"]]], jsii.get(self, "parseKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parsePostgresInput")
    def parse_postgres_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParsePostgres"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParsePostgres"]]], jsii.get(self, "parsePostgresInput"))

    @builtins.property
    @jsii.member(jsii_name="parseRoute53Input")
    def parse_route53_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseRoute53"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseRoute53"]]], jsii.get(self, "parseRoute53Input"))

    @builtins.property
    @jsii.member(jsii_name="parseToOcsfInput")
    def parse_to_ocsf_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseToOcsf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseToOcsf"]]], jsii.get(self, "parseToOcsfInput"))

    @builtins.property
    @jsii.member(jsii_name="parseVpcInput")
    def parse_vpc_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseVpc"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseVpc"]]], jsii.get(self, "parseVpcInput"))

    @builtins.property
    @jsii.member(jsii_name="parseWafInput")
    def parse_waf_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseWaf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigParseWaf"]]], jsii.get(self, "parseWafInput"))

    @builtins.property
    @jsii.member(jsii_name="renameKeysInput")
    def rename_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigRenameKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigRenameKeys"]]], jsii.get(self, "renameKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="splitStringInput")
    def split_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSplitString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSplitString"]]], jsii.get(self, "splitStringInput"))

    @builtins.property
    @jsii.member(jsii_name="substituteStringInput")
    def substitute_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSubstituteString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSubstituteString"]]], jsii.get(self, "substituteStringInput"))

    @builtins.property
    @jsii.member(jsii_name="trimStringInput")
    def trim_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTrimString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTrimString"]]], jsii.get(self, "trimStringInput"))

    @builtins.property
    @jsii.member(jsii_name="typeConverterInput")
    def type_converter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTypeConverter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTypeConverter"]]], jsii.get(self, "typeConverterInput"))

    @builtins.property
    @jsii.member(jsii_name="upperCaseStringInput")
    def upper_case_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigUpperCaseString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigUpperCaseString"]]], jsii.get(self, "upperCaseStringInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f24b1ba716bed3f4232fc611daa3f500dcd6ea085f851ef4f82a0635d684d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseCloudfront",
    jsii_struct_bases=[],
    name_mapping={"source": "source"},
)
class CloudwatchLogTransformerTransformerConfigParseCloudfront:
    def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89372fadb09c69c7b1ba469132d80c3a1fb16e838a0e412f29dd3ad011d70cc5)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParseCloudfront(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParseCloudfrontList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseCloudfrontList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9bf2c4405a45a88ce336441885e332c3b66801b65432301f8e5a13ac5eed178)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParseCloudfrontOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5edc137cba231b59905b865a6e02f4de6c71783387bcb94d9bd1aceac6d9d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseCloudfrontOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8496ed59c9aed559179fad5e47e2a61dfe19706a630d8525d1037bc1d94376f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b98a837c93588c56adae17e7e839595d2859e34f70cd5fed50a849e4c282ec3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4b3d25a97786689d19267826b410b2cec958932a49cd4d0c30b1476600c43d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseCloudfront]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseCloudfront]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseCloudfront]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5a0fad3a303ecf515be76a2bb988ac81fe71bcdd993cc3d8e80c87fb8e4cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParseCloudfrontOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseCloudfrontOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__759b7f71cb41fa64b69a0f5506c3159b707907688a44c8b7a8853e7692934722)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79d1ff501a247d501e65a3c36d09edb934e44adf07784abe5331fcfbb4d9d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseCloudfront]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseCloudfront]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseCloudfront]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744b68d059e5a4135d2e7f582150feb5f3117cbad91802313d6aac3024ccd100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseJson",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "source": "source"},
)
class CloudwatchLogTransformerTransformerConfigParseJson:
    def __init__(
        self,
        *,
        destination: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#destination CloudwatchLogTransformer#destination}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed3c0a59390073093d19738ed9634420f9cefb74bc96a9b6f1f36e93e39351c)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#destination CloudwatchLogTransformer#destination}.'''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParseJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParseJsonList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseJsonList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__354e96c1ea4afbf298cbe11b843e6841825aac6ec361725f9a58c609ab0110c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParseJsonOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9446644e17a4e9c847b5de217a875f2a2853c42a8bfc6fa1cc3561f6e0aff3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseJsonOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e5f5a81e9e75f6738263c45e553a3ce4da65b1bd6068f96735c87423fa8daa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb5ca2e5b051221c4173d61c714ac0d0c0533c610fe7ec293cb1b31e6589f784)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10224f7dd9907ad903793ad7f13725d9b3f2f0b2ccffb4e19a26e39512d80c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseJson]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseJson]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseJson]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cca358ce66b1fb9d53b339ae6053cce7545e6991150864e2a2ff82a0a50586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParseJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2231e3b5090a01fefc48f2c0f5b5431d0d3821b05d7cd141841f9957c568048)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937eca076ec7fdb14d60690e89f93d4ce203a5f46d6f896acd4840cddc2cfc76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0753f062b2f162c1f7a2584c20db861a9327a1a6e8b7dadf856f3ef097509268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseJson]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseJson]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseJson]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61760eb679f61880f400b7ad448a767094a5c3ad8caf57e6eb7a32ca4ee7092b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseKeyValue",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "field_delimiter": "fieldDelimiter",
        "key_prefix": "keyPrefix",
        "key_value_delimiter": "keyValueDelimiter",
        "non_match_value": "nonMatchValue",
        "overwrite_if_exists": "overwriteIfExists",
        "source": "source",
    },
)
class CloudwatchLogTransformerTransformerConfigParseKeyValue:
    def __init__(
        self,
        *,
        destination: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        key_value_delimiter: typing.Optional[builtins.str] = None,
        non_match_value: typing.Optional[builtins.str] = None,
        overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#destination CloudwatchLogTransformer#destination}.
        :param field_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#field_delimiter CloudwatchLogTransformer#field_delimiter}.
        :param key_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key_prefix CloudwatchLogTransformer#key_prefix}.
        :param key_value_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key_value_delimiter CloudwatchLogTransformer#key_value_delimiter}.
        :param non_match_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#non_match_value CloudwatchLogTransformer#non_match_value}.
        :param overwrite_if_exists: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112a5338d22878ad8c018581ecc6407b4d46680f6f9d774fed625851f4a6a079)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument key_value_delimiter", value=key_value_delimiter, expected_type=type_hints["key_value_delimiter"])
            check_type(argname="argument non_match_value", value=non_match_value, expected_type=type_hints["non_match_value"])
            check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if key_value_delimiter is not None:
            self._values["key_value_delimiter"] = key_value_delimiter
        if non_match_value is not None:
            self._values["non_match_value"] = non_match_value
        if overwrite_if_exists is not None:
            self._values["overwrite_if_exists"] = overwrite_if_exists
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#destination CloudwatchLogTransformer#destination}.'''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#field_delimiter CloudwatchLogTransformer#field_delimiter}.'''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key_prefix CloudwatchLogTransformer#key_prefix}.'''
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_value_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key_value_delimiter CloudwatchLogTransformer#key_value_delimiter}.'''
        result = self._values.get("key_value_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_match_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#non_match_value CloudwatchLogTransformer#non_match_value}.'''
        result = self._values.get("non_match_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overwrite_if_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.'''
        result = self._values.get("overwrite_if_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParseKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParseKeyValueList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseKeyValueList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__987182d3b75c47b09ebeeb7b80ffabf111400cbd2133d8bbbf00e0ffdb00ad51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParseKeyValueOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56412d9bad8f6fae440db9faffc8396e68a4ed6dcf6c01a94e416e32660bc12e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseKeyValueOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8dd1f0a91fcc23bce46fab47153db00ee7f9a68fbc86b4bf31f6a37bc5085d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8456a7d62a473d89b46516f9b49cb9e561a616c2cb32e7a72e10380af32ed0a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2813fe25a1efbb38757a9e34ef9a3f0d01f69ad9505f3d0902de574a1ac2d24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseKeyValue]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseKeyValue]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseKeyValue]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc292b488a136e5eedb7a0ff2aeb9a7be9640977806a5a9fa46d985f54618be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParseKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8fc1cebc69e41e5a9142a58e3ef9ef2e97c3934ee89f68277fa136dcbaa83a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @jsii.member(jsii_name="resetFieldDelimiter")
    def reset_field_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldDelimiter", []))

    @jsii.member(jsii_name="resetKeyPrefix")
    def reset_key_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPrefix", []))

    @jsii.member(jsii_name="resetKeyValueDelimiter")
    def reset_key_value_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyValueDelimiter", []))

    @jsii.member(jsii_name="resetNonMatchValue")
    def reset_non_match_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonMatchValue", []))

    @jsii.member(jsii_name="resetOverwriteIfExists")
    def reset_overwrite_if_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteIfExists", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiterInput")
    def field_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPrefixInput")
    def key_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="keyValueDelimiterInput")
    def key_value_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyValueDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="nonMatchValueInput")
    def non_match_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nonMatchValueInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExistsInput")
    def overwrite_if_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteIfExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c66644953c71c8abe9bc3abaaa8c67cbd947b32d41563bd4b39d8668f187d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldDelimiter"))

    @field_delimiter.setter
    def field_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6527f0e441ed12e0c47306bd83e00f4bd243569a26c70d4827ad35c9b95a985e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPrefix")
    def key_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPrefix"))

    @key_prefix.setter
    def key_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe0ae01ea8b41afa5bf69998f42ea6d2014333f21259b1241fbe54e507ce204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyValueDelimiter")
    def key_value_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyValueDelimiter"))

    @key_value_delimiter.setter
    def key_value_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1249534ce05cc287cff4a8ff2b1c244a50a7d62a63141b768f44108f58df3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyValueDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonMatchValue")
    def non_match_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nonMatchValue"))

    @non_match_value.setter
    def non_match_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e00d274bafef85737c2186a6dcab3510939d1ae61ed3aae497320046d12df0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonMatchValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExists")
    def overwrite_if_exists(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteIfExists"))

    @overwrite_if_exists.setter
    def overwrite_if_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82c0c4bb16962938e12fea94d63b2ce82c298b11bc69f1bf18c4289552077d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteIfExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c7623c988023cea45096b8a00f141f7827fd455a47bf782f4dd8fd03d0d1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseKeyValue]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseKeyValue]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseKeyValue]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf60e2208a232e98ef0fcf7ab30447adb6ee5c7dfd928e9607693d3a79f854b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParsePostgres",
    jsii_struct_bases=[],
    name_mapping={"source": "source"},
)
class CloudwatchLogTransformerTransformerConfigParsePostgres:
    def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13cbb5ec0d8f72039ad17bb24e86026ea51ed9b95315d9ee4a935872e69b9ad)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParsePostgres(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParsePostgresList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParsePostgresList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2068c893871fe5b52469c1323f017025b8dbaaf6f2a159b4312c5427ce84e66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParsePostgresOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480b84b05f997b27f1ac20ba9566c0026ffe5d805f6fb2e892148bd255ae358c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParsePostgresOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0864fb6ecfc0fc45f86d208d38599cef7c9051e6ed9c3342ab777c13ed3740)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19e64cfa433c2ffd9e64d851ae85b20bd23cbaabf3b4e3834750303f267a958)
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
            type_hints = typing.get_type_hints(_typecheckingstub__945e5971c75870afe5cd9da5b4deeb31dc7cf54e64aafec584e90cd67fc23eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParsePostgres]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParsePostgres]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParsePostgres]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a8fbfea4f21c284353985ee5037e15880af5c474095cb4a74331e940a61972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParsePostgresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParsePostgresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3817669ca4483850cb3f56c2dcb8b6ee02111d35afdc33e1afcc713e56bd4ad3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31719d2b56601c6f9893e9147f815d4a4713acea7cd4e19313cfd9fef218a500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParsePostgres]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParsePostgres]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParsePostgres]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7cf1d1044f8c9d9c5584df245c9687925b3473638340a395f9380df91ee0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseRoute53",
    jsii_struct_bases=[],
    name_mapping={"source": "source"},
)
class CloudwatchLogTransformerTransformerConfigParseRoute53:
    def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8826743120f73e580ed2c6995c15da40997edeb3bb3a408a017c4b66c419233)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParseRoute53(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParseRoute53List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseRoute53List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0861f863dfa36ae87da3e83a48fd21ee6d11a13d12e9a8ad30ee5adfc13f2c4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParseRoute53OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2585344cf07dfd4fdb712b1caf1f8c3df507f414bb9364898046b0ae90da9cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseRoute53OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5d3535d9b0fa7dfd9056ff5f624badf326780ff9d0b9fe117f08e73d200dfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3da1557376cfbbe03125e53ce214937d015ecf88e1b08917fc73fa08531bebf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__698ad9f47d8e05d5e17a55432127248835a4081c179d2127c6d250bc47755b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseRoute53]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseRoute53]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseRoute53]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43aac3e4de26235997c1d26e114cb9658b9fb784d6f30125a474d3db4564744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParseRoute53OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseRoute53OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4dc3d14f094a399ece17144777cff82f16edc2e2be6797545dc296cf12ae0ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd07f152f16eb9531f30567e98080184510958e28d13603ceb351891f0aa271b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseRoute53]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseRoute53]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseRoute53]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40dbef195ad73bfb8713a46bb9577a8ad859290c0c8502bb380c70ff0359b813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseToOcsf",
    jsii_struct_bases=[],
    name_mapping={
        "event_source": "eventSource",
        "ocsf_version": "ocsfVersion",
        "source": "source",
    },
)
class CloudwatchLogTransformerTransformerConfigParseToOcsf:
    def __init__(
        self,
        *,
        event_source: builtins.str,
        ocsf_version: builtins.str,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#event_source CloudwatchLogTransformer#event_source}.
        :param ocsf_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#ocsf_version CloudwatchLogTransformer#ocsf_version}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717a2ebb85f0c1b857b7db1f443b27aa0b035da072408ccc18c5eccce9a18026)
            check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
            check_type(argname="argument ocsf_version", value=ocsf_version, expected_type=type_hints["ocsf_version"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_source": event_source,
            "ocsf_version": ocsf_version,
        }
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def event_source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#event_source CloudwatchLogTransformer#event_source}.'''
        result = self._values.get("event_source")
        assert result is not None, "Required property 'event_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ocsf_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#ocsf_version CloudwatchLogTransformer#ocsf_version}.'''
        result = self._values.get("ocsf_version")
        assert result is not None, "Required property 'ocsf_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParseToOcsf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParseToOcsfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseToOcsfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c048f17819d3e05408102ede5075cda4f59ee9a609a05113d36cf3ef6439fd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParseToOcsfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef58375c375ae15b0c6401d550cea0a368e6b4c5789f1ac13b4bf8cb579b92ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseToOcsfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5217c8510927d9d793eaa4e084670f4373e93d5b20b6bf45bb8c1aad2eda87ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40f34c41ea4e9af0c983a1dddb9aabf8a19cf866d03c5f8ba5174847dac1f33d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2725307d8c13021626ce4ec925cb04ce6fb7396da02a8c8428fbeafc1161b25b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseToOcsf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseToOcsf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseToOcsf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff764de85ade8c3c486439f884913b0179371fb57237442d385957fefb692d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParseToOcsfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseToOcsfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d3dafa678248591cc4a88c79a0be4ab2e7469d90a63b62c0627b786df7a61b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="eventSourceInput")
    def event_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="ocsfVersionInput")
    def ocsf_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ocsfVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSource")
    def event_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSource"))

    @event_source.setter
    def event_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b85ed77ba3c8f00f5661f97d7cd6c7a07f2295898074f2259b5116ff36896e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ocsfVersion")
    def ocsf_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocsfVersion"))

    @ocsf_version.setter
    def ocsf_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab8d05a2372b0738680b9c609cbc34f47ac231d1c4631e2fcf7839a36f0a4e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocsfVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baffc2808326c7118fbc855024bb4b700999ee87fbbedd9891813143379570f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseToOcsf]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseToOcsf]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseToOcsf]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06c16ecbfb8f05c49eb547124131d3bf2c986784314b5a9d1b6f2d519eaefbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseVpc",
    jsii_struct_bases=[],
    name_mapping={"source": "source"},
)
class CloudwatchLogTransformerTransformerConfigParseVpc:
    def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54aa190504460e0a727db9bbcbe8e1f2795d3521ea0080481ed3926bdf193fee)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParseVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParseVpcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseVpcList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e35e11993662440c5632b7a7f880d6fc70e65e2006ab5f3b5a2fe42d1de869f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParseVpcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c921bef35032109a348f7ba1b59e322a51b67266001b43df55a925d83d82db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseVpcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ebe209f3002d5db59acc13301806d76deedf88f06f4c5550355ed5ff2dd846b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d205c7987f5330df96b2cfc665305c765ab914799c44b5ff84402dd0cce71649)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24592abb1c1fac295e412884f7b19cb77b4e62f57dbc247f113a6a827d2fb03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseVpc]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseVpc]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseVpc]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a1c2098cb4ac41b1d56d949361db54cb129d203f9d3caa14fbf4ed8ef4d268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParseVpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseVpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f67dd7a957b3f65e07a2ce507ddfcc982320a4bddd840626c29abd9ea20db271)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d51c1a13b59a5747d09687442d82bbbcd9fe66eb25b6441df90b4a9f0354c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseVpc]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseVpc]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseVpc]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46e05e0ac94fdf65686414d54351cd0fe7cf6b9982bd40fc4a0f1945fe2c0df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseWaf",
    jsii_struct_bases=[],
    name_mapping={"source": "source"},
)
class CloudwatchLogTransformerTransformerConfigParseWaf:
    def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e11ef264e4dd2383233f4ee65e6447766faf5bc1e5f314ebc599c0a99d14c3)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigParseWaf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigParseWafList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseWafList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2163e3a66ff2835b2799ff0ab30796900a0f87612370aa6edb7368ad984d0e88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigParseWafOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d63ee36725a97e41102bd006c7da381a359b9352401c45b4c8578ad6e470e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigParseWafOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0603e9eae98069ed4e43c21e255a2878d2a4a5fa15e036ef4efdd573e361a3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48801d1e076171b99d6a95037656b95f643cc052d04283ea0a9289ea17b8829a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dffd65801444e348dddb7f0b5e2925c65be09429b82cdaca186d5a6033cb190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseWaf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseWaf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseWaf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc5c0fc612f70d92a855bfe4ad5d33bfa227287347009d67cf02c2c206348d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigParseWafOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigParseWafOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6193720a904a9b8a4e238beda6e41a03528891eacd475f590e1a2526747f687c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d133942f9ceb782bb60f6f7c21714069fdde65f03260f4ef784a149562145ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseWaf]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseWaf]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseWaf]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f004b77d165c8bc6cc8e8e97b4ab2caee7e2a145f487d91db6d025fe3bd1d094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigRenameKeys",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry"},
)
class CloudwatchLogTransformerTransformerConfigRenameKeys:
    def __init__(
        self,
        *,
        entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigRenameKeysEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entry: entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d8d02fd1e3fc4945ce4f97e4c845db3808d9fb4f8098397e95b5a983cf5f5c)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry is not None:
            self._values["entry"] = entry

    @builtins.property
    def entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigRenameKeysEntry"]]]:
        '''entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigRenameKeysEntry"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigRenameKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigRenameKeysEntry",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "rename_to": "renameTo",
        "overwrite_if_exists": "overwriteIfExists",
    },
)
class CloudwatchLogTransformerTransformerConfigRenameKeysEntry:
    def __init__(
        self,
        *,
        key: builtins.str,
        rename_to: builtins.str,
        overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.
        :param rename_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#rename_to CloudwatchLogTransformer#rename_to}.
        :param overwrite_if_exists: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1547e7b9a9aa7c005a44b729306eb640f9f2dbf2c3f056db958180e7c848f565)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument rename_to", value=rename_to, expected_type=type_hints["rename_to"])
            check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "rename_to": rename_to,
        }
        if overwrite_if_exists is not None:
            self._values["overwrite_if_exists"] = overwrite_if_exists

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rename_to(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#rename_to CloudwatchLogTransformer#rename_to}.'''
        result = self._values.get("rename_to")
        assert result is not None, "Required property 'rename_to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overwrite_if_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#overwrite_if_exists CloudwatchLogTransformer#overwrite_if_exists}.'''
        result = self._values.get("overwrite_if_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigRenameKeysEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigRenameKeysEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigRenameKeysEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a3c25f6955106c2a9f406c65453aef3166a96eb1e6af5705a17d0b5ffaeec9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigRenameKeysEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c794e14a03f0133d3365410272f8a8e0fa3347194a5d08d16d8ea89a782412fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigRenameKeysEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34aa4a0aa5fb5740cfe54f1b34797dbd101888cff0846b651d45687ae4dfa286)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62a5308dd5eb24f7922b35e529d2347fb50b3d31da74e05d1a8904392253c099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26105730137d8155eb632853ac2a36ed2c495a8ebd177a6682e951b79b833d2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeysEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeysEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeysEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2aed413ff2428599084a3edebcc23fe455d289da09017e68b9c65b1668c2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigRenameKeysEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigRenameKeysEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3152716d23c7ef748a48b81f5e6b6424d45d83aadabf0e6afca685b97d9ec51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOverwriteIfExists")
    def reset_overwrite_if_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteIfExists", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExistsInput")
    def overwrite_if_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteIfExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="renameToInput")
    def rename_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "renameToInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0a62b6273ba46df95adee0c822e9b1725c29f34fc7a17393c0d3a7b2bc8a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteIfExists")
    def overwrite_if_exists(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteIfExists"))

    @overwrite_if_exists.setter
    def overwrite_if_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c967dcbb1a506ca3fa41245efb962f48a688ac18cb3f55e3354fedd291fbe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteIfExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renameTo")
    def rename_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "renameTo"))

    @rename_to.setter
    def rename_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ce93369e9d0f03f780eda563702619e05d5e70ce9f525ecdf12edd96a76c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renameTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeysEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeysEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeysEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3ebbbe2df958d5f929782a752016be710294807cd90fee0492b4d6300d8e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigRenameKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigRenameKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e5ca9ca905ae0261bd27a14c87e424fe8dbb8df8718e46d9b86f5517262fa76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigRenameKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f732f670acf15345446ada1465ebf2edd5e783adf2137a25630c0cb6a85e8a8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigRenameKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0520e1b9ad2d6a3836c7aacfa342c9098cd252aac03d92dcd897da796ef91f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fb2a90a459af48b7f771f5f9bae2c3e928749edd8ab9d96f7d2ed1219feda7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c6425ed33b3fe844545fe71f8852f09969c13a74b632048ef041bfb67116976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b296fadc2a8185012713eda45ee430f1291e692bee46ef6d2de87633743269ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigRenameKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigRenameKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28b327e60e2540dcd6f72f8a011caca97064e40fe92a7b138febdb754dbc68a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEntry")
    def put_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigRenameKeysEntry, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74266748e939b05c082e1fa780a341af4d299ff948f7528b18fd6541798addd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntry", [value]))

    @jsii.member(jsii_name="resetEntry")
    def reset_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntry", []))

    @builtins.property
    @jsii.member(jsii_name="entry")
    def entry(self) -> CloudwatchLogTransformerTransformerConfigRenameKeysEntryList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigRenameKeysEntryList, jsii.get(self, "entry"))

    @builtins.property
    @jsii.member(jsii_name="entryInput")
    def entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeysEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeysEntry]]], jsii.get(self, "entryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09b5b563c364ffe32646e7ab37572eaf7be521b6492f64f9906b1bed500c5c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSplitString",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry"},
)
class CloudwatchLogTransformerTransformerConfigSplitString:
    def __init__(
        self,
        *,
        entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigSplitStringEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entry: entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af024799e4eefb48d6775b2100f8050015ff6f25ad6751d5c165c02b5e3aa409)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry is not None:
            self._values["entry"] = entry

    @builtins.property
    def entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSplitStringEntry"]]]:
        '''entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSplitStringEntry"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigSplitString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSplitStringEntry",
    jsii_struct_bases=[],
    name_mapping={"delimiter": "delimiter", "source": "source"},
)
class CloudwatchLogTransformerTransformerConfigSplitStringEntry:
    def __init__(self, *, delimiter: builtins.str, source: builtins.str) -> None:
        '''
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#delimiter CloudwatchLogTransformer#delimiter}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79078d47b3dd800cbb13ebc29841899995e3a0f9066c27d2fd55d2d088c31d5)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delimiter": delimiter,
            "source": source,
        }

    @builtins.property
    def delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#delimiter CloudwatchLogTransformer#delimiter}.'''
        result = self._values.get("delimiter")
        assert result is not None, "Required property 'delimiter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigSplitStringEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigSplitStringEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSplitStringEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28da1ed1a72772b05bdcd9844f7e4da10905851faaa6a85333fee08824aa6ae0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigSplitStringEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00bf2af26fe77d7e33ac299bc14b820e1b5fb1f3b09a6f18c26e7407513771c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigSplitStringEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5365c7f9c60240b2eeb4553d196f60ed4c224584b51908774288029833ddd99e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d9666bbe866b722753131e09b341ba069ce1163927270bc8cc3d497ae4716d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26663a93aea451b1032aa2cf2b82c8cfe382d6becd5097375ffdd27be1f21909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitStringEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitStringEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitStringEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643a244557af43f2747870db2ed21d8323d906b36a978d2e8a769ecbede37f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigSplitStringEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSplitStringEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aadd92bb464478a87edac05564b181579b415ee50e6cb947139bfd4306ead5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee1666ef4249707ad2e74d6eda38a089a329d4e2290958b3ba67ef9e44c44f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b78459ee096e20170825b0fe965575466151152c4e3e9e606115c271cbcb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitStringEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitStringEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitStringEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496b08f53fa353654edc30a870b87a8c1bf4db0ad36597eb532f9f5d061d006d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigSplitStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSplitStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a640f6bf1f9b122588ac192831676f8fb25c4600bf55fbcc73b2cf454df159ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigSplitStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e492e611422fd5dc989f45b30e11bcb2edfe94b2d90e3b14dc47e2865f111097)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigSplitStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a00d05bfb4714b6ecdb52b6b079c3eee695f0ae83c20c14993f5ef0973083f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a0f6142e1726e1376e8d90fbf9caea0a5fa008838b5c0abf42c9235f3135349)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76aec3e5afda30908714ac83ca8510a25edda91b7dc717dbbef3b108e068fd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069ef21a8f93b5921072914f9049f776eaf72875695ad5ffc3c66081266086a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigSplitStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSplitStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4db654b6f114932b2d21f7cb9f321a7c8ba8b205cdd82287edf39fd42ebbc17e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEntry")
    def put_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSplitStringEntry, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d445a2f17753f80f641a6406e3fbf449b28086284e4ef12975fd60a5d71d719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntry", [value]))

    @jsii.member(jsii_name="resetEntry")
    def reset_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntry", []))

    @builtins.property
    @jsii.member(jsii_name="entry")
    def entry(self) -> CloudwatchLogTransformerTransformerConfigSplitStringEntryList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigSplitStringEntryList, jsii.get(self, "entry"))

    @builtins.property
    @jsii.member(jsii_name="entryInput")
    def entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitStringEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitStringEntry]]], jsii.get(self, "entryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6506f3386c74d76395505a9148de903068eb81eaaf8c1651ccd345bed729d5df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSubstituteString",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry"},
)
class CloudwatchLogTransformerTransformerConfigSubstituteString:
    def __init__(
        self,
        *,
        entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigSubstituteStringEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entry: entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3c138d1d227864efd217f28bddfb4c7435a7a438b634f35299b86283080e67)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry is not None:
            self._values["entry"] = entry

    @builtins.property
    def entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSubstituteStringEntry"]]]:
        '''entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigSubstituteStringEntry"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigSubstituteString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSubstituteStringEntry",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "source": "source", "to": "to"},
)
class CloudwatchLogTransformerTransformerConfigSubstituteStringEntry:
    def __init__(
        self,
        *,
        from_: builtins.str,
        source: builtins.str,
        to: builtins.str,
    ) -> None:
        '''
        :param from_: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#from CloudwatchLogTransformer#from}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.
        :param to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#to CloudwatchLogTransformer#to}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639c1bd7dd405767b591429aa2855db88e161d5cb48a807da7660646ae350b35)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "from_": from_,
            "source": source,
            "to": to,
        }

    @builtins.property
    def from_(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#from CloudwatchLogTransformer#from}.'''
        result = self._values.get("from_")
        assert result is not None, "Required property 'from_' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#source CloudwatchLogTransformer#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#to CloudwatchLogTransformer#to}.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigSubstituteStringEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigSubstituteStringEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSubstituteStringEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a2e6597a7098dc8e8865a312fda4a679ebc39c7b761041ba053d6e798a72b01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigSubstituteStringEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfce4c8b7cbd9a0b2cd9ba486991190a38581845570c54c275ce5bb99e34e344)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigSubstituteStringEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2684ad3c71e53f9874c1b35da65e767ddb1cca386ed805def1e1c8c5992f7a4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30b43af111e14670b94a24095ebba9aac32b907f0ad90a9b968f9e3b94f6a6f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4377aeb58802c568283e87be268711582df3cb6cfb84d2ae8590b30e6a8a0d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1839ce7577ed032db655bc0ccaab884fd135eef56a740b09f2fba5fffda1ac6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigSubstituteStringEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSubstituteStringEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb8c4598df3d82d06b153ebf1f865013464225f6b89ada5c700169d8f04086a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="toInput")
    def to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toInput"))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9915248aae7e1a943c8d54d0252064046c09e537e9c44f9066c2be3adb597ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9383674cd5d7c54e97581544ad237cd73d9a97665c0eacb3e52ff93d003ff5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="to")
    def to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "to"))

    @to.setter
    def to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9239162eacf23c6bad9cc6de2c55fb5ed496070bf2e8a4b5572eddb6f83d5c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "to", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97375fb7c3343b0fa6b291a1677c50f58d5bdc6b93bb69861d15ca6673a9b2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigSubstituteStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSubstituteStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c998ccf814f160ec60384038c37926de73425704670bfad77bf2428a14f793e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigSubstituteStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39838b3c2fce972ef9f67879c157013222f8b1df3b980b1dab8ebce6b45dd52)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigSubstituteStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57da22c36ef8ccd5fca02b5626d55d06feb96127a366d1741341e029093d517)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc81eba8139b18f3bd00774eebc1d722ad46d23705403761003dcb67b10fb1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16e048dbc0ca60d6ddca3cd8c432f8c25828ef9bf6e6bcd41393eecd8fcd48a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0de34008a43eba87afb6d1bef5b1fa3051cf78eab8e814740fb0f403439477c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigSubstituteStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigSubstituteStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08054d0b5af2455e9e7f873c5f5aa84556bbf3435a23de2f79169d39b1027f36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEntry")
    def put_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c574db98d976aad9dd230fdc9af09c488441546085c5d1405d02b44a0898569f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntry", [value]))

    @jsii.member(jsii_name="resetEntry")
    def reset_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntry", []))

    @builtins.property
    @jsii.member(jsii_name="entry")
    def entry(
        self,
    ) -> CloudwatchLogTransformerTransformerConfigSubstituteStringEntryList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigSubstituteStringEntryList, jsii.get(self, "entry"))

    @builtins.property
    @jsii.member(jsii_name="entryInput")
    def entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]]], jsii.get(self, "entryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0999f5603891155b145b087037d44e8f190820521534442605df58fb6859158a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTrimString",
    jsii_struct_bases=[],
    name_mapping={"with_keys": "withKeys"},
)
class CloudwatchLogTransformerTransformerConfigTrimString:
    def __init__(self, *, with_keys: typing.Sequence[builtins.str]) -> None:
        '''
        :param with_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca44f1deacf6d189dcdc80735e3644791a9e1c29ee07117a6ac99aafab724a61)
            check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "with_keys": with_keys,
        }

    @builtins.property
    def with_keys(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.'''
        result = self._values.get("with_keys")
        assert result is not None, "Required property 'with_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigTrimString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigTrimStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTrimStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__381d2391ab62d12366376f7c38b2cc8b25a6b909eeff19067c9c14015e9ada78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigTrimStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf141e8ab03677e87be90de7c6335fcf021c773a5de25ca6272f124d3d64a1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigTrimStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0418928b6165b55cd48b0cb736bdd21c4350d6144476ae83e4d9496fb465be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__407cc7d8205b1e821336884d551f7368ccc89d9a9a37a83c5e0561d66d042e99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__262e54c7d7f0b810ebf2800335df13a005ae52799a7893428f3b0ba6ca75c68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTrimString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTrimString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTrimString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c94ca14846fc501d4dbe349ef50c89ae359ea9b59898a120004816a60644f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigTrimStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTrimStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__010521b3af75826c8e9d9464ea9682bbc4056238505558a6ca6e6e645294d029)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="withKeysInput")
    def with_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "withKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="withKeys")
    def with_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "withKeys"))

    @with_keys.setter
    def with_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6468b46ccda524c31077f0684321c73436975361f71e018164738fd00d696dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTrimString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTrimString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTrimString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3464e40d787fb06b85af911d5562979a38252924c7f3f843f14d092098a887df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTypeConverter",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry"},
)
class CloudwatchLogTransformerTransformerConfigTypeConverter:
    def __init__(
        self,
        *,
        entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchLogTransformerTransformerConfigTypeConverterEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entry: entry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cda410fa5602d4752b7eed4975bf881a29d0912dd6ecc704bf54c8553930a5)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if entry is not None:
            self._values["entry"] = entry

    @builtins.property
    def entry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTypeConverterEntry"]]]:
        '''entry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#entry CloudwatchLogTransformer#entry}
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchLogTransformerTransformerConfigTypeConverterEntry"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigTypeConverter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTypeConverterEntry",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type"},
)
class CloudwatchLogTransformerTransformerConfigTypeConverterEntry:
    def __init__(self, *, key: builtins.str, type: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#type CloudwatchLogTransformer#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281d4d72b4d089d4d03a699597cb50cd07da2fa17e391364af79c2f81c4427eb)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "type": type,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#key CloudwatchLogTransformer#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#type CloudwatchLogTransformer#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigTypeConverterEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigTypeConverterEntryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTypeConverterEntryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0d4e35415b2cd03428a0a8d61d071e87ad17621d97068ea9367a348df4c5b2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigTypeConverterEntryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67da1a099734770a73ab728b7d5b95c986db9e520734aa9f15deddf1e41f8815)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigTypeConverterEntryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a43d7a162b0a42ba381b7284a25ea9b71715c0ed18337e24d69a449b64108e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1193bed62f1a663d8665bb098066836bd03e6db1e20e76d61294c58bc77063c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fda61d4cf9295bf7069cd9f2c35f4d0d761edebaf1da5afafa81f45498960009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverterEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverterEntry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverterEntry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc24dea59be5d61cde974a0f2c30b777a03c24f04f57e305db6c6799e750d248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigTypeConverterEntryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTypeConverterEntryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b379c8223a77ba9163b2b614ee8d166c1902ccbdfc5e18f0afa9227c473fe6)
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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a708d4583125cd87101242c1f6559b60abfe086d5478b89510a43312d30ab38f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759d903f68c8cf0700ea98f3c6e7f5c7f331d2422d2e16e355994744385dde88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverterEntry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverterEntry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverterEntry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4331ef2ee71c87c3a74686768944c6a753680c778083180cad6a1fe687f89cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigTypeConverterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTypeConverterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4a1d1efc7dd06c80e1112b1b084a2cf0cdbdf8d07e1016bb46c46c312774274)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigTypeConverterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3fbd7f3dbf5ec67e8fa82513e22d2fae12cfff7bb033463f38875f9fbd358a3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigTypeConverterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c38806dc97a02e7fe79c6679d9792f60b76c4a3490bf35ce487d188869bea34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d00862ee75d8c56f905d4583c57063cb99529d3bde635e05fc1a3f090b5c0884)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbf1e2235ab28e9a2021ead2d7edeed3143590d44a75dc05cf5335ccc796207c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db30f7b7395d89304163d0f4fdcc81d49b6117eafeb268e714b7e4164e89004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigTypeConverterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigTypeConverterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__270309791485cde47f986d441ebd2bda8aa7f9bbced3ee27b3111544eb506813)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEntry")
    def put_entry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigTypeConverterEntry, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0339a6b57149fccad1dea2f83e34de35bd5aa1acf14a92e3d2d4148a7461c486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEntry", [value]))

    @jsii.member(jsii_name="resetEntry")
    def reset_entry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntry", []))

    @builtins.property
    @jsii.member(jsii_name="entry")
    def entry(self) -> CloudwatchLogTransformerTransformerConfigTypeConverterEntryList:
        return typing.cast(CloudwatchLogTransformerTransformerConfigTypeConverterEntryList, jsii.get(self, "entry"))

    @builtins.property
    @jsii.member(jsii_name="entryInput")
    def entry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverterEntry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverterEntry]]], jsii.get(self, "entryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb27b94491b4a741da09b6724f14f14f92148ea857c7e3252a45d5ce554cf1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigUpperCaseString",
    jsii_struct_bases=[],
    name_mapping={"with_keys": "withKeys"},
)
class CloudwatchLogTransformerTransformerConfigUpperCaseString:
    def __init__(self, *, with_keys: typing.Sequence[builtins.str]) -> None:
        '''
        :param with_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e7077f9bd1654858a7ac90909f1ccd2486187e2491b4bfe510656b6a84a13e)
            check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "with_keys": with_keys,
        }

    @builtins.property
    def with_keys(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/cloudwatch_log_transformer#with_keys CloudwatchLogTransformer#with_keys}.'''
        result = self._values.get("with_keys")
        assert result is not None, "Required property 'with_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchLogTransformerTransformerConfigUpperCaseString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchLogTransformerTransformerConfigUpperCaseStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigUpperCaseStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__615a5303a74352aa3ed7ba6940c724c68313d2535ead07d92a581e334b2c5a6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchLogTransformerTransformerConfigUpperCaseStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f35406148957aee01371a666fae1ae769543336628ad4c88882911134a3d087)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchLogTransformerTransformerConfigUpperCaseStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d863afa889628a4b3055736588c5a4c18b8fba49b92b2a7e70d8bcf0dd9f99b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2005513c5f1c77a00e9ea13bee2007ea9b99886db296171b7a46dbc8d915a443)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cc114d6c21e6073bcd3fb450c1f380b43f41e94275d5c1cc0d74dcd92f35977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigUpperCaseString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigUpperCaseString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigUpperCaseString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05aad38ca82de8534de087e64ebd9ada2430dbd0c224480e9d04d6d847a737a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchLogTransformerTransformerConfigUpperCaseStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchLogTransformer.CloudwatchLogTransformerTransformerConfigUpperCaseStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a478afdc6da559b734ca5049749fe8a3d336ff62ca372de2aab7691be695aba7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="withKeysInput")
    def with_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "withKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="withKeys")
    def with_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "withKeys"))

    @with_keys.setter
    def with_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31713275edf65168355d6345d4077dac1f44c2f99139db8e0f0e8fa8865f17ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigUpperCaseString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigUpperCaseString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigUpperCaseString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c17e9fdfb6557895514c282054c5c964061c51b538373729849ab1b9213b220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudwatchLogTransformer",
    "CloudwatchLogTransformerConfig",
    "CloudwatchLogTransformerTransformerConfig",
    "CloudwatchLogTransformerTransformerConfigAddKeys",
    "CloudwatchLogTransformerTransformerConfigAddKeysEntry",
    "CloudwatchLogTransformerTransformerConfigAddKeysEntryList",
    "CloudwatchLogTransformerTransformerConfigAddKeysEntryOutputReference",
    "CloudwatchLogTransformerTransformerConfigAddKeysList",
    "CloudwatchLogTransformerTransformerConfigAddKeysOutputReference",
    "CloudwatchLogTransformerTransformerConfigCopyValue",
    "CloudwatchLogTransformerTransformerConfigCopyValueEntry",
    "CloudwatchLogTransformerTransformerConfigCopyValueEntryList",
    "CloudwatchLogTransformerTransformerConfigCopyValueEntryOutputReference",
    "CloudwatchLogTransformerTransformerConfigCopyValueList",
    "CloudwatchLogTransformerTransformerConfigCopyValueOutputReference",
    "CloudwatchLogTransformerTransformerConfigCsv",
    "CloudwatchLogTransformerTransformerConfigCsvList",
    "CloudwatchLogTransformerTransformerConfigCsvOutputReference",
    "CloudwatchLogTransformerTransformerConfigDateTimeConverter",
    "CloudwatchLogTransformerTransformerConfigDateTimeConverterList",
    "CloudwatchLogTransformerTransformerConfigDateTimeConverterOutputReference",
    "CloudwatchLogTransformerTransformerConfigDeleteKeys",
    "CloudwatchLogTransformerTransformerConfigDeleteKeysList",
    "CloudwatchLogTransformerTransformerConfigDeleteKeysOutputReference",
    "CloudwatchLogTransformerTransformerConfigGrok",
    "CloudwatchLogTransformerTransformerConfigGrokList",
    "CloudwatchLogTransformerTransformerConfigGrokOutputReference",
    "CloudwatchLogTransformerTransformerConfigList",
    "CloudwatchLogTransformerTransformerConfigListToMap",
    "CloudwatchLogTransformerTransformerConfigListToMapList",
    "CloudwatchLogTransformerTransformerConfigListToMapOutputReference",
    "CloudwatchLogTransformerTransformerConfigLowerCaseString",
    "CloudwatchLogTransformerTransformerConfigLowerCaseStringList",
    "CloudwatchLogTransformerTransformerConfigLowerCaseStringOutputReference",
    "CloudwatchLogTransformerTransformerConfigMoveKeys",
    "CloudwatchLogTransformerTransformerConfigMoveKeysEntry",
    "CloudwatchLogTransformerTransformerConfigMoveKeysEntryList",
    "CloudwatchLogTransformerTransformerConfigMoveKeysEntryOutputReference",
    "CloudwatchLogTransformerTransformerConfigMoveKeysList",
    "CloudwatchLogTransformerTransformerConfigMoveKeysOutputReference",
    "CloudwatchLogTransformerTransformerConfigOutputReference",
    "CloudwatchLogTransformerTransformerConfigParseCloudfront",
    "CloudwatchLogTransformerTransformerConfigParseCloudfrontList",
    "CloudwatchLogTransformerTransformerConfigParseCloudfrontOutputReference",
    "CloudwatchLogTransformerTransformerConfigParseJson",
    "CloudwatchLogTransformerTransformerConfigParseJsonList",
    "CloudwatchLogTransformerTransformerConfigParseJsonOutputReference",
    "CloudwatchLogTransformerTransformerConfigParseKeyValue",
    "CloudwatchLogTransformerTransformerConfigParseKeyValueList",
    "CloudwatchLogTransformerTransformerConfigParseKeyValueOutputReference",
    "CloudwatchLogTransformerTransformerConfigParsePostgres",
    "CloudwatchLogTransformerTransformerConfigParsePostgresList",
    "CloudwatchLogTransformerTransformerConfigParsePostgresOutputReference",
    "CloudwatchLogTransformerTransformerConfigParseRoute53",
    "CloudwatchLogTransformerTransformerConfigParseRoute53List",
    "CloudwatchLogTransformerTransformerConfigParseRoute53OutputReference",
    "CloudwatchLogTransformerTransformerConfigParseToOcsf",
    "CloudwatchLogTransformerTransformerConfigParseToOcsfList",
    "CloudwatchLogTransformerTransformerConfigParseToOcsfOutputReference",
    "CloudwatchLogTransformerTransformerConfigParseVpc",
    "CloudwatchLogTransformerTransformerConfigParseVpcList",
    "CloudwatchLogTransformerTransformerConfigParseVpcOutputReference",
    "CloudwatchLogTransformerTransformerConfigParseWaf",
    "CloudwatchLogTransformerTransformerConfigParseWafList",
    "CloudwatchLogTransformerTransformerConfigParseWafOutputReference",
    "CloudwatchLogTransformerTransformerConfigRenameKeys",
    "CloudwatchLogTransformerTransformerConfigRenameKeysEntry",
    "CloudwatchLogTransformerTransformerConfigRenameKeysEntryList",
    "CloudwatchLogTransformerTransformerConfigRenameKeysEntryOutputReference",
    "CloudwatchLogTransformerTransformerConfigRenameKeysList",
    "CloudwatchLogTransformerTransformerConfigRenameKeysOutputReference",
    "CloudwatchLogTransformerTransformerConfigSplitString",
    "CloudwatchLogTransformerTransformerConfigSplitStringEntry",
    "CloudwatchLogTransformerTransformerConfigSplitStringEntryList",
    "CloudwatchLogTransformerTransformerConfigSplitStringEntryOutputReference",
    "CloudwatchLogTransformerTransformerConfigSplitStringList",
    "CloudwatchLogTransformerTransformerConfigSplitStringOutputReference",
    "CloudwatchLogTransformerTransformerConfigSubstituteString",
    "CloudwatchLogTransformerTransformerConfigSubstituteStringEntry",
    "CloudwatchLogTransformerTransformerConfigSubstituteStringEntryList",
    "CloudwatchLogTransformerTransformerConfigSubstituteStringEntryOutputReference",
    "CloudwatchLogTransformerTransformerConfigSubstituteStringList",
    "CloudwatchLogTransformerTransformerConfigSubstituteStringOutputReference",
    "CloudwatchLogTransformerTransformerConfigTrimString",
    "CloudwatchLogTransformerTransformerConfigTrimStringList",
    "CloudwatchLogTransformerTransformerConfigTrimStringOutputReference",
    "CloudwatchLogTransformerTransformerConfigTypeConverter",
    "CloudwatchLogTransformerTransformerConfigTypeConverterEntry",
    "CloudwatchLogTransformerTransformerConfigTypeConverterEntryList",
    "CloudwatchLogTransformerTransformerConfigTypeConverterEntryOutputReference",
    "CloudwatchLogTransformerTransformerConfigTypeConverterList",
    "CloudwatchLogTransformerTransformerConfigTypeConverterOutputReference",
    "CloudwatchLogTransformerTransformerConfigUpperCaseString",
    "CloudwatchLogTransformerTransformerConfigUpperCaseStringList",
    "CloudwatchLogTransformerTransformerConfigUpperCaseStringOutputReference",
]

publication.publish()

def _typecheckingstub__4c36969cc39a3712e08b49439f37abfaa97a91da915b31a7fc8675034b887755(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group_arn: builtins.str,
    region: typing.Optional[builtins.str] = None,
    transformer_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__6204bff60aa4592e2ded4ff755210de54ca1a587f42a658a199b8ee5df7367d3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b89437e4d33e6db26a83bbb31cc4749dccbb3f4fc2d3832f5010293a375d809(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5067f04ce3c8f32cbcbac5aae47a5c10c4cb2ad4c19b5a22d4d24506c8176f95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3042dc25f6d7cd2b6338039c0273c3dfa7a8a6ef8327b1dc1904165405ba0ff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1812fb2d38fd4c3d3860135319e49d0171a220eb97d89bafcc81455aa5f3493(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_group_arn: builtins.str,
    region: typing.Optional[builtins.str] = None,
    transformer_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914d5b1e5db99c195fbc4e8ab2cf154404a9b541779bd303440e943aca27e17c(
    *,
    add_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigAddKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    copy_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCopyValue, typing.Dict[builtins.str, typing.Any]]]]] = None,
    csv: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCsv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    date_time_converter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigDateTimeConverter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    delete_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigDeleteKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    grok: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigGrok, typing.Dict[builtins.str, typing.Any]]]]] = None,
    list_to_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigListToMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lower_case_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigLowerCaseString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    move_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigMoveKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_cloudfront: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseCloudfront, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseJson, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_key_value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseKeyValue, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_postgres: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParsePostgres, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_route53: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseRoute53, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_to_ocsf: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseToOcsf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_vpc: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseVpc, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_waf: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseWaf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rename_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigRenameKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    split_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSplitString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    substitute_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSubstituteString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trim_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigTrimString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type_converter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigTypeConverter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    upper_case_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigUpperCaseString, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fed55d03c26775187137d06980797ee3ccccafb31dc48260c069e4932108daf(
    *,
    entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigAddKeysEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae3b47fe61f71ff6c54247b4ddf3bb267bf33bff13b3bc4e6fc5b5436db7e0f(
    *,
    key: builtins.str,
    value: builtins.str,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542ad670ae56bfc3b52f62af263b621a38b5d740e1335fc4403a7b7e369f0d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e894e20bb48ed2f72812a9df194994d8ba5f9ba84fed16f03d750ccc5137cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c52d8eb6f4aca11f1fcfc73f1e37ef242895a1f198060943c93393a95ce0e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1affb74e796fd9afe5d37f6497a2ee19d57955113c2345707ec8856b559db8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bbc4e861c67f30c1cc8540e7353bc85593b41367c52269b6a4bc46b6009028(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d794f68027b3916c403070526e48c5305032f4818a410a33e166243b32055ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeysEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405d48d8586614d8e4fdbc743f6365dd6c97bfcbdee112aca64b2548ac9a2065(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef35d304919b48635a1c30f784cc9ec0bf13f36c347d17f562cf8e55792c6080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d56cdbd27900e303d0cac18c91e17dcea20c340cb5eef14e958fe2319f4039a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002568abd4c8d91c89dd41b566941279e01ed15e0480f7c60c21e08204d78b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506224493c62b90f96f8ba627815b30e2c33241ccdf7554353caecd18d9a80af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeysEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57577fcd721742e699a8af562664dd532c376721bc24c70fe546d4e0bbda5d48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be6bb448584d3040a66ccd09323aa3c6f621629f229a41db444b16e73854a6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba6e6dcde3a116b6aed2fa8464e1516910cb31792bce71254767ef6f9170794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0399706d1460b043f54b8464ccdba84351bc48c79de4feb83175f0581a122ae0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5026ca4c0404c4d3aee57eb67a32ff978a6e6c6f860ccd7c87535feb39c59d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fda2c9b29fcd19f0ae2e7ec730044be209a16ea79cea474a3d833a84c136a7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigAddKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1119c426f3738d7f9eebcec2a2f3d5588ee343c76b015af1aa03b09aea78442f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1f7961a9962723a6088c072f6dfe067abbfb72860944dd859415cc9de4fd3b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigAddKeysEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de9cce377581421eeaf4d346efda68ace0a475fe815deb113297416749c4030(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigAddKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0649b40eac7a06e1d2fd23286c029a612b131cbe9a9c6a02fea433f031c8c29e(
    *,
    entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCopyValueEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78989d51b605a65ec09e0f1665e21f8020a7f77039322f7437bcf9589ab85750(
    *,
    source: builtins.str,
    target: builtins.str,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a696db04289ea8b7fba15d69b18b6c3fa1abff64b1cc7a75d53f7d0f124e967b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7529a4a30a358d0eff845f9e641259316e7d058d54f165ff7ede57fc00e8d591(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2827130ba63ada66e9e8e2751bfeea4ec82954ab1789fa396b13c31a8767de8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1d8795d35cbbdde01078392ebe03e968b74967cda3de8dbefe361d25667ab6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919535d1edacd5555f6978f440ef2c6af1c244f2c82baf7691a158b16d2e5dca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076ae7cb4f0ff3dc1a14dc2a58dba92d8a8be2265881c7b65be683701fff75f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValueEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244985696f6348dc46878e42ba1eca03c29af77dace8dbc637a16577d9ecf717(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88456b787cd33a3658eefb746aee9e9ffee062dbf12413cae1dc156d43395ea1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a7639ced8a817810ba3a75463c9ffb63ac460338a0fd8ff518c7edf0e329ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6d055fbdf4b1796a9a5bf7569d2c49919ca647d60b997a271aed1e4cc64733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496b5f50a2129b6814dd887130ac622dca4183be83b60270ca897989faee8feb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValueEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6d866877af6f5c727116fdefec29131f3eaf97fdd59d6de8a9bf7c0c74ce31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5433d3388eb1f9a55dca94eaee558048f71e5369665f1d2f5408eff5dca8fb28(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b48ab01f3b3118df166e891f481d876f6eb02f34a6cd3adcb96f3af2e597a5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d73eb6ca2f78ab477f35cf853878115ed3197b9af5f631da4f02732fb4e143(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543bab7ae042bffa8bae4817a6655f619c347f84c4c14980c0c5d6a7bc7da733(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f001349d1a404b923ca5e932d7f5964a51244946e675ea3ec36abe3629e33b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCopyValue]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3433715805a8bc26e0d2be67a06bdf3dffd91e99a90fa479e1cf6ce5c78bfc8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49555e49f42a20fbfa61faee360c2bb03784658a8e018ee995860f19ba2f919(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCopyValueEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7aca0c690c462224e0ffd69edd3dc1dbb67e5e27d9c3fa19f206f75361efdc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCopyValue]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d554579a52894a9a10756bcccb6c6ed418248967e551759a7fa212be45f62f(
    *,
    columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    quote_character: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f308640224fe44289ea17b3f90a61f6713780140ee3b49766b2aa30bc28fe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39e46861460f2c679bca9d650684a00cf0b1de620128b82dd7b449f2b90cda9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f122bfd7973e2f928923607e758b2a4b19d4bb174cb18795239a1aa4bb09021a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0514c28fd373fb9f977f6a912cd6ff3623184cb34f1417e64ac684418c7656dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db43d4311c9897829e562fe73cbd8e0145e44cb162917462985c646596101c15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4849a105d7cab2d580761df870ca0dce130dc8ecda68755f96c66cbe0d05d312(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigCsv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f989b58720cb10ca0e0f61b69ce3823f26b3b40d9ef820cc4abcbd11d24fe73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce1c299eb6323947e19b542eac1d3c02e7c0d43884eacb31a790b68b0d6d7ec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef016b4ee6866473817960972fadc92688e7c40c655d88cd75cdd7b14020dc97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5e62aad385afbece00097bfca455a302972bf234e4822a658f33ee748c38ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5034f77994c2229d7f1c0b78817162c8eba9ccfd2be145524450717a64d6a606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0971ad0b386acfd2c137c73fbb69bd82f44439ddb7dbc2a5386dc68ba6db590c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigCsv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e863f4c091697276b2a71ad7abd84b9bf65506389b9dada7b3eae34e7f9301cf(
    *,
    match_patterns: typing.Sequence[builtins.str],
    source: builtins.str,
    target: builtins.str,
    locale: typing.Optional[builtins.str] = None,
    source_timezone: typing.Optional[builtins.str] = None,
    target_format: typing.Optional[builtins.str] = None,
    target_timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1798b67a13037ebe3b5d9f8c99b23c78664b1cf9bb7399c4f249ab4b24ddea7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d541459d88a8b505515a621e7846f3f92edbbf824f20201287fd4ec0bc8fff6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5dd8527d83bbc91cbdfa0dd3b9e2273b4b4cc9d730850fb5faebf98c179c6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c25422e4a737d2035da4c0eb2b11dd05290dd598087053c65ad892d9d61de9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381d99e7a6b69f9eab1171e5d02243287e0586bb4efbb9297325c2c0973e33fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca2ea5cb3477259bef4c1228b8d50e428e5282a2f05d64706e23b6108557598(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDateTimeConverter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e425aab2ad6598eb204faf8cb82adf3fc3cdf0deffe35e15728a0ad6b6169e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69501efecb8b7ad567ac494c70ee52ace60ed6b17a4687a97fce91c2e2461f42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889d28fe35bee9dd68d605bb62ccd7390054d633317ce360f673db4c04d880c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c6812a845f3aa16b56399fa2f8bdcff70d7e0e2812547e338f66f7a16b4811(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097c63e88617c040d58b1b1e71a620319693743b566e70ddb3dcc1fbc42b148d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1d28be2995321edb9e100fbd504b3ef5d5fc0a8b4275868132b16e842f1150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ecce82edbafa6e68bd807f5c8c772db86b7fedddd226c5838e741c493aab2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6ad5554161d64f781f3c8e1b6aaf4e650021a54d33a37f1024552f59357eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d69849c04a742796e1e31af07e5db9d86de85513585ddf94e174b3213c9b00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDateTimeConverter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd8406ab950b30fe2c2c7d9ef5186c586e8d343b1eeac1fb40e2d0cb6ff30ca(
    *,
    with_keys: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11386b2297028334497a8fccde3a3521201831cacf92289f24e49c8eb2680cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f48398865ddcb0d7b701b1156e58a3ea84d7ef4be9bd9e25a10b1e94ed226e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdddf752ba658f943db2f3bc319c81234e151690828910cfdae1b88bd2c14273(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b025a869ee00d134e14f8ed89b9b31e62278b7cd28a03691858183d6928b32c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275a4b144f83e2152bb0696b2d546f3853fe3cf7d7aad0953d619d5e6a74ec41(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9f58bf661be7c5157c79b6c6e0aef5eaab8e8a8840737e41305ed23e335840(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigDeleteKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86ef7e4128a91b892d637b310dd4c02e032fd51d2a8c0393f6c175eee9a2118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f88f3a31d84986f8d23f609aef219414497d1626712cc65da0b54f53a34f449(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6fb0d0bf2938124aebffd6dac2490401c251659b04aba6d8c5bf90f212ceda8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigDeleteKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5b9464f98c6680da4b938e88465973eed833e227f7847b35346e596019cf56(
    *,
    match: builtins.str,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682e2a464e226285b49f7e750141051791483f389d23d929130d08378be2b62a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79aea2746c5f440b4127dd61a159e4c4daac32009d09c8e0af300f4345cb0b98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3281442c704817b7a58ba5b36c3edf7a152f7cda2b8c31cc55b35851956e6482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0939ae76fec75367f1395313e4c35cc2615b4af4725677381b1c9ac0b745cb41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f70da70970fa2a1bd26c5582e9b09b1c83d50a35f75acc39a49ec9c3dcc6e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe7aed7abed8a418ba64c03503e550e353bf14e298a2a5b294a36ba8ff4eaac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigGrok]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eff3a88b7bc1888405a7062cddec4aeb23dd2ff248e44d8d8ad4966c02baf1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1805b9db89e7b9edabe4179195b59a086c107c1b1b7ca11daf54016e954f1c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb630f8a5aa44e27fe9fe698504c5ef8919ec513bae85dc14819d40095a620a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c119b9a46affde951245131cd87dc5902c0ae48ef2e2f399ca78149952378b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigGrok]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916d2f8404a22976659e740238ff401b7d2197eb8417e989f97330ec0bc65442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be25f60176a8b50708c713a1a132062e4e5684d65e51210b7bf7fd201270bbc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5908f19a6de81b1c0596353e83e2fee7296cc46cc19ea72c59ac046b5424c7f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4974b926ca7a141dd806c12b7104bcd3b4e112027691ed89ee9ebe7adf3965(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a21c35674de48c79a301402d5fbd32307475266518ecc76b5081abd2395eef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3887c6983d51c677af825175710e6985a37514024e7665860cf556c20cff65b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc91ca19c40650791a56a639d3264be9ef47b55751d90e8204f4d2d63e5efed4(
    *,
    key: builtins.str,
    source: builtins.str,
    flatten: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    flattened_element: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    value_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2115d05b37e73dbf8b25181664a8841088db3d114fbca6c5a0a0161b779ba108(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0deec93540d86ad9b8c38995d75376e7eed512bf1293a72ac16f1db365ee6821(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f938acff6e41aff4a066e08a42b7a48838be7608274966fa3edec1966dc2fb61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccffc10750c4c3203b919d4144c3ee07885932ddd6d8a8c10975df70caf8c0e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a966fe6ab1e301d232b983b7d28bb91cfecebfec5fa8e0863480a3d68bef0885(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6ce31e0ed85922daa3c977ac11b3c3e9c0f20d4bbe3f83d4d79a1504cf9ea6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigListToMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d11464fc732b00e46bceb186be88eb045841948cdea81fca2177805648e0db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9494793b805b043667119944b156fc9955cb5e38763aa746af674ddcd624e74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4979e3ae8aa4bf339e342dd6428c93a3cbdae2f7471cf7de9f6625a787b67fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad7ae2d9753de7bf88ac29aba2af7f03b25e609efab9d72c31b508750a03e7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73410b12680faca2189500c74e2a9855c40edde8771fc14a45f2b612ff53944(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551d783e82fabfb55fb1bb910584dc78914803f3bdedb521c97bc6ad03b3a709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7023c732f9ff4a23a46bbcb80b7316b2c34942e1f84ff6f2e6d988635000af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b257b3fb1320c8488351e38e9122cb6fc52d4979a722a4d85faf74d916f429a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigListToMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41374eb17c53962a8d76dbac51115e7eb3584cbdb8e2f355cfa0a1266b7de9dc(
    *,
    with_keys: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5a68933394574570c0797cc2d42fb24db6680d3ddb7a7a33b9d353730383d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5deb17d12bba7f17213f7caa2c9bd0e4f4e4bed536bcc3457ac0d9e1558d7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f61e9b3010207e0df3ac821c7db33dae76a276ec8cb6cd33515e5732668fd10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b53d49c77b120652e82084d0f5c4f11f76538708a1e63e9a38d5b00ea17bb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f582719e402e7dd2ebebc06dfe6adc5dec2b1808c76b22a23f94c8f534b212(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5cda84c9ceef911ea783242ed0c485f8479848ff997cd5d8d4d4d86bcbdf1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigLowerCaseString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa43d0287aef7cca3c28091152fd5b7dc685481ddade7311519e7eb79394e27d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb63d546444121ee5ae7cd26e00aa6732cc37634977099648ce71bb57ee40dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c70531ad522853867dd8ba13d619f6fb7fa335601bb445052415d86f87a4c95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigLowerCaseString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedb7abb82e9364f66b643be5ae4c860a3ef034f9bb2fa90591b6c613fc4edaa(
    *,
    entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigMoveKeysEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692c7efad9e10ebcae250d9c2a4cd37566fcca89676f58d5a2da2c9fba1a5637(
    *,
    source: builtins.str,
    target: builtins.str,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320e208907b1cf85c691b6e70ab5fd4ddaf1822218fa913dba22711e46fc7883(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1a2a85af50cd36f6d04b4c9da6e0fc2e44b9b59eb60b6f8b13b94040154d83(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779ad649353a08692c8a14033ef9979ed29d08494d701c70e5b060599b5a6963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9911b0de42318cd59025f538742d3c77615b72827c5c8e7b1e0e510a6611b7c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca49d80f933c333fec6eef47f256a6d1e06e952f363f98e2cb5c2c51cad5b8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fe58e5814bf667f02deb99c9d66bdc2468071070fed45d23cadd218760a56b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeysEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad356acd88340564ab3985eb5a8ee9c06f080c53ad6aa904c7f15be81c4ff51d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fdc1e4b3c306da5df1d3eea1e4546ea3a99d393aadc4dddfbb46c91193fa11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7634065105950284b1f32876d19964dfac87bd43a707bbdbf0acc8e8135bbde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db72fdafdb5635a39ca52c0d600f0208ced3f61625b83dc71159184d62efa6e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441e6869c4524fc9ae4b73f46f6fa8eb391a95266d3fd862d852efcf8bb4503a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeysEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64afe641c4ba2e11455a60686c1335dd28eb77188ffd69910e71857dde17f7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2975d76ae4fa935a0e8551a5fb61b5ade49f3a912c7c86fa42f1ed31102103(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8bd7196938fc9fb26a79f65dfa1eef0acbc20ac031201b5370b446135857dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216dcf365ac6570af396fba01afeeb85e3af947d6179dd5105ddf4f5c0b26d6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62555cf2e15352e8f7c5df47b8652d25313a3186ac3c8118cd776b8befda3cfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c957bdd9f29cbc13f8db41926c0dcf2cc33d8f09c11189a51a4732007403d7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigMoveKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617aa53a95c99b3f5be105c8734e40a995db2b4498cd8761373ec4c212f4994e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf5c63c71e0edffbc48f4fbd0a8301cc7f7372b2575abc9ebb80ca42451db6b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigMoveKeysEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647ba4e0c69a2b560270f6afb9086e06c56c8e2d63a36591a0508fdd4b8989f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigMoveKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c73c5e54961328b019d8805fb8358201256262be2d44f433e00932fb57b3957(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0543f88be8f37ee0cfe9011b7764eb4604cdc9181e60a68dde05331b41478a06(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigAddKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6673023a65ce338e29d6771b1acaf96d01667b7db67163d1d0084977ad526c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCopyValue, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fa8553735b42f57ec2d3d64db1a81190c4b5a411b5ffbe9947658ac977482c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigCsv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4bfa5394ed5131f5ec2203874462c43ca17797585f815c83c2db69f0c8828f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigDateTimeConverter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551798ef9a6e473beae54e9dbb159e6d6c859d78fbc9ced75440ba0346dde3b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigDeleteKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8811c5361fa4ff53f424539ff55c4d7ff104250b9528e4449fb59978af6e087(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigGrok, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e83a821ce301c0df9337f716fd1594eedca34db4f40c35c203ea1355c20b19f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigListToMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec3eb2f865d0f5f5f33d20ea4ee28faee4d014e0cfdb9fc0fa7e7bef92591e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigLowerCaseString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b768c4fcbe3662cc8eed48021baec45e4a62831d445c3164b3423345b1a9f81(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigMoveKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668ca5ef0d8d13ed25e244968e8b8f387bd058e062653ed01930312c08bbe7be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseCloudfront, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2a7fb776b5e9129ef99ec7e377ebb1050b077eadaa5dc646036519edd21e1d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseJson, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b566920b897a9255f06d85dad31576a639dcf35168635931f75f6eb223aacbd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseKeyValue, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a7bfdb6e1364b1e809290c3b2e7ac6c2f8d482969e9e7f2304fdaeb7085e1c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParsePostgres, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb0193e72339390cf55b34790ddc3ffe798a5b729ea16f5478f4197beef8dbf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseRoute53, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c2ad83b5c71622e85ca635d2b97cbd8664c875fb9c07115e0308b891a8a620(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseToOcsf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87655561e40174eff6806e0a35ebf86a39690c747f8f044250e4b8b78cb2569d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseVpc, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80306cc7fc4197f90f2dd2b954ea6cc5d8ad4d76b3c0029b4806e791be420dba(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigParseWaf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658d407742f2cc736e9cffd089d67fd771f270002e11a91ac0be28e6c28894a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigRenameKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be79bf3e156255126e4956b126fd3db6db3a9d79c8281dc843069d2914c186f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSplitString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa7b0c1a78ffbaf9800cc755dddf998536aef6827e8f42bede45f19888dcdf6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSubstituteString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde505157e27f8f93a18c79005c84ac5479830fd4449f4d417fd8a50696656b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigTrimString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fd5cbfb5870055db2f920d27cf94dc1e9d09f581129a831605bc728ed9cc92(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigTypeConverter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a57bd7503c5e0f2301d6d9d058eaf79f3a4420a73d5ff42b98dab7b384bac2b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigUpperCaseString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f24b1ba716bed3f4232fc611daa3f500dcd6ea085f851ef4f82a0635d684d96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89372fadb09c69c7b1ba469132d80c3a1fb16e838a0e412f29dd3ad011d70cc5(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bf2c4405a45a88ce336441885e332c3b66801b65432301f8e5a13ac5eed178(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5edc137cba231b59905b865a6e02f4de6c71783387bcb94d9bd1aceac6d9d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8496ed59c9aed559179fad5e47e2a61dfe19706a630d8525d1037bc1d94376f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b98a837c93588c56adae17e7e839595d2859e34f70cd5fed50a849e4c282ec3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b3d25a97786689d19267826b410b2cec958932a49cd4d0c30b1476600c43d1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5a0fad3a303ecf515be76a2bb988ac81fe71bcdd993cc3d8e80c87fb8e4cf9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseCloudfront]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759b7f71cb41fa64b69a0f5506c3159b707907688a44c8b7a8853e7692934722(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79d1ff501a247d501e65a3c36d09edb934e44adf07784abe5331fcfbb4d9d3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744b68d059e5a4135d2e7f582150feb5f3117cbad91802313d6aac3024ccd100(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseCloudfront]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed3c0a59390073093d19738ed9634420f9cefb74bc96a9b6f1f36e93e39351c(
    *,
    destination: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354e96c1ea4afbf298cbe11b843e6841825aac6ec361725f9a58c609ab0110c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9446644e17a4e9c847b5de217a875f2a2853c42a8bfc6fa1cc3561f6e0aff3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e5f5a81e9e75f6738263c45e553a3ce4da65b1bd6068f96735c87423fa8daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5ca2e5b051221c4173d61c714ac0d0c0533c610fe7ec293cb1b31e6589f784(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10224f7dd9907ad903793ad7f13725d9b3f2f0b2ccffb4e19a26e39512d80c42(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cca358ce66b1fb9d53b339ae6053cce7545e6991150864e2a2ff82a0a50586(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseJson]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2231e3b5090a01fefc48f2c0f5b5431d0d3821b05d7cd141841f9957c568048(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937eca076ec7fdb14d60690e89f93d4ce203a5f46d6f896acd4840cddc2cfc76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0753f062b2f162c1f7a2584c20db861a9327a1a6e8b7dadf856f3ef097509268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61760eb679f61880f400b7ad448a767094a5c3ad8caf57e6eb7a32ca4ee7092b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseJson]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112a5338d22878ad8c018581ecc6407b4d46680f6f9d774fed625851f4a6a079(
    *,
    destination: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    key_value_delimiter: typing.Optional[builtins.str] = None,
    non_match_value: typing.Optional[builtins.str] = None,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987182d3b75c47b09ebeeb7b80ffabf111400cbd2133d8bbbf00e0ffdb00ad51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56412d9bad8f6fae440db9faffc8396e68a4ed6dcf6c01a94e416e32660bc12e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8dd1f0a91fcc23bce46fab47153db00ee7f9a68fbc86b4bf31f6a37bc5085d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8456a7d62a473d89b46516f9b49cb9e561a616c2cb32e7a72e10380af32ed0a3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2813fe25a1efbb38757a9e34ef9a3f0d01f69ad9505f3d0902de574a1ac2d24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc292b488a136e5eedb7a0ff2aeb9a7be9640977806a5a9fa46d985f54618be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseKeyValue]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fc1cebc69e41e5a9142a58e3ef9ef2e97c3934ee89f68277fa136dcbaa83a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c66644953c71c8abe9bc3abaaa8c67cbd947b32d41563bd4b39d8668f187d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6527f0e441ed12e0c47306bd83e00f4bd243569a26c70d4827ad35c9b95a985e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe0ae01ea8b41afa5bf69998f42ea6d2014333f21259b1241fbe54e507ce204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1249534ce05cc287cff4a8ff2b1c244a50a7d62a63141b768f44108f58df3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e00d274bafef85737c2186a6dcab3510939d1ae61ed3aae497320046d12df0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82c0c4bb16962938e12fea94d63b2ce82c298b11bc69f1bf18c4289552077d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c7623c988023cea45096b8a00f141f7827fd455a47bf782f4dd8fd03d0d1fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf60e2208a232e98ef0fcf7ab30447adb6ee5c7dfd928e9607693d3a79f854b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseKeyValue]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13cbb5ec0d8f72039ad17bb24e86026ea51ed9b95315d9ee4a935872e69b9ad(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2068c893871fe5b52469c1323f017025b8dbaaf6f2a159b4312c5427ce84e66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480b84b05f997b27f1ac20ba9566c0026ffe5d805f6fb2e892148bd255ae358c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0864fb6ecfc0fc45f86d208d38599cef7c9051e6ed9c3342ab777c13ed3740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19e64cfa433c2ffd9e64d851ae85b20bd23cbaabf3b4e3834750303f267a958(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945e5971c75870afe5cd9da5b4deeb31dc7cf54e64aafec584e90cd67fc23eda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a8fbfea4f21c284353985ee5037e15880af5c474095cb4a74331e940a61972(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParsePostgres]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3817669ca4483850cb3f56c2dcb8b6ee02111d35afdc33e1afcc713e56bd4ad3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31719d2b56601c6f9893e9147f815d4a4713acea7cd4e19313cfd9fef218a500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7cf1d1044f8c9d9c5584df245c9687925b3473638340a395f9380df91ee0e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParsePostgres]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8826743120f73e580ed2c6995c15da40997edeb3bb3a408a017c4b66c419233(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0861f863dfa36ae87da3e83a48fd21ee6d11a13d12e9a8ad30ee5adfc13f2c4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2585344cf07dfd4fdb712b1caf1f8c3df507f414bb9364898046b0ae90da9cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5d3535d9b0fa7dfd9056ff5f624badf326780ff9d0b9fe117f08e73d200dfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3da1557376cfbbe03125e53ce214937d015ecf88e1b08917fc73fa08531bebf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698ad9f47d8e05d5e17a55432127248835a4081c179d2127c6d250bc47755b11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43aac3e4de26235997c1d26e114cb9658b9fb784d6f30125a474d3db4564744(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseRoute53]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4dc3d14f094a399ece17144777cff82f16edc2e2be6797545dc296cf12ae0ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd07f152f16eb9531f30567e98080184510958e28d13603ceb351891f0aa271b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40dbef195ad73bfb8713a46bb9577a8ad859290c0c8502bb380c70ff0359b813(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseRoute53]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717a2ebb85f0c1b857b7db1f443b27aa0b035da072408ccc18c5eccce9a18026(
    *,
    event_source: builtins.str,
    ocsf_version: builtins.str,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c048f17819d3e05408102ede5075cda4f59ee9a609a05113d36cf3ef6439fd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef58375c375ae15b0c6401d550cea0a368e6b4c5789f1ac13b4bf8cb579b92ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5217c8510927d9d793eaa4e084670f4373e93d5b20b6bf45bb8c1aad2eda87ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f34c41ea4e9af0c983a1dddb9aabf8a19cf866d03c5f8ba5174847dac1f33d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2725307d8c13021626ce4ec925cb04ce6fb7396da02a8c8428fbeafc1161b25b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff764de85ade8c3c486439f884913b0179371fb57237442d385957fefb692d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseToOcsf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d3dafa678248591cc4a88c79a0be4ab2e7469d90a63b62c0627b786df7a61b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b85ed77ba3c8f00f5661f97d7cd6c7a07f2295898074f2259b5116ff36896e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab8d05a2372b0738680b9c609cbc34f47ac231d1c4631e2fcf7839a36f0a4e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baffc2808326c7118fbc855024bb4b700999ee87fbbedd9891813143379570f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06c16ecbfb8f05c49eb547124131d3bf2c986784314b5a9d1b6f2d519eaefbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseToOcsf]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54aa190504460e0a727db9bbcbe8e1f2795d3521ea0080481ed3926bdf193fee(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e35e11993662440c5632b7a7f880d6fc70e65e2006ab5f3b5a2fe42d1de869f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c921bef35032109a348f7ba1b59e322a51b67266001b43df55a925d83d82db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebe209f3002d5db59acc13301806d76deedf88f06f4c5550355ed5ff2dd846b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d205c7987f5330df96b2cfc665305c765ab914799c44b5ff84402dd0cce71649(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24592abb1c1fac295e412884f7b19cb77b4e62f57dbc247f113a6a827d2fb03e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a1c2098cb4ac41b1d56d949361db54cb129d203f9d3caa14fbf4ed8ef4d268(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseVpc]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67dd7a957b3f65e07a2ce507ddfcc982320a4bddd840626c29abd9ea20db271(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d51c1a13b59a5747d09687442d82bbbcd9fe66eb25b6441df90b4a9f0354c50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46e05e0ac94fdf65686414d54351cd0fe7cf6b9982bd40fc4a0f1945fe2c0df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseVpc]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e11ef264e4dd2383233f4ee65e6447766faf5bc1e5f314ebc599c0a99d14c3(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2163e3a66ff2835b2799ff0ab30796900a0f87612370aa6edb7368ad984d0e88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d63ee36725a97e41102bd006c7da381a359b9352401c45b4c8578ad6e470e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0603e9eae98069ed4e43c21e255a2878d2a4a5fa15e036ef4efdd573e361a3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48801d1e076171b99d6a95037656b95f643cc052d04283ea0a9289ea17b8829a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dffd65801444e348dddb7f0b5e2925c65be09429b82cdaca186d5a6033cb190(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc5c0fc612f70d92a855bfe4ad5d33bfa227287347009d67cf02c2c206348d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigParseWaf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6193720a904a9b8a4e238beda6e41a03528891eacd475f590e1a2526747f687c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d133942f9ceb782bb60f6f7c21714069fdde65f03260f4ef784a149562145ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f004b77d165c8bc6cc8e8e97b4ab2caee7e2a145f487d91db6d025fe3bd1d094(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigParseWaf]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d8d02fd1e3fc4945ce4f97e4c845db3808d9fb4f8098397e95b5a983cf5f5c(
    *,
    entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigRenameKeysEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1547e7b9a9aa7c005a44b729306eb640f9f2dbf2c3f056db958180e7c848f565(
    *,
    key: builtins.str,
    rename_to: builtins.str,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3c25f6955106c2a9f406c65453aef3166a96eb1e6af5705a17d0b5ffaeec9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c794e14a03f0133d3365410272f8a8e0fa3347194a5d08d16d8ea89a782412fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34aa4a0aa5fb5740cfe54f1b34797dbd101888cff0846b651d45687ae4dfa286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a5308dd5eb24f7922b35e529d2347fb50b3d31da74e05d1a8904392253c099(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26105730137d8155eb632853ac2a36ed2c495a8ebd177a6682e951b79b833d2e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2aed413ff2428599084a3edebcc23fe455d289da09017e68b9c65b1668c2b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeysEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3152716d23c7ef748a48b81f5e6b6424d45d83aadabf0e6afca685b97d9ec51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0a62b6273ba46df95adee0c822e9b1725c29f34fc7a17393c0d3a7b2bc8a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c967dcbb1a506ca3fa41245efb962f48a688ac18cb3f55e3354fedd291fbe0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ce93369e9d0f03f780eda563702619e05d5e70ce9f525ecdf12edd96a76c06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3ebbbe2df958d5f929782a752016be710294807cd90fee0492b4d6300d8e65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeysEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5ca9ca905ae0261bd27a14c87e424fe8dbb8df8718e46d9b86f5517262fa76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f732f670acf15345446ada1465ebf2edd5e783adf2137a25630c0cb6a85e8a8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0520e1b9ad2d6a3836c7aacfa342c9098cd252aac03d92dcd897da796ef91f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb2a90a459af48b7f771f5f9bae2c3e928749edd8ab9d96f7d2ed1219feda7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6425ed33b3fe844545fe71f8852f09969c13a74b632048ef041bfb67116976(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b296fadc2a8185012713eda45ee430f1291e692bee46ef6d2de87633743269ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigRenameKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28b327e60e2540dcd6f72f8a011caca97064e40fe92a7b138febdb754dbc68a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74266748e939b05c082e1fa780a341af4d299ff948f7528b18fd6541798addd0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigRenameKeysEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09b5b563c364ffe32646e7ab37572eaf7be521b6492f64f9906b1bed500c5c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigRenameKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af024799e4eefb48d6775b2100f8050015ff6f25ad6751d5c165c02b5e3aa409(
    *,
    entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSplitStringEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79078d47b3dd800cbb13ebc29841899995e3a0f9066c27d2fd55d2d088c31d5(
    *,
    delimiter: builtins.str,
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28da1ed1a72772b05bdcd9844f7e4da10905851faaa6a85333fee08824aa6ae0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bf2af26fe77d7e33ac299bc14b820e1b5fb1f3b09a6f18c26e7407513771c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5365c7f9c60240b2eeb4553d196f60ed4c224584b51908774288029833ddd99e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9666bbe866b722753131e09b341ba069ce1163927270bc8cc3d497ae4716d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26663a93aea451b1032aa2cf2b82c8cfe382d6becd5097375ffdd27be1f21909(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643a244557af43f2747870db2ed21d8323d906b36a978d2e8a769ecbede37f9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitStringEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aadd92bb464478a87edac05564b181579b415ee50e6cb947139bfd4306ead5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee1666ef4249707ad2e74d6eda38a089a329d4e2290958b3ba67ef9e44c44f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b78459ee096e20170825b0fe965575466151152c4e3e9e606115c271cbcb44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496b08f53fa353654edc30a870b87a8c1bf4db0ad36597eb532f9f5d061d006d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitStringEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a640f6bf1f9b122588ac192831676f8fb25c4600bf55fbcc73b2cf454df159ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e492e611422fd5dc989f45b30e11bcb2edfe94b2d90e3b14dc47e2865f111097(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a00d05bfb4714b6ecdb52b6b079c3eee695f0ae83c20c14993f5ef0973083f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0f6142e1726e1376e8d90fbf9caea0a5fa008838b5c0abf42c9235f3135349(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76aec3e5afda30908714ac83ca8510a25edda91b7dc717dbbef3b108e068fd4f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069ef21a8f93b5921072914f9049f776eaf72875695ad5ffc3c66081266086a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSplitString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db654b6f114932b2d21f7cb9f321a7c8ba8b205cdd82287edf39fd42ebbc17e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d445a2f17753f80f641a6406e3fbf449b28086284e4ef12975fd60a5d71d719(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSplitStringEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6506f3386c74d76395505a9148de903068eb81eaaf8c1651ccd345bed729d5df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSplitString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3c138d1d227864efd217f28bddfb4c7435a7a438b634f35299b86283080e67(
    *,
    entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639c1bd7dd405767b591429aa2855db88e161d5cb48a807da7660646ae350b35(
    *,
    from_: builtins.str,
    source: builtins.str,
    to: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2e6597a7098dc8e8865a312fda4a679ebc39c7b761041ba053d6e798a72b01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfce4c8b7cbd9a0b2cd9ba486991190a38581845570c54c275ce5bb99e34e344(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2684ad3c71e53f9874c1b35da65e767ddb1cca386ed805def1e1c8c5992f7a4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b43af111e14670b94a24095ebba9aac32b907f0ad90a9b968f9e3b94f6a6f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4377aeb58802c568283e87be268711582df3cb6cfb84d2ae8590b30e6a8a0d6d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1839ce7577ed032db655bc0ccaab884fd135eef56a740b09f2fba5fffda1ac6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8c4598df3d82d06b153ebf1f865013464225f6b89ada5c700169d8f04086a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9915248aae7e1a943c8d54d0252064046c09e537e9c44f9066c2be3adb597ab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9383674cd5d7c54e97581544ad237cd73d9a97665c0eacb3e52ff93d003ff5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9239162eacf23c6bad9cc6de2c55fb5ed496070bf2e8a4b5572eddb6f83d5c5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97375fb7c3343b0fa6b291a1677c50f58d5bdc6b93bb69861d15ca6673a9b2a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteStringEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c998ccf814f160ec60384038c37926de73425704670bfad77bf2428a14f793e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39838b3c2fce972ef9f67879c157013222f8b1df3b980b1dab8ebce6b45dd52(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57da22c36ef8ccd5fca02b5626d55d06feb96127a366d1741341e029093d517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc81eba8139b18f3bd00774eebc1d722ad46d23705403761003dcb67b10fb1c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e048dbc0ca60d6ddca3cd8c432f8c25828ef9bf6e6bcd41393eecd8fcd48a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0de34008a43eba87afb6d1bef5b1fa3051cf78eab8e814740fb0f403439477c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigSubstituteString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08054d0b5af2455e9e7f873c5f5aa84556bbf3435a23de2f79169d39b1027f36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c574db98d976aad9dd230fdc9af09c488441546085c5d1405d02b44a0898569f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigSubstituteStringEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0999f5603891155b145b087037d44e8f190820521534442605df58fb6859158a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigSubstituteString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca44f1deacf6d189dcdc80735e3644791a9e1c29ee07117a6ac99aafab724a61(
    *,
    with_keys: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381d2391ab62d12366376f7c38b2cc8b25a6b909eeff19067c9c14015e9ada78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf141e8ab03677e87be90de7c6335fcf021c773a5de25ca6272f124d3d64a1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0418928b6165b55cd48b0cb736bdd21c4350d6144476ae83e4d9496fb465be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407cc7d8205b1e821336884d551f7368ccc89d9a9a37a83c5e0561d66d042e99(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262e54c7d7f0b810ebf2800335df13a005ae52799a7893428f3b0ba6ca75c68a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c94ca14846fc501d4dbe349ef50c89ae359ea9b59898a120004816a60644f94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTrimString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010521b3af75826c8e9d9464ea9682bbc4056238505558a6ca6e6e645294d029(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6468b46ccda524c31077f0684321c73436975361f71e018164738fd00d696dde(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3464e40d787fb06b85af911d5562979a38252924c7f3f843f14d092098a887df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTrimString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cda410fa5602d4752b7eed4975bf881a29d0912dd6ecc704bf54c8553930a5(
    *,
    entry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigTypeConverterEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281d4d72b4d089d4d03a699597cb50cd07da2fa17e391364af79c2f81c4427eb(
    *,
    key: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d4e35415b2cd03428a0a8d61d071e87ad17621d97068ea9367a348df4c5b2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67da1a099734770a73ab728b7d5b95c986db9e520734aa9f15deddf1e41f8815(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a43d7a162b0a42ba381b7284a25ea9b71715c0ed18337e24d69a449b64108e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1193bed62f1a663d8665bb098066836bd03e6db1e20e76d61294c58bc77063c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda61d4cf9295bf7069cd9f2c35f4d0d761edebaf1da5afafa81f45498960009(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc24dea59be5d61cde974a0f2c30b777a03c24f04f57e305db6c6799e750d248(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverterEntry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b379c8223a77ba9163b2b614ee8d166c1902ccbdfc5e18f0afa9227c473fe6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a708d4583125cd87101242c1f6559b60abfe086d5478b89510a43312d30ab38f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759d903f68c8cf0700ea98f3c6e7f5c7f331d2422d2e16e355994744385dde88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4331ef2ee71c87c3a74686768944c6a753680c778083180cad6a1fe687f89cfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverterEntry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a1d1efc7dd06c80e1112b1b084a2cf0cdbdf8d07e1016bb46c46c312774274(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fbd7f3dbf5ec67e8fa82513e22d2fae12cfff7bb033463f38875f9fbd358a3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c38806dc97a02e7fe79c6679d9792f60b76c4a3490bf35ce487d188869bea34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00862ee75d8c56f905d4583c57063cb99529d3bde635e05fc1a3f090b5c0884(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf1e2235ab28e9a2021ead2d7edeed3143590d44a75dc05cf5335ccc796207c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db30f7b7395d89304163d0f4fdcc81d49b6117eafeb268e714b7e4164e89004(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigTypeConverter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270309791485cde47f986d441ebd2bda8aa7f9bbced3ee27b3111544eb506813(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0339a6b57149fccad1dea2f83e34de35bd5aa1acf14a92e3d2d4148a7461c486(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchLogTransformerTransformerConfigTypeConverterEntry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb27b94491b4a741da09b6724f14f14f92148ea857c7e3252a45d5ce554cf1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigTypeConverter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e7077f9bd1654858a7ac90909f1ccd2486187e2491b4bfe510656b6a84a13e(
    *,
    with_keys: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615a5303a74352aa3ed7ba6940c724c68313d2535ead07d92a581e334b2c5a6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f35406148957aee01371a666fae1ae769543336628ad4c88882911134a3d087(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d863afa889628a4b3055736588c5a4c18b8fba49b92b2a7e70d8bcf0dd9f99b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2005513c5f1c77a00e9ea13bee2007ea9b99886db296171b7a46dbc8d915a443(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc114d6c21e6073bcd3fb450c1f380b43f41e94275d5c1cc0d74dcd92f35977(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05aad38ca82de8534de087e64ebd9ada2430dbd0c224480e9d04d6d847a737a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchLogTransformerTransformerConfigUpperCaseString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a478afdc6da559b734ca5049749fe8a3d336ff62ca372de2aab7691be695aba7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31713275edf65168355d6345d4077dac1f44c2f99139db8e0f0e8fa8865f17ae(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c17e9fdfb6557895514c282054c5c964061c51b538373729849ab1b9213b220(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchLogTransformerTransformerConfigUpperCaseString]],
) -> None:
    """Type checking stubs"""
    pass
