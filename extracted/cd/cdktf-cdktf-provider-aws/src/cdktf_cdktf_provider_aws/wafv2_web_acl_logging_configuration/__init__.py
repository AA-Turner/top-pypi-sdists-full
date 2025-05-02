r'''
# `aws_wafv2_web_acl_logging_configuration`

Refer to the Terraform Registry for docs: [`aws_wafv2_web_acl_logging_configuration`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration).
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


class Wafv2WebAclLoggingConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration aws_wafv2_web_acl_logging_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        log_destination_configs: typing.Sequence[builtins.str],
        resource_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        logging_filter: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration aws_wafv2_web_acl_logging_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param log_destination_configs: AWS Kinesis Firehose Delivery Stream ARNs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#log_destination_configs Wafv2WebAclLoggingConfiguration#log_destination_configs}
        :param resource_arn: AWS WebACL ARN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#resource_arn Wafv2WebAclLoggingConfiguration#resource_arn}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#id Wafv2WebAclLoggingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_filter: logging_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#logging_filter Wafv2WebAclLoggingConfiguration#logging_filter}
        :param redacted_fields: redacted_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#redacted_fields Wafv2WebAclLoggingConfiguration#redacted_fields}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49f9cd502c86be5b2aa415a67313f4d5475b9bb50e1db8a0c671e3a85a6674d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Wafv2WebAclLoggingConfigurationConfig(
            log_destination_configs=log_destination_configs,
            resource_arn=resource_arn,
            id=id,
            logging_filter=logging_filter,
            redacted_fields=redacted_fields,
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
        '''Generates CDKTF code for importing a Wafv2WebAclLoggingConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Wafv2WebAclLoggingConfiguration to import.
        :param import_from_id: The id of the existing Wafv2WebAclLoggingConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Wafv2WebAclLoggingConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6c1078c3bfc294ad0c88bc22d3bd151b7d46c1760c9d7be80dea809aa536eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLoggingFilter")
    def put_logging_filter(
        self,
        *,
        default_behavior: builtins.str,
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param default_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#default_behavior Wafv2WebAclLoggingConfiguration#default_behavior}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#filter Wafv2WebAclLoggingConfiguration#filter}
        '''
        value = Wafv2WebAclLoggingConfigurationLoggingFilter(
            default_behavior=default_behavior, filter=filter
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingFilter", [value]))

    @jsii.member(jsii_name="putRedactedFields")
    def put_redacted_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7cfaa94f7510d5e66bedbe71840095113c33d6f33b61d6dbbc37813aa11baa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedactedFields", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingFilter")
    def reset_logging_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingFilter", []))

    @jsii.member(jsii_name="resetRedactedFields")
    def reset_redacted_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedactedFields", []))

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
    @jsii.member(jsii_name="loggingFilter")
    def logging_filter(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference", jsii.get(self, "loggingFilter"))

    @builtins.property
    @jsii.member(jsii_name="redactedFields")
    def redacted_fields(self) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsList":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsList", jsii.get(self, "redactedFields"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationConfigsInput")
    def log_destination_configs_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logDestinationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingFilterInput")
    def logging_filter_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"], jsii.get(self, "loggingFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="redactedFieldsInput")
    def redacted_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]], jsii.get(self, "redactedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef349584739cd5a58568773c325d643661804fd3ed449ded7a8ae34b297ac751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logDestinationConfigs")
    def log_destination_configs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logDestinationConfigs"))

    @log_destination_configs.setter
    def log_destination_configs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09bb3e563c77b9e91d33063c940255670e15d8ae99264536f140d7327f203cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDestinationConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65a07d60b41b57d7c3d3beea9656f40bc34aae4246587ce0b870c3a4ff9ac3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "log_destination_configs": "logDestinationConfigs",
        "resource_arn": "resourceArn",
        "id": "id",
        "logging_filter": "loggingFilter",
        "redacted_fields": "redactedFields",
    },
)
class Wafv2WebAclLoggingConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        log_destination_configs: typing.Sequence[builtins.str],
        resource_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        logging_filter: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param log_destination_configs: AWS Kinesis Firehose Delivery Stream ARNs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#log_destination_configs Wafv2WebAclLoggingConfiguration#log_destination_configs}
        :param resource_arn: AWS WebACL ARN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#resource_arn Wafv2WebAclLoggingConfiguration#resource_arn}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#id Wafv2WebAclLoggingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_filter: logging_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#logging_filter Wafv2WebAclLoggingConfiguration#logging_filter}
        :param redacted_fields: redacted_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#redacted_fields Wafv2WebAclLoggingConfiguration#redacted_fields}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(logging_filter, dict):
            logging_filter = Wafv2WebAclLoggingConfigurationLoggingFilter(**logging_filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3073abd3a4bc06e779bcde29b3be5d1212331dee56d0465c9e0048088808ad6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument log_destination_configs", value=log_destination_configs, expected_type=type_hints["log_destination_configs"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_filter", value=logging_filter, expected_type=type_hints["logging_filter"])
            check_type(argname="argument redacted_fields", value=redacted_fields, expected_type=type_hints["redacted_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_destination_configs": log_destination_configs,
            "resource_arn": resource_arn,
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
        if logging_filter is not None:
            self._values["logging_filter"] = logging_filter
        if redacted_fields is not None:
            self._values["redacted_fields"] = redacted_fields

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
    def log_destination_configs(self) -> typing.List[builtins.str]:
        '''AWS Kinesis Firehose Delivery Stream ARNs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#log_destination_configs Wafv2WebAclLoggingConfiguration#log_destination_configs}
        '''
        result = self._values.get("log_destination_configs")
        assert result is not None, "Required property 'log_destination_configs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''AWS WebACL ARN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#resource_arn Wafv2WebAclLoggingConfiguration#resource_arn}
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#id Wafv2WebAclLoggingConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_filter(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"]:
        '''logging_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#logging_filter Wafv2WebAclLoggingConfiguration#logging_filter}
        '''
        result = self._values.get("logging_filter")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"], result)

    @builtins.property
    def redacted_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]]:
        '''redacted_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#redacted_fields Wafv2WebAclLoggingConfiguration#redacted_fields}
        '''
        result = self._values.get("redacted_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilter",
    jsii_struct_bases=[],
    name_mapping={"default_behavior": "defaultBehavior", "filter": "filter"},
)
class Wafv2WebAclLoggingConfigurationLoggingFilter:
    def __init__(
        self,
        *,
        default_behavior: builtins.str,
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param default_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#default_behavior Wafv2WebAclLoggingConfiguration#default_behavior}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#filter Wafv2WebAclLoggingConfiguration#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8371ff235ca4c0c1570a7723fd03e9b163bfc5bfef6a51e758855ec1f4992d9)
            check_type(argname="argument default_behavior", value=default_behavior, expected_type=type_hints["default_behavior"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_behavior": default_behavior,
            "filter": filter,
        }

    @builtins.property
    def default_behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#default_behavior Wafv2WebAclLoggingConfiguration#default_behavior}.'''
        result = self._values.get("default_behavior")
        assert result is not None, "Required property 'default_behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilter"]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#filter Wafv2WebAclLoggingConfiguration#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilter"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilter",
    jsii_struct_bases=[],
    name_mapping={
        "behavior": "behavior",
        "condition": "condition",
        "requirement": "requirement",
    },
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilter:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition", typing.Dict[builtins.str, typing.Any]]]],
        requirement: builtins.str,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#behavior Wafv2WebAclLoggingConfiguration#behavior}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#condition Wafv2WebAclLoggingConfiguration#condition}
        :param requirement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#requirement Wafv2WebAclLoggingConfiguration#requirement}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9dc151b6122156add217128c153406165f91dcac04c0245318c9d2a0da0540)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument requirement", value=requirement, expected_type=type_hints["requirement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
            "condition": condition,
            "requirement": requirement,
        }

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#behavior Wafv2WebAclLoggingConfiguration#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition"]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#condition Wafv2WebAclLoggingConfiguration#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition"]], result)

    @builtins.property
    def requirement(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#requirement Wafv2WebAclLoggingConfiguration#requirement}.'''
        result = self._values.get("requirement")
        assert result is not None, "Required property 'requirement' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition",
    jsii_struct_bases=[],
    name_mapping={
        "action_condition": "actionCondition",
        "label_name_condition": "labelNameCondition",
    },
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition:
    def __init__(
        self,
        *,
        action_condition: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        label_name_condition: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action_condition: action_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#action_condition Wafv2WebAclLoggingConfiguration#action_condition}
        :param label_name_condition: label_name_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#label_name_condition Wafv2WebAclLoggingConfiguration#label_name_condition}
        '''
        if isinstance(action_condition, dict):
            action_condition = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition(**action_condition)
        if isinstance(label_name_condition, dict):
            label_name_condition = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition(**label_name_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4e71826fd28199fc221aaf17a28addefda06485ac0b9f089de3d43344c94d1)
            check_type(argname="argument action_condition", value=action_condition, expected_type=type_hints["action_condition"])
            check_type(argname="argument label_name_condition", value=label_name_condition, expected_type=type_hints["label_name_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_condition is not None:
            self._values["action_condition"] = action_condition
        if label_name_condition is not None:
            self._values["label_name_condition"] = label_name_condition

    @builtins.property
    def action_condition(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition"]:
        '''action_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#action_condition Wafv2WebAclLoggingConfiguration#action_condition}
        '''
        result = self._values.get("action_condition")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition"], result)

    @builtins.property
    def label_name_condition(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition"]:
        '''label_name_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#label_name_condition Wafv2WebAclLoggingConfiguration#label_name_condition}
        '''
        result = self._values.get("label_name_condition")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition",
    jsii_struct_bases=[],
    name_mapping={"action": "action"},
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition:
    def __init__(self, *, action: builtins.str) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#action Wafv2WebAclLoggingConfiguration#action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07fffff3cda6ce7b67144ae5c09b341eea2b95202b05e36aa47e95e07a1ea7ca)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#action Wafv2WebAclLoggingConfiguration#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2464420521d4df1dff3c910f7f5161e3c08059ceacb8a9d12886b6368f4185d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__526904af0411cdd6be713011c2a727f8f69c4b672ca45d586fe00af5e71e715a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146e182e846e0e5c267876f2846ddf2d8816291c0fa17aaf336709cb3e38bce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition",
    jsii_struct_bases=[],
    name_mapping={"label_name": "labelName"},
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition:
    def __init__(self, *, label_name: builtins.str) -> None:
        '''
        :param label_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#label_name Wafv2WebAclLoggingConfiguration#label_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf087a06a0171cc210ad0c713c85daeb00c0e986f54453b290f503a2563151b)
            check_type(argname="argument label_name", value=label_name, expected_type=type_hints["label_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label_name": label_name,
        }

    @builtins.property
    def label_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#label_name Wafv2WebAclLoggingConfiguration#label_name}.'''
        result = self._values.get("label_name")
        assert result is not None, "Required property 'label_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__574e2817f73c5f2fc03b2be8e8f70042b871de4ffc920a507f4314fa6c32166c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="labelNameInput")
    def label_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelName")
    def label_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelName"))

    @label_name.setter
    def label_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b929dfefa42803303db10b3e76af12e00069e25bd197cbb5ec2fab1ec664ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7176ef749009f43ef3d23528bfd4f840258703e8480e74167cc13244d2e373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e107fbfcd274f42d05d411c3a287fee02679944b034bb045d773b060e44a9e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90841796c0359c074dffbf712e430c9699f41662fbb0d8c6fda26e7b77522841)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d5067204c3d7bae4c273f7bcb2afd6b1eaacb942dd58fc5a30ce0be910d00e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ce9f63b05df64727ddb71c9ad347f8aeba3c956d9fbafc2f8904a8f26650103)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b7dbc5f31633511f09d0f5488544945b51d6e3a8dc05265fa2214bf6cad1385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee85b189f592fd19380f5a97bd7e65c7c3bb07b25d772cd76cd4ea30b6e9859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ba205ecfc8ad89e4341ac79b7e156d7037877f7cf7f9ef5a841d2985b9809c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActionCondition")
    def put_action_condition(self, *, action: builtins.str) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#action Wafv2WebAclLoggingConfiguration#action}.
        '''
        value = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition(
            action=action
        )

        return typing.cast(None, jsii.invoke(self, "putActionCondition", [value]))

    @jsii.member(jsii_name="putLabelNameCondition")
    def put_label_name_condition(self, *, label_name: builtins.str) -> None:
        '''
        :param label_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#label_name Wafv2WebAclLoggingConfiguration#label_name}.
        '''
        value = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition(
            label_name=label_name
        )

        return typing.cast(None, jsii.invoke(self, "putLabelNameCondition", [value]))

    @jsii.member(jsii_name="resetActionCondition")
    def reset_action_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionCondition", []))

    @jsii.member(jsii_name="resetLabelNameCondition")
    def reset_label_name_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelNameCondition", []))

    @builtins.property
    @jsii.member(jsii_name="actionCondition")
    def action_condition(
        self,
    ) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference, jsii.get(self, "actionCondition"))

    @builtins.property
    @jsii.member(jsii_name="labelNameCondition")
    def label_name_condition(
        self,
    ) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference, jsii.get(self, "labelNameCondition"))

    @builtins.property
    @jsii.member(jsii_name="actionConditionInput")
    def action_condition_input(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition], jsii.get(self, "actionConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="labelNameConditionInput")
    def label_name_condition_input(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition], jsii.get(self, "labelNameConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bc2f22b5668d1e946a8fe5fe25568562561db592207e82f056c0ddec54e53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30b7952b2a83f57c429a763629ff6a6c5bc945074a26ff75516856ef7131e101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a206455172d04d60ce1e06c8ec47a07867410cb6996dc5b24fb47ad6c71f9dd6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f13f9db612cff7eb86bd9cbe93f2b2b74e88c8349ce920504b4f6173e0384d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf7211592ad32abab1ff25b8cd50db91ea8cd32facc67d8bffdf713e95be5ef9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__103f4d03609d147de06ab87bd787bd6761ee5e6fd96b6af422532753bc5a8cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea56621a09218e12d4bee554c351c8029bd8726af55b92e97e960978244ab696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27106464359a09a30ef6021f777a3fd4830df107f6ed2e1ff52b5947ee7e5722)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8688b61247ee44b77969a5fae9c92f0b613de9ef4730114fc3c4e572905276aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requirementInput")
    def requirement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec9446a8c0ca93f7fdeb0912532ced86b540a274385c435d2c915598919b5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirement")
    def requirement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requirement"))

    @requirement.setter
    def requirement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c892af3b73e43a467cf06ec923ebd04f03ee476616006aa0dd4803e65fb7ff1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463a11ea31b9b75cea8c933bf4fb6ef4a2d7b4e72f1693b571966728c93831de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__705be604e0573d7d4c3bec835d474e3544738188f0a60758c6d5f2de690af153)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4cec8cf7a42bc62fef2643941b628b012719a6cad1d3e375baf26b72a64ac98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterList:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="defaultBehaviorInput")
    def default_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBehavior")
    def default_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBehavior"))

    @default_behavior.setter
    def default_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5276ddecce71067cf279e6598843fd3df47ec1debe76880040ee8a2a2edf5b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b2095bf0b9e1401441cfd80b57618d09251b47e94d4655f892e5aa84f2e729)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFields",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "query_string": "queryString",
        "single_header": "singleHeader",
        "uri_path": "uriPath",
    },
)
class Wafv2WebAclLoggingConfigurationRedactedFields:
    def __init__(
        self,
        *,
        method: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsMethod", typing.Dict[builtins.str, typing.Any]]] = None,
        query_string: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString", typing.Dict[builtins.str, typing.Any]]] = None,
        single_header: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        uri_path: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param method: method block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#method Wafv2WebAclLoggingConfiguration#method}
        :param query_string: query_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#query_string Wafv2WebAclLoggingConfiguration#query_string}
        :param single_header: single_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#single_header Wafv2WebAclLoggingConfiguration#single_header}
        :param uri_path: uri_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#uri_path Wafv2WebAclLoggingConfiguration#uri_path}
        '''
        if isinstance(method, dict):
            method = Wafv2WebAclLoggingConfigurationRedactedFieldsMethod(**method)
        if isinstance(query_string, dict):
            query_string = Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString(**query_string)
        if isinstance(single_header, dict):
            single_header = Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader(**single_header)
        if isinstance(uri_path, dict):
            uri_path = Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath(**uri_path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b725d49020edcd631da2a28aadce944b2fcc1433d07c5629d8aa3ed87ac4e5)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument single_header", value=single_header, expected_type=type_hints["single_header"])
            check_type(argname="argument uri_path", value=uri_path, expected_type=type_hints["uri_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if query_string is not None:
            self._values["query_string"] = query_string
        if single_header is not None:
            self._values["single_header"] = single_header
        if uri_path is not None:
            self._values["uri_path"] = uri_path

    @builtins.property
    def method(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsMethod"]:
        '''method block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#method Wafv2WebAclLoggingConfiguration#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsMethod"], result)

    @builtins.property
    def query_string(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"]:
        '''query_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#query_string Wafv2WebAclLoggingConfiguration#query_string}
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"], result)

    @builtins.property
    def single_header(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"]:
        '''single_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#single_header Wafv2WebAclLoggingConfiguration#single_header}
        '''
        result = self._values.get("single_header")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"], result)

    @builtins.property
    def uri_path(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"]:
        '''uri_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#uri_path Wafv2WebAclLoggingConfiguration#uri_path}
        '''
        result = self._values.get("uri_path")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cdf35c910b97c9482680cd644ff8c499d920a569dd9628df6839c9d20a83ebb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64a936138200dc40ff2d4c22c6168d71b9765722dfade73be4954ffee792eb0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0b325f2d400a7ec408fbccf4445395ecbf8f15841a594dc6a5b8435a4cc5c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea70ae3ada4fe3383769f74441c4540c8db4cbfba9155d85ca396f0b3e4b10a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67dd294affe90760265b3dece42b71f6cb93e90f11bcc4cd40addb7fdc964ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb205e54cde5b7c19306ba4479a40c1adb6854e1ed77a58b2b9d1f01d7022a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsMethod",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsMethod:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf10955946c13faf1869a9b85bc0efba4dc471407ca1f646af500f73087cd83e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af4a39dbd4f57b8adad57dd384ef1e48e53bce7547b1f4436425dd6032eaf7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c93e4f3134947ebe50244708c1029208299a47ed9c6467911c578c4676777b9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethod")
    def put_method(self) -> None:
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsMethod()

        return typing.cast(None, jsii.invoke(self, "putMethod", [value]))

    @jsii.member(jsii_name="putQueryString")
    def put_query_string(self) -> None:
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString()

        return typing.cast(None, jsii.invoke(self, "putQueryString", [value]))

    @jsii.member(jsii_name="putSingleHeader")
    def put_single_header(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#name Wafv2WebAclLoggingConfiguration#name}.
        '''
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader(name=name)

        return typing.cast(None, jsii.invoke(self, "putSingleHeader", [value]))

    @jsii.member(jsii_name="putUriPath")
    def put_uri_path(self) -> None:
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath()

        return typing.cast(None, jsii.invoke(self, "putUriPath", [value]))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @jsii.member(jsii_name="resetSingleHeader")
    def reset_single_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleHeader", []))

    @jsii.member(jsii_name="resetUriPath")
    def reset_uri_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUriPath", []))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(
        self,
    ) -> Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference:
        return typing.cast(Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference, jsii.get(self, "method"))

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference", jsii.get(self, "queryString"))

    @builtins.property
    @jsii.member(jsii_name="singleHeader")
    def single_header(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference", jsii.get(self, "singleHeader"))

    @builtins.property
    @jsii.member(jsii_name="uriPath")
    def uri_path(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference", jsii.get(self, "uriPath"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="singleHeaderInput")
    def single_header_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"], jsii.get(self, "singleHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="uriPathInput")
    def uri_path_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"], jsii.get(self, "uriPathInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d48b6a52d8d67e0face87ad7ef1e8d9debd3cd42002810e3c68b3d807b069fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d27047c272ce9a1ade90129655e442e900288b4bf45d0717d09811a4083d378e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c87f6e9a82508e3c42424345100df4da900f79c4b72b0cd999f53cbeda84f1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#name Wafv2WebAclLoggingConfiguration#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00469d9ac0bad062d5d1c2721825afb9073d35e687ea01c47f4777a9fe00aca7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/wafv2_web_acl_logging_configuration#name Wafv2WebAclLoggingConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b84248aabe5a3b1fef0a364d2afce1a82f05a2eea25eb0eeb68dd0fa4f3691f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__bbf23c6df135e70cf8233551ed6a9ed8b456252dc7f32f0a42ab72b48685b1fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96ee4afb7f1fba5f43180b05050f96d25dd2d777a4987b2cf5bd7059fa04a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e93e2fddba7132b00078d81d596ee7bf43b19d4725d8edcb6a54e940cde5e824)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c92367ec578016819d24da9f0782d40fe7f0fd0bdac36d6d4cf9c9f94d218b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Wafv2WebAclLoggingConfiguration",
    "Wafv2WebAclLoggingConfigurationConfig",
    "Wafv2WebAclLoggingConfigurationLoggingFilter",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilter",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterList",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFields",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsList",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsMethod",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference",
]

publication.publish()

def _typecheckingstub__b49f9cd502c86be5b2aa415a67313f4d5475b9bb50e1db8a0c671e3a85a6674d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    log_destination_configs: typing.Sequence[builtins.str],
    resource_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    logging_filter: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__2e6c1078c3bfc294ad0c88bc22d3bd151b7d46c1760c9d7be80dea809aa536eb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7cfaa94f7510d5e66bedbe71840095113c33d6f33b61d6dbbc37813aa11baa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef349584739cd5a58568773c325d643661804fd3ed449ded7a8ae34b297ac751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09bb3e563c77b9e91d33063c940255670e15d8ae99264536f140d7327f203cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65a07d60b41b57d7c3d3beea9656f40bc34aae4246587ce0b870c3a4ff9ac3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3073abd3a4bc06e779bcde29b3be5d1212331dee56d0465c9e0048088808ad6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_destination_configs: typing.Sequence[builtins.str],
    resource_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    logging_filter: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8371ff235ca4c0c1570a7723fd03e9b163bfc5bfef6a51e758855ec1f4992d9(
    *,
    default_behavior: builtins.str,
    filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9dc151b6122156add217128c153406165f91dcac04c0245318c9d2a0da0540(
    *,
    behavior: builtins.str,
    condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition, typing.Dict[builtins.str, typing.Any]]]],
    requirement: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4e71826fd28199fc221aaf17a28addefda06485ac0b9f089de3d43344c94d1(
    *,
    action_condition: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    label_name_condition: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fffff3cda6ce7b67144ae5c09b341eea2b95202b05e36aa47e95e07a1ea7ca(
    *,
    action: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2464420521d4df1dff3c910f7f5161e3c08059ceacb8a9d12886b6368f4185d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526904af0411cdd6be713011c2a727f8f69c4b672ca45d586fe00af5e71e715a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146e182e846e0e5c267876f2846ddf2d8816291c0fa17aaf336709cb3e38bce2(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf087a06a0171cc210ad0c713c85daeb00c0e986f54453b290f503a2563151b(
    *,
    label_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574e2817f73c5f2fc03b2be8e8f70042b871de4ffc920a507f4314fa6c32166c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b929dfefa42803303db10b3e76af12e00069e25bd197cbb5ec2fab1ec664ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7176ef749009f43ef3d23528bfd4f840258703e8480e74167cc13244d2e373(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e107fbfcd274f42d05d411c3a287fee02679944b034bb045d773b060e44a9e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90841796c0359c074dffbf712e430c9699f41662fbb0d8c6fda26e7b77522841(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d5067204c3d7bae4c273f7bcb2afd6b1eaacb942dd58fc5a30ce0be910d00e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce9f63b05df64727ddb71c9ad347f8aeba3c956d9fbafc2f8904a8f26650103(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7dbc5f31633511f09d0f5488544945b51d6e3a8dc05265fa2214bf6cad1385(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee85b189f592fd19380f5a97bd7e65c7c3bb07b25d772cd76cd4ea30b6e9859(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ba205ecfc8ad89e4341ac79b7e156d7037877f7cf7f9ef5a841d2985b9809c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bc2f22b5668d1e946a8fe5fe25568562561db592207e82f056c0ddec54e53c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b7952b2a83f57c429a763629ff6a6c5bc945074a26ff75516856ef7131e101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a206455172d04d60ce1e06c8ec47a07867410cb6996dc5b24fb47ad6c71f9dd6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f13f9db612cff7eb86bd9cbe93f2b2b74e88c8349ce920504b4f6173e0384d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7211592ad32abab1ff25b8cd50db91ea8cd32facc67d8bffdf713e95be5ef9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103f4d03609d147de06ab87bd787bd6761ee5e6fd96b6af422532753bc5a8cc0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea56621a09218e12d4bee554c351c8029bd8726af55b92e97e960978244ab696(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27106464359a09a30ef6021f777a3fd4830df107f6ed2e1ff52b5947ee7e5722(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8688b61247ee44b77969a5fae9c92f0b613de9ef4730114fc3c4e572905276aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec9446a8c0ca93f7fdeb0912532ced86b540a274385c435d2c915598919b5f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c892af3b73e43a467cf06ec923ebd04f03ee476616006aa0dd4803e65fb7ff1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463a11ea31b9b75cea8c933bf4fb6ef4a2d7b4e72f1693b571966728c93831de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705be604e0573d7d4c3bec835d474e3544738188f0a60758c6d5f2de690af153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4cec8cf7a42bc62fef2643941b628b012719a6cad1d3e375baf26b72a64ac98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5276ddecce71067cf279e6598843fd3df47ec1debe76880040ee8a2a2edf5b43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b2095bf0b9e1401441cfd80b57618d09251b47e94d4655f892e5aa84f2e729(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b725d49020edcd631da2a28aadce944b2fcc1433d07c5629d8aa3ed87ac4e5(
    *,
    method: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod, typing.Dict[builtins.str, typing.Any]]] = None,
    query_string: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString, typing.Dict[builtins.str, typing.Any]]] = None,
    single_header: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader, typing.Dict[builtins.str, typing.Any]]] = None,
    uri_path: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdf35c910b97c9482680cd644ff8c499d920a569dd9628df6839c9d20a83ebb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64a936138200dc40ff2d4c22c6168d71b9765722dfade73be4954ffee792eb0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0b325f2d400a7ec408fbccf4445395ecbf8f15841a594dc6a5b8435a4cc5c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea70ae3ada4fe3383769f74441c4540c8db4cbfba9155d85ca396f0b3e4b10a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67dd294affe90760265b3dece42b71f6cb93e90f11bcc4cd40addb7fdc964ec7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb205e54cde5b7c19306ba4479a40c1adb6854e1ed77a58b2b9d1f01d7022a63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf10955946c13faf1869a9b85bc0efba4dc471407ca1f646af500f73087cd83e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af4a39dbd4f57b8adad57dd384ef1e48e53bce7547b1f4436425dd6032eaf7a(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93e4f3134947ebe50244708c1029208299a47ed9c6467911c578c4676777b9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d48b6a52d8d67e0face87ad7ef1e8d9debd3cd42002810e3c68b3d807b069fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27047c272ce9a1ade90129655e442e900288b4bf45d0717d09811a4083d378e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c87f6e9a82508e3c42424345100df4da900f79c4b72b0cd999f53cbeda84f1d(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00469d9ac0bad062d5d1c2721825afb9073d35e687ea01c47f4777a9fe00aca7(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b84248aabe5a3b1fef0a364d2afce1a82f05a2eea25eb0eeb68dd0fa4f3691f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf23c6df135e70cf8233551ed6a9ed8b456252dc7f32f0a42ab72b48685b1fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96ee4afb7f1fba5f43180b05050f96d25dd2d777a4987b2cf5bd7059fa04a69(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93e2fddba7132b00078d81d596ee7bf43b19d4725d8edcb6a54e940cde5e824(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c92367ec578016819d24da9f0782d40fe7f0fd0bdac36d6d4cf9c9f94d218b(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath],
) -> None:
    """Type checking stubs"""
    pass
