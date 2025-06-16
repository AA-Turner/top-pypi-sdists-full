r'''
# `google_cloud_asset_organization_feed`

Refer to the Terraform Registry for docs: [`google_cloud_asset_organization_feed`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed).
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


class GoogleCloudAssetOrganizationFeed(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeed",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed google_cloud_asset_organization_feed}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        billing_project: builtins.str,
        feed_id: builtins.str,
        feed_output_config: typing.Union["GoogleCloudAssetOrganizationFeedFeedOutputConfig", typing.Dict[builtins.str, typing.Any]],
        org_id: builtins.str,
        asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[typing.Union["GoogleCloudAssetOrganizationFeedCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudAssetOrganizationFeedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed google_cloud_asset_organization_feed} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param billing_project: The project whose identity will be used when sending messages to the destination pubsub topic. It also specifies the project for API enablement check, quota, and billing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#billing_project GoogleCloudAssetOrganizationFeed#billing_project}
        :param feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#feed_id GoogleCloudAssetOrganizationFeed#feed_id}
        :param feed_output_config: feed_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#feed_output_config GoogleCloudAssetOrganizationFeed#feed_output_config}
        :param org_id: The organization this feed should be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#org_id GoogleCloudAssetOrganizationFeed#org_id}
        :param asset_names: A list of the full names of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1. See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#asset_names GoogleCloudAssetOrganizationFeed#asset_names}
        :param asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: "compute.googleapis.com/Disk" See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all supported asset types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#asset_types GoogleCloudAssetOrganizationFeed#asset_types}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#condition GoogleCloudAssetOrganizationFeed#condition}
        :param content_type: Asset content type. If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#content_type GoogleCloudAssetOrganizationFeed#content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#id GoogleCloudAssetOrganizationFeed#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#timeouts GoogleCloudAssetOrganizationFeed#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ab5c59f08edfd2184056229e276b0a112dca3e3df8cafbacaa6a0745701b25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudAssetOrganizationFeedConfig(
            billing_project=billing_project,
            feed_id=feed_id,
            feed_output_config=feed_output_config,
            org_id=org_id,
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
        '''Generates CDKTF code for importing a GoogleCloudAssetOrganizationFeed resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudAssetOrganizationFeed to import.
        :param import_from_id: The id of the existing GoogleCloudAssetOrganizationFeed that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudAssetOrganizationFeed to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed4dae8dcfebce0142e87d3edf1489e16e75df7c8a2edbeb0d2661c49ab76c7)
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#expression GoogleCloudAssetOrganizationFeed#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#description GoogleCloudAssetOrganizationFeed#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#location GoogleCloudAssetOrganizationFeed#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#title GoogleCloudAssetOrganizationFeed#title}
        '''
        value = GoogleCloudAssetOrganizationFeedCondition(
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
        pubsub_destination: typing.Union["GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#pubsub_destination GoogleCloudAssetOrganizationFeed#pubsub_destination}
        '''
        value = GoogleCloudAssetOrganizationFeedFeedOutputConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#create GoogleCloudAssetOrganizationFeed#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#delete GoogleCloudAssetOrganizationFeed#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#update GoogleCloudAssetOrganizationFeed#update}.
        '''
        value = GoogleCloudAssetOrganizationFeedTimeouts(
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
    def condition(self) -> "GoogleCloudAssetOrganizationFeedConditionOutputReference":
        return typing.cast("GoogleCloudAssetOrganizationFeedConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="feedOutputConfig")
    def feed_output_config(
        self,
    ) -> "GoogleCloudAssetOrganizationFeedFeedOutputConfigOutputReference":
        return typing.cast("GoogleCloudAssetOrganizationFeedFeedOutputConfigOutputReference", jsii.get(self, "feedOutputConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudAssetOrganizationFeedTimeoutsOutputReference":
        return typing.cast("GoogleCloudAssetOrganizationFeedTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def condition_input(
        self,
    ) -> typing.Optional["GoogleCloudAssetOrganizationFeedCondition"]:
        return typing.cast(typing.Optional["GoogleCloudAssetOrganizationFeedCondition"], jsii.get(self, "conditionInput"))

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
    ) -> typing.Optional["GoogleCloudAssetOrganizationFeedFeedOutputConfig"]:
        return typing.cast(typing.Optional["GoogleCloudAssetOrganizationFeedFeedOutputConfig"], jsii.get(self, "feedOutputConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudAssetOrganizationFeedTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudAssetOrganizationFeedTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="assetNames")
    def asset_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assetNames"))

    @asset_names.setter
    def asset_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae71c5c2e2e31b9c39540a3de14944edf554374014962282d9d6a2c45531c841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assetTypes")
    def asset_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assetTypes"))

    @asset_types.setter
    def asset_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6012fc4a8a49d047d1617a85018b7c9474a33b582222de78dffcb8cd0e8a235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingProject")
    def billing_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingProject"))

    @billing_project.setter
    def billing_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7139bdb197cb39c3538854e66943c88feead722464d9728becf96f82647bf161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc11d26b3d1a153f7646c23e38752156a0d051c2e43ae5a4b505f153cc90979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="feedId")
    def feed_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "feedId"))

    @feed_id.setter
    def feed_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff7ad45389adc2a3a557bca9a3d7fde8c9a6fb4d2e1b61e18cf1330fb73868c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feedId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09059d0f1a4656725186d61c67ae30657b0aa4000ee0f8685991c9ecf808eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b532b70db281294be326633b2eb52de39d5b9030b6095eade16e4f635b4be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class GoogleCloudAssetOrganizationFeedCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#expression GoogleCloudAssetOrganizationFeed#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#description GoogleCloudAssetOrganizationFeed#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#location GoogleCloudAssetOrganizationFeed#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#title GoogleCloudAssetOrganizationFeed#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a99e95fdd5be55f3b1cf56346c49bb82f60fa0fa507531f14ce0df037199da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#expression GoogleCloudAssetOrganizationFeed#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the expression,
        e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#description GoogleCloudAssetOrganizationFeed#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#location GoogleCloudAssetOrganizationFeed#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#title GoogleCloudAssetOrganizationFeed#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudAssetOrganizationFeedCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudAssetOrganizationFeedConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b01f6d4803c4e3dde239541fac8906fa3b94c31d8a65ca4ce0f38f4624ba100d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4a40701137534989d5c6e920614776357de4b640de0a2d50b7067d293e8db20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7300468f1ae18e794e72fb19e1debe61c802601c5df06129c016674b8b3f60f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7affd38ec19213a0f33fab0b50a4289f5ca7fef7c46f90d807a0fff6172a0638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a0f08af4d3ec81a83ccfff871c82171f7f968df398b60afe5d04ed78867d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudAssetOrganizationFeedCondition]:
        return typing.cast(typing.Optional[GoogleCloudAssetOrganizationFeedCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudAssetOrganizationFeedCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa256c4c0cc9ec75aee94cf6ce9275f349a8bf6a24e8c5a734ede1aedf11bec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedConfig",
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
        "org_id": "orgId",
        "asset_names": "assetNames",
        "asset_types": "assetTypes",
        "condition": "condition",
        "content_type": "contentType",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GoogleCloudAssetOrganizationFeedConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        feed_output_config: typing.Union["GoogleCloudAssetOrganizationFeedFeedOutputConfig", typing.Dict[builtins.str, typing.Any]],
        org_id: builtins.str,
        asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[typing.Union[GoogleCloudAssetOrganizationFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        content_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudAssetOrganizationFeedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param billing_project: The project whose identity will be used when sending messages to the destination pubsub topic. It also specifies the project for API enablement check, quota, and billing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#billing_project GoogleCloudAssetOrganizationFeed#billing_project}
        :param feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#feed_id GoogleCloudAssetOrganizationFeed#feed_id}
        :param feed_output_config: feed_output_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#feed_output_config GoogleCloudAssetOrganizationFeed#feed_output_config}
        :param org_id: The organization this feed should be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#org_id GoogleCloudAssetOrganizationFeed#org_id}
        :param asset_names: A list of the full names of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1. See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#asset_names GoogleCloudAssetOrganizationFeed#asset_names}
        :param asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to the feed. For example: "compute.googleapis.com/Disk" See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all supported asset types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#asset_types GoogleCloudAssetOrganizationFeed#asset_types}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#condition GoogleCloudAssetOrganizationFeed#condition}
        :param content_type: Asset content type. If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#content_type GoogleCloudAssetOrganizationFeed#content_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#id GoogleCloudAssetOrganizationFeed#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#timeouts GoogleCloudAssetOrganizationFeed#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(feed_output_config, dict):
            feed_output_config = GoogleCloudAssetOrganizationFeedFeedOutputConfig(**feed_output_config)
        if isinstance(condition, dict):
            condition = GoogleCloudAssetOrganizationFeedCondition(**condition)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudAssetOrganizationFeedTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5267f9f3b0afefa5e677149f23e9181a85eaf0576bac1784cd37642a360d1d3)
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
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
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
            "org_id": org_id,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#billing_project GoogleCloudAssetOrganizationFeed#billing_project}
        '''
        result = self._values.get("billing_project")
        assert result is not None, "Required property 'billing_project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feed_id(self) -> builtins.str:
        '''This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#feed_id GoogleCloudAssetOrganizationFeed#feed_id}
        '''
        result = self._values.get("feed_id")
        assert result is not None, "Required property 'feed_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feed_output_config(self) -> "GoogleCloudAssetOrganizationFeedFeedOutputConfig":
        '''feed_output_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#feed_output_config GoogleCloudAssetOrganizationFeed#feed_output_config}
        '''
        result = self._values.get("feed_output_config")
        assert result is not None, "Required property 'feed_output_config' is missing"
        return typing.cast("GoogleCloudAssetOrganizationFeedFeedOutputConfig", result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The organization this feed should be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#org_id GoogleCloudAssetOrganizationFeed#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the full names of the assets to receive updates.

        You must specify either or both of
        assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
        exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
        See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#asset_names GoogleCloudAssetOrganizationFeed#asset_names}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#asset_types GoogleCloudAssetOrganizationFeed#asset_types}
        '''
        result = self._values.get("asset_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def condition(self) -> typing.Optional[GoogleCloudAssetOrganizationFeedCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#condition GoogleCloudAssetOrganizationFeed#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[GoogleCloudAssetOrganizationFeedCondition], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Asset content type.

        If not specified, no content but the asset name and type will be returned. Possible values: ["CONTENT_TYPE_UNSPECIFIED", "RESOURCE", "IAM_POLICY", "ORG_POLICY", "OS_INVENTORY", "ACCESS_POLICY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#content_type GoogleCloudAssetOrganizationFeed#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#id GoogleCloudAssetOrganizationFeed#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudAssetOrganizationFeedTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#timeouts GoogleCloudAssetOrganizationFeed#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudAssetOrganizationFeedTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudAssetOrganizationFeedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedFeedOutputConfig",
    jsii_struct_bases=[],
    name_mapping={"pubsub_destination": "pubsubDestination"},
)
class GoogleCloudAssetOrganizationFeedFeedOutputConfig:
    def __init__(
        self,
        *,
        pubsub_destination: typing.Union["GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#pubsub_destination GoogleCloudAssetOrganizationFeed#pubsub_destination}
        '''
        if isinstance(pubsub_destination, dict):
            pubsub_destination = GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination(**pubsub_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e756dcda646da4d1b1b7ffced1557093d6cb36d1a1490323365b4acedefaa6e)
            check_type(argname="argument pubsub_destination", value=pubsub_destination, expected_type=type_hints["pubsub_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_destination": pubsub_destination,
        }

    @builtins.property
    def pubsub_destination(
        self,
    ) -> "GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination":
        '''pubsub_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#pubsub_destination GoogleCloudAssetOrganizationFeed#pubsub_destination}
        '''
        result = self._values.get("pubsub_destination")
        assert result is not None, "Required property 'pubsub_destination' is missing"
        return typing.cast("GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudAssetOrganizationFeedFeedOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudAssetOrganizationFeedFeedOutputConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedFeedOutputConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed96b80644f2813db221f679a304039a26f8fc2bf43829556c6ed00734928a79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPubsubDestination")
    def put_pubsub_destination(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Destination on Cloud Pubsub topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#topic GoogleCloudAssetOrganizationFeed#topic}
        '''
        value = GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination(
            topic=topic
        )

        return typing.cast(None, jsii.invoke(self, "putPubsubDestination", [value]))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestination")
    def pubsub_destination(
        self,
    ) -> "GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestinationOutputReference":
        return typing.cast("GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestinationOutputReference", jsii.get(self, "pubsubDestination"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestinationInput")
    def pubsub_destination_input(
        self,
    ) -> typing.Optional["GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination"]:
        return typing.cast(typing.Optional["GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination"], jsii.get(self, "pubsubDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfig]:
        return typing.cast(typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c908d96bf0d89c2dacf8a6f27d8d524044fe18fc33dff75712c14bc0e554bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination:
    def __init__(self, *, topic: builtins.str) -> None:
        '''
        :param topic: Destination on Cloud Pubsub topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#topic GoogleCloudAssetOrganizationFeed#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c73072a35073508bfa52b926c46b12f8cc15c9a7be0b415cd91534c3f38e3c)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }

    @builtins.property
    def topic(self) -> builtins.str:
        '''Destination on Cloud Pubsub topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#topic GoogleCloudAssetOrganizationFeed#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a5a5c4c565b0bbc7ea6bac5bba00bfecef74f7d994f4753086894de1ce0c1d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__709935df2a75c2e0df58c004fa1b33594ae3b499bfd5f2cc7c2e7809feaee975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination]:
        return typing.cast(typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976560efe3eff1e9d9cc2ef39c99a7fc46cc1b9eb98b726f5095cd462d690f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudAssetOrganizationFeedTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#create GoogleCloudAssetOrganizationFeed#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#delete GoogleCloudAssetOrganizationFeed#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#update GoogleCloudAssetOrganizationFeed#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39463378c2c743edb42484c89d7d7e3e39bfd012eb1750d9f54bcb0f9ad05ad)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#create GoogleCloudAssetOrganizationFeed#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#delete GoogleCloudAssetOrganizationFeed#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_asset_organization_feed#update GoogleCloudAssetOrganizationFeed#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudAssetOrganizationFeedTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudAssetOrganizationFeedTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudAssetOrganizationFeed.GoogleCloudAssetOrganizationFeedTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a43a02a3a744436b682e35d729c482e26c977f2b767e3103c86a4c7ba794b3b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c610e98bddafce1d35bad694b950650e870382aa7b433628951e84e38c353f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc8d028ea5da124db52cf334550011232119ba61500f105d60375c7a5eea00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e060e9ed23c703ffa25efafd1c8e8373d94c3d95f79fca14126141a4f1d980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudAssetOrganizationFeedTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudAssetOrganizationFeedTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudAssetOrganizationFeedTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cba168578f2f6f71248030e62ed8a6cd5a4f50c39d52f63ed90239738f1efeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudAssetOrganizationFeed",
    "GoogleCloudAssetOrganizationFeedCondition",
    "GoogleCloudAssetOrganizationFeedConditionOutputReference",
    "GoogleCloudAssetOrganizationFeedConfig",
    "GoogleCloudAssetOrganizationFeedFeedOutputConfig",
    "GoogleCloudAssetOrganizationFeedFeedOutputConfigOutputReference",
    "GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination",
    "GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestinationOutputReference",
    "GoogleCloudAssetOrganizationFeedTimeouts",
    "GoogleCloudAssetOrganizationFeedTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a6ab5c59f08edfd2184056229e276b0a112dca3e3df8cafbacaa6a0745701b25(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    billing_project: builtins.str,
    feed_id: builtins.str,
    feed_output_config: typing.Union[GoogleCloudAssetOrganizationFeedFeedOutputConfig, typing.Dict[builtins.str, typing.Any]],
    org_id: builtins.str,
    asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[typing.Union[GoogleCloudAssetOrganizationFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudAssetOrganizationFeedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0ed4dae8dcfebce0142e87d3edf1489e16e75df7c8a2edbeb0d2661c49ab76c7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae71c5c2e2e31b9c39540a3de14944edf554374014962282d9d6a2c45531c841(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6012fc4a8a49d047d1617a85018b7c9474a33b582222de78dffcb8cd0e8a235(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7139bdb197cb39c3538854e66943c88feead722464d9728becf96f82647bf161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc11d26b3d1a153f7646c23e38752156a0d051c2e43ae5a4b505f153cc90979(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff7ad45389adc2a3a557bca9a3d7fde8c9a6fb4d2e1b61e18cf1330fb73868c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09059d0f1a4656725186d61c67ae30657b0aa4000ee0f8685991c9ecf808eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b532b70db281294be326633b2eb52de39d5b9030b6095eade16e4f635b4be3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a99e95fdd5be55f3b1cf56346c49bb82f60fa0fa507531f14ce0df037199da(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01f6d4803c4e3dde239541fac8906fa3b94c31d8a65ca4ce0f38f4624ba100d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a40701137534989d5c6e920614776357de4b640de0a2d50b7067d293e8db20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7300468f1ae18e794e72fb19e1debe61c802601c5df06129c016674b8b3f60f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7affd38ec19213a0f33fab0b50a4289f5ca7fef7c46f90d807a0fff6172a0638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a0f08af4d3ec81a83ccfff871c82171f7f968df398b60afe5d04ed78867d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa256c4c0cc9ec75aee94cf6ce9275f349a8bf6a24e8c5a734ede1aedf11bec8(
    value: typing.Optional[GoogleCloudAssetOrganizationFeedCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5267f9f3b0afefa5e677149f23e9181a85eaf0576bac1784cd37642a360d1d3(
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
    feed_output_config: typing.Union[GoogleCloudAssetOrganizationFeedFeedOutputConfig, typing.Dict[builtins.str, typing.Any]],
    org_id: builtins.str,
    asset_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[typing.Union[GoogleCloudAssetOrganizationFeedCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudAssetOrganizationFeedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e756dcda646da4d1b1b7ffced1557093d6cb36d1a1490323365b4acedefaa6e(
    *,
    pubsub_destination: typing.Union[GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed96b80644f2813db221f679a304039a26f8fc2bf43829556c6ed00734928a79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c908d96bf0d89c2dacf8a6f27d8d524044fe18fc33dff75712c14bc0e554bd0(
    value: typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c73072a35073508bfa52b926c46b12f8cc15c9a7be0b415cd91534c3f38e3c(
    *,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5a5c4c565b0bbc7ea6bac5bba00bfecef74f7d994f4753086894de1ce0c1d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709935df2a75c2e0df58c004fa1b33594ae3b499bfd5f2cc7c2e7809feaee975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976560efe3eff1e9d9cc2ef39c99a7fc46cc1b9eb98b726f5095cd462d690f44(
    value: typing.Optional[GoogleCloudAssetOrganizationFeedFeedOutputConfigPubsubDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39463378c2c743edb42484c89d7d7e3e39bfd012eb1750d9f54bcb0f9ad05ad(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43a02a3a744436b682e35d729c482e26c977f2b767e3103c86a4c7ba794b3b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c610e98bddafce1d35bad694b950650e870382aa7b433628951e84e38c353f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc8d028ea5da124db52cf334550011232119ba61500f105d60375c7a5eea00b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e060e9ed23c703ffa25efafd1c8e8373d94c3d95f79fca14126141a4f1d980(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cba168578f2f6f71248030e62ed8a6cd5a4f50c39d52f63ed90239738f1efeb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudAssetOrganizationFeedTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
