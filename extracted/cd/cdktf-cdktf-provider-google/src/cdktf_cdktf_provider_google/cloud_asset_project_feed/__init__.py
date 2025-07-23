r'''
# `google_cloud_asset_project_feed`

Refer to the Terraform Registry for docs: [`google_cloud_asset_project_feed`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed).
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


class CloudAssetProjectFeed(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeed",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed google_cloud_asset_project_feed}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        feed_id: builtins.str,
        feed_output_config: typing.Union["CloudAssetProjectFeedFeedOutputConfig", typing.Dict[builtins.str, typing.Any]],
        asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        billing_project: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["CloudAssetProjectFeedCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudAssetProjectFeedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed google_cloud_asset_project_feed} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#feed_id CloudAssetProjectFeed#feed_id}
        :param feed_output_config: feed_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#feed_output_config CloudAssetProjectFeed#feed_output_config}
        :param asset_names: A list of the full names of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1. See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#asset_names CloudAssetProjectFeed#asset_names}
        :param asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: "compute.googleapis.com/Disk" See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all supported asset types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#asset_types CloudAssetProjectFeed#asset_types}
        :param billing_project: The project whose identity will be used when sending messages to the destination pubsub topic. It also specifies the project for API enablement check, quota, and billing. If not specified, the resource's project will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#billing_project CloudAssetProjectFeed#billing_project}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#condition CloudAssetProjectFeed#condition}
        :param content_type: Asset content type. If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#content_type CloudAssetProjectFeed#content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#id CloudAssetProjectFeed#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#project CloudAssetProjectFeed#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#timeouts CloudAssetProjectFeed#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed001b6f8b108ed2b10513fa594d34f53a35421b2a2c758d2a76d6d4cfeb2ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudAssetProjectFeedConfig(
            feed_id=feed_id,
            feed_output_config=feed_output_config,
            asset_names=asset_names,
            asset_types=asset_types,
            billing_project=billing_project,
            condition=condition,
            content_type=content_type,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a CloudAssetProjectFeed resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudAssetProjectFeed to import.
        :param import_from_id: The id of the existing CloudAssetProjectFeed that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudAssetProjectFeed to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915f4d17f61994b8c5751f7cdba0192cc5d996e866e368c541504c031566fd17)
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#expression CloudAssetProjectFeed#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#description CloudAssetProjectFeed#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#location CloudAssetProjectFeed#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#title CloudAssetProjectFeed#title}
        '''
        value = CloudAssetProjectFeedCondition(
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
        pubsub_destination: typing.Union["CloudAssetProjectFeedFeedOutputConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#pubsub_destination CloudAssetProjectFeed#pubsub_destination}
        '''
        value = CloudAssetProjectFeedFeedOutputConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#create CloudAssetProjectFeed#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#delete CloudAssetProjectFeed#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#update CloudAssetProjectFeed#update}.
        '''
        value = CloudAssetProjectFeedTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAssetNames")
    def reset_asset_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetNames", []))

    @jsii.member(jsii_name="resetAssetTypes")
    def reset_asset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetTypes", []))

    @jsii.member(jsii_name="resetBillingProject")
    def reset_billing_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingProject", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    def condition(self) -> "CloudAssetProjectFeedConditionOutputReference":
        return typing.cast("CloudAssetProjectFeedConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="feedOutputConfig")
    def feed_output_config(
        self,
    ) -> "CloudAssetProjectFeedFeedOutputConfigOutputReference":
        return typing.cast("CloudAssetProjectFeedFeedOutputConfigOutputReference", jsii.get(self, "feedOutputConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudAssetProjectFeedTimeoutsOutputReference":
        return typing.cast("CloudAssetProjectFeedTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def condition_input(self) -> typing.Optional["CloudAssetProjectFeedCondition"]:
        return typing.cast(typing.Optional["CloudAssetProjectFeedCondition"], jsii.get(self, "conditionInput"))

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
    ) -> typing.Optional["CloudAssetProjectFeedFeedOutputConfig"]:
        return typing.cast(typing.Optional["CloudAssetProjectFeedFeedOutputConfig"], jsii.get(self, "feedOutputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudAssetProjectFeedTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudAssetProjectFeedTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="assetNames")
    def asset_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assetNames"))

    @asset_names.setter
    def asset_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564d7cff33076fe44f8cbd0d294c2a406b6bccfdd85306703fc7fb31e7d45beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assetTypes")
    def asset_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assetTypes"))

    @asset_types.setter
    def asset_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c20a877db3db08d5177f31e03f17fc38c4a145cd5e38f04b1ed950a424b24ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingProject")
    def billing_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingProject"))

    @billing_project.setter
    def billing_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e14c20badc7c8d43d99d0fdff4b3b28df0fa10edd62b0a05537c90b32f6497c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16eb5dd002d259d0120c70700c73a70cc55cf0ad85910db9c65684e40011e6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="feedId")
    def feed_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "feedId"))

    @feed_id.setter
    def feed_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba7d65d86d051804efa55455db1e658e23fadb116ffec6befd7e2f32008c4fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feedId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c48ec4429a8efc397b102704353ca2bd6b9a05a3ade162e700a0df746c8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a255d6648fb84a51c31a8dae168deaeccfe74e95f2c4a80e9e56f05bf52d501f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class CloudAssetProjectFeedCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#expression CloudAssetProjectFeed#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#description CloudAssetProjectFeed#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#location CloudAssetProjectFeed#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#title CloudAssetProjectFeed#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc0bc5eeed116092c33c357051aab8dd34d4382263a9fc3242bdb0d71b2d777)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#expression CloudAssetProjectFeed#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the expression,
        e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#description CloudAssetProjectFeed#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#location CloudAssetProjectFeed#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#title CloudAssetProjectFeed#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetProjectFeedCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetProjectFeedConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f399a96b8692f54673d247439d4afc3809a5b09e726e65b97837b0590ca74e1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86c4ca3981cfc2df7f24a7865acf5b489f31bb2d6765e684266435d0f2c6311e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7876556c7da02144f844d5f6635e1c6fb2cb9915dab1f3b22114fea194498abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbacd94735c7cfab456a2f1e2d2e87f86103fef9d3befd57a5abc87535034c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4044d3a123ecdf5b5c911b8ea33049288956b8d955668b7f972ba8c7aa9aff6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAssetProjectFeedCondition]:
        return typing.cast(typing.Optional[CloudAssetProjectFeedCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAssetProjectFeedCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ef84c06b559798788b883e61a550691360fb0cea851237beba4c4f7538b0c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "feed_id": "feedId",
        "feed_output_config": "feedOutputConfig",
        "asset_names": "assetNames",
        "asset_types": "assetTypes",
        "billing_project": "billingProject",
        "condition": "condition",
        "content_type": "contentType",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class CloudAssetProjectFeedConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        feed_id: builtins.str,
        feed_output_config: typing.Union["CloudAssetProjectFeedFeedOutputConfig", typing.Dict[builtins.str, typing.Any]],
        asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        billing_project: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union[CloudAssetProjectFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudAssetProjectFeedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#feed_id CloudAssetProjectFeed#feed_id}
        :param feed_output_config: feed_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#feed_output_config CloudAssetProjectFeed#feed_output_config}
        :param asset_names: A list of the full names of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1. See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#asset_names CloudAssetProjectFeed#asset_names}
        :param asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: "compute.googleapis.com/Disk" See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all supported asset types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#asset_types CloudAssetProjectFeed#asset_types}
        :param billing_project: The project whose identity will be used when sending messages to the destination pubsub topic. It also specifies the project for API enablement check, quota, and billing. If not specified, the resource's project will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#billing_project CloudAssetProjectFeed#billing_project}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#condition CloudAssetProjectFeed#condition}
        :param content_type: Asset content type. If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#content_type CloudAssetProjectFeed#content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#id CloudAssetProjectFeed#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#project CloudAssetProjectFeed#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#timeouts CloudAssetProjectFeed#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(feed_output_config, dict):
            feed_output_config = CloudAssetProjectFeedFeedOutputConfig(**feed_output_config)
        if isinstance(condition, dict):
            condition = CloudAssetProjectFeedCondition(**condition)
        if isinstance(timeouts, dict):
            timeouts = CloudAssetProjectFeedTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18db4ad75bd84c26f47d46ee5b2a11a4d20ed4ba25d36300ea0685acf28c59c6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument feed_id", value=feed_id, expected_type=type_hints["feed_id"])
            check_type(argname="argument feed_output_config", value=feed_output_config, expected_type=type_hints["feed_output_config"])
            check_type(argname="argument asset_names", value=asset_names, expected_type=type_hints["asset_names"])
            check_type(argname="argument asset_types", value=asset_types, expected_type=type_hints["asset_types"])
            check_type(argname="argument billing_project", value=billing_project, expected_type=type_hints["billing_project"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feed_id": feed_id,
            "feed_output_config": feed_output_config,
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
        if billing_project is not None:
            self._values["billing_project"] = billing_project
        if condition is not None:
            self._values["condition"] = condition
        if content_type is not None:
            self._values["content_type"] = content_type
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
    def feed_id(self) -> builtins.str:
        '''This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#feed_id CloudAssetProjectFeed#feed_id}
        '''
        result = self._values.get("feed_id")
        assert result is not None, "Required property 'feed_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feed_output_config(self) -> "CloudAssetProjectFeedFeedOutputConfig":
        '''feed_output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#feed_output_config CloudAssetProjectFeed#feed_output_config}
        '''
        result = self._values.get("feed_output_config")
        assert result is not None, "Required property 'feed_output_config' is missing"
        return typing.cast("CloudAssetProjectFeedFeedOutputConfig", result)

    @builtins.property
    def asset_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the full names of the assets to receive updates.

        You must specify either or both of
        assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
        exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
        See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#asset_names CloudAssetProjectFeed#asset_names}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#asset_types CloudAssetProjectFeed#asset_types}
        '''
        result = self._values.get("asset_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def billing_project(self) -> typing.Optional[builtins.str]:
        '''The project whose identity will be used when sending messages to the destination pubsub topic.

        It also specifies the project for API
        enablement check, quota, and billing. If not specified, the resource's
        project will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#billing_project CloudAssetProjectFeed#billing_project}
        '''
        result = self._values.get("billing_project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(self) -> typing.Optional[CloudAssetProjectFeedCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#condition CloudAssetProjectFeed#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[CloudAssetProjectFeedCondition], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Asset content type.

        If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#content_type CloudAssetProjectFeed#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#id CloudAssetProjectFeed#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#project CloudAssetProjectFeed#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudAssetProjectFeedTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#timeouts CloudAssetProjectFeed#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudAssetProjectFeedTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetProjectFeedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedFeedOutputConfig",
    jsii_struct_bases=[],
    name_mapping={"pubsub_destination": "pubsubDestination"},
)
class CloudAssetProjectFeedFeedOutputConfig:
    def __init__(
        self,
        *,
        pubsub_destination: typing.Union["CloudAssetProjectFeedFeedOutputConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#pubsub_destination CloudAssetProjectFeed#pubsub_destination}
        '''
        if isinstance(pubsub_destination, dict):
            pubsub_destination = CloudAssetProjectFeedFeedOutputConfigPubsubDestination(**pubsub_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98aa10fe752843351217c60b6f23cd4896234db3436b773b6b043e10cd46379)
            check_type(argname="argument pubsub_destination", value=pubsub_destination, expected_type=type_hints["pubsub_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_destination": pubsub_destination,
        }

    @builtins.property
    def pubsub_destination(
        self,
    ) -> "CloudAssetProjectFeedFeedOutputConfigPubsubDestination":
        '''pubsub_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#pubsub_destination CloudAssetProjectFeed#pubsub_destination}
        '''
        result = self._values.get("pubsub_destination")
        assert result is not None, "Required property 'pubsub_destination' is missing"
        return typing.cast("CloudAssetProjectFeedFeedOutputConfigPubsubDestination", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetProjectFeedFeedOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetProjectFeedFeedOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedFeedOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdee3c63b0c6a4625c84bebdfaf03441ff55c630c4e4245886222459515ab0c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPubsubDestination")
    def put_pubsub_destination(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Destination on Cloud Pubsub topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#topic CloudAssetProjectFeed#topic}
        '''
        value = CloudAssetProjectFeedFeedOutputConfigPubsubDestination(topic=topic)

        return typing.cast(None, jsii.invoke(self, "putPubsubDestination", [value]))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestination")
    def pubsub_destination(
        self,
    ) -> "CloudAssetProjectFeedFeedOutputConfigPubsubDestinationOutputReference":
        return typing.cast("CloudAssetProjectFeedFeedOutputConfigPubsubDestinationOutputReference", jsii.get(self, "pubsubDestination"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestinationInput")
    def pubsub_destination_input(
        self,
    ) -> typing.Optional["CloudAssetProjectFeedFeedOutputConfigPubsubDestination"]:
        return typing.cast(typing.Optional["CloudAssetProjectFeedFeedOutputConfigPubsubDestination"], jsii.get(self, "pubsubDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAssetProjectFeedFeedOutputConfig]:
        return typing.cast(typing.Optional[CloudAssetProjectFeedFeedOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAssetProjectFeedFeedOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ad527220f076929321ee2166c8ab728f6997cd77d661b2bbcdceb263465ded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedFeedOutputConfigPubsubDestination",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class CloudAssetProjectFeedFeedOutputConfigPubsubDestination:
    def __init__(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Destination on Cloud Pubsub topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#topic CloudAssetProjectFeed#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b406a0d60a2041dfd73fe3d97ea1f212f81588c05774a8d3c099407a03932229)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }

    @builtins.property
    def topic(self) -> builtins.str:
        '''Destination on Cloud Pubsub topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#topic CloudAssetProjectFeed#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetProjectFeedFeedOutputConfigPubsubDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetProjectFeedFeedOutputConfigPubsubDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedFeedOutputConfigPubsubDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__636cec58cadf8260335212423af943b482fab090570a5f4cff558bbd3bca8924)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b62f013d38af52c1a0246621a75bb88d1854b5216ee012bb419113cbcff51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudAssetProjectFeedFeedOutputConfigPubsubDestination]:
        return typing.cast(typing.Optional[CloudAssetProjectFeedFeedOutputConfigPubsubDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAssetProjectFeedFeedOutputConfigPubsubDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe30708643c0822c36e68b113e1fc3da8b73be2697391c5d82d173b1b434edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudAssetProjectFeedTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#create CloudAssetProjectFeed#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#delete CloudAssetProjectFeed#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#update CloudAssetProjectFeed#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b5adf5d576fa983ff88087f6ed3ea494c82dfe6d68faa622bc7b1de691f30c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#create CloudAssetProjectFeed#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#delete CloudAssetProjectFeed#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_asset_project_feed#update CloudAssetProjectFeed#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssetProjectFeedTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAssetProjectFeedTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudAssetProjectFeed.CloudAssetProjectFeedTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f7fc80dc823064f7ef21767bb03941da1a7404f9c11f7c92dc07fd9ec333bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a33fef53eaa163d372e2439e5c4278460b2ab0f5fb2ec8600e45ae20c13750e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e02db67cf44510001eb5f85dc202555f9fc2ce0b706149fd1937aef9b433a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418ca7fcdb4228d0722efef20c4fa26a2ad4dc00fd83f6c7f8e2f0f9f15998c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetProjectFeedTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetProjectFeedTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetProjectFeedTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5afa7ed7f1a6a049d8f291281ef93560196299e61d2344e287889976d28503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudAssetProjectFeed",
    "CloudAssetProjectFeedCondition",
    "CloudAssetProjectFeedConditionOutputReference",
    "CloudAssetProjectFeedConfig",
    "CloudAssetProjectFeedFeedOutputConfig",
    "CloudAssetProjectFeedFeedOutputConfigOutputReference",
    "CloudAssetProjectFeedFeedOutputConfigPubsubDestination",
    "CloudAssetProjectFeedFeedOutputConfigPubsubDestinationOutputReference",
    "CloudAssetProjectFeedTimeouts",
    "CloudAssetProjectFeedTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1ed001b6f8b108ed2b10513fa594d34f53a35421b2a2c758d2a76d6d4cfeb2ff(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    feed_id: builtins.str,
    feed_output_config: typing.Union[CloudAssetProjectFeedFeedOutputConfig, typing.Dict[builtins.str, typing.Any]],
    asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    billing_project: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[CloudAssetProjectFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudAssetProjectFeedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__915f4d17f61994b8c5751f7cdba0192cc5d996e866e368c541504c031566fd17(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564d7cff33076fe44f8cbd0d294c2a406b6bccfdd85306703fc7fb31e7d45beb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c20a877db3db08d5177f31e03f17fc38c4a145cd5e38f04b1ed950a424b24ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e14c20badc7c8d43d99d0fdff4b3b28df0fa10edd62b0a05537c90b32f6497c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16eb5dd002d259d0120c70700c73a70cc55cf0ad85910db9c65684e40011e6b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba7d65d86d051804efa55455db1e658e23fadb116ffec6befd7e2f32008c4fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c48ec4429a8efc397b102704353ca2bd6b9a05a3ade162e700a0df746c8d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a255d6648fb84a51c31a8dae168deaeccfe74e95f2c4a80e9e56f05bf52d501f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc0bc5eeed116092c33c357051aab8dd34d4382263a9fc3242bdb0d71b2d777(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f399a96b8692f54673d247439d4afc3809a5b09e726e65b97837b0590ca74e1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c4ca3981cfc2df7f24a7865acf5b489f31bb2d6765e684266435d0f2c6311e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7876556c7da02144f844d5f6635e1c6fb2cb9915dab1f3b22114fea194498abe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbacd94735c7cfab456a2f1e2d2e87f86103fef9d3befd57a5abc87535034c7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4044d3a123ecdf5b5c911b8ea33049288956b8d955668b7f972ba8c7aa9aff6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ef84c06b559798788b883e61a550691360fb0cea851237beba4c4f7538b0c5(
    value: typing.Optional[CloudAssetProjectFeedCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18db4ad75bd84c26f47d46ee5b2a11a4d20ed4ba25d36300ea0685acf28c59c6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    feed_id: builtins.str,
    feed_output_config: typing.Union[CloudAssetProjectFeedFeedOutputConfig, typing.Dict[builtins.str, typing.Any]],
    asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    billing_project: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[CloudAssetProjectFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudAssetProjectFeedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98aa10fe752843351217c60b6f23cd4896234db3436b773b6b043e10cd46379(
    *,
    pubsub_destination: typing.Union[CloudAssetProjectFeedFeedOutputConfigPubsubDestination, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdee3c63b0c6a4625c84bebdfaf03441ff55c630c4e4245886222459515ab0c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ad527220f076929321ee2166c8ab728f6997cd77d661b2bbcdceb263465ded(
    value: typing.Optional[CloudAssetProjectFeedFeedOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b406a0d60a2041dfd73fe3d97ea1f212f81588c05774a8d3c099407a03932229(
    *,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636cec58cadf8260335212423af943b482fab090570a5f4cff558bbd3bca8924(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b62f013d38af52c1a0246621a75bb88d1854b5216ee012bb419113cbcff51d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe30708643c0822c36e68b113e1fc3da8b73be2697391c5d82d173b1b434edf(
    value: typing.Optional[CloudAssetProjectFeedFeedOutputConfigPubsubDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b5adf5d576fa983ff88087f6ed3ea494c82dfe6d68faa622bc7b1de691f30c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f7fc80dc823064f7ef21767bb03941da1a7404f9c11f7c92dc07fd9ec333bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a33fef53eaa163d372e2439e5c4278460b2ab0f5fb2ec8600e45ae20c13750e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e02db67cf44510001eb5f85dc202555f9fc2ce0b706149fd1937aef9b433a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418ca7fcdb4228d0722efef20c4fa26a2ad4dc00fd83f6c7f8e2f0f9f15998c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5afa7ed7f1a6a049d8f291281ef93560196299e61d2344e287889976d28503(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudAssetProjectFeedTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
