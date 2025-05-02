r'''
# `aws_appflow_connector_profile`

Refer to the Terraform Registry for docs: [`aws_appflow_connector_profile`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile).
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


class AppflowConnectorProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile aws_appflow_connector_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_mode: builtins.str,
        connector_profile_config: typing.Union["AppflowConnectorProfileConnectorProfileConfig", typing.Dict[builtins.str, typing.Any]],
        connector_type: builtins.str,
        name: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile aws_appflow_connector_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connection_mode AppflowConnectorProfile#connection_mode}.
        :param connector_profile_config: connector_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_config AppflowConnectorProfile#connector_profile_config}
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_type AppflowConnectorProfile#connector_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#name AppflowConnectorProfile#name}.
        :param connector_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_label AppflowConnectorProfile#connector_label}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#id AppflowConnectorProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#kms_arn AppflowConnectorProfile#kms_arn}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c77efecfffbe5deda621a7d10bccb2a5097535fbc657f41fbde51cdedcb22b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppflowConnectorProfileConfig(
            connection_mode=connection_mode,
            connector_profile_config=connector_profile_config,
            connector_type=connector_type,
            name=name,
            connector_label=connector_label,
            id=id,
            kms_arn=kms_arn,
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
        '''Generates CDKTF code for importing a AppflowConnectorProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppflowConnectorProfile to import.
        :param import_from_id: The id of the existing AppflowConnectorProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppflowConnectorProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d235022e0efbf8b108e299261f0f39b7dec4fde2d34786ba23070f84a7ae6b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConnectorProfileConfig")
    def put_connector_profile_config(
        self,
        *,
        connector_profile_credentials: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials", typing.Dict[builtins.str, typing.Any]],
        connector_profile_properties: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param connector_profile_credentials: connector_profile_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_credentials AppflowConnectorProfile#connector_profile_credentials}
        :param connector_profile_properties: connector_profile_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_properties AppflowConnectorProfile#connector_profile_properties}
        '''
        value = AppflowConnectorProfileConnectorProfileConfig(
            connector_profile_credentials=connector_profile_credentials,
            connector_profile_properties=connector_profile_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectorProfileConfig", [value]))

    @jsii.member(jsii_name="resetConnectorLabel")
    def reset_connector_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorLabel", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsArn")
    def reset_kms_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsArn", []))

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
    @jsii.member(jsii_name="connectorProfileConfig")
    def connector_profile_config(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigOutputReference", jsii.get(self, "connectorProfileConfig"))

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialsArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionModeInput")
    def connection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorLabelInput")
    def connector_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileConfigInput")
    def connector_profile_config_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfig"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfig"], jsii.get(self, "connectorProfileConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorTypeInput")
    def connector_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsArnInput")
    def kms_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionMode")
    def connection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionMode"))

    @connection_mode.setter
    def connection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f224e49620571185f2b85a19052a498a9b1eba9f7d42ac25d0e6523f29c9d056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorLabel")
    def connector_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorLabel"))

    @connector_label.setter
    def connector_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244928185646bbc8c88276a568b77f990f4b4eec74868546cbd1467d3a5ff372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f948850b47008a78d7c68008d7a9599f848ee41ef257eb1959c79a6b71e6b34f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc4f38c06faec1602cd39334a7509f0acbfad38c99fc98b6b625d540cdc3223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f24832a546999b478fd8dca734de8976b76ba125cb899e39b02fea5a1a12bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fdb49881b6dc6fd2b4933edfbd6e78b89a6dfb1bc3595c8c8497d36e5bfb69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_mode": "connectionMode",
        "connector_profile_config": "connectorProfileConfig",
        "connector_type": "connectorType",
        "name": "name",
        "connector_label": "connectorLabel",
        "id": "id",
        "kms_arn": "kmsArn",
    },
)
class AppflowConnectorProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connection_mode: builtins.str,
        connector_profile_config: typing.Union["AppflowConnectorProfileConnectorProfileConfig", typing.Dict[builtins.str, typing.Any]],
        connector_type: builtins.str,
        name: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connection_mode AppflowConnectorProfile#connection_mode}.
        :param connector_profile_config: connector_profile_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_config AppflowConnectorProfile#connector_profile_config}
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_type AppflowConnectorProfile#connector_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#name AppflowConnectorProfile#name}.
        :param connector_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_label AppflowConnectorProfile#connector_label}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#id AppflowConnectorProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#kms_arn AppflowConnectorProfile#kms_arn}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(connector_profile_config, dict):
            connector_profile_config = AppflowConnectorProfileConnectorProfileConfig(**connector_profile_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f7c04e014af53c5237f67178ad97e09f417a392ce887babf8ce0a2c49682ea)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_mode", value=connection_mode, expected_type=type_hints["connection_mode"])
            check_type(argname="argument connector_profile_config", value=connector_profile_config, expected_type=type_hints["connector_profile_config"])
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument connector_label", value=connector_label, expected_type=type_hints["connector_label"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_mode": connection_mode,
            "connector_profile_config": connector_profile_config,
            "connector_type": connector_type,
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
        if connector_label is not None:
            self._values["connector_label"] = connector_label
        if id is not None:
            self._values["id"] = id
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn

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
    def connection_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connection_mode AppflowConnectorProfile#connection_mode}.'''
        result = self._values.get("connection_mode")
        assert result is not None, "Required property 'connection_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_profile_config(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfig":
        '''connector_profile_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_config AppflowConnectorProfile#connector_profile_config}
        '''
        result = self._values.get("connector_profile_config")
        assert result is not None, "Required property 'connector_profile_config' is missing"
        return typing.cast("AppflowConnectorProfileConnectorProfileConfig", result)

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_type AppflowConnectorProfile#connector_type}.'''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#name AppflowConnectorProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_label AppflowConnectorProfile#connector_label}.'''
        result = self._values.get("connector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#id AppflowConnectorProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#kms_arn AppflowConnectorProfile#kms_arn}.'''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connector_profile_credentials": "connectorProfileCredentials",
        "connector_profile_properties": "connectorProfileProperties",
    },
)
class AppflowConnectorProfileConnectorProfileConfig:
    def __init__(
        self,
        *,
        connector_profile_credentials: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials", typing.Dict[builtins.str, typing.Any]],
        connector_profile_properties: typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param connector_profile_credentials: connector_profile_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_credentials AppflowConnectorProfile#connector_profile_credentials}
        :param connector_profile_properties: connector_profile_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_properties AppflowConnectorProfile#connector_profile_properties}
        '''
        if isinstance(connector_profile_credentials, dict):
            connector_profile_credentials = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials(**connector_profile_credentials)
        if isinstance(connector_profile_properties, dict):
            connector_profile_properties = AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties(**connector_profile_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4790a2075e98441b8097180f95be7fa01ab2e6a1b20d9842672e820f2ac987b9)
            check_type(argname="argument connector_profile_credentials", value=connector_profile_credentials, expected_type=type_hints["connector_profile_credentials"])
            check_type(argname="argument connector_profile_properties", value=connector_profile_properties, expected_type=type_hints["connector_profile_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_profile_credentials": connector_profile_credentials,
            "connector_profile_properties": connector_profile_properties,
        }

    @builtins.property
    def connector_profile_credentials(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials":
        '''connector_profile_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_credentials AppflowConnectorProfile#connector_profile_credentials}
        '''
        result = self._values.get("connector_profile_credentials")
        assert result is not None, "Required property 'connector_profile_credentials' is missing"
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials", result)

    @builtins.property
    def connector_profile_properties(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties":
        '''connector_profile_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#connector_profile_properties AppflowConnectorProfile#connector_profile_properties}
        '''
        result = self._values.get("connector_profile_properties")
        assert result is not None, "Required property 'connector_profile_properties' is missing"
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "honeycode": "honeycode",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "redshift": "redshift",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "snowflake": "snowflake",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        if isinstance(amplitude, dict):
            amplitude = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude(**amplitude)
        if isinstance(custom_connector, dict):
            custom_connector = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector(**custom_connector)
        if isinstance(datadog, dict):
            datadog = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog(**datadog)
        if isinstance(dynatrace, dict):
            dynatrace = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace(**dynatrace)
        if isinstance(google_analytics, dict):
            google_analytics = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics(**google_analytics)
        if isinstance(honeycode, dict):
            honeycode = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode(**honeycode)
        if isinstance(infor_nexus, dict):
            infor_nexus = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus(**infor_nexus)
        if isinstance(marketo, dict):
            marketo = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo(**marketo)
        if isinstance(redshift, dict):
            redshift = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift(**redshift)
        if isinstance(salesforce, dict):
            salesforce = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData(**sapo_data)
        if isinstance(service_now, dict):
            service_now = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow(**service_now)
        if isinstance(singular, dict):
            singular = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular(**singular)
        if isinstance(slack, dict):
            slack = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack(**slack)
        if isinstance(snowflake, dict):
            snowflake = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake(**snowflake)
        if isinstance(trendmicro, dict):
            trendmicro = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro(**trendmicro)
        if isinstance(veeva, dict):
            veeva = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva(**veeva)
        if isinstance(zendesk, dict):
            zendesk = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c87c137db4ca68ecb27a7b0cf3977a46c1411788faf9873ae1a8a5c9c118c53)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument honeycode", value=honeycode, expected_type=type_hints["honeycode"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
            check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amplitude is not None:
            self._values["amplitude"] = amplitude
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if datadog is not None:
            self._values["datadog"] = datadog
        if dynatrace is not None:
            self._values["dynatrace"] = dynatrace
        if google_analytics is not None:
            self._values["google_analytics"] = google_analytics
        if honeycode is not None:
            self._values["honeycode"] = honeycode
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if redshift is not None:
            self._values["redshift"] = redshift
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if service_now is not None:
            self._values["service_now"] = service_now
        if singular is not None:
            self._values["singular"] = singular
        if slack is not None:
            self._values["slack"] = slack
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude"]:
        '''amplitude block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        '''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude"], result)

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector"], result)

    @builtins.property
    def datadog(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog"]:
        '''datadog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        '''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog"], result)

    @builtins.property
    def dynatrace(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace"]:
        '''dynatrace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        '''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace"], result)

    @builtins.property
    def google_analytics(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics"]:
        '''google_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        '''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics"], result)

    @builtins.property
    def honeycode(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode"]:
        '''honeycode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        '''
        result = self._values.get("honeycode")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode"], result)

    @builtins.property
    def infor_nexus(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus"]:
        '''infor_nexus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        '''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo"], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"], result)

    @builtins.property
    def singular(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"]:
        '''singular block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        '''
        result = self._values.get("singular")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"], result)

    @builtins.property
    def slack(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"]:
        '''slack block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"], result)

    @builtins.property
    def snowflake(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"], result)

    @builtins.property
    def trendmicro(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"]:
        '''trendmicro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        '''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"], result)

    @builtins.property
    def veeva(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"]:
        '''veeva block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        '''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey", "secret_key": "secretKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude:
    def __init__(self, *, api_key: builtins.str, secret_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#secret_key AppflowConnectorProfile#secret_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e750a1c287e345a9cfd066208b9209308c878db9ba3b6d9d0a5c7ed4b2ca948)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "secret_key": secret_key,
        }

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#secret_key AppflowConnectorProfile#secret_key}.'''
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2c1d9135285abc916b05769a3bfb65ba6163d228afd08b69286d044539c9225)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8915a9e4bed346661b7ad68cba93429492db7164f934926f61c775149b08b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2810ee98d65ffe107b0b33737a9d211948ddc52ea42c61d5532c92d9cdbf45cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77888663df9c9161637bc65b356f96f33183c972b9ab5926bba79c1677375394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "api_key": "apiKey",
        "basic": "basic",
        "custom": "custom",
        "oauth2": "oauth2",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        api_key: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey", typing.Dict[builtins.str, typing.Any]]] = None,
        basic: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#authentication_type AppflowConnectorProfile#authentication_type}.
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#basic AppflowConnectorProfile#basic}
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom AppflowConnectorProfile#custom}
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2 AppflowConnectorProfile#oauth2}
        '''
        if isinstance(api_key, dict):
            api_key = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey(**api_key)
        if isinstance(basic, dict):
            basic = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic(**basic)
        if isinstance(custom, dict):
            custom = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom(**custom)
        if isinstance(oauth2, dict):
            oauth2 = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2(**oauth2)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120788d3f077a5da35210469622f1d41b740ab10eaa2a8d80931a804321d4a1d)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument oauth2", value=oauth2, expected_type=type_hints["oauth2"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
        }
        if api_key is not None:
            self._values["api_key"] = api_key
        if basic is not None:
            self._values["basic"] = basic
        if custom is not None:
            self._values["custom"] = custom
        if oauth2 is not None:
            self._values["oauth2"] = oauth2

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#authentication_type AppflowConnectorProfile#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey"]:
        '''api_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey"], result)

    @builtins.property
    def basic(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic"]:
        '''basic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#basic AppflowConnectorProfile#basic}
        '''
        result = self._values.get("basic")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic"], result)

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom"]:
        '''custom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom AppflowConnectorProfile#custom}
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom"], result)

    @builtins.property
    def oauth2(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2"]:
        '''oauth2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2 AppflowConnectorProfile#oauth2}
        '''
        result = self._values.get("oauth2")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey", "api_secret_key": "apiSecretKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        api_secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed3491a4a8e3303e2fd26e7aec33ba6f4277c28d7a282537b88e3c48cd7570f)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
        }
        if api_secret_key is not None:
            self._values["api_secret_key"] = api_secret_key

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_secret_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.'''
        result = self._values.get("api_secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55d76ea93bb301b49f4a5840e88964804aa5893b5e7c6f14fa203a6c3d60f7b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApiSecretKey")
    def reset_api_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiSecretKey", []))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSecretKeyInput")
    def api_secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSecretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33286cf2819fbc4cf3ca5a9c288d596d230e8b5bae2389b7e3ec1aaa6b84307a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiSecretKey")
    def api_secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSecretKey"))

    @api_secret_key.setter
    def api_secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ecb930fa2f788c340aed83965aa952b7a333236c1c291a7dfdff2d0165a812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSecretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac060c7ede2a1b811f65c01c5913f8c56d645afca3c16100e7a9c86a2162af0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349b09f29a2922e9dbf95f830174143bdc96e0301e8ec496ba36f343d762a691)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ec45a89f307bb92caf322704f3a955a6eea3e01b8220a21b721f7d3f8908625)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbcf0dd85b177dc9f2ba9aa2063edc7223629990340bdea2113cf1b7c3203169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b52f46150969d30cd1862d86fe9df4c8497ac68f913c7f1921500d46621262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503d49223b70a321423cfe8c9667c252da1c06aba62ac8272089df6cae4f01e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom",
    jsii_struct_bases=[],
    name_mapping={
        "custom_authentication_type": "customAuthenticationType",
        "credentials_map": "credentialsMap",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom:
    def __init__(
        self,
        *,
        custom_authentication_type: builtins.str,
        credentials_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param custom_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_authentication_type AppflowConnectorProfile#custom_authentication_type}.
        :param credentials_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#credentials_map AppflowConnectorProfile#credentials_map}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e865dc3c8db82c257f2b7fe5dda30048e671102d1731c35c2c9326638070f69)
            check_type(argname="argument custom_authentication_type", value=custom_authentication_type, expected_type=type_hints["custom_authentication_type"])
            check_type(argname="argument credentials_map", value=credentials_map, expected_type=type_hints["credentials_map"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_authentication_type": custom_authentication_type,
        }
        if credentials_map is not None:
            self._values["credentials_map"] = credentials_map

    @builtins.property
    def custom_authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_authentication_type AppflowConnectorProfile#custom_authentication_type}.'''
        result = self._values.get("custom_authentication_type")
        assert result is not None, "Required property 'custom_authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials_map(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#credentials_map AppflowConnectorProfile#credentials_map}.'''
        result = self._values.get("credentials_map")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e94bff6209670aa5daf4ab730e3a6a57d00832b578ecf29e95e86f828d17456d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCredentialsMap")
    def reset_credentials_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialsMap", []))

    @builtins.property
    @jsii.member(jsii_name="credentialsMapInput")
    def credentials_map_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "credentialsMapInput"))

    @builtins.property
    @jsii.member(jsii_name="customAuthenticationTypeInput")
    def custom_authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customAuthenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsMap")
    def credentials_map(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "credentialsMap"))

    @credentials_map.setter
    def credentials_map(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c7e38315536d540c2fa014781f6530ee77b90ab4c261c7b44db07ccc3ed0e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsMap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customAuthenticationType")
    def custom_authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customAuthenticationType"))

    @custom_authentication_type.setter
    def custom_authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195ba4b85e3e47dc35de487e486cbd128ae9b702a7a3cff98935363076eb2858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAuthenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29748a7cbf90ca4f89240799079bc13a9ef291c7d502d1e54194d9214dcbf9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebb51b101dfadb9ca1e3fd5c75123412a091e6242f8ddc7b8e3b2b3c4d10aec)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4792571588aca63a1980a450b5447632da7a65dc83c854205798052070e0a267)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36d6cc3166374f9c4ce904ea764b9b2a4d4c22c1917f31f3ab03e12da503d7bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f609522402975593b947b9ac9d1f6e84368fa10c8c7578bf8b4ef6f6358f0d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da49fadc9103ced71c115a68fa26f8bce0d90b65fdca17e409d83eb138f78281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6eeb191ea5b683d0990ed7507137e4cafa65ca850515ab61e47a1ad94facad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b61db2621bb0dfa2cef0eea0e5a5aa090ba4727b1618edb96cbbdee084671bde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074c155389b49083139db08ab5c4488129c6bcc81eb39e03c49d1d37f3290408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee82c46c02eb8d2e08bd85343a42a0807d18c9ff44e63b1ab3ca9f797ae7b6f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d8087afbc92651ace2e959f37532e20b3c4b8fb64030aae8513e2ae03bf312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722dc47bc0f83a91e30024e8956768b73343296fb6aa90cd543a5124402873b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548db3cb91a8350b2466e0bc1ffe2751b02c4db83556d17f95b2174cbe0d2f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b6b500f5b832c230c47ab2c3bce432f62b0e1f8721c9f9c32f67f0f2dc38b58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKey")
    def put_api_key(
        self,
        *,
        api_key: builtins.str,
        api_secret_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey(
            api_key=api_key, api_secret_key=api_secret_key
        )

        return typing.cast(None, jsii.invoke(self, "putApiKey", [value]))

    @jsii.member(jsii_name="putBasic")
    def put_basic(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasic", [value]))

    @jsii.member(jsii_name="putCustom")
    def put_custom(
        self,
        *,
        custom_authentication_type: builtins.str,
        credentials_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param custom_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_authentication_type AppflowConnectorProfile#custom_authentication_type}.
        :param credentials_map: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#credentials_map AppflowConnectorProfile#credentials_map}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom(
            custom_authentication_type=custom_authentication_type,
            credentials_map=credentials_map,
        )

        return typing.cast(None, jsii.invoke(self, "putCustom", [value]))

    @jsii.member(jsii_name="putOauth2")
    def put_oauth2(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2(
            access_token=access_token,
            client_id=client_id,
            client_secret=client_secret,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2", [value]))

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetBasic")
    def reset_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasic", []))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetOauth2")
    def reset_oauth2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2", []))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="basic")
    def basic(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference, jsii.get(self, "basic"))

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference, jsii.get(self, "custom"))

    @builtins.property
    @jsii.member(jsii_name="oauth2")
    def oauth2(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference, jsii.get(self, "oauth2"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="basicInput")
    def basic_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic], jsii.get(self, "basicInput"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2Input")
    def oauth2_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2], jsii.get(self, "oauth2Input"))

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fec2a6b818bdf43c0572d65b41d0c1b0048b4ebd988751735fdc46f7ba322f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e173df80741a3167b9372ddedfef73ab0029141a998050a9416d791a4dffc36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey", "application_key": "applicationKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog:
    def __init__(self, *, api_key: builtins.str, application_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param application_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_key AppflowConnectorProfile#application_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb368de38e48a08c8f36cbd1189ad61af711b407d7c5d2c575abc0241036b47)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument application_key", value=application_key, expected_type=type_hints["application_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "application_key": application_key,
        }

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_key AppflowConnectorProfile#application_key}.'''
        result = self._values.get("application_key")
        assert result is not None, "Required property 'application_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b7864a7ba6fdb637b1d5da19d228f1ccd906ecee2de8df52725810568571c90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationKeyInput")
    def application_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5f91c42f7b32a2e282623a84059b155b5122f9112e69f53a1bdc9d5b19690e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationKey")
    def application_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationKey"))

    @application_key.setter
    def application_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223d60728025b5c82af8d5092a4ee7f81be7d59290ae2314177524d0d88a830f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a8d43b14512de5d42d812d8f5685e55e4d828b7a377c8479a3b70af73258c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace",
    jsii_struct_bases=[],
    name_mapping={"api_token": "apiToken"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace:
    def __init__(self, *, api_token: builtins.str) -> None:
        '''
        :param api_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_token AppflowConnectorProfile#api_token}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8741009c3fecc832012dde3a00ff7cc624b0857260545a30670467cab67c67)
            check_type(argname="argument api_token", value=api_token, expected_type=type_hints["api_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_token": api_token,
        }

    @builtins.property
    def api_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_token AppflowConnectorProfile#api_token}.'''
        result = self._values.get("api_token")
        assert result is not None, "Required property 'api_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3a3e75759ec0ddaa955c7f00594b47f88ff428b86f271c67f88aa9a22f9246c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiTokenInput")
    def api_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="apiToken")
    def api_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiToken"))

    @api_token.setter
    def api_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b619f8dbec53e8a8e9bd8c67e7eec0a99e7381c8d088d1753cd53cf535ea50c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212b66a1f71cb2227d49323b897c59f87e3e636994145c8b499bcc40a12af167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f181dc7e6d47b08589556a550057a826fc8457ae23dbd220bb35dd50c725b3)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afb42a5260090cd033b2c18145c75a8ea0b6aea1c93ec6ae28d0a3b9884d09f)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc9303a2cdf0d63bac690bee9eb29e446ab3917243283c5ad534874c79db9e70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b06635239c51c28fa1e261b513965c7e5517a30f566c5a76ba192b5df4c41c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a12b4c8d25bed6f0f97e054205842351a8bd11087f59663309b19b883ecfd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07b592d2aab9f8428e188d80fab2270fd66ead4142c72e889baf45f73725d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a8d0bec360bef90357d689deed5740c590a0ea115c88015a471abfea9f77846)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945edfbfaf41b91f6a071b412b001e8a4e389c5f35ad540c78a366e438373275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8c5bd03fb3d0e78f5630d783a6fe3d2046ecf0d64f9dab2d2cbcf9a6ef489d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5debd68bc98abdfd91dc650064b73c101051620b9991e007cd83eaa5f52d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1d7ae5989e55dae8d196a4e0b10a9812221f862813ca6041beef92eefeaaec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511b43d783d5540fba0083f70c062fd3c960751367ec6b4fe0a296da0dc1938a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a644cf85933e9bea4b5e01b0e85dc71ff2780c916eb5be637584f887f7b5b5)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c33e6ed4f2839797cbead3a434930ad363d3aa6e8165c391bdab12d0acc58b4)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0f1fcee25faa99b99cdef25925b2174808fc2972ffbe398f71b84bd7197361b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5cc0a75ca6e8b495a836b10cff7b2e3bc3577993c2f5912eac498a7b016a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc932e220f2ce5e0a70f58c5f9fb61994d2f5cee1105c299b26b777c51af8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760defb0001bb526381ed6ea243752ac6bce8c484eac9b59606f2aac703615c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af425bf32b31da1eb2cddfe857044a219c02c53487bb7a8955c12e5be0e3bd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0222a1207d836644f536e9ac28af2c1e526a05bdab31e88c280c899831740c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483ce9e52de80fd107086bb13f635c582eb8f50c8fa63ce42d48f2ec74c5ff8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b92d85b71a24dd8efa7b25b774be43b460114b4b546d1997f32510735a5526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "datakey": "datakey",
        "secret_access_key": "secretAccessKey",
        "user_id": "userId",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        datakey: builtins.str,
        secret_access_key: builtins.str,
        user_id: builtins.str,
    ) -> None:
        '''
        :param access_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_key_id AppflowConnectorProfile#access_key_id}.
        :param datakey: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datakey AppflowConnectorProfile#datakey}.
        :param secret_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#secret_access_key AppflowConnectorProfile#secret_access_key}.
        :param user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#user_id AppflowConnectorProfile#user_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c5813a0886b341013d4b5b261580c5a846b3ef89b80125d3b798c17e02f99c)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument datakey", value=datakey, expected_type=type_hints["datakey"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "datakey": datakey,
            "secret_access_key": secret_access_key,
            "user_id": user_id,
        }

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_key_id AppflowConnectorProfile#access_key_id}.'''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datakey(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datakey AppflowConnectorProfile#datakey}.'''
        result = self._values.get("datakey")
        assert result is not None, "Required property 'datakey' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#secret_access_key AppflowConnectorProfile#secret_access_key}.'''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#user_id AppflowConnectorProfile#user_id}.'''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ade280458fd17365b03fed60446786559ac26bd66f1920daeb721017a7b7966)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datakeyInput")
    def datakey_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datakeyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298d1a5f61f99820f990e34a8d3f699339a14c48a4ed358b27b176cb6f1dbb9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datakey")
    def datakey(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datakey"))

    @datakey.setter
    def datakey(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65248daefa58a0eb7dd3ecef1a4e01afbccdad8bc7607f575e4de46ce166c90e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datakey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849c91226eec9ae2c63e291cd04e45af45cee5620caa575f8ce1b220773fd740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b1f5526e8aac78d26454792df63b5544eb2b1f2c1cc4a3855f6f1e795a0b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5812e896ea6431a558156182d5eda9beb4c667335924f73177a2d056b35058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0af9810bfa26e69659483c902e087f4fca0f7d388d3bfb7783efa2be016d7c)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4dddffe9a8494f2f765a19b607697a328633e2e223a50896123cf34646939e)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ab415c3e0760b1c765b8643b7ddff53b2a7be019a3df3f1ba2cb07a98271a5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8d38dd91c6947cb0a918ff2075eb4b5014ff3fb29d2b737368dee543bd97bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2eef75cee2a8683c14941668ca296f7831bb4577906a41880990ff665c9407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b73f506f39057b7e1a947b64c9698afb17fc5eddfb1fe4320f5d9ae977292d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1386c704e11652a4dd0d9975050c2ed6c470f778ad99b843b4981d8a151b3d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6070e876a7c40ac935f5b9673d27d3f43482c0b3ade416b6801b283c16562e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5f9f3ab02a5193abce73ffe8af5a2c61320f7e459e9f4861d5a39f3981ed11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca05b58fa74635a96682407c9f1a083e40f8d9006226f4f1d9d63cb5a1d5fff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdfd4a8aaf49daddff1e046b57a93107abe871f13e137481d15a4a985fd532c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0053d44f5d817d623179648a9b0a006e870bd7d9dba8f3dd3ed843e57c0266d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmplitude")
    def put_amplitude(self, *, api_key: builtins.str, secret_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#secret_key AppflowConnectorProfile#secret_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude(
            api_key=api_key, secret_key=secret_key
        )

        return typing.cast(None, jsii.invoke(self, "putAmplitude", [value]))

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        authentication_type: builtins.str,
        api_key: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey, typing.Dict[builtins.str, typing.Any]]] = None,
        basic: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic, typing.Dict[builtins.str, typing.Any]]] = None,
        custom: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom, typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#authentication_type AppflowConnectorProfile#authentication_type}.
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#basic AppflowConnectorProfile#basic}
        :param custom: custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom AppflowConnectorProfile#custom}
        :param oauth2: oauth2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2 AppflowConnectorProfile#oauth2}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector(
            authentication_type=authentication_type,
            api_key=api_key,
            basic=basic,
            custom=custom,
            oauth2=oauth2,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putDatadog")
    def put_datadog(
        self,
        *,
        api_key: builtins.str,
        application_key: builtins.str,
    ) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        :param application_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_key AppflowConnectorProfile#application_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog(
            api_key=api_key, application_key=application_key
        )

        return typing.cast(None, jsii.invoke(self, "putDatadog", [value]))

    @jsii.member(jsii_name="putDynatrace")
    def put_dynatrace(self, *, api_token: builtins.str) -> None:
        '''
        :param api_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_token AppflowConnectorProfile#api_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace(
            api_token=api_token
        )

        return typing.cast(None, jsii.invoke(self, "putDynatrace", [value]))

    @jsii.member(jsii_name="putGoogleAnalytics")
    def put_google_analytics(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleAnalytics", [value]))

    @jsii.member(jsii_name="putHoneycode")
    def put_honeycode(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode(
            access_token=access_token,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putHoneycode", [value]))

    @jsii.member(jsii_name="putInforNexus")
    def put_infor_nexus(
        self,
        *,
        access_key_id: builtins.str,
        datakey: builtins.str,
        secret_access_key: builtins.str,
        user_id: builtins.str,
    ) -> None:
        '''
        :param access_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_key_id AppflowConnectorProfile#access_key_id}.
        :param datakey: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datakey AppflowConnectorProfile#datakey}.
        :param secret_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#secret_access_key AppflowConnectorProfile#secret_access_key}.
        :param user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#user_id AppflowConnectorProfile#user_id}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus(
            access_key_id=access_key_id,
            datakey=datakey,
            secret_access_key=secret_access_key,
            user_id=user_id,
        )

        return typing.cast(None, jsii.invoke(self, "putInforNexus", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_credentials_arn: typing.Optional[builtins.str] = None,
        jwt_token: typing.Optional[builtins.str] = None,
        oauth2_grant_type: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_credentials_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_credentials_arn AppflowConnectorProfile#client_credentials_arn}.
        :param jwt_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#jwt_token AppflowConnectorProfile#jwt_token}.
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce(
            access_token=access_token,
            client_credentials_arn=client_credentials_arn,
            jwt_token=jwt_token,
            oauth2_grant_type=oauth2_grant_type,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        basic_auth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param basic_auth_credentials: basic_auth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#basic_auth_credentials AppflowConnectorProfile#basic_auth_credentials}
        :param oauth_credentials: oauth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_credentials AppflowConnectorProfile#oauth_credentials}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData(
            basic_auth_credentials=basic_auth_credentials,
            oauth_credentials=oauth_credentials,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSingular")
    def put_singular(self, *, api_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular(
            api_key=api_key
        )

        return typing.cast(None, jsii.invoke(self, "putSingular", [value]))

    @jsii.member(jsii_name="putSlack")
    def put_slack(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
        )

        return typing.cast(None, jsii.invoke(self, "putSlack", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putTrendmicro")
    def put_trendmicro(self, *, api_secret_key: builtins.str) -> None:
        '''
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro(
            api_secret_key=api_secret_key
        )

        return typing.cast(None, jsii.invoke(self, "putTrendmicro", [value]))

    @jsii.member(jsii_name="putVeeva")
    def put_veeva(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putVeeva", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
        )

        return typing.cast(None, jsii.invoke(self, "putZendesk", [value]))

    @jsii.member(jsii_name="resetAmplitude")
    def reset_amplitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmplitude", []))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetDatadog")
    def reset_datadog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadog", []))

    @jsii.member(jsii_name="resetDynatrace")
    def reset_dynatrace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynatrace", []))

    @jsii.member(jsii_name="resetGoogleAnalytics")
    def reset_google_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleAnalytics", []))

    @jsii.member(jsii_name="resetHoneycode")
    def reset_honeycode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoneycode", []))

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSingular")
    def reset_singular(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingular", []))

    @jsii.member(jsii_name="resetSlack")
    def reset_slack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlack", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetTrendmicro")
    def reset_trendmicro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrendmicro", []))

    @jsii.member(jsii_name="resetVeeva")
    def reset_veeva(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVeeva", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="amplitude")
    def amplitude(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference, jsii.get(self, "amplitude"))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference, jsii.get(self, "datadog"))

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference, jsii.get(self, "dynatrace"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference, jsii.get(self, "googleAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="honeycode")
    def honeycode(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference, jsii.get(self, "honeycode"))

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference, jsii.get(self, "inforNexus"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference", jsii.get(self, "singular"))

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference", jsii.get(self, "slack"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference", jsii.get(self, "trendmicro"))

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference", jsii.get(self, "veeva"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="honeycodeInput")
    def honeycode_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode], jsii.get(self, "honeycodeInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular"], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack"], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro"], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva"], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232eb785c655609eb12c0075321faeffc2a30478b45ecea94ae1a54de1121298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87aaed92c36e91c6f52d976c46181c6221cf5adea758863535d9de2a6fa9d89)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2132db1fc337a7f390594ab5aab0cd12d51dc8d9963e59f0f1bba285af3ae658)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8787efa761df2758bd27183e418f6d3f0f24253cb2d2346bbe81200c6d9011f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c81b5274a1da64bef3068bf7649898d72dd998589038de1b9b8b2238b43b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9307d6acd3f5ddb99effa8d859d89f99e05d192a8387392cb14c722e20c599c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "client_credentials_arn": "clientCredentialsArn",
        "jwt_token": "jwtToken",
        "oauth2_grant_type": "oauth2GrantType",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        client_credentials_arn: typing.Optional[builtins.str] = None,
        jwt_token: typing.Optional[builtins.str] = None,
        oauth2_grant_type: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param client_credentials_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_credentials_arn AppflowConnectorProfile#client_credentials_arn}.
        :param jwt_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#jwt_token AppflowConnectorProfile#jwt_token}.
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bd4c167c83f31c68ce47e22809355aef5423d9f63c3b51b2a4c1fe36215127)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument client_credentials_arn", value=client_credentials_arn, expected_type=type_hints["client_credentials_arn"])
            check_type(argname="argument jwt_token", value=jwt_token, expected_type=type_hints["jwt_token"])
            check_type(argname="argument oauth2_grant_type", value=oauth2_grant_type, expected_type=type_hints["oauth2_grant_type"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if client_credentials_arn is not None:
            self._values["client_credentials_arn"] = client_credentials_arn
        if jwt_token is not None:
            self._values["jwt_token"] = jwt_token
        if oauth2_grant_type is not None:
            self._values["oauth2_grant_type"] = oauth2_grant_type
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_credentials_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_credentials_arn AppflowConnectorProfile#client_credentials_arn}.'''
        result = self._values.get("client_credentials_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwt_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#jwt_token AppflowConnectorProfile#jwt_token}.'''
        result = self._values.get("jwt_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_grant_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.'''
        result = self._values.get("oauth2_grant_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496f6512fe4dd625947947caf58814c7943a5a4baa6d56901431ec080c121c71)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e89fce5babe4d3ca1eb5f87b8ce295b7b414fe0385c80599947eb9fb3804cb58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0a22563f3be9074561e6e0d7c5c121b84d76610cd38cb58606964fccc2d23b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e28e53f4229db657f6209aed7380da31a421eb978178d848a7ea2322268c87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5a1af282215a3c5f7c342c22ac59e5f7a31b25fee4f56859f798d89602ffe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d0f3f115beda05839a678358ec6bd1202186c83fd41f556789b4fd0ae80c03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetClientCredentialsArn")
    def reset_client_credentials_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCredentialsArn", []))

    @jsii.member(jsii_name="resetJwtToken")
    def reset_jwt_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtToken", []))

    @jsii.member(jsii_name="resetOauth2GrantType")
    def reset_oauth2_grant_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2GrantType", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCredentialsArnInput")
    def client_credentials_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCredentialsArnInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtTokenInput")
    def jwt_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwtTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantTypeInput")
    def oauth2_grant_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2GrantTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0b6f035623efc4726f873bf1398952a8634f3b650b0e4d8c529931bc9044a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCredentialsArn")
    def client_credentials_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCredentialsArn"))

    @client_credentials_arn.setter
    def client_credentials_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a78a582120d633c50371336f9e25dfbc7a501a923b12c228340ebe1030ed08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCredentialsArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtToken")
    def jwt_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwtToken"))

    @jwt_token.setter
    def jwt_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f575ac18e83af0cfad8032555930b07faadd5b2e1a7a18f673187b1e8170933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantType")
    def oauth2_grant_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2GrantType"))

    @oauth2_grant_type.setter
    def oauth2_grant_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889159e5bf511de33382662cafbbcfbda2788b5007bf2117680d66a09db8b17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2GrantType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04790af1a8083e4c61d7ac0f286d933d681f339bd0556417f77144a14402a11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c70b5e7c2595bdb0759dfadd1c2e606081d0e1141bf247db50b88e039da9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "basic_auth_credentials": "basicAuthCredentials",
        "oauth_credentials": "oauthCredentials",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData:
    def __init__(
        self,
        *,
        basic_auth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_credentials: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param basic_auth_credentials: basic_auth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#basic_auth_credentials AppflowConnectorProfile#basic_auth_credentials}
        :param oauth_credentials: oauth_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_credentials AppflowConnectorProfile#oauth_credentials}
        '''
        if isinstance(basic_auth_credentials, dict):
            basic_auth_credentials = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials(**basic_auth_credentials)
        if isinstance(oauth_credentials, dict):
            oauth_credentials = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials(**oauth_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293f7dbc7135262bbda4ab967cf19cbd4647a80a3481f78487b7f38da1a0b2ed)
            check_type(argname="argument basic_auth_credentials", value=basic_auth_credentials, expected_type=type_hints["basic_auth_credentials"])
            check_type(argname="argument oauth_credentials", value=oauth_credentials, expected_type=type_hints["oauth_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_auth_credentials is not None:
            self._values["basic_auth_credentials"] = basic_auth_credentials
        if oauth_credentials is not None:
            self._values["oauth_credentials"] = oauth_credentials

    @builtins.property
    def basic_auth_credentials(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials"]:
        '''basic_auth_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#basic_auth_credentials AppflowConnectorProfile#basic_auth_credentials}
        '''
        result = self._values.get("basic_auth_credentials")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials"], result)

    @builtins.property
    def oauth_credentials(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials"]:
        '''oauth_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_credentials AppflowConnectorProfile#oauth_credentials}
        '''
        result = self._values.get("oauth_credentials")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ba028ec3b1202870eee9de8e843b3a2831ef3a0998a52df0ef585f43b4d64f)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a44e3d672e5744044201ef1cb69dd4823723e4c9b614b2d91f26dc025798a44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024cd796d4b107a8d8ff2ae943c4159311f2e6c44a3e409d6b6d403af8948a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd323b09d62a6bed5432604ee4489c272670e2a1581df591bac58354dd9c06d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63712334da6c07c7772b14efa1a84cada034611848e1f7154098803053d3bac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
        "refresh_token": "refreshToken",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313b61a437a1c2ea1b7d612af176bc2c44e7c7c24523bd90cab18561dad87399)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request
        if refresh_token is not None:
            self._values["refresh_token"] = refresh_token

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest"], result)

    @builtins.property
    def refresh_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.'''
        result = self._values.get("refresh_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec3805f91f4ff0bda60f5c67d9df8a84c90e9cafee7b8769bb03d76bad82db6)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97071e81c1d033eb22199bf795fd8bf22c6c4e9ac8ca594c3eda75ad5c0b5d2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a214185c5c45db428cfe70f8d1e9d1408a2ad526c9cca7978e707b775bf766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b40e9597a6f750c354c366bcf01b0c1af569efb2dce481577bf2a83f81d509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b2117de16d6561d3356fbf249e3072ad38aa474906594977072dbb384a020c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__838a6ccd3ee0842eb7b1ffaa9a083253401da2ffa7f3d717c6036ae0c161396d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @jsii.member(jsii_name="resetRefreshToken")
    def reset_refresh_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshToken", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenInput")
    def refresh_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9450ca381e1b20d60ded2faf10f132ccd04c58826a9f225c6da693986f567050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6045d2105c53b9183e81c4cac4ef1aa6967d8ecdb69dffa578478ddc7034c895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a19b293c59def028c9308f0aa250095d5369612e61dbb058792a744bae637e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshToken")
    def refresh_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshToken"))

    @refresh_token.setter
    def refresh_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89798ed3e3986180b0cccb569b59401d37c277b2fc810c3470104e867728077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1bcf2d093de38abbfb411f76902dee1317188d5b714d04d1a324734cba467b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6850bb2838d961240c5899da61adfaf879b86c3f335c246e2932332669a8636)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicAuthCredentials")
    def put_basic_auth_credentials(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasicAuthCredentials", [value]))

    @jsii.member(jsii_name="putOauthCredentials")
    def put_oauth_credentials(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        refresh_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        :param refresh_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#refresh_token AppflowConnectorProfile#refresh_token}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            oauth_request=oauth_request,
            refresh_token=refresh_token,
        )

        return typing.cast(None, jsii.invoke(self, "putOauthCredentials", [value]))

    @jsii.member(jsii_name="resetBasicAuthCredentials")
    def reset_basic_auth_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuthCredentials", []))

    @jsii.member(jsii_name="resetOauthCredentials")
    def reset_oauth_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuthCredentials")
    def basic_auth_credentials(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference, jsii.get(self, "basicAuthCredentials"))

    @builtins.property
    @jsii.member(jsii_name="oauthCredentials")
    def oauth_credentials(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference, jsii.get(self, "oauthCredentials"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthCredentialsInput")
    def basic_auth_credentials_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials], jsii.get(self, "basicAuthCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthCredentialsInput")
    def oauth_credentials_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials], jsii.get(self, "oauthCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b044fbcdd617226db469afdbefb46a55f235b9cbd749b0a919163fe2788129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fde00243188e9090ee195d76f062bd061b75ab41c83c4c2fb16cda01d88a18)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6f09c2268f0d31a7155ab65052df7f97c085ff798208acd2cd136dda3fddab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97296c180963fb86ea60356d915a4e2849ca4f7745fef0111ec78b3b426e94bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf82fee7b2ae7312eeb549b055c94f448acd00e3cdca28bbe296ac18e252416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2f475ccc397b19a7f26313be4c05528827b2f9959bc96eef3f5ece686223be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular:
    def __init__(self, *, api_key: builtins.str) -> None:
        '''
        :param api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6ca4f54914aa3e9045b9722572e5a7a96c99dffd3d898e0a66079f158107ef)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
        }

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_key AppflowConnectorProfile#api_key}.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96937b6a98d20ada07654525ed3978c4c7a4bad96eaaff80eaa96a9451d5f0ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649a50757e459a04f3e103d445c28560a91b7466a5c6c2bda1509f6b7acd7a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3778fbe9704c120cd8c6b71970e9dfc621f2efaf4123952cb4ae016fd6acb89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2655e807b374f140a36cfdf7487bb7517225c7e238b58843d0db6144289e04f9)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3b8177e802e57ade557c0ddcd3a96844a8f7e575168f26683fd1b69590a37c)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2973a2a25a6475b972753dddb3947e81b07d1548255f4560e63d2a439abb201f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4935b7f6717ce829421bb3fde4c18e62257ab9502e8901300d8c8d3389d1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2cf96a13df282ff977bfc6224b9a07e9a62ee7a7fe5db0e28a0f0f32abe8ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f212be9e03f51a008431b56fb7fb24154daec3fe6703bc2ba3024664bc349f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccdceba6df0dd5ce547aabdb1727d324cb72fd07ce2728bb91127b688daa4a4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d867c0fcc48e8f070afb606ccaf48015bffe7302834a9637b862513aa5e31e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5f605eb8b3dd6b2078c8341657329e598907598ff45a0ac0b22994259e6b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f257c109ffa91c8afd4fcc4f13392fe7d485c882a1c8cec5c5b742a15f82948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d853bd8e2de792bfe71b7fbc277491dc51abd589d2e6513b88e4f9a396f4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9d71908b05e2d983447d9601156cdef9feb9d792d7c8ad8da14a9d6c0d5316)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__314b68bc669d198e670d1c67dd3cb25c5b9116c27dd4d50c327e329012ef58c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a42b01ad0b0922dcc5cfdf4b5112f0cb9e621b9637a5af4fbc80fd53d9dd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7a7b9533076bec6c4d12eb285fff2fe3ac417a1eee0484ab0721ed9c43ce75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e471fb895aedb976db4902b359d2025aff9715859c0584c8f6a71fae510d229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro",
    jsii_struct_bases=[],
    name_mapping={"api_secret_key": "apiSecretKey"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro:
    def __init__(self, *, api_secret_key: builtins.str) -> None:
        '''
        :param api_secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe0eed58d83be8097be2339872eaca1ed8451e6e7412d5153e911dd6178d91e)
            check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_secret_key": api_secret_key,
        }

    @builtins.property
    def api_secret_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#api_secret_key AppflowConnectorProfile#api_secret_key}.'''
        result = self._values.get("api_secret_key")
        assert result is not None, "Required property 'api_secret_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d18e50a8ebb000b7e421f84794f0543e2898fc38ef5e2b896de1c0adde816698)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="apiSecretKeyInput")
    def api_secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSecretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSecretKey")
    def api_secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSecretKey"))

    @api_secret_key.setter
    def api_secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4707e9948acd52d35a2ae2eb681c07b1b9c4436b2a8a7804dcb104b39d21731d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSecretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce383b0d89dbe490c6f241fbbc1b678870152cc759bba6c2f60380cf99e93de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd5f2ff5f0ea4fac482245256ada3b1d547f232bc6f75704d58b429960e3e5f)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#password AppflowConnectorProfile#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#username AppflowConnectorProfile#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab49abcac2f9d5d7fa56813613bd98cfaaae7a008a3c22b035760cb1385a44e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540c17dc23305daa96559adff83606d8632cb800e154d39aedee93aaeab46906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004f5a3ea03016da824667060cf95adcbcffac6671d4fb9885e3008bd3212187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e18f51c7b1da83578af8e3f7d7cd884422a0417b5355b878dc3eb4c1acb8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "access_token": "accessToken",
        "oauth_request": "oauthRequest",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        oauth_request: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.
        :param oauth_request: oauth_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        if isinstance(oauth_request, dict):
            oauth_request = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest(**oauth_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb6445ad5b61a5622c0c859c58602dd62c8af61416c3ca6ce884172d842d627)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_request", value=oauth_request, expected_type=type_hints["oauth_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_request is not None:
            self._values["oauth_request"] = oauth_request

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_id AppflowConnectorProfile#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_secret AppflowConnectorProfile#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#access_token AppflowConnectorProfile#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_request(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest"]:
        '''oauth_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_request AppflowConnectorProfile#oauth_request}
        '''
        result = self._values.get("oauth_request")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest",
    jsii_struct_bases=[],
    name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest:
    def __init__(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b056472356c1f8762da1248b957193fbbe5e0dd04659b04168f947a95cc7fa)
            check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_code is not None:
            self._values["auth_code"] = auth_code
        if redirect_uri is not None:
            self._values["redirect_uri"] = redirect_uri

    @builtins.property
    def auth_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.'''
        result = self._values.get("auth_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.'''
        result = self._values.get("redirect_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1a0d08f3c0039c2676e8a52c72fe9c65b13e9da9cf6be5eb99410be4667aded)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthCode")
    def reset_auth_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthCode", []))

    @jsii.member(jsii_name="resetRedirectUri")
    def reset_redirect_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUri", []))

    @builtins.property
    @jsii.member(jsii_name="authCodeInput")
    def auth_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUriInput")
    def redirect_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUriInput"))

    @builtins.property
    @jsii.member(jsii_name="authCode")
    def auth_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCode"))

    @auth_code.setter
    def auth_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adaa2769d2a8071d34c9bf95be68e96b2978a049d99d6cd5c2785fe1f33a3911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @redirect_uri.setter
    def redirect_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af63822b7ba72ee19fc42fe1c1088ba3256330c670f29ca1c2cd2e7944652b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9962eb43b93cb827e932b6ffc85811375221d809171f17f5e7a79009bdd88431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec9f53a795a2971e930cd66195fea1d639114bf325af6698ced90b90db9e91b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthRequest")
    def put_oauth_request(
        self,
        *,
        auth_code: typing.Optional[builtins.str] = None,
        redirect_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code AppflowConnectorProfile#auth_code}.
        :param redirect_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redirect_uri AppflowConnectorProfile#redirect_uri}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest(
            auth_code=auth_code, redirect_uri=redirect_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOauthRequest", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetOauthRequest")
    def reset_oauth_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthRequest", []))

    @builtins.property
    @jsii.member(jsii_name="oauthRequest")
    def oauth_request(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference, jsii.get(self, "oauthRequest"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthRequestInput")
    def oauth_request_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest], jsii.get(self, "oauthRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f450a2c41cfa9b0162d12fbe1316343b11fd6fdf7a1a919d1912dc9fbab90480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e007852570ed83a58156e8018b64d3c31e9fe4310c6c2fdf8d745232c02dba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e079a4c705ae40285df666fab9bc488b2402f8e813a8e00c86d8689bde5c75ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095538d5972b48020aea6aef692149f613e56ff3852a1744c3a178376d295a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "honeycode": "honeycode",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "redshift": "redshift",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "snowflake": "snowflake",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        if isinstance(amplitude, dict):
            amplitude = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude(**amplitude)
        if isinstance(custom_connector, dict):
            custom_connector = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector(**custom_connector)
        if isinstance(datadog, dict):
            datadog = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog(**datadog)
        if isinstance(dynatrace, dict):
            dynatrace = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace(**dynatrace)
        if isinstance(google_analytics, dict):
            google_analytics = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics(**google_analytics)
        if isinstance(honeycode, dict):
            honeycode = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode(**honeycode)
        if isinstance(infor_nexus, dict):
            infor_nexus = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus(**infor_nexus)
        if isinstance(marketo, dict):
            marketo = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo(**marketo)
        if isinstance(redshift, dict):
            redshift = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift(**redshift)
        if isinstance(salesforce, dict):
            salesforce = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData(**sapo_data)
        if isinstance(service_now, dict):
            service_now = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow(**service_now)
        if isinstance(singular, dict):
            singular = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular(**singular)
        if isinstance(slack, dict):
            slack = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack(**slack)
        if isinstance(snowflake, dict):
            snowflake = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake(**snowflake)
        if isinstance(trendmicro, dict):
            trendmicro = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro(**trendmicro)
        if isinstance(veeva, dict):
            veeva = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva(**veeva)
        if isinstance(zendesk, dict):
            zendesk = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be40e378e74a6ef1c4d0b48e580299be5b2b99179087012959978e4f82f72a16)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument honeycode", value=honeycode, expected_type=type_hints["honeycode"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
            check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amplitude is not None:
            self._values["amplitude"] = amplitude
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if datadog is not None:
            self._values["datadog"] = datadog
        if dynatrace is not None:
            self._values["dynatrace"] = dynatrace
        if google_analytics is not None:
            self._values["google_analytics"] = google_analytics
        if honeycode is not None:
            self._values["honeycode"] = honeycode
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if redshift is not None:
            self._values["redshift"] = redshift
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if service_now is not None:
            self._values["service_now"] = service_now
        if singular is not None:
            self._values["singular"] = singular
        if slack is not None:
            self._values["slack"] = slack
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude"]:
        '''amplitude block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        '''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude"], result)

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector"], result)

    @builtins.property
    def datadog(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog"]:
        '''datadog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        '''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog"], result)

    @builtins.property
    def dynatrace(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace"]:
        '''dynatrace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        '''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace"], result)

    @builtins.property
    def google_analytics(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics"]:
        '''google_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        '''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics"], result)

    @builtins.property
    def honeycode(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode"]:
        '''honeycode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        '''
        result = self._values.get("honeycode")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode"], result)

    @builtins.property
    def infor_nexus(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus"]:
        '''infor_nexus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        '''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo"], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"], result)

    @builtins.property
    def singular(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"]:
        '''singular block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        '''
        result = self._values.get("singular")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"], result)

    @builtins.property
    def slack(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"]:
        '''slack block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"], result)

    @builtins.property
    def snowflake(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"], result)

    @builtins.property
    def trendmicro(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"]:
        '''trendmicro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        '''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"], result)

    @builtins.property
    def veeva(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"]:
        '''veeva block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        '''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9f90c3e0d311fd52a51536d3284cc8324892ed25ace3c171b060ef678cce6fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96eca5ccb729c57f7a2c129316cf607eb20af56a79a0e2ec6146989c9b159d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "oauth2_properties": "oauth2Properties",
        "profile_properties": "profileProperties",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector:
    def __init__(
        self,
        *,
        oauth2_properties: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties", typing.Dict[builtins.str, typing.Any]]] = None,
        profile_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_properties: oauth2_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_properties AppflowConnectorProfile#oauth2_properties}
        :param profile_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#profile_properties AppflowConnectorProfile#profile_properties}.
        '''
        if isinstance(oauth2_properties, dict):
            oauth2_properties = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties(**oauth2_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c4da38ac8577601d61f1d31dd2ff835822df5441e82f136d3792a6433ce3dd)
            check_type(argname="argument oauth2_properties", value=oauth2_properties, expected_type=type_hints["oauth2_properties"])
            check_type(argname="argument profile_properties", value=profile_properties, expected_type=type_hints["profile_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if oauth2_properties is not None:
            self._values["oauth2_properties"] = oauth2_properties
        if profile_properties is not None:
            self._values["profile_properties"] = profile_properties

    @builtins.property
    def oauth2_properties(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties"]:
        '''oauth2_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_properties AppflowConnectorProfile#oauth2_properties}
        '''
        result = self._values.get("oauth2_properties")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties"], result)

    @builtins.property
    def profile_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#profile_properties AppflowConnectorProfile#profile_properties}.'''
        result = self._values.get("profile_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties",
    jsii_struct_bases=[],
    name_mapping={
        "oauth2_grant_type": "oauth2GrantType",
        "token_url": "tokenUrl",
        "token_url_custom_properties": "tokenUrlCustomProperties",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties:
    def __init__(
        self,
        *,
        oauth2_grant_type: builtins.str,
        token_url: builtins.str,
        token_url_custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        :param token_url_custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url_custom_properties AppflowConnectorProfile#token_url_custom_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c205fc9fa836e1e496293d7d5c1d18ddf358ac26b6d2ad18b06905f555b6980)
            check_type(argname="argument oauth2_grant_type", value=oauth2_grant_type, expected_type=type_hints["oauth2_grant_type"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            check_type(argname="argument token_url_custom_properties", value=token_url_custom_properties, expected_type=type_hints["token_url_custom_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth2_grant_type": oauth2_grant_type,
            "token_url": token_url,
        }
        if token_url_custom_properties is not None:
            self._values["token_url_custom_properties"] = token_url_custom_properties

    @builtins.property
    def oauth2_grant_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.'''
        result = self._values.get("oauth2_grant_type")
        assert result is not None, "Required property 'oauth2_grant_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.'''
        result = self._values.get("token_url")
        assert result is not None, "Required property 'token_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_url_custom_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url_custom_properties AppflowConnectorProfile#token_url_custom_properties}.'''
        result = self._values.get("token_url_custom_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4146944aee6e125625d6ba689a23a47343bcf62a7a568d12bb1995b681f8e779)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTokenUrlCustomProperties")
    def reset_token_url_custom_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenUrlCustomProperties", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantTypeInput")
    def oauth2_grant_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2GrantTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlCustomPropertiesInput")
    def token_url_custom_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tokenUrlCustomPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlInput")
    def token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2GrantType")
    def oauth2_grant_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2GrantType"))

    @oauth2_grant_type.setter
    def oauth2_grant_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98bb50d947a269af83d36a8f809693e4b7fcf0fe4e65c6f9a73c00f66b04428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2GrantType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d14a7513cecbc701816ba244d1ae7e590799063be0d93691817c64fd73ab06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrlCustomProperties")
    def token_url_custom_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tokenUrlCustomProperties"))

    @token_url_custom_properties.setter
    def token_url_custom_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1334dcab335b41d222919daf951621e1dfc1ab358b5cb80c73ba65e0c135ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrlCustomProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a501589eb460dd966ab02a8cbf4c4c8f8f591061192af9a18f67486e0541924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90da0bbc570a68c152cc10e20e1acfce7c85f6a5241084fe0a63f8a7a904b255)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauth2Properties")
    def put_oauth2_properties(
        self,
        *,
        oauth2_grant_type: builtins.str,
        token_url: builtins.str,
        token_url_custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_grant_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_grant_type AppflowConnectorProfile#oauth2_grant_type}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        :param token_url_custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url_custom_properties AppflowConnectorProfile#token_url_custom_properties}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties(
            oauth2_grant_type=oauth2_grant_type,
            token_url=token_url,
            token_url_custom_properties=token_url_custom_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2Properties", [value]))

    @jsii.member(jsii_name="resetOauth2Properties")
    def reset_oauth2_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2Properties", []))

    @jsii.member(jsii_name="resetProfileProperties")
    def reset_profile_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileProperties", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2Properties")
    def oauth2_properties(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference, jsii.get(self, "oauth2Properties"))

    @builtins.property
    @jsii.member(jsii_name="oauth2PropertiesInput")
    def oauth2_properties_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties], jsii.get(self, "oauth2PropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="profilePropertiesInput")
    def profile_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "profilePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="profileProperties")
    def profile_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "profileProperties"))

    @profile_properties.setter
    def profile_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872bac9ccce9e8c8d025e736c503246e1d668f53ebf48c3da4daec6a797402b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3da34dc7a64832d073adb831318f592dec1330ff81c44c67fd063e5951413d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84cc8a5f4fc82fcbb0df96b7c434c31088caa096974a857a654f879fa7a20db)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c85b4bc2d265d1f629c91f4ae25899be2c9d5c71a35dc62fdefa07931a61c48f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823332a9dc6e35a4d0f4517ed949bd55a3f7f714a8d9585f480f3b08a6fdf16e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d298d7be5f8ffd75e4da095f31229671a71e2e33951fcb0a30eb51610f08f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafa46462c63ce8c851a38330d38fc9f2783cb43e3f8e39da68100c8b2bd6e32)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__586ec572611ee845ced93816505c5b00c9ccbbfdf3b9c60a2a3a8422a91de382)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1463c189daf4615feefbaa10262896ffcd6951ea77d1b8b3036b8675b28fca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117bfd3d92c6cab80996a563aab2ce791ebb7adffb21f6b3b150a39daaa4fa3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69dbe9d98418a275ba46c56a9e8437a08dc3ceddd0c16f3fa1ac73e27b629776)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51676257789c6b7830254e7dac37fba5c12b6331c837c85e147c7f2dff44cb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eefbe88796b3985f1890176beeb13dfda943cb9abec642b86149a98372407818)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353472a9b6b8089f1d9e5c231c032d01bc5a348a10caa3e255519650f94822e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9656519824c3aeb802b60f2e466a70e5a548cb152b4fb4c9a9cb8baf348ac855)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f38d18a8e7106b691c58e6ff2ea5c3074b7da581fe000157b1532e3eb1c3713)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d258033b000d43dea771ad143e463d00652d43c711da70a10f287b7017530a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a54fa291b45527dd4d5bccb8e4d975d91463f38049cb98543bfe8e2c94e79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af32d0bce6a7f0884bf4a59c2df101770332d194a85870650b0c04aeea6ec69c)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__151a516ba0376742a532e6ee1ed76031dc172f634bbff14a9b6d65a8a3f0a508)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cc7379bac41602f1620810cf1fa5e9747e8cdb0e677a04a414a4fb01218590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5316eab0f9e2bf43d3fdb4aec8f2304dd87f427fbf289ddeb831e09467b738d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97df88eb853fa9a1a3f3aa74fb7fa0bbb76fce6e1510027059fa58d15277042d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmplitude")
    def put_amplitude(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude()

        return typing.cast(None, jsii.invoke(self, "putAmplitude", [value]))

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        oauth2_properties: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties, typing.Dict[builtins.str, typing.Any]]] = None,
        profile_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param oauth2_properties: oauth2_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth2_properties AppflowConnectorProfile#oauth2_properties}
        :param profile_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#profile_properties AppflowConnectorProfile#profile_properties}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector(
            oauth2_properties=oauth2_properties, profile_properties=profile_properties
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putDatadog")
    def put_datadog(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putDatadog", [value]))

    @jsii.member(jsii_name="putDynatrace")
    def put_dynatrace(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putDynatrace", [value]))

    @jsii.member(jsii_name="putGoogleAnalytics")
    def put_google_analytics(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics()

        return typing.cast(None, jsii.invoke(self, "putGoogleAnalytics", [value]))

    @jsii.member(jsii_name="putHoneycode")
    def put_honeycode(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode()

        return typing.cast(None, jsii.invoke(self, "putHoneycode", [value]))

    @jsii.member(jsii_name="putInforNexus")
    def put_infor_nexus(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putInforNexus", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        *,
        bucket_name: builtins.str,
        role_arn: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        data_api_role_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        database_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#role_arn AppflowConnectorProfile#role_arn}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param cluster_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#cluster_identifier AppflowConnectorProfile#cluster_identifier}.
        :param data_api_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#data_api_role_arn AppflowConnectorProfile#data_api_role_arn}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#database_name AppflowConnectorProfile#database_name}.
        :param database_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#database_url AppflowConnectorProfile#database_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift(
            bucket_name=bucket_name,
            role_arn=role_arn,
            bucket_prefix=bucket_prefix,
            cluster_identifier=cluster_identifier,
            data_api_role_arn=data_api_role_arn,
            database_name=database_name,
            database_url=database_url,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        instance_url: typing.Optional[builtins.str] = None,
        is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_privatelink_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        :param is_sandbox_environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#is_sandbox_environment AppflowConnectorProfile#is_sandbox_environment}.
        :param use_privatelink_for_metadata_and_authorization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#use_privatelink_for_metadata_and_authorization AppflowConnectorProfile#use_privatelink_for_metadata_and_authorization}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce(
            instance_url=instance_url,
            is_sandbox_environment=is_sandbox_environment,
            use_privatelink_for_metadata_and_authorization=use_privatelink_for_metadata_and_authorization,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        application_host_url: builtins.str,
        application_service_path: builtins.str,
        client_number: builtins.str,
        port_number: jsii.Number,
        logon_language: typing.Optional[builtins.str] = None,
        oauth_properties: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_host_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_host_url AppflowConnectorProfile#application_host_url}.
        :param application_service_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_service_path AppflowConnectorProfile#application_service_path}.
        :param client_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_number AppflowConnectorProfile#client_number}.
        :param port_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#port_number AppflowConnectorProfile#port_number}.
        :param logon_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#logon_language AppflowConnectorProfile#logon_language}.
        :param oauth_properties: oauth_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_properties AppflowConnectorProfile#oauth_properties}
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData(
            application_host_url=application_host_url,
            application_service_path=application_service_path,
            client_number=client_number,
            port_number=port_number,
            logon_language=logon_language,
            oauth_properties=oauth_properties,
            private_link_service_name=private_link_service_name,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSingular")
    def put_singular(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular()

        return typing.cast(None, jsii.invoke(self, "putSingular", [value]))

    @jsii.member(jsii_name="putSlack")
    def put_slack(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putSlack", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(
        self,
        *,
        bucket_name: builtins.str,
        stage: builtins.str,
        warehouse: builtins.str,
        account_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param stage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#stage AppflowConnectorProfile#stage}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#warehouse AppflowConnectorProfile#warehouse}.
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#account_name AppflowConnectorProfile#account_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake(
            bucket_name=bucket_name,
            stage=stage,
            warehouse=warehouse,
            account_name=account_name,
            bucket_prefix=bucket_prefix,
            private_link_service_name=private_link_service_name,
            region=region,
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putTrendmicro")
    def put_trendmicro(self) -> None:
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro()

        return typing.cast(None, jsii.invoke(self, "putTrendmicro", [value]))

    @jsii.member(jsii_name="putVeeva")
    def put_veeva(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putVeeva", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk(
            instance_url=instance_url
        )

        return typing.cast(None, jsii.invoke(self, "putZendesk", [value]))

    @jsii.member(jsii_name="resetAmplitude")
    def reset_amplitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmplitude", []))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetDatadog")
    def reset_datadog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadog", []))

    @jsii.member(jsii_name="resetDynatrace")
    def reset_dynatrace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynatrace", []))

    @jsii.member(jsii_name="resetGoogleAnalytics")
    def reset_google_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleAnalytics", []))

    @jsii.member(jsii_name="resetHoneycode")
    def reset_honeycode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoneycode", []))

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSingular")
    def reset_singular(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingular", []))

    @jsii.member(jsii_name="resetSlack")
    def reset_slack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlack", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetTrendmicro")
    def reset_trendmicro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrendmicro", []))

    @jsii.member(jsii_name="resetVeeva")
    def reset_veeva(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVeeva", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="amplitude")
    def amplitude(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference, jsii.get(self, "amplitude"))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference, jsii.get(self, "datadog"))

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference, jsii.get(self, "dynatrace"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference, jsii.get(self, "googleAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="honeycode")
    def honeycode(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference, jsii.get(self, "honeycode"))

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference, jsii.get(self, "inforNexus"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference", jsii.get(self, "singular"))

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference", jsii.get(self, "slack"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference", jsii.get(self, "trendmicro"))

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference", jsii.get(self, "veeva"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference":
        return typing.cast("AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="honeycodeInput")
    def honeycode_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode], jsii.get(self, "honeycodeInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular"], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack"], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro"], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva"], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"]:
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da05ea775832c54533461e03186db702117abc68dba2f13fdb41305e621e1eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "role_arn": "roleArn",
        "bucket_prefix": "bucketPrefix",
        "cluster_identifier": "clusterIdentifier",
        "data_api_role_arn": "dataApiRoleArn",
        "database_name": "databaseName",
        "database_url": "databaseUrl",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        role_arn: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        data_api_role_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        database_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#role_arn AppflowConnectorProfile#role_arn}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param cluster_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#cluster_identifier AppflowConnectorProfile#cluster_identifier}.
        :param data_api_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#data_api_role_arn AppflowConnectorProfile#data_api_role_arn}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#database_name AppflowConnectorProfile#database_name}.
        :param database_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#database_url AppflowConnectorProfile#database_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53171a920fc9f383ab550cd23accad63fc55b99f7c17f57e073980e2df945df3)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument data_api_role_arn", value=data_api_role_arn, expected_type=type_hints["data_api_role_arn"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument database_url", value=database_url, expected_type=type_hints["database_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "role_arn": role_arn,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if data_api_role_arn is not None:
            self._values["data_api_role_arn"] = data_api_role_arn
        if database_name is not None:
            self._values["database_name"] = database_name
        if database_url is not None:
            self._values["database_url"] = database_url

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#role_arn AppflowConnectorProfile#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#cluster_identifier AppflowConnectorProfile#cluster_identifier}.'''
        result = self._values.get("cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_api_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#data_api_role_arn AppflowConnectorProfile#data_api_role_arn}.'''
        result = self._values.get("data_api_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#database_name AppflowConnectorProfile#database_name}.'''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#database_url AppflowConnectorProfile#database_url}.'''
        result = self._values.get("database_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1f86ead776ec5ace561e52b48028faf900eb6128f7de3c23241c207c1d7cdaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetClusterIdentifier")
    def reset_cluster_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIdentifier", []))

    @jsii.member(jsii_name="resetDataApiRoleArn")
    def reset_data_api_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataApiRoleArn", []))

    @jsii.member(jsii_name="resetDatabaseName")
    def reset_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseName", []))

    @jsii.member(jsii_name="resetDatabaseUrl")
    def reset_database_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseUrl", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifierInput")
    def cluster_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="dataApiRoleArnInput")
    def data_api_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataApiRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseUrlInput")
    def database_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980e2e913684e29fb43e05f9181323bdb93047d2ed03e53a668f43cdeefe6fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8b67bca71f22ab7098137b32c59542f6476aba21f6a376cb23f4e428a10f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @cluster_identifier.setter
    def cluster_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119a0362a3b9a221af6cf0231bf22bf1b784540a42a6a7bdb121590a09d439e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataApiRoleArn")
    def data_api_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataApiRoleArn"))

    @data_api_role_arn.setter
    def data_api_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de361a99fcfc9c558d06409aa85ccf2a32f1d49a3f85fe2527a82d3e067e309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataApiRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d5b993e7f0f2d92d2d8cf62dda4cdc8ac6739acb76e218393f6fab7e3dad95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseUrl")
    def database_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseUrl"))

    @database_url.setter
    def database_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e157859fde45865bc27e43d41b293198322358b5d54ddc658a1f449430a4e53a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4016c6e214bca9f93db18634f88cd85c2f2ba5adab1d2bea6a09a93a086a1757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb177c6f60d7769d437938246d278fd7e43df8a8ad74e5405b96402340e59be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "instance_url": "instanceUrl",
        "is_sandbox_environment": "isSandboxEnvironment",
        "use_privatelink_for_metadata_and_authorization": "usePrivatelinkForMetadataAndAuthorization",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce:
    def __init__(
        self,
        *,
        instance_url: typing.Optional[builtins.str] = None,
        is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_privatelink_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        :param is_sandbox_environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#is_sandbox_environment AppflowConnectorProfile#is_sandbox_environment}.
        :param use_privatelink_for_metadata_and_authorization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#use_privatelink_for_metadata_and_authorization AppflowConnectorProfile#use_privatelink_for_metadata_and_authorization}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354bad9bb2e0e4db9bc12b7e02e34fe3a34c92871294761275f53edb3967ced1)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            check_type(argname="argument is_sandbox_environment", value=is_sandbox_environment, expected_type=type_hints["is_sandbox_environment"])
            check_type(argname="argument use_privatelink_for_metadata_and_authorization", value=use_privatelink_for_metadata_and_authorization, expected_type=type_hints["use_privatelink_for_metadata_and_authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_url is not None:
            self._values["instance_url"] = instance_url
        if is_sandbox_environment is not None:
            self._values["is_sandbox_environment"] = is_sandbox_environment
        if use_privatelink_for_metadata_and_authorization is not None:
            self._values["use_privatelink_for_metadata_and_authorization"] = use_privatelink_for_metadata_and_authorization

    @builtins.property
    def instance_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_sandbox_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#is_sandbox_environment AppflowConnectorProfile#is_sandbox_environment}.'''
        result = self._values.get("is_sandbox_environment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_privatelink_for_metadata_and_authorization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#use_privatelink_for_metadata_and_authorization AppflowConnectorProfile#use_privatelink_for_metadata_and_authorization}.'''
        result = self._values.get("use_privatelink_for_metadata_and_authorization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09ea5895dd3e24fb056df2e45d4f2efce96399747d1b6b1ee18d772d03d15d22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceUrl")
    def reset_instance_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceUrl", []))

    @jsii.member(jsii_name="resetIsSandboxEnvironment")
    def reset_is_sandbox_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSandboxEnvironment", []))

    @jsii.member(jsii_name="resetUsePrivatelinkForMetadataAndAuthorization")
    def reset_use_privatelink_for_metadata_and_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsePrivatelinkForMetadataAndAuthorization", []))

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="isSandboxEnvironmentInput")
    def is_sandbox_environment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSandboxEnvironmentInput"))

    @builtins.property
    @jsii.member(jsii_name="usePrivatelinkForMetadataAndAuthorizationInput")
    def use_privatelink_for_metadata_and_authorization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "usePrivatelinkForMetadataAndAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f60faadf1caf9c9c1cf17107d6cd6fdec6b4989a7e23da923da66a50ad6eb00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSandboxEnvironment")
    def is_sandbox_environment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSandboxEnvironment"))

    @is_sandbox_environment.setter
    def is_sandbox_environment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8a4c6454d99917c3e29ceb5ea34260f220a7eceb5229678f2cc6b49da106cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSandboxEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usePrivatelinkForMetadataAndAuthorization")
    def use_privatelink_for_metadata_and_authorization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "usePrivatelinkForMetadataAndAuthorization"))

    @use_privatelink_for_metadata_and_authorization.setter
    def use_privatelink_for_metadata_and_authorization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3495724532f7eba8bd549634c54ded1bc86cac716d41799e2042475f45399ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usePrivatelinkForMetadataAndAuthorization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252e74a3627afd2f955d7ac4e5763ec5c6eb65a71ffbfc3220abd6cecc66cdf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "application_host_url": "applicationHostUrl",
        "application_service_path": "applicationServicePath",
        "client_number": "clientNumber",
        "port_number": "portNumber",
        "logon_language": "logonLanguage",
        "oauth_properties": "oauthProperties",
        "private_link_service_name": "privateLinkServiceName",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData:
    def __init__(
        self,
        *,
        application_host_url: builtins.str,
        application_service_path: builtins.str,
        client_number: builtins.str,
        port_number: jsii.Number,
        logon_language: typing.Optional[builtins.str] = None,
        oauth_properties: typing.Optional[typing.Union["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_host_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_host_url AppflowConnectorProfile#application_host_url}.
        :param application_service_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_service_path AppflowConnectorProfile#application_service_path}.
        :param client_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_number AppflowConnectorProfile#client_number}.
        :param port_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#port_number AppflowConnectorProfile#port_number}.
        :param logon_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#logon_language AppflowConnectorProfile#logon_language}.
        :param oauth_properties: oauth_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_properties AppflowConnectorProfile#oauth_properties}
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        '''
        if isinstance(oauth_properties, dict):
            oauth_properties = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties(**oauth_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ebfb642890d7f55577ea558cac0b4bf56223bcb4329dc31ddba12b01205a4e)
            check_type(argname="argument application_host_url", value=application_host_url, expected_type=type_hints["application_host_url"])
            check_type(argname="argument application_service_path", value=application_service_path, expected_type=type_hints["application_service_path"])
            check_type(argname="argument client_number", value=client_number, expected_type=type_hints["client_number"])
            check_type(argname="argument port_number", value=port_number, expected_type=type_hints["port_number"])
            check_type(argname="argument logon_language", value=logon_language, expected_type=type_hints["logon_language"])
            check_type(argname="argument oauth_properties", value=oauth_properties, expected_type=type_hints["oauth_properties"])
            check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_host_url": application_host_url,
            "application_service_path": application_service_path,
            "client_number": client_number,
            "port_number": port_number,
        }
        if logon_language is not None:
            self._values["logon_language"] = logon_language
        if oauth_properties is not None:
            self._values["oauth_properties"] = oauth_properties
        if private_link_service_name is not None:
            self._values["private_link_service_name"] = private_link_service_name

    @builtins.property
    def application_host_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_host_url AppflowConnectorProfile#application_host_url}.'''
        result = self._values.get("application_host_url")
        assert result is not None, "Required property 'application_host_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_service_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#application_service_path AppflowConnectorProfile#application_service_path}.'''
        result = self._values.get("application_service_path")
        assert result is not None, "Required property 'application_service_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_number(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#client_number AppflowConnectorProfile#client_number}.'''
        result = self._values.get("client_number")
        assert result is not None, "Required property 'client_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port_number(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#port_number AppflowConnectorProfile#port_number}.'''
        result = self._values.get("port_number")
        assert result is not None, "Required property 'port_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def logon_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#logon_language AppflowConnectorProfile#logon_language}.'''
        result = self._values.get("logon_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_properties(
        self,
    ) -> typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties"]:
        '''oauth_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_properties AppflowConnectorProfile#oauth_properties}
        '''
        result = self._values.get("oauth_properties")
        return typing.cast(typing.Optional["AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties"], result)

    @builtins.property
    def private_link_service_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.'''
        result = self._values.get("private_link_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties",
    jsii_struct_bases=[],
    name_mapping={
        "auth_code_url": "authCodeUrl",
        "oauth_scopes": "oauthScopes",
        "token_url": "tokenUrl",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties:
    def __init__(
        self,
        *,
        auth_code_url: builtins.str,
        oauth_scopes: typing.Sequence[builtins.str],
        token_url: builtins.str,
    ) -> None:
        '''
        :param auth_code_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code_url AppflowConnectorProfile#auth_code_url}.
        :param oauth_scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_scopes AppflowConnectorProfile#oauth_scopes}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a851c7ce629ca694e175df21b48b94966842d34a4f49cb257a9b2a90389102d7)
            check_type(argname="argument auth_code_url", value=auth_code_url, expected_type=type_hints["auth_code_url"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_code_url": auth_code_url,
            "oauth_scopes": oauth_scopes,
            "token_url": token_url,
        }

    @builtins.property
    def auth_code_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code_url AppflowConnectorProfile#auth_code_url}.'''
        result = self._values.get("auth_code_url")
        assert result is not None, "Required property 'auth_code_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_scopes AppflowConnectorProfile#oauth_scopes}.'''
        result = self._values.get("oauth_scopes")
        assert result is not None, "Required property 'oauth_scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def token_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.'''
        result = self._values.get("token_url")
        assert result is not None, "Required property 'token_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59fd257b66af32c9bd980b014b6359ad6ca5f71de95624b7fafb6c841b96175d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="authCodeUrlInput")
    def auth_code_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authCodeUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlInput")
    def token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="authCodeUrl")
    def auth_code_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authCodeUrl"))

    @auth_code_url.setter
    def auth_code_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b7a30147c9a6d4842e86fed14a297c6cb021987b7b899ac3a24a843145fa63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authCodeUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35a1e2f038c6515345c431538c9fbf1d068d556de7f354c15700fbf41fadad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728ddd6a061ff0711ac60e5d261af6801bd0e907964efdfb7a5419c51c6b20eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65724943e46e05e7eea8bc06d4752b6e7515edc3a6ee03055d82de9ded059f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ee6ebac5c0cf06d46a67624ee3a1fea1b9ceac5d4c9c893d87b6d2fb79e676d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOauthProperties")
    def put_oauth_properties(
        self,
        *,
        auth_code_url: builtins.str,
        oauth_scopes: typing.Sequence[builtins.str],
        token_url: builtins.str,
    ) -> None:
        '''
        :param auth_code_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#auth_code_url AppflowConnectorProfile#auth_code_url}.
        :param oauth_scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#oauth_scopes AppflowConnectorProfile#oauth_scopes}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#token_url AppflowConnectorProfile#token_url}.
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties(
            auth_code_url=auth_code_url, oauth_scopes=oauth_scopes, token_url=token_url
        )

        return typing.cast(None, jsii.invoke(self, "putOauthProperties", [value]))

    @jsii.member(jsii_name="resetLogonLanguage")
    def reset_logon_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogonLanguage", []))

    @jsii.member(jsii_name="resetOauthProperties")
    def reset_oauth_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthProperties", []))

    @jsii.member(jsii_name="resetPrivateLinkServiceName")
    def reset_private_link_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="oauthProperties")
    def oauth_properties(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference, jsii.get(self, "oauthProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationHostUrlInput")
    def application_host_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationHostUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationServicePathInput")
    def application_service_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationServicePathInput"))

    @builtins.property
    @jsii.member(jsii_name="clientNumberInput")
    def client_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="logonLanguageInput")
    def logon_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logonLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthPropertiesInput")
    def oauth_properties_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties], jsii.get(self, "oauthPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="portNumberInput")
    def port_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceNameInput")
    def private_link_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateLinkServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationHostUrl")
    def application_host_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationHostUrl"))

    @application_host_url.setter
    def application_host_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2baba90665604934b75b2b0d79f553e225e4a436a5053319007e6e7e8ac877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationHostUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationServicePath")
    def application_service_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationServicePath"))

    @application_service_path.setter
    def application_service_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f240b192d96e42038e145941dd58416b5ce1e87a2898d85949a4cf23288e7514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationServicePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientNumber")
    def client_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientNumber"))

    @client_number.setter
    def client_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a80d3e5b5d514e1ba2bd2f8a705e7fd3b513bf57a67881152f3ff7e9ebe582e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logonLanguage")
    def logon_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logonLanguage"))

    @logon_language.setter
    def logon_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af4055c55f00e69556e6bc3b75772c02fec89c7ed059ecf3a7fb6218451f501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logonLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portNumber")
    def port_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portNumber"))

    @port_number.setter
    def port_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54c77c99478407274bcc3a905b8eb106198bdd5f5ac16dc995f2863df4b0904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceName")
    def private_link_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateLinkServiceName"))

    @private_link_service_name.setter
    def private_link_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a71821eb95d9b193f8d4403786d81714cf8fe8f36d5da5327fdba7d4b942ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8751ddb5cd9d40da5cb2834faef84a7dfcc37d6053ca262d04c3a57ed6a7b713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6517c7fd52fb09c4e8e76e1a87d9211901a862c38edfda6c14b31f47cad986d6)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2013bde61bcd28c9fc577aae6c6a406c829a257076be558676ae73c4f9aebdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18af9eedc276831f0da48023cd33ade73ee5719cb509a9da47c1264a4c78d393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3681db72c2fb615f6096b78a40992774891f75dfcb5f757679095fb5ad7302b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5e5eaec6b7b33f4ed76382bec6f2fcb82e45b582d61cfb4f8dd2a20da679576)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e329e1e8d6aa370bc14cdf199d3555658b7923a24e0e8de13579b4bbcfe61cb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11ed2a060d0e2a13da4c5265b1e4bd853b0bd24ae8b0fb4838d64a99d18993d)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91d24065be4dcf533fe7899c998b2dfb01d70a3420c764561498deb36f645a50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6db88df485de09444d04c148152a5b1b60751f761bd3c6ead6ab5e1b234af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aac7c07e22f9513e4b38624a05a818d91a5d4e9b8d8344abca9e1e63943ea08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "stage": "stage",
        "warehouse": "warehouse",
        "account_name": "accountName",
        "bucket_prefix": "bucketPrefix",
        "private_link_service_name": "privateLinkServiceName",
        "region": "region",
    },
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        stage: builtins.str,
        warehouse: builtins.str,
        account_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        private_link_service_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.
        :param stage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#stage AppflowConnectorProfile#stage}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#warehouse AppflowConnectorProfile#warehouse}.
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#account_name AppflowConnectorProfile#account_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.
        :param private_link_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fb3f6fca3a5053e7ff111409eb0671d01a6bdab8e99064bb4abcce6192b1c2)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "stage": stage,
            "warehouse": warehouse,
        }
        if account_name is not None:
            self._values["account_name"] = account_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if private_link_service_name is not None:
            self._values["private_link_service_name"] = private_link_service_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_name AppflowConnectorProfile#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#stage AppflowConnectorProfile#stage}.'''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def warehouse(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#warehouse AppflowConnectorProfile#warehouse}.'''
        result = self._values.get("warehouse")
        assert result is not None, "Required property 'warehouse' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#account_name AppflowConnectorProfile#account_name}.'''
        result = self._values.get("account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#bucket_prefix AppflowConnectorProfile#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_service_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#private_link_service_name AppflowConnectorProfile#private_link_service_name}.'''
        result = self._values.get("private_link_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#region AppflowConnectorProfile#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05942b5747ec420d7b43ddfd00c71675439795eef3b1ed33e5e2f902f12ac9b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountName")
    def reset_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetPrivateLinkServiceName")
    def reset_private_link_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkServiceName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceNameInput")
    def private_link_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateLinkServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="stageInput")
    def stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseInput")
    def warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b2c93a61d5d3b28cc50da6e6b4138ea568879ac8ced7df6662116eba9390be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8959dfe3b6b8ebedac2e37a4d07eaa93dee02d0a774ca7ba3aebbf76c5db39c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c46032748ebf23e88e08a98a67fe8a0fe24554f6877b4341e3e1a304da959b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateLinkServiceName")
    def private_link_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateLinkServiceName"))

    @private_link_service_name.setter
    def private_link_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7dd6149773d34cf97e71d0d7f95e4860a86ed0766ddb187f6ab8e91d2ee3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842c89725d4623c2e6892bee344a3ccca1444386debc4d86dc8f55a84282186c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5d995e2fc39bca6e81b7461a09db8b41785a5bbe6fdb4d500229e4f855b1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouse"))

    @warehouse.setter
    def warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d98dbbd9ba1fac50af9b22de408038ca9414145586a182d3da0b5a06de1e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be61d6bbfa733001d62710b790f80b937064910a8841b834b0d716db17aba7cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bece5b74a7c41750c35b40e8ae11a1356dbd5f616c26f72357eead45aa3d389)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5309d54d0c8fef6ccd2c09977bc046e87b6ae50eebe42170a1887de44c656ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce1028e3986595573bf18c25af875ef881c4475de3618c55359bfc9ff1c98c7)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e79cb6dcdb59f47e732588cf230927dbe1b6f6bc266c5ac8b5e5f08a02f418a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf10cff61f4703bb7feb9769de83731489c8344614bce821022a7657a727b60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14dd24709acb3659c04f28e009b972851dbcec459d388f3ea67c1bbec07b4ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk",
    jsii_struct_bases=[],
    name_mapping={"instance_url": "instanceUrl"},
)
class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk:
    def __init__(self, *, instance_url: builtins.str) -> None:
        '''
        :param instance_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37aacca09f0f6337ae7c7b418858fcd52accd1ca2bfd692ea21fce7511b8268b)
            check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_url": instance_url,
        }

    @builtins.property
    def instance_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#instance_url AppflowConnectorProfile#instance_url}.'''
        result = self._values.get("instance_url")
        assert result is not None, "Required property 'instance_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87e61d0b7c94605e27dc6012c14ab5474e79b9ad0fd275c87080c9f5028f3501)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceUrlInput")
    def instance_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUrl")
    def instance_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceUrl"))

    @instance_url.setter
    def instance_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354ed2efacaa854a9cd1c3c15a047c27a1a07426f3388635ca14b210d14b551d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7fe7744b96fa6c9c98a5b6a9b3541450c97f431bed39e11c680e2dfe71f5438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowConnectorProfileConnectorProfileConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowConnectorProfile.AppflowConnectorProfileConnectorProfileConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__837dc4b4a25ad7d86284e378f8452e16e3bf9c3f07b4272558572e0e978e5887)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConnectorProfileCredentials")
    def put_connector_profile_credentials(
        self,
        *,
        amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular, typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack, typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials(
            amplitude=amplitude,
            custom_connector=custom_connector,
            datadog=datadog,
            dynatrace=dynatrace,
            google_analytics=google_analytics,
            honeycode=honeycode,
            infor_nexus=infor_nexus,
            marketo=marketo,
            redshift=redshift,
            salesforce=salesforce,
            sapo_data=sapo_data,
            service_now=service_now,
            singular=singular,
            slack=slack,
            snowflake=snowflake,
            trendmicro=trendmicro,
            veeva=veeva,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectorProfileCredentials", [value]))

    @jsii.member(jsii_name="putConnectorProfileProperties")
    def put_connector_profile_properties(
        self,
        *,
        amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular, typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack, typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#amplitude AppflowConnectorProfile#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#custom_connector AppflowConnectorProfile#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#datadog AppflowConnectorProfile#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#dynatrace AppflowConnectorProfile#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#google_analytics AppflowConnectorProfile#google_analytics}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#honeycode AppflowConnectorProfile#honeycode}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#infor_nexus AppflowConnectorProfile#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#marketo AppflowConnectorProfile#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#redshift AppflowConnectorProfile#redshift}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#salesforce AppflowConnectorProfile#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#sapo_data AppflowConnectorProfile#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#service_now AppflowConnectorProfile#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#singular AppflowConnectorProfile#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#slack AppflowConnectorProfile#slack}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#snowflake AppflowConnectorProfile#snowflake}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#trendmicro AppflowConnectorProfile#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#veeva AppflowConnectorProfile#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_connector_profile#zendesk AppflowConnectorProfile#zendesk}
        '''
        value = AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties(
            amplitude=amplitude,
            custom_connector=custom_connector,
            datadog=datadog,
            dynatrace=dynatrace,
            google_analytics=google_analytics,
            honeycode=honeycode,
            infor_nexus=infor_nexus,
            marketo=marketo,
            redshift=redshift,
            salesforce=salesforce,
            sapo_data=sapo_data,
            service_now=service_now,
            singular=singular,
            slack=slack,
            snowflake=snowflake,
            trendmicro=trendmicro,
            veeva=veeva,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectorProfileProperties", [value]))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileCredentials")
    def connector_profile_credentials(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference, jsii.get(self, "connectorProfileCredentials"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileProperties")
    def connector_profile_properties(
        self,
    ) -> AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference:
        return typing.cast(AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference, jsii.get(self, "connectorProfileProperties"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileCredentialsInput")
    def connector_profile_credentials_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials], jsii.get(self, "connectorProfileCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfilePropertiesInput")
    def connector_profile_properties_input(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties], jsii.get(self, "connectorProfilePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowConnectorProfileConnectorProfileConfig]:
        return typing.cast(typing.Optional[AppflowConnectorProfileConnectorProfileConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowConnectorProfileConnectorProfileConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934566f58a8b0f97ccceb0f9d94f6340bbc4bc89b99b8334db62db151591edfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppflowConnectorProfile",
    "AppflowConnectorProfileConfig",
    "AppflowConnectorProfileConnectorProfileConfig",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitudeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKeyOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasicOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustomOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadogOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatraceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexusOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshiftOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentialsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNowOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingularOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflakeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicroOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeevaOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequestOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitudeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2PropertiesOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadogOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatraceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalyticsOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycodeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexusOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketoOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshiftOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforceOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthPropertiesOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNowOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingularOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlackOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflakeOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicroOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeevaOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk",
    "AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendeskOutputReference",
    "AppflowConnectorProfileConnectorProfileConfigOutputReference",
]

publication.publish()

def _typecheckingstub__b7c77efecfffbe5deda621a7d10bccb2a5097535fbc657f41fbde51cdedcb22b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_mode: builtins.str,
    connector_profile_config: typing.Union[AppflowConnectorProfileConnectorProfileConfig, typing.Dict[builtins.str, typing.Any]],
    connector_type: builtins.str,
    name: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2d235022e0efbf8b108e299261f0f39b7dec4fde2d34786ba23070f84a7ae6b9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f224e49620571185f2b85a19052a498a9b1eba9f7d42ac25d0e6523f29c9d056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244928185646bbc8c88276a568b77f990f4b4eec74868546cbd1467d3a5ff372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f948850b47008a78d7c68008d7a9599f848ee41ef257eb1959c79a6b71e6b34f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc4f38c06faec1602cd39334a7509f0acbfad38c99fc98b6b625d540cdc3223(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f24832a546999b478fd8dca734de8976b76ba125cb899e39b02fea5a1a12bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fdb49881b6dc6fd2b4933edfbd6e78b89a6dfb1bc3595c8c8497d36e5bfb69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f7c04e014af53c5237f67178ad97e09f417a392ce887babf8ce0a2c49682ea(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_mode: builtins.str,
    connector_profile_config: typing.Union[AppflowConnectorProfileConnectorProfileConfig, typing.Dict[builtins.str, typing.Any]],
    connector_type: builtins.str,
    name: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4790a2075e98441b8097180f95be7fa01ab2e6a1b20d9842672e820f2ac987b9(
    *,
    connector_profile_credentials: typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials, typing.Dict[builtins.str, typing.Any]],
    connector_profile_properties: typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c87c137db4ca68ecb27a7b0cf3977a46c1411788faf9873ae1a8a5c9c118c53(
    *,
    amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
    google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
    infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
    veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e750a1c287e345a9cfd066208b9209308c878db9ba3b6d9d0a5c7ed4b2ca948(
    *,
    api_key: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c1d9135285abc916b05769a3bfb65ba6163d228afd08b69286d044539c9225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8915a9e4bed346661b7ad68cba93429492db7164f934926f61c775149b08b48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2810ee98d65ffe107b0b33737a9d211948ddc52ea42c61d5532c92d9cdbf45cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77888663df9c9161637bc65b356f96f33183c972b9ab5926bba79c1677375394(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsAmplitude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120788d3f077a5da35210469622f1d41b740ab10eaa2a8d80931a804321d4a1d(
    *,
    authentication_type: builtins.str,
    api_key: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey, typing.Dict[builtins.str, typing.Any]]] = None,
    basic: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    custom: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed3491a4a8e3303e2fd26e7aec33ba6f4277c28d7a282537b88e3c48cd7570f(
    *,
    api_key: builtins.str,
    api_secret_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d76ea93bb301b49f4a5840e88964804aa5893b5e7c6f14fa203a6c3d60f7b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33286cf2819fbc4cf3ca5a9c288d596d230e8b5bae2389b7e3ec1aaa6b84307a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ecb930fa2f788c340aed83965aa952b7a333236c1c291a7dfdff2d0165a812(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac060c7ede2a1b811f65c01c5913f8c56d645afca3c16100e7a9c86a2162af0a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorApiKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349b09f29a2922e9dbf95f830174143bdc96e0301e8ec496ba36f343d762a691(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec45a89f307bb92caf322704f3a955a6eea3e01b8220a21b721f7d3f8908625(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbcf0dd85b177dc9f2ba9aa2063edc7223629990340bdea2113cf1b7c3203169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b52f46150969d30cd1862d86fe9df4c8497ac68f913c7f1921500d46621262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503d49223b70a321423cfe8c9667c252da1c06aba62ac8272089df6cae4f01e8(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e865dc3c8db82c257f2b7fe5dda30048e671102d1731c35c2c9326638070f69(
    *,
    custom_authentication_type: builtins.str,
    credentials_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94bff6209670aa5daf4ab730e3a6a57d00832b578ecf29e95e86f828d17456d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c7e38315536d540c2fa014781f6530ee77b90ab4c261c7b44db07ccc3ed0e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195ba4b85e3e47dc35de487e486cbd128ae9b702a7a3cff98935363076eb2858(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29748a7cbf90ca4f89240799079bc13a9ef291c7d502d1e54194d9214dcbf9e(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorCustom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebb51b101dfadb9ca1e3fd5c75123412a091e6242f8ddc7b8e3b2b3c4d10aec(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4792571588aca63a1980a450b5447632da7a65dc83c854205798052070e0a267(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d6cc3166374f9c4ce904ea764b9b2a4d4c22c1917f31f3ab03e12da503d7bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f609522402975593b947b9ac9d1f6e84368fa10c8c7578bf8b4ef6f6358f0d1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da49fadc9103ced71c115a68fa26f8bce0d90b65fdca17e409d83eb138f78281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6eeb191ea5b683d0990ed7507137e4cafa65ca850515ab61e47a1ad94facad(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2OauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61db2621bb0dfa2cef0eea0e5a5aa090ba4727b1618edb96cbbdee084671bde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074c155389b49083139db08ab5c4488129c6bcc81eb39e03c49d1d37f3290408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee82c46c02eb8d2e08bd85343a42a0807d18c9ff44e63b1ab3ca9f797ae7b6f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d8087afbc92651ace2e959f37532e20b3c4b8fb64030aae8513e2ae03bf312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722dc47bc0f83a91e30024e8956768b73343296fb6aa90cd543a5124402873b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548db3cb91a8350b2466e0bc1ffe2751b02c4db83556d17f95b2174cbe0d2f61(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnectorOauth2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6b500f5b832c230c47ab2c3bce432f62b0e1f8721c9f9c32f67f0f2dc38b58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fec2a6b818bdf43c0572d65b41d0c1b0048b4ebd988751735fdc46f7ba322f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e173df80741a3167b9372ddedfef73ab0029141a998050a9416d791a4dffc36a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb368de38e48a08c8f36cbd1189ad61af711b407d7c5d2c575abc0241036b47(
    *,
    api_key: builtins.str,
    application_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7864a7ba6fdb637b1d5da19d228f1ccd906ecee2de8df52725810568571c90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5f91c42f7b32a2e282623a84059b155b5122f9112e69f53a1bdc9d5b19690e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223d60728025b5c82af8d5092a4ee7f81be7d59290ae2314177524d0d88a830f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8d43b14512de5d42d812d8f5685e55e4d828b7a377c8479a3b70af73258c8e(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDatadog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8741009c3fecc832012dde3a00ff7cc624b0857260545a30670467cab67c67(
    *,
    api_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a3e75759ec0ddaa955c7f00594b47f88ff428b86f271c67f88aa9a22f9246c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b619f8dbec53e8a8e9bd8c67e7eec0a99e7381c8d088d1753cd53cf535ea50c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212b66a1f71cb2227d49323b897c59f87e3e636994145c8b499bcc40a12af167(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsDynatrace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f181dc7e6d47b08589556a550057a826fc8457ae23dbd220bb35dd50c725b3(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afb42a5260090cd033b2c18145c75a8ea0b6aea1c93ec6ae28d0a3b9884d09f(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9303a2cdf0d63bac690bee9eb29e446ab3917243283c5ad534874c79db9e70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b06635239c51c28fa1e261b513965c7e5517a30f566c5a76ba192b5df4c41c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a12b4c8d25bed6f0f97e054205842351a8bd11087f59663309b19b883ecfd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07b592d2aab9f8428e188d80fab2270fd66ead4142c72e889baf45f73725d86(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalyticsOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8d0bec360bef90357d689deed5740c590a0ea115c88015a471abfea9f77846(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945edfbfaf41b91f6a071b412b001e8a4e389c5f35ad540c78a366e438373275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8c5bd03fb3d0e78f5630d783a6fe3d2046ecf0d64f9dab2d2cbcf9a6ef489d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5debd68bc98abdfd91dc650064b73c101051620b9991e007cd83eaa5f52d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1d7ae5989e55dae8d196a4e0b10a9812221f862813ca6041beef92eefeaaec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511b43d783d5540fba0083f70c062fd3c960751367ec6b4fe0a296da0dc1938a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsGoogleAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a644cf85933e9bea4b5e01b0e85dc71ff2780c916eb5be637584f887f7b5b5(
    *,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c33e6ed4f2839797cbead3a434930ad363d3aa6e8165c391bdab12d0acc58b4(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f1fcee25faa99b99cdef25925b2174808fc2972ffbe398f71b84bd7197361b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5cc0a75ca6e8b495a836b10cff7b2e3bc3577993c2f5912eac498a7b016a7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc932e220f2ce5e0a70f58c5f9fb61994d2f5cee1105c299b26b777c51af8d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760defb0001bb526381ed6ea243752ac6bce8c484eac9b59606f2aac703615c4(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycodeOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af425bf32b31da1eb2cddfe857044a219c02c53487bb7a8955c12e5be0e3bd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0222a1207d836644f536e9ac28af2c1e526a05bdab31e88c280c899831740c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483ce9e52de80fd107086bb13f635c582eb8f50c8fa63ce42d48f2ec74c5ff8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b92d85b71a24dd8efa7b25b774be43b460114b4b546d1997f32510735a5526(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsHoneycode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c5813a0886b341013d4b5b261580c5a846b3ef89b80125d3b798c17e02f99c(
    *,
    access_key_id: builtins.str,
    datakey: builtins.str,
    secret_access_key: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ade280458fd17365b03fed60446786559ac26bd66f1920daeb721017a7b7966(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298d1a5f61f99820f990e34a8d3f699339a14c48a4ed358b27b176cb6f1dbb9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65248daefa58a0eb7dd3ecef1a4e01afbccdad8bc7607f575e4de46ce166c90e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849c91226eec9ae2c63e291cd04e45af45cee5620caa575f8ce1b220773fd740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b1f5526e8aac78d26454792df63b5544eb2b1f2c1cc4a3855f6f1e795a0b2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5812e896ea6431a558156182d5eda9beb4c667335924f73177a2d056b35058(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsInforNexus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0af9810bfa26e69659483c902e087f4fca0f7d388d3bfb7783efa2be016d7c(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4dddffe9a8494f2f765a19b607697a328633e2e223a50896123cf34646939e(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab415c3e0760b1c765b8643b7ddff53b2a7be019a3df3f1ba2cb07a98271a5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8d38dd91c6947cb0a918ff2075eb4b5014ff3fb29d2b737368dee543bd97bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2eef75cee2a8683c14941668ca296f7831bb4577906a41880990ff665c9407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73f506f39057b7e1a947b64c9698afb17fc5eddfb1fe4320f5d9ae977292d11(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketoOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1386c704e11652a4dd0d9975050c2ed6c470f778ad99b843b4981d8a151b3d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6070e876a7c40ac935f5b9673d27d3f43482c0b3ade416b6801b283c16562e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5f9f3ab02a5193abce73ffe8af5a2c61320f7e459e9f4861d5a39f3981ed11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca05b58fa74635a96682407c9f1a083e40f8d9006226f4f1d9d63cb5a1d5fff9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdfd4a8aaf49daddff1e046b57a93107abe871f13e137481d15a4a985fd532c(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0053d44f5d817d623179648a9b0a006e870bd7d9dba8f3dd3ed843e57c0266d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232eb785c655609eb12c0075321faeffc2a30478b45ecea94ae1a54de1121298(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87aaed92c36e91c6f52d976c46181c6221cf5adea758863535d9de2a6fa9d89(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2132db1fc337a7f390594ab5aab0cd12d51dc8d9963e59f0f1bba285af3ae658(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8787efa761df2758bd27183e418f6d3f0f24253cb2d2346bbe81200c6d9011f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c81b5274a1da64bef3068bf7649898d72dd998589038de1b9b8b2238b43b17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9307d6acd3f5ddb99effa8d859d89f99e05d192a8387392cb14c722e20c599c1(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bd4c167c83f31c68ce47e22809355aef5423d9f63c3b51b2a4c1fe36215127(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_credentials_arn: typing.Optional[builtins.str] = None,
    jwt_token: typing.Optional[builtins.str] = None,
    oauth2_grant_type: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496f6512fe4dd625947947caf58814c7943a5a4baa6d56901431ec080c121c71(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89fce5babe4d3ca1eb5f87b8ce295b7b414fe0385c80599947eb9fb3804cb58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0a22563f3be9074561e6e0d7c5c121b84d76610cd38cb58606964fccc2d23b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e28e53f4229db657f6209aed7380da31a421eb978178d848a7ea2322268c87c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5a1af282215a3c5f7c342c22ac59e5f7a31b25fee4f56859f798d89602ffe0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforceOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d0f3f115beda05839a678358ec6bd1202186c83fd41f556789b4fd0ae80c03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0b6f035623efc4726f873bf1398952a8634f3b650b0e4d8c529931bc9044a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a78a582120d633c50371336f9e25dfbc7a501a923b12c228340ebe1030ed08d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f575ac18e83af0cfad8032555930b07faadd5b2e1a7a18f673187b1e8170933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889159e5bf511de33382662cafbbcfbda2788b5007bf2117680d66a09db8b17c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04790af1a8083e4c61d7ac0f286d933d681f339bd0556417f77144a14402a11b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c70b5e7c2595bdb0759dfadd1c2e606081d0e1141bf247db50b88e039da9b2(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293f7dbc7135262bbda4ab967cf19cbd4647a80a3481f78487b7f38da1a0b2ed(
    *,
    basic_auth_credentials: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_credentials: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ba028ec3b1202870eee9de8e843b3a2831ef3a0998a52df0ef585f43b4d64f(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a44e3d672e5744044201ef1cb69dd4823723e4c9b614b2d91f26dc025798a44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024cd796d4b107a8d8ff2ae943c4159311f2e6c44a3e409d6b6d403af8948a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd323b09d62a6bed5432604ee4489c272670e2a1581df591bac58354dd9c06d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63712334da6c07c7772b14efa1a84cada034611848e1f7154098803053d3bac6(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataBasicAuthCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313b61a437a1c2ea1b7d612af176bc2c44e7c7c24523bd90cab18561dad87399(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec3805f91f4ff0bda60f5c67d9df8a84c90e9cafee7b8769bb03d76bad82db6(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97071e81c1d033eb22199bf795fd8bf22c6c4e9ac8ca594c3eda75ad5c0b5d2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a214185c5c45db428cfe70f8d1e9d1408a2ad526c9cca7978e707b775bf766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b40e9597a6f750c354c366bcf01b0c1af569efb2dce481577bf2a83f81d509(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b2117de16d6561d3356fbf249e3072ad38aa474906594977072dbb384a020c(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentialsOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838a6ccd3ee0842eb7b1ffaa9a083253401da2ffa7f3d717c6036ae0c161396d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9450ca381e1b20d60ded2faf10f132ccd04c58826a9f225c6da693986f567050(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6045d2105c53b9183e81c4cac4ef1aa6967d8ecdb69dffa578478ddc7034c895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a19b293c59def028c9308f0aa250095d5369612e61dbb058792a744bae637e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89798ed3e3986180b0cccb569b59401d37c277b2fc810c3470104e867728077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1bcf2d093de38abbfb411f76902dee1317188d5b714d04d1a324734cba467b(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoDataOauthCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6850bb2838d961240c5899da61adfaf879b86c3f335c246e2932332669a8636(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b044fbcdd617226db469afdbefb46a55f235b9cbd749b0a919163fe2788129(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fde00243188e9090ee195d76f062bd061b75ab41c83c4c2fb16cda01d88a18(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6f09c2268f0d31a7155ab65052df7f97c085ff798208acd2cd136dda3fddab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97296c180963fb86ea60356d915a4e2849ca4f7745fef0111ec78b3b426e94bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf82fee7b2ae7312eeb549b055c94f448acd00e3cdca28bbe296ac18e252416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2f475ccc397b19a7f26313be4c05528827b2f9959bc96eef3f5ece686223be(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6ca4f54914aa3e9045b9722572e5a7a96c99dffd3d898e0a66079f158107ef(
    *,
    api_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96937b6a98d20ada07654525ed3978c4c7a4bad96eaaff80eaa96a9451d5f0ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649a50757e459a04f3e103d445c28560a91b7466a5c6c2bda1509f6b7acd7a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3778fbe9704c120cd8c6b71970e9dfc621f2efaf4123952cb4ae016fd6acb89(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSingular],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2655e807b374f140a36cfdf7487bb7517225c7e238b58843d0db6144289e04f9(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3b8177e802e57ade557c0ddcd3a96844a8f7e575168f26683fd1b69590a37c(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2973a2a25a6475b972753dddb3947e81b07d1548255f4560e63d2a439abb201f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4935b7f6717ce829421bb3fde4c18e62257ab9502e8901300d8c8d3389d1a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2cf96a13df282ff977bfc6224b9a07e9a62ee7a7fe5db0e28a0f0f32abe8ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f212be9e03f51a008431b56fb7fb24154daec3fe6703bc2ba3024664bc349f2(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlackOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdceba6df0dd5ce547aabdb1727d324cb72fd07ce2728bb91127b688daa4a4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d867c0fcc48e8f070afb606ccaf48015bffe7302834a9637b862513aa5e31e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5f605eb8b3dd6b2078c8341657329e598907598ff45a0ac0b22994259e6b84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f257c109ffa91c8afd4fcc4f13392fe7d485c882a1c8cec5c5b742a15f82948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d853bd8e2de792bfe71b7fbc277491dc51abd589d2e6513b88e4f9a396f4ab(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSlack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9d71908b05e2d983447d9601156cdef9feb9d792d7c8ad8da14a9d6c0d5316(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314b68bc669d198e670d1c67dd3cb25c5b9116c27dd4d50c327e329012ef58c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a42b01ad0b0922dcc5cfdf4b5112f0cb9e621b9637a5af4fbc80fd53d9dd31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7a7b9533076bec6c4d12eb285fff2fe3ac417a1eee0484ab0721ed9c43ce75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e471fb895aedb976db4902b359d2025aff9715859c0584c8f6a71fae510d229(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe0eed58d83be8097be2339872eaca1ed8451e6e7412d5153e911dd6178d91e(
    *,
    api_secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18e50a8ebb000b7e421f84794f0543e2898fc38ef5e2b896de1c0adde816698(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4707e9948acd52d35a2ae2eb681c07b1b9c4436b2a8a7804dcb104b39d21731d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce383b0d89dbe490c6f241fbbc1b678870152cc759bba6c2f60380cf99e93de0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsTrendmicro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd5f2ff5f0ea4fac482245256ada3b1d547f232bc6f75704d58b429960e3e5f(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab49abcac2f9d5d7fa56813613bd98cfaaae7a008a3c22b035760cb1385a44e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540c17dc23305daa96559adff83606d8632cb800e154d39aedee93aaeab46906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004f5a3ea03016da824667060cf95adcbcffac6671d4fb9885e3008bd3212187(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e18f51c7b1da83578af8e3f7d7cd884422a0417b5355b878dc3eb4c1acb8a1(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsVeeva],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb6445ad5b61a5622c0c859c58602dd62c8af61416c3ca6ce884172d842d627(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    oauth_request: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b056472356c1f8762da1248b957193fbbe5e0dd04659b04168f947a95cc7fa(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a0d08f3c0039c2676e8a52c72fe9c65b13e9da9cf6be5eb99410be4667aded(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adaa2769d2a8071d34c9bf95be68e96b2978a049d99d6cd5c2785fe1f33a3911(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af63822b7ba72ee19fc42fe1c1088ba3256330c670f29ca1c2cd2e7944652b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9962eb43b93cb827e932b6ffc85811375221d809171f17f5e7a79009bdd88431(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendeskOauthRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9f53a795a2971e930cd66195fea1d639114bf325af6698ced90b90db9e91b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f450a2c41cfa9b0162d12fbe1316343b11fd6fdf7a1a919d1912dc9fbab90480(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e007852570ed83a58156e8018b64d3c31e9fe4310c6c2fdf8d745232c02dba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e079a4c705ae40285df666fab9bc488b2402f8e813a8e00c86d8689bde5c75ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095538d5972b48020aea6aef692149f613e56ff3852a1744c3a178376d295a00(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileCredentialsZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be40e378e74a6ef1c4d0b48e580299be5b2b99179087012959978e4f82f72a16(
    *,
    amplitude: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_connector: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    dynatrace: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
    google_analytics: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    honeycode: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
    infor_nexus: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    singular: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    trendmicro: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
    veeva: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f90c3e0d311fd52a51536d3284cc8324892ed25ace3c171b060ef678cce6fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96eca5ccb729c57f7a2c129316cf607eb20af56a79a0e2ec6146989c9b159d16(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesAmplitude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c4da38ac8577601d61f1d31dd2ff835822df5441e82f136d3792a6433ce3dd(
    *,
    oauth2_properties: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties, typing.Dict[builtins.str, typing.Any]]] = None,
    profile_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c205fc9fa836e1e496293d7d5c1d18ddf358ac26b6d2ad18b06905f555b6980(
    *,
    oauth2_grant_type: builtins.str,
    token_url: builtins.str,
    token_url_custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4146944aee6e125625d6ba689a23a47343bcf62a7a568d12bb1995b681f8e779(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98bb50d947a269af83d36a8f809693e4b7fcf0fe4e65c6f9a73c00f66b04428(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d14a7513cecbc701816ba244d1ae7e590799063be0d93691817c64fd73ab06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1334dcab335b41d222919daf951621e1dfc1ab358b5cb80c73ba65e0c135ead(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a501589eb460dd966ab02a8cbf4c4c8f8f591061192af9a18f67486e0541924(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnectorOauth2Properties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90da0bbc570a68c152cc10e20e1acfce7c85f6a5241084fe0a63f8a7a904b255(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872bac9ccce9e8c8d025e736c503246e1d668f53ebf48c3da4daec6a797402b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3da34dc7a64832d073adb831318f592dec1330ff81c44c67fd063e5951413d(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84cc8a5f4fc82fcbb0df96b7c434c31088caa096974a857a654f879fa7a20db(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85b4bc2d265d1f629c91f4ae25899be2c9d5c71a35dc62fdefa07931a61c48f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823332a9dc6e35a4d0f4517ed949bd55a3f7f714a8d9585f480f3b08a6fdf16e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d298d7be5f8ffd75e4da095f31229671a71e2e33951fcb0a30eb51610f08f5(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDatadog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafa46462c63ce8c851a38330d38fc9f2783cb43e3f8e39da68100c8b2bd6e32(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586ec572611ee845ced93816505c5b00c9ccbbfdf3b9c60a2a3a8422a91de382(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1463c189daf4615feefbaa10262896ffcd6951ea77d1b8b3036b8675b28fca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117bfd3d92c6cab80996a563aab2ce791ebb7adffb21f6b3b150a39daaa4fa3c(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesDynatrace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69dbe9d98418a275ba46c56a9e8437a08dc3ceddd0c16f3fa1ac73e27b629776(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51676257789c6b7830254e7dac37fba5c12b6331c837c85e147c7f2dff44cb27(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesGoogleAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefbe88796b3985f1890176beeb13dfda943cb9abec642b86149a98372407818(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353472a9b6b8089f1d9e5c231c032d01bc5a348a10caa3e255519650f94822e3(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesHoneycode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9656519824c3aeb802b60f2e466a70e5a548cb152b4fb4c9a9cb8baf348ac855(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f38d18a8e7106b691c58e6ff2ea5c3074b7da581fe000157b1532e3eb1c3713(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d258033b000d43dea771ad143e463d00652d43c711da70a10f287b7017530a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a54fa291b45527dd4d5bccb8e4d975d91463f38049cb98543bfe8e2c94e79a(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesInforNexus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af32d0bce6a7f0884bf4a59c2df101770332d194a85870650b0c04aeea6ec69c(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151a516ba0376742a532e6ee1ed76031dc172f634bbff14a9b6d65a8a3f0a508(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cc7379bac41602f1620810cf1fa5e9747e8cdb0e677a04a414a4fb01218590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5316eab0f9e2bf43d3fdb4aec8f2304dd87f427fbf289ddeb831e09467b738d(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97df88eb853fa9a1a3f3aa74fb7fa0bbb76fce6e1510027059fa58d15277042d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da05ea775832c54533461e03186db702117abc68dba2f13fdb41305e621e1eeb(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfileProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53171a920fc9f383ab550cd23accad63fc55b99f7c17f57e073980e2df945df3(
    *,
    bucket_name: builtins.str,
    role_arn: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    data_api_role_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f86ead776ec5ace561e52b48028faf900eb6128f7de3c23241c207c1d7cdaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980e2e913684e29fb43e05f9181323bdb93047d2ed03e53a668f43cdeefe6fb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8b67bca71f22ab7098137b32c59542f6476aba21f6a376cb23f4e428a10f15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119a0362a3b9a221af6cf0231bf22bf1b784540a42a6a7bdb121590a09d439e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de361a99fcfc9c558d06409aa85ccf2a32f1d49a3f85fe2527a82d3e067e309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d5b993e7f0f2d92d2d8cf62dda4cdc8ac6739acb76e218393f6fab7e3dad95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e157859fde45865bc27e43d41b293198322358b5d54ddc658a1f449430a4e53a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4016c6e214bca9f93db18634f88cd85c2f2ba5adab1d2bea6a09a93a086a1757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb177c6f60d7769d437938246d278fd7e43df8a8ad74e5405b96402340e59be(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354bad9bb2e0e4db9bc12b7e02e34fe3a34c92871294761275f53edb3967ced1(
    *,
    instance_url: typing.Optional[builtins.str] = None,
    is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_privatelink_for_metadata_and_authorization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ea5895dd3e24fb056df2e45d4f2efce96399747d1b6b1ee18d772d03d15d22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f60faadf1caf9c9c1cf17107d6cd6fdec6b4989a7e23da923da66a50ad6eb00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8a4c6454d99917c3e29ceb5ea34260f220a7eceb5229678f2cc6b49da106cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3495724532f7eba8bd549634c54ded1bc86cac716d41799e2042475f45399ae4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252e74a3627afd2f955d7ac4e5763ec5c6eb65a71ffbfc3220abd6cecc66cdf4(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ebfb642890d7f55577ea558cac0b4bf56223bcb4329dc31ddba12b01205a4e(
    *,
    application_host_url: builtins.str,
    application_service_path: builtins.str,
    client_number: builtins.str,
    port_number: jsii.Number,
    logon_language: typing.Optional[builtins.str] = None,
    oauth_properties: typing.Optional[typing.Union[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a851c7ce629ca694e175df21b48b94966842d34a4f49cb257a9b2a90389102d7(
    *,
    auth_code_url: builtins.str,
    oauth_scopes: typing.Sequence[builtins.str],
    token_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fd257b66af32c9bd980b014b6359ad6ca5f71de95624b7fafb6c841b96175d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b7a30147c9a6d4842e86fed14a297c6cb021987b7b899ac3a24a843145fa63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35a1e2f038c6515345c431538c9fbf1d068d556de7f354c15700fbf41fadad9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728ddd6a061ff0711ac60e5d261af6801bd0e907964efdfb7a5419c51c6b20eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65724943e46e05e7eea8bc06d4752b6e7515edc3a6ee03055d82de9ded059f0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoDataOauthProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee6ebac5c0cf06d46a67624ee3a1fea1b9ceac5d4c9c893d87b6d2fb79e676d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2baba90665604934b75b2b0d79f553e225e4a436a5053319007e6e7e8ac877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f240b192d96e42038e145941dd58416b5ce1e87a2898d85949a4cf23288e7514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a80d3e5b5d514e1ba2bd2f8a705e7fd3b513bf57a67881152f3ff7e9ebe582e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af4055c55f00e69556e6bc3b75772c02fec89c7ed059ecf3a7fb6218451f501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54c77c99478407274bcc3a905b8eb106198bdd5f5ac16dc995f2863df4b0904(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a71821eb95d9b193f8d4403786d81714cf8fe8f36d5da5327fdba7d4b942ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8751ddb5cd9d40da5cb2834faef84a7dfcc37d6053ca262d04c3a57ed6a7b713(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6517c7fd52fb09c4e8e76e1a87d9211901a862c38edfda6c14b31f47cad986d6(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2013bde61bcd28c9fc577aae6c6a406c829a257076be558676ae73c4f9aebdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18af9eedc276831f0da48023cd33ade73ee5719cb509a9da47c1264a4c78d393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3681db72c2fb615f6096b78a40992774891f75dfcb5f757679095fb5ad7302b0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e5eaec6b7b33f4ed76382bec6f2fcb82e45b582d61cfb4f8dd2a20da679576(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e329e1e8d6aa370bc14cdf199d3555658b7923a24e0e8de13579b4bbcfe61cb0(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSingular],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11ed2a060d0e2a13da4c5265b1e4bd853b0bd24ae8b0fb4838d64a99d18993d(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d24065be4dcf533fe7899c998b2dfb01d70a3420c764561498deb36f645a50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6db88df485de09444d04c148152a5b1b60751f761bd3c6ead6ab5e1b234af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aac7c07e22f9513e4b38624a05a818d91a5d4e9b8d8344abca9e1e63943ea08(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSlack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fb3f6fca3a5053e7ff111409eb0671d01a6bdab8e99064bb4abcce6192b1c2(
    *,
    bucket_name: builtins.str,
    stage: builtins.str,
    warehouse: builtins.str,
    account_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05942b5747ec420d7b43ddfd00c71675439795eef3b1ed33e5e2f902f12ac9b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b2c93a61d5d3b28cc50da6e6b4138ea568879ac8ced7df6662116eba9390be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8959dfe3b6b8ebedac2e37a4d07eaa93dee02d0a774ca7ba3aebbf76c5db39c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c46032748ebf23e88e08a98a67fe8a0fe24554f6877b4341e3e1a304da959b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7dd6149773d34cf97e71d0d7f95e4860a86ed0766ddb187f6ab8e91d2ee3c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842c89725d4623c2e6892bee344a3ccca1444386debc4d86dc8f55a84282186c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5d995e2fc39bca6e81b7461a09db8b41785a5bbe6fdb4d500229e4f855b1df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d98dbbd9ba1fac50af9b22de408038ca9414145586a182d3da0b5a06de1e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be61d6bbfa733001d62710b790f80b937064910a8841b834b0d716db17aba7cc(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bece5b74a7c41750c35b40e8ae11a1356dbd5f616c26f72357eead45aa3d389(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5309d54d0c8fef6ccd2c09977bc046e87b6ae50eebe42170a1887de44c656ed(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesTrendmicro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce1028e3986595573bf18c25af875ef881c4475de3618c55359bfc9ff1c98c7(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e79cb6dcdb59f47e732588cf230927dbe1b6f6bc266c5ac8b5e5f08a02f418a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf10cff61f4703bb7feb9769de83731489c8344614bce821022a7657a727b60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14dd24709acb3659c04f28e009b972851dbcec459d388f3ea67c1bbec07b4ccc(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesVeeva],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37aacca09f0f6337ae7c7b418858fcd52accd1ca2bfd692ea21fce7511b8268b(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e61d0b7c94605e27dc6012c14ab5474e79b9ad0fd275c87080c9f5028f3501(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354ed2efacaa854a9cd1c3c15a047c27a1a07426f3388635ca14b210d14b551d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fe7744b96fa6c9c98a5b6a9b3541450c97f431bed39e11c680e2dfe71f5438(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfigConnectorProfilePropertiesZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837dc4b4a25ad7d86284e378f8452e16e3bf9c3f07b4272558572e0e978e5887(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934566f58a8b0f97ccceb0f9d94f6340bbc4bc89b99b8334db62db151591edfc(
    value: typing.Optional[AppflowConnectorProfileConnectorProfileConfig],
) -> None:
    """Type checking stubs"""
    pass
