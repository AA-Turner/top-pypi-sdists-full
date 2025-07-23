r'''
# `google_cloud_asset_folder_feed`

Refer to the Terraform Registry for docs: [`google_cloud_asset_folder_feed`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed).
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


class CloudAssetFolderFeed(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeed",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed google_cloud_asset_folder_feed}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        billing_project: builtins.str,
        feed_id: builtins.str,
        feed_output_config: typing.Union["CloudAssetFolderFeedFeedOutputConfig", typing.Dict[builtins.str, typing.Any]],
        folder: builtins.str,
        asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[typing.Union["CloudAssetFolderFeedCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudAssetFolderFeedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed google_cloud_asset_folder_feed} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param billing_project: The project whose identity will be used when sending messages to the destination pubsub topic. It also specifies the project for API enablement check, quota, and billing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#billing_project CloudAssetFolderFeed#billing_project}
        :param feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#feed_id CloudAssetFolderFeed#feed_id}
        :param feed_output_config: feed_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#feed_output_config CloudAssetFolderFeed#feed_output_config}
        :param folder: The folder this feed should be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#folder CloudAssetFolderFeed#folder}
        :param asset_names: A list of the full names of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1. See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#asset_names CloudAssetFolderFeed#asset_names}
        :param asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: "compute.googleapis.com/Disk" See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all supported asset types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#asset_types CloudAssetFolderFeed#asset_types}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#condition CloudAssetFolderFeed#condition}
        :param content_type: Asset content type. If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#content_type CloudAssetFolderFeed#content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#id CloudAssetFolderFeed#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#timeouts CloudAssetFolderFeed#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381706f5f1d4c1a693b228f8dc7885d5903f252e5922def915b1a576f403de60)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudAssetFolderFeedConfig(
            billing_project=billing_project,
            feed_id=feed_id,
            feed_output_config=feed_output_config,
            folder=folder,
            asset_names=asset_names,
            asset_types=asset_types,
            condition=condition,
            content_type=content_type,
            id=id,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a CloudAssetFolderFeed resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudAssetFolderFeed to import.
        :param import_from_id: The id of the existing CloudAssetFolderFeed that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudAssetFolderFeed to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f99f8ce4917344749452acc1ff765d6f9debdeb8f86c112af4b56a63fb8836)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#expression CloudAssetFolderFeed#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#description CloudAssetFolderFeed#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#location CloudAssetFolderFeed#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#title CloudAssetFolderFeed#title}
        '''
        value = CloudAssetFolderFeedCondition(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putFeedOutputConfig")
    def put_feed_output_config(
        self,
        *,
        pubsub_destination: typing.Union["CloudAssetFolderFeedFeedOutputConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#pubsub_destination CloudAssetFolderFeed#pubsub_destination}
        '''
        value = CloudAssetFolderFeedFeedOutputConfig(
            pubsub_destination=pubsub_destination
        )

        return typing.cast(None, jsii.invoke(self, "putFeedOutputConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#create CloudAssetFolderFeed#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#delete CloudAssetFolderFeed#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#update CloudAssetFolderFeed#update}.
        '''
        value = CloudAssetFolderFeedTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAssetNames")
    def reset_asset_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetNames", []))

    @jsii.member(jsii_name="resetAssetTypes")
    def reset_asset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetTypes", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="condition")
    def condition(self) -> "CloudAssetFolderFeedConditionOutputReference":
        return typing.cast("CloudAssetFolderFeedConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="feedOutputConfig")
    def feed_output_config(
        self,
    ) -> "CloudAssetFolderFeedFeedOutputConfigOutputReference":
        return typing.cast("CloudAssetFolderFeedFeedOutputConfigOutputReference", jsii.get(self, "feedOutputConfig"))

    @builtins.property
    @jsii.member(jsii_name="folderId")
    def folder_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folderId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudAssetFolderFeedTimeoutsOutputReference":
        return typing.cast("CloudAssetFolderFeedTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="assetNamesInput")
    def asset_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "assetNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="assetTypesInput")
    def asset_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "assetTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="billingProjectInput")
    def billing_project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingProjectInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional["CloudAssetFolderFeedCondition"]:
        return typing.cast(typing.Optional["CloudAssetFolderFeedCondition"], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="feedIdInput")
    def feed_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "feedIdInput"))

    @builtins.property
    @jsii.member(jsii_name="feedOutputConfigInput")
    def feed_output_config_input(
        self,
    ) -> typing.Optional["CloudAssetFolderFeedFeedOutputConfig"]:
        return typing.cast(typing.Optional["CloudAssetFolderFeedFeedOutputConfig"], jsii.get(self, "feedOutputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="folderInput")
    def folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudAssetFolderFeedTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudAssetFolderFeedTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="assetNames")
    def asset_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assetNames"))

    @asset_names.setter
    def asset_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607c0c4e52f15e2010c2cc61a18aacb479222aeae1a64c9dd0cc47f0c7eb3788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assetTypes")
    def asset_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assetTypes"))

    @asset_types.setter
    def asset_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cd276a94b36b2458c40cc021c362bfdb98a5220cb51338b9939449d3f7772a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingProject")
    def billing_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingProject"))

    @billing_project.setter
    def billing_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cfcccf3f26b8acffb761337e95c1c7cebb1f949663cc642ecd28a3439c1131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a6b475637561cf4f3ee943ad8c37d9d3c8ae54e893279b0d6560334e9faf23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="feedId")
    def feed_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "feedId"))

    @feed_id.setter
    def feed_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b5a7b8b5461711e8e994bd8e375a7610e37c5af3dc9812520bdaa8a871b27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feedId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566d8e4085f98b24798836956ef4fa0ab224d3cf2e5ede2049b793b923632624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e434095e547513654f9c6c7650736e2bac2968828df8e955cfe9879ac633781b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class CloudAssetFolderFeedCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#expression CloudAssetFolderFeed#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#description CloudAssetFolderFeed#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#location CloudAssetFolderFeed#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#title CloudAssetFolderFeed#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff79577d278e79cc9d5fcdc41cb868c2616bd23347cfad5d4719056210c0ad1)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#expression CloudAssetFolderFeed#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the expression,
        e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#description CloudAssetFolderFeed#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#location CloudAssetFolderFeed#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#title CloudAssetFolderFeed#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetFolderFeedCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetFolderFeedConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0acaeb2b92009bd3f7dae918c01456b0c000f3fa3b78b4d38bb489f9c65cc21a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76fe94e12338c15d4eaaa3a59bf113924ede5ec62cec84d62c21ce7f0b15dccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d0a7470aed1f2644d1241e5b10d5625bf8663689dfa1f10ee5ce3e2186d415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f589a54bab10a06e2bc0d7887b24e07cc88aa132f9d518d7a9d90289187aa202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555baad498e4b1172d2be941d70c7f0084ab9fcfa9bb7f8d8721e4083a33496c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAssetFolderFeedCondition]:
        return typing.cast(typing.Optional[CloudAssetFolderFeedCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAssetFolderFeedCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba0dcaba4c866fab20ed6ad59d82168021914baf54c2d4ac61c4b565ed42388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "billing_project": "billingProject",
        "feed_id": "feedId",
        "feed_output_config": "feedOutputConfig",
        "folder": "folder",
        "asset_names": "assetNames",
        "asset_types": "assetTypes",
        "condition": "condition",
        "content_type": "contentType",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class CloudAssetFolderFeedConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        billing_project: builtins.str,
        feed_id: builtins.str,
        feed_output_config: typing.Union["CloudAssetFolderFeedFeedOutputConfig", typing.Dict[builtins.str, typing.Any]],
        folder: builtins.str,
        asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[typing.Union[CloudAssetFolderFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudAssetFolderFeedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param billing_project: The project whose identity will be used when sending messages to the destination pubsub topic. It also specifies the project for API enablement check, quota, and billing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#billing_project CloudAssetFolderFeed#billing_project}
        :param feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#feed_id CloudAssetFolderFeed#feed_id}
        :param feed_output_config: feed_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#feed_output_config CloudAssetFolderFeed#feed_output_config}
        :param folder: The folder this feed should be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#folder CloudAssetFolderFeed#folder}
        :param asset_names: A list of the full names of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1. See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#asset_names CloudAssetFolderFeed#asset_names}
        :param asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: "compute.googleapis.com/Disk" See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all supported asset types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#asset_types CloudAssetFolderFeed#asset_types}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#condition CloudAssetFolderFeed#condition}
        :param content_type: Asset content type. If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#content_type CloudAssetFolderFeed#content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#id CloudAssetFolderFeed#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#timeouts CloudAssetFolderFeed#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(feed_output_config, dict):
            feed_output_config = CloudAssetFolderFeedFeedOutputConfig(**feed_output_config)
        if isinstance(condition, dict):
            condition = CloudAssetFolderFeedCondition(**condition)
        if isinstance(timeouts, dict):
            timeouts = CloudAssetFolderFeedTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc13c3a95bb9cdf2537b678617e70a75cc9ea13afcdaefd5f83b9e397dd0c6e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument billing_project", value=billing_project, expected_type=type_hints["billing_project"])
            check_type(argname="argument feed_id", value=feed_id, expected_type=type_hints["feed_id"])
            check_type(argname="argument feed_output_config", value=feed_output_config, expected_type=type_hints["feed_output_config"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument asset_names", value=asset_names, expected_type=type_hints["asset_names"])
            check_type(argname="argument asset_types", value=asset_types, expected_type=type_hints["asset_types"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "billing_project": billing_project,
            "feed_id": feed_id,
            "feed_output_config": feed_output_config,
            "folder": folder,
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
        if asset_names is not None:
            self._values["asset_names"] = asset_names
        if asset_types is not None:
            self._values["asset_types"] = asset_types
        if condition is not None:
            self._values["condition"] = condition
        if content_type is not None:
            self._values["content_type"] = content_type
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def billing_project(self) -> builtins.str:
        '''The project whose identity will be used when sending messages to the destination pubsub topic.

        It also specifies the project for API
        enablement check, quota, and billing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#billing_project CloudAssetFolderFeed#billing_project}
        '''
        result = self._values.get("billing_project")
        assert result is not None, "Required property 'billing_project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feed_id(self) -> builtins.str:
        '''This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#feed_id CloudAssetFolderFeed#feed_id}
        '''
        result = self._values.get("feed_id")
        assert result is not None, "Required property 'feed_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feed_output_config(self) -> "CloudAssetFolderFeedFeedOutputConfig":
        '''feed_output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#feed_output_config CloudAssetFolderFeed#feed_output_config}
        '''
        result = self._values.get("feed_output_config")
        assert result is not None, "Required property 'feed_output_config' is missing"
        return typing.cast("CloudAssetFolderFeedFeedOutputConfig", result)

    @builtins.property
    def folder(self) -> builtins.str:
        '''The folder this feed should be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#folder CloudAssetFolderFeed#folder}
        '''
        result = self._values.get("folder")
        assert result is not None, "Required property 'folder' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the full names of the assets to receive updates.

        You must specify either or both of
        assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
        exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
        See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#asset_names CloudAssetFolderFeed#asset_names}
        '''
        result = self._values.get("asset_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def asset_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of types of the assets to receive updates.

        You must specify either or both of assetNames
        and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
        the feed. For example: "compute.googleapis.com/Disk"
        See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
        supported asset types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#asset_types CloudAssetFolderFeed#asset_types}
        '''
        result = self._values.get("asset_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def condition(self) -> typing.Optional[CloudAssetFolderFeedCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#condition CloudAssetFolderFeed#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[CloudAssetFolderFeedCondition], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Asset content type.

        If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#content_type CloudAssetFolderFeed#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#id CloudAssetFolderFeed#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudAssetFolderFeedTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#timeouts CloudAssetFolderFeed#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudAssetFolderFeedTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetFolderFeedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedFeedOutputConfig",
    jsii_struct_bases=[],
    name_mapping={"pubsub_destination": "pubsubDestination"},
)
class CloudAssetFolderFeedFeedOutputConfig:
    def __init__(
        self,
        *,
        pubsub_destination: typing.Union["CloudAssetFolderFeedFeedOutputConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#pubsub_destination CloudAssetFolderFeed#pubsub_destination}
        '''
        if isinstance(pubsub_destination, dict):
            pubsub_destination = CloudAssetFolderFeedFeedOutputConfigPubsubDestination(**pubsub_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ded8dfa7707a4becde2e44b1790aaff26d293ef202acf69ef6e489c547fde1)
            check_type(argname="argument pubsub_destination", value=pubsub_destination, expected_type=type_hints["pubsub_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_destination": pubsub_destination,
        }

    @builtins.property
    def pubsub_destination(
        self,
    ) -> "CloudAssetFolderFeedFeedOutputConfigPubsubDestination":
        '''pubsub_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#pubsub_destination CloudAssetFolderFeed#pubsub_destination}
        '''
        result = self._values.get("pubsub_destination")
        assert result is not None, "Required property 'pubsub_destination' is missing"
        return typing.cast("CloudAssetFolderFeedFeedOutputConfigPubsubDestination", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetFolderFeedFeedOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetFolderFeedFeedOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedFeedOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4741eede974c8789180a8b2f2351df773e573f4c28d91858c2f3a4f216727b2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPubsubDestination")
    def put_pubsub_destination(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Destination on Cloud Pubsub topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#topic CloudAssetFolderFeed#topic}
        '''
        value = CloudAssetFolderFeedFeedOutputConfigPubsubDestination(topic=topic)

        return typing.cast(None, jsii.invoke(self, "putPubsubDestination", [value]))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestination")
    def pubsub_destination(
        self,
    ) -> "CloudAssetFolderFeedFeedOutputConfigPubsubDestinationOutputReference":
        return typing.cast("CloudAssetFolderFeedFeedOutputConfigPubsubDestinationOutputReference", jsii.get(self, "pubsubDestination"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestinationInput")
    def pubsub_destination_input(
        self,
    ) -> typing.Optional["CloudAssetFolderFeedFeedOutputConfigPubsubDestination"]:
        return typing.cast(typing.Optional["CloudAssetFolderFeedFeedOutputConfigPubsubDestination"], jsii.get(self, "pubsubDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAssetFolderFeedFeedOutputConfig]:
        return typing.cast(typing.Optional[CloudAssetFolderFeedFeedOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAssetFolderFeedFeedOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c452a8515d914dbdcaf1aeefdc860cfc4cb288f38428eec85cea09fb894308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedFeedOutputConfigPubsubDestination",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class CloudAssetFolderFeedFeedOutputConfigPubsubDestination:
    def __init__(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Destination on Cloud Pubsub topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#topic CloudAssetFolderFeed#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f149cb072f9f08aced053a0cbfd837b83c2641313adb85ece07db365e83e3e70)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }

    @builtins.property
    def topic(self) -> builtins.str:
        '''Destination on Cloud Pubsub topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#topic CloudAssetFolderFeed#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetFolderFeedFeedOutputConfigPubsubDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetFolderFeedFeedOutputConfigPubsubDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedFeedOutputConfigPubsubDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd33b5000773a875ffd86c1803a561cd96f140ea137a84021fde91ca8e6e8fb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e79de6d3f7be7a50e5801276211e377d084593dd60b3d2a313fbc8e080c770b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudAssetFolderFeedFeedOutputConfigPubsubDestination]:
        return typing.cast(typing.Optional[CloudAssetFolderFeedFeedOutputConfigPubsubDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAssetFolderFeedFeedOutputConfigPubsubDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1fde28fe4c78e4ce45f534bc07626f48a5bca0ee617a295eca10d2dce816f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudAssetFolderFeedTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#create CloudAssetFolderFeed#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#delete CloudAssetFolderFeed#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#update CloudAssetFolderFeed#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b9d0823191ac1fd7cd78c20f86d03defc21cbeb897f188910db4e46c694c82)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#create CloudAssetFolderFeed#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#delete CloudAssetFolderFeed#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_folder_feed#update CloudAssetFolderFeed#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetFolderFeedTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetFolderFeedTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetFolderFeed.CloudAssetFolderFeedTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__583a635bb2f8fa7e8d114a32987cd29282ba8ad67f526eda1eb5b9a5494d5516)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b32dee5734e8942f9025614e6282cd55adbd52b796c99f4c7fd0ad6497a188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321b74a96514f7745d8207893104171ec9c0312cc8b4b17a9781bbf9798eb867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c31e15e2381b14bea87bc753249d186e782038a3b2baf5f733e84c6cb09f27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetFolderFeedTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetFolderFeedTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetFolderFeedTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203db2d8e60a7ea2df2eb94fff1a945a7d64613b9d972c3ff665a3ce532d4c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudAssetFolderFeed",
    "CloudAssetFolderFeedCondition",
    "CloudAssetFolderFeedConditionOutputReference",
    "CloudAssetFolderFeedConfig",
    "CloudAssetFolderFeedFeedOutputConfig",
    "CloudAssetFolderFeedFeedOutputConfigOutputReference",
    "CloudAssetFolderFeedFeedOutputConfigPubsubDestination",
    "CloudAssetFolderFeedFeedOutputConfigPubsubDestinationOutputReference",
    "CloudAssetFolderFeedTimeouts",
    "CloudAssetFolderFeedTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__381706f5f1d4c1a693b228f8dc7885d5903f252e5922def915b1a576f403de60(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    billing_project: builtins.str,
    feed_id: builtins.str,
    feed_output_config: typing.Union[CloudAssetFolderFeedFeedOutputConfig, typing.Dict[builtins.str, typing.Any]],
    folder: builtins.str,
    asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[typing.Union[CloudAssetFolderFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudAssetFolderFeedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a3f99f8ce4917344749452acc1ff765d6f9debdeb8f86c112af4b56a63fb8836(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607c0c4e52f15e2010c2cc61a18aacb479222aeae1a64c9dd0cc47f0c7eb3788(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cd276a94b36b2458c40cc021c362bfdb98a5220cb51338b9939449d3f7772a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cfcccf3f26b8acffb761337e95c1c7cebb1f949663cc642ecd28a3439c1131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a6b475637561cf4f3ee943ad8c37d9d3c8ae54e893279b0d6560334e9faf23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b5a7b8b5461711e8e994bd8e375a7610e37c5af3dc9812520bdaa8a871b27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566d8e4085f98b24798836956ef4fa0ab224d3cf2e5ede2049b793b923632624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e434095e547513654f9c6c7650736e2bac2968828df8e955cfe9879ac633781b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff79577d278e79cc9d5fcdc41cb868c2616bd23347cfad5d4719056210c0ad1(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acaeb2b92009bd3f7dae918c01456b0c000f3fa3b78b4d38bb489f9c65cc21a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fe94e12338c15d4eaaa3a59bf113924ede5ec62cec84d62c21ce7f0b15dccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d0a7470aed1f2644d1241e5b10d5625bf8663689dfa1f10ee5ce3e2186d415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f589a54bab10a06e2bc0d7887b24e07cc88aa132f9d518d7a9d90289187aa202(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555baad498e4b1172d2be941d70c7f0084ab9fcfa9bb7f8d8721e4083a33496c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba0dcaba4c866fab20ed6ad59d82168021914baf54c2d4ac61c4b565ed42388(
    value: typing.Optional[CloudAssetFolderFeedCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc13c3a95bb9cdf2537b678617e70a75cc9ea13afcdaefd5f83b9e397dd0c6e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    billing_project: builtins.str,
    feed_id: builtins.str,
    feed_output_config: typing.Union[CloudAssetFolderFeedFeedOutputConfig, typing.Dict[builtins.str, typing.Any]],
    folder: builtins.str,
    asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[typing.Union[CloudAssetFolderFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudAssetFolderFeedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ded8dfa7707a4becde2e44b1790aaff26d293ef202acf69ef6e489c547fde1(
    *,
    pubsub_destination: typing.Union[CloudAssetFolderFeedFeedOutputConfigPubsubDestination, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4741eede974c8789180a8b2f2351df773e573f4c28d91858c2f3a4f216727b2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c452a8515d914dbdcaf1aeefdc860cfc4cb288f38428eec85cea09fb894308(
    value: typing.Optional[CloudAssetFolderFeedFeedOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f149cb072f9f08aced053a0cbfd837b83c2641313adb85ece07db365e83e3e70(
    *,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd33b5000773a875ffd86c1803a561cd96f140ea137a84021fde91ca8e6e8fb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e79de6d3f7be7a50e5801276211e377d084593dd60b3d2a313fbc8e080c770b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1fde28fe4c78e4ce45f534bc07626f48a5bca0ee617a295eca10d2dce816f3(
    value: typing.Optional[CloudAssetFolderFeedFeedOutputConfigPubsubDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b9d0823191ac1fd7cd78c20f86d03defc21cbeb897f188910db4e46c694c82(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583a635bb2f8fa7e8d114a32987cd29282ba8ad67f526eda1eb5b9a5494d5516(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b32dee5734e8942f9025614e6282cd55adbd52b796c99f4c7fd0ad6497a188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321b74a96514f7745d8207893104171ec9c0312cc8b4b17a9781bbf9798eb867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c31e15e2381b14bea87bc753249d186e782038a3b2baf5f733e84c6cb09f27f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203db2d8e60a7ea2df2eb94fff1a945a7d64613b9d972c3ff665a3ce532d4c0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetFolderFeedTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
