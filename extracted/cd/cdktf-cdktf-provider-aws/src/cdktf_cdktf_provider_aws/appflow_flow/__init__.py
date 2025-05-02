r'''
# `aws_appflow_flow`

Refer to the Terraform Registry for docs: [`aws_appflow_flow`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow).
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


class AppflowFlow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlow",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow aws_appflow_flow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowDestinationFlowConfig", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        source_flow_config: typing.Union["AppflowFlowSourceFlowConfig", typing.Dict[builtins.str, typing.Any]],
        task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTask", typing.Dict[builtins.str, typing.Any]]]],
        trigger_config: typing.Union["AppflowFlowTriggerConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        metadata_catalog_config: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow aws_appflow_flow} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_flow_config: destination_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#destination_flow_config AppflowFlow#destination_flow_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#name AppflowFlow#name}.
        :param source_flow_config: source_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_flow_config AppflowFlow#source_flow_config}
        :param task: task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#task AppflowFlow#task}
        :param trigger_config: trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_config AppflowFlow#trigger_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#description AppflowFlow#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id AppflowFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#kms_arn AppflowFlow#kms_arn}.
        :param metadata_catalog_config: metadata_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#metadata_catalog_config AppflowFlow#metadata_catalog_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#tags AppflowFlow#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#tags_all AppflowFlow#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d8912010333000454cbf0c65b1f6e3ac0661fc69209522717ea8a534f14c34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppflowFlowConfig(
            destination_flow_config=destination_flow_config,
            name=name,
            source_flow_config=source_flow_config,
            task=task,
            trigger_config=trigger_config,
            description=description,
            id=id,
            kms_arn=kms_arn,
            metadata_catalog_config=metadata_catalog_config,
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
        '''Generates CDKTF code for importing a AppflowFlow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppflowFlow to import.
        :param import_from_id: The id of the existing AppflowFlow that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppflowFlow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1529ec5157a8972f07dd5e138b3529e9a2f2706da2407a15f150d02dede65dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationFlowConfig")
    def put_destination_flow_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowDestinationFlowConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbc5880479a4f92b9a8bc4df33440645ee2f3078e82cc44e8edbab333de33a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinationFlowConfig", [value]))

    @jsii.member(jsii_name="putMetadataCatalogConfig")
    def put_metadata_catalog_config(
        self,
        *,
        glue_data_catalog: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfigGlueDataCatalog", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param glue_data_catalog: glue_data_catalog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#glue_data_catalog AppflowFlow#glue_data_catalog}
        '''
        value = AppflowFlowMetadataCatalogConfig(glue_data_catalog=glue_data_catalog)

        return typing.cast(None, jsii.invoke(self, "putMetadataCatalogConfig", [value]))

    @jsii.member(jsii_name="putSourceFlowConfig")
    def put_source_flow_config(
        self,
        *,
        connector_type: builtins.str,
        source_connector_properties: typing.Union["AppflowFlowSourceFlowConfigSourceConnectorProperties", typing.Dict[builtins.str, typing.Any]],
        api_version: typing.Optional[builtins.str] = None,
        connector_profile_name: typing.Optional[builtins.str] = None,
        incremental_pull_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigIncrementalPullConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.
        :param source_connector_properties: source_connector_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_connector_properties AppflowFlow#source_connector_properties}
        :param api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.
        :param connector_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.
        :param incremental_pull_config: incremental_pull_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#incremental_pull_config AppflowFlow#incremental_pull_config}
        '''
        value = AppflowFlowSourceFlowConfig(
            connector_type=connector_type,
            source_connector_properties=source_connector_properties,
            api_version=api_version,
            connector_profile_name=connector_profile_name,
            incremental_pull_config=incremental_pull_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceFlowConfig", [value]))

    @jsii.member(jsii_name="putTask")
    def put_task(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTask", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9089c0d28179f8ee7ad2bac5ee19f1688d1bed507421e112a5b59b8d55512d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTask", [value]))

    @jsii.member(jsii_name="putTriggerConfig")
    def put_trigger_config(
        self,
        *,
        trigger_type: builtins.str,
        trigger_properties: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trigger_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_type AppflowFlow#trigger_type}.
        :param trigger_properties: trigger_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_properties AppflowFlow#trigger_properties}
        '''
        value = AppflowFlowTriggerConfig(
            trigger_type=trigger_type, trigger_properties=trigger_properties
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsArn")
    def reset_kms_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsArn", []))

    @jsii.member(jsii_name="resetMetadataCatalogConfig")
    def reset_metadata_catalog_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataCatalogConfig", []))

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
    @jsii.member(jsii_name="destinationFlowConfig")
    def destination_flow_config(self) -> "AppflowFlowDestinationFlowConfigList":
        return typing.cast("AppflowFlowDestinationFlowConfigList", jsii.get(self, "destinationFlowConfig"))

    @builtins.property
    @jsii.member(jsii_name="flowStatus")
    def flow_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flowStatus"))

    @builtins.property
    @jsii.member(jsii_name="metadataCatalogConfig")
    def metadata_catalog_config(
        self,
    ) -> "AppflowFlowMetadataCatalogConfigOutputReference":
        return typing.cast("AppflowFlowMetadataCatalogConfigOutputReference", jsii.get(self, "metadataCatalogConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceFlowConfig")
    def source_flow_config(self) -> "AppflowFlowSourceFlowConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigOutputReference", jsii.get(self, "sourceFlowConfig"))

    @builtins.property
    @jsii.member(jsii_name="task")
    def task(self) -> "AppflowFlowTaskList":
        return typing.cast("AppflowFlowTaskList", jsii.get(self, "task"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfig")
    def trigger_config(self) -> "AppflowFlowTriggerConfigOutputReference":
        return typing.cast("AppflowFlowTriggerConfigOutputReference", jsii.get(self, "triggerConfig"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFlowConfigInput")
    def destination_flow_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]]], jsii.get(self, "destinationFlowConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsArnInput")
    def kms_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArnInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataCatalogConfigInput")
    def metadata_catalog_config_input(
        self,
    ) -> typing.Optional["AppflowFlowMetadataCatalogConfig"]:
        return typing.cast(typing.Optional["AppflowFlowMetadataCatalogConfig"], jsii.get(self, "metadataCatalogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFlowConfigInput")
    def source_flow_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfig"], jsii.get(self, "sourceFlowConfigInput"))

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
    @jsii.member(jsii_name="taskInput")
    def task_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]]], jsii.get(self, "taskInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfigInput")
    def trigger_config_input(self) -> typing.Optional["AppflowFlowTriggerConfig"]:
        return typing.cast(typing.Optional["AppflowFlowTriggerConfig"], jsii.get(self, "triggerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43144f57e20621519e3bbac26bbf52308b7e6cbadee51b6a6140addc6312080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a4362db5d23ff9333b9e1633a715bf887e897ca3fc2de5422abbd83f47676a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30917fe220eb051a92c4a106c5e3c7be2df8c52a89344f6c71b4c3b079384034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99eaebb35798a2d45c68288b85ea45facbb40c9040ec66295a3d5fc237eefaa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1ea8d78a2167a706c73485d6fa479b2a32c7f02ff5c28805f98e29a5ee5e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22626e2259c7a951b2e71f2282e68f98c3647c10c60c231228b6a1317d79c82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination_flow_config": "destinationFlowConfig",
        "name": "name",
        "source_flow_config": "sourceFlowConfig",
        "task": "task",
        "trigger_config": "triggerConfig",
        "description": "description",
        "id": "id",
        "kms_arn": "kmsArn",
        "metadata_catalog_config": "metadataCatalogConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class AppflowFlowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowDestinationFlowConfig", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        source_flow_config: typing.Union["AppflowFlowSourceFlowConfig", typing.Dict[builtins.str, typing.Any]],
        task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTask", typing.Dict[builtins.str, typing.Any]]]],
        trigger_config: typing.Union["AppflowFlowTriggerConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        metadata_catalog_config: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param destination_flow_config: destination_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#destination_flow_config AppflowFlow#destination_flow_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#name AppflowFlow#name}.
        :param source_flow_config: source_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_flow_config AppflowFlow#source_flow_config}
        :param task: task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#task AppflowFlow#task}
        :param trigger_config: trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_config AppflowFlow#trigger_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#description AppflowFlow#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id AppflowFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#kms_arn AppflowFlow#kms_arn}.
        :param metadata_catalog_config: metadata_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#metadata_catalog_config AppflowFlow#metadata_catalog_config}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#tags AppflowFlow#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#tags_all AppflowFlow#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(source_flow_config, dict):
            source_flow_config = AppflowFlowSourceFlowConfig(**source_flow_config)
        if isinstance(trigger_config, dict):
            trigger_config = AppflowFlowTriggerConfig(**trigger_config)
        if isinstance(metadata_catalog_config, dict):
            metadata_catalog_config = AppflowFlowMetadataCatalogConfig(**metadata_catalog_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5fd331020a945882c9cc3561daf42aa20a0e2701f2c2ccd72ef3ed193a2f30)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination_flow_config", value=destination_flow_config, expected_type=type_hints["destination_flow_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_flow_config", value=source_flow_config, expected_type=type_hints["source_flow_config"])
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument trigger_config", value=trigger_config, expected_type=type_hints["trigger_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
            check_type(argname="argument metadata_catalog_config", value=metadata_catalog_config, expected_type=type_hints["metadata_catalog_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_flow_config": destination_flow_config,
            "name": name,
            "source_flow_config": source_flow_config,
            "task": task,
            "trigger_config": trigger_config,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn
        if metadata_catalog_config is not None:
            self._values["metadata_catalog_config"] = metadata_catalog_config
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
    def destination_flow_config(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]]:
        '''destination_flow_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#destination_flow_config AppflowFlow#destination_flow_config}
        '''
        result = self._values.get("destination_flow_config")
        assert result is not None, "Required property 'destination_flow_config' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#name AppflowFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_flow_config(self) -> "AppflowFlowSourceFlowConfig":
        '''source_flow_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_flow_config AppflowFlow#source_flow_config}
        '''
        result = self._values.get("source_flow_config")
        assert result is not None, "Required property 'source_flow_config' is missing"
        return typing.cast("AppflowFlowSourceFlowConfig", result)

    @builtins.property
    def task(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]]:
        '''task block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#task AppflowFlow#task}
        '''
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]], result)

    @builtins.property
    def trigger_config(self) -> "AppflowFlowTriggerConfig":
        '''trigger_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_config AppflowFlow#trigger_config}
        '''
        result = self._values.get("trigger_config")
        assert result is not None, "Required property 'trigger_config' is missing"
        return typing.cast("AppflowFlowTriggerConfig", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#description AppflowFlow#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id AppflowFlow#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#kms_arn AppflowFlow#kms_arn}.'''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_catalog_config(
        self,
    ) -> typing.Optional["AppflowFlowMetadataCatalogConfig"]:
        '''metadata_catalog_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#metadata_catalog_config AppflowFlow#metadata_catalog_config}
        '''
        result = self._values.get("metadata_catalog_config")
        return typing.cast(typing.Optional["AppflowFlowMetadataCatalogConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#tags AppflowFlow#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#tags_all AppflowFlow#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connector_type": "connectorType",
        "destination_connector_properties": "destinationConnectorProperties",
        "api_version": "apiVersion",
        "connector_profile_name": "connectorProfileName",
    },
)
class AppflowFlowDestinationFlowConfig:
    def __init__(
        self,
        *,
        connector_type: builtins.str,
        destination_connector_properties: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorProperties", typing.Dict[builtins.str, typing.Any]],
        api_version: typing.Optional[builtins.str] = None,
        connector_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.
        :param destination_connector_properties: destination_connector_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#destination_connector_properties AppflowFlow#destination_connector_properties}
        :param api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.
        :param connector_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.
        '''
        if isinstance(destination_connector_properties, dict):
            destination_connector_properties = AppflowFlowDestinationFlowConfigDestinationConnectorProperties(**destination_connector_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc750cf8766c07181e8efe398a097ef2e21accdf60c72e03030ee3ca081aaa7)
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument destination_connector_properties", value=destination_connector_properties, expected_type=type_hints["destination_connector_properties"])
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_type": connector_type,
            "destination_connector_properties": destination_connector_properties,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if connector_profile_name is not None:
            self._values["connector_profile_name"] = connector_profile_name

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.'''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_connector_properties(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorProperties":
        '''destination_connector_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#destination_connector_properties AppflowFlow#destination_connector_properties}
        '''
        result = self._values.get("destination_connector_properties")
        assert result is not None, "Required property 'destination_connector_properties' is missing"
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorProperties", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.'''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_profile_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.'''
        result = self._values.get("connector_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorProperties",
    jsii_struct_bases=[],
    name_mapping={
        "custom_connector": "customConnector",
        "customer_profiles": "customerProfiles",
        "event_bridge": "eventBridge",
        "honeycode": "honeycode",
        "lookout_metrics": "lookoutMetrics",
        "marketo": "marketo",
        "redshift": "redshift",
        "s3": "s3",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "snowflake": "snowflake",
        "upsolver": "upsolver",
        "zendesk": "zendesk",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorProperties:
    def __init__(
        self,
        *,
        custom_connector: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        customer_profiles: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles", typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge", typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode", typing.Dict[builtins.str, typing.Any]]] = None,
        lookout_metrics: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        upsolver: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param customer_profiles: customer_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#customer_profiles AppflowFlow#customer_profiles}
        :param event_bridge: event_bridge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#event_bridge AppflowFlow#event_bridge}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#honeycode AppflowFlow#honeycode}
        :param lookout_metrics: lookout_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#lookout_metrics AppflowFlow#lookout_metrics}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#redshift AppflowFlow#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#snowflake AppflowFlow#snowflake}
        :param upsolver: upsolver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#upsolver AppflowFlow#upsolver}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        if isinstance(custom_connector, dict):
            custom_connector = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector(**custom_connector)
        if isinstance(customer_profiles, dict):
            customer_profiles = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles(**customer_profiles)
        if isinstance(event_bridge, dict):
            event_bridge = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge(**event_bridge)
        if isinstance(honeycode, dict):
            honeycode = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode(**honeycode)
        if isinstance(lookout_metrics, dict):
            lookout_metrics = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics(**lookout_metrics)
        if isinstance(marketo, dict):
            marketo = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo(**marketo)
        if isinstance(redshift, dict):
            redshift = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift(**redshift)
        if isinstance(s3, dict):
            s3 = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3(**s3)
        if isinstance(salesforce, dict):
            salesforce = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData(**sapo_data)
        if isinstance(snowflake, dict):
            snowflake = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake(**snowflake)
        if isinstance(upsolver, dict):
            upsolver = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver(**upsolver)
        if isinstance(zendesk, dict):
            zendesk = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8432ec939175200818ab9360fb66f1a016217afff588107a294823237e6cb3f)
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument customer_profiles", value=customer_profiles, expected_type=type_hints["customer_profiles"])
            check_type(argname="argument event_bridge", value=event_bridge, expected_type=type_hints["event_bridge"])
            check_type(argname="argument honeycode", value=honeycode, expected_type=type_hints["honeycode"])
            check_type(argname="argument lookout_metrics", value=lookout_metrics, expected_type=type_hints["lookout_metrics"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument upsolver", value=upsolver, expected_type=type_hints["upsolver"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if customer_profiles is not None:
            self._values["customer_profiles"] = customer_profiles
        if event_bridge is not None:
            self._values["event_bridge"] = event_bridge
        if honeycode is not None:
            self._values["honeycode"] = honeycode
        if lookout_metrics is not None:
            self._values["lookout_metrics"] = lookout_metrics
        if marketo is not None:
            self._values["marketo"] = marketo
        if redshift is not None:
            self._values["redshift"] = redshift
        if s3 is not None:
            self._values["s3"] = s3
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if upsolver is not None:
            self._values["upsolver"] = upsolver
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector"], result)

    @builtins.property
    def customer_profiles(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles"]:
        '''customer_profiles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#customer_profiles AppflowFlow#customer_profiles}
        '''
        result = self._values.get("customer_profiles")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles"], result)

    @builtins.property
    def event_bridge(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge"]:
        '''event_bridge block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#event_bridge AppflowFlow#event_bridge}
        '''
        result = self._values.get("event_bridge")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge"], result)

    @builtins.property
    def honeycode(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode"]:
        '''honeycode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#honeycode AppflowFlow#honeycode}
        '''
        result = self._values.get("honeycode")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode"], result)

    @builtins.property
    def lookout_metrics(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics"]:
        '''lookout_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#lookout_metrics AppflowFlow#lookout_metrics}
        '''
        result = self._values.get("lookout_metrics")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo"], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#redshift AppflowFlow#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"], result)

    @builtins.property
    def snowflake(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#snowflake AppflowFlow#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"], result)

    @builtins.property
    def upsolver(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"]:
        '''upsolver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#upsolver AppflowFlow#upsolver}
        '''
        result = self._values.get("upsolver")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "entity_name": "entityName",
        "custom_properties": "customProperties",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector:
    def __init__(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c260ff2ee9c096e40266ee68a31f50933e445d1717c1aecf73f6d03affd25a2a)
            check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_name": entity_name,
        }
        if custom_properties is not None:
            self._values["custom_properties"] = custom_properties
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def entity_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.'''
        result = self._values.get("entity_name")
        assert result is not None, "Required property 'entity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.'''
        result = self._values.get("custom_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002a6807352cf6cf096dbda89df004e19690f8d06251c6c1dce0e2658b70476a)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6d64b5a760f4a27b92723ce062ebe8e7e28b2f363c01e4c8d07517e1be3e0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac3291f9b1814df3d9a2acd63a1492904a929a632126c6e555c589ac4ddaf83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99de399e1354c84ce95d9cd10a347363e4fa7c6b891c4b200f42847620873558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a6b6e2227103d1b7a264dc9a0260eab88cf59cf4aaccfeb45b876b9267fadd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18bd98288ac88df5458effdacd5aea6bb190eb709b57160eeafe4c02fecdd0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33458563f58e501465332440a9d055246b8faea5457088542ba7e54e2ec97646)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetCustomProperties")
    def reset_custom_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomProperties", []))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="customPropertiesInput")
    def custom_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="entityNameInput")
    def entity_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityNameInput"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customProperties")
    def custom_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customProperties"))

    @custom_properties.setter
    def custom_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9edcfa168a31273dbb85109f4b2f9c0f5e3294aa2a091a488f184a36840dd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entityName")
    def entity_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityName"))

    @entity_name.setter
    def entity_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abdbf2b78ef547594c864eb142fa39b47819ae1f5124641d879521cc25dd354d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d3694890146273c796f7a42bf6cb9f4236fd15a7f4ee0e655d055fb5b6c19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814ab467c242749c549d23e305c6cea4edf688a5284194eee01acad12a394e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4906f72fdc8edbd1c354817bb65f51a97a0280bea4c16b651a19d8d79545ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles",
    jsii_struct_bases=[],
    name_mapping={"domain_name": "domainName", "object_type_name": "objectTypeName"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        object_type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#domain_name AppflowFlow#domain_name}.
        :param object_type_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_type_name AppflowFlow#object_type_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd40c27555f3b981d849934f1bb8f4041533a8c5e2571876beb17b002e87a4f)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument object_type_name", value=object_type_name, expected_type=type_hints["object_type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if object_type_name is not None:
            self._values["object_type_name"] = object_type_name

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#domain_name AppflowFlow#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_type_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_type_name AppflowFlow#object_type_name}.'''
        result = self._values.get("object_type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a352abe28d40d9f39d7cc37cbdc50bd2f73925d22f7fb8e6183100e174343dbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetObjectTypeName")
    def reset_object_type_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectTypeName", []))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypeNameInput")
    def object_type_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c5921c8a3235fc3d8f9bbb427639e122493b4ce85c552f039e2630b2b37dcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypeName")
    def object_type_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypeName"))

    @object_type_name.setter
    def object_type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35969b779f23675ffcebf0750fddc80eea827775cbb2037b4a26b39a36f5c880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae816928e81255454bb85b720285faef110332d2c20706af0153bc0ff903e875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge",
    jsii_struct_bases=[],
    name_mapping={"object": "object", "error_handling_config": "errorHandlingConfig"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9511721f765c7f4110f5cbe3dd4a39994ef8e5174af9aaf4cec5dcac147b41c)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4184c3515a58d1f5be78cbfc6e0b456a90f5d4bb566ed80e1b064ae8a449f33a)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4576b4833efc9bb003f86f23fb3b9cc1d96c88a011f9939e5e70dafdc8db4532)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8878456f0009ec7d86f01e82ecac475e44c8767a4ee89a774f1e0b622b1aa931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbed43e13503f241cf855ccdafcf9c202c4b2d4d0766586e92c3bec7c713796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__451113c9b550c47f27529cac89de0038dac44db64d26f9d734093c2aa715e3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ea33bad3287ecc66aae6caf8c623aa81ead6ae084d4f0de257cfe2e7a06e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2cd5d7fbad6e307aa3ceb8bf81d5a8d7c6a73544f9659da9b1429667657cc9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2a66b2f40229c96d75bf5cccb56358e8138b8c67812016aaf8f5b6f57412e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ca4bec7cc4a7502192ed535a6d7a70007e96d76f6d5b1208628ceb3372f638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode",
    jsii_struct_bases=[],
    name_mapping={"object": "object", "error_handling_config": "errorHandlingConfig"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9607350e66f9d4c73de559e3d834ae768b8afbdfea37723e6f7a6011a96390c2)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884504dc6d1279515b47026cf454e4648ccfbc51d5bece5fa7620e4e61e20d88)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5b16c89e1d9f75c3297ce8aeffe2c3ba2e6035c412caccb97c7af7212f9c0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb2125f4dfb5928dc9371eac809881cb4afa7f8cb9f8ec3dfc630626f44a518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f836c2085696ad6344a1ab3fd67e4974f3dddd2e6643af7b8677546869c6cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d319ef6d33770dd4e2fd1c01932723cd70f17e210080bb8424762f9938c6a571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d33c9f033f8411b2350b08e38eecb1b9aed0cd46851e1369584ad07bc208e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7325aa232a697122dbc21a0c80e47d66ecb56dc3b42c6dd49adb1be3e2b91b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d577e4d097a5077f5a9c238540fa6bda2fa13e132efe3d4b2dfe4bdf33f20cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac70bd9cc6bf155e3a486bd2ae0f000abbc76ccc8f83e0467c6e11478d46badb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdb8dffd28f2d83ed5c87a77e4f89fb7e6944392116b22a1304de34e785bd3a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5525588879197e15f3bde180985e662e809560f16ed3629e554851f66ff5e92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo",
    jsii_struct_bases=[],
    name_mapping={"object": "object", "error_handling_config": "errorHandlingConfig"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b37f3c2b6f30fc0156e96a44a5d068362647b3a1b80dd6cfbdad737b84b757)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfdce1e90419b7c1196d86468d4e01fd14afec86ad3eeb70ecd0c64cf920c3fd)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6722a00bce1c1d5abcba312d746777b5afcde66e6566108128321d0d2a9c452)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf8986ac2602f874236c5e6d5591314dfd08834e5e9d164b8249e00f02499ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8009e0a305864018f7378ff409c2f5a5107bb6f015029ad69684b45fb801bdf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2300d390700b04569cee5660da97f31cf7008d26e85ec10c1be18b507854fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9e59ef239b5b66328c9fad106161d3db937e8b785bb0c4ef850bb43b89823a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7a6d7d6131958febf42a2061e616a51fb8380398fe4465f6a24fe3e88fd0d34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1cacf282b11d59c5258b236a2634c95bd26e5fa7ff3559dab2d065d4158ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2ca4a49cefc054f233348fd7ce3bc96909949f58e5747344821f21d177c725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1573fbd4b55788ccd1a1a67eb621dd6914b2a02788a637f959951669b492bfb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector(
            entity_name=entity_name,
            custom_properties=custom_properties,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putCustomerProfiles")
    def put_customer_profiles(
        self,
        *,
        domain_name: builtins.str,
        object_type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#domain_name AppflowFlow#domain_name}.
        :param object_type_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_type_name AppflowFlow#object_type_name}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles(
            domain_name=domain_name, object_type_name=object_type_name
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerProfiles", [value]))

    @jsii.member(jsii_name="putEventBridge")
    def put_event_bridge(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge(
            object=object, error_handling_config=error_handling_config
        )

        return typing.cast(None, jsii.invoke(self, "putEventBridge", [value]))

    @jsii.member(jsii_name="putHoneycode")
    def put_honeycode(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode(
            object=object, error_handling_config=error_handling_config
        )

        return typing.cast(None, jsii.invoke(self, "putHoneycode", [value]))

    @jsii.member(jsii_name="putLookoutMetrics")
    def put_lookout_metrics(self) -> None:
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics()

        return typing.cast(None, jsii.invoke(self, "putLookoutMetrics", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo(
            object=object, error_handling_config=error_handling_config
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift(
            intermediate_bucket_name=intermediate_bucket_name,
            object=object,
            bucket_prefix=bucket_prefix,
            error_handling_config=error_handling_config,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        s3_output_format_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            s3_output_format_config=s3_output_format_config,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce(
            object=object,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        object_path: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_response_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param success_response_handling_config: success_response_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#success_response_handling_config AppflowFlow#success_response_handling_config}
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData(
            object_path=object_path,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            success_response_handling_config=success_response_handling_config,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake(
            intermediate_bucket_name=intermediate_bucket_name,
            object=object,
            bucket_prefix=bucket_prefix,
            error_handling_config=error_handling_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putUpsolver")
    def put_upsolver(
        self,
        *,
        bucket_name: builtins.str,
        s3_output_format_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]],
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver(
            bucket_name=bucket_name,
            s3_output_format_config=s3_output_format_config,
            bucket_prefix=bucket_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putUpsolver", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk(
            object=object,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putZendesk", [value]))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetCustomerProfiles")
    def reset_customer_profiles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerProfiles", []))

    @jsii.member(jsii_name="resetEventBridge")
    def reset_event_bridge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventBridge", []))

    @jsii.member(jsii_name="resetHoneycode")
    def reset_honeycode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoneycode", []))

    @jsii.member(jsii_name="resetLookoutMetrics")
    def reset_lookout_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookoutMetrics", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetUpsolver")
    def reset_upsolver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpsolver", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="customerProfiles")
    def customer_profiles(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference, jsii.get(self, "customerProfiles"))

    @builtins.property
    @jsii.member(jsii_name="eventBridge")
    def event_bridge(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference, jsii.get(self, "eventBridge"))

    @builtins.property
    @jsii.member(jsii_name="honeycode")
    def honeycode(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference, jsii.get(self, "honeycode"))

    @builtins.property
    @jsii.member(jsii_name="lookoutMetrics")
    def lookout_metrics(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference, jsii.get(self, "lookoutMetrics"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="upsolver")
    def upsolver(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference", jsii.get(self, "upsolver"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="customerProfilesInput")
    def customer_profiles_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles], jsii.get(self, "customerProfilesInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeInput")
    def event_bridge_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge], jsii.get(self, "eventBridgeInput"))

    @builtins.property
    @jsii.member(jsii_name="honeycodeInput")
    def honeycode_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode], jsii.get(self, "honeycodeInput"))

    @builtins.property
    @jsii.member(jsii_name="lookoutMetricsInput")
    def lookout_metrics_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics], jsii.get(self, "lookoutMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="upsolverInput")
    def upsolver_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"], jsii.get(self, "upsolverInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb036a4729236edfcf1539faa27822cc81468a19b7e6e398bd0ecd61e66c8c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "intermediate_bucket_name": "intermediateBucketName",
        "object": "object",
        "bucket_prefix": "bucketPrefix",
        "error_handling_config": "errorHandlingConfig",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift:
    def __init__(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc3a2939798abf0bbb0680af559bdc16656d1ad3f0becbfef242b9b2bf85d36)
            check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "intermediate_bucket_name": intermediate_bucket_name,
            "object": object,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def intermediate_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.'''
        result = self._values.get("intermediate_bucket_name")
        assert result is not None, "Required property 'intermediate_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c7983a9f4aeb6fa8badd6ae8a422981379a724f96b916ba2f2119766f5a650)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5332f758cb4b2d1d906f1cca91b5cf172529aacb223b4e2c2026b6c78905909c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdcb6ac1015e2ef453760ece5d9237978f238085bd5c32c6659c803457c0692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e95c954861016f7832a7137f2b2ca615cf7427b569d83949b95e70de5a578a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d794b86c48f1dd6fcacc874c3087d326c1335e119e4fa9ec750f4fe6186cdfd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7283d6bf7ae9ec9802c80b7e9946eaab271ae01bb1a5e3c41d3338d16e4695a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da1e0d99a4a719293c4cd82176e7f36fd8ba62ebb536aa80d869b970c3484af5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketNameInput")
    def intermediate_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intermediateBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ac9543f1ad2aae4ca860d5d5403950f2c21234b1fa7d8499bad3a72cce5827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketName")
    def intermediate_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intermediateBucketName"))

    @intermediate_bucket_name.setter
    def intermediate_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd63a3d2ddc68bb8c327a1248f70a1c4ca6e75b690896d05d7ac75c3197054a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intermediateBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b3099346f04e244d30fb213aee47f423a41ef470697ca139879cbfa1d6c94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23de7386ef2a405f46c79176e1671e4ee70da45ba823c34bf39b99b1cf2227f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "s3_output_format_config": "s3OutputFormatConfig",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        s3_output_format_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        if isinstance(s3_output_format_config, dict):
            s3_output_format_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig(**s3_output_format_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ec773bb1d99edf024af231020aea695d79c83fe23f65e59fbcb9c1ca007254)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if s3_output_format_config is not None:
            self._values["s3_output_format_config"] = s3_output_format_config

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_output_format_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"]:
        '''s3_output_format_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        result = self._values.get("s3_output_format_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62956e2917ff4eb007a8a3f4748e5c34ab017890ece72141d6d39760e3ff26e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3OutputFormatConfig")
    def put_s3_output_format_config(
        self,
        *,
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
        prefix_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param preserve_source_data_typing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#preserve_source_data_typing AppflowFlow#preserve_source_data_typing}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig(
            aggregation_config=aggregation_config,
            file_type=file_type,
            prefix_config=prefix_config,
            preserve_source_data_typing=preserve_source_data_typing,
        )

        return typing.cast(None, jsii.invoke(self, "putS3OutputFormatConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetS3OutputFormatConfig")
    def reset_s3_output_format_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3OutputFormatConfig", []))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfig")
    def s3_output_format_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference", jsii.get(self, "s3OutputFormatConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfigInput")
    def s3_output_format_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"], jsii.get(self, "s3OutputFormatConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321690f2bfdaad8980049ce025230a2e03426148df91a558e98e97f53dbea918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b3c6f88384f39520c19c029699de260518036cfc731f5fb93646666369d9fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9790fa7ac8af18f1248b7bd74935596d3fcec9659dcdd12ee5369210be2e674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_config": "aggregationConfig",
        "file_type": "fileType",
        "prefix_config": "prefixConfig",
        "preserve_source_data_typing": "preserveSourceDataTyping",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig:
    def __init__(
        self,
        *,
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
        prefix_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param preserve_source_data_typing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#preserve_source_data_typing AppflowFlow#preserve_source_data_typing}.
        '''
        if isinstance(aggregation_config, dict):
            aggregation_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig(**aggregation_config)
        if isinstance(prefix_config, dict):
            prefix_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig(**prefix_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52945ce783444b85156919463f6b8c7bdee7784e80d6088dcc7e0589eef6c714)
            check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
            check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
            check_type(argname="argument preserve_source_data_typing", value=preserve_source_data_typing, expected_type=type_hints["preserve_source_data_typing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_config is not None:
            self._values["aggregation_config"] = aggregation_config
        if file_type is not None:
            self._values["file_type"] = file_type
        if prefix_config is not None:
            self._values["prefix_config"] = prefix_config
        if preserve_source_data_typing is not None:
            self._values["preserve_source_data_typing"] = preserve_source_data_typing

    @builtins.property
    def aggregation_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig"]:
        '''aggregation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        '''
        result = self._values.get("aggregation_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig"], result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.'''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"]:
        '''prefix_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        '''
        result = self._values.get("prefix_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"], result)

    @builtins.property
    def preserve_source_data_typing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#preserve_source_data_typing AppflowFlow#preserve_source_data_typing}.'''
        result = self._values.get("preserve_source_data_typing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_type": "aggregationType",
        "target_file_size": "targetFileSize",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig:
    def __init__(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
        target_file_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        :param target_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#target_file_size AppflowFlow#target_file_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584ecfe1fdfc18f2e99a94fd3203e8d593da524a9cc8326b34d890ccd45ff55c)
            check_type(argname="argument aggregation_type", value=aggregation_type, expected_type=type_hints["aggregation_type"])
            check_type(argname="argument target_file_size", value=target_file_size, expected_type=type_hints["target_file_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_type is not None:
            self._values["aggregation_type"] = aggregation_type
        if target_file_size is not None:
            self._values["target_file_size"] = target_file_size

    @builtins.property
    def aggregation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.'''
        result = self._values.get("aggregation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_file_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#target_file_size AppflowFlow#target_file_size}.'''
        result = self._values.get("target_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf2c835bcef10f90bf084ece9adc3d2f793f95d938ecd3cb58c1f6e99af593c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregationType")
    def reset_aggregation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationType", []))

    @jsii.member(jsii_name="resetTargetFileSize")
    def reset_target_file_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFileSize", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationTypeInput")
    def aggregation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFileSizeInput")
    def target_file_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetFileSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationType")
    def aggregation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationType"))

    @aggregation_type.setter
    def aggregation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437e644918a740d6296cb2655278cd48ca1804b5c67f51ade496486181b712fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFileSize")
    def target_file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetFileSize"))

    @target_file_size.setter
    def target_file_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a9d2bf5144026b3df293596a5148086865219fb1aca14562a784e8169f087e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFileSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b17fc41e9040831ce8edadaa62f4af246df86432cea456fdcbd1a67f0394032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bbe9e0a9fe313001e415670130c14a3c9553f0601cba23025d5fc5e99fa7200)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAggregationConfig")
    def put_aggregation_config(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
        target_file_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        :param target_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#target_file_size AppflowFlow#target_file_size}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig(
            aggregation_type=aggregation_type, target_file_size=target_file_size
        )

        return typing.cast(None, jsii.invoke(self, "putAggregationConfig", [value]))

    @jsii.member(jsii_name="putPrefixConfig")
    def put_prefix_config(
        self,
        *,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig(
            prefix_format=prefix_format,
            prefix_hierarchy=prefix_hierarchy,
            prefix_type=prefix_type,
        )

        return typing.cast(None, jsii.invoke(self, "putPrefixConfig", [value]))

    @jsii.member(jsii_name="resetAggregationConfig")
    def reset_aggregation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationConfig", []))

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @jsii.member(jsii_name="resetPrefixConfig")
    def reset_prefix_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixConfig", []))

    @jsii.member(jsii_name="resetPreserveSourceDataTyping")
    def reset_preserve_source_data_typing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveSourceDataTyping", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfig")
    def aggregation_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference, jsii.get(self, "aggregationConfig"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfig")
    def prefix_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference", jsii.get(self, "prefixConfig"))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfigInput")
    def aggregation_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig], jsii.get(self, "aggregationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfigInput")
    def prefix_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"], jsii.get(self, "prefixConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveSourceDataTypingInput")
    def preserve_source_data_typing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveSourceDataTypingInput"))

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f079efa86233624cb98e6529ea77527bc057bc0fa40fbb5948a002f1d5dc7d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveSourceDataTyping")
    def preserve_source_data_typing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveSourceDataTyping"))

    @preserve_source_data_typing.setter
    def preserve_source_data_typing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9617d5a3c4a68552e8af540840f24c088d79d320394f61b500796cc430a188cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveSourceDataTyping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da50d507ec50d131340ae710eef29dfed1a27584228c9a878f231e14808d01f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig",
    jsii_struct_bases=[],
    name_mapping={
        "prefix_format": "prefixFormat",
        "prefix_hierarchy": "prefixHierarchy",
        "prefix_type": "prefixType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig:
    def __init__(
        self,
        *,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d04afd9f0724df621192a3203519fb6fce4f3a6cbbd4d9cef1f48e49c13043)
            check_type(argname="argument prefix_format", value=prefix_format, expected_type=type_hints["prefix_format"])
            check_type(argname="argument prefix_hierarchy", value=prefix_hierarchy, expected_type=type_hints["prefix_hierarchy"])
            check_type(argname="argument prefix_type", value=prefix_type, expected_type=type_hints["prefix_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix_format is not None:
            self._values["prefix_format"] = prefix_format
        if prefix_hierarchy is not None:
            self._values["prefix_hierarchy"] = prefix_hierarchy
        if prefix_type is not None:
            self._values["prefix_type"] = prefix_type

    @builtins.property
    def prefix_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.'''
        result = self._values.get("prefix_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_hierarchy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.'''
        result = self._values.get("prefix_hierarchy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prefix_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.'''
        result = self._values.get("prefix_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6407b3492d71380ec9e084a5356ca0bb8da6f09f54fc771a87099cabf9d8c5cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefixFormat")
    def reset_prefix_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixFormat", []))

    @jsii.member(jsii_name="resetPrefixHierarchy")
    def reset_prefix_hierarchy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixHierarchy", []))

    @jsii.member(jsii_name="resetPrefixType")
    def reset_prefix_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixType", []))

    @builtins.property
    @jsii.member(jsii_name="prefixFormatInput")
    def prefix_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchyInput")
    def prefix_hierarchy_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prefixHierarchyInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixTypeInput")
    def prefix_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixFormat")
    def prefix_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixFormat"))

    @prefix_format.setter
    def prefix_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf5a82ef2e40302d8d2af1553f3105b4b7c408bfb0c6a7b0a251f5d499d4773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchy")
    def prefix_hierarchy(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prefixHierarchy"))

    @prefix_hierarchy.setter
    def prefix_hierarchy(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8ac6bdfd184cc540221b675e30cf4f7fb100fe54af2d566088352f3c9cb4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixHierarchy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixType")
    def prefix_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixType"))

    @prefix_type.setter
    def prefix_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0703fbf39d1c295ac62646be5048af8775c2b31fc77f9ffc314ded51621db258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1054974018b4cd7d1abfc8b4b69c9325c044df4cb4b5296022c5d37e75871f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8965e3d6fc8000a051b3f5eab6dfcb5f63683ef1cb3c3e6beedb20475de42ec2)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66e4879c08d751a122672d38a83a381c7c0011cbd68a14c7e7583f9eac20d8f)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8d68ae52b72937d8212df24e59cc908b28df9ca147c201d6e33e74b775773c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58a16b8d9e6718c05ee396d32daf76270ecb8b479cf309e8b7973ebf56e7a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f54d7f82abe2ebd1e2af0ec95c8f160518644a2d68112d24d9a8f0f6d6622b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895defe93a45f0b079d7dd78f874a3da14ce656a60dfc18209650771e79f7dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa3f8ef5227807366aff42f96033708bcc3382267f2a4a77dd578cb4e8958aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51010cfc882e9901eaa398332f8c013458ef75117fdd9992bb0b46c046960b76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff458f8bc5afe339e9e48eb5d5fdb81ec0d7dc55afea4c65f9df04f8e3d416f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5272e966f7dfe576b57efb5d3197b63894944cd89a83567a2ca8beb0a9a0a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976ff5ca0389d5c30647ea4cd1381b97ad0eca1c24d191637338371d19ad5c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c99c4c3b502f4043e7d94491dadc1106a670d023067d07cb9b3770fd3865d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "object_path": "objectPath",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "success_response_handling_config": "successResponseHandlingConfig",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData:
    def __init__(
        self,
        *,
        object_path: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_response_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param success_response_handling_config: success_response_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#success_response_handling_config AppflowFlow#success_response_handling_config}
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig(**error_handling_config)
        if isinstance(success_response_handling_config, dict):
            success_response_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig(**success_response_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c413aed1791e9486bf60de96be672d4576beec0fe6a17e59542fd515530f06e)
            check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument success_response_handling_config", value=success_response_handling_config, expected_type=type_hints["success_response_handling_config"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_path": object_path,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if success_response_handling_config is not None:
            self._values["success_response_handling_config"] = success_response_handling_config
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def object_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.'''
        result = self._values.get("object_path")
        assert result is not None, "Required property 'object_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def success_response_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"]:
        '''success_response_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#success_response_handling_config AppflowFlow#success_response_handling_config}
        '''
        result = self._values.get("success_response_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba250468ec5e5637d5adfd26b974a1ee3c5545f6072704398a9d2cd59841fe7)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8e718ca2d6a2961e94e0740c9761a9a91427e72560ede490f0f40453eaa2e4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab0163e996bcda5f42e01976d50e558da0c0ffbcc59eebe4948bdb44f34f1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470acb0dc796c6a9a01c26f920ba049d679489b66631a067b44748c6ed52eb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497fbd4b318b29828023f6b19af6eea7925dddb7cc3cbbeb00548fd30f08da8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbad9786a98ad87a853b08ab81b5b39f0ea501fd3799927ed671601930b56e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b40c01fbe90c6b91161eec35ff1bc55675c8066c49360a5b928bcabe7cd35363)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="putSuccessResponseHandlingConfig")
    def put_success_response_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig(
            bucket_name=bucket_name, bucket_prefix=bucket_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putSuccessResponseHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetSuccessResponseHandlingConfig")
    def reset_success_response_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessResponseHandlingConfig", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="successResponseHandlingConfig")
    def success_response_handling_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference", jsii.get(self, "successResponseHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectPathInput")
    def object_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectPathInput"))

    @builtins.property
    @jsii.member(jsii_name="successResponseHandlingConfigInput")
    def success_response_handling_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"], jsii.get(self, "successResponseHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54a7eda343441240aa41433efa73d9ece0da69134e202f652a0bc3a17e0fae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectPath")
    def object_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectPath"))

    @object_path.setter
    def object_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb63cfddbe9e959bafd6114a138e97ee8247d9ff4d6aaea923f6b12012f7dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc7c83ed2343919ef3bc999bb8b592a19c6bf8401dd5c4140b20fbeb595d5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8263d36f0dd5e923442e6d544d80aab11cf5e16efc29c739e8ba6fb792cb95a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "bucket_prefix": "bucketPrefix"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfcb15d6979b5e5531fe10d2b05282c9899beb501006fe1ca0d5edab3761b02)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d026585aa5b840dc4a19f5a53f15f3496eb04f65a1b354e03f3eba8c5c11356f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd6b7a9d25412346ce712c6ee824f5d92df059221d5bc359e18b5c2a79416af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409758b985689de93465e1efdef359d7254a739b7a8df5b7b46a89a22bebf467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2444ad494a31eda60312eaf20ceb25e4eac8d33e1e3a5ad903516848bec145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake",
    jsii_struct_bases=[],
    name_mapping={
        "intermediate_bucket_name": "intermediateBucketName",
        "object": "object",
        "bucket_prefix": "bucketPrefix",
        "error_handling_config": "errorHandlingConfig",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake:
    def __init__(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b121ef03d25e81ba1b8aa0074d5831187018bdefdd1220d8e74b64d1d18893d8)
            check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "intermediate_bucket_name": intermediate_bucket_name,
            "object": object,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def intermediate_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.'''
        result = self._values.get("intermediate_bucket_name")
        assert result is not None, "Required property 'intermediate_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a5e8cabe13fd56ffb3b34d041068b85652af1f7a494335885ee767812e61cc)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__007ef3d880e7ccf5d4e907c9fbf50ad335e2dc7b9f18f6f27cb84ec4b89a4ad1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad732d24bf392429c19dadb2c23827bc312c32ce4019dc0128460bf44a31865b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2feb635677cd8c7c44dc668c3618cb908cfdfd65d36719e4f3a79f0d5ad8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f85cc384c3b4d4060b88bbeaff5b7b502bff5f0d9c8355d9c197d0545306e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdafe2f49137f1e80f664bc50605e0397e78bb49e10eebd956e0554969a7a346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21ba749bdf3f1ff85535e60ce8fd5bfd0dd5aa4fcf8f970f8047623c0ce7285d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketNameInput")
    def intermediate_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intermediateBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c092ba298beff37f762db686808bbf921364c6e5d7a60eedcf481a7d81066f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketName")
    def intermediate_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intermediateBucketName"))

    @intermediate_bucket_name.setter
    def intermediate_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa58b872214896d48cd62cbcb094aa70ed7880aae64415af70b28c5a402856d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intermediateBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8809aadccfabd8a59aaf6467732d6ec1d9ddf2bd9207fb5ac3b4238a60ed12b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb0e3fdb5767b3ce85a6f738a021c67599cbb3de1ff024f23e12bc97f702a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "s3_output_format_config": "s3OutputFormatConfig",
        "bucket_prefix": "bucketPrefix",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        s3_output_format_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]],
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        if isinstance(s3_output_format_config, dict):
            s3_output_format_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig(**s3_output_format_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d40b297f6b1802da6ddc9387ddd5a4dc647df19eaf73b92f7513a7e44c8945)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "s3_output_format_config": s3_output_format_config,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_output_format_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig":
        '''s3_output_format_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        result = self._values.get("s3_output_format_config")
        assert result is not None, "Required property 's3_output_format_config' is missing"
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig", result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dafd0adf8720736a6ddeabcc785b25a87b0db1ae166684e36f851b9bade752e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3OutputFormatConfig")
    def put_s3_output_format_config(
        self,
        *,
        prefix_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]],
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig(
            prefix_config=prefix_config,
            aggregation_config=aggregation_config,
            file_type=file_type,
        )

        return typing.cast(None, jsii.invoke(self, "putS3OutputFormatConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfig")
    def s3_output_format_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference", jsii.get(self, "s3OutputFormatConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfigInput")
    def s3_output_format_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig"], jsii.get(self, "s3OutputFormatConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501f124740a2518ffa9c3567a80c64f1c87e10d869ef291f357678361ed69825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb06cd9e063e7e9c73fb280d8edbe8b3b1c1ca9e6f75bd092fcf072045635441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acdbd2f32ba3e878aad354f1a52a824d7ca75c12297e1a6b5696f35d1d5a81e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig",
    jsii_struct_bases=[],
    name_mapping={
        "prefix_config": "prefixConfig",
        "aggregation_config": "aggregationConfig",
        "file_type": "fileType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig:
    def __init__(
        self,
        *,
        prefix_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]],
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        '''
        if isinstance(prefix_config, dict):
            prefix_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig(**prefix_config)
        if isinstance(aggregation_config, dict):
            aggregation_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig(**aggregation_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988f2d3b908fe51becade7bd8cd11fd3f963ea9b421f3266b788a3f9ca373bde)
            check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
            check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prefix_config": prefix_config,
        }
        if aggregation_config is not None:
            self._values["aggregation_config"] = aggregation_config
        if file_type is not None:
            self._values["file_type"] = file_type

    @builtins.property
    def prefix_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig":
        '''prefix_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        '''
        result = self._values.get("prefix_config")
        assert result is not None, "Required property 'prefix_config' is missing"
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig", result)

    @builtins.property
    def aggregation_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig"]:
        '''aggregation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        '''
        result = self._values.get("aggregation_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig"], result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.'''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig",
    jsii_struct_bases=[],
    name_mapping={"aggregation_type": "aggregationType"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig:
    def __init__(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab819b17d7d798618d456f980572d2937f88b2d86e91c25357391849f3fe611)
            check_type(argname="argument aggregation_type", value=aggregation_type, expected_type=type_hints["aggregation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_type is not None:
            self._values["aggregation_type"] = aggregation_type

    @builtins.property
    def aggregation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.'''
        result = self._values.get("aggregation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc58910bc9b60417d12a822aac9b740c448ca0f16158b0a770c2a5a806f2f249)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregationType")
    def reset_aggregation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationType", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationTypeInput")
    def aggregation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationType")
    def aggregation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationType"))

    @aggregation_type.setter
    def aggregation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7678d971a00fabf44b6c613c14d4e73b2da0c412ea614be99c24bbdad6868fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff830a6a31562272079c6f207a93f26289bb7e1197621f08a60ef4693767447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be576d692a793056ac7f58e96055a43a71d0888290ffddbbb867f24ec8bdfb4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAggregationConfig")
    def put_aggregation_config(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig(
            aggregation_type=aggregation_type
        )

        return typing.cast(None, jsii.invoke(self, "putAggregationConfig", [value]))

    @jsii.member(jsii_name="putPrefixConfig")
    def put_prefix_config(
        self,
        *,
        prefix_type: builtins.str,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig(
            prefix_type=prefix_type,
            prefix_format=prefix_format,
            prefix_hierarchy=prefix_hierarchy,
        )

        return typing.cast(None, jsii.invoke(self, "putPrefixConfig", [value]))

    @jsii.member(jsii_name="resetAggregationConfig")
    def reset_aggregation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationConfig", []))

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfig")
    def aggregation_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference, jsii.get(self, "aggregationConfig"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfig")
    def prefix_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference", jsii.get(self, "prefixConfig"))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfigInput")
    def aggregation_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig], jsii.get(self, "aggregationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfigInput")
    def prefix_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig"], jsii.get(self, "prefixConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868203fa3f735f3353f27dcf04a97b62f8c41c59f44e4ba511c7601db06762e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2935e3a6747debbd5d074dc5be50aa2fa158a0748ba1cb353f732999559b476a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig",
    jsii_struct_bases=[],
    name_mapping={
        "prefix_type": "prefixType",
        "prefix_format": "prefixFormat",
        "prefix_hierarchy": "prefixHierarchy",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig:
    def __init__(
        self,
        *,
        prefix_type: builtins.str,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6be9f160622b52a2d10bb8d7ee7f70b33551dd8187cbd4648bbd84ed201505)
            check_type(argname="argument prefix_type", value=prefix_type, expected_type=type_hints["prefix_type"])
            check_type(argname="argument prefix_format", value=prefix_format, expected_type=type_hints["prefix_format"])
            check_type(argname="argument prefix_hierarchy", value=prefix_hierarchy, expected_type=type_hints["prefix_hierarchy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prefix_type": prefix_type,
        }
        if prefix_format is not None:
            self._values["prefix_format"] = prefix_format
        if prefix_hierarchy is not None:
            self._values["prefix_hierarchy"] = prefix_hierarchy

    @builtins.property
    def prefix_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.'''
        result = self._values.get("prefix_type")
        assert result is not None, "Required property 'prefix_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.'''
        result = self._values.get("prefix_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_hierarchy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.'''
        result = self._values.get("prefix_hierarchy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f7f8085663b70e3383ab5bcfe623952cb50f7a7338b0f5032658adbf17bcde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefixFormat")
    def reset_prefix_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixFormat", []))

    @jsii.member(jsii_name="resetPrefixHierarchy")
    def reset_prefix_hierarchy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixHierarchy", []))

    @builtins.property
    @jsii.member(jsii_name="prefixFormatInput")
    def prefix_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchyInput")
    def prefix_hierarchy_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prefixHierarchyInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixTypeInput")
    def prefix_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixFormat")
    def prefix_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixFormat"))

    @prefix_format.setter
    def prefix_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd608f75732ec7cfcb06554cd3dd2ae61e34095574c1fbf624b3559b823d863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchy")
    def prefix_hierarchy(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prefixHierarchy"))

    @prefix_hierarchy.setter
    def prefix_hierarchy(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5449d873aafd385c1b30e4114e810fd72bec789db7c0f72c40b96eeb4e31b509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixHierarchy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixType")
    def prefix_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixType"))

    @prefix_type.setter
    def prefix_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8949cae58d40d669dd4403f4fa0cbf8885ae8019bb5c299202b3ff203d3abf21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f53bd0b34b52edee4a6e083a147d67dd62655aa2de64c7363658e26710f50d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3330e45e9f4bf7145a5d3f075cd74465c5dae086ac2d0dd3fc65e21bf468ed)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261e8dedeb625de4a7f8c9edbd03040b5b82717862a2d504dd0e52c789300c55)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5889e06b9dbb7ea7a85c8ffd868cf5c7f5a7c7ecee0e66aef22a6fa37ee579f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d982cfe4ab296bf9b5087ea15b81f5acb204709dd29da73ec52d070d524ff459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c5da36391ac58891069edfa3563a3c7469cec4384ec9a6b665210ca925c278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88054266769af4a594ad766d3f141a80b07dfa2433883c0b51096f882c4f7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f65af162ea2bc612895b9f01cfcba3db8785b51af5c9ca402d76a3eb00d570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9d4c8c437e95f6925370417381a4ccb0f8d46162ec98d6ad96605deb5803576)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a75def861f5ad9916a317c8c849c9819470779af34829fd9acaee2109512b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518ae2b79fccbdde1eee14caf153cde10485d63fbe9e348e19cb9dd69c5a6682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62748052e66fe6e2e5bc1546b884f5801586b9d04bf95a449452c54eb4c185d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac73b7867e49b8d707112b97039fb5372d4eb84a38007ff5ea6c08b96303d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__801ac70bd423b21e0f8f91d2542016691245a9dcc96b551cd55cb931ed435bdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppflowFlowDestinationFlowConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab60b6ab04559a2fbd2a4f7e507a239edef3e3dea54d2dbb3b20d9872bc6a0f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppflowFlowDestinationFlowConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363bd796ce40e68b4240dd266b60f5ff8e70b87c42507536afbd624dc031dda2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2473c70cac2260f015fe576d40ca08fffd91301393af9873862879b65f09151)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2086e7a7d6bf5d428e29d2962011dfb6cabe40d98b8ca49c24b5dee1b103686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac49f1270041c65a25b7c7e8e8a16c3008d25395dc635998e7a3b54208445d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76ed323262d42a1a30603ae4a1be3b838e19f1f7e0e7550a900efc260ed52ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDestinationConnectorProperties")
    def put_destination_connector_properties(
        self,
        *,
        custom_connector: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
        customer_profiles: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge, typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
        lookout_metrics: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3, typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
        upsolver: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver, typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param customer_profiles: customer_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#customer_profiles AppflowFlow#customer_profiles}
        :param event_bridge: event_bridge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#event_bridge AppflowFlow#event_bridge}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#honeycode AppflowFlow#honeycode}
        :param lookout_metrics: lookout_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#lookout_metrics AppflowFlow#lookout_metrics}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#redshift AppflowFlow#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#snowflake AppflowFlow#snowflake}
        :param upsolver: upsolver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#upsolver AppflowFlow#upsolver}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorProperties(
            custom_connector=custom_connector,
            customer_profiles=customer_profiles,
            event_bridge=event_bridge,
            honeycode=honeycode,
            lookout_metrics=lookout_metrics,
            marketo=marketo,
            redshift=redshift,
            s3=s3,
            salesforce=salesforce,
            sapo_data=sapo_data,
            snowflake=snowflake,
            upsolver=upsolver,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationConnectorProperties", [value]))

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetConnectorProfileName")
    def reset_connector_profile_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorProfileName", []))

    @builtins.property
    @jsii.member(jsii_name="destinationConnectorProperties")
    def destination_connector_properties(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference, jsii.get(self, "destinationConnectorProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileNameInput")
    def connector_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorTypeInput")
    def connector_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConnectorPropertiesInput")
    def destination_connector_properties_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties], jsii.get(self, "destinationConnectorPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c59fd6044f7e23792df9d760383c72b248df64eb17318594c7ba7884837d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorProfileName")
    def connector_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorProfileName"))

    @connector_profile_name.setter
    def connector_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872f3583e1a9390f3cb9f213ec0b21991f55b6d6daa350f42a6303284491fcde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProfileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0c979c5c302abc290d95310a02fd4a000a0691188c743364d6e82bef2f456c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d6cd47e978875353713151e0239bf96f83b8b150e7019d9b148ebf5eaa7395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfig",
    jsii_struct_bases=[],
    name_mapping={"glue_data_catalog": "glueDataCatalog"},
)
class AppflowFlowMetadataCatalogConfig:
    def __init__(
        self,
        *,
        glue_data_catalog: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfigGlueDataCatalog", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param glue_data_catalog: glue_data_catalog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#glue_data_catalog AppflowFlow#glue_data_catalog}
        '''
        if isinstance(glue_data_catalog, dict):
            glue_data_catalog = AppflowFlowMetadataCatalogConfigGlueDataCatalog(**glue_data_catalog)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447d833232d6580e8b738754fbca19b62530bdac2f2451543b0da43e12e37d63)
            check_type(argname="argument glue_data_catalog", value=glue_data_catalog, expected_type=type_hints["glue_data_catalog"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if glue_data_catalog is not None:
            self._values["glue_data_catalog"] = glue_data_catalog

    @builtins.property
    def glue_data_catalog(
        self,
    ) -> typing.Optional["AppflowFlowMetadataCatalogConfigGlueDataCatalog"]:
        '''glue_data_catalog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#glue_data_catalog AppflowFlow#glue_data_catalog}
        '''
        result = self._values.get("glue_data_catalog")
        return typing.cast(typing.Optional["AppflowFlowMetadataCatalogConfigGlueDataCatalog"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowMetadataCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfigGlueDataCatalog",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "role_arn": "roleArn",
        "table_prefix": "tablePrefix",
    },
)
class AppflowFlowMetadataCatalogConfigGlueDataCatalog:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        role_arn: builtins.str,
        table_prefix: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#database_name AppflowFlow#database_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#role_arn AppflowFlow#role_arn}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#table_prefix AppflowFlow#table_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9977c4cee39bcbfb4daee0d6720652e133c7969de3d8d4efbcb9873e70a5b1)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "role_arn": role_arn,
            "table_prefix": table_prefix,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#database_name AppflowFlow#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#role_arn AppflowFlow#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#table_prefix AppflowFlow#table_prefix}.'''
        result = self._values.get("table_prefix")
        assert result is not None, "Required property 'table_prefix' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowMetadataCatalogConfigGlueDataCatalog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__024c53ee79c5e464bb9521d09c0c3022f5dcc871454876ee3f17de65b58f9648)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefixInput")
    def table_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25534f59a9c09364cb6b52dbe048193e1d15a17a9c049b058f3f2f9adc3fe0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265dbc3efebc9dafaa1d46ba9dff85f7397f0a8ebf5755f08518d0fc6a2ecb29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @table_prefix.setter
    def table_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fbc64f11e49f765c1860f9b4a6570f1be06afbd66b07158494354773cfc773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog]:
        return typing.cast(typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643630ba88c184d6a298f6b6b2fc309b1b2dfd962d8142e07b4cc9d7149bdfc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowMetadataCatalogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3f804019d800ba279dc9a86b8d82db0890a8a25fc0ed2d9e5a38d683703a812)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGlueDataCatalog")
    def put_glue_data_catalog(
        self,
        *,
        database_name: builtins.str,
        role_arn: builtins.str,
        table_prefix: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#database_name AppflowFlow#database_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#role_arn AppflowFlow#role_arn}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#table_prefix AppflowFlow#table_prefix}.
        '''
        value = AppflowFlowMetadataCatalogConfigGlueDataCatalog(
            database_name=database_name, role_arn=role_arn, table_prefix=table_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putGlueDataCatalog", [value]))

    @jsii.member(jsii_name="resetGlueDataCatalog")
    def reset_glue_data_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlueDataCatalog", []))

    @builtins.property
    @jsii.member(jsii_name="glueDataCatalog")
    def glue_data_catalog(
        self,
    ) -> AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference:
        return typing.cast(AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference, jsii.get(self, "glueDataCatalog"))

    @builtins.property
    @jsii.member(jsii_name="glueDataCatalogInput")
    def glue_data_catalog_input(
        self,
    ) -> typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog]:
        return typing.cast(typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog], jsii.get(self, "glueDataCatalogInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppflowFlowMetadataCatalogConfig]:
        return typing.cast(typing.Optional[AppflowFlowMetadataCatalogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowMetadataCatalogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf51b22be105dac6861374d2234decd001e71a6fa854f52fd43ff9309d33d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connector_type": "connectorType",
        "source_connector_properties": "sourceConnectorProperties",
        "api_version": "apiVersion",
        "connector_profile_name": "connectorProfileName",
        "incremental_pull_config": "incrementalPullConfig",
    },
)
class AppflowFlowSourceFlowConfig:
    def __init__(
        self,
        *,
        connector_type: builtins.str,
        source_connector_properties: typing.Union["AppflowFlowSourceFlowConfigSourceConnectorProperties", typing.Dict[builtins.str, typing.Any]],
        api_version: typing.Optional[builtins.str] = None,
        connector_profile_name: typing.Optional[builtins.str] = None,
        incremental_pull_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigIncrementalPullConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.
        :param source_connector_properties: source_connector_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_connector_properties AppflowFlow#source_connector_properties}
        :param api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.
        :param connector_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.
        :param incremental_pull_config: incremental_pull_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#incremental_pull_config AppflowFlow#incremental_pull_config}
        '''
        if isinstance(source_connector_properties, dict):
            source_connector_properties = AppflowFlowSourceFlowConfigSourceConnectorProperties(**source_connector_properties)
        if isinstance(incremental_pull_config, dict):
            incremental_pull_config = AppflowFlowSourceFlowConfigIncrementalPullConfig(**incremental_pull_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf66e0a94a16c07fc4f9753d98d3c8bee2a3abf4d7640f13b7c335a772fe0f1e)
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument source_connector_properties", value=source_connector_properties, expected_type=type_hints["source_connector_properties"])
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
            check_type(argname="argument incremental_pull_config", value=incremental_pull_config, expected_type=type_hints["incremental_pull_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_type": connector_type,
            "source_connector_properties": source_connector_properties,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if connector_profile_name is not None:
            self._values["connector_profile_name"] = connector_profile_name
        if incremental_pull_config is not None:
            self._values["incremental_pull_config"] = incremental_pull_config

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.'''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_connector_properties(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorProperties":
        '''source_connector_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_connector_properties AppflowFlow#source_connector_properties}
        '''
        result = self._values.get("source_connector_properties")
        assert result is not None, "Required property 'source_connector_properties' is missing"
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorProperties", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.'''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_profile_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.'''
        result = self._values.get("connector_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental_pull_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigIncrementalPullConfig"]:
        '''incremental_pull_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#incremental_pull_config AppflowFlow#incremental_pull_config}
        '''
        result = self._values.get("incremental_pull_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigIncrementalPullConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigIncrementalPullConfig",
    jsii_struct_bases=[],
    name_mapping={"datetime_type_field_name": "datetimeTypeFieldName"},
)
class AppflowFlowSourceFlowConfigIncrementalPullConfig:
    def __init__(
        self,
        *,
        datetime_type_field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param datetime_type_field_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datetime_type_field_name AppflowFlow#datetime_type_field_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847cdfe0511582182fcf539c1ed0e0ab8751c6905b71679599bbd9b545466727)
            check_type(argname="argument datetime_type_field_name", value=datetime_type_field_name, expected_type=type_hints["datetime_type_field_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if datetime_type_field_name is not None:
            self._values["datetime_type_field_name"] = datetime_type_field_name

    @builtins.property
    def datetime_type_field_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datetime_type_field_name AppflowFlow#datetime_type_field_name}.'''
        result = self._values.get("datetime_type_field_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigIncrementalPullConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0898c6e067b56cc5dad4a6a8ee5a7d5518d932da03f86ae0511cc3449e18dc70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatetimeTypeFieldName")
    def reset_datetime_type_field_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatetimeTypeFieldName", []))

    @builtins.property
    @jsii.member(jsii_name="datetimeTypeFieldNameInput")
    def datetime_type_field_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datetimeTypeFieldNameInput"))

    @builtins.property
    @jsii.member(jsii_name="datetimeTypeFieldName")
    def datetime_type_field_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datetimeTypeFieldName"))

    @datetime_type_field_name.setter
    def datetime_type_field_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b129898eaeff5124e44969ad521de79f993acd0838b92e4d2fe0b1eb84ae0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datetimeTypeFieldName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6770adda1677b99cd207d35f8198e027ec933ffed029b757b6de52c62198b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowSourceFlowConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff50d36b38cbd9e8ad32276c9ae7bceeaa9be63a34a5f884a49a4f0251275030)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncrementalPullConfig")
    def put_incremental_pull_config(
        self,
        *,
        datetime_type_field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param datetime_type_field_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datetime_type_field_name AppflowFlow#datetime_type_field_name}.
        '''
        value = AppflowFlowSourceFlowConfigIncrementalPullConfig(
            datetime_type_field_name=datetime_type_field_name
        )

        return typing.cast(None, jsii.invoke(self, "putIncrementalPullConfig", [value]))

    @jsii.member(jsii_name="putSourceConnectorProperties")
    def put_source_connector_properties(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#singular AppflowFlow#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#slack AppflowFlow#slack}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorProperties(
            amplitude=amplitude,
            custom_connector=custom_connector,
            datadog=datadog,
            dynatrace=dynatrace,
            google_analytics=google_analytics,
            infor_nexus=infor_nexus,
            marketo=marketo,
            s3=s3,
            salesforce=salesforce,
            sapo_data=sapo_data,
            service_now=service_now,
            singular=singular,
            slack=slack,
            trendmicro=trendmicro,
            veeva=veeva,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceConnectorProperties", [value]))

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetConnectorProfileName")
    def reset_connector_profile_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorProfileName", []))

    @jsii.member(jsii_name="resetIncrementalPullConfig")
    def reset_incremental_pull_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncrementalPullConfig", []))

    @builtins.property
    @jsii.member(jsii_name="incrementalPullConfig")
    def incremental_pull_config(
        self,
    ) -> AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference, jsii.get(self, "incrementalPullConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceConnectorProperties")
    def source_connector_properties(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference", jsii.get(self, "sourceConnectorProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileNameInput")
    def connector_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorTypeInput")
    def connector_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="incrementalPullConfigInput")
    def incremental_pull_config_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig], jsii.get(self, "incrementalPullConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceConnectorPropertiesInput")
    def source_connector_properties_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorProperties"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorProperties"], jsii.get(self, "sourceConnectorPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb35b38e489c862e8c5151317c7d662630a567572e512e8939b80cf673308111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorProfileName")
    def connector_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorProfileName"))

    @connector_profile_name.setter
    def connector_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44465f81e02c9790a23f55e7107d0a0d465171d9b6cb312267f24f6fa35562ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProfileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3fd6c8c8187781b71c968c63c502e0a8e421f825a4e9642c4f3372f1ce9b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppflowFlowSourceFlowConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc2ccdc02a2efab7407673ed01474e7ae4c508c1a14e121f58aa9118f000c53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorProperties",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "s3": "s3",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorProperties:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#singular AppflowFlow#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#slack AppflowFlow#slack}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        if isinstance(amplitude, dict):
            amplitude = AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude(**amplitude)
        if isinstance(custom_connector, dict):
            custom_connector = AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector(**custom_connector)
        if isinstance(datadog, dict):
            datadog = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog(**datadog)
        if isinstance(dynatrace, dict):
            dynatrace = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace(**dynatrace)
        if isinstance(google_analytics, dict):
            google_analytics = AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics(**google_analytics)
        if isinstance(infor_nexus, dict):
            infor_nexus = AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus(**infor_nexus)
        if isinstance(marketo, dict):
            marketo = AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo(**marketo)
        if isinstance(s3, dict):
            s3 = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3(**s3)
        if isinstance(salesforce, dict):
            salesforce = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData(**sapo_data)
        if isinstance(service_now, dict):
            service_now = AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow(**service_now)
        if isinstance(singular, dict):
            singular = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular(**singular)
        if isinstance(slack, dict):
            slack = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack(**slack)
        if isinstance(trendmicro, dict):
            trendmicro = AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro(**trendmicro)
        if isinstance(veeva, dict):
            veeva = AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva(**veeva)
        if isinstance(zendesk, dict):
            zendesk = AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e717f8dc78d87a1aef06090bfeea786aa4f2c1669279a42d1494d95c3b43a4bc)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
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
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if s3 is not None:
            self._values["s3"] = s3
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
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude"]:
        '''amplitude block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}
        '''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude"], result)

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector"], result)

    @builtins.property
    def datadog(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog"]:
        '''datadog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}
        '''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog"], result)

    @builtins.property
    def dynatrace(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace"]:
        '''dynatrace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}
        '''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace"], result)

    @builtins.property
    def google_analytics(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics"]:
        '''google_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}
        '''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics"], result)

    @builtins.property
    def infor_nexus(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus"]:
        '''infor_nexus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}
        '''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"], result)

    @builtins.property
    def singular(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"]:
        '''singular block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#singular AppflowFlow#singular}
        '''
        result = self._values.get("singular")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"], result)

    @builtins.property
    def slack(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"]:
        '''slack block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#slack AppflowFlow#slack}
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"], result)

    @builtins.property
    def trendmicro(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"]:
        '''trendmicro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}
        '''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"], result)

    @builtins.property
    def veeva(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"]:
        '''veeva block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}
        '''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f3ac80550cdaef3a884598d7fb6051065936a9cb60bef1469b88bcd30b15eeb)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba12285f05350039637cb6a65105fb8c5afff64299edaa3f071fc858f5da7ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca4589b727be2bd49e67fa67564cb22d9d8d548ff49d89ab4d6977c2401c0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7713b66c07ebc03a2ffa9ec71965c85cc43420ffb958ab1e7fa134d0563e858e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "entity_name": "entityName",
        "custom_properties": "customProperties",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector:
    def __init__(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35506281b6e355855f9b5edb7efc9ccc9bde03d4e99512a6ae5d20bed840e8dd)
            check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_name": entity_name,
        }
        if custom_properties is not None:
            self._values["custom_properties"] = custom_properties

    @builtins.property
    def entity_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.'''
        result = self._values.get("entity_name")
        assert result is not None, "Required property 'entity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.'''
        result = self._values.get("custom_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39659cc203275494c21e7538a41afe07b320fb31e9dd0cd1cf4ea5c3c30ebe00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomProperties")
    def reset_custom_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomProperties", []))

    @builtins.property
    @jsii.member(jsii_name="customPropertiesInput")
    def custom_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="entityNameInput")
    def entity_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityNameInput"))

    @builtins.property
    @jsii.member(jsii_name="customProperties")
    def custom_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customProperties"))

    @custom_properties.setter
    def custom_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab6e8588355853ae6169104e056ce84b18e7c67ac6d466f2b2f8aca455e6dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entityName")
    def entity_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityName"))

    @entity_name.setter
    def entity_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30ef72c1f5ff19c9cbf4a10176b5cdfd188a3dd39c345b1dfb99c5ceb89a97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab37b4105bd743c59c41df991cd62d6ecc9c8da2993025927bca8e8e5e1d939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c182fa6b0a84310cd0ff83fe4cb8dc061e9fe3c5597f7fe2a06d09f051f0e86)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cb39ce3f214e960a78b97c5943b72f9403555f729a06be5ab2c801e0b748a9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6015b1ea6fa87a687f28e89516a3728aef2782574a8a2f7000611620d5eb76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653c832316f5fffa5b0bbb68b0e587229db90989fdcb1acee6c5a1a5abebac91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b715ca4a794fb5ea5434f04f8aa5043a493b724e49012668067bed0abb2fe68)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__028ad66d343e3f4cf9ef5fbf99086b703e749c5fbfa42f3563663c646797d0d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab166048f053826a7a651c96a2a45d9790ea11f678f01ecac04ea8ead5bbd040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f85b0e9bca76879ec7f83462c51028b65ccc97bbfe274df03d3597162b872dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74e857b7b44cf9797ef1afea43d6262634471fd9512ec7d99a57381dda71453)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28aa2f87c347f0f4a41a2409360876c2997c054784c4c7ec746cea0cfb3d13ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af928fc3dcbdb52671345bc3e8ac79e6e17cac387bf71f7885dc6fa115b83692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2c09c97de5843fce2f2c98b0ba0eecef9db5b88f96f4d70d2cbe720ed239ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd1f64603fce6964321e4c2fa3ef508be2afef22daf31def9ad51c6bcf87aa5)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9184354d046ec5afb65f35a69d93fda0e03b779b5b0992141f4ce5a3213e6260)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4782cd71d5ac10565925efb59768c8758e55a790a9b361f48ccf59817f604c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714273349e990e6293c0071eb08bb4a3fdab92d100a2d7c9e00b9089cf33fad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e15841d46e41243d71c2144b715dd9712adbe3bd64117cfa29a113041d2a69)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aed3fb2317ef289d3f46b9812a8ec2ab484c259b44f25a0cbaca5bee2d32d9f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2788ff5266b04e5127322be590ec0a9e56aed3be61641811045d5cd3793f47c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa08c9dbdde463e85b732164084cbeb4c53ca12e8f0cd679481ca59c6d26821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d65e98092c888e5726613c3fa6dc16d99142037dc0aa85de0ea32b7aab19b52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmplitude")
    def put_amplitude(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putAmplitude", [value]))

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector(
            entity_name=entity_name, custom_properties=custom_properties
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putDatadog")
    def put_datadog(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putDatadog", [value]))

    @jsii.member(jsii_name="putDynatrace")
    def put_dynatrace(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putDynatrace", [value]))

    @jsii.member(jsii_name="putGoogleAnalytics")
    def put_google_analytics(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleAnalytics", [value]))

    @jsii.member(jsii_name="putInforNexus")
    def put_infor_nexus(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putInforNexus", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: builtins.str,
        s3_input_format_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_input_format_config: s3_input_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_input_format_config AppflowFlow#s3_input_format_config}
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            s3_input_format_config=s3_input_format_config,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        object: builtins.str,
        data_transfer_api: typing.Optional[builtins.str] = None,
        enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_deleted_records: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param data_transfer_api: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.
        :param enable_dynamic_field_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#enable_dynamic_field_update AppflowFlow#enable_dynamic_field_update}.
        :param include_deleted_records: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_deleted_records AppflowFlow#include_deleted_records}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce(
            object=object,
            data_transfer_api=data_transfer_api,
            enable_dynamic_field_update=enable_dynamic_field_update,
            include_deleted_records=include_deleted_records,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        object_path: builtins.str,
        pagination_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param pagination_config: pagination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#pagination_config AppflowFlow#pagination_config}
        :param parallelism_config: parallelism_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#parallelism_config AppflowFlow#parallelism_config}
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData(
            object_path=object_path,
            pagination_config=pagination_config,
            parallelism_config=parallelism_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSingular")
    def put_singular(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putSingular", [value]))

    @jsii.member(jsii_name="putSlack")
    def put_slack(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putSlack", [value]))

    @jsii.member(jsii_name="putTrendmicro")
    def put_trendmicro(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putTrendmicro", [value]))

    @jsii.member(jsii_name="putVeeva")
    def put_veeva(
        self,
        *,
        object: builtins.str,
        document_type: typing.Optional[builtins.str] = None,
        include_all_versions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_renditions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_source_files: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param document_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#document_type AppflowFlow#document_type}.
        :param include_all_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_all_versions AppflowFlow#include_all_versions}.
        :param include_renditions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_renditions AppflowFlow#include_renditions}.
        :param include_source_files: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_source_files AppflowFlow#include_source_files}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva(
            object=object,
            document_type=document_type,
            include_all_versions=include_all_versions,
            include_renditions=include_renditions,
            include_source_files=include_source_files,
        )

        return typing.cast(None, jsii.invoke(self, "putVeeva", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk(
            object=object
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

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

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
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference, jsii.get(self, "amplitude"))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference, jsii.get(self, "datadog"))

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference, jsii.get(self, "dynatrace"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference, jsii.get(self, "googleAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference, jsii.get(self, "inforNexus"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference", jsii.get(self, "singular"))

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference", jsii.get(self, "slack"))

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference", jsii.get(self, "trendmicro"))

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference", jsii.get(self, "veeva"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593554ac43278ee390230a4247c3c01c51e0548a30a2265aa1fcba73a80f27fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "s3_input_format_config": "s3InputFormatConfig",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: builtins.str,
        s3_input_format_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_input_format_config: s3_input_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_input_format_config AppflowFlow#s3_input_format_config}
        '''
        if isinstance(s3_input_format_config, dict):
            s3_input_format_config = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig(**s3_input_format_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1960554cfccbfd49b0a7d416962b3c8e47204ef287de1e06ecfa15c38c724a2)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument s3_input_format_config", value=s3_input_format_config, expected_type=type_hints["s3_input_format_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "bucket_prefix": bucket_prefix,
        }
        if s3_input_format_config is not None:
            self._values["s3_input_format_config"] = s3_input_format_config

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        assert result is not None, "Required property 'bucket_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_input_format_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"]:
        '''s3_input_format_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_input_format_config AppflowFlow#s3_input_format_config}
        '''
        result = self._values.get("s3_input_format_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35682b3128dc6450c88ba32e0cf1dd195941ecad84337892cc934107a8ebb2c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3InputFormatConfig")
    def put_s3_input_format_config(
        self,
        *,
        s3_input_file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_input_file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_input_file_type AppflowFlow#s3_input_file_type}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig(
            s3_input_file_type=s3_input_file_type
        )

        return typing.cast(None, jsii.invoke(self, "putS3InputFormatConfig", [value]))

    @jsii.member(jsii_name="resetS3InputFormatConfig")
    def reset_s3_input_format_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputFormatConfig", []))

    @builtins.property
    @jsii.member(jsii_name="s3InputFormatConfig")
    def s3_input_format_config(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference", jsii.get(self, "s3InputFormatConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputFormatConfigInput")
    def s3_input_format_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"], jsii.get(self, "s3InputFormatConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05e746e8239ed240326f3d6b230c9f7269246e9ecdd603f49599dbc3fa49b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1531c64b9164353a5ae29e94c0e2734136e514af2be81137ccebda9bcb3a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed413489c5622deb2bb70cdad576b08666a34d35d269479c9f1cee3bd56b0142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig",
    jsii_struct_bases=[],
    name_mapping={"s3_input_file_type": "s3InputFileType"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig:
    def __init__(
        self,
        *,
        s3_input_file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_input_file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_input_file_type AppflowFlow#s3_input_file_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4b125128ce4c1396e1c7b1995ab13916fcd9b008753752a5579f9d0e2e0d3c)
            check_type(argname="argument s3_input_file_type", value=s3_input_file_type, expected_type=type_hints["s3_input_file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_input_file_type is not None:
            self._values["s3_input_file_type"] = s3_input_file_type

    @builtins.property
    def s3_input_file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3_input_file_type AppflowFlow#s3_input_file_type}.'''
        result = self._values.get("s3_input_file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41bd556b96d1b866c979f8b51e4bb02a920f0d4d1a277370f8cd302190231875)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3InputFileType")
    def reset_s3_input_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputFileType", []))

    @builtins.property
    @jsii.member(jsii_name="s3InputFileTypeInput")
    def s3_input_file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3InputFileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputFileType")
    def s3_input_file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3InputFileType"))

    @s3_input_file_type.setter
    def s3_input_file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468965409be00b2130e295765c3c09db1c34f4a25bb4ced113e16d116ba2dd14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3InputFileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0edaa07e9c5d5fc5a16a9938dbfc873d447be37fd8131098712fad3d65a8f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "data_transfer_api": "dataTransferApi",
        "enable_dynamic_field_update": "enableDynamicFieldUpdate",
        "include_deleted_records": "includeDeletedRecords",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce:
    def __init__(
        self,
        *,
        object: builtins.str,
        data_transfer_api: typing.Optional[builtins.str] = None,
        enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_deleted_records: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param data_transfer_api: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.
        :param enable_dynamic_field_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#enable_dynamic_field_update AppflowFlow#enable_dynamic_field_update}.
        :param include_deleted_records: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_deleted_records AppflowFlow#include_deleted_records}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3af5da59677baec1b66bc364d4ec3887aa003330e421225eb55795d7c76d6b9)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
            check_type(argname="argument enable_dynamic_field_update", value=enable_dynamic_field_update, expected_type=type_hints["enable_dynamic_field_update"])
            check_type(argname="argument include_deleted_records", value=include_deleted_records, expected_type=type_hints["include_deleted_records"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if data_transfer_api is not None:
            self._values["data_transfer_api"] = data_transfer_api
        if enable_dynamic_field_update is not None:
            self._values["enable_dynamic_field_update"] = enable_dynamic_field_update
        if include_deleted_records is not None:
            self._values["include_deleted_records"] = include_deleted_records

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_transfer_api(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.'''
        result = self._values.get("data_transfer_api")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dynamic_field_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#enable_dynamic_field_update AppflowFlow#enable_dynamic_field_update}.'''
        result = self._values.get("enable_dynamic_field_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_deleted_records(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_deleted_records AppflowFlow#include_deleted_records}.'''
        result = self._values.get("include_deleted_records")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebaf330df7fe47d75bfd037e1c69858839ce5f14e6a3cf8de614dd6c7a477efe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataTransferApi")
    def reset_data_transfer_api(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataTransferApi", []))

    @jsii.member(jsii_name="resetEnableDynamicFieldUpdate")
    def reset_enable_dynamic_field_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDynamicFieldUpdate", []))

    @jsii.member(jsii_name="resetIncludeDeletedRecords")
    def reset_include_deleted_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeDeletedRecords", []))

    @builtins.property
    @jsii.member(jsii_name="dataTransferApiInput")
    def data_transfer_api_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTransferApiInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDynamicFieldUpdateInput")
    def enable_dynamic_field_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDynamicFieldUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="includeDeletedRecordsInput")
    def include_deleted_records_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeDeletedRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTransferApi")
    def data_transfer_api(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataTransferApi"))

    @data_transfer_api.setter
    def data_transfer_api(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d848b74d83dcac6945f943441abd3ba6cd19ead31c8c765f4156e8025b50d529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTransferApi", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDynamicFieldUpdate")
    def enable_dynamic_field_update(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDynamicFieldUpdate"))

    @enable_dynamic_field_update.setter
    def enable_dynamic_field_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21dc5e292d236956d5fed45d6454ea4fb2846271eda4e9356bc50da729385a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDynamicFieldUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeDeletedRecords")
    def include_deleted_records(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeDeletedRecords"))

    @include_deleted_records.setter
    def include_deleted_records(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa72154db1cf08499a3d20f421c3393a03893cac6afd2af4205c40cf7105bb9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeDeletedRecords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7c7d94ee9238d71d138d5c82ef480f72d915bb308a1c8ea74d5989b2996160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__482425d76fd1f1a5167f37be2d1a328ef7cd7b770b5793c87bbbd1dd5823f0b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "object_path": "objectPath",
        "pagination_config": "paginationConfig",
        "parallelism_config": "parallelismConfig",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData:
    def __init__(
        self,
        *,
        object_path: builtins.str,
        pagination_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param pagination_config: pagination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#pagination_config AppflowFlow#pagination_config}
        :param parallelism_config: parallelism_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#parallelism_config AppflowFlow#parallelism_config}
        '''
        if isinstance(pagination_config, dict):
            pagination_config = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig(**pagination_config)
        if isinstance(parallelism_config, dict):
            parallelism_config = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig(**parallelism_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d14d224d5f75f5ce9e229d805b50a0aaa87bbd2c6ab8ca17e8f749ce3a66ca)
            check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
            check_type(argname="argument pagination_config", value=pagination_config, expected_type=type_hints["pagination_config"])
            check_type(argname="argument parallelism_config", value=parallelism_config, expected_type=type_hints["parallelism_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_path": object_path,
        }
        if pagination_config is not None:
            self._values["pagination_config"] = pagination_config
        if parallelism_config is not None:
            self._values["parallelism_config"] = parallelism_config

    @builtins.property
    def object_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.'''
        result = self._values.get("object_path")
        assert result is not None, "Required property 'object_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pagination_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"]:
        '''pagination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#pagination_config AppflowFlow#pagination_config}
        '''
        result = self._values.get("pagination_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"], result)

    @builtins.property
    def parallelism_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"]:
        '''parallelism_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#parallelism_config AppflowFlow#parallelism_config}
        '''
        result = self._values.get("parallelism_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8ddee1e8647f81b76f9a71710cbb2e3495f29f274498cadcf3ce850cbb657c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPaginationConfig")
    def put_pagination_config(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig(
            max_page_size=max_page_size
        )

        return typing.cast(None, jsii.invoke(self, "putPaginationConfig", [value]))

    @jsii.member(jsii_name="putParallelismConfig")
    def put_parallelism_config(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig(
            max_page_size=max_page_size
        )

        return typing.cast(None, jsii.invoke(self, "putParallelismConfig", [value]))

    @jsii.member(jsii_name="resetPaginationConfig")
    def reset_pagination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaginationConfig", []))

    @jsii.member(jsii_name="resetParallelismConfig")
    def reset_parallelism_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelismConfig", []))

    @builtins.property
    @jsii.member(jsii_name="paginationConfig")
    def pagination_config(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference", jsii.get(self, "paginationConfig"))

    @builtins.property
    @jsii.member(jsii_name="parallelismConfig")
    def parallelism_config(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference", jsii.get(self, "parallelismConfig"))

    @builtins.property
    @jsii.member(jsii_name="objectPathInput")
    def object_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectPathInput"))

    @builtins.property
    @jsii.member(jsii_name="paginationConfigInput")
    def pagination_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"], jsii.get(self, "paginationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismConfigInput")
    def parallelism_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"], jsii.get(self, "parallelismConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectPath")
    def object_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectPath"))

    @object_path.setter
    def object_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c934f3e720ef613a2d8948eccdd4c1d8d2560814e60872bd0b9d7e252ed845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e051fca70e67537de17190b7697231faa98d6a51a3ed27266a407ec557bcb62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig",
    jsii_struct_bases=[],
    name_mapping={"max_page_size": "maxPageSize"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig:
    def __init__(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8f54d0a959bc5efd5a0f7aa88cef358b4c8a6baa297af23dcab36c33a1875c)
            check_type(argname="argument max_page_size", value=max_page_size, expected_type=type_hints["max_page_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_page_size": max_page_size,
        }

    @builtins.property
    def max_page_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.'''
        result = self._values.get("max_page_size")
        assert result is not None, "Required property 'max_page_size' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e914d4290b889c518216c9d206f3d73c043fd7885617d262288a360c8abfaf59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxPageSizeInput")
    def max_page_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPageSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPageSize")
    def max_page_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPageSize"))

    @max_page_size.setter
    def max_page_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc7a87a215d50678dea8d26dee324bde4c25b227b40ea57a8e5cb21f7b39a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPageSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2c0c5ff15cdeb761c294b6604cdb74938b78605950dd7594961f1979ed6d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig",
    jsii_struct_bases=[],
    name_mapping={"max_page_size": "maxPageSize"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig:
    def __init__(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520a721409d6c1d62a67728a763d0dabc4ff533f2fe27d09885219bb7f737322)
            check_type(argname="argument max_page_size", value=max_page_size, expected_type=type_hints["max_page_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_page_size": max_page_size,
        }

    @builtins.property
    def max_page_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.'''
        result = self._values.get("max_page_size")
        assert result is not None, "Required property 'max_page_size' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9c4373e592c3707d1db73804ef9a57859601aa670f12bea026e33f2b6bfc6f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxPageSizeInput")
    def max_page_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPageSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPageSize")
    def max_page_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPageSize"))

    @max_page_size.setter
    def max_page_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8d453bc71fb4fa5f13661fd10ba5ee4776a43bebe6d1edb80663916a95f6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPageSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ebf53ce49b40cf3a17e2757cf7f7058b5a4ccf41736b17d97d3c5f513f9cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c59dabc229d2d9f7a92d6ba538f24c68f2b902ef131480f0ed09a41f488230)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__297aee73df4d7790e73046e1ba22cc573aca53fff536e5fffe4c1ce6d0df2e10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966ff77c09a8a17d3b0f66ccbf7e5913d82db8369f95b323c50e1e1ea110c7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f019093917f345e0d6aa7cac83bab9bb99f6b1a73a35b794e208164e8e28c27e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd26348b3548506ec1f29ecf149b91aa8fa53bc9160213a748dc6a05bc17d796)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ba9209a934452ee06ae5df3de4275c652afc5e40821755002d23f84ba5f945c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72efa7a4f8899534c9e3610e6f095bed563ff712d3c7ff55366d5accf5c2d8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6793919802a4944d38f92c4d698100dd578a321837b42ff55945f9bb1e5bea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11389da639b58d72225b21093edb5e2549d426d59b8bac51d5676fadbc19827c)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be3a11fd19c77da727fe680d669db11db264a14a77649b20b4ea929925d20d73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b1ad39f7ddf87dd3864b821f7a668362494b73f9a8a650e354ae9bc5c04b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db30b262f1b34db6236ec4123ae07f16a77dfad1d60c9f3fb3e63e515c8e8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640b1aab906fbd87b7c5131a22e9d8dc4f96832fccef6f5678718b26d718b254)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b88eca2a61192c89c75ba98e8f2ab71bb645651e8354ffe3203fcce686529c22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8cd5e41093bb8b123671c52e7c271fe8ef848eece9f3306158a696638b1925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5a499d05dc04cfa4b84b73faf81781bd422c8f68b96a9fd60ef29684ae09c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "document_type": "documentType",
        "include_all_versions": "includeAllVersions",
        "include_renditions": "includeRenditions",
        "include_source_files": "includeSourceFiles",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva:
    def __init__(
        self,
        *,
        object: builtins.str,
        document_type: typing.Optional[builtins.str] = None,
        include_all_versions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_renditions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_source_files: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param document_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#document_type AppflowFlow#document_type}.
        :param include_all_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_all_versions AppflowFlow#include_all_versions}.
        :param include_renditions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_renditions AppflowFlow#include_renditions}.
        :param include_source_files: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_source_files AppflowFlow#include_source_files}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f290a87dc94b9e789dfb64d3018514fa5527cc5e5bcb21ddc02feed930806d2)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument document_type", value=document_type, expected_type=type_hints["document_type"])
            check_type(argname="argument include_all_versions", value=include_all_versions, expected_type=type_hints["include_all_versions"])
            check_type(argname="argument include_renditions", value=include_renditions, expected_type=type_hints["include_renditions"])
            check_type(argname="argument include_source_files", value=include_source_files, expected_type=type_hints["include_source_files"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if document_type is not None:
            self._values["document_type"] = document_type
        if include_all_versions is not None:
            self._values["include_all_versions"] = include_all_versions
        if include_renditions is not None:
            self._values["include_renditions"] = include_renditions
        if include_source_files is not None:
            self._values["include_source_files"] = include_source_files

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def document_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#document_type AppflowFlow#document_type}.'''
        result = self._values.get("document_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_all_versions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_all_versions AppflowFlow#include_all_versions}.'''
        result = self._values.get("include_all_versions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_renditions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_renditions AppflowFlow#include_renditions}.'''
        result = self._values.get("include_renditions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_source_files(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#include_source_files AppflowFlow#include_source_files}.'''
        result = self._values.get("include_source_files")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__534b396aedf47ed1025ce7d9ca8af1d1859a552a9abd94745bd157a07f95422a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDocumentType")
    def reset_document_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentType", []))

    @jsii.member(jsii_name="resetIncludeAllVersions")
    def reset_include_all_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAllVersions", []))

    @jsii.member(jsii_name="resetIncludeRenditions")
    def reset_include_renditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRenditions", []))

    @jsii.member(jsii_name="resetIncludeSourceFiles")
    def reset_include_source_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSourceFiles", []))

    @builtins.property
    @jsii.member(jsii_name="documentTypeInput")
    def document_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAllVersionsInput")
    def include_all_versions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAllVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeRenditionsInput")
    def include_renditions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeRenditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSourceFilesInput")
    def include_source_files_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSourceFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="documentType")
    def document_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentType"))

    @document_type.setter
    def document_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a88dcc3fb3c42436552fbeba76585467cf533e87d924881f631d00d4d5b9c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeAllVersions")
    def include_all_versions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAllVersions"))

    @include_all_versions.setter
    def include_all_versions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211f08f497e93b8486f6b7b87b0c4a2a5240125258fcd73d234adea1f16915e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAllVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeRenditions")
    def include_renditions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeRenditions"))

    @include_renditions.setter
    def include_renditions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c02e66315bff96626e428d718bd47981df98f97b68837e197d44eeca1c9493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRenditions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSourceFiles")
    def include_source_files(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSourceFiles"))

    @include_source_files.setter
    def include_source_files(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36173f11f20b57ae047fb532ed70db42181bb5a728533be1b6c900625897a3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSourceFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1779609377bd87b250e61d8a5089946dae4a09a1ef654870da7cb54aa6223528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1016d297bb7627a64b55e9214b78f0e5bf5779d8bcb0b3b78759d37fc00a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5108e53872e2405281c5631623930b81b6b2436e909c5e0a9315f8ec004f8e7)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05e9bbad0bf8ff9b4a056011d6ec7c7b99fd7fa566e94ee51f18bca17914c5d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a21999e7b76c12a252b637e28742c47e9fa0dea6177cc33816e924e1d8c6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b3e79a2945e0bde491139eb5be8d35ac44305a5e6e20d696f16582951bbb66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTask",
    jsii_struct_bases=[],
    name_mapping={
        "task_type": "taskType",
        "connector_operator": "connectorOperator",
        "destination_field": "destinationField",
        "source_fields": "sourceFields",
        "task_properties": "taskProperties",
    },
)
class AppflowFlowTask:
    def __init__(
        self,
        *,
        task_type: builtins.str,
        connector_operator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTaskConnectorOperator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        destination_field: typing.Optional[builtins.str] = None,
        source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        task_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#task_type AppflowFlow#task_type}.
        :param connector_operator: connector_operator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_operator AppflowFlow#connector_operator}
        :param destination_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#destination_field AppflowFlow#destination_field}.
        :param source_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_fields AppflowFlow#source_fields}.
        :param task_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#task_properties AppflowFlow#task_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac785ffe16f428e8bae58cf17f09e15e658f24662be2fa36c7d9ecbbe7a77bf)
            check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            check_type(argname="argument connector_operator", value=connector_operator, expected_type=type_hints["connector_operator"])
            check_type(argname="argument destination_field", value=destination_field, expected_type=type_hints["destination_field"])
            check_type(argname="argument source_fields", value=source_fields, expected_type=type_hints["source_fields"])
            check_type(argname="argument task_properties", value=task_properties, expected_type=type_hints["task_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_type": task_type,
        }
        if connector_operator is not None:
            self._values["connector_operator"] = connector_operator
        if destination_field is not None:
            self._values["destination_field"] = destination_field
        if source_fields is not None:
            self._values["source_fields"] = source_fields
        if task_properties is not None:
            self._values["task_properties"] = task_properties

    @builtins.property
    def task_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#task_type AppflowFlow#task_type}.'''
        result = self._values.get("task_type")
        assert result is not None, "Required property 'task_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_operator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTaskConnectorOperator"]]]:
        '''connector_operator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#connector_operator AppflowFlow#connector_operator}
        '''
        result = self._values.get("connector_operator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTaskConnectorOperator"]]], result)

    @builtins.property
    def destination_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#destination_field AppflowFlow#destination_field}.'''
        result = self._values.get("destination_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#source_fields AppflowFlow#source_fields}.'''
        result = self._values.get("source_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def task_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#task_properties AppflowFlow#task_properties}.'''
        result = self._values.get("task_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTaskConnectorOperator",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "s3": "s3",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowFlowTaskConnectorOperator:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[builtins.str] = None,
        custom_connector: typing.Optional[builtins.str] = None,
        datadog: typing.Optional[builtins.str] = None,
        dynatrace: typing.Optional[builtins.str] = None,
        google_analytics: typing.Optional[builtins.str] = None,
        infor_nexus: typing.Optional[builtins.str] = None,
        marketo: typing.Optional[builtins.str] = None,
        s3: typing.Optional[builtins.str] = None,
        salesforce: typing.Optional[builtins.str] = None,
        sapo_data: typing.Optional[builtins.str] = None,
        service_now: typing.Optional[builtins.str] = None,
        singular: typing.Optional[builtins.str] = None,
        slack: typing.Optional[builtins.str] = None,
        trendmicro: typing.Optional[builtins.str] = None,
        veeva: typing.Optional[builtins.str] = None,
        zendesk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param amplitude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}.
        :param custom_connector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}.
        :param datadog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}.
        :param dynatrace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}.
        :param google_analytics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}.
        :param infor_nexus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}.
        :param marketo: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}.
        :param salesforce: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}.
        :param sapo_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}.
        :param service_now: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}.
        :param singular: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#singular AppflowFlow#singular}.
        :param slack: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#slack AppflowFlow#slack}.
        :param trendmicro: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}.
        :param veeva: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}.
        :param zendesk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdec0a5501b36e42b0ae642737c41cc4c3541208b85192ef7aa094376cc2e5bc)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
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
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if s3 is not None:
            self._values["s3"] = s3
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
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}.'''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_connector(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}.'''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datadog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}.'''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynatrace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}.'''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def google_analytics(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}.'''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infor_nexus(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}.'''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketo(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}.'''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}.'''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def salesforce(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}.'''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sapo_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}.'''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_now(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}.'''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def singular(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#singular AppflowFlow#singular}.'''
        result = self._values.get("singular")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#slack AppflowFlow#slack}.'''
        result = self._values.get("slack")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trendmicro(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}.'''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def veeva(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}.'''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zendesk(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}.'''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTaskConnectorOperator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTaskConnectorOperatorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTaskConnectorOperatorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__296a6cdbe2b29c0308e5ff4a055ca69cfe6a34aaf0e2110d82c04bfaa741625d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppflowFlowTaskConnectorOperatorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c1e8cb60d1c280c42e6b27a2dfa747113a43d36b5dbbf6a11bbeb2a5ea25aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppflowFlowTaskConnectorOperatorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47661404a26e19b0031614e47cd835b68a8d4173ef46504786834535be30ad43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6528151debc9f9095e9da3e2ae9a000addeac1c73f6d865eb036132cd68a2750)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c86a3b57c559847fa814fac2e13a433fc5cf902ac4c02b27cb4b52af5743cba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d8a0f366e76c4aa07ca2afdc9110f177c893be399e59bbe584d22062524092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowTaskConnectorOperatorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTaskConnectorOperatorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3bce4094c9c9f437c27b0076be1c3515e2911e47c551d835fecad43351f8028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

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
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="amplitude")
    def amplitude(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amplitude"))

    @amplitude.setter
    def amplitude(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f227f59a621ae59137ac87158fbb6966cdd0f2baabfa8e8a88b5d0d543d9c3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amplitude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customConnector"))

    @custom_connector.setter
    def custom_connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3381ce2151e60132de896fa3c134f50830cbbe49a518128e0678dbfa22f6f82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customConnector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datadog"))

    @datadog.setter
    def datadog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91024379644d639316198ae16eebf6c98cf618daabed27e16df67b11ba1f9abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datadog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dynatrace"))

    @dynatrace.setter
    def dynatrace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c0cc183f2ac1775cd82b523ec1c35f9fd4f4c57bf4bd8bc2f018211be8741f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynatrace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleAnalytics"))

    @google_analytics.setter
    def google_analytics(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2a948caa4fc25e86404885ecc157dc716a20f5cff9b388093c188273f04586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "googleAnalytics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inforNexus"))

    @infor_nexus.setter
    def infor_nexus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23e7fd0509a633878e87d4e1a0deda29a7ad4ae76d093c7beb8c8b4dea41783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inforNexus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketo"))

    @marketo.setter
    def marketo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa99c322115756f8e2c2ab1184a04f9dae98653a0073fbbe9dd2a6e97dddc07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3"))

    @s3.setter
    def s3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cbf7bf3f8cb158cd368d4d130d098a9bd417f63397c4e1133bef7f287c19b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "salesforce"))

    @salesforce.setter
    def salesforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2226382e080b6bb29f166fa3f6e1080b298f2ab8b32249f82430ccaf0f2419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "salesforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sapoData"))

    @sapo_data.setter
    def sapo_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1170782ffb67de367faa668d14bbcad6bc4ec9ff1f0577f894998573ffc0e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sapoData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceNow"))

    @service_now.setter
    def service_now(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e149ef723cca62ca270f01820eecfa021c50bd7c377b69535d3e9a665f54c1a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceNow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singular"))

    @singular.setter
    def singular(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32abf8ceddab3a238081ed61372d1af020446ffe528766953a79e322b2179219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singular", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slack"))

    @slack.setter
    def slack(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7158a6c4fd3d90269de25a6bca4dd4ee16d0a088bfba7f70d000f193d6ee09e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trendmicro"))

    @trendmicro.setter
    def trendmicro(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76e7124c811a6dc7d2d5a03f3ec1c64ddf52e6159be52d929bb1d25ddf590dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trendmicro", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "veeva"))

    @veeva.setter
    def veeva(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1fedec54732a09ba1f8c144a4b4517e5cdcef99a8ba06f656d1cd79a1dc4151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "veeva", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zendesk"))

    @zendesk.setter
    def zendesk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c561e51695fdf559fdab0d77d1bc517e1b7ccf28d835aef5497946a2c561321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zendesk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df45efbc88cbd368953cbd7d4f7b85180082c0ea77320e3e985d32f7c576c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowTaskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTaskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdda4e71ea08feb58b1c73ddfb02a2a7b3ed10f0b7d9a4a937b79e72975b6d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppflowFlowTaskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28df48823d645a4e9417962e5e47440cc1ef0fc3277c9977e006684f2c26137d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppflowFlowTaskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0346625da2d68e5bc374589a9d416f933a79e8931b5df63e7dc0fd1fbb2fd29a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b55ddbcda17eecf0b3753f2c0daf07ac44fec9ac68b3cff1c65d5c8b6ecda61b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__241c79bab0c4980e32928316f4c4f26eb196933e3a037167cc1cfd72b74d83a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e069bc0ee24612e2c9870815ae34e1245997175d9e5d9f4a2e4310cb2e67ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowTaskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTaskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14383d6c71d12d36dfa7345104e58af54041c924be78cb0d0ca307ec764002b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConnectorOperator")
    def put_connector_operator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTaskConnectorOperator, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e1d7c5114777a454f4dfe6c12f6fd1c8c22f1c1855e76818c6a9ef31bd303f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectorOperator", [value]))

    @jsii.member(jsii_name="resetConnectorOperator")
    def reset_connector_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorOperator", []))

    @jsii.member(jsii_name="resetDestinationField")
    def reset_destination_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationField", []))

    @jsii.member(jsii_name="resetSourceFields")
    def reset_source_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFields", []))

    @jsii.member(jsii_name="resetTaskProperties")
    def reset_task_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskProperties", []))

    @builtins.property
    @jsii.member(jsii_name="connectorOperator")
    def connector_operator(self) -> AppflowFlowTaskConnectorOperatorList:
        return typing.cast(AppflowFlowTaskConnectorOperatorList, jsii.get(self, "connectorOperator"))

    @builtins.property
    @jsii.member(jsii_name="connectorOperatorInput")
    def connector_operator_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]], jsii.get(self, "connectorOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFieldInput")
    def destination_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFieldsInput")
    def source_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="taskPropertiesInput")
    def task_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "taskPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="taskTypeInput")
    def task_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationField")
    def destination_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationField"))

    @destination_field.setter
    def destination_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00807a099b2a0e356c5811891d7a88bc5208dea5784b9d18301b96d32696ae44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFields")
    def source_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceFields"))

    @source_fields.setter
    def source_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa38934794db6a7a91ce131d9926dc710c46c46ede0bcb7fe9f2e861ef9e637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskProperties")
    def task_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "taskProperties"))

    @task_properties.setter
    def task_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4192c67e3f5edcf166741432f7f92f537b45ea00dc319274561bfecd050755d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskType")
    def task_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskType"))

    @task_type.setter
    def task_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc36bfd7a9738e35247ab25862cdf947a17a949959b4c93484457e8bcc454db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fe2ddecd9a0152ce68e1fff21ff175b5f974aa974c8e11ed97287eccd7172d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "trigger_type": "triggerType",
        "trigger_properties": "triggerProperties",
    },
)
class AppflowFlowTriggerConfig:
    def __init__(
        self,
        *,
        trigger_type: builtins.str,
        trigger_properties: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trigger_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_type AppflowFlow#trigger_type}.
        :param trigger_properties: trigger_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_properties AppflowFlow#trigger_properties}
        '''
        if isinstance(trigger_properties, dict):
            trigger_properties = AppflowFlowTriggerConfigTriggerProperties(**trigger_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df22188bd1fcbf9414eb4896e0eb6bfc62ed93a9fe0911b7c7794e6ba2b767f)
            check_type(argname="argument trigger_type", value=trigger_type, expected_type=type_hints["trigger_type"])
            check_type(argname="argument trigger_properties", value=trigger_properties, expected_type=type_hints["trigger_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger_type": trigger_type,
        }
        if trigger_properties is not None:
            self._values["trigger_properties"] = trigger_properties

    @builtins.property
    def trigger_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_type AppflowFlow#trigger_type}.'''
        result = self._values.get("trigger_type")
        assert result is not None, "Required property 'trigger_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_properties(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerProperties"]:
        '''trigger_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#trigger_properties AppflowFlow#trigger_properties}
        '''
        result = self._values.get("trigger_properties")
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTriggerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTriggerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5afa3bebc88af9f3e98b659e3d6efab07557e36778bb139a5467cb3e6595579a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTriggerProperties")
    def put_trigger_properties(
        self,
        *,
        scheduled: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerPropertiesScheduled", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled: scheduled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#scheduled AppflowFlow#scheduled}
        '''
        value = AppflowFlowTriggerConfigTriggerProperties(scheduled=scheduled)

        return typing.cast(None, jsii.invoke(self, "putTriggerProperties", [value]))

    @jsii.member(jsii_name="resetTriggerProperties")
    def reset_trigger_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerProperties", []))

    @builtins.property
    @jsii.member(jsii_name="triggerProperties")
    def trigger_properties(
        self,
    ) -> "AppflowFlowTriggerConfigTriggerPropertiesOutputReference":
        return typing.cast("AppflowFlowTriggerConfigTriggerPropertiesOutputReference", jsii.get(self, "triggerProperties"))

    @builtins.property
    @jsii.member(jsii_name="triggerPropertiesInput")
    def trigger_properties_input(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerProperties"]:
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerProperties"], jsii.get(self, "triggerPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTypeInput")
    def trigger_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerType")
    def trigger_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerType"))

    @trigger_type.setter
    def trigger_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294983ecaca1fc52c04301b33f59acd7fcd61761fb092f16060f779422ea5bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppflowFlowTriggerConfig]:
        return typing.cast(typing.Optional[AppflowFlowTriggerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppflowFlowTriggerConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7589dd285ac1137d5214eb3054a9711718613ba0f8b279e7cbdb074dcef3fe8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerProperties",
    jsii_struct_bases=[],
    name_mapping={"scheduled": "scheduled"},
)
class AppflowFlowTriggerConfigTriggerProperties:
    def __init__(
        self,
        *,
        scheduled: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerPropertiesScheduled", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled: scheduled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#scheduled AppflowFlow#scheduled}
        '''
        if isinstance(scheduled, dict):
            scheduled = AppflowFlowTriggerConfigTriggerPropertiesScheduled(**scheduled)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__508662c09014ef3cabe6d56a423e9c4f47ae926cc25b8549ec9a118d3b6ef254)
            check_type(argname="argument scheduled", value=scheduled, expected_type=type_hints["scheduled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scheduled is not None:
            self._values["scheduled"] = scheduled

    @builtins.property
    def scheduled(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"]:
        '''scheduled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#scheduled AppflowFlow#scheduled}
        '''
        result = self._values.get("scheduled")
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTriggerConfigTriggerProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTriggerConfigTriggerPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8b93918121ff8624a4c364cf3cf710844bb6985ab8d8aaf5594375243ceb106)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScheduled")
    def put_scheduled(
        self,
        *,
        schedule_expression: builtins.str,
        data_pull_mode: typing.Optional[builtins.str] = None,
        first_execution_from: typing.Optional[builtins.str] = None,
        schedule_end_time: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        schedule_start_time: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_expression AppflowFlow#schedule_expression}.
        :param data_pull_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#data_pull_mode AppflowFlow#data_pull_mode}.
        :param first_execution_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#first_execution_from AppflowFlow#first_execution_from}.
        :param schedule_end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_end_time AppflowFlow#schedule_end_time}.
        :param schedule_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_offset AppflowFlow#schedule_offset}.
        :param schedule_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_start_time AppflowFlow#schedule_start_time}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#timezone AppflowFlow#timezone}.
        '''
        value = AppflowFlowTriggerConfigTriggerPropertiesScheduled(
            schedule_expression=schedule_expression,
            data_pull_mode=data_pull_mode,
            first_execution_from=first_execution_from,
            schedule_end_time=schedule_end_time,
            schedule_offset=schedule_offset,
            schedule_start_time=schedule_start_time,
            timezone=timezone,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduled", [value]))

    @jsii.member(jsii_name="resetScheduled")
    def reset_scheduled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduled", []))

    @builtins.property
    @jsii.member(jsii_name="scheduled")
    def scheduled(
        self,
    ) -> "AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference":
        return typing.cast("AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference", jsii.get(self, "scheduled"))

    @builtins.property
    @jsii.member(jsii_name="scheduledInput")
    def scheduled_input(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"]:
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"], jsii.get(self, "scheduledInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowTriggerConfigTriggerProperties]:
        return typing.cast(typing.Optional[AppflowFlowTriggerConfigTriggerProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowTriggerConfigTriggerProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bea63811f086289a01272fdef6a3987ea5f51e58f2e1eb023d6d86f028eb11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerPropertiesScheduled",
    jsii_struct_bases=[],
    name_mapping={
        "schedule_expression": "scheduleExpression",
        "data_pull_mode": "dataPullMode",
        "first_execution_from": "firstExecutionFrom",
        "schedule_end_time": "scheduleEndTime",
        "schedule_offset": "scheduleOffset",
        "schedule_start_time": "scheduleStartTime",
        "timezone": "timezone",
    },
)
class AppflowFlowTriggerConfigTriggerPropertiesScheduled:
    def __init__(
        self,
        *,
        schedule_expression: builtins.str,
        data_pull_mode: typing.Optional[builtins.str] = None,
        first_execution_from: typing.Optional[builtins.str] = None,
        schedule_end_time: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        schedule_start_time: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_expression AppflowFlow#schedule_expression}.
        :param data_pull_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#data_pull_mode AppflowFlow#data_pull_mode}.
        :param first_execution_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#first_execution_from AppflowFlow#first_execution_from}.
        :param schedule_end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_end_time AppflowFlow#schedule_end_time}.
        :param schedule_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_offset AppflowFlow#schedule_offset}.
        :param schedule_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_start_time AppflowFlow#schedule_start_time}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#timezone AppflowFlow#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fc03d1d6f52547e9f24aa67a74c6ae40b1902a1d6fb73ad51b82c88a85acc8)
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument data_pull_mode", value=data_pull_mode, expected_type=type_hints["data_pull_mode"])
            check_type(argname="argument first_execution_from", value=first_execution_from, expected_type=type_hints["first_execution_from"])
            check_type(argname="argument schedule_end_time", value=schedule_end_time, expected_type=type_hints["schedule_end_time"])
            check_type(argname="argument schedule_offset", value=schedule_offset, expected_type=type_hints["schedule_offset"])
            check_type(argname="argument schedule_start_time", value=schedule_start_time, expected_type=type_hints["schedule_start_time"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule_expression": schedule_expression,
        }
        if data_pull_mode is not None:
            self._values["data_pull_mode"] = data_pull_mode
        if first_execution_from is not None:
            self._values["first_execution_from"] = first_execution_from
        if schedule_end_time is not None:
            self._values["schedule_end_time"] = schedule_end_time
        if schedule_offset is not None:
            self._values["schedule_offset"] = schedule_offset
        if schedule_start_time is not None:
            self._values["schedule_start_time"] = schedule_start_time
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def schedule_expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_expression AppflowFlow#schedule_expression}.'''
        result = self._values.get("schedule_expression")
        assert result is not None, "Required property 'schedule_expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_pull_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#data_pull_mode AppflowFlow#data_pull_mode}.'''
        result = self._values.get("data_pull_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_execution_from(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#first_execution_from AppflowFlow#first_execution_from}.'''
        result = self._values.get("first_execution_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_end_time AppflowFlow#schedule_end_time}.'''
        result = self._values.get("schedule_end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_offset(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_offset AppflowFlow#schedule_offset}.'''
        result = self._values.get("schedule_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule_start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#schedule_start_time AppflowFlow#schedule_start_time}.'''
        result = self._values.get("schedule_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appflow_flow#timezone AppflowFlow#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTriggerConfigTriggerPropertiesScheduled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b42bebb22e77e09e865ee505af1ced75970a02b5a0add7402247923f8ac227ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataPullMode")
    def reset_data_pull_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPullMode", []))

    @jsii.member(jsii_name="resetFirstExecutionFrom")
    def reset_first_execution_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstExecutionFrom", []))

    @jsii.member(jsii_name="resetScheduleEndTime")
    def reset_schedule_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleEndTime", []))

    @jsii.member(jsii_name="resetScheduleOffset")
    def reset_schedule_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleOffset", []))

    @jsii.member(jsii_name="resetScheduleStartTime")
    def reset_schedule_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleStartTime", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="dataPullModeInput")
    def data_pull_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataPullModeInput"))

    @builtins.property
    @jsii.member(jsii_name="firstExecutionFromInput")
    def first_execution_from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstExecutionFromInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleEndTimeInput")
    def schedule_end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleEndTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleExpressionInput")
    def schedule_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleOffsetInput")
    def schedule_offset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scheduleOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleStartTimeInput")
    def schedule_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPullMode")
    def data_pull_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataPullMode"))

    @data_pull_mode.setter
    def data_pull_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3fbd43f23771b96f22b9d02ed02b67cc1f812ea71c011a198b33513ca94d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataPullMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstExecutionFrom")
    def first_execution_from(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstExecutionFrom"))

    @first_execution_from.setter
    def first_execution_from(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbeec3ed2615adb9323084ebaa71146302e9a2fd3d3fa4947266a267f8608074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstExecutionFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleEndTime")
    def schedule_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleEndTime"))

    @schedule_end_time.setter
    def schedule_end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1191a3767d3f00f3f8c444128b0a464e6a31d032bb3cb97a52a7151eadc418ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleEndTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleExpression"))

    @schedule_expression.setter
    def schedule_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f82ab9fce08435b59f855e6c7f3839c9c069c609d06bc72d62b1b989758b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleOffset")
    def schedule_offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scheduleOffset"))

    @schedule_offset.setter
    def schedule_offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0dedea7c121e0f8d3a2bab212df8f49a8e9155bdf32eefa8af8c31918a1808e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleStartTime")
    def schedule_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleStartTime"))

    @schedule_start_time.setter
    def schedule_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fc925c7873203a1cf872dcbc25e4bac2ba0bfd88f810d5218f3f5ea91abbdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcc82148b97bafc233050ba4ce62ea357bad1b94053082f3fd205f9f89ce582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled]:
        return typing.cast(typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45d06a9e2af347a05d2a443b4f9133d565c0f064bc9a354ec1b19c38d1ece81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppflowFlow",
    "AppflowFlowConfig",
    "AppflowFlowDestinationFlowConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorProperties",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference",
    "AppflowFlowDestinationFlowConfigList",
    "AppflowFlowDestinationFlowConfigOutputReference",
    "AppflowFlowMetadataCatalogConfig",
    "AppflowFlowMetadataCatalogConfigGlueDataCatalog",
    "AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference",
    "AppflowFlowMetadataCatalogConfigOutputReference",
    "AppflowFlowSourceFlowConfig",
    "AppflowFlowSourceFlowConfigIncrementalPullConfig",
    "AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference",
    "AppflowFlowSourceFlowConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorProperties",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference",
    "AppflowFlowTask",
    "AppflowFlowTaskConnectorOperator",
    "AppflowFlowTaskConnectorOperatorList",
    "AppflowFlowTaskConnectorOperatorOutputReference",
    "AppflowFlowTaskList",
    "AppflowFlowTaskOutputReference",
    "AppflowFlowTriggerConfig",
    "AppflowFlowTriggerConfigOutputReference",
    "AppflowFlowTriggerConfigTriggerProperties",
    "AppflowFlowTriggerConfigTriggerPropertiesOutputReference",
    "AppflowFlowTriggerConfigTriggerPropertiesScheduled",
    "AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference",
]

publication.publish()

def _typecheckingstub__30d8912010333000454cbf0c65b1f6e3ac0661fc69209522717ea8a534f14c34(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowDestinationFlowConfig, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    source_flow_config: typing.Union[AppflowFlowSourceFlowConfig, typing.Dict[builtins.str, typing.Any]],
    task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTask, typing.Dict[builtins.str, typing.Any]]]],
    trigger_config: typing.Union[AppflowFlowTriggerConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    metadata_catalog_config: typing.Optional[typing.Union[AppflowFlowMetadataCatalogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e1529ec5157a8972f07dd5e138b3529e9a2f2706da2407a15f150d02dede65dd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbc5880479a4f92b9a8bc4df33440645ee2f3078e82cc44e8edbab333de33a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowDestinationFlowConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9089c0d28179f8ee7ad2bac5ee19f1688d1bed507421e112a5b59b8d55512d5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTask, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43144f57e20621519e3bbac26bbf52308b7e6cbadee51b6a6140addc6312080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a4362db5d23ff9333b9e1633a715bf887e897ca3fc2de5422abbd83f47676a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30917fe220eb051a92c4a106c5e3c7be2df8c52a89344f6c71b4c3b079384034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99eaebb35798a2d45c68288b85ea45facbb40c9040ec66295a3d5fc237eefaa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1ea8d78a2167a706c73485d6fa479b2a32c7f02ff5c28805f98e29a5ee5e30(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22626e2259c7a951b2e71f2282e68f98c3647c10c60c231228b6a1317d79c82(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5fd331020a945882c9cc3561daf42aa20a0e2701f2c2ccd72ef3ed193a2f30(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowDestinationFlowConfig, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    source_flow_config: typing.Union[AppflowFlowSourceFlowConfig, typing.Dict[builtins.str, typing.Any]],
    task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTask, typing.Dict[builtins.str, typing.Any]]]],
    trigger_config: typing.Union[AppflowFlowTriggerConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    metadata_catalog_config: typing.Optional[typing.Union[AppflowFlowMetadataCatalogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc750cf8766c07181e8efe398a097ef2e21accdf60c72e03030ee3ca081aaa7(
    *,
    connector_type: builtins.str,
    destination_connector_properties: typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorProperties, typing.Dict[builtins.str, typing.Any]],
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8432ec939175200818ab9360fb66f1a016217afff588107a294823237e6cb3f(
    *,
    custom_connector: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_profiles: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bridge: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge, typing.Dict[builtins.str, typing.Any]]] = None,
    honeycode: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
    lookout_metrics: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    upsolver: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c260ff2ee9c096e40266ee68a31f50933e445d1717c1aecf73f6d03affd25a2a(
    *,
    entity_name: builtins.str,
    custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002a6807352cf6cf096dbda89df004e19690f8d06251c6c1dce0e2658b70476a(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6d64b5a760f4a27b92723ce062ebe8e7e28b2f363c01e4c8d07517e1be3e0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac3291f9b1814df3d9a2acd63a1492904a929a632126c6e555c589ac4ddaf83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99de399e1354c84ce95d9cd10a347363e4fa7c6b891c4b200f42847620873558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a6b6e2227103d1b7a264dc9a0260eab88cf59cf4aaccfeb45b876b9267fadd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bd98288ac88df5458effdacd5aea6bb190eb709b57160eeafe4c02fecdd0f8(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33458563f58e501465332440a9d055246b8faea5457088542ba7e54e2ec97646(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9edcfa168a31273dbb85109f4b2f9c0f5e3294aa2a091a488f184a36840dd67(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdbf2b78ef547594c864eb142fa39b47819ae1f5124641d879521cc25dd354d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d3694890146273c796f7a42bf6cb9f4236fd15a7f4ee0e655d055fb5b6c19a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814ab467c242749c549d23e305c6cea4edf688a5284194eee01acad12a394e09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4906f72fdc8edbd1c354817bb65f51a97a0280bea4c16b651a19d8d79545ffb(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd40c27555f3b981d849934f1bb8f4041533a8c5e2571876beb17b002e87a4f(
    *,
    domain_name: builtins.str,
    object_type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a352abe28d40d9f39d7cc37cbdc50bd2f73925d22f7fb8e6183100e174343dbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c5921c8a3235fc3d8f9bbb427639e122493b4ce85c552f039e2630b2b37dcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35969b779f23675ffcebf0750fddc80eea827775cbb2037b4a26b39a36f5c880(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae816928e81255454bb85b720285faef110332d2c20706af0153bc0ff903e875(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9511721f765c7f4110f5cbe3dd4a39994ef8e5174af9aaf4cec5dcac147b41c(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4184c3515a58d1f5be78cbfc6e0b456a90f5d4bb566ed80e1b064ae8a449f33a(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4576b4833efc9bb003f86f23fb3b9cc1d96c88a011f9939e5e70dafdc8db4532(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8878456f0009ec7d86f01e82ecac475e44c8767a4ee89a774f1e0b622b1aa931(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbed43e13503f241cf855ccdafcf9c202c4b2d4d0766586e92c3bec7c713796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451113c9b550c47f27529cac89de0038dac44db64d26f9d734093c2aa715e3fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ea33bad3287ecc66aae6caf8c623aa81ead6ae084d4f0de257cfe2e7a06e79(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cd5d7fbad6e307aa3ceb8bf81d5a8d7c6a73544f9659da9b1429667657cc9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2a66b2f40229c96d75bf5cccb56358e8138b8c67812016aaf8f5b6f57412e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ca4bec7cc4a7502192ed535a6d7a70007e96d76f6d5b1208628ceb3372f638(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9607350e66f9d4c73de559e3d834ae768b8afbdfea37723e6f7a6011a96390c2(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884504dc6d1279515b47026cf454e4648ccfbc51d5bece5fa7620e4e61e20d88(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5b16c89e1d9f75c3297ce8aeffe2c3ba2e6035c412caccb97c7af7212f9c0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb2125f4dfb5928dc9371eac809881cb4afa7f8cb9f8ec3dfc630626f44a518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f836c2085696ad6344a1ab3fd67e4974f3dddd2e6643af7b8677546869c6cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d319ef6d33770dd4e2fd1c01932723cd70f17e210080bb8424762f9938c6a571(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d33c9f033f8411b2350b08e38eecb1b9aed0cd46851e1369584ad07bc208e40(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7325aa232a697122dbc21a0c80e47d66ecb56dc3b42c6dd49adb1be3e2b91b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d577e4d097a5077f5a9c238540fa6bda2fa13e132efe3d4b2dfe4bdf33f20cb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac70bd9cc6bf155e3a486bd2ae0f000abbc76ccc8f83e0467c6e11478d46badb(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb8dffd28f2d83ed5c87a77e4f89fb7e6944392116b22a1304de34e785bd3a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5525588879197e15f3bde180985e662e809560f16ed3629e554851f66ff5e92d(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b37f3c2b6f30fc0156e96a44a5d068362647b3a1b80dd6cfbdad737b84b757(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdce1e90419b7c1196d86468d4e01fd14afec86ad3eeb70ecd0c64cf920c3fd(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6722a00bce1c1d5abcba312d746777b5afcde66e6566108128321d0d2a9c452(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf8986ac2602f874236c5e6d5591314dfd08834e5e9d164b8249e00f02499ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8009e0a305864018f7378ff409c2f5a5107bb6f015029ad69684b45fb801bdf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2300d390700b04569cee5660da97f31cf7008d26e85ec10c1be18b507854fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9e59ef239b5b66328c9fad106161d3db937e8b785bb0c4ef850bb43b89823a(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a6d7d6131958febf42a2061e616a51fb8380398fe4465f6a24fe3e88fd0d34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1cacf282b11d59c5258b236a2634c95bd26e5fa7ff3559dab2d065d4158ed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2ca4a49cefc054f233348fd7ce3bc96909949f58e5747344821f21d177c725(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1573fbd4b55788ccd1a1a67eb621dd6914b2a02788a637f959951669b492bfb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb036a4729236edfcf1539faa27822cc81468a19b7e6e398bd0ecd61e66c8c79(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc3a2939798abf0bbb0680af559bdc16656d1ad3f0becbfef242b9b2bf85d36(
    *,
    intermediate_bucket_name: builtins.str,
    object: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c7983a9f4aeb6fa8badd6ae8a422981379a724f96b916ba2f2119766f5a650(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5332f758cb4b2d1d906f1cca91b5cf172529aacb223b4e2c2026b6c78905909c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdcb6ac1015e2ef453760ece5d9237978f238085bd5c32c6659c803457c0692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e95c954861016f7832a7137f2b2ca615cf7427b569d83949b95e70de5a578a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d794b86c48f1dd6fcacc874c3087d326c1335e119e4fa9ec750f4fe6186cdfd9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7283d6bf7ae9ec9802c80b7e9946eaab271ae01bb1a5e3c41d3338d16e4695a(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1e0d99a4a719293c4cd82176e7f36fd8ba62ebb536aa80d869b970c3484af5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ac9543f1ad2aae4ca860d5d5403950f2c21234b1fa7d8499bad3a72cce5827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd63a3d2ddc68bb8c327a1248f70a1c4ca6e75b690896d05d7ac75c3197054a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b3099346f04e244d30fb213aee47f423a41ef470697ca139879cbfa1d6c94f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23de7386ef2a405f46c79176e1671e4ee70da45ba823c34bf39b99b1cf2227f2(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ec773bb1d99edf024af231020aea695d79c83fe23f65e59fbcb9c1ca007254(
    *,
    bucket_name: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    s3_output_format_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62956e2917ff4eb007a8a3f4748e5c34ab017890ece72141d6d39760e3ff26e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321690f2bfdaad8980049ce025230a2e03426148df91a558e98e97f53dbea918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b3c6f88384f39520c19c029699de260518036cfc731f5fb93646666369d9fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9790fa7ac8af18f1248b7bd74935596d3fcec9659dcdd12ee5369210be2e674(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52945ce783444b85156919463f6b8c7bdee7784e80d6088dcc7e0589eef6c714(
    *,
    aggregation_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    file_type: typing.Optional[builtins.str] = None,
    prefix_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584ecfe1fdfc18f2e99a94fd3203e8d593da524a9cc8326b34d890ccd45ff55c(
    *,
    aggregation_type: typing.Optional[builtins.str] = None,
    target_file_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2c835bcef10f90bf084ece9adc3d2f793f95d938ecd3cb58c1f6e99af593c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437e644918a740d6296cb2655278cd48ca1804b5c67f51ade496486181b712fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a9d2bf5144026b3df293596a5148086865219fb1aca14562a784e8169f087e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b17fc41e9040831ce8edadaa62f4af246df86432cea456fdcbd1a67f0394032(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbe9e0a9fe313001e415670130c14a3c9553f0601cba23025d5fc5e99fa7200(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f079efa86233624cb98e6529ea77527bc057bc0fa40fbb5948a002f1d5dc7d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9617d5a3c4a68552e8af540840f24c088d79d320394f61b500796cc430a188cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da50d507ec50d131340ae710eef29dfed1a27584228c9a878f231e14808d01f8(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d04afd9f0724df621192a3203519fb6fce4f3a6cbbd4d9cef1f48e49c13043(
    *,
    prefix_format: typing.Optional[builtins.str] = None,
    prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6407b3492d71380ec9e084a5356ca0bb8da6f09f54fc771a87099cabf9d8c5cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf5a82ef2e40302d8d2af1553f3105b4b7c408bfb0c6a7b0a251f5d499d4773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8ac6bdfd184cc540221b675e30cf4f7fb100fe54af2d566088352f3c9cb4be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0703fbf39d1c295ac62646be5048af8775c2b31fc77f9ffc314ded51621db258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1054974018b4cd7d1abfc8b4b69c9325c044df4cb4b5296022c5d37e75871f(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8965e3d6fc8000a051b3f5eab6dfcb5f63683ef1cb3c3e6beedb20475de42ec2(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66e4879c08d751a122672d38a83a381c7c0011cbd68a14c7e7583f9eac20d8f(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d68ae52b72937d8212df24e59cc908b28df9ca147c201d6e33e74b775773c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58a16b8d9e6718c05ee396d32daf76270ecb8b479cf309e8b7973ebf56e7a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f54d7f82abe2ebd1e2af0ec95c8f160518644a2d68112d24d9a8f0f6d6622b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895defe93a45f0b079d7dd78f874a3da14ce656a60dfc18209650771e79f7dc4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa3f8ef5227807366aff42f96033708bcc3382267f2a4a77dd578cb4e8958aa(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51010cfc882e9901eaa398332f8c013458ef75117fdd9992bb0b46c046960b76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff458f8bc5afe339e9e48eb5d5fdb81ec0d7dc55afea4c65f9df04f8e3d416f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5272e966f7dfe576b57efb5d3197b63894944cd89a83567a2ca8beb0a9a0a43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976ff5ca0389d5c30647ea4cd1381b97ad0eca1c24d191637338371d19ad5c45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c99c4c3b502f4043e7d94491dadc1106a670d023067d07cb9b3770fd3865d5e(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c413aed1791e9486bf60de96be672d4576beec0fe6a17e59542fd515530f06e(
    *,
    object_path: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    success_response_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba250468ec5e5637d5adfd26b974a1ee3c5545f6072704398a9d2cd59841fe7(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e718ca2d6a2961e94e0740c9761a9a91427e72560ede490f0f40453eaa2e4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab0163e996bcda5f42e01976d50e558da0c0ffbcc59eebe4948bdb44f34f1ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470acb0dc796c6a9a01c26f920ba049d679489b66631a067b44748c6ed52eb26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497fbd4b318b29828023f6b19af6eea7925dddb7cc3cbbeb00548fd30f08da8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbad9786a98ad87a853b08ab81b5b39f0ea501fd3799927ed671601930b56e5b(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40c01fbe90c6b91161eec35ff1bc55675c8066c49360a5b928bcabe7cd35363(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54a7eda343441240aa41433efa73d9ece0da69134e202f652a0bc3a17e0fae8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb63cfddbe9e959bafd6114a138e97ee8247d9ff4d6aaea923f6b12012f7dce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc7c83ed2343919ef3bc999bb8b592a19c6bf8401dd5c4140b20fbeb595d5c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8263d36f0dd5e923442e6d544d80aab11cf5e16efc29c739e8ba6fb792cb95a(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfcb15d6979b5e5531fe10d2b05282c9899beb501006fe1ca0d5edab3761b02(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d026585aa5b840dc4a19f5a53f15f3496eb04f65a1b354e03f3eba8c5c11356f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd6b7a9d25412346ce712c6ee824f5d92df059221d5bc359e18b5c2a79416af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409758b985689de93465e1efdef359d7254a739b7a8df5b7b46a89a22bebf467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2444ad494a31eda60312eaf20ceb25e4eac8d33e1e3a5ad903516848bec145(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b121ef03d25e81ba1b8aa0074d5831187018bdefdd1220d8e74b64d1d18893d8(
    *,
    intermediate_bucket_name: builtins.str,
    object: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a5e8cabe13fd56ffb3b34d041068b85652af1f7a494335885ee767812e61cc(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007ef3d880e7ccf5d4e907c9fbf50ad335e2dc7b9f18f6f27cb84ec4b89a4ad1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad732d24bf392429c19dadb2c23827bc312c32ce4019dc0128460bf44a31865b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2feb635677cd8c7c44dc668c3618cb908cfdfd65d36719e4f3a79f0d5ad8e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f85cc384c3b4d4060b88bbeaff5b7b502bff5f0d9c8355d9c197d0545306e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdafe2f49137f1e80f664bc50605e0397e78bb49e10eebd956e0554969a7a346(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ba749bdf3f1ff85535e60ce8fd5bfd0dd5aa4fcf8f970f8047623c0ce7285d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c092ba298beff37f762db686808bbf921364c6e5d7a60eedcf481a7d81066f7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa58b872214896d48cd62cbcb094aa70ed7880aae64415af70b28c5a402856d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8809aadccfabd8a59aaf6467732d6ec1d9ddf2bd9207fb5ac3b4238a60ed12b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb0e3fdb5767b3ce85a6f738a021c67599cbb3de1ff024f23e12bc97f702a7d(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d40b297f6b1802da6ddc9387ddd5a4dc647df19eaf73b92f7513a7e44c8945(
    *,
    bucket_name: builtins.str,
    s3_output_format_config: typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig, typing.Dict[builtins.str, typing.Any]],
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dafd0adf8720736a6ddeabcc785b25a87b0db1ae166684e36f851b9bade752e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501f124740a2518ffa9c3567a80c64f1c87e10d869ef291f357678361ed69825(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb06cd9e063e7e9c73fb280d8edbe8b3b1c1ca9e6f75bd092fcf072045635441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdbd2f32ba3e878aad354f1a52a824d7ca75c12297e1a6b5696f35d1d5a81e1(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988f2d3b908fe51becade7bd8cd11fd3f963ea9b421f3266b788a3f9ca373bde(
    *,
    prefix_config: typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig, typing.Dict[builtins.str, typing.Any]],
    aggregation_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab819b17d7d798618d456f980572d2937f88b2d86e91c25357391849f3fe611(
    *,
    aggregation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc58910bc9b60417d12a822aac9b740c448ca0f16158b0a770c2a5a806f2f249(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7678d971a00fabf44b6c613c14d4e73b2da0c412ea614be99c24bbdad6868fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff830a6a31562272079c6f207a93f26289bb7e1197621f08a60ef4693767447(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be576d692a793056ac7f58e96055a43a71d0888290ffddbbb867f24ec8bdfb4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868203fa3f735f3353f27dcf04a97b62f8c41c59f44e4ba511c7601db06762e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2935e3a6747debbd5d074dc5be50aa2fa158a0748ba1cb353f732999559b476a(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6be9f160622b52a2d10bb8d7ee7f70b33551dd8187cbd4648bbd84ed201505(
    *,
    prefix_type: builtins.str,
    prefix_format: typing.Optional[builtins.str] = None,
    prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f7f8085663b70e3383ab5bcfe623952cb50f7a7338b0f5032658adbf17bcde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd608f75732ec7cfcb06554cd3dd2ae61e34095574c1fbf624b3559b823d863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5449d873aafd385c1b30e4114e810fd72bec789db7c0f72c40b96eeb4e31b509(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8949cae58d40d669dd4403f4fa0cbf8885ae8019bb5c299202b3ff203d3abf21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f53bd0b34b52edee4a6e083a147d67dd62655aa2de64c7363658e26710f50d(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3330e45e9f4bf7145a5d3f075cd74465c5dae086ac2d0dd3fc65e21bf468ed(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261e8dedeb625de4a7f8c9edbd03040b5b82717862a2d504dd0e52c789300c55(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5889e06b9dbb7ea7a85c8ffd868cf5c7f5a7c7ecee0e66aef22a6fa37ee579f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d982cfe4ab296bf9b5087ea15b81f5acb204709dd29da73ec52d070d524ff459(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c5da36391ac58891069edfa3563a3c7469cec4384ec9a6b665210ca925c278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88054266769af4a594ad766d3f141a80b07dfa2433883c0b51096f882c4f7ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f65af162ea2bc612895b9f01cfcba3db8785b51af5c9ca402d76a3eb00d570(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d4c8c437e95f6925370417381a4ccb0f8d46162ec98d6ad96605deb5803576(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a75def861f5ad9916a317c8c849c9819470779af34829fd9acaee2109512b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518ae2b79fccbdde1eee14caf153cde10485d63fbe9e348e19cb9dd69c5a6682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62748052e66fe6e2e5bc1546b884f5801586b9d04bf95a449452c54eb4c185d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac73b7867e49b8d707112b97039fb5372d4eb84a38007ff5ea6c08b96303d4c(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801ac70bd423b21e0f8f91d2542016691245a9dcc96b551cd55cb931ed435bdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab60b6ab04559a2fbd2a4f7e507a239edef3e3dea54d2dbb3b20d9872bc6a0f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363bd796ce40e68b4240dd266b60f5ff8e70b87c42507536afbd624dc031dda2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2473c70cac2260f015fe576d40ca08fffd91301393af9873862879b65f09151(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2086e7a7d6bf5d428e29d2962011dfb6cabe40d98b8ca49c24b5dee1b103686(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac49f1270041c65a25b7c7e8e8a16c3008d25395dc635998e7a3b54208445d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76ed323262d42a1a30603ae4a1be3b838e19f1f7e0e7550a900efc260ed52ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c59fd6044f7e23792df9d760383c72b248df64eb17318594c7ba7884837d5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872f3583e1a9390f3cb9f213ec0b21991f55b6d6daa350f42a6303284491fcde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0c979c5c302abc290d95310a02fd4a000a0691188c743364d6e82bef2f456c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d6cd47e978875353713151e0239bf96f83b8b150e7019d9b148ebf5eaa7395(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447d833232d6580e8b738754fbca19b62530bdac2f2451543b0da43e12e37d63(
    *,
    glue_data_catalog: typing.Optional[typing.Union[AppflowFlowMetadataCatalogConfigGlueDataCatalog, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9977c4cee39bcbfb4daee0d6720652e133c7969de3d8d4efbcb9873e70a5b1(
    *,
    database_name: builtins.str,
    role_arn: builtins.str,
    table_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024c53ee79c5e464bb9521d09c0c3022f5dcc871454876ee3f17de65b58f9648(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25534f59a9c09364cb6b52dbe048193e1d15a17a9c049b058f3f2f9adc3fe0f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265dbc3efebc9dafaa1d46ba9dff85f7397f0a8ebf5755f08518d0fc6a2ecb29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fbc64f11e49f765c1860f9b4a6570f1be06afbd66b07158494354773cfc773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643630ba88c184d6a298f6b6b2fc309b1b2dfd962d8142e07b4cc9d7149bdfc9(
    value: typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f804019d800ba279dc9a86b8d82db0890a8a25fc0ed2d9e5a38d683703a812(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf51b22be105dac6861374d2234decd001e71a6fa854f52fd43ff9309d33d16(
    value: typing.Optional[AppflowFlowMetadataCatalogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf66e0a94a16c07fc4f9753d98d3c8bee2a3abf4d7640f13b7c335a772fe0f1e(
    *,
    connector_type: builtins.str,
    source_connector_properties: typing.Union[AppflowFlowSourceFlowConfigSourceConnectorProperties, typing.Dict[builtins.str, typing.Any]],
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
    incremental_pull_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigIncrementalPullConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847cdfe0511582182fcf539c1ed0e0ab8751c6905b71679599bbd9b545466727(
    *,
    datetime_type_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0898c6e067b56cc5dad4a6a8ee5a7d5518d932da03f86ae0511cc3449e18dc70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b129898eaeff5124e44969ad521de79f993acd0838b92e4d2fe0b1eb84ae0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6770adda1677b99cd207d35f8198e027ec933ffed029b757b6de52c62198b8d(
    value: typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff50d36b38cbd9e8ad32276c9ae7bceeaa9be63a34a5f884a49a4f0251275030(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb35b38e489c862e8c5151317c7d662630a567572e512e8939b80cf673308111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44465f81e02c9790a23f55e7107d0a0d465171d9b6cb312267f24f6fa35562ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3fd6c8c8187781b71c968c63c502e0a8e421f825a4e9642c4f3372f1ce9b32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc2ccdc02a2efab7407673ed01474e7ae4c508c1a14e121f58aa9118f000c53(
    value: typing.Optional[AppflowFlowSourceFlowConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e717f8dc78d87a1aef06090bfeea786aa4f2c1669279a42d1494d95c3b43a4bc(
    *,
    amplitude: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_connector: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    dynatrace: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
    google_analytics: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    infor_nexus: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    singular: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack, typing.Dict[builtins.str, typing.Any]]] = None,
    trendmicro: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
    veeva: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3ac80550cdaef3a884598d7fb6051065936a9cb60bef1469b88bcd30b15eeb(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba12285f05350039637cb6a65105fb8c5afff64299edaa3f071fc858f5da7ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca4589b727be2bd49e67fa67564cb22d9d8d548ff49d89ab4d6977c2401c0fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7713b66c07ebc03a2ffa9ec71965c85cc43420ffb958ab1e7fa134d0563e858e(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35506281b6e355855f9b5edb7efc9ccc9bde03d4e99512a6ae5d20bed840e8dd(
    *,
    entity_name: builtins.str,
    custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39659cc203275494c21e7538a41afe07b320fb31e9dd0cd1cf4ea5c3c30ebe00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab6e8588355853ae6169104e056ce84b18e7c67ac6d466f2b2f8aca455e6dec(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30ef72c1f5ff19c9cbf4a10176b5cdfd188a3dd39c345b1dfb99c5ceb89a97c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab37b4105bd743c59c41df991cd62d6ecc9c8da2993025927bca8e8e5e1d939(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c182fa6b0a84310cd0ff83fe4cb8dc061e9fe3c5597f7fe2a06d09f051f0e86(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb39ce3f214e960a78b97c5943b72f9403555f729a06be5ab2c801e0b748a9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6015b1ea6fa87a687f28e89516a3728aef2782574a8a2f7000611620d5eb76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653c832316f5fffa5b0bbb68b0e587229db90989fdcb1acee6c5a1a5abebac91(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b715ca4a794fb5ea5434f04f8aa5043a493b724e49012668067bed0abb2fe68(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028ad66d343e3f4cf9ef5fbf99086b703e749c5fbfa42f3563663c646797d0d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab166048f053826a7a651c96a2a45d9790ea11f678f01ecac04ea8ead5bbd040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f85b0e9bca76879ec7f83462c51028b65ccc97bbfe274df03d3597162b872dd(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74e857b7b44cf9797ef1afea43d6262634471fd9512ec7d99a57381dda71453(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aa2f87c347f0f4a41a2409360876c2997c054784c4c7ec746cea0cfb3d13ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af928fc3dcbdb52671345bc3e8ac79e6e17cac387bf71f7885dc6fa115b83692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2c09c97de5843fce2f2c98b0ba0eecef9db5b88f96f4d70d2cbe720ed239ec(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd1f64603fce6964321e4c2fa3ef508be2afef22daf31def9ad51c6bcf87aa5(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9184354d046ec5afb65f35a69d93fda0e03b779b5b0992141f4ce5a3213e6260(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4782cd71d5ac10565925efb59768c8758e55a790a9b361f48ccf59817f604c11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714273349e990e6293c0071eb08bb4a3fdab92d100a2d7c9e00b9089cf33fad3(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e15841d46e41243d71c2144b715dd9712adbe3bd64117cfa29a113041d2a69(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed3fb2317ef289d3f46b9812a8ec2ab484c259b44f25a0cbaca5bee2d32d9f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2788ff5266b04e5127322be590ec0a9e56aed3be61641811045d5cd3793f47c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa08c9dbdde463e85b732164084cbeb4c53ca12e8f0cd679481ca59c6d26821(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d65e98092c888e5726613c3fa6dc16d99142037dc0aa85de0ea32b7aab19b52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593554ac43278ee390230a4247c3c01c51e0548a30a2265aa1fcba73a80f27fd(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1960554cfccbfd49b0a7d416962b3c8e47204ef287de1e06ecfa15c38c724a2(
    *,
    bucket_name: builtins.str,
    bucket_prefix: builtins.str,
    s3_input_format_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35682b3128dc6450c88ba32e0cf1dd195941ecad84337892cc934107a8ebb2c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05e746e8239ed240326f3d6b230c9f7269246e9ecdd603f49599dbc3fa49b7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1531c64b9164353a5ae29e94c0e2734136e514af2be81137ccebda9bcb3a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed413489c5622deb2bb70cdad576b08666a34d35d269479c9f1cee3bd56b0142(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4b125128ce4c1396e1c7b1995ab13916fcd9b008753752a5579f9d0e2e0d3c(
    *,
    s3_input_file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41bd556b96d1b866c979f8b51e4bb02a920f0d4d1a277370f8cd302190231875(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468965409be00b2130e295765c3c09db1c34f4a25bb4ced113e16d116ba2dd14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0edaa07e9c5d5fc5a16a9938dbfc873d447be37fd8131098712fad3d65a8f0d(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3af5da59677baec1b66bc364d4ec3887aa003330e421225eb55795d7c76d6b9(
    *,
    object: builtins.str,
    data_transfer_api: typing.Optional[builtins.str] = None,
    enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_deleted_records: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebaf330df7fe47d75bfd037e1c69858839ce5f14e6a3cf8de614dd6c7a477efe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d848b74d83dcac6945f943441abd3ba6cd19ead31c8c765f4156e8025b50d529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21dc5e292d236956d5fed45d6454ea4fb2846271eda4e9356bc50da729385a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa72154db1cf08499a3d20f421c3393a03893cac6afd2af4205c40cf7105bb9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7c7d94ee9238d71d138d5c82ef480f72d915bb308a1c8ea74d5989b2996160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482425d76fd1f1a5167f37be2d1a328ef7cd7b770b5793c87bbbd1dd5823f0b2(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d14d224d5f75f5ce9e229d805b50a0aaa87bbd2c6ab8ca17e8f749ce3a66ca(
    *,
    object_path: builtins.str,
    pagination_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelism_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ddee1e8647f81b76f9a71710cbb2e3495f29f274498cadcf3ce850cbb657c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c934f3e720ef613a2d8948eccdd4c1d8d2560814e60872bd0b9d7e252ed845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e051fca70e67537de17190b7697231faa98d6a51a3ed27266a407ec557bcb62a(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8f54d0a959bc5efd5a0f7aa88cef358b4c8a6baa297af23dcab36c33a1875c(
    *,
    max_page_size: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e914d4290b889c518216c9d206f3d73c043fd7885617d262288a360c8abfaf59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc7a87a215d50678dea8d26dee324bde4c25b227b40ea57a8e5cb21f7b39a8d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2c0c5ff15cdeb761c294b6604cdb74938b78605950dd7594961f1979ed6d12(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520a721409d6c1d62a67728a763d0dabc4ff533f2fe27d09885219bb7f737322(
    *,
    max_page_size: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c4373e592c3707d1db73804ef9a57859601aa670f12bea026e33f2b6bfc6f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8d453bc71fb4fa5f13661fd10ba5ee4776a43bebe6d1edb80663916a95f6b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ebf53ce49b40cf3a17e2757cf7f7058b5a4ccf41736b17d97d3c5f513f9cad(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c59dabc229d2d9f7a92d6ba538f24c68f2b902ef131480f0ed09a41f488230(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297aee73df4d7790e73046e1ba22cc573aca53fff536e5fffe4c1ce6d0df2e10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966ff77c09a8a17d3b0f66ccbf7e5913d82db8369f95b323c50e1e1ea110c7b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f019093917f345e0d6aa7cac83bab9bb99f6b1a73a35b794e208164e8e28c27e(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd26348b3548506ec1f29ecf149b91aa8fa53bc9160213a748dc6a05bc17d796(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba9209a934452ee06ae5df3de4275c652afc5e40821755002d23f84ba5f945c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72efa7a4f8899534c9e3610e6f095bed563ff712d3c7ff55366d5accf5c2d8a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6793919802a4944d38f92c4d698100dd578a321837b42ff55945f9bb1e5bea6(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11389da639b58d72225b21093edb5e2549d426d59b8bac51d5676fadbc19827c(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3a11fd19c77da727fe680d669db11db264a14a77649b20b4ea929925d20d73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b1ad39f7ddf87dd3864b821f7a668362494b73f9a8a650e354ae9bc5c04b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db30b262f1b34db6236ec4123ae07f16a77dfad1d60c9f3fb3e63e515c8e8ef(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640b1aab906fbd87b7c5131a22e9d8dc4f96832fccef6f5678718b26d718b254(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88eca2a61192c89c75ba98e8f2ab71bb645651e8354ffe3203fcce686529c22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8cd5e41093bb8b123671c52e7c271fe8ef848eece9f3306158a696638b1925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5a499d05dc04cfa4b84b73faf81781bd422c8f68b96a9fd60ef29684ae09c5(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f290a87dc94b9e789dfb64d3018514fa5527cc5e5bcb21ddc02feed930806d2(
    *,
    object: builtins.str,
    document_type: typing.Optional[builtins.str] = None,
    include_all_versions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_renditions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_source_files: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534b396aedf47ed1025ce7d9ca8af1d1859a552a9abd94745bd157a07f95422a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a88dcc3fb3c42436552fbeba76585467cf533e87d924881f631d00d4d5b9c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211f08f497e93b8486f6b7b87b0c4a2a5240125258fcd73d234adea1f16915e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c02e66315bff96626e428d718bd47981df98f97b68837e197d44eeca1c9493(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36173f11f20b57ae047fb532ed70db42181bb5a728533be1b6c900625897a3fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1779609377bd87b250e61d8a5089946dae4a09a1ef654870da7cb54aa6223528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1016d297bb7627a64b55e9214b78f0e5bf5779d8bcb0b3b78759d37fc00a52(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5108e53872e2405281c5631623930b81b6b2436e909c5e0a9315f8ec004f8e7(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e9bbad0bf8ff9b4a056011d6ec7c7b99fd7fa566e94ee51f18bca17914c5d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a21999e7b76c12a252b637e28742c47e9fa0dea6177cc33816e924e1d8c6fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b3e79a2945e0bde491139eb5be8d35ac44305a5e6e20d696f16582951bbb66(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac785ffe16f428e8bae58cf17f09e15e658f24662be2fa36c7d9ecbbe7a77bf(
    *,
    task_type: builtins.str,
    connector_operator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTaskConnectorOperator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_field: typing.Optional[builtins.str] = None,
    source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdec0a5501b36e42b0ae642737c41cc4c3541208b85192ef7aa094376cc2e5bc(
    *,
    amplitude: typing.Optional[builtins.str] = None,
    custom_connector: typing.Optional[builtins.str] = None,
    datadog: typing.Optional[builtins.str] = None,
    dynatrace: typing.Optional[builtins.str] = None,
    google_analytics: typing.Optional[builtins.str] = None,
    infor_nexus: typing.Optional[builtins.str] = None,
    marketo: typing.Optional[builtins.str] = None,
    s3: typing.Optional[builtins.str] = None,
    salesforce: typing.Optional[builtins.str] = None,
    sapo_data: typing.Optional[builtins.str] = None,
    service_now: typing.Optional[builtins.str] = None,
    singular: typing.Optional[builtins.str] = None,
    slack: typing.Optional[builtins.str] = None,
    trendmicro: typing.Optional[builtins.str] = None,
    veeva: typing.Optional[builtins.str] = None,
    zendesk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296a6cdbe2b29c0308e5ff4a055ca69cfe6a34aaf0e2110d82c04bfaa741625d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c1e8cb60d1c280c42e6b27a2dfa747113a43d36b5dbbf6a11bbeb2a5ea25aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47661404a26e19b0031614e47cd835b68a8d4173ef46504786834535be30ad43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6528151debc9f9095e9da3e2ae9a000addeac1c73f6d865eb036132cd68a2750(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86a3b57c559847fa814fac2e13a433fc5cf902ac4c02b27cb4b52af5743cba3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d8a0f366e76c4aa07ca2afdc9110f177c893be399e59bbe584d22062524092(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bce4094c9c9f437c27b0076be1c3515e2911e47c551d835fecad43351f8028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f227f59a621ae59137ac87158fbb6966cdd0f2baabfa8e8a88b5d0d543d9c3ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3381ce2151e60132de896fa3c134f50830cbbe49a518128e0678dbfa22f6f82d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91024379644d639316198ae16eebf6c98cf618daabed27e16df67b11ba1f9abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c0cc183f2ac1775cd82b523ec1c35f9fd4f4c57bf4bd8bc2f018211be8741f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2a948caa4fc25e86404885ecc157dc716a20f5cff9b388093c188273f04586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23e7fd0509a633878e87d4e1a0deda29a7ad4ae76d093c7beb8c8b4dea41783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa99c322115756f8e2c2ab1184a04f9dae98653a0073fbbe9dd2a6e97dddc07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cbf7bf3f8cb158cd368d4d130d098a9bd417f63397c4e1133bef7f287c19b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2226382e080b6bb29f166fa3f6e1080b298f2ab8b32249f82430ccaf0f2419(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1170782ffb67de367faa668d14bbcad6bc4ec9ff1f0577f894998573ffc0e16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e149ef723cca62ca270f01820eecfa021c50bd7c377b69535d3e9a665f54c1a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32abf8ceddab3a238081ed61372d1af020446ffe528766953a79e322b2179219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7158a6c4fd3d90269de25a6bca4dd4ee16d0a088bfba7f70d000f193d6ee09e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76e7124c811a6dc7d2d5a03f3ec1c64ddf52e6159be52d929bb1d25ddf590dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fedec54732a09ba1f8c144a4b4517e5cdcef99a8ba06f656d1cd79a1dc4151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c561e51695fdf559fdab0d77d1bc517e1b7ccf28d835aef5497946a2c561321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df45efbc88cbd368953cbd7d4f7b85180082c0ea77320e3e985d32f7c576c52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdda4e71ea08feb58b1c73ddfb02a2a7b3ed10f0b7d9a4a937b79e72975b6d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28df48823d645a4e9417962e5e47440cc1ef0fc3277c9977e006684f2c26137d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0346625da2d68e5bc374589a9d416f933a79e8931b5df63e7dc0fd1fbb2fd29a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55ddbcda17eecf0b3753f2c0daf07ac44fec9ac68b3cff1c65d5c8b6ecda61b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241c79bab0c4980e32928316f4c4f26eb196933e3a037167cc1cfd72b74d83a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e069bc0ee24612e2c9870815ae34e1245997175d9e5d9f4a2e4310cb2e67ede(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14383d6c71d12d36dfa7345104e58af54041c924be78cb0d0ca307ec764002b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e1d7c5114777a454f4dfe6c12f6fd1c8c22f1c1855e76818c6a9ef31bd303f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTaskConnectorOperator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00807a099b2a0e356c5811891d7a88bc5208dea5784b9d18301b96d32696ae44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa38934794db6a7a91ce131d9926dc710c46c46ede0bcb7fe9f2e861ef9e637(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4192c67e3f5edcf166741432f7f92f537b45ea00dc319274561bfecd050755d8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc36bfd7a9738e35247ab25862cdf947a17a949959b4c93484457e8bcc454db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fe2ddecd9a0152ce68e1fff21ff175b5f974aa974c8e11ed97287eccd7172d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df22188bd1fcbf9414eb4896e0eb6bfc62ed93a9fe0911b7c7794e6ba2b767f(
    *,
    trigger_type: builtins.str,
    trigger_properties: typing.Optional[typing.Union[AppflowFlowTriggerConfigTriggerProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afa3bebc88af9f3e98b659e3d6efab07557e36778bb139a5467cb3e6595579a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294983ecaca1fc52c04301b33f59acd7fcd61761fb092f16060f779422ea5bac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7589dd285ac1137d5214eb3054a9711718613ba0f8b279e7cbdb074dcef3fe8d(
    value: typing.Optional[AppflowFlowTriggerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508662c09014ef3cabe6d56a423e9c4f47ae926cc25b8549ec9a118d3b6ef254(
    *,
    scheduled: typing.Optional[typing.Union[AppflowFlowTriggerConfigTriggerPropertiesScheduled, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b93918121ff8624a4c364cf3cf710844bb6985ab8d8aaf5594375243ceb106(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bea63811f086289a01272fdef6a3987ea5f51e58f2e1eb023d6d86f028eb11(
    value: typing.Optional[AppflowFlowTriggerConfigTriggerProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fc03d1d6f52547e9f24aa67a74c6ae40b1902a1d6fb73ad51b82c88a85acc8(
    *,
    schedule_expression: builtins.str,
    data_pull_mode: typing.Optional[builtins.str] = None,
    first_execution_from: typing.Optional[builtins.str] = None,
    schedule_end_time: typing.Optional[builtins.str] = None,
    schedule_offset: typing.Optional[jsii.Number] = None,
    schedule_start_time: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42bebb22e77e09e865ee505af1ced75970a02b5a0add7402247923f8ac227ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3fbd43f23771b96f22b9d02ed02b67cc1f812ea71c011a198b33513ca94d98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbeec3ed2615adb9323084ebaa71146302e9a2fd3d3fa4947266a267f8608074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1191a3767d3f00f3f8c444128b0a464e6a31d032bb3cb97a52a7151eadc418ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f82ab9fce08435b59f855e6c7f3839c9c069c609d06bc72d62b1b989758b89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0dedea7c121e0f8d3a2bab212df8f49a8e9155bdf32eefa8af8c31918a1808e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fc925c7873203a1cf872dcbc25e4bac2ba0bfd88f810d5218f3f5ea91abbdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcc82148b97bafc233050ba4ce62ea357bad1b94053082f3fd205f9f89ce582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45d06a9e2af347a05d2a443b4f9133d565c0f064bc9a354ec1b19c38d1ece81(
    value: typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled],
) -> None:
    """Type checking stubs"""
    pass
