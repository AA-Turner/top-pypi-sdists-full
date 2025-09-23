r'''
# `aws_quicksight_custom_permissions`

Refer to the Terraform Registry for docs: [`aws_quicksight_custom_permissions`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions).
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


class QuicksightCustomPermissions(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightCustomPermissions.QuicksightCustomPermissions",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions aws_quicksight_custom_permissions}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        custom_permissions_name: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightCustomPermissionsCapabilities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions aws_quicksight_custom_permissions} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param custom_permissions_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#custom_permissions_name QuicksightCustomPermissions#custom_permissions_name}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#aws_account_id QuicksightCustomPermissions#aws_account_id}.
        :param capabilities: capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#capabilities QuicksightCustomPermissions#capabilities}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#region QuicksightCustomPermissions#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#tags QuicksightCustomPermissions#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddf361c415cf562785ed3d19858cdeda23df01a493974ddca6b5d4453da7e19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = QuicksightCustomPermissionsConfig(
            custom_permissions_name=custom_permissions_name,
            aws_account_id=aws_account_id,
            capabilities=capabilities,
            region=region,
            tags=tags,
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
        '''Generates CDKTF code for importing a QuicksightCustomPermissions resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightCustomPermissions to import.
        :param import_from_id: The id of the existing QuicksightCustomPermissions that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightCustomPermissions to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de48f57726dcd1e5ad9028654275808aac620377cbf395e58643acc2504c01d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapabilities")
    def put_capabilities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightCustomPermissionsCapabilities", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713010ccab0db0efdf31556636ba2aa8436e8d8ab7a201a60ea6e3cb92707911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCapabilities", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetCapabilities")
    def reset_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapabilities", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> "QuicksightCustomPermissionsCapabilitiesList":
        return typing.cast("QuicksightCustomPermissionsCapabilitiesList", jsii.get(self, "capabilities"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilitiesInput")
    def capabilities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightCustomPermissionsCapabilities"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightCustomPermissionsCapabilities"]]], jsii.get(self, "capabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="customPermissionsNameInput")
    def custom_permissions_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPermissionsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080a6cfe510534ec6c42f07ae82a614fa11d6d2ca71791042f1c15be6a73e8a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPermissionsName")
    def custom_permissions_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPermissionsName"))

    @custom_permissions_name.setter
    def custom_permissions_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c4796db61d4fcf8e0a237abb03c09e4c14ab0dee9db490a6595667dc3261e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPermissionsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1d1eccb9ee64b36015cd79d658253a2b9ebb535cd823c59155c6b3245daa1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d39ccfc7e50ed9c41dd974dbabf67df3a69f7f807b212f0a785f01202e856d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightCustomPermissions.QuicksightCustomPermissionsCapabilities",
    jsii_struct_bases=[],
    name_mapping={
        "add_or_run_anomaly_detection_for_analyses": "addOrRunAnomalyDetectionForAnalyses",
        "create_and_update_dashboard_email_reports": "createAndUpdateDashboardEmailReports",
        "create_and_update_datasets": "createAndUpdateDatasets",
        "create_and_update_data_sources": "createAndUpdateDataSources",
        "create_and_update_themes": "createAndUpdateThemes",
        "create_and_update_threshold_alerts": "createAndUpdateThresholdAlerts",
        "create_shared_folders": "createSharedFolders",
        "create_spice_dataset": "createSpiceDataset",
        "export_to_csv": "exportToCsv",
        "export_to_csv_in_scheduled_reports": "exportToCsvInScheduledReports",
        "export_to_excel": "exportToExcel",
        "export_to_excel_in_scheduled_reports": "exportToExcelInScheduledReports",
        "export_to_pdf": "exportToPdf",
        "export_to_pdf_in_scheduled_reports": "exportToPdfInScheduledReports",
        "include_content_in_scheduled_reports_email": "includeContentInScheduledReportsEmail",
        "print_reports": "printReports",
        "rename_shared_folders": "renameSharedFolders",
        "share_analyses": "shareAnalyses",
        "share_dashboards": "shareDashboards",
        "share_datasets": "shareDatasets",
        "share_data_sources": "shareDataSources",
        "subscribe_dashboard_email_reports": "subscribeDashboardEmailReports",
        "view_account_spice_capacity": "viewAccountSpiceCapacity",
    },
)
class QuicksightCustomPermissionsCapabilities:
    def __init__(
        self,
        *,
        add_or_run_anomaly_detection_for_analyses: typing.Optional[builtins.str] = None,
        create_and_update_dashboard_email_reports: typing.Optional[builtins.str] = None,
        create_and_update_datasets: typing.Optional[builtins.str] = None,
        create_and_update_data_sources: typing.Optional[builtins.str] = None,
        create_and_update_themes: typing.Optional[builtins.str] = None,
        create_and_update_threshold_alerts: typing.Optional[builtins.str] = None,
        create_shared_folders: typing.Optional[builtins.str] = None,
        create_spice_dataset: typing.Optional[builtins.str] = None,
        export_to_csv: typing.Optional[builtins.str] = None,
        export_to_csv_in_scheduled_reports: typing.Optional[builtins.str] = None,
        export_to_excel: typing.Optional[builtins.str] = None,
        export_to_excel_in_scheduled_reports: typing.Optional[builtins.str] = None,
        export_to_pdf: typing.Optional[builtins.str] = None,
        export_to_pdf_in_scheduled_reports: typing.Optional[builtins.str] = None,
        include_content_in_scheduled_reports_email: typing.Optional[builtins.str] = None,
        print_reports: typing.Optional[builtins.str] = None,
        rename_shared_folders: typing.Optional[builtins.str] = None,
        share_analyses: typing.Optional[builtins.str] = None,
        share_dashboards: typing.Optional[builtins.str] = None,
        share_datasets: typing.Optional[builtins.str] = None,
        share_data_sources: typing.Optional[builtins.str] = None,
        subscribe_dashboard_email_reports: typing.Optional[builtins.str] = None,
        view_account_spice_capacity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param add_or_run_anomaly_detection_for_analyses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#add_or_run_anomaly_detection_for_analyses QuicksightCustomPermissions#add_or_run_anomaly_detection_for_analyses}.
        :param create_and_update_dashboard_email_reports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_dashboard_email_reports QuicksightCustomPermissions#create_and_update_dashboard_email_reports}.
        :param create_and_update_datasets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_datasets QuicksightCustomPermissions#create_and_update_datasets}.
        :param create_and_update_data_sources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_data_sources QuicksightCustomPermissions#create_and_update_data_sources}.
        :param create_and_update_themes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_themes QuicksightCustomPermissions#create_and_update_themes}.
        :param create_and_update_threshold_alerts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_threshold_alerts QuicksightCustomPermissions#create_and_update_threshold_alerts}.
        :param create_shared_folders: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_shared_folders QuicksightCustomPermissions#create_shared_folders}.
        :param create_spice_dataset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_spice_dataset QuicksightCustomPermissions#create_spice_dataset}.
        :param export_to_csv: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_csv QuicksightCustomPermissions#export_to_csv}.
        :param export_to_csv_in_scheduled_reports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_csv_in_scheduled_reports QuicksightCustomPermissions#export_to_csv_in_scheduled_reports}.
        :param export_to_excel: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_excel QuicksightCustomPermissions#export_to_excel}.
        :param export_to_excel_in_scheduled_reports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_excel_in_scheduled_reports QuicksightCustomPermissions#export_to_excel_in_scheduled_reports}.
        :param export_to_pdf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_pdf QuicksightCustomPermissions#export_to_pdf}.
        :param export_to_pdf_in_scheduled_reports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_pdf_in_scheduled_reports QuicksightCustomPermissions#export_to_pdf_in_scheduled_reports}.
        :param include_content_in_scheduled_reports_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#include_content_in_scheduled_reports_email QuicksightCustomPermissions#include_content_in_scheduled_reports_email}.
        :param print_reports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#print_reports QuicksightCustomPermissions#print_reports}.
        :param rename_shared_folders: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#rename_shared_folders QuicksightCustomPermissions#rename_shared_folders}.
        :param share_analyses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_analyses QuicksightCustomPermissions#share_analyses}.
        :param share_dashboards: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_dashboards QuicksightCustomPermissions#share_dashboards}.
        :param share_datasets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_datasets QuicksightCustomPermissions#share_datasets}.
        :param share_data_sources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_data_sources QuicksightCustomPermissions#share_data_sources}.
        :param subscribe_dashboard_email_reports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#subscribe_dashboard_email_reports QuicksightCustomPermissions#subscribe_dashboard_email_reports}.
        :param view_account_spice_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#view_account_spice_capacity QuicksightCustomPermissions#view_account_spice_capacity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2ce9d79d789ffa8c8a901b9a8ccb6612b7011d173da45f51b80617da5c8632)
            check_type(argname="argument add_or_run_anomaly_detection_for_analyses", value=add_or_run_anomaly_detection_for_analyses, expected_type=type_hints["add_or_run_anomaly_detection_for_analyses"])
            check_type(argname="argument create_and_update_dashboard_email_reports", value=create_and_update_dashboard_email_reports, expected_type=type_hints["create_and_update_dashboard_email_reports"])
            check_type(argname="argument create_and_update_datasets", value=create_and_update_datasets, expected_type=type_hints["create_and_update_datasets"])
            check_type(argname="argument create_and_update_data_sources", value=create_and_update_data_sources, expected_type=type_hints["create_and_update_data_sources"])
            check_type(argname="argument create_and_update_themes", value=create_and_update_themes, expected_type=type_hints["create_and_update_themes"])
            check_type(argname="argument create_and_update_threshold_alerts", value=create_and_update_threshold_alerts, expected_type=type_hints["create_and_update_threshold_alerts"])
            check_type(argname="argument create_shared_folders", value=create_shared_folders, expected_type=type_hints["create_shared_folders"])
            check_type(argname="argument create_spice_dataset", value=create_spice_dataset, expected_type=type_hints["create_spice_dataset"])
            check_type(argname="argument export_to_csv", value=export_to_csv, expected_type=type_hints["export_to_csv"])
            check_type(argname="argument export_to_csv_in_scheduled_reports", value=export_to_csv_in_scheduled_reports, expected_type=type_hints["export_to_csv_in_scheduled_reports"])
            check_type(argname="argument export_to_excel", value=export_to_excel, expected_type=type_hints["export_to_excel"])
            check_type(argname="argument export_to_excel_in_scheduled_reports", value=export_to_excel_in_scheduled_reports, expected_type=type_hints["export_to_excel_in_scheduled_reports"])
            check_type(argname="argument export_to_pdf", value=export_to_pdf, expected_type=type_hints["export_to_pdf"])
            check_type(argname="argument export_to_pdf_in_scheduled_reports", value=export_to_pdf_in_scheduled_reports, expected_type=type_hints["export_to_pdf_in_scheduled_reports"])
            check_type(argname="argument include_content_in_scheduled_reports_email", value=include_content_in_scheduled_reports_email, expected_type=type_hints["include_content_in_scheduled_reports_email"])
            check_type(argname="argument print_reports", value=print_reports, expected_type=type_hints["print_reports"])
            check_type(argname="argument rename_shared_folders", value=rename_shared_folders, expected_type=type_hints["rename_shared_folders"])
            check_type(argname="argument share_analyses", value=share_analyses, expected_type=type_hints["share_analyses"])
            check_type(argname="argument share_dashboards", value=share_dashboards, expected_type=type_hints["share_dashboards"])
            check_type(argname="argument share_datasets", value=share_datasets, expected_type=type_hints["share_datasets"])
            check_type(argname="argument share_data_sources", value=share_data_sources, expected_type=type_hints["share_data_sources"])
            check_type(argname="argument subscribe_dashboard_email_reports", value=subscribe_dashboard_email_reports, expected_type=type_hints["subscribe_dashboard_email_reports"])
            check_type(argname="argument view_account_spice_capacity", value=view_account_spice_capacity, expected_type=type_hints["view_account_spice_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_or_run_anomaly_detection_for_analyses is not None:
            self._values["add_or_run_anomaly_detection_for_analyses"] = add_or_run_anomaly_detection_for_analyses
        if create_and_update_dashboard_email_reports is not None:
            self._values["create_and_update_dashboard_email_reports"] = create_and_update_dashboard_email_reports
        if create_and_update_datasets is not None:
            self._values["create_and_update_datasets"] = create_and_update_datasets
        if create_and_update_data_sources is not None:
            self._values["create_and_update_data_sources"] = create_and_update_data_sources
        if create_and_update_themes is not None:
            self._values["create_and_update_themes"] = create_and_update_themes
        if create_and_update_threshold_alerts is not None:
            self._values["create_and_update_threshold_alerts"] = create_and_update_threshold_alerts
        if create_shared_folders is not None:
            self._values["create_shared_folders"] = create_shared_folders
        if create_spice_dataset is not None:
            self._values["create_spice_dataset"] = create_spice_dataset
        if export_to_csv is not None:
            self._values["export_to_csv"] = export_to_csv
        if export_to_csv_in_scheduled_reports is not None:
            self._values["export_to_csv_in_scheduled_reports"] = export_to_csv_in_scheduled_reports
        if export_to_excel is not None:
            self._values["export_to_excel"] = export_to_excel
        if export_to_excel_in_scheduled_reports is not None:
            self._values["export_to_excel_in_scheduled_reports"] = export_to_excel_in_scheduled_reports
        if export_to_pdf is not None:
            self._values["export_to_pdf"] = export_to_pdf
        if export_to_pdf_in_scheduled_reports is not None:
            self._values["export_to_pdf_in_scheduled_reports"] = export_to_pdf_in_scheduled_reports
        if include_content_in_scheduled_reports_email is not None:
            self._values["include_content_in_scheduled_reports_email"] = include_content_in_scheduled_reports_email
        if print_reports is not None:
            self._values["print_reports"] = print_reports
        if rename_shared_folders is not None:
            self._values["rename_shared_folders"] = rename_shared_folders
        if share_analyses is not None:
            self._values["share_analyses"] = share_analyses
        if share_dashboards is not None:
            self._values["share_dashboards"] = share_dashboards
        if share_datasets is not None:
            self._values["share_datasets"] = share_datasets
        if share_data_sources is not None:
            self._values["share_data_sources"] = share_data_sources
        if subscribe_dashboard_email_reports is not None:
            self._values["subscribe_dashboard_email_reports"] = subscribe_dashboard_email_reports
        if view_account_spice_capacity is not None:
            self._values["view_account_spice_capacity"] = view_account_spice_capacity

    @builtins.property
    def add_or_run_anomaly_detection_for_analyses(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#add_or_run_anomaly_detection_for_analyses QuicksightCustomPermissions#add_or_run_anomaly_detection_for_analyses}.'''
        result = self._values.get("add_or_run_anomaly_detection_for_analyses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_and_update_dashboard_email_reports(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_dashboard_email_reports QuicksightCustomPermissions#create_and_update_dashboard_email_reports}.'''
        result = self._values.get("create_and_update_dashboard_email_reports")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_and_update_datasets(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_datasets QuicksightCustomPermissions#create_and_update_datasets}.'''
        result = self._values.get("create_and_update_datasets")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_and_update_data_sources(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_data_sources QuicksightCustomPermissions#create_and_update_data_sources}.'''
        result = self._values.get("create_and_update_data_sources")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_and_update_themes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_themes QuicksightCustomPermissions#create_and_update_themes}.'''
        result = self._values.get("create_and_update_themes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_and_update_threshold_alerts(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_and_update_threshold_alerts QuicksightCustomPermissions#create_and_update_threshold_alerts}.'''
        result = self._values.get("create_and_update_threshold_alerts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_shared_folders(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_shared_folders QuicksightCustomPermissions#create_shared_folders}.'''
        result = self._values.get("create_shared_folders")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_spice_dataset(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#create_spice_dataset QuicksightCustomPermissions#create_spice_dataset}.'''
        result = self._values.get("create_spice_dataset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_to_csv(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_csv QuicksightCustomPermissions#export_to_csv}.'''
        result = self._values.get("export_to_csv")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_to_csv_in_scheduled_reports(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_csv_in_scheduled_reports QuicksightCustomPermissions#export_to_csv_in_scheduled_reports}.'''
        result = self._values.get("export_to_csv_in_scheduled_reports")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_to_excel(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_excel QuicksightCustomPermissions#export_to_excel}.'''
        result = self._values.get("export_to_excel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_to_excel_in_scheduled_reports(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_excel_in_scheduled_reports QuicksightCustomPermissions#export_to_excel_in_scheduled_reports}.'''
        result = self._values.get("export_to_excel_in_scheduled_reports")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_to_pdf(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_pdf QuicksightCustomPermissions#export_to_pdf}.'''
        result = self._values.get("export_to_pdf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_to_pdf_in_scheduled_reports(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#export_to_pdf_in_scheduled_reports QuicksightCustomPermissions#export_to_pdf_in_scheduled_reports}.'''
        result = self._values.get("export_to_pdf_in_scheduled_reports")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_content_in_scheduled_reports_email(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#include_content_in_scheduled_reports_email QuicksightCustomPermissions#include_content_in_scheduled_reports_email}.'''
        result = self._values.get("include_content_in_scheduled_reports_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def print_reports(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#print_reports QuicksightCustomPermissions#print_reports}.'''
        result = self._values.get("print_reports")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rename_shared_folders(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#rename_shared_folders QuicksightCustomPermissions#rename_shared_folders}.'''
        result = self._values.get("rename_shared_folders")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_analyses(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_analyses QuicksightCustomPermissions#share_analyses}.'''
        result = self._values.get("share_analyses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_dashboards(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_dashboards QuicksightCustomPermissions#share_dashboards}.'''
        result = self._values.get("share_dashboards")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_datasets(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_datasets QuicksightCustomPermissions#share_datasets}.'''
        result = self._values.get("share_datasets")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_data_sources(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#share_data_sources QuicksightCustomPermissions#share_data_sources}.'''
        result = self._values.get("share_data_sources")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscribe_dashboard_email_reports(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#subscribe_dashboard_email_reports QuicksightCustomPermissions#subscribe_dashboard_email_reports}.'''
        result = self._values.get("subscribe_dashboard_email_reports")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view_account_spice_capacity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#view_account_spice_capacity QuicksightCustomPermissions#view_account_spice_capacity}.'''
        result = self._values.get("view_account_spice_capacity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightCustomPermissionsCapabilities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightCustomPermissionsCapabilitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightCustomPermissions.QuicksightCustomPermissionsCapabilitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d9fc075943f85f5fd7455316a0bcfc1d9834c3d9c43bdc9fdbeac459e576a35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightCustomPermissionsCapabilitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139cd7cc77fce22f609b7ffdda8fd907377da7e7c3a1e7711c81109efde51e4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightCustomPermissionsCapabilitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6589c069b52a69f428b998c7483ea1faab3a206430fad2cecaee60ab1ba27c80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__734f99ad34fad16a5f3e058538cf87ae59cc6078747d8fea6cdedda50064bc59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ee385c02e00cb2eefea0fe353cbd05b7ec27d11aed38ab318e9cae15ef5d1c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightCustomPermissionsCapabilities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightCustomPermissionsCapabilities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightCustomPermissionsCapabilities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1808f30c0c6bb6720df926e58927a0039fbded28c23b3cf26276459b54799d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightCustomPermissionsCapabilitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightCustomPermissions.QuicksightCustomPermissionsCapabilitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adb9a186fb0e19002922968b869e4bf91feb1e0fac43ba268ef3ce4f34938430)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAddOrRunAnomalyDetectionForAnalyses")
    def reset_add_or_run_anomaly_detection_for_analyses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddOrRunAnomalyDetectionForAnalyses", []))

    @jsii.member(jsii_name="resetCreateAndUpdateDashboardEmailReports")
    def reset_create_and_update_dashboard_email_reports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateAndUpdateDashboardEmailReports", []))

    @jsii.member(jsii_name="resetCreateAndUpdateDatasets")
    def reset_create_and_update_datasets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateAndUpdateDatasets", []))

    @jsii.member(jsii_name="resetCreateAndUpdateDataSources")
    def reset_create_and_update_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateAndUpdateDataSources", []))

    @jsii.member(jsii_name="resetCreateAndUpdateThemes")
    def reset_create_and_update_themes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateAndUpdateThemes", []))

    @jsii.member(jsii_name="resetCreateAndUpdateThresholdAlerts")
    def reset_create_and_update_threshold_alerts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateAndUpdateThresholdAlerts", []))

    @jsii.member(jsii_name="resetCreateSharedFolders")
    def reset_create_shared_folders(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateSharedFolders", []))

    @jsii.member(jsii_name="resetCreateSpiceDataset")
    def reset_create_spice_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateSpiceDataset", []))

    @jsii.member(jsii_name="resetExportToCsv")
    def reset_export_to_csv(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToCsv", []))

    @jsii.member(jsii_name="resetExportToCsvInScheduledReports")
    def reset_export_to_csv_in_scheduled_reports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToCsvInScheduledReports", []))

    @jsii.member(jsii_name="resetExportToExcel")
    def reset_export_to_excel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToExcel", []))

    @jsii.member(jsii_name="resetExportToExcelInScheduledReports")
    def reset_export_to_excel_in_scheduled_reports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToExcelInScheduledReports", []))

    @jsii.member(jsii_name="resetExportToPdf")
    def reset_export_to_pdf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToPdf", []))

    @jsii.member(jsii_name="resetExportToPdfInScheduledReports")
    def reset_export_to_pdf_in_scheduled_reports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToPdfInScheduledReports", []))

    @jsii.member(jsii_name="resetIncludeContentInScheduledReportsEmail")
    def reset_include_content_in_scheduled_reports_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeContentInScheduledReportsEmail", []))

    @jsii.member(jsii_name="resetPrintReports")
    def reset_print_reports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrintReports", []))

    @jsii.member(jsii_name="resetRenameSharedFolders")
    def reset_rename_shared_folders(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenameSharedFolders", []))

    @jsii.member(jsii_name="resetShareAnalyses")
    def reset_share_analyses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareAnalyses", []))

    @jsii.member(jsii_name="resetShareDashboards")
    def reset_share_dashboards(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareDashboards", []))

    @jsii.member(jsii_name="resetShareDatasets")
    def reset_share_datasets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareDatasets", []))

    @jsii.member(jsii_name="resetShareDataSources")
    def reset_share_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareDataSources", []))

    @jsii.member(jsii_name="resetSubscribeDashboardEmailReports")
    def reset_subscribe_dashboard_email_reports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscribeDashboardEmailReports", []))

    @jsii.member(jsii_name="resetViewAccountSpiceCapacity")
    def reset_view_account_spice_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViewAccountSpiceCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="addOrRunAnomalyDetectionForAnalysesInput")
    def add_or_run_anomaly_detection_for_analyses_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addOrRunAnomalyDetectionForAnalysesInput"))

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateDashboardEmailReportsInput")
    def create_and_update_dashboard_email_reports_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createAndUpdateDashboardEmailReportsInput"))

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateDatasetsInput")
    def create_and_update_datasets_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createAndUpdateDatasetsInput"))

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateDataSourcesInput")
    def create_and_update_data_sources_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createAndUpdateDataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateThemesInput")
    def create_and_update_themes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createAndUpdateThemesInput"))

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateThresholdAlertsInput")
    def create_and_update_threshold_alerts_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createAndUpdateThresholdAlertsInput"))

    @builtins.property
    @jsii.member(jsii_name="createSharedFoldersInput")
    def create_shared_folders_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createSharedFoldersInput"))

    @builtins.property
    @jsii.member(jsii_name="createSpiceDatasetInput")
    def create_spice_dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createSpiceDatasetInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToCsvInput")
    def export_to_csv_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportToCsvInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToCsvInScheduledReportsInput")
    def export_to_csv_in_scheduled_reports_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportToCsvInScheduledReportsInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToExcelInput")
    def export_to_excel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportToExcelInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToExcelInScheduledReportsInput")
    def export_to_excel_in_scheduled_reports_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportToExcelInScheduledReportsInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToPdfInput")
    def export_to_pdf_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportToPdfInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToPdfInScheduledReportsInput")
    def export_to_pdf_in_scheduled_reports_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportToPdfInScheduledReportsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeContentInScheduledReportsEmailInput")
    def include_content_in_scheduled_reports_email_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeContentInScheduledReportsEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="printReportsInput")
    def print_reports_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "printReportsInput"))

    @builtins.property
    @jsii.member(jsii_name="renameSharedFoldersInput")
    def rename_shared_folders_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "renameSharedFoldersInput"))

    @builtins.property
    @jsii.member(jsii_name="shareAnalysesInput")
    def share_analyses_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareAnalysesInput"))

    @builtins.property
    @jsii.member(jsii_name="shareDashboardsInput")
    def share_dashboards_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareDashboardsInput"))

    @builtins.property
    @jsii.member(jsii_name="shareDatasetsInput")
    def share_datasets_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareDatasetsInput"))

    @builtins.property
    @jsii.member(jsii_name="shareDataSourcesInput")
    def share_data_sources_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareDataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="subscribeDashboardEmailReportsInput")
    def subscribe_dashboard_email_reports_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscribeDashboardEmailReportsInput"))

    @builtins.property
    @jsii.member(jsii_name="viewAccountSpiceCapacityInput")
    def view_account_spice_capacity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewAccountSpiceCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="addOrRunAnomalyDetectionForAnalyses")
    def add_or_run_anomaly_detection_for_analyses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addOrRunAnomalyDetectionForAnalyses"))

    @add_or_run_anomaly_detection_for_analyses.setter
    def add_or_run_anomaly_detection_for_analyses(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5eaabf0e5498e3d1c63b89c4f2f067499cd8c8f04c4877fb822fdaf2d37d929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addOrRunAnomalyDetectionForAnalyses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateDashboardEmailReports")
    def create_and_update_dashboard_email_reports(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createAndUpdateDashboardEmailReports"))

    @create_and_update_dashboard_email_reports.setter
    def create_and_update_dashboard_email_reports(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873d48a55f903d2ab7ec047eea6b6897a6103c5699c4341c55dc8220f340cd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAndUpdateDashboardEmailReports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateDatasets")
    def create_and_update_datasets(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createAndUpdateDatasets"))

    @create_and_update_datasets.setter
    def create_and_update_datasets(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc0946d4712e2f37acd70643d3e252bdaf86a50eff6b40142520af7f548df20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAndUpdateDatasets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateDataSources")
    def create_and_update_data_sources(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createAndUpdateDataSources"))

    @create_and_update_data_sources.setter
    def create_and_update_data_sources(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbeb99b6bfff2469b45a5bdafd5d97d588e486788289ba6910686395ad6961c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAndUpdateDataSources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateThemes")
    def create_and_update_themes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createAndUpdateThemes"))

    @create_and_update_themes.setter
    def create_and_update_themes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f877e3f10c862a51945fa9c2d9edef7702b15eeb7381233530e54d00fbfcf4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAndUpdateThemes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createAndUpdateThresholdAlerts")
    def create_and_update_threshold_alerts(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createAndUpdateThresholdAlerts"))

    @create_and_update_threshold_alerts.setter
    def create_and_update_threshold_alerts(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ab4926ad3009858693851c787fcf2700fdabbedc8920a4c04e0300232fc484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAndUpdateThresholdAlerts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createSharedFolders")
    def create_shared_folders(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createSharedFolders"))

    @create_shared_folders.setter
    def create_shared_folders(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b77ceee8bb50a5769bdcbc0f58ef658dab2c69aa73151ebacf09d18c057ae1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSharedFolders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createSpiceDataset")
    def create_spice_dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createSpiceDataset"))

    @create_spice_dataset.setter
    def create_spice_dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e905f5e346da44555fefe41ba9ef442484acb9a15fac07d7456ee13fe2021d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSpiceDataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportToCsv")
    def export_to_csv(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportToCsv"))

    @export_to_csv.setter
    def export_to_csv(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cb1a01372eda9c24ff018c7c4b07e86b19ead4083511bb495fb8572039023b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportToCsv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportToCsvInScheduledReports")
    def export_to_csv_in_scheduled_reports(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportToCsvInScheduledReports"))

    @export_to_csv_in_scheduled_reports.setter
    def export_to_csv_in_scheduled_reports(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe06f1d864a28a3f0b6ee1f1db7df5be468352c1ec132802b6cf3c9348b03e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportToCsvInScheduledReports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportToExcel")
    def export_to_excel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportToExcel"))

    @export_to_excel.setter
    def export_to_excel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc090f322351c7abb917bdf5afa9e22a786ec92c8f29a034c47e9d779f14fb00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportToExcel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportToExcelInScheduledReports")
    def export_to_excel_in_scheduled_reports(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportToExcelInScheduledReports"))

    @export_to_excel_in_scheduled_reports.setter
    def export_to_excel_in_scheduled_reports(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252505b025b2c318cfaee0d3e4e19f829009dedbe876d8abe1af96db26ec8608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportToExcelInScheduledReports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportToPdf")
    def export_to_pdf(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportToPdf"))

    @export_to_pdf.setter
    def export_to_pdf(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de7e5aa38911de0ca5c2fb3330873b5558d56a20ebe18488f668e2cb5e65d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportToPdf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportToPdfInScheduledReports")
    def export_to_pdf_in_scheduled_reports(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportToPdfInScheduledReports"))

    @export_to_pdf_in_scheduled_reports.setter
    def export_to_pdf_in_scheduled_reports(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c8956f9bc2bb1f044a2e0a046d5947a95faa9dcb67f6ede5e200ba6e9ec1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportToPdfInScheduledReports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeContentInScheduledReportsEmail")
    def include_content_in_scheduled_reports_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "includeContentInScheduledReportsEmail"))

    @include_content_in_scheduled_reports_email.setter
    def include_content_in_scheduled_reports_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36367a4abe175b246e150c657fa8902bb6f351baa4937e7d0009394b05bba1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeContentInScheduledReportsEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="printReports")
    def print_reports(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "printReports"))

    @print_reports.setter
    def print_reports(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8bb4af43813315c9528361adfc3e7102ada1e88cf544b627b17d3a88cdd9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "printReports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renameSharedFolders")
    def rename_shared_folders(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "renameSharedFolders"))

    @rename_shared_folders.setter
    def rename_shared_folders(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6315c3e00e2ed3ba0fca32ca118b3cf2b715cd6cc5b1df295cc532cd4b6aae3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renameSharedFolders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareAnalyses")
    def share_analyses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareAnalyses"))

    @share_analyses.setter
    def share_analyses(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc5a46c5a4c02741087bea2147f3a113e2e1366695f12bc37f5df101319707f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareAnalyses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareDashboards")
    def share_dashboards(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareDashboards"))

    @share_dashboards.setter
    def share_dashboards(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3704ef3c100497fa1d13472c9b27895fce04ee9d9e83cbd7b9b88cafe9c45115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareDashboards", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareDatasets")
    def share_datasets(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareDatasets"))

    @share_datasets.setter
    def share_datasets(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3275c58c651a28db0bfb1bc7e1c7fccf3c8ca460e5fe612c2a502f755783be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareDatasets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareDataSources")
    def share_data_sources(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareDataSources"))

    @share_data_sources.setter
    def share_data_sources(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5e9e6a1f7225c30d39d3930e820d8ea102137cec55534fea314c1221519af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareDataSources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscribeDashboardEmailReports")
    def subscribe_dashboard_email_reports(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscribeDashboardEmailReports"))

    @subscribe_dashboard_email_reports.setter
    def subscribe_dashboard_email_reports(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5859aead7e8ab7cf810eb1238f7e423469ec5187ef8054ae3024c6498f26a0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribeDashboardEmailReports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="viewAccountSpiceCapacity")
    def view_account_spice_capacity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "viewAccountSpiceCapacity"))

    @view_account_spice_capacity.setter
    def view_account_spice_capacity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b09f3eaa8e74e5212d3fdc8f3e85c1c5fc9c56a6f7f3d6c81dd8acda007cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewAccountSpiceCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightCustomPermissionsCapabilities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightCustomPermissionsCapabilities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightCustomPermissionsCapabilities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ce90783d2507f434d84ce9a930263cc258d4c69b0ff4ff0d6bac6f0320de64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightCustomPermissions.QuicksightCustomPermissionsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "custom_permissions_name": "customPermissionsName",
        "aws_account_id": "awsAccountId",
        "capabilities": "capabilities",
        "region": "region",
        "tags": "tags",
    },
)
class QuicksightCustomPermissionsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_permissions_name: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightCustomPermissionsCapabilities, typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param custom_permissions_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#custom_permissions_name QuicksightCustomPermissions#custom_permissions_name}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#aws_account_id QuicksightCustomPermissions#aws_account_id}.
        :param capabilities: capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#capabilities QuicksightCustomPermissions#capabilities}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#region QuicksightCustomPermissions#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#tags QuicksightCustomPermissions#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58cdebe38d47b783921a2aa94ce9f99d6ff313acdd485c69488efa98ee4afee)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument custom_permissions_name", value=custom_permissions_name, expected_type=type_hints["custom_permissions_name"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_permissions_name": custom_permissions_name,
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
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags

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
    def custom_permissions_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#custom_permissions_name QuicksightCustomPermissions#custom_permissions_name}.'''
        result = self._values.get("custom_permissions_name")
        assert result is not None, "Required property 'custom_permissions_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#aws_account_id QuicksightCustomPermissions#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capabilities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightCustomPermissionsCapabilities]]]:
        '''capabilities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#capabilities QuicksightCustomPermissions#capabilities}
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightCustomPermissionsCapabilities]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#region QuicksightCustomPermissions#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/quicksight_custom_permissions#tags QuicksightCustomPermissions#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightCustomPermissionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "QuicksightCustomPermissions",
    "QuicksightCustomPermissionsCapabilities",
    "QuicksightCustomPermissionsCapabilitiesList",
    "QuicksightCustomPermissionsCapabilitiesOutputReference",
    "QuicksightCustomPermissionsConfig",
]

publication.publish()

def _typecheckingstub__7ddf361c415cf562785ed3d19858cdeda23df01a493974ddca6b5d4453da7e19(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    custom_permissions_name: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightCustomPermissionsCapabilities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__2de48f57726dcd1e5ad9028654275808aac620377cbf395e58643acc2504c01d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713010ccab0db0efdf31556636ba2aa8436e8d8ab7a201a60ea6e3cb92707911(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightCustomPermissionsCapabilities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080a6cfe510534ec6c42f07ae82a614fa11d6d2ca71791042f1c15be6a73e8a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c4796db61d4fcf8e0a237abb03c09e4c14ab0dee9db490a6595667dc3261e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1d1eccb9ee64b36015cd79d658253a2b9ebb535cd823c59155c6b3245daa1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d39ccfc7e50ed9c41dd974dbabf67df3a69f7f807b212f0a785f01202e856d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2ce9d79d789ffa8c8a901b9a8ccb6612b7011d173da45f51b80617da5c8632(
    *,
    add_or_run_anomaly_detection_for_analyses: typing.Optional[builtins.str] = None,
    create_and_update_dashboard_email_reports: typing.Optional[builtins.str] = None,
    create_and_update_datasets: typing.Optional[builtins.str] = None,
    create_and_update_data_sources: typing.Optional[builtins.str] = None,
    create_and_update_themes: typing.Optional[builtins.str] = None,
    create_and_update_threshold_alerts: typing.Optional[builtins.str] = None,
    create_shared_folders: typing.Optional[builtins.str] = None,
    create_spice_dataset: typing.Optional[builtins.str] = None,
    export_to_csv: typing.Optional[builtins.str] = None,
    export_to_csv_in_scheduled_reports: typing.Optional[builtins.str] = None,
    export_to_excel: typing.Optional[builtins.str] = None,
    export_to_excel_in_scheduled_reports: typing.Optional[builtins.str] = None,
    export_to_pdf: typing.Optional[builtins.str] = None,
    export_to_pdf_in_scheduled_reports: typing.Optional[builtins.str] = None,
    include_content_in_scheduled_reports_email: typing.Optional[builtins.str] = None,
    print_reports: typing.Optional[builtins.str] = None,
    rename_shared_folders: typing.Optional[builtins.str] = None,
    share_analyses: typing.Optional[builtins.str] = None,
    share_dashboards: typing.Optional[builtins.str] = None,
    share_datasets: typing.Optional[builtins.str] = None,
    share_data_sources: typing.Optional[builtins.str] = None,
    subscribe_dashboard_email_reports: typing.Optional[builtins.str] = None,
    view_account_spice_capacity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9fc075943f85f5fd7455316a0bcfc1d9834c3d9c43bdc9fdbeac459e576a35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139cd7cc77fce22f609b7ffdda8fd907377da7e7c3a1e7711c81109efde51e4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6589c069b52a69f428b998c7483ea1faab3a206430fad2cecaee60ab1ba27c80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734f99ad34fad16a5f3e058538cf87ae59cc6078747d8fea6cdedda50064bc59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee385c02e00cb2eefea0fe353cbd05b7ec27d11aed38ab318e9cae15ef5d1c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1808f30c0c6bb6720df926e58927a0039fbded28c23b3cf26276459b54799d1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightCustomPermissionsCapabilities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb9a186fb0e19002922968b869e4bf91feb1e0fac43ba268ef3ce4f34938430(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5eaabf0e5498e3d1c63b89c4f2f067499cd8c8f04c4877fb822fdaf2d37d929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873d48a55f903d2ab7ec047eea6b6897a6103c5699c4341c55dc8220f340cd45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc0946d4712e2f37acd70643d3e252bdaf86a50eff6b40142520af7f548df20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbeb99b6bfff2469b45a5bdafd5d97d588e486788289ba6910686395ad6961c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f877e3f10c862a51945fa9c2d9edef7702b15eeb7381233530e54d00fbfcf4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ab4926ad3009858693851c787fcf2700fdabbedc8920a4c04e0300232fc484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b77ceee8bb50a5769bdcbc0f58ef658dab2c69aa73151ebacf09d18c057ae1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e905f5e346da44555fefe41ba9ef442484acb9a15fac07d7456ee13fe2021d15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cb1a01372eda9c24ff018c7c4b07e86b19ead4083511bb495fb8572039023b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe06f1d864a28a3f0b6ee1f1db7df5be468352c1ec132802b6cf3c9348b03e15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc090f322351c7abb917bdf5afa9e22a786ec92c8f29a034c47e9d779f14fb00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252505b025b2c318cfaee0d3e4e19f829009dedbe876d8abe1af96db26ec8608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de7e5aa38911de0ca5c2fb3330873b5558d56a20ebe18488f668e2cb5e65d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c8956f9bc2bb1f044a2e0a046d5947a95faa9dcb67f6ede5e200ba6e9ec1a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36367a4abe175b246e150c657fa8902bb6f351baa4937e7d0009394b05bba1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8bb4af43813315c9528361adfc3e7102ada1e88cf544b627b17d3a88cdd9b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6315c3e00e2ed3ba0fca32ca118b3cf2b715cd6cc5b1df295cc532cd4b6aae3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc5a46c5a4c02741087bea2147f3a113e2e1366695f12bc37f5df101319707f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3704ef3c100497fa1d13472c9b27895fce04ee9d9e83cbd7b9b88cafe9c45115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3275c58c651a28db0bfb1bc7e1c7fccf3c8ca460e5fe612c2a502f755783be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5e9e6a1f7225c30d39d3930e820d8ea102137cec55534fea314c1221519af2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5859aead7e8ab7cf810eb1238f7e423469ec5187ef8054ae3024c6498f26a0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b09f3eaa8e74e5212d3fdc8f3e85c1c5fc9c56a6f7f3d6c81dd8acda007cae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ce90783d2507f434d84ce9a930263cc258d4c69b0ff4ff0d6bac6f0320de64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightCustomPermissionsCapabilities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58cdebe38d47b783921a2aa94ce9f99d6ff313acdd485c69488efa98ee4afee(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_permissions_name: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightCustomPermissionsCapabilities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
