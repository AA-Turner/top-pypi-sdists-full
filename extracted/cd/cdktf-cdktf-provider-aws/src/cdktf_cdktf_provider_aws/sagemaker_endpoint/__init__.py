r'''
# `aws_sagemaker_endpoint`

Refer to the Terraform Registry for docs: [`aws_sagemaker_endpoint`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint).
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


class SagemakerEndpoint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpoint",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint aws_sagemaker_endpoint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        endpoint_config_name: builtins.str,
        deployment_config: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint aws_sagemaker_endpoint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param endpoint_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#endpoint_config_name SagemakerEndpoint#endpoint_config_name}.
        :param deployment_config: deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#deployment_config SagemakerEndpoint#deployment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#id SagemakerEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#name SagemakerEndpoint#name}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#tags SagemakerEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#tags_all SagemakerEndpoint#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f65893232cfaebf6a9a73cd365a7ffd80eb653cd8209fe984635e3a6a1b59a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerEndpointConfig(
            endpoint_config_name=endpoint_config_name,
            deployment_config=deployment_config,
            id=id,
            name=name,
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
        '''Generates CDKTF code for importing a SagemakerEndpoint resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SagemakerEndpoint to import.
        :param import_from_id: The id of the existing SagemakerEndpoint that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SagemakerEndpoint to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d5d70111730674ea7380f9e53ccf7e032f36b845194de36f06c8cf71d734c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeploymentConfig")
    def put_deployment_config(
        self,
        *,
        auto_rollback_configuration: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        blue_green_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#auto_rollback_configuration SagemakerEndpoint#auto_rollback_configuration}
        :param blue_green_update_policy: blue_green_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#blue_green_update_policy SagemakerEndpoint#blue_green_update_policy}
        :param rolling_update_policy: rolling_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#rolling_update_policy SagemakerEndpoint#rolling_update_policy}
        '''
        value = SagemakerEndpointDeploymentConfig(
            auto_rollback_configuration=auto_rollback_configuration,
            blue_green_update_policy=blue_green_update_policy,
            rolling_update_policy=rolling_update_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentConfig", [value]))

    @jsii.member(jsii_name="resetDeploymentConfig")
    def reset_deployment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "SagemakerEndpointDeploymentConfigOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigOutputReference", jsii.get(self, "deploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigInput")
    def deployment_config_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfig"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfig"], jsii.get(self, "deploymentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigNameInput")
    def endpoint_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
    @jsii.member(jsii_name="endpointConfigName")
    def endpoint_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointConfigName"))

    @endpoint_config_name.setter
    def endpoint_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bf3d96da257f418cf4702d469b33defee477561a12ad88088e0e3c7a1054db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointConfigName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8012c26c4502457d0f6a0a3bf557543bb9d35ceec43d2fd133a6d19daebc154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ec521d0ace0a544c539205e5952afb0abe666ff3e10b974990724fa3556b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7327f94205a1cb85798bb71a9c7e49a8c1fa71702eed2f0d96babd08b4b70a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958237648b846fbbe33e0f7f6bc14946b8debe70148e8f2b1bdb55308c7498c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "endpoint_config_name": "endpointConfigName",
        "deployment_config": "deploymentConfig",
        "id": "id",
        "name": "name",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerEndpointConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        endpoint_config_name: builtins.str,
        deployment_config: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
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
        :param endpoint_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#endpoint_config_name SagemakerEndpoint#endpoint_config_name}.
        :param deployment_config: deployment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#deployment_config SagemakerEndpoint#deployment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#id SagemakerEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#name SagemakerEndpoint#name}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#tags SagemakerEndpoint#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#tags_all SagemakerEndpoint#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deployment_config, dict):
            deployment_config = SagemakerEndpointDeploymentConfig(**deployment_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe31387b58c6495c7d82b9ac62f6f083a142f69c062023216433474ea7057eb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument endpoint_config_name", value=endpoint_config_name, expected_type=type_hints["endpoint_config_name"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_config_name": endpoint_config_name,
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
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
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
    def endpoint_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#endpoint_config_name SagemakerEndpoint#endpoint_config_name}.'''
        result = self._values.get("endpoint_config_name")
        assert result is not None, "Required property 'endpoint_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional["SagemakerEndpointDeploymentConfig"]:
        '''deployment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#deployment_config SagemakerEndpoint#deployment_config}
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#id SagemakerEndpoint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#name SagemakerEndpoint#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#tags SagemakerEndpoint#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#tags_all SagemakerEndpoint#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auto_rollback_configuration": "autoRollbackConfiguration",
        "blue_green_update_policy": "blueGreenUpdatePolicy",
        "rolling_update_policy": "rollingUpdatePolicy",
    },
)
class SagemakerEndpointDeploymentConfig:
    def __init__(
        self,
        *,
        auto_rollback_configuration: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        blue_green_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rolling_update_policy: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_rollback_configuration: auto_rollback_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#auto_rollback_configuration SagemakerEndpoint#auto_rollback_configuration}
        :param blue_green_update_policy: blue_green_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#blue_green_update_policy SagemakerEndpoint#blue_green_update_policy}
        :param rolling_update_policy: rolling_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#rolling_update_policy SagemakerEndpoint#rolling_update_policy}
        '''
        if isinstance(auto_rollback_configuration, dict):
            auto_rollback_configuration = SagemakerEndpointDeploymentConfigAutoRollbackConfiguration(**auto_rollback_configuration)
        if isinstance(blue_green_update_policy, dict):
            blue_green_update_policy = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy(**blue_green_update_policy)
        if isinstance(rolling_update_policy, dict):
            rolling_update_policy = SagemakerEndpointDeploymentConfigRollingUpdatePolicy(**rolling_update_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8914a0032c8846d5b17112129517b3a42334214284070e8e7ebeb39e21825dc1)
            check_type(argname="argument auto_rollback_configuration", value=auto_rollback_configuration, expected_type=type_hints["auto_rollback_configuration"])
            check_type(argname="argument blue_green_update_policy", value=blue_green_update_policy, expected_type=type_hints["blue_green_update_policy"])
            check_type(argname="argument rolling_update_policy", value=rolling_update_policy, expected_type=type_hints["rolling_update_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_rollback_configuration is not None:
            self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if blue_green_update_policy is not None:
            self._values["blue_green_update_policy"] = blue_green_update_policy
        if rolling_update_policy is not None:
            self._values["rolling_update_policy"] = rolling_update_policy

    @builtins.property
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration"]:
        '''auto_rollback_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#auto_rollback_configuration SagemakerEndpoint#auto_rollback_configuration}
        '''
        result = self._values.get("auto_rollback_configuration")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigAutoRollbackConfiguration"], result)

    @builtins.property
    def blue_green_update_policy(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy"]:
        '''blue_green_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#blue_green_update_policy SagemakerEndpoint#blue_green_update_policy}
        '''
        result = self._values.get("blue_green_update_policy")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy"], result)

    @builtins.property
    def rolling_update_policy(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"]:
        '''rolling_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#rolling_update_policy SagemakerEndpoint#rolling_update_policy}
        '''
        result = self._values.get("rolling_update_policy")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfiguration",
    jsii_struct_bases=[],
    name_mapping={"alarms": "alarms"},
)
class SagemakerEndpointDeploymentConfigAutoRollbackConfiguration:
    def __init__(
        self,
        *,
        alarms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alarms: alarms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#alarms SagemakerEndpoint#alarms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60403c3aed1f457890e8a4ce5f7be711a6e2ec579d3f2b517260cc3fb502bd20)
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarms is not None:
            self._values["alarms"] = alarms

    @builtins.property
    def alarms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms"]]]:
        '''alarms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#alarms SagemakerEndpoint#alarms}
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigAutoRollbackConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms",
    jsii_struct_bases=[],
    name_mapping={"alarm_name": "alarmName"},
)
class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms:
    def __init__(self, *, alarm_name: builtins.str) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#alarm_name SagemakerEndpoint#alarm_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9ab3ba1a3f6ca04690c5ba65a404cad8094043f1a58910098e08ad383d3d63)
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_name": alarm_name,
        }

    @builtins.property
    def alarm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#alarm_name SagemakerEndpoint#alarm_name}.'''
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__060a5194fb51c634aac64b61f9467622c8c0b0a7afc0e4847effc17a486da947)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676a28fc8bbc84189435e4a45ea0adc8935b1c36ea897c0b4554af01a2d4de0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dc1664423d77402b69e23655bc8a11197c69912452ddea3bd804fc35ebb57d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e53a49488279eaf4cdefed89c1cc19565ba83c6c2e3156d78ea32fc770f1b972)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2db2152c19758380297656673867ca553f5bb60aa87b09af7ae98c54a67f890a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf7301b733dc5b836b88a5964843d193aaa7590a245ac8819de1e3fae73bc7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b6f2aeadc3e8c0e16d79a413bbabe301b8f926a0adaf241a624a9e71b0d6780)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="alarmNameInput")
    def alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2b98730757fe3b076325f79987c44dcf112e61306304ac92ac537c2acaad40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5221d5f8dafa47a3ef921101488f0fe385236cde42b38efcb451fdd85d36339c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a21d09a513c257f32ef204b6423b962fc11d6210bc856145ef063d0902e7a38b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAlarms")
    def put_alarms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7484e910acb5102134537020ab0fa136b54e3694dbb10cb0a6febe72971408d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAlarms", [value]))

    @jsii.member(jsii_name="resetAlarms")
    def reset_alarms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarms", []))

    @builtins.property
    @jsii.member(jsii_name="alarms")
    def alarms(
        self,
    ) -> SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList:
        return typing.cast(SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList, jsii.get(self, "alarms"))

    @builtins.property
    @jsii.member(jsii_name="alarmsInput")
    def alarms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]], jsii.get(self, "alarmsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9935f9bb6ba5bd18568829661b4961b6ac9773897ae9338c9e9501b056772785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "traffic_routing_configuration": "trafficRoutingConfiguration",
        "maximum_execution_timeout_in_seconds": "maximumExecutionTimeoutInSeconds",
        "termination_wait_in_seconds": "terminationWaitInSeconds",
    },
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy:
    def __init__(
        self,
        *,
        traffic_routing_configuration: typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration", typing.Dict[builtins.str, typing.Any]],
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        termination_wait_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param traffic_routing_configuration: traffic_routing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#traffic_routing_configuration SagemakerEndpoint#traffic_routing_configuration}
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param termination_wait_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#termination_wait_in_seconds SagemakerEndpoint#termination_wait_in_seconds}.
        '''
        if isinstance(traffic_routing_configuration, dict):
            traffic_routing_configuration = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration(**traffic_routing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bfaa5c103019072f32cf7a550ed0f0123078c1c0d9deff4c55c21c97e5876a)
            check_type(argname="argument traffic_routing_configuration", value=traffic_routing_configuration, expected_type=type_hints["traffic_routing_configuration"])
            check_type(argname="argument maximum_execution_timeout_in_seconds", value=maximum_execution_timeout_in_seconds, expected_type=type_hints["maximum_execution_timeout_in_seconds"])
            check_type(argname="argument termination_wait_in_seconds", value=termination_wait_in_seconds, expected_type=type_hints["termination_wait_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "traffic_routing_configuration": traffic_routing_configuration,
        }
        if maximum_execution_timeout_in_seconds is not None:
            self._values["maximum_execution_timeout_in_seconds"] = maximum_execution_timeout_in_seconds
        if termination_wait_in_seconds is not None:
            self._values["termination_wait_in_seconds"] = termination_wait_in_seconds

    @builtins.property
    def traffic_routing_configuration(
        self,
    ) -> "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration":
        '''traffic_routing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#traffic_routing_configuration SagemakerEndpoint#traffic_routing_configuration}
        '''
        result = self._values.get("traffic_routing_configuration")
        assert result is not None, "Required property 'traffic_routing_configuration' is missing"
        return typing.cast("SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration", result)

    @builtins.property
    def maximum_execution_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.'''
        result = self._values.get("maximum_execution_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def termination_wait_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#termination_wait_in_seconds SagemakerEndpoint#termination_wait_in_seconds}.'''
        result = self._values.get("termination_wait_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__773681bd7da06ac22fe8353eb0b62f2cc299eb8cf59ffff9f90ae3cb9806237f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrafficRoutingConfiguration")
    def put_traffic_routing_configuration(
        self,
        *,
        type: builtins.str,
        wait_interval_in_seconds: jsii.Number,
        canary_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_step_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param canary_size: canary_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#canary_size SagemakerEndpoint#canary_size}
        :param linear_step_size: linear_step_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#linear_step_size SagemakerEndpoint#linear_step_size}
        '''
        value = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration(
            type=type,
            wait_interval_in_seconds=wait_interval_in_seconds,
            canary_size=canary_size,
            linear_step_size=linear_step_size,
        )

        return typing.cast(None, jsii.invoke(self, "putTrafficRoutingConfiguration", [value]))

    @jsii.member(jsii_name="resetMaximumExecutionTimeoutInSeconds")
    def reset_maximum_execution_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumExecutionTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetTerminationWaitInSeconds")
    def reset_termination_wait_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationWaitInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingConfiguration")
    def traffic_routing_configuration(
        self,
    ) -> "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference", jsii.get(self, "trafficRoutingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSecondsInput")
    def maximum_execution_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumExecutionTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationWaitInSecondsInput")
    def termination_wait_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminationWaitInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingConfigurationInput")
    def traffic_routing_configuration_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration"], jsii.get(self, "trafficRoutingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSeconds")
    def maximum_execution_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumExecutionTimeoutInSeconds"))

    @maximum_execution_timeout_in_seconds.setter
    def maximum_execution_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337fcc1a810c7b999c726accdea7121635ee37e803b002e36cd4ac134aedb026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumExecutionTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationWaitInSeconds")
    def termination_wait_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationWaitInSeconds"))

    @termination_wait_in_seconds.setter
    def termination_wait_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4bc670867133a7c1f53209ad4459c0f162d7bd6196d493f86eae02bc6b093d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationWaitInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab770fc9a59c971349e1d08bc96de96017b6509716339c73a060361b9c7c3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "wait_interval_in_seconds": "waitIntervalInSeconds",
        "canary_size": "canarySize",
        "linear_step_size": "linearStepSize",
    },
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration:
    def __init__(
        self,
        *,
        type: builtins.str,
        wait_interval_in_seconds: jsii.Number,
        canary_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize", typing.Dict[builtins.str, typing.Any]]] = None,
        linear_step_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param canary_size: canary_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#canary_size SagemakerEndpoint#canary_size}
        :param linear_step_size: linear_step_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#linear_step_size SagemakerEndpoint#linear_step_size}
        '''
        if isinstance(canary_size, dict):
            canary_size = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize(**canary_size)
        if isinstance(linear_step_size, dict):
            linear_step_size = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize(**linear_step_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b45034a5b5502ed9d84a0826b33300763a0fee02ec01a98b4a8d48fa9092e6)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument wait_interval_in_seconds", value=wait_interval_in_seconds, expected_type=type_hints["wait_interval_in_seconds"])
            check_type(argname="argument canary_size", value=canary_size, expected_type=type_hints["canary_size"])
            check_type(argname="argument linear_step_size", value=linear_step_size, expected_type=type_hints["linear_step_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "wait_interval_in_seconds": wait_interval_in_seconds,
        }
        if canary_size is not None:
            self._values["canary_size"] = canary_size
        if linear_step_size is not None:
            self._values["linear_step_size"] = linear_step_size

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wait_interval_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.'''
        result = self._values.get("wait_interval_in_seconds")
        assert result is not None, "Required property 'wait_interval_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def canary_size(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize"]:
        '''canary_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#canary_size SagemakerEndpoint#canary_size}
        '''
        result = self._values.get("canary_size")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize"], result)

    @builtins.property
    def linear_step_size(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize"]:
        '''linear_step_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#linear_step_size SagemakerEndpoint#linear_step_size}
        '''
        result = self._values.get("linear_step_size")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11b81974a8369bf514168284786081803fb8d72164c512128abe15e42be02c5)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f4b922cabb9d0379fe200e1ea72c6efa7fedd91ac5ab7d0e5f08e62f5832a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37a223c46c96af19f7fffec98fd5956c55cc6a28cc39fa7746162c7c7695b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d69afceb474f235cfafcf5cd54d73327ccfe6b07247ed83a3ff34f2cd7d85e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6459b1daf0049f94b9694d0c5f43c4aaeb68b17352e439948bb32ee3c6ff204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1814d4e0bbd76af30a367391aa4f08cebec6aed978c9935e3faa2edbd95b9f71)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84dccee116b1c54d26095742f9d5137af954373d11c1ea7396b25b65f27fe4a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf20a23ce48a3001b35ae311a7a1958fcf3a0231491009ed159d89ab522cf8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930f715edea7a2d4474e43edbabd109bfa506710b6d2ed30ade130256f398f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dff398ffad681de9e4ee58a414e159ea055d2c97077652361929c8dbd80af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dd912f784cbdb47276bdf51b6fc62f3781ea095668221fa64aa3c5db64903ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanarySize")
    def put_canary_size(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putCanarySize", [value_]))

    @jsii.member(jsii_name="putLinearStepSize")
    def put_linear_step_size(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putLinearStepSize", [value_]))

    @jsii.member(jsii_name="resetCanarySize")
    def reset_canary_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanarySize", []))

    @jsii.member(jsii_name="resetLinearStepSize")
    def reset_linear_step_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinearStepSize", []))

    @builtins.property
    @jsii.member(jsii_name="canarySize")
    def canary_size(
        self,
    ) -> SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference, jsii.get(self, "canarySize"))

    @builtins.property
    @jsii.member(jsii_name="linearStepSize")
    def linear_step_size(
        self,
    ) -> SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference, jsii.get(self, "linearStepSize"))

    @builtins.property
    @jsii.member(jsii_name="canarySizeInput")
    def canary_size_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize], jsii.get(self, "canarySizeInput"))

    @builtins.property
    @jsii.member(jsii_name="linearStepSizeInput")
    def linear_step_size_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize], jsii.get(self, "linearStepSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSecondsInput")
    def wait_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5668f64962dffff543cb2ad87f8cff2eebe71273e2c45321c375c8167b87aef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSeconds")
    def wait_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitIntervalInSeconds"))

    @wait_interval_in_seconds.setter
    def wait_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316fa970793c02df64db0fcb77190630e102d5dcb563d3c5dab3856929e874ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26569d7aa73c8b9fc3fa009ec63f013a05a23927a35c0109994dd8c84014a7c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ad4990208d0b0ed7ed4c46f593461121ea09606b37018886610f04521da42d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoRollbackConfiguration")
    def put_auto_rollback_configuration(
        self,
        *,
        alarms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alarms: alarms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#alarms SagemakerEndpoint#alarms}
        '''
        value = SagemakerEndpointDeploymentConfigAutoRollbackConfiguration(
            alarms=alarms
        )

        return typing.cast(None, jsii.invoke(self, "putAutoRollbackConfiguration", [value]))

    @jsii.member(jsii_name="putBlueGreenUpdatePolicy")
    def put_blue_green_update_policy(
        self,
        *,
        traffic_routing_configuration: typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration, typing.Dict[builtins.str, typing.Any]],
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        termination_wait_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param traffic_routing_configuration: traffic_routing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#traffic_routing_configuration SagemakerEndpoint#traffic_routing_configuration}
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param termination_wait_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#termination_wait_in_seconds SagemakerEndpoint#termination_wait_in_seconds}.
        '''
        value = SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy(
            traffic_routing_configuration=traffic_routing_configuration,
            maximum_execution_timeout_in_seconds=maximum_execution_timeout_in_seconds,
            termination_wait_in_seconds=termination_wait_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putBlueGreenUpdatePolicy", [value]))

    @jsii.member(jsii_name="putRollingUpdatePolicy")
    def put_rolling_update_policy(
        self,
        *,
        maximum_batch_size: typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize", typing.Dict[builtins.str, typing.Any]],
        wait_interval_in_seconds: jsii.Number,
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        rollback_maximum_batch_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param maximum_batch_size: maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_batch_size SagemakerEndpoint#maximum_batch_size}
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param rollback_maximum_batch_size: rollback_maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#rollback_maximum_batch_size SagemakerEndpoint#rollback_maximum_batch_size}
        '''
        value = SagemakerEndpointDeploymentConfigRollingUpdatePolicy(
            maximum_batch_size=maximum_batch_size,
            wait_interval_in_seconds=wait_interval_in_seconds,
            maximum_execution_timeout_in_seconds=maximum_execution_timeout_in_seconds,
            rollback_maximum_batch_size=rollback_maximum_batch_size,
        )

        return typing.cast(None, jsii.invoke(self, "putRollingUpdatePolicy", [value]))

    @jsii.member(jsii_name="resetAutoRollbackConfiguration")
    def reset_auto_rollback_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRollbackConfiguration", []))

    @jsii.member(jsii_name="resetBlueGreenUpdatePolicy")
    def reset_blue_green_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlueGreenUpdatePolicy", []))

    @jsii.member(jsii_name="resetRollingUpdatePolicy")
    def reset_rolling_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollingUpdatePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(
        self,
    ) -> SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference, jsii.get(self, "autoRollbackConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenUpdatePolicy")
    def blue_green_update_policy(
        self,
    ) -> SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference, jsii.get(self, "blueGreenUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="rollingUpdatePolicy")
    def rolling_update_policy(
        self,
    ) -> "SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference", jsii.get(self, "rollingUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfigurationInput")
    def auto_rollback_configuration_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration], jsii.get(self, "autoRollbackConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="blueGreenUpdatePolicyInput")
    def blue_green_update_policy_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy], jsii.get(self, "blueGreenUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="rollingUpdatePolicyInput")
    def rolling_update_policy_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicy"], jsii.get(self, "rollingUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerEndpointDeploymentConfig]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df46696b265cbf2821c0671c5a91b70e8e86246a110b86dc645b2d438c2233a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_batch_size": "maximumBatchSize",
        "wait_interval_in_seconds": "waitIntervalInSeconds",
        "maximum_execution_timeout_in_seconds": "maximumExecutionTimeoutInSeconds",
        "rollback_maximum_batch_size": "rollbackMaximumBatchSize",
    },
)
class SagemakerEndpointDeploymentConfigRollingUpdatePolicy:
    def __init__(
        self,
        *,
        maximum_batch_size: typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize", typing.Dict[builtins.str, typing.Any]],
        wait_interval_in_seconds: jsii.Number,
        maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        rollback_maximum_batch_size: typing.Optional[typing.Union["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param maximum_batch_size: maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_batch_size SagemakerEndpoint#maximum_batch_size}
        :param wait_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.
        :param maximum_execution_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.
        :param rollback_maximum_batch_size: rollback_maximum_batch_size block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#rollback_maximum_batch_size SagemakerEndpoint#rollback_maximum_batch_size}
        '''
        if isinstance(maximum_batch_size, dict):
            maximum_batch_size = SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize(**maximum_batch_size)
        if isinstance(rollback_maximum_batch_size, dict):
            rollback_maximum_batch_size = SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize(**rollback_maximum_batch_size)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba402b4d85beab8df1c283f31a318357905cee63efdace6418d3f16a907cbeda)
            check_type(argname="argument maximum_batch_size", value=maximum_batch_size, expected_type=type_hints["maximum_batch_size"])
            check_type(argname="argument wait_interval_in_seconds", value=wait_interval_in_seconds, expected_type=type_hints["wait_interval_in_seconds"])
            check_type(argname="argument maximum_execution_timeout_in_seconds", value=maximum_execution_timeout_in_seconds, expected_type=type_hints["maximum_execution_timeout_in_seconds"])
            check_type(argname="argument rollback_maximum_batch_size", value=rollback_maximum_batch_size, expected_type=type_hints["rollback_maximum_batch_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_batch_size": maximum_batch_size,
            "wait_interval_in_seconds": wait_interval_in_seconds,
        }
        if maximum_execution_timeout_in_seconds is not None:
            self._values["maximum_execution_timeout_in_seconds"] = maximum_execution_timeout_in_seconds
        if rollback_maximum_batch_size is not None:
            self._values["rollback_maximum_batch_size"] = rollback_maximum_batch_size

    @builtins.property
    def maximum_batch_size(
        self,
    ) -> "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize":
        '''maximum_batch_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_batch_size SagemakerEndpoint#maximum_batch_size}
        '''
        result = self._values.get("maximum_batch_size")
        assert result is not None, "Required property 'maximum_batch_size' is missing"
        return typing.cast("SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize", result)

    @builtins.property
    def wait_interval_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#wait_interval_in_seconds SagemakerEndpoint#wait_interval_in_seconds}.'''
        result = self._values.get("wait_interval_in_seconds")
        assert result is not None, "Required property 'wait_interval_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def maximum_execution_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#maximum_execution_timeout_in_seconds SagemakerEndpoint#maximum_execution_timeout_in_seconds}.'''
        result = self._values.get("maximum_execution_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rollback_maximum_batch_size(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"]:
        '''rollback_maximum_batch_size block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#rollback_maximum_batch_size SagemakerEndpoint#rollback_maximum_batch_size}
        '''
        result = self._values.get("rollback_maximum_batch_size")
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigRollingUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18636c44317e9998f04fd7ad4440bb8554333cc1bd2d369c2803890963b36d02)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0957259654ab0ac97acf3e9790f0cffa43670e660b193f3ab2c6aabe5e9d1250)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96caeebcade9648eb5b8d3d60777e4958c6605f1a7d85e34a6896b6f018bd7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5e1f29ea8e2ca050232e585c8487caadca79d24eb9ec87e0fbec5cf8550781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd57e4dc6cd6a158aef3f3f49e12dccfda2c1aca4ec1a93f7cb6be55a9708c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__918043eb2e0561e0e22645e2ac8ac414c442fdb19672651102b7f7e53199f433)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaximumBatchSize")
    def put_maximum_batch_size(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putMaximumBatchSize", [value_]))

    @jsii.member(jsii_name="putRollbackMaximumBatchSize")
    def put_rollback_maximum_batch_size(
        self,
        *,
        type: builtins.str,
        value: jsii.Number,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        value_ = SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putRollbackMaximumBatchSize", [value_]))

    @jsii.member(jsii_name="resetMaximumExecutionTimeoutInSeconds")
    def reset_maximum_execution_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumExecutionTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetRollbackMaximumBatchSize")
    def reset_rollback_maximum_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollbackMaximumBatchSize", []))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchSize")
    def maximum_batch_size(
        self,
    ) -> SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference:
        return typing.cast(SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference, jsii.get(self, "maximumBatchSize"))

    @builtins.property
    @jsii.member(jsii_name="rollbackMaximumBatchSize")
    def rollback_maximum_batch_size(
        self,
    ) -> "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference":
        return typing.cast("SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference", jsii.get(self, "rollbackMaximumBatchSize"))

    @builtins.property
    @jsii.member(jsii_name="maximumBatchSizeInput")
    def maximum_batch_size_input(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize], jsii.get(self, "maximumBatchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSecondsInput")
    def maximum_execution_timeout_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumExecutionTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackMaximumBatchSizeInput")
    def rollback_maximum_batch_size_input(
        self,
    ) -> typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"]:
        return typing.cast(typing.Optional["SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize"], jsii.get(self, "rollbackMaximumBatchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSecondsInput")
    def wait_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionTimeoutInSeconds")
    def maximum_execution_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumExecutionTimeoutInSeconds"))

    @maximum_execution_timeout_in_seconds.setter
    def maximum_execution_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def14d0ee8d2deb27b96db1598082d6007caa3f1ad93eef81387f428efcb90c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumExecutionTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitIntervalInSeconds")
    def wait_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitIntervalInSeconds"))

    @wait_interval_in_seconds.setter
    def wait_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a22fb0019370f5df20a8169c0716b0834f5061a6ae3d6c62648c902486c85fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f6db0ec7493c9dc8b1c0b29d216feb12993dcbcd6f0c11b1ccdffc24ba58ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize:
    def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fb47c4cfd7d104e3b8ac2b87129696e94e934a75365ec76b7539fb6c210d08)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#type SagemakerEndpoint#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/sagemaker_endpoint#value SagemakerEndpoint#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerEndpoint.SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c8a4b2efaa9c0fb6569b7dde24045e05b476a2663fa9995c715cdbd3afc8365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0440e6babfe7c7d06c1e1c53a43bd8166fd9cf3dfc7e6584a27cb4d3a80b03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e0d879b8c9c2754ba520f1bffc8d32b16f722a9b42637c36ef8a6163f048b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize]:
        return typing.cast(typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e2842065362d139442a506031e0899445242949849a12127f5eef0a96fa7b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SagemakerEndpoint",
    "SagemakerEndpointConfig",
    "SagemakerEndpointDeploymentConfig",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfiguration",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsList",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarmsOutputReference",
    "SagemakerEndpointDeploymentConfigAutoRollbackConfigurationOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySizeOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSizeOutputReference",
    "SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationOutputReference",
    "SagemakerEndpointDeploymentConfigOutputReference",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicy",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSizeOutputReference",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyOutputReference",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize",
    "SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSizeOutputReference",
]

publication.publish()

def _typecheckingstub__73f65893232cfaebf6a9a73cd365a7ffd80eb653cd8209fe984635e3a6a1b59a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    endpoint_config_name: builtins.str,
    deployment_config: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__05d5d70111730674ea7380f9e53ccf7e032f36b845194de36f06c8cf71d734c6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bf3d96da257f418cf4702d469b33defee477561a12ad88088e0e3c7a1054db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8012c26c4502457d0f6a0a3bf557543bb9d35ceec43d2fd133a6d19daebc154(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ec521d0ace0a544c539205e5952afb0abe666ff3e10b974990724fa3556b11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7327f94205a1cb85798bb71a9c7e49a8c1fa71702eed2f0d96babd08b4b70a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958237648b846fbbe33e0f7f6bc14946b8debe70148e8f2b1bdb55308c7498c2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe31387b58c6495c7d82b9ac62f6f083a142f69c062023216433474ea7057eb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    endpoint_config_name: builtins.str,
    deployment_config: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8914a0032c8846d5b17112129517b3a42334214284070e8e7ebeb39e21825dc1(
    *,
    auto_rollback_configuration: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    blue_green_update_policy: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rolling_update_policy: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigRollingUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60403c3aed1f457890e8a4ce5f7be711a6e2ec579d3f2b517260cc3fb502bd20(
    *,
    alarms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9ab3ba1a3f6ca04690c5ba65a404cad8094043f1a58910098e08ad383d3d63(
    *,
    alarm_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060a5194fb51c634aac64b61f9467622c8c0b0a7afc0e4847effc17a486da947(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676a28fc8bbc84189435e4a45ea0adc8935b1c36ea897c0b4554af01a2d4de0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dc1664423d77402b69e23655bc8a11197c69912452ddea3bd804fc35ebb57d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53a49488279eaf4cdefed89c1cc19565ba83c6c2e3156d78ea32fc770f1b972(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db2152c19758380297656673867ca553f5bb60aa87b09af7ae98c54a67f890a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf7301b733dc5b836b88a5964843d193aaa7590a245ac8819de1e3fae73bc7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6f2aeadc3e8c0e16d79a413bbabe301b8f926a0adaf241a624a9e71b0d6780(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2b98730757fe3b076325f79987c44dcf112e61306304ac92ac537c2acaad40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5221d5f8dafa47a3ef921101488f0fe385236cde42b38efcb451fdd85d36339c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21d09a513c257f32ef204b6423b962fc11d6210bc856145ef063d0902e7a38b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7484e910acb5102134537020ab0fa136b54e3694dbb10cb0a6febe72971408d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerEndpointDeploymentConfigAutoRollbackConfigurationAlarms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9935f9bb6ba5bd18568829661b4961b6ac9773897ae9338c9e9501b056772785(
    value: typing.Optional[SagemakerEndpointDeploymentConfigAutoRollbackConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bfaa5c103019072f32cf7a550ed0f0123078c1c0d9deff4c55c21c97e5876a(
    *,
    traffic_routing_configuration: typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration, typing.Dict[builtins.str, typing.Any]],
    maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    termination_wait_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773681bd7da06ac22fe8353eb0b62f2cc299eb8cf59ffff9f90ae3cb9806237f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337fcc1a810c7b999c726accdea7121635ee37e803b002e36cd4ac134aedb026(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4bc670867133a7c1f53209ad4459c0f162d7bd6196d493f86eae02bc6b093d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab770fc9a59c971349e1d08bc96de96017b6509716339c73a060361b9c7c3f1(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b45034a5b5502ed9d84a0826b33300763a0fee02ec01a98b4a8d48fa9092e6(
    *,
    type: builtins.str,
    wait_interval_in_seconds: jsii.Number,
    canary_size: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize, typing.Dict[builtins.str, typing.Any]]] = None,
    linear_step_size: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11b81974a8369bf514168284786081803fb8d72164c512128abe15e42be02c5(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f4b922cabb9d0379fe200e1ea72c6efa7fedd91ac5ab7d0e5f08e62f5832a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37a223c46c96af19f7fffec98fd5956c55cc6a28cc39fa7746162c7c7695b1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d69afceb474f235cfafcf5cd54d73327ccfe6b07247ed83a3ff34f2cd7d85e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6459b1daf0049f94b9694d0c5f43c4aaeb68b17352e439948bb32ee3c6ff204(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationCanarySize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1814d4e0bbd76af30a367391aa4f08cebec6aed978c9935e3faa2edbd95b9f71(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dccee116b1c54d26095742f9d5137af954373d11c1ea7396b25b65f27fe4a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf20a23ce48a3001b35ae311a7a1958fcf3a0231491009ed159d89ab522cf8f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930f715edea7a2d4474e43edbabd109bfa506710b6d2ed30ade130256f398f63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dff398ffad681de9e4ee58a414e159ea055d2c97077652361929c8dbd80af5(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfigurationLinearStepSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd912f784cbdb47276bdf51b6fc62f3781ea095668221fa64aa3c5db64903ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5668f64962dffff543cb2ad87f8cff2eebe71273e2c45321c375c8167b87aef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316fa970793c02df64db0fcb77190630e102d5dcb563d3c5dab3856929e874ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26569d7aa73c8b9fc3fa009ec63f013a05a23927a35c0109994dd8c84014a7c8(
    value: typing.Optional[SagemakerEndpointDeploymentConfigBlueGreenUpdatePolicyTrafficRoutingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad4990208d0b0ed7ed4c46f593461121ea09606b37018886610f04521da42d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df46696b265cbf2821c0671c5a91b70e8e86246a110b86dc645b2d438c2233a5(
    value: typing.Optional[SagemakerEndpointDeploymentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba402b4d85beab8df1c283f31a318357905cee63efdace6418d3f16a907cbeda(
    *,
    maximum_batch_size: typing.Union[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize, typing.Dict[builtins.str, typing.Any]],
    wait_interval_in_seconds: jsii.Number,
    maximum_execution_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    rollback_maximum_batch_size: typing.Optional[typing.Union[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18636c44317e9998f04fd7ad4440bb8554333cc1bd2d369c2803890963b36d02(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0957259654ab0ac97acf3e9790f0cffa43670e660b193f3ab2c6aabe5e9d1250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96caeebcade9648eb5b8d3d60777e4958c6605f1a7d85e34a6896b6f018bd7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5e1f29ea8e2ca050232e585c8487caadca79d24eb9ec87e0fbec5cf8550781(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd57e4dc6cd6a158aef3f3f49e12dccfda2c1aca4ec1a93f7cb6be55a9708c4(
    value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyMaximumBatchSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918043eb2e0561e0e22645e2ac8ac414c442fdb19672651102b7f7e53199f433(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def14d0ee8d2deb27b96db1598082d6007caa3f1ad93eef81387f428efcb90c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a22fb0019370f5df20a8169c0716b0834f5061a6ae3d6c62648c902486c85fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f6db0ec7493c9dc8b1c0b29d216feb12993dcbcd6f0c11b1ccdffc24ba58ef(
    value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fb47c4cfd7d104e3b8ac2b87129696e94e934a75365ec76b7539fb6c210d08(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8a4b2efaa9c0fb6569b7dde24045e05b476a2663fa9995c715cdbd3afc8365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0440e6babfe7c7d06c1e1c53a43bd8166fd9cf3dfc7e6584a27cb4d3a80b03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e0d879b8c9c2754ba520f1bffc8d32b16f722a9b42637c36ef8a6163f048b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e2842065362d139442a506031e0899445242949849a12127f5eef0a96fa7b2(
    value: typing.Optional[SagemakerEndpointDeploymentConfigRollingUpdatePolicyRollbackMaximumBatchSize],
) -> None:
    """Type checking stubs"""
    pass
