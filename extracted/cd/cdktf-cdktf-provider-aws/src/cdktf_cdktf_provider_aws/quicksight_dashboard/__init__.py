r'''
# `aws_quicksight_dashboard`

Refer to the Terraform Registry for docs: [`aws_quicksight_dashboard`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard).
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


class QuicksightDashboard(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboard",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard aws_quicksight_dashboard}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dashboard_id: builtins.str,
        name: builtins.str,
        version_description: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        dashboard_publish_options: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        definition: typing.Any = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union["QuicksightDashboardParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_entity: typing.Optional[typing.Union["QuicksightDashboardSourceEntity", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        theme_arn: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["QuicksightDashboardTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard aws_quicksight_dashboard} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dashboard_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#dashboard_id QuicksightDashboard#dashboard_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#version_description QuicksightDashboard#version_description}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#aws_account_id QuicksightDashboard#aws_account_id}.
        :param dashboard_publish_options: dashboard_publish_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#dashboard_publish_options QuicksightDashboard#dashboard_publish_options}
        :param definition: definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#definition QuicksightDashboard#definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#id QuicksightDashboard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#parameters QuicksightDashboard#parameters}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#permissions QuicksightDashboard#permissions}
        :param source_entity: source_entity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#source_entity QuicksightDashboard#source_entity}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#tags QuicksightDashboard#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#tags_all QuicksightDashboard#tags_all}.
        :param theme_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#theme_arn QuicksightDashboard#theme_arn}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#timeouts QuicksightDashboard#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0142371e5ecafa09f1d7801393ac6f73c90ae54d5e083a55b63a13d2ee548170)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightDashboardConfig(
            dashboard_id=dashboard_id,
            name=name,
            version_description=version_description,
            aws_account_id=aws_account_id,
            dashboard_publish_options=dashboard_publish_options,
            definition=definition,
            id=id,
            parameters=parameters,
            permissions=permissions,
            source_entity=source_entity,
            tags=tags,
            tags_all=tags_all,
            theme_arn=theme_arn,
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
        '''Generates CDKTF code for importing a QuicksightDashboard resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightDashboard to import.
        :param import_from_id: The id of the existing QuicksightDashboard that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightDashboard to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129cfb5758f57fec86ebb8d956d270025a674e435d260e1347f9a3da9c268df4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDashboardPublishOptions")
    def put_dashboard_publish_options(
        self,
        *,
        ad_hoc_filtering_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_drill_up_down_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_menu_label_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_tooltip_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_to_csv_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportToCsvOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_with_hidden_fields_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_controls_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetControlsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_layout_element_maximization_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_axis_sort_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_menu_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualMenuOption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_hoc_filtering_option: ad_hoc_filtering_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#ad_hoc_filtering_option QuicksightDashboard#ad_hoc_filtering_option}
        :param data_point_drill_up_down_option: data_point_drill_up_down_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_drill_up_down_option QuicksightDashboard#data_point_drill_up_down_option}
        :param data_point_menu_label_option: data_point_menu_label_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_menu_label_option QuicksightDashboard#data_point_menu_label_option}
        :param data_point_tooltip_option: data_point_tooltip_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_tooltip_option QuicksightDashboard#data_point_tooltip_option}
        :param export_to_csv_option: export_to_csv_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#export_to_csv_option QuicksightDashboard#export_to_csv_option}
        :param export_with_hidden_fields_option: export_with_hidden_fields_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#export_with_hidden_fields_option QuicksightDashboard#export_with_hidden_fields_option}
        :param sheet_controls_option: sheet_controls_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#sheet_controls_option QuicksightDashboard#sheet_controls_option}
        :param sheet_layout_element_maximization_option: sheet_layout_element_maximization_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#sheet_layout_element_maximization_option QuicksightDashboard#sheet_layout_element_maximization_option}
        :param visual_axis_sort_option: visual_axis_sort_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visual_axis_sort_option QuicksightDashboard#visual_axis_sort_option}
        :param visual_menu_option: visual_menu_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visual_menu_option QuicksightDashboard#visual_menu_option}
        '''
        value = QuicksightDashboardDashboardPublishOptions(
            ad_hoc_filtering_option=ad_hoc_filtering_option,
            data_point_drill_up_down_option=data_point_drill_up_down_option,
            data_point_menu_label_option=data_point_menu_label_option,
            data_point_tooltip_option=data_point_tooltip_option,
            export_to_csv_option=export_to_csv_option,
            export_with_hidden_fields_option=export_with_hidden_fields_option,
            sheet_controls_option=sheet_controls_option,
            sheet_layout_element_maximization_option=sheet_layout_element_maximization_option,
            visual_axis_sort_option=visual_axis_sort_option,
            visual_menu_option=visual_menu_option,
        )

        return typing.cast(None, jsii.invoke(self, "putDashboardPublishOptions", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        date_time_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDateTimeParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        decimal_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDecimalParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        integer_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersIntegerParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersStringParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param date_time_parameters: date_time_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#date_time_parameters QuicksightDashboard#date_time_parameters}
        :param decimal_parameters: decimal_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#decimal_parameters QuicksightDashboard#decimal_parameters}
        :param integer_parameters: integer_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#integer_parameters QuicksightDashboard#integer_parameters}
        :param string_parameters: string_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#string_parameters QuicksightDashboard#string_parameters}
        '''
        value = QuicksightDashboardParameters(
            date_time_parameters=date_time_parameters,
            decimal_parameters=decimal_parameters,
            integer_parameters=integer_parameters,
            string_parameters=string_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardPermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01b81f79d5eaf224102650dc797fc44d62a0b2cbd97a63e514487a77c6ea714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="putSourceEntity")
    def put_source_entity(
        self,
        *,
        source_template: typing.Optional[typing.Union["QuicksightDashboardSourceEntitySourceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param source_template: source_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#source_template QuicksightDashboard#source_template}
        '''
        value = QuicksightDashboardSourceEntity(source_template=source_template)

        return typing.cast(None, jsii.invoke(self, "putSourceEntity", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#create QuicksightDashboard#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#delete QuicksightDashboard#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#update QuicksightDashboard#update}.
        '''
        value = QuicksightDashboardTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetDashboardPublishOptions")
    def reset_dashboard_publish_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDashboardPublishOptions", []))

    @jsii.member(jsii_name="resetDefinition")
    def reset_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefinition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetSourceEntity")
    def reset_source_entity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceEntity", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetThemeArn")
    def reset_theme_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThemeArn", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property
    @jsii.member(jsii_name="dashboardPublishOptions")
    def dashboard_publish_options(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsOutputReference", jsii.get(self, "dashboardPublishOptions"))

    @builtins.property
    @jsii.member(jsii_name="definitionInput")
    def definition_input(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "definitionInput"))

    @builtins.property
    @jsii.member(jsii_name="lastPublishedTime")
    def last_published_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastPublishedTime"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedTime")
    def last_updated_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "QuicksightDashboardParametersOutputReference":
        return typing.cast("QuicksightDashboardParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "QuicksightDashboardPermissionsList":
        return typing.cast("QuicksightDashboardPermissionsList", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="sourceEntity")
    def source_entity(self) -> "QuicksightDashboardSourceEntityOutputReference":
        return typing.cast("QuicksightDashboardSourceEntityOutputReference", jsii.get(self, "sourceEntity"))

    @builtins.property
    @jsii.member(jsii_name="sourceEntityArn")
    def source_entity_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceEntityArn"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "QuicksightDashboardTimeoutsOutputReference":
        return typing.cast("QuicksightDashboardTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionNumber")
    def version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "versionNumber"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dashboardIdInput")
    def dashboard_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dashboardIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dashboardPublishOptionsInput")
    def dashboard_publish_options_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptions"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptions"], jsii.get(self, "dashboardPublishOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional["QuicksightDashboardParameters"]:
        return typing.cast(typing.Optional["QuicksightDashboardParameters"], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceEntityInput")
    def source_entity_input(self) -> typing.Optional["QuicksightDashboardSourceEntity"]:
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntity"], jsii.get(self, "sourceEntityInput"))

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
    @jsii.member(jsii_name="themeArnInput")
    def theme_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "themeArnInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightDashboardTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightDashboardTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionDescriptionInput")
    def version_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95532f0d66eaae109434396f33762437469f8eb4a9be1c2621ca0afbf4ba592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dashboardId")
    def dashboard_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dashboardId"))

    @dashboard_id.setter
    def dashboard_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef938f1586ebb043e694cdd848be4f9d6196894f419dcd7b7c5ee22d7ffdb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20857df778db6d35870c1b0a98f20a2f0664ad0e2bc98dce0f455ec60a6045d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e72e3a09b68789a747424f6e82517d456ce57b0c17080f40ced3e263870ec2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08aeb73c0bce5391f5f9933c434f8efad6ed33116a255bf61e5bc78c9171225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382ffcd6441fd7b0cca276a108a445f2e1dc5dd70d26212b7e3f6a3d02731d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce8d348ecaadbd80d6787987ec19096168213b753fa56fd06ffbf85ba36270d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="themeArn")
    def theme_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "themeArn"))

    @theme_arn.setter
    def theme_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767d04bf3c4669d5d30a21335f94be9428e7c0cc259c83c9c4cb1355c3944969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "themeArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionDescription")
    def version_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionDescription"))

    @version_description.setter
    def version_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434a869f55e7cab11867bc2da111bf5eaa7a0abd4df78ea38fc4c8cc6765f6d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDescription", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dashboard_id": "dashboardId",
        "name": "name",
        "version_description": "versionDescription",
        "aws_account_id": "awsAccountId",
        "dashboard_publish_options": "dashboardPublishOptions",
        "definition": "definition",
        "id": "id",
        "parameters": "parameters",
        "permissions": "permissions",
        "source_entity": "sourceEntity",
        "tags": "tags",
        "tags_all": "tagsAll",
        "theme_arn": "themeArn",
        "timeouts": "timeouts",
    },
)
class QuicksightDashboardConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dashboard_id: builtins.str,
        name: builtins.str,
        version_description: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        dashboard_publish_options: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        definition: typing.Any = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union["QuicksightDashboardParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_entity: typing.Optional[typing.Union["QuicksightDashboardSourceEntity", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        theme_arn: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["QuicksightDashboardTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dashboard_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#dashboard_id QuicksightDashboard#dashboard_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#version_description QuicksightDashboard#version_description}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#aws_account_id QuicksightDashboard#aws_account_id}.
        :param dashboard_publish_options: dashboard_publish_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#dashboard_publish_options QuicksightDashboard#dashboard_publish_options}
        :param definition: definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#definition QuicksightDashboard#definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#id QuicksightDashboard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#parameters QuicksightDashboard#parameters}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#permissions QuicksightDashboard#permissions}
        :param source_entity: source_entity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#source_entity QuicksightDashboard#source_entity}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#tags QuicksightDashboard#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#tags_all QuicksightDashboard#tags_all}.
        :param theme_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#theme_arn QuicksightDashboard#theme_arn}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#timeouts QuicksightDashboard#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dashboard_publish_options, dict):
            dashboard_publish_options = QuicksightDashboardDashboardPublishOptions(**dashboard_publish_options)
        if isinstance(parameters, dict):
            parameters = QuicksightDashboardParameters(**parameters)
        if isinstance(source_entity, dict):
            source_entity = QuicksightDashboardSourceEntity(**source_entity)
        if isinstance(timeouts, dict):
            timeouts = QuicksightDashboardTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd2be5bd8c47f2242be9410fa55cbd7662770bc8faa40072f571609e9e94ab2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dashboard_id", value=dashboard_id, expected_type=type_hints["dashboard_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument dashboard_publish_options", value=dashboard_publish_options, expected_type=type_hints["dashboard_publish_options"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument source_entity", value=source_entity, expected_type=type_hints["source_entity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument theme_arn", value=theme_arn, expected_type=type_hints["theme_arn"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dashboard_id": dashboard_id,
            "name": name,
            "version_description": version_description,
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
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if dashboard_publish_options is not None:
            self._values["dashboard_publish_options"] = dashboard_publish_options
        if definition is not None:
            self._values["definition"] = definition
        if id is not None:
            self._values["id"] = id
        if parameters is not None:
            self._values["parameters"] = parameters
        if permissions is not None:
            self._values["permissions"] = permissions
        if source_entity is not None:
            self._values["source_entity"] = source_entity
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if theme_arn is not None:
            self._values["theme_arn"] = theme_arn
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
    def dashboard_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#dashboard_id QuicksightDashboard#dashboard_id}.'''
        result = self._values.get("dashboard_id")
        assert result is not None, "Required property 'dashboard_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#version_description QuicksightDashboard#version_description}.'''
        result = self._values.get("version_description")
        assert result is not None, "Required property 'version_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#aws_account_id QuicksightDashboard#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dashboard_publish_options(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptions"]:
        '''dashboard_publish_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#dashboard_publish_options QuicksightDashboard#dashboard_publish_options}
        '''
        result = self._values.get("dashboard_publish_options")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptions"], result)

    @builtins.property
    def definition(self) -> typing.Any:
        '''definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#definition QuicksightDashboard#definition}
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Any, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#id QuicksightDashboard#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional["QuicksightDashboardParameters"]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#parameters QuicksightDashboard#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["QuicksightDashboardParameters"], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#permissions QuicksightDashboard#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]], result)

    @builtins.property
    def source_entity(self) -> typing.Optional["QuicksightDashboardSourceEntity"]:
        '''source_entity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#source_entity QuicksightDashboard#source_entity}
        '''
        result = self._values.get("source_entity")
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntity"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#tags QuicksightDashboard#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#tags_all QuicksightDashboard#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def theme_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#theme_arn QuicksightDashboard#theme_arn}.'''
        result = self._values.get("theme_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["QuicksightDashboardTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#timeouts QuicksightDashboard#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["QuicksightDashboardTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ad_hoc_filtering_option": "adHocFilteringOption",
        "data_point_drill_up_down_option": "dataPointDrillUpDownOption",
        "data_point_menu_label_option": "dataPointMenuLabelOption",
        "data_point_tooltip_option": "dataPointTooltipOption",
        "export_to_csv_option": "exportToCsvOption",
        "export_with_hidden_fields_option": "exportWithHiddenFieldsOption",
        "sheet_controls_option": "sheetControlsOption",
        "sheet_layout_element_maximization_option": "sheetLayoutElementMaximizationOption",
        "visual_axis_sort_option": "visualAxisSortOption",
        "visual_menu_option": "visualMenuOption",
    },
)
class QuicksightDashboardDashboardPublishOptions:
    def __init__(
        self,
        *,
        ad_hoc_filtering_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_drill_up_down_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_menu_label_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_tooltip_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_to_csv_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportToCsvOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_with_hidden_fields_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_controls_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetControlsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_layout_element_maximization_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_axis_sort_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_menu_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualMenuOption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_hoc_filtering_option: ad_hoc_filtering_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#ad_hoc_filtering_option QuicksightDashboard#ad_hoc_filtering_option}
        :param data_point_drill_up_down_option: data_point_drill_up_down_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_drill_up_down_option QuicksightDashboard#data_point_drill_up_down_option}
        :param data_point_menu_label_option: data_point_menu_label_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_menu_label_option QuicksightDashboard#data_point_menu_label_option}
        :param data_point_tooltip_option: data_point_tooltip_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_tooltip_option QuicksightDashboard#data_point_tooltip_option}
        :param export_to_csv_option: export_to_csv_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#export_to_csv_option QuicksightDashboard#export_to_csv_option}
        :param export_with_hidden_fields_option: export_with_hidden_fields_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#export_with_hidden_fields_option QuicksightDashboard#export_with_hidden_fields_option}
        :param sheet_controls_option: sheet_controls_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#sheet_controls_option QuicksightDashboard#sheet_controls_option}
        :param sheet_layout_element_maximization_option: sheet_layout_element_maximization_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#sheet_layout_element_maximization_option QuicksightDashboard#sheet_layout_element_maximization_option}
        :param visual_axis_sort_option: visual_axis_sort_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visual_axis_sort_option QuicksightDashboard#visual_axis_sort_option}
        :param visual_menu_option: visual_menu_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visual_menu_option QuicksightDashboard#visual_menu_option}
        '''
        if isinstance(ad_hoc_filtering_option, dict):
            ad_hoc_filtering_option = QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption(**ad_hoc_filtering_option)
        if isinstance(data_point_drill_up_down_option, dict):
            data_point_drill_up_down_option = QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption(**data_point_drill_up_down_option)
        if isinstance(data_point_menu_label_option, dict):
            data_point_menu_label_option = QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption(**data_point_menu_label_option)
        if isinstance(data_point_tooltip_option, dict):
            data_point_tooltip_option = QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption(**data_point_tooltip_option)
        if isinstance(export_to_csv_option, dict):
            export_to_csv_option = QuicksightDashboardDashboardPublishOptionsExportToCsvOption(**export_to_csv_option)
        if isinstance(export_with_hidden_fields_option, dict):
            export_with_hidden_fields_option = QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption(**export_with_hidden_fields_option)
        if isinstance(sheet_controls_option, dict):
            sheet_controls_option = QuicksightDashboardDashboardPublishOptionsSheetControlsOption(**sheet_controls_option)
        if isinstance(sheet_layout_element_maximization_option, dict):
            sheet_layout_element_maximization_option = QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption(**sheet_layout_element_maximization_option)
        if isinstance(visual_axis_sort_option, dict):
            visual_axis_sort_option = QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption(**visual_axis_sort_option)
        if isinstance(visual_menu_option, dict):
            visual_menu_option = QuicksightDashboardDashboardPublishOptionsVisualMenuOption(**visual_menu_option)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f170a515381f9399d2d541dfd60b64220904aadf3ff3ea262e00745d7c43a6)
            check_type(argname="argument ad_hoc_filtering_option", value=ad_hoc_filtering_option, expected_type=type_hints["ad_hoc_filtering_option"])
            check_type(argname="argument data_point_drill_up_down_option", value=data_point_drill_up_down_option, expected_type=type_hints["data_point_drill_up_down_option"])
            check_type(argname="argument data_point_menu_label_option", value=data_point_menu_label_option, expected_type=type_hints["data_point_menu_label_option"])
            check_type(argname="argument data_point_tooltip_option", value=data_point_tooltip_option, expected_type=type_hints["data_point_tooltip_option"])
            check_type(argname="argument export_to_csv_option", value=export_to_csv_option, expected_type=type_hints["export_to_csv_option"])
            check_type(argname="argument export_with_hidden_fields_option", value=export_with_hidden_fields_option, expected_type=type_hints["export_with_hidden_fields_option"])
            check_type(argname="argument sheet_controls_option", value=sheet_controls_option, expected_type=type_hints["sheet_controls_option"])
            check_type(argname="argument sheet_layout_element_maximization_option", value=sheet_layout_element_maximization_option, expected_type=type_hints["sheet_layout_element_maximization_option"])
            check_type(argname="argument visual_axis_sort_option", value=visual_axis_sort_option, expected_type=type_hints["visual_axis_sort_option"])
            check_type(argname="argument visual_menu_option", value=visual_menu_option, expected_type=type_hints["visual_menu_option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ad_hoc_filtering_option is not None:
            self._values["ad_hoc_filtering_option"] = ad_hoc_filtering_option
        if data_point_drill_up_down_option is not None:
            self._values["data_point_drill_up_down_option"] = data_point_drill_up_down_option
        if data_point_menu_label_option is not None:
            self._values["data_point_menu_label_option"] = data_point_menu_label_option
        if data_point_tooltip_option is not None:
            self._values["data_point_tooltip_option"] = data_point_tooltip_option
        if export_to_csv_option is not None:
            self._values["export_to_csv_option"] = export_to_csv_option
        if export_with_hidden_fields_option is not None:
            self._values["export_with_hidden_fields_option"] = export_with_hidden_fields_option
        if sheet_controls_option is not None:
            self._values["sheet_controls_option"] = sheet_controls_option
        if sheet_layout_element_maximization_option is not None:
            self._values["sheet_layout_element_maximization_option"] = sheet_layout_element_maximization_option
        if visual_axis_sort_option is not None:
            self._values["visual_axis_sort_option"] = visual_axis_sort_option
        if visual_menu_option is not None:
            self._values["visual_menu_option"] = visual_menu_option

    @builtins.property
    def ad_hoc_filtering_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption"]:
        '''ad_hoc_filtering_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#ad_hoc_filtering_option QuicksightDashboard#ad_hoc_filtering_option}
        '''
        result = self._values.get("ad_hoc_filtering_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption"], result)

    @builtins.property
    def data_point_drill_up_down_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption"]:
        '''data_point_drill_up_down_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_drill_up_down_option QuicksightDashboard#data_point_drill_up_down_option}
        '''
        result = self._values.get("data_point_drill_up_down_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption"], result)

    @builtins.property
    def data_point_menu_label_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption"]:
        '''data_point_menu_label_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_menu_label_option QuicksightDashboard#data_point_menu_label_option}
        '''
        result = self._values.get("data_point_menu_label_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption"], result)

    @builtins.property
    def data_point_tooltip_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption"]:
        '''data_point_tooltip_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_point_tooltip_option QuicksightDashboard#data_point_tooltip_option}
        '''
        result = self._values.get("data_point_tooltip_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption"], result)

    @builtins.property
    def export_to_csv_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsExportToCsvOption"]:
        '''export_to_csv_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#export_to_csv_option QuicksightDashboard#export_to_csv_option}
        '''
        result = self._values.get("export_to_csv_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsExportToCsvOption"], result)

    @builtins.property
    def export_with_hidden_fields_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption"]:
        '''export_with_hidden_fields_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#export_with_hidden_fields_option QuicksightDashboard#export_with_hidden_fields_option}
        '''
        result = self._values.get("export_with_hidden_fields_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption"], result)

    @builtins.property
    def sheet_controls_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"]:
        '''sheet_controls_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#sheet_controls_option QuicksightDashboard#sheet_controls_option}
        '''
        result = self._values.get("sheet_controls_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"], result)

    @builtins.property
    def sheet_layout_element_maximization_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"]:
        '''sheet_layout_element_maximization_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#sheet_layout_element_maximization_option QuicksightDashboard#sheet_layout_element_maximization_option}
        '''
        result = self._values.get("sheet_layout_element_maximization_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"], result)

    @builtins.property
    def visual_axis_sort_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"]:
        '''visual_axis_sort_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visual_axis_sort_option QuicksightDashboard#visual_axis_sort_option}
        '''
        result = self._values.get("visual_axis_sort_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"], result)

    @builtins.property
    def visual_menu_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"]:
        '''visual_menu_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visual_menu_option QuicksightDashboard#visual_menu_option}
        '''
        result = self._values.get("visual_menu_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2613bdfa8665d7153a9d846a698c4fb3fa1e779d60a18452b6ad970ce4418f)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b89a0d16bfbe2e7f1e1e8789374466d05830e76405c3279c9d15f7352655f9dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b0b5f8f70fe3d6ad1017305c53f4c3fe117486593f4abbe674e51006f199d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9208c5f389813ca0c0f0827a1a77a708057cc3eb7c224141dd02c64e141559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2485280f7dffc230e14823beca272229f50461f98759403f598e313b3f5b6c0)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e53613609827321e29c86b5c49239dc3b8f36a603fe6756bf1a7d9d56b8c715d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca0fa8f1cbf46b8d29d4e11f94df32ce0285eef44ff55679605a08a5ccf04c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff1d4b733fc31fb0c96775faaed61e66e5a64d7f1d7c6b133e21e321401429d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3613d0dfc6aa00d1f804909fc62b68839d621740b17e4582e34c8cce88b077)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d45d1b359aa5017feeccd40ea8ed0ed6c197df8486ed285ceed1ca7ec8459821)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33643a459ff8da79b6baf2c16e6def028f07cc36fc806fa16b65c161c477f68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8979c541ecc0e9674ae53cf07e69330e7850cf4aaec1c8a6c1fb4429fd2bab96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b460e3cb24617c0c24bc456896df0d12ba4d32032a419066b6777d2e0d22fd7a)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d9ffa7feb54d7472f625d2680ae0396ee7c0f4678a28830f96f03930ae4daf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4b0afed9ee7b8d75804fa97429e45f11e6eb6fd44e68abef639d7a28417860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3593e156d57517cfd11b9f71944dfa1c96fc12e925ae9e149d1fa1ffbb31464b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportToCsvOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsExportToCsvOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8367d68118412c6f84aa1bf4e322787cd5c50a1f2082c14766bb711d75f47bb8)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsExportToCsvOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__716562338a6938e13be6f0fbba6626e1e457c1932e1bc9819ec87dfdd3154e09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac8e1e1f182cf044b5340469625cb1923311097ecb2715eb4ef2486c237a114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b04700bd25168a8c3e4cd632ad792a87297312233d76ac06f224d37943527f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea1f783d2e42717f1a7067ff74d632dacb176dd6054a46bf46a98021f4aef62)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b969e08dc823364135c28148fe4e44c59220539af2ac01d9d7938343302e7ac5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63dfbd43d755082078d69131430157a493aea25dacc4ab9722f6f54cc22d8647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7e530f9adcc1cd7a93747f196f0b11257c58e4c45de708d61fbdcc6f9d6964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardDashboardPublishOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92ef915b9d3f9f0009806e3846ea0f3ed522ebec275f50055b167907c9f68c6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdHocFilteringOption")
    def put_ad_hoc_filtering_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putAdHocFilteringOption", [value]))

    @jsii.member(jsii_name="putDataPointDrillUpDownOption")
    def put_data_point_drill_up_down_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putDataPointDrillUpDownOption", [value]))

    @jsii.member(jsii_name="putDataPointMenuLabelOption")
    def put_data_point_menu_label_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putDataPointMenuLabelOption", [value]))

    @jsii.member(jsii_name="putDataPointTooltipOption")
    def put_data_point_tooltip_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putDataPointTooltipOption", [value]))

    @jsii.member(jsii_name="putExportToCsvOption")
    def put_export_to_csv_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsExportToCsvOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putExportToCsvOption", [value]))

    @jsii.member(jsii_name="putExportWithHiddenFieldsOption")
    def put_export_with_hidden_fields_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putExportWithHiddenFieldsOption", [value]))

    @jsii.member(jsii_name="putSheetControlsOption")
    def put_sheet_controls_option(
        self,
        *,
        visibility_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param visibility_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visibility_state QuicksightDashboard#visibility_state}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsSheetControlsOption(
            visibility_state=visibility_state
        )

        return typing.cast(None, jsii.invoke(self, "putSheetControlsOption", [value]))

    @jsii.member(jsii_name="putSheetLayoutElementMaximizationOption")
    def put_sheet_layout_element_maximization_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putSheetLayoutElementMaximizationOption", [value]))

    @jsii.member(jsii_name="putVisualAxisSortOption")
    def put_visual_axis_sort_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putVisualAxisSortOption", [value]))

    @jsii.member(jsii_name="putVisualMenuOption")
    def put_visual_menu_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsVisualMenuOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putVisualMenuOption", [value]))

    @jsii.member(jsii_name="resetAdHocFilteringOption")
    def reset_ad_hoc_filtering_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdHocFilteringOption", []))

    @jsii.member(jsii_name="resetDataPointDrillUpDownOption")
    def reset_data_point_drill_up_down_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPointDrillUpDownOption", []))

    @jsii.member(jsii_name="resetDataPointMenuLabelOption")
    def reset_data_point_menu_label_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPointMenuLabelOption", []))

    @jsii.member(jsii_name="resetDataPointTooltipOption")
    def reset_data_point_tooltip_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPointTooltipOption", []))

    @jsii.member(jsii_name="resetExportToCsvOption")
    def reset_export_to_csv_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToCsvOption", []))

    @jsii.member(jsii_name="resetExportWithHiddenFieldsOption")
    def reset_export_with_hidden_fields_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportWithHiddenFieldsOption", []))

    @jsii.member(jsii_name="resetSheetControlsOption")
    def reset_sheet_controls_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSheetControlsOption", []))

    @jsii.member(jsii_name="resetSheetLayoutElementMaximizationOption")
    def reset_sheet_layout_element_maximization_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSheetLayoutElementMaximizationOption", []))

    @jsii.member(jsii_name="resetVisualAxisSortOption")
    def reset_visual_axis_sort_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisualAxisSortOption", []))

    @jsii.member(jsii_name="resetVisualMenuOption")
    def reset_visual_menu_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisualMenuOption", []))

    @builtins.property
    @jsii.member(jsii_name="adHocFilteringOption")
    def ad_hoc_filtering_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference, jsii.get(self, "adHocFilteringOption"))

    @builtins.property
    @jsii.member(jsii_name="dataPointDrillUpDownOption")
    def data_point_drill_up_down_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference, jsii.get(self, "dataPointDrillUpDownOption"))

    @builtins.property
    @jsii.member(jsii_name="dataPointMenuLabelOption")
    def data_point_menu_label_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference, jsii.get(self, "dataPointMenuLabelOption"))

    @builtins.property
    @jsii.member(jsii_name="dataPointTooltipOption")
    def data_point_tooltip_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference, jsii.get(self, "dataPointTooltipOption"))

    @builtins.property
    @jsii.member(jsii_name="exportToCsvOption")
    def export_to_csv_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference, jsii.get(self, "exportToCsvOption"))

    @builtins.property
    @jsii.member(jsii_name="exportWithHiddenFieldsOption")
    def export_with_hidden_fields_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference, jsii.get(self, "exportWithHiddenFieldsOption"))

    @builtins.property
    @jsii.member(jsii_name="sheetControlsOption")
    def sheet_controls_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference", jsii.get(self, "sheetControlsOption"))

    @builtins.property
    @jsii.member(jsii_name="sheetLayoutElementMaximizationOption")
    def sheet_layout_element_maximization_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference", jsii.get(self, "sheetLayoutElementMaximizationOption"))

    @builtins.property
    @jsii.member(jsii_name="visualAxisSortOption")
    def visual_axis_sort_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference", jsii.get(self, "visualAxisSortOption"))

    @builtins.property
    @jsii.member(jsii_name="visualMenuOption")
    def visual_menu_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference", jsii.get(self, "visualMenuOption"))

    @builtins.property
    @jsii.member(jsii_name="adHocFilteringOptionInput")
    def ad_hoc_filtering_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption], jsii.get(self, "adHocFilteringOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPointDrillUpDownOptionInput")
    def data_point_drill_up_down_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption], jsii.get(self, "dataPointDrillUpDownOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPointMenuLabelOptionInput")
    def data_point_menu_label_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption], jsii.get(self, "dataPointMenuLabelOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPointTooltipOptionInput")
    def data_point_tooltip_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption], jsii.get(self, "dataPointTooltipOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToCsvOptionInput")
    def export_to_csv_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption], jsii.get(self, "exportToCsvOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="exportWithHiddenFieldsOptionInput")
    def export_with_hidden_fields_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption], jsii.get(self, "exportWithHiddenFieldsOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sheetControlsOptionInput")
    def sheet_controls_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"], jsii.get(self, "sheetControlsOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sheetLayoutElementMaximizationOptionInput")
    def sheet_layout_element_maximization_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"], jsii.get(self, "sheetLayoutElementMaximizationOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="visualAxisSortOptionInput")
    def visual_axis_sort_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"], jsii.get(self, "visualAxisSortOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="visualMenuOptionInput")
    def visual_menu_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"], jsii.get(self, "visualMenuOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptions]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274b70b315641279d44d696a2bc9c3bfa2d62e628fb02e15b6d75bb85f3c94b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetControlsOption",
    jsii_struct_bases=[],
    name_mapping={"visibility_state": "visibilityState"},
)
class QuicksightDashboardDashboardPublishOptionsSheetControlsOption:
    def __init__(
        self,
        *,
        visibility_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param visibility_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visibility_state QuicksightDashboard#visibility_state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11557a62d378a61358f6b60ee803e4ac9c7fcf4f6f775dab661a38192d162e87)
            check_type(argname="argument visibility_state", value=visibility_state, expected_type=type_hints["visibility_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if visibility_state is not None:
            self._values["visibility_state"] = visibility_state

    @builtins.property
    def visibility_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#visibility_state QuicksightDashboard#visibility_state}.'''
        result = self._values.get("visibility_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsSheetControlsOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cb563f32261d3775dcfef79b183304a6447956365b242a26bcff2509abbf52a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVisibilityState")
    def reset_visibility_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibilityState", []))

    @builtins.property
    @jsii.member(jsii_name="visibilityStateInput")
    def visibility_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityStateInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityState")
    def visibility_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibilityState"))

    @visibility_state.setter
    def visibility_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e2949afcb7e324d0cb05e4aa3fd037caaca0f3c37f572929b71df33c9d6d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibilityState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3f86816275fdd2aba0203b5b78a6475ad7cb87ba3a5d41ae8c670e502e3b56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70b814680390886f046f72b66b14935f29e26f4769b446bbe272c39bbef2a87)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44889362a9c956174a0915a7f825e2ee4358b602ef34e33926d87d12dffc7f0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5150f76284a653bd5c3366ed8d15232411f9d86930ac690b8690084913687e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f383086f5fb60643156a10232ff7b6fa050b54d19c7adf5a1e933e576e19f47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9460ed0526df21e52efee23557a4ccf19a6c818a861d287a78713addde95f2a1)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a6715451f79c644c6266f890f8d8d2350f2f3b3b654d54ff42253d74c9466e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f69c35507a46b0812427b1ada8c4fd3d8e906c02ce918c4ae53c9a39092397d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0f4734b6bb80cc10b9352f41925a898be4c1efc3da311086334c86cafa1c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualMenuOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsVisualMenuOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03074491a25d067744d284d65f94a920759f536e1f591dde0129c3d59225d64b)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsVisualMenuOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2def11dfd9c9094d9785279c49293969645365fe3b0ad3e24554277bd5ac6917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5568e829690ae2af9e1a093ef6cb37fc531c1e767f58e42e83a1eb804c7389b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37b8a8181e37d617239464f9cc92a0464e6754eeff0b25eaf9dc95c3f744ad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParameters",
    jsii_struct_bases=[],
    name_mapping={
        "date_time_parameters": "dateTimeParameters",
        "decimal_parameters": "decimalParameters",
        "integer_parameters": "integerParameters",
        "string_parameters": "stringParameters",
    },
)
class QuicksightDashboardParameters:
    def __init__(
        self,
        *,
        date_time_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDateTimeParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        decimal_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDecimalParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        integer_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersIntegerParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersStringParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param date_time_parameters: date_time_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#date_time_parameters QuicksightDashboard#date_time_parameters}
        :param decimal_parameters: decimal_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#decimal_parameters QuicksightDashboard#decimal_parameters}
        :param integer_parameters: integer_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#integer_parameters QuicksightDashboard#integer_parameters}
        :param string_parameters: string_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#string_parameters QuicksightDashboard#string_parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478346108de6548d464713f912ab1acbb869c1fea57e7bbfa631471138e985c8)
            check_type(argname="argument date_time_parameters", value=date_time_parameters, expected_type=type_hints["date_time_parameters"])
            check_type(argname="argument decimal_parameters", value=decimal_parameters, expected_type=type_hints["decimal_parameters"])
            check_type(argname="argument integer_parameters", value=integer_parameters, expected_type=type_hints["integer_parameters"])
            check_type(argname="argument string_parameters", value=string_parameters, expected_type=type_hints["string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_time_parameters is not None:
            self._values["date_time_parameters"] = date_time_parameters
        if decimal_parameters is not None:
            self._values["decimal_parameters"] = decimal_parameters
        if integer_parameters is not None:
            self._values["integer_parameters"] = integer_parameters
        if string_parameters is not None:
            self._values["string_parameters"] = string_parameters

    @builtins.property
    def date_time_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDateTimeParameters"]]]:
        '''date_time_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#date_time_parameters QuicksightDashboard#date_time_parameters}
        '''
        result = self._values.get("date_time_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDateTimeParameters"]]], result)

    @builtins.property
    def decimal_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDecimalParameters"]]]:
        '''decimal_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#decimal_parameters QuicksightDashboard#decimal_parameters}
        '''
        result = self._values.get("decimal_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDecimalParameters"]]], result)

    @builtins.property
    def integer_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersIntegerParameters"]]]:
        '''integer_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#integer_parameters QuicksightDashboard#integer_parameters}
        '''
        result = self._values.get("integer_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersIntegerParameters"]]], result)

    @builtins.property
    def string_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]]:
        '''string_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#string_parameters QuicksightDashboard#string_parameters}
        '''
        result = self._values.get("string_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersDateTimeParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersDateTimeParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ea3c38f723c7680c280d6a00811c66314303fbf2140778fe6e5c80eb13f1f7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersDateTimeParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersDateTimeParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersDateTimeParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd291bbf08fd4c8ac12ee2d3686555928359b043c929c245e1e2539d7606641)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersDateTimeParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a72c341c43c202bce12f49012b274b3cb8558f4285343f5dc8f0fdd58429d78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersDateTimeParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d3c5fa178cc02d28d903b6c9ff17ee90f5bfa36e7b440257a4215040524621)
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
            type_hints = typing.get_type_hints(_typecheckingstub__973178a40a368767aaa069b3f5022ba7b7db8cb07427347220d75f7e4a1e7bf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b7cabe9e97de8895e03ac7ce2dbb1001618c0d6134da50a023973f19603875b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e25f10f75c7f1cc4b1cd84eaa48a904189c9f5a235ec66d4e0805f6449fc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersDateTimeParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersDateTimeParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72e89ea01cc75ee069e6063a752937dfc089c138371e58b665476f8c810e9041)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5d8d94602dcf9f68a636e0182e01f5c6ac21086f4e2afc7519181bb48f4272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5510c071037dedcff422b32205fe93ce6039651fdb68c2599539db9ffa74e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd37463c6d7ff00061b39edb248c5b9054bbc6f87b01ed1fb738ea71e44b5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersDecimalParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersDecimalParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d59397d7604571d20133dafccbb7187d258d44cbebcb634fe49cc90bc9ed1e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersDecimalParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersDecimalParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersDecimalParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d163ef4b8d62ed1a744746fa8873e507bcb78eb21459b393634b29c95ce07036)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersDecimalParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b19dde1936102374353521bce68685438c92dd3c1a3fc8071b7eadbf320355)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersDecimalParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16f3a8618d40dab64418efe94bbc48cc2c8b129f37b5fc0e41d973b70c93247)
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
            type_hints = typing.get_type_hints(_typecheckingstub__947e77e4cb709445f80c50c13f1ec2a1fdb95defa4c8d5ee126032b324bceb6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6c3c06b1f6087cdae470346404694b1f3eb2b74f21b8c702cdb938b597f4723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f058b0c24242bc4e504e6e57f4551be99e7f43ff85927bdbaff5d395ea06af85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersDecimalParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersDecimalParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bada009e8eebfde8ae587ea9ac42d5693c3cb0464435513d4643ed39cc8820db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62280628bb5d8f83c0d04ce95c3c6c38453b7c7af3a3ab96d5f5621436ecf27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0724ab6ed644c14114bbcc26ac6182c06ebcea90737c9257397affcd523e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fd794de969f8163ec51b14aeefaf48aa3aa5627520649162c12c1ed7712041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersIntegerParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersIntegerParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057dae497491d09ae2ca11645434cea9086dda7d746575c5e85e05f8a534ba7b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersIntegerParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersIntegerParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersIntegerParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e52fc36bf4f8036b481a3cf9f49fbdd05edd3d20f0e86e06951f51d1f9e6a288)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersIntegerParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb227dab9fe770e3ef0f11776d2a3fa0513ad0d37b03541d9febba575a43b17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersIntegerParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd81339be82b0eedf613a0884cbadcaecc52887e89222db8029b77e639beccbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb89e095c1dd5128128fa0161dc85087a360bc62128cd36f0e498fe93c85dfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8fdde77a0d17e063f09155b79a338f8b3b1e8cd84968b77ad70a6eb0e1217c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af909419725639e347b7a95a5418ad6f330fed9a47693d2a6a8c45141c550c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersIntegerParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersIntegerParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e635cf5b50039f7c090ecec99bbf253b4f7572d207c1585928876f8b605c31d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e98a935b8959c5fcef316f85a286e707fdeec4db8ae7a82b3d3ca40de627ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c4c1cfd40fc4c2bfbdf7ed79d244b971cf43e6bdefd37144256e3620c8427a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8273ec0297c47b217e1a6ec924db8f2663ececa9d99846debb079e9b990a636e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b570f3f6dd3116e8b36cd73a018ea83db92827e103f75e7b9efdd2122527893)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDateTimeParameters")
    def put_date_time_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDateTimeParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b5b7d228589c57a2ec5952c848692b6655cb9719e9c561837d64dc4cbb2b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateTimeParameters", [value]))

    @jsii.member(jsii_name="putDecimalParameters")
    def put_decimal_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDecimalParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4bcd5f0a0e7779e16eef9008ae2eb27ee1cb4194dbf64b0869b0562ea34b59c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDecimalParameters", [value]))

    @jsii.member(jsii_name="putIntegerParameters")
    def put_integer_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersIntegerParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0740bc11e58c0738d324feefb01501533c98f47e4f51e7b7cb4c0f2cd55355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIntegerParameters", [value]))

    @jsii.member(jsii_name="putStringParameters")
    def put_string_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersStringParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f1ac47ccedc366f838c0f5ac3ddaf2419bc147bcefad82180824d0bc4936d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringParameters", [value]))

    @jsii.member(jsii_name="resetDateTimeParameters")
    def reset_date_time_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateTimeParameters", []))

    @jsii.member(jsii_name="resetDecimalParameters")
    def reset_decimal_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecimalParameters", []))

    @jsii.member(jsii_name="resetIntegerParameters")
    def reset_integer_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerParameters", []))

    @jsii.member(jsii_name="resetStringParameters")
    def reset_string_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringParameters", []))

    @builtins.property
    @jsii.member(jsii_name="dateTimeParameters")
    def date_time_parameters(
        self,
    ) -> QuicksightDashboardParametersDateTimeParametersList:
        return typing.cast(QuicksightDashboardParametersDateTimeParametersList, jsii.get(self, "dateTimeParameters"))

    @builtins.property
    @jsii.member(jsii_name="decimalParameters")
    def decimal_parameters(self) -> QuicksightDashboardParametersDecimalParametersList:
        return typing.cast(QuicksightDashboardParametersDecimalParametersList, jsii.get(self, "decimalParameters"))

    @builtins.property
    @jsii.member(jsii_name="integerParameters")
    def integer_parameters(self) -> QuicksightDashboardParametersIntegerParametersList:
        return typing.cast(QuicksightDashboardParametersIntegerParametersList, jsii.get(self, "integerParameters"))

    @builtins.property
    @jsii.member(jsii_name="stringParameters")
    def string_parameters(self) -> "QuicksightDashboardParametersStringParametersList":
        return typing.cast("QuicksightDashboardParametersStringParametersList", jsii.get(self, "stringParameters"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeParametersInput")
    def date_time_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]], jsii.get(self, "dateTimeParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="decimalParametersInput")
    def decimal_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]], jsii.get(self, "decimalParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="integerParametersInput")
    def integer_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]], jsii.get(self, "integerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="stringParametersInput")
    def string_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]], jsii.get(self, "stringParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDashboardParameters]:
        return typing.cast(typing.Optional[QuicksightDashboardParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2504fa01e3bfd39f75b2910d9aff92b5e9e4ca368236c0f1dd27da644568d08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersStringParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersStringParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de184a4481fa42475483c6951c359869159b7cc94682f9e70cbf877646a86cf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersStringParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersStringParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersStringParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22967a11dca014e8821965db3def14a7766528c2ecfbefa675119b7131cbdc85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersStringParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d03a56484aafed075a8041e82705006f916e8912eee69bb808a92ae7e309d8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersStringParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a76a8e0ea6997f5c3f12e183457cf900291cd42abe7909f3634d5c481cccbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14f2ad6abcdad0a0082ac864584a74b7d910c80efc40ed4a0d2c8a9eee6620d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e10229d2f6353e1bc8c70e847c2d040c16f2a8851b3cb9c1ed1e52926dc3330b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111b38e0a1ec48cbe4d7bb89ac3851cc4073f5a77164a769a3a1d3724369d106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersStringParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardParametersStringParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__984d08c03df02b10590cec9b7c1aa3d02323457cc4bf76b9a53e574b6a4ecad5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fcd33ea16dfe85d027ead4a3e7198a6012b22417c05be681ae578a0806edd91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c0a14d023d78fb174c01ae50417008352d97573df03c634b48d92e8dcfb1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af77bd21947982b4794c828e3487640a9eee1284fd1cecceb90be35564523d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardPermissions",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightDashboardPermissions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#actions QuicksightDashboard#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#principal QuicksightDashboard#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82c5daa33f44f99d7bf44521adb572eb73f76bf1f51beb4462de54fe8e5144f)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#actions QuicksightDashboard#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#principal QuicksightDashboard#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardPermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardPermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__175c7cf4da0cdd9c45ad55b958a6a9c0ba64e042b198532eeaaca68df395d795)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981717881292fd3104c66b81d9677375e65b965b1c53da0accd4bca847194b2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0af0111f47917ec36ebddc2818495829179a728027178da6edbfd7bff165fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cbbffff1339d81d166b98bcd992907b9be9066e9fe2bb5c19d8e7c4f2318501)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e72f4355ba5dc6217fd82cf757418eab2ca2166dcdedeedcf1cb7c09e7fbd471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf3de8fdbb651543d7777a7843bd91f1eebf8f01987445a28c8d4f3c2e5f7a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8b876a6754e934d02256452950c09d40f675f573c8dd301709c29b356e62c57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee44c4ebb94b70b59eb55022e97808cc7aa52e398d53bdb1e95f81ed5ec65361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57808b175082a559672bb2f303b5f66154750a3c38d5eaa9a9330b54a820fd99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c925905d6cd1be7701e2091b9c36762075b73298dbc539c6b1ef5868ed2a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntity",
    jsii_struct_bases=[],
    name_mapping={"source_template": "sourceTemplate"},
)
class QuicksightDashboardSourceEntity:
    def __init__(
        self,
        *,
        source_template: typing.Optional[typing.Union["QuicksightDashboardSourceEntitySourceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param source_template: source_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#source_template QuicksightDashboard#source_template}
        '''
        if isinstance(source_template, dict):
            source_template = QuicksightDashboardSourceEntitySourceTemplate(**source_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6f6c90f8c4ef23e7c185d7342c1b62d59ae295a5ed69f67e6ace06f517e543)
            check_type(argname="argument source_template", value=source_template, expected_type=type_hints["source_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_template is not None:
            self._values["source_template"] = source_template

    @builtins.property
    def source_template(
        self,
    ) -> typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"]:
        '''source_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#source_template QuicksightDashboard#source_template}
        '''
        result = self._values.get("source_template")
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardSourceEntity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardSourceEntityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92c292632c9ee9ee1cd190ad24f186bf2e7037ff9da9024e4183f178e482df7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSourceTemplate")
    def put_source_template(
        self,
        *,
        arn: builtins.str,
        data_set_references: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#arn QuicksightDashboard#arn}.
        :param data_set_references: data_set_references block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_set_references QuicksightDashboard#data_set_references}
        '''
        value = QuicksightDashboardSourceEntitySourceTemplate(
            arn=arn, data_set_references=data_set_references
        )

        return typing.cast(None, jsii.invoke(self, "putSourceTemplate", [value]))

    @jsii.member(jsii_name="resetSourceTemplate")
    def reset_source_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="sourceTemplate")
    def source_template(
        self,
    ) -> "QuicksightDashboardSourceEntitySourceTemplateOutputReference":
        return typing.cast("QuicksightDashboardSourceEntitySourceTemplateOutputReference", jsii.get(self, "sourceTemplate"))

    @builtins.property
    @jsii.member(jsii_name="sourceTemplateInput")
    def source_template_input(
        self,
    ) -> typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"]:
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"], jsii.get(self, "sourceTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDashboardSourceEntity]:
        return typing.cast(typing.Optional[QuicksightDashboardSourceEntity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardSourceEntity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043dae8ea193965964b1d25b82ca3a3ba2ec0f479e2403c4f7ff437e479b6c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplate",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "data_set_references": "dataSetReferences"},
)
class QuicksightDashboardSourceEntitySourceTemplate:
    def __init__(
        self,
        *,
        arn: builtins.str,
        data_set_references: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#arn QuicksightDashboard#arn}.
        :param data_set_references: data_set_references block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_set_references QuicksightDashboard#data_set_references}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846d82b572abae5a05f17991462916d2aab8140c197ed360ed0fdb3b229829f7)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument data_set_references", value=data_set_references, expected_type=type_hints["data_set_references"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "data_set_references": data_set_references,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#arn QuicksightDashboard#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_set_references(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences"]]:
        '''data_set_references block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_set_references QuicksightDashboard#data_set_references}
        '''
        result = self._values.get("data_set_references")
        assert result is not None, "Required property 'data_set_references' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardSourceEntitySourceTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateDataSetReferences",
    jsii_struct_bases=[],
    name_mapping={
        "data_set_arn": "dataSetArn",
        "data_set_placeholder": "dataSetPlaceholder",
    },
)
class QuicksightDashboardSourceEntitySourceTemplateDataSetReferences:
    def __init__(
        self,
        *,
        data_set_arn: builtins.str,
        data_set_placeholder: builtins.str,
    ) -> None:
        '''
        :param data_set_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_set_arn QuicksightDashboard#data_set_arn}.
        :param data_set_placeholder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_set_placeholder QuicksightDashboard#data_set_placeholder}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ac365679c95f625c1db363197e211119071c998661d9808cf6b38960e3acfa)
            check_type(argname="argument data_set_arn", value=data_set_arn, expected_type=type_hints["data_set_arn"])
            check_type(argname="argument data_set_placeholder", value=data_set_placeholder, expected_type=type_hints["data_set_placeholder"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_set_arn": data_set_arn,
            "data_set_placeholder": data_set_placeholder,
        }

    @builtins.property
    def data_set_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_set_arn QuicksightDashboard#data_set_arn}.'''
        result = self._values.get("data_set_arn")
        assert result is not None, "Required property 'data_set_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_set_placeholder(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#data_set_placeholder QuicksightDashboard#data_set_placeholder}.'''
        result = self._values.get("data_set_placeholder")
        assert result is not None, "Required property 'data_set_placeholder' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardSourceEntitySourceTemplateDataSetReferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff042d44deea82c3a61beab14994aec30fcd1d182a969689e42966e388a5cc3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142c926fee0809f2c1a1e2ed59d3d9a2e40666d22e932a692e31f786c1776638)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ce36874a5c68725bfa0a8ae6f2c07c7645137c311ed14ad792d7518f91e29a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f121f0a0fc4c5ad3cf18e8a79e14efe46df4ebf646e4b292f0984661ea3bdb66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__427c193aed0914231a29d8c08aab21370b57877b70ff87c5573ceafeccf41308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28aae1667b24ecc72083147c5247cc2eaaa1fe281a7352ec4e8588e4e3a96bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f3f7be9e95cf86db46ec98237648169dadf0d2897bef01b594b9a0ef944303)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataSetArnInput")
    def data_set_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetPlaceholderInput")
    def data_set_placeholder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetPlaceholderInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetArn")
    def data_set_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetArn"))

    @data_set_arn.setter
    def data_set_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d144109b4b049b7520a3da8112a78c99164a818026b441a6785e6648c241a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSetPlaceholder")
    def data_set_placeholder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetPlaceholder"))

    @data_set_placeholder.setter
    def data_set_placeholder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0729bf014cd1467ce197ba8906e8d4758a7f5d28c8fabe6306a4482c902dca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetPlaceholder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c42c98012afd4abbd9dffbed9bae5c365fb511f3cf1b3378ace68e79d504697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardSourceEntitySourceTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e4b547a7324333122547906daa8990bd2a7ff687b9978d8a9f0616ef334f64f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataSetReferences")
    def put_data_set_references(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd6db5143d0d3b938bc453244c97294f3036fb8ce833ba6050c87e32583f9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataSetReferences", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataSetReferences")
    def data_set_references(
        self,
    ) -> QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList:
        return typing.cast(QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList, jsii.get(self, "dataSetReferences"))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetReferencesInput")
    def data_set_references_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]], jsii.get(self, "dataSetReferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7325689af9e6d49da4edb03853f7971eb1c97afe076169d2177579564835fd5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardSourceEntitySourceTemplate]:
        return typing.cast(typing.Optional[QuicksightDashboardSourceEntitySourceTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardSourceEntitySourceTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2778e2622f643d37814597ad949a90e29d606240f405f99d1d11f62e4f44a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class QuicksightDashboardTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#create QuicksightDashboard#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#delete QuicksightDashboard#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#update QuicksightDashboard#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8aa81a353a21b2caf0930db1fc100fc8191f9683ff1335bc7c5ad8599627ae)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#create QuicksightDashboard#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#delete QuicksightDashboard#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_dashboard#update QuicksightDashboard#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDashboard.QuicksightDashboardTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__476fac4c053053bf42c452d0aa9bf06d4df5f187b831bb49fa1fa27b1dc45347)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fad482953490e63fc3d3170d76f54e01002e005628378e024ae599bfe58a5774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3ca12397e7ac5e6aa6104518d6544d7ed49183c37e5a175174aad60f94c488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa1fc607e14be77e1e4e8d4d2d2a860b3c6b287bb1ee4742619cdf589c6e47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db9706c26c8b29fbad552b21981c76ba992b65d4f8a6422e67f912b2baab280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightDashboard",
    "QuicksightDashboardConfig",
    "QuicksightDashboardDashboardPublishOptions",
    "QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption",
    "QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption",
    "QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption",
    "QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption",
    "QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsExportToCsvOption",
    "QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption",
    "QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsOutputReference",
    "QuicksightDashboardDashboardPublishOptionsSheetControlsOption",
    "QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption",
    "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption",
    "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsVisualMenuOption",
    "QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference",
    "QuicksightDashboardParameters",
    "QuicksightDashboardParametersDateTimeParameters",
    "QuicksightDashboardParametersDateTimeParametersList",
    "QuicksightDashboardParametersDateTimeParametersOutputReference",
    "QuicksightDashboardParametersDecimalParameters",
    "QuicksightDashboardParametersDecimalParametersList",
    "QuicksightDashboardParametersDecimalParametersOutputReference",
    "QuicksightDashboardParametersIntegerParameters",
    "QuicksightDashboardParametersIntegerParametersList",
    "QuicksightDashboardParametersIntegerParametersOutputReference",
    "QuicksightDashboardParametersOutputReference",
    "QuicksightDashboardParametersStringParameters",
    "QuicksightDashboardParametersStringParametersList",
    "QuicksightDashboardParametersStringParametersOutputReference",
    "QuicksightDashboardPermissions",
    "QuicksightDashboardPermissionsList",
    "QuicksightDashboardPermissionsOutputReference",
    "QuicksightDashboardSourceEntity",
    "QuicksightDashboardSourceEntityOutputReference",
    "QuicksightDashboardSourceEntitySourceTemplate",
    "QuicksightDashboardSourceEntitySourceTemplateDataSetReferences",
    "QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList",
    "QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference",
    "QuicksightDashboardSourceEntitySourceTemplateOutputReference",
    "QuicksightDashboardTimeouts",
    "QuicksightDashboardTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0142371e5ecafa09f1d7801393ac6f73c90ae54d5e083a55b63a13d2ee548170(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dashboard_id: builtins.str,
    name: builtins.str,
    version_description: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    dashboard_publish_options: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    definition: typing.Any = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[QuicksightDashboardParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_entity: typing.Optional[typing.Union[QuicksightDashboardSourceEntity, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    theme_arn: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[QuicksightDashboardTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__129cfb5758f57fec86ebb8d956d270025a674e435d260e1347f9a3da9c268df4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01b81f79d5eaf224102650dc797fc44d62a0b2cbd97a63e514487a77c6ea714(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardPermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95532f0d66eaae109434396f33762437469f8eb4a9be1c2621ca0afbf4ba592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef938f1586ebb043e694cdd848be4f9d6196894f419dcd7b7c5ee22d7ffdb17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20857df778db6d35870c1b0a98f20a2f0664ad0e2bc98dce0f455ec60a6045d(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e72e3a09b68789a747424f6e82517d456ce57b0c17080f40ced3e263870ec2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08aeb73c0bce5391f5f9933c434f8efad6ed33116a255bf61e5bc78c9171225(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382ffcd6441fd7b0cca276a108a445f2e1dc5dd70d26212b7e3f6a3d02731d61(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce8d348ecaadbd80d6787987ec19096168213b753fa56fd06ffbf85ba36270d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767d04bf3c4669d5d30a21335f94be9428e7c0cc259c83c9c4cb1355c3944969(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434a869f55e7cab11867bc2da111bf5eaa7a0abd4df78ea38fc4c8cc6765f6d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd2be5bd8c47f2242be9410fa55cbd7662770bc8faa40072f571609e9e94ab2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dashboard_id: builtins.str,
    name: builtins.str,
    version_description: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    dashboard_publish_options: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    definition: typing.Any = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[QuicksightDashboardParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_entity: typing.Optional[typing.Union[QuicksightDashboardSourceEntity, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    theme_arn: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[QuicksightDashboardTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f170a515381f9399d2d541dfd60b64220904aadf3ff3ea262e00745d7c43a6(
    *,
    ad_hoc_filtering_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption, typing.Dict[builtins.str, typing.Any]]] = None,
    data_point_drill_up_down_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption, typing.Dict[builtins.str, typing.Any]]] = None,
    data_point_menu_label_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption, typing.Dict[builtins.str, typing.Any]]] = None,
    data_point_tooltip_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption, typing.Dict[builtins.str, typing.Any]]] = None,
    export_to_csv_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsExportToCsvOption, typing.Dict[builtins.str, typing.Any]]] = None,
    export_with_hidden_fields_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption, typing.Dict[builtins.str, typing.Any]]] = None,
    sheet_controls_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsSheetControlsOption, typing.Dict[builtins.str, typing.Any]]] = None,
    sheet_layout_element_maximization_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption, typing.Dict[builtins.str, typing.Any]]] = None,
    visual_axis_sort_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption, typing.Dict[builtins.str, typing.Any]]] = None,
    visual_menu_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsVisualMenuOption, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2613bdfa8665d7153a9d846a698c4fb3fa1e779d60a18452b6ad970ce4418f(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89a0d16bfbe2e7f1e1e8789374466d05830e76405c3279c9d15f7352655f9dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b0b5f8f70fe3d6ad1017305c53f4c3fe117486593f4abbe674e51006f199d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9208c5f389813ca0c0f0827a1a77a708057cc3eb7c224141dd02c64e141559(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2485280f7dffc230e14823beca272229f50461f98759403f598e313b3f5b6c0(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53613609827321e29c86b5c49239dc3b8f36a603fe6756bf1a7d9d56b8c715d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca0fa8f1cbf46b8d29d4e11f94df32ce0285eef44ff55679605a08a5ccf04c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff1d4b733fc31fb0c96775faaed61e66e5a64d7f1d7c6b133e21e321401429d(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3613d0dfc6aa00d1f804909fc62b68839d621740b17e4582e34c8cce88b077(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45d1b359aa5017feeccd40ea8ed0ed6c197df8486ed285ceed1ca7ec8459821(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33643a459ff8da79b6baf2c16e6def028f07cc36fc806fa16b65c161c477f68d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8979c541ecc0e9674ae53cf07e69330e7850cf4aaec1c8a6c1fb4429fd2bab96(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b460e3cb24617c0c24bc456896df0d12ba4d32032a419066b6777d2e0d22fd7a(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9ffa7feb54d7472f625d2680ae0396ee7c0f4678a28830f96f03930ae4daf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4b0afed9ee7b8d75804fa97429e45f11e6eb6fd44e68abef639d7a28417860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3593e156d57517cfd11b9f71944dfa1c96fc12e925ae9e149d1fa1ffbb31464b(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8367d68118412c6f84aa1bf4e322787cd5c50a1f2082c14766bb711d75f47bb8(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716562338a6938e13be6f0fbba6626e1e457c1932e1bc9819ec87dfdd3154e09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac8e1e1f182cf044b5340469625cb1923311097ecb2715eb4ef2486c237a114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04700bd25168a8c3e4cd632ad792a87297312233d76ac06f224d37943527f3a(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea1f783d2e42717f1a7067ff74d632dacb176dd6054a46bf46a98021f4aef62(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b969e08dc823364135c28148fe4e44c59220539af2ac01d9d7938343302e7ac5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63dfbd43d755082078d69131430157a493aea25dacc4ab9722f6f54cc22d8647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7e530f9adcc1cd7a93747f196f0b11257c58e4c45de708d61fbdcc6f9d6964(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ef915b9d3f9f0009806e3846ea0f3ed522ebec275f50055b167907c9f68c6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274b70b315641279d44d696a2bc9c3bfa2d62e628fb02e15b6d75bb85f3c94b7(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11557a62d378a61358f6b60ee803e4ac9c7fcf4f6f775dab661a38192d162e87(
    *,
    visibility_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb563f32261d3775dcfef79b183304a6447956365b242a26bcff2509abbf52a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e2949afcb7e324d0cb05e4aa3fd037caaca0f3c37f572929b71df33c9d6d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3f86816275fdd2aba0203b5b78a6475ad7cb87ba3a5d41ae8c670e502e3b56(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70b814680390886f046f72b66b14935f29e26f4769b446bbe272c39bbef2a87(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44889362a9c956174a0915a7f825e2ee4358b602ef34e33926d87d12dffc7f0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5150f76284a653bd5c3366ed8d15232411f9d86930ac690b8690084913687e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f383086f5fb60643156a10232ff7b6fa050b54d19c7adf5a1e933e576e19f47a(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9460ed0526df21e52efee23557a4ccf19a6c818a861d287a78713addde95f2a1(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6715451f79c644c6266f890f8d8d2350f2f3b3b654d54ff42253d74c9466e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f69c35507a46b0812427b1ada8c4fd3d8e906c02ce918c4ae53c9a39092397d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0f4734b6bb80cc10b9352f41925a898be4c1efc3da311086334c86cafa1c2f(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03074491a25d067744d284d65f94a920759f536e1f591dde0129c3d59225d64b(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2def11dfd9c9094d9785279c49293969645365fe3b0ad3e24554277bd5ac6917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5568e829690ae2af9e1a093ef6cb37fc531c1e767f58e42e83a1eb804c7389b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37b8a8181e37d617239464f9cc92a0464e6754eeff0b25eaf9dc95c3f744ad5(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478346108de6548d464713f912ab1acbb869c1fea57e7bbfa631471138e985c8(
    *,
    date_time_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDateTimeParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    decimal_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDecimalParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    integer_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersIntegerParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersStringParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ea3c38f723c7680c280d6a00811c66314303fbf2140778fe6e5c80eb13f1f7(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd291bbf08fd4c8ac12ee2d3686555928359b043c929c245e1e2539d7606641(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a72c341c43c202bce12f49012b274b3cb8558f4285343f5dc8f0fdd58429d78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d3c5fa178cc02d28d903b6c9ff17ee90f5bfa36e7b440257a4215040524621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973178a40a368767aaa069b3f5022ba7b7db8cb07427347220d75f7e4a1e7bf9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7cabe9e97de8895e03ac7ce2dbb1001618c0d6134da50a023973f19603875b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e25f10f75c7f1cc4b1cd84eaa48a904189c9f5a235ec66d4e0805f6449fc30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e89ea01cc75ee069e6063a752937dfc089c138371e58b665476f8c810e9041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5d8d94602dcf9f68a636e0182e01f5c6ac21086f4e2afc7519181bb48f4272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5510c071037dedcff422b32205fe93ce6039651fdb68c2599539db9ffa74e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd37463c6d7ff00061b39edb248c5b9054bbc6f87b01ed1fb738ea71e44b5a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d59397d7604571d20133dafccbb7187d258d44cbebcb634fe49cc90bc9ed1e(
    *,
    name: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d163ef4b8d62ed1a744746fa8873e507bcb78eb21459b393634b29c95ce07036(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b19dde1936102374353521bce68685438c92dd3c1a3fc8071b7eadbf320355(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16f3a8618d40dab64418efe94bbc48cc2c8b129f37b5fc0e41d973b70c93247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947e77e4cb709445f80c50c13f1ec2a1fdb95defa4c8d5ee126032b324bceb6d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c3c06b1f6087cdae470346404694b1f3eb2b74f21b8c702cdb938b597f4723(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f058b0c24242bc4e504e6e57f4551be99e7f43ff85927bdbaff5d395ea06af85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bada009e8eebfde8ae587ea9ac42d5693c3cb0464435513d4643ed39cc8820db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62280628bb5d8f83c0d04ce95c3c6c38453b7c7af3a3ab96d5f5621436ecf27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0724ab6ed644c14114bbcc26ac6182c06ebcea90737c9257397affcd523e18(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fd794de969f8163ec51b14aeefaf48aa3aa5627520649162c12c1ed7712041(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057dae497491d09ae2ca11645434cea9086dda7d746575c5e85e05f8a534ba7b(
    *,
    name: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52fc36bf4f8036b481a3cf9f49fbdd05edd3d20f0e86e06951f51d1f9e6a288(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb227dab9fe770e3ef0f11776d2a3fa0513ad0d37b03541d9febba575a43b17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd81339be82b0eedf613a0884cbadcaecc52887e89222db8029b77e639beccbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb89e095c1dd5128128fa0161dc85087a360bc62128cd36f0e498fe93c85dfc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fdde77a0d17e063f09155b79a338f8b3b1e8cd84968b77ad70a6eb0e1217c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af909419725639e347b7a95a5418ad6f330fed9a47693d2a6a8c45141c550c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e635cf5b50039f7c090ecec99bbf253b4f7572d207c1585928876f8b605c31d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e98a935b8959c5fcef316f85a286e707fdeec4db8ae7a82b3d3ca40de627ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c4c1cfd40fc4c2bfbdf7ed79d244b971cf43e6bdefd37144256e3620c8427a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8273ec0297c47b217e1a6ec924db8f2663ececa9d99846debb079e9b990a636e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b570f3f6dd3116e8b36cd73a018ea83db92827e103f75e7b9efdd2122527893(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b5b7d228589c57a2ec5952c848692b6655cb9719e9c561837d64dc4cbb2b7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDateTimeParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bcd5f0a0e7779e16eef9008ae2eb27ee1cb4194dbf64b0869b0562ea34b59c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDecimalParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0740bc11e58c0738d324feefb01501533c98f47e4f51e7b7cb4c0f2cd55355(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersIntegerParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f1ac47ccedc366f838c0f5ac3ddaf2419bc147bcefad82180824d0bc4936d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersStringParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2504fa01e3bfd39f75b2910d9aff92b5e9e4ca368236c0f1dd27da644568d08c(
    value: typing.Optional[QuicksightDashboardParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de184a4481fa42475483c6951c359869159b7cc94682f9e70cbf877646a86cf(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22967a11dca014e8821965db3def14a7766528c2ecfbefa675119b7131cbdc85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d03a56484aafed075a8041e82705006f916e8912eee69bb808a92ae7e309d8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a76a8e0ea6997f5c3f12e183457cf900291cd42abe7909f3634d5c481cccbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f2ad6abcdad0a0082ac864584a74b7d910c80efc40ed4a0d2c8a9eee6620d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10229d2f6353e1bc8c70e847c2d040c16f2a8851b3cb9c1ed1e52926dc3330b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111b38e0a1ec48cbe4d7bb89ac3851cc4073f5a77164a769a3a1d3724369d106(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984d08c03df02b10590cec9b7c1aa3d02323457cc4bf76b9a53e574b6a4ecad5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcd33ea16dfe85d027ead4a3e7198a6012b22417c05be681ae578a0806edd91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c0a14d023d78fb174c01ae50417008352d97573df03c634b48d92e8dcfb1b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af77bd21947982b4794c828e3487640a9eee1284fd1cecceb90be35564523d1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82c5daa33f44f99d7bf44521adb572eb73f76bf1f51beb4462de54fe8e5144f(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175c7cf4da0cdd9c45ad55b958a6a9c0ba64e042b198532eeaaca68df395d795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981717881292fd3104c66b81d9677375e65b965b1c53da0accd4bca847194b2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0af0111f47917ec36ebddc2818495829179a728027178da6edbfd7bff165fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbbffff1339d81d166b98bcd992907b9be9066e9fe2bb5c19d8e7c4f2318501(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72f4355ba5dc6217fd82cf757418eab2ca2166dcdedeedcf1cb7c09e7fbd471(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf3de8fdbb651543d7777a7843bd91f1eebf8f01987445a28c8d4f3c2e5f7a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b876a6754e934d02256452950c09d40f675f573c8dd301709c29b356e62c57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee44c4ebb94b70b59eb55022e97808cc7aa52e398d53bdb1e95f81ed5ec65361(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57808b175082a559672bb2f303b5f66154750a3c38d5eaa9a9330b54a820fd99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c925905d6cd1be7701e2091b9c36762075b73298dbc539c6b1ef5868ed2a17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6f6c90f8c4ef23e7c185d7342c1b62d59ae295a5ed69f67e6ace06f517e543(
    *,
    source_template: typing.Optional[typing.Union[QuicksightDashboardSourceEntitySourceTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c292632c9ee9ee1cd190ad24f186bf2e7037ff9da9024e4183f178e482df7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043dae8ea193965964b1d25b82ca3a3ba2ec0f479e2403c4f7ff437e479b6c3e(
    value: typing.Optional[QuicksightDashboardSourceEntity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846d82b572abae5a05f17991462916d2aab8140c197ed360ed0fdb3b229829f7(
    *,
    arn: builtins.str,
    data_set_references: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ac365679c95f625c1db363197e211119071c998661d9808cf6b38960e3acfa(
    *,
    data_set_arn: builtins.str,
    data_set_placeholder: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff042d44deea82c3a61beab14994aec30fcd1d182a969689e42966e388a5cc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142c926fee0809f2c1a1e2ed59d3d9a2e40666d22e932a692e31f786c1776638(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ce36874a5c68725bfa0a8ae6f2c07c7645137c311ed14ad792d7518f91e29a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f121f0a0fc4c5ad3cf18e8a79e14efe46df4ebf646e4b292f0984661ea3bdb66(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427c193aed0914231a29d8c08aab21370b57877b70ff87c5573ceafeccf41308(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aae1667b24ecc72083147c5247cc2eaaa1fe281a7352ec4e8588e4e3a96bb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f3f7be9e95cf86db46ec98237648169dadf0d2897bef01b594b9a0ef944303(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d144109b4b049b7520a3da8112a78c99164a818026b441a6785e6648c241a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0729bf014cd1467ce197ba8906e8d4758a7f5d28c8fabe6306a4482c902dca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c42c98012afd4abbd9dffbed9bae5c365fb511f3cf1b3378ace68e79d504697(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4b547a7324333122547906daa8990bd2a7ff687b9978d8a9f0616ef334f64f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd6db5143d0d3b938bc453244c97294f3036fb8ce833ba6050c87e32583f9af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7325689af9e6d49da4edb03853f7971eb1c97afe076169d2177579564835fd5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2778e2622f643d37814597ad949a90e29d606240f405f99d1d11f62e4f44a12(
    value: typing.Optional[QuicksightDashboardSourceEntitySourceTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8aa81a353a21b2caf0930db1fc100fc8191f9683ff1335bc7c5ad8599627ae(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476fac4c053053bf42c452d0aa9bf06d4df5f187b831bb49fa1fa27b1dc45347(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad482953490e63fc3d3170d76f54e01002e005628378e024ae599bfe58a5774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3ca12397e7ac5e6aa6104518d6544d7ed49183c37e5a175174aad60f94c488(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa1fc607e14be77e1e4e8d4d2d2a860b3c6b287bb1ee4742619cdf589c6e47a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db9706c26c8b29fbad552b21981c76ba992b65d4f8a6422e67f912b2baab280(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
