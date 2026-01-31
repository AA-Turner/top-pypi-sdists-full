"""
Type annotations for quicksight service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_quicksight.type_defs import APIKeyConnectionMetadataTypeDef

    data: APIKeyConnectionMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    ActionConnectorSearchFilterNameEnumType,
    ActionConnectorTypeType,
    AggTypeType,
    AnalysisErrorTypeType,
    AnalysisFilterAttributeType,
    ArcThicknessOptionsType,
    ArcThicknessType,
    AssetBundleExportFormatType,
    AssetBundleExportJobDataSetPropertyToOverrideType,
    AssetBundleExportJobDataSourcePropertyToOverrideType,
    AssetBundleExportJobFolderPropertyToOverrideType,
    AssetBundleExportJobStatusType,
    AssetBundleExportJobVPCConnectionPropertyToOverrideType,
    AssetBundleImportFailureActionType,
    AssetBundleImportJobStatusType,
    AssignmentStatusType,
    AuthenticationMethodOptionType,
    AuthenticationTypeType,
    AuthorSpecifiedAggregationType,
    AxisBindingType,
    BarChartOrientationType,
    BarsArrangementType,
    BaseMapStyleTypeType,
    BoxPlotFillStyleType,
    BrandStatusType,
    BrandVersionStatusType,
    CategoricalAggregationFunctionType,
    CategoryFilterFunctionType,
    CategoryFilterMatchOperatorType,
    CategoryFilterTypeType,
    ColorFillTypeType,
    ColumnDataRoleType,
    ColumnDataSubTypeType,
    ColumnDataTypeType,
    ColumnOrderingTypeType,
    ColumnRoleType,
    ColumnTagNameType,
    CommitModeType,
    ComparisonMethodType,
    ComparisonMethodTypeType,
    ConditionalFormattingIconSetTypeType,
    ConnectionAuthTypeType,
    ConstantTypeType,
    ContributionAnalysisDirectionType,
    ContributionAnalysisSortTypeType,
    CrossDatasetTypesType,
    CustomContentImageScalingConfigurationType,
    CustomContentTypeType,
    DashboardBehaviorType,
    DashboardCustomizationStatusType,
    DashboardErrorTypeType,
    DashboardFilterAttributeType,
    DashboardsQAStatusType,
    DashboardUIStateType,
    DataLabelContentType,
    DataLabelOverlapType,
    DataLabelPositionType,
    DataPrepSimpleAggregationFunctionTypeType,
    DataSetDateComparisonFilterOperatorType,
    DataSetFilterAttributeType,
    DataSetImportModeType,
    DataSetNumericComparisonFilterOperatorType,
    DatasetParameterValueTypeType,
    DataSetStringComparisonFilterOperatorType,
    DataSetStringListFilterOperatorType,
    DataSourceErrorInfoTypeType,
    DataSourceFilterAttributeType,
    DataSourceTypeType,
    DateAggregationFunctionType,
    DayOfTheWeekType,
    DayOfWeekType,
    DecalPatternTypeType,
    DecalStyleTypeType,
    DefaultAggregationType,
    DigitGroupingStyleType,
    DisplayFormatType,
    EditionType,
    EmbeddingIdentityTypeType,
    FieldNameType,
    FileFormatType,
    FilterClassType,
    FilterNullOptionType,
    FilterOperatorType,
    FilterVisualScopeType,
    FlowPublishStateType,
    FolderFilterAttributeType,
    FolderTypeType,
    FontDecorationType,
    FontStyleType,
    FontWeightNameType,
    ForecastComputationSeasonalityType,
    FunnelChartMeasureDataLabelStyleType,
    GeneratedAnswerStatusType,
    GeospatialColorStateType,
    GeoSpatialDataRoleType,
    GeospatialLayerTypeType,
    GeospatialMapNavigationType,
    GeospatialSelectedPointStyleType,
    HistogramBinTypeType,
    HorizontalTextAlignmentType,
    IconType,
    IdentityTypeType,
    ImageCustomActionTriggerType,
    IncludeFolderMembersType,
    IncludeGeneratedAnswerType,
    IncludeQuickSightQIndexType,
    IngestionErrorTypeType,
    IngestionRequestSourceType,
    IngestionRequestTypeType,
    IngestionStatusType,
    IngestionTypeType,
    InputColumnDataTypeType,
    JoinOperationTypeType,
    JoinTypeType,
    KPISparklineTypeType,
    KPIVisualStandardLayoutTypeType,
    LayerCustomActionTriggerType,
    LayoutElementTypeType,
    LegendPositionType,
    LineChartLineStyleType,
    LineChartMarkerShapeType,
    LineChartTypeType,
    LineInterpolationType,
    LookbackWindowSizeUnitType,
    MapZoomModeType,
    MaximumMinimumComputationTypeType,
    MemberTypeType,
    MissingDataTreatmentOptionType,
    NamedEntityAggTypeType,
    NamedFilterAggTypeType,
    NamedFilterTypeType,
    NamespaceErrorTypeType,
    NamespaceStatusType,
    NegativeValueDisplayModeType,
    NetworkInterfaceStatusType,
    NullFilterOptionType,
    NullFilterTypeType,
    NumberScaleType,
    NumericEqualityMatchOperatorType,
    NumericSeparatorSymbolType,
    OtherCategoriesType,
    PanelBorderStyleType,
    PaperOrientationType,
    PaperSizeType,
    ParameterValueTypeType,
    PersonalizationModeType,
    PivotTableConditionalFormattingScopeRoleType,
    PivotTableDataPathTypeType,
    PivotTableFieldCollapseStateType,
    PivotTableMetricPlacementType,
    PivotTableRowsLayoutType,
    PivotTableSubtotalLevelType,
    PluginVisualAxisNameType,
    PrimaryValueDisplayTypeType,
    PropertyRoleType,
    PropertyUsageType,
    PurchaseModeType,
    QAResultTypeType,
    QBusinessInsightsStatusType,
    QDataKeyTypeType,
    QSearchStatusType,
    QueryExecutionModeType,
    RadarChartAxesRangeScaleType,
    RadarChartShapeType,
    ReferenceLineLabelHorizontalPositionType,
    ReferenceLineLabelVerticalPositionType,
    ReferenceLinePatternTypeType,
    ReferenceLineSeriesTypeType,
    ReferenceLineValueLabelRelativePositionType,
    RefreshFailureAlertStatusType,
    RefreshIntervalType,
    RelativeDateTypeType,
    RelativeFontSizeType,
    ResizeOptionType,
    ResourceStatusType,
    ReviewedAnswerErrorCodeType,
    RoleType,
    RowLevelPermissionFormatVersionType,
    RowLevelPermissionPolicyType,
    SearchFilterOperatorType,
    SectionPageBreakStatusType,
    SelectedTooltipTypeType,
    SelfUpgradeAdminActionType,
    SelfUpgradeRequestStatusType,
    SelfUpgradeStatusType,
    ServiceTypeType,
    SharingModelType,
    SheetContentTypeType,
    SheetControlDateTimePickerTypeType,
    SheetControlListTypeType,
    SheetControlSliderTypeType,
    SheetImageScalingTypeType,
    SheetLayoutGroupMemberTypeType,
    SimpleNumericalAggregationFunctionType,
    SimpleTotalAggregationFunctionType,
    SmallMultiplesAxisPlacementType,
    SmallMultiplesAxisScaleType,
    SnapshotFileFormatTypeType,
    SnapshotFileSheetSelectionScopeType,
    SnapshotJobStatusType,
    SortDirectionType,
    SpecialValueType,
    StarburstProductTypeType,
    StatusType,
    StyledCellTypeType,
    TableBorderStyleType,
    TableCellImageScalingConfigurationType,
    TableOrientationType,
    TableTotalsPlacementType,
    TableTotalsScrollStatusType,
    TemplateErrorTypeType,
    TextQualifierType,
    TextWrapType,
    ThemeTypeType,
    TimeGranularityType,
    TooltipTargetType,
    TooltipTitleTypeType,
    TopBottomComputationTypeType,
    TopBottomSortOrderType,
    TopicFilterAttributeType,
    TopicFilterOperatorType,
    TopicIRFilterFunctionType,
    TopicIRFilterTypeType,
    TopicNumericSeparatorSymbolType,
    TopicRefreshStatusType,
    TopicRelativeDateFilterFunctionType,
    TopicScheduleTypeType,
    TopicSortDirectionType,
    TopicTimeGranularityType,
    TopicUserExperienceVersionType,
    TransposedColumnTypeType,
    UndefinedSpecifiedValueTypeType,
    URLTargetConfigurationType,
    UserRoleType,
    ValidationStrategyModeType,
    ValueWhenUnsetOptionType,
    VerticalTextAlignmentType,
    VisibilityType,
    VisualCustomActionTriggerType,
    VisualHighlightTriggerType,
    VisualRoleType,
    VPCConnectionAvailabilityStatusType,
    VPCConnectionResourceStatusType,
    WebCrawlerAuthTypeType,
    WidgetStatusType,
    WordCloudCloudLayoutType,
    WordCloudWordCasingType,
    WordCloudWordOrientationType,
    WordCloudWordPaddingType,
    WordCloudWordScalingType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "APIKeyConnectionMetadataTypeDef",
    "AccountCustomizationTypeDef",
    "AccountInfoTypeDef",
    "AccountSettingsTypeDef",
    "ActionConnectorErrorTypeDef",
    "ActionConnectorSearchFilterTypeDef",
    "ActionConnectorSummaryTypeDef",
    "ActionConnectorTypeDef",
    "ActiveIAMPolicyAssignmentTypeDef",
    "AdHocFilteringOptionTypeDef",
    "AggFunctionOutputTypeDef",
    "AggFunctionTypeDef",
    "AggFunctionUnionTypeDef",
    "AggregateOperationOutputTypeDef",
    "AggregateOperationTypeDef",
    "AggregationFunctionTypeDef",
    "AggregationPartitionByTypeDef",
    "AggregationSortConfigurationTypeDef",
    "AggregationTypeDef",
    "AmazonElasticsearchParametersTypeDef",
    "AmazonOpenSearchParametersTypeDef",
    "AmazonQInQuickSightConsoleConfigurationsTypeDef",
    "AmazonQInQuickSightDashboardConfigurationsTypeDef",
    "AnalysisDefaultsTypeDef",
    "AnalysisDefinitionOutputTypeDef",
    "AnalysisDefinitionTypeDef",
    "AnalysisDefinitionUnionTypeDef",
    "AnalysisErrorTypeDef",
    "AnalysisSearchFilterTypeDef",
    "AnalysisSourceEntityTypeDef",
    "AnalysisSourceTemplateTypeDef",
    "AnalysisSummaryTypeDef",
    "AnalysisTypeDef",
    "AnchorDateConfigurationTypeDef",
    "AnchorTypeDef",
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    "AnonymousUserDashboardFeatureConfigurationsTypeDef",
    "AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef",
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    "AnonymousUserGenerativeQnAEmbeddingConfigurationTypeDef",
    "AnonymousUserQSearchBarEmbeddingConfigurationTypeDef",
    "AnonymousUserSnapshotJobResultTypeDef",
    "AppendOperationOutputTypeDef",
    "AppendOperationTypeDef",
    "AppendedColumnTypeDef",
    "ApplicationThemeTypeDef",
    "ArcAxisConfigurationTypeDef",
    "ArcAxisDisplayRangeTypeDef",
    "ArcConfigurationTypeDef",
    "ArcOptionsTypeDef",
    "AssetBundleCloudFormationOverridePropertyConfigurationOutputTypeDef",
    "AssetBundleCloudFormationOverridePropertyConfigurationTypeDef",
    "AssetBundleCloudFormationOverridePropertyConfigurationUnionTypeDef",
    "AssetBundleExportJobAnalysisOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobAnalysisOverridePropertiesTypeDef",
    "AssetBundleExportJobDashboardOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobDashboardOverridePropertiesTypeDef",
    "AssetBundleExportJobDataSetOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobDataSetOverridePropertiesTypeDef",
    "AssetBundleExportJobDataSourceOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobDataSourceOverridePropertiesTypeDef",
    "AssetBundleExportJobErrorTypeDef",
    "AssetBundleExportJobFolderOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobFolderOverridePropertiesTypeDef",
    "AssetBundleExportJobRefreshScheduleOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef",
    "AssetBundleExportJobResourceIdOverrideConfigurationTypeDef",
    "AssetBundleExportJobSummaryTypeDef",
    "AssetBundleExportJobThemeOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobThemeOverridePropertiesTypeDef",
    "AssetBundleExportJobVPCConnectionOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef",
    "AssetBundleExportJobValidationStrategyTypeDef",
    "AssetBundleExportJobWarningTypeDef",
    "AssetBundleImportJobAnalysisOverrideParametersTypeDef",
    "AssetBundleImportJobAnalysisOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobAnalysisOverridePermissionsTypeDef",
    "AssetBundleImportJobAnalysisOverrideTagsOutputTypeDef",
    "AssetBundleImportJobAnalysisOverrideTagsTypeDef",
    "AssetBundleImportJobDashboardOverrideParametersTypeDef",
    "AssetBundleImportJobDashboardOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobDashboardOverridePermissionsTypeDef",
    "AssetBundleImportJobDashboardOverrideTagsOutputTypeDef",
    "AssetBundleImportJobDashboardOverrideTagsTypeDef",
    "AssetBundleImportJobDataSetOverrideParametersTypeDef",
    "AssetBundleImportJobDataSetOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobDataSetOverridePermissionsTypeDef",
    "AssetBundleImportJobDataSetOverrideTagsOutputTypeDef",
    "AssetBundleImportJobDataSetOverrideTagsTypeDef",
    "AssetBundleImportJobDataSourceCredentialPairTypeDef",
    "AssetBundleImportJobDataSourceCredentialsTypeDef",
    "AssetBundleImportJobDataSourceOverrideParametersOutputTypeDef",
    "AssetBundleImportJobDataSourceOverrideParametersTypeDef",
    "AssetBundleImportJobDataSourceOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobDataSourceOverridePermissionsTypeDef",
    "AssetBundleImportJobDataSourceOverrideTagsOutputTypeDef",
    "AssetBundleImportJobDataSourceOverrideTagsTypeDef",
    "AssetBundleImportJobErrorTypeDef",
    "AssetBundleImportJobFolderOverrideParametersTypeDef",
    "AssetBundleImportJobFolderOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobFolderOverridePermissionsTypeDef",
    "AssetBundleImportJobFolderOverrideTagsOutputTypeDef",
    "AssetBundleImportJobFolderOverrideTagsTypeDef",
    "AssetBundleImportJobOverrideParametersOutputTypeDef",
    "AssetBundleImportJobOverrideParametersTypeDef",
    "AssetBundleImportJobOverrideParametersUnionTypeDef",
    "AssetBundleImportJobOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobOverridePermissionsTypeDef",
    "AssetBundleImportJobOverridePermissionsUnionTypeDef",
    "AssetBundleImportJobOverrideTagsOutputTypeDef",
    "AssetBundleImportJobOverrideTagsTypeDef",
    "AssetBundleImportJobOverrideTagsUnionTypeDef",
    "AssetBundleImportJobOverrideValidationStrategyTypeDef",
    "AssetBundleImportJobRefreshScheduleOverrideParametersOutputTypeDef",
    "AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef",
    "AssetBundleImportJobResourceIdOverrideConfigurationTypeDef",
    "AssetBundleImportJobSummaryTypeDef",
    "AssetBundleImportJobThemeOverrideParametersTypeDef",
    "AssetBundleImportJobThemeOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobThemeOverridePermissionsTypeDef",
    "AssetBundleImportJobThemeOverrideTagsOutputTypeDef",
    "AssetBundleImportJobThemeOverrideTagsTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideParametersOutputTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideParametersTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideTagsOutputTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideTagsTypeDef",
    "AssetBundleImportJobWarningTypeDef",
    "AssetBundleImportSourceDescriptionTypeDef",
    "AssetBundleImportSourceTypeDef",
    "AssetBundleResourceLinkSharingConfigurationOutputTypeDef",
    "AssetBundleResourceLinkSharingConfigurationTypeDef",
    "AssetBundleResourcePermissionsOutputTypeDef",
    "AssetBundleResourcePermissionsTypeDef",
    "AssetOptionsOutputTypeDef",
    "AssetOptionsTypeDef",
    "AthenaParametersTypeDef",
    "AttributeAggregationFunctionTypeDef",
    "AuroraParametersTypeDef",
    "AuroraPostgreSqlParametersTypeDef",
    "AuthConfigTypeDef",
    "AuthenticationMetadataTypeDef",
    "AuthorizationCodeGrantCredentialsDetailsTypeDef",
    "AuthorizationCodeGrantDetailsTypeDef",
    "AuthorizationCodeGrantMetadataTypeDef",
    "AuthorizedTargetsByServiceTypeDef",
    "AwsIotAnalyticsParametersTypeDef",
    "AxisDataOptionsOutputTypeDef",
    "AxisDataOptionsTypeDef",
    "AxisDisplayMinMaxRangeTypeDef",
    "AxisDisplayOptionsOutputTypeDef",
    "AxisDisplayOptionsTypeDef",
    "AxisDisplayRangeOutputTypeDef",
    "AxisDisplayRangeTypeDef",
    "AxisLabelOptionsTypeDef",
    "AxisLabelReferenceOptionsTypeDef",
    "AxisLinearScaleTypeDef",
    "AxisLogarithmicScaleTypeDef",
    "AxisScaleTypeDef",
    "AxisTickLabelOptionsTypeDef",
    "BarChartAggregatedFieldWellsOutputTypeDef",
    "BarChartAggregatedFieldWellsTypeDef",
    "BarChartConfigurationOutputTypeDef",
    "BarChartConfigurationTypeDef",
    "BarChartDefaultSeriesSettingsTypeDef",
    "BarChartFieldWellsOutputTypeDef",
    "BarChartFieldWellsTypeDef",
    "BarChartSeriesSettingsTypeDef",
    "BarChartSortConfigurationOutputTypeDef",
    "BarChartSortConfigurationTypeDef",
    "BarChartVisualOutputTypeDef",
    "BarChartVisualTypeDef",
    "BarSeriesItemTypeDef",
    "BasicAuthConnectionMetadataTypeDef",
    "BatchCreateTopicReviewedAnswerRequestTypeDef",
    "BatchCreateTopicReviewedAnswerResponseTypeDef",
    "BatchDeleteTopicReviewedAnswerRequestTypeDef",
    "BatchDeleteTopicReviewedAnswerResponseTypeDef",
    "BigQueryParametersTypeDef",
    "BinCountOptionsTypeDef",
    "BinWidthOptionsTypeDef",
    "BlobTypeDef",
    "BodySectionConfigurationOutputTypeDef",
    "BodySectionConfigurationTypeDef",
    "BodySectionContentOutputTypeDef",
    "BodySectionContentTypeDef",
    "BodySectionDynamicCategoryDimensionConfigurationOutputTypeDef",
    "BodySectionDynamicCategoryDimensionConfigurationTypeDef",
    "BodySectionDynamicNumericDimensionConfigurationOutputTypeDef",
    "BodySectionDynamicNumericDimensionConfigurationTypeDef",
    "BodySectionRepeatConfigurationOutputTypeDef",
    "BodySectionRepeatConfigurationTypeDef",
    "BodySectionRepeatDimensionConfigurationOutputTypeDef",
    "BodySectionRepeatDimensionConfigurationTypeDef",
    "BodySectionRepeatPageBreakConfigurationTypeDef",
    "BookmarksConfigurationsTypeDef",
    "BorderSettingsTypeDef",
    "BorderStyleTypeDef",
    "BoxPlotAggregatedFieldWellsOutputTypeDef",
    "BoxPlotAggregatedFieldWellsTypeDef",
    "BoxPlotChartConfigurationOutputTypeDef",
    "BoxPlotChartConfigurationTypeDef",
    "BoxPlotFieldWellsOutputTypeDef",
    "BoxPlotFieldWellsTypeDef",
    "BoxPlotOptionsTypeDef",
    "BoxPlotSortConfigurationOutputTypeDef",
    "BoxPlotSortConfigurationTypeDef",
    "BoxPlotStyleOptionsTypeDef",
    "BoxPlotVisualOutputTypeDef",
    "BoxPlotVisualTypeDef",
    "BrandColorPaletteTypeDef",
    "BrandDefinitionTypeDef",
    "BrandDetailTypeDef",
    "BrandElementStyleTypeDef",
    "BrandSummaryTypeDef",
    "CalculatedColumnTypeDef",
    "CalculatedFieldTypeDef",
    "CalculatedMeasureFieldTypeDef",
    "CancelIngestionRequestTypeDef",
    "CancelIngestionResponseTypeDef",
    "CapabilitiesTypeDef",
    "CascadingControlConfigurationOutputTypeDef",
    "CascadingControlConfigurationTypeDef",
    "CascadingControlSourceTypeDef",
    "CastColumnTypeOperationTypeDef",
    "CastColumnTypesOperationOutputTypeDef",
    "CastColumnTypesOperationTypeDef",
    "CategoricalDimensionFieldTypeDef",
    "CategoricalMeasureFieldTypeDef",
    "CategoryDrillDownFilterOutputTypeDef",
    "CategoryDrillDownFilterTypeDef",
    "CategoryFilterConfigurationOutputTypeDef",
    "CategoryFilterConfigurationTypeDef",
    "CategoryFilterOutputTypeDef",
    "CategoryFilterTypeDef",
    "CategoryInnerFilterOutputTypeDef",
    "CategoryInnerFilterTypeDef",
    "CellValueSynonymOutputTypeDef",
    "CellValueSynonymTypeDef",
    "ChartAxisLabelOptionsOutputTypeDef",
    "ChartAxisLabelOptionsTypeDef",
    "ClientCredentialsDetailsTypeDef",
    "ClientCredentialsGrantDetailsTypeDef",
    "ClientCredentialsGrantMetadataTypeDef",
    "ClusterMarkerConfigurationTypeDef",
    "ClusterMarkerTypeDef",
    "CollectiveConstantEntryTypeDef",
    "CollectiveConstantOutputTypeDef",
    "CollectiveConstantTypeDef",
    "ColorScaleOutputTypeDef",
    "ColorScaleTypeDef",
    "ColorsConfigurationOutputTypeDef",
    "ColorsConfigurationTypeDef",
    "ColumnConfigurationOutputTypeDef",
    "ColumnConfigurationTypeDef",
    "ColumnDescriptionTypeDef",
    "ColumnGroupColumnSchemaTypeDef",
    "ColumnGroupOutputTypeDef",
    "ColumnGroupSchemaOutputTypeDef",
    "ColumnGroupSchemaTypeDef",
    "ColumnGroupTypeDef",
    "ColumnGroupUnionTypeDef",
    "ColumnHierarchyOutputTypeDef",
    "ColumnHierarchyTypeDef",
    "ColumnIdentifierTypeDef",
    "ColumnLevelPermissionRuleOutputTypeDef",
    "ColumnLevelPermissionRuleTypeDef",
    "ColumnLevelPermissionRuleUnionTypeDef",
    "ColumnSchemaTypeDef",
    "ColumnSortTypeDef",
    "ColumnTagTypeDef",
    "ColumnToUnpivotTypeDef",
    "ColumnTooltipItemTypeDef",
    "ComboChartAggregatedFieldWellsOutputTypeDef",
    "ComboChartAggregatedFieldWellsTypeDef",
    "ComboChartConfigurationOutputTypeDef",
    "ComboChartConfigurationTypeDef",
    "ComboChartDefaultSeriesSettingsTypeDef",
    "ComboChartFieldWellsOutputTypeDef",
    "ComboChartFieldWellsTypeDef",
    "ComboChartSeriesSettingsTypeDef",
    "ComboChartSortConfigurationOutputTypeDef",
    "ComboChartSortConfigurationTypeDef",
    "ComboChartVisualOutputTypeDef",
    "ComboChartVisualTypeDef",
    "ComboSeriesItemTypeDef",
    "ComparativeOrderOutputTypeDef",
    "ComparativeOrderTypeDef",
    "ComparisonConfigurationTypeDef",
    "ComparisonFormatConfigurationTypeDef",
    "ComputationTypeDef",
    "ConditionalFormattingColorOutputTypeDef",
    "ConditionalFormattingColorTypeDef",
    "ConditionalFormattingCustomIconConditionTypeDef",
    "ConditionalFormattingCustomIconOptionsTypeDef",
    "ConditionalFormattingGradientColorOutputTypeDef",
    "ConditionalFormattingGradientColorTypeDef",
    "ConditionalFormattingIconDisplayConfigurationTypeDef",
    "ConditionalFormattingIconSetTypeDef",
    "ConditionalFormattingIconTypeDef",
    "ConditionalFormattingSolidColorTypeDef",
    "ConfluenceParametersTypeDef",
    "ContextMenuOptionTypeDef",
    "ContextualAccentPaletteTypeDef",
    "ContributionAnalysisDefaultOutputTypeDef",
    "ContributionAnalysisDefaultTypeDef",
    "ContributionAnalysisFactorTypeDef",
    "ContributionAnalysisTimeRangesOutputTypeDef",
    "ContributionAnalysisTimeRangesTypeDef",
    "ContributionAnalysisTimeRangesUnionTypeDef",
    "CoordinateTypeDef",
    "CreateAccountCustomizationRequestTypeDef",
    "CreateAccountCustomizationResponseTypeDef",
    "CreateAccountSubscriptionRequestTypeDef",
    "CreateAccountSubscriptionResponseTypeDef",
    "CreateActionConnectorRequestTypeDef",
    "CreateActionConnectorResponseTypeDef",
    "CreateAnalysisRequestTypeDef",
    "CreateAnalysisResponseTypeDef",
    "CreateBrandRequestTypeDef",
    "CreateBrandResponseTypeDef",
    "CreateColumnsOperationOutputTypeDef",
    "CreateColumnsOperationTypeDef",
    "CreateColumnsOperationUnionTypeDef",
    "CreateCustomPermissionsRequestTypeDef",
    "CreateCustomPermissionsResponseTypeDef",
    "CreateDashboardRequestTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDataSetRequestTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateDataSourceRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFolderMembershipRequestTypeDef",
    "CreateFolderMembershipResponseTypeDef",
    "CreateFolderRequestTypeDef",
    "CreateFolderResponseTypeDef",
    "CreateGroupMembershipRequestTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "CreateGroupRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateIAMPolicyAssignmentRequestTypeDef",
    "CreateIAMPolicyAssignmentResponseTypeDef",
    "CreateIngestionRequestTypeDef",
    "CreateIngestionResponseTypeDef",
    "CreateNamespaceRequestTypeDef",
    "CreateNamespaceResponseTypeDef",
    "CreateRefreshScheduleRequestTypeDef",
    "CreateRefreshScheduleResponseTypeDef",
    "CreateRoleMembershipRequestTypeDef",
    "CreateRoleMembershipResponseTypeDef",
    "CreateTemplateAliasRequestTypeDef",
    "CreateTemplateAliasResponseTypeDef",
    "CreateTemplateRequestTypeDef",
    "CreateTemplateResponseTypeDef",
    "CreateThemeAliasRequestTypeDef",
    "CreateThemeAliasResponseTypeDef",
    "CreateThemeRequestTypeDef",
    "CreateThemeResponseTypeDef",
    "CreateTopicRefreshScheduleRequestTypeDef",
    "CreateTopicRefreshScheduleResponseTypeDef",
    "CreateTopicRequestTypeDef",
    "CreateTopicResponseTypeDef",
    "CreateTopicReviewedAnswerTypeDef",
    "CreateVPCConnectionRequestTypeDef",
    "CreateVPCConnectionResponseTypeDef",
    "CredentialPairTypeDef",
    "CurrencyDisplayFormatConfigurationTypeDef",
    "CustomActionFilterOperationOutputTypeDef",
    "CustomActionFilterOperationTypeDef",
    "CustomActionNavigationOperationTypeDef",
    "CustomActionSetParametersOperationOutputTypeDef",
    "CustomActionSetParametersOperationTypeDef",
    "CustomActionURLOperationTypeDef",
    "CustomColorTypeDef",
    "CustomConnectionParametersTypeDef",
    "CustomContentConfigurationTypeDef",
    "CustomContentVisualOutputTypeDef",
    "CustomContentVisualTypeDef",
    "CustomFilterConfigurationTypeDef",
    "CustomFilterListConfigurationOutputTypeDef",
    "CustomFilterListConfigurationTypeDef",
    "CustomInstructionsTypeDef",
    "CustomNarrativeOptionsTypeDef",
    "CustomParameterValuesOutputTypeDef",
    "CustomParameterValuesTypeDef",
    "CustomPermissionsTypeDef",
    "CustomSqlOutputTypeDef",
    "CustomSqlTypeDef",
    "CustomSqlUnionTypeDef",
    "CustomValuesConfigurationOutputTypeDef",
    "CustomValuesConfigurationTypeDef",
    "DashboardCustomizationVisualOptionsOutputTypeDef",
    "DashboardCustomizationVisualOptionsTypeDef",
    "DashboardErrorTypeDef",
    "DashboardPublishOptionsTypeDef",
    "DashboardSearchFilterTypeDef",
    "DashboardSourceEntityTypeDef",
    "DashboardSourceTemplateTypeDef",
    "DashboardSummaryTypeDef",
    "DashboardTypeDef",
    "DashboardVersionDefinitionOutputTypeDef",
    "DashboardVersionDefinitionTypeDef",
    "DashboardVersionDefinitionUnionTypeDef",
    "DashboardVersionSummaryTypeDef",
    "DashboardVersionTypeDef",
    "DashboardVisualIdTypeDef",
    "DashboardVisualPublishOptionsTypeDef",
    "DashboardVisualResultTypeDef",
    "DataAggregationTypeDef",
    "DataBarsOptionsTypeDef",
    "DataColorPaletteOutputTypeDef",
    "DataColorPaletteTypeDef",
    "DataColorTypeDef",
    "DataFieldBarSeriesItemTypeDef",
    "DataFieldComboSeriesItemTypeDef",
    "DataFieldSeriesItemTypeDef",
    "DataLabelOptionsOutputTypeDef",
    "DataLabelOptionsTypeDef",
    "DataLabelTypeTypeDef",
    "DataPathColorTypeDef",
    "DataPathLabelTypeTypeDef",
    "DataPathSortOutputTypeDef",
    "DataPathSortTypeDef",
    "DataPathTypeTypeDef",
    "DataPathValueTypeDef",
    "DataPointDrillUpDownOptionTypeDef",
    "DataPointMenuLabelOptionTypeDef",
    "DataPointTooltipOptionTypeDef",
    "DataPrepAggregationFunctionTypeDef",
    "DataPrepConfigurationOutputTypeDef",
    "DataPrepConfigurationTypeDef",
    "DataPrepConfigurationUnionTypeDef",
    "DataPrepListAggregationFunctionTypeDef",
    "DataPrepSimpleAggregationFunctionTypeDef",
    "DataQAEnabledOptionTypeDef",
    "DataQnAConfigurationsTypeDef",
    "DataSetColumnIdMappingTypeDef",
    "DataSetConfigurationOutputTypeDef",
    "DataSetConfigurationTypeDef",
    "DataSetDateComparisonFilterConditionOutputTypeDef",
    "DataSetDateComparisonFilterConditionTypeDef",
    "DataSetDateComparisonFilterConditionUnionTypeDef",
    "DataSetDateFilterConditionOutputTypeDef",
    "DataSetDateFilterConditionTypeDef",
    "DataSetDateFilterConditionUnionTypeDef",
    "DataSetDateFilterValueOutputTypeDef",
    "DataSetDateFilterValueTypeDef",
    "DataSetDateFilterValueUnionTypeDef",
    "DataSetDateRangeFilterConditionOutputTypeDef",
    "DataSetDateRangeFilterConditionTypeDef",
    "DataSetDateRangeFilterConditionUnionTypeDef",
    "DataSetIdentifierDeclarationTypeDef",
    "DataSetNumericComparisonFilterConditionTypeDef",
    "DataSetNumericFilterConditionTypeDef",
    "DataSetNumericFilterValueTypeDef",
    "DataSetNumericRangeFilterConditionTypeDef",
    "DataSetReferenceTypeDef",
    "DataSetRefreshPropertiesTypeDef",
    "DataSetSchemaOutputTypeDef",
    "DataSetSchemaTypeDef",
    "DataSetSearchFilterTypeDef",
    "DataSetStringComparisonFilterConditionTypeDef",
    "DataSetStringFilterConditionOutputTypeDef",
    "DataSetStringFilterConditionTypeDef",
    "DataSetStringFilterConditionUnionTypeDef",
    "DataSetStringFilterValueTypeDef",
    "DataSetStringListFilterConditionOutputTypeDef",
    "DataSetStringListFilterConditionTypeDef",
    "DataSetStringListFilterConditionUnionTypeDef",
    "DataSetStringListFilterValueOutputTypeDef",
    "DataSetStringListFilterValueTypeDef",
    "DataSetStringListFilterValueUnionTypeDef",
    "DataSetSummaryTypeDef",
    "DataSetTypeDef",
    "DataSetUsageConfigurationTypeDef",
    "DataSourceCredentialsTypeDef",
    "DataSourceErrorInfoTypeDef",
    "DataSourceParametersOutputTypeDef",
    "DataSourceParametersTypeDef",
    "DataSourceParametersUnionTypeDef",
    "DataSourceSearchFilterTypeDef",
    "DataSourceSummaryTypeDef",
    "DataSourceTypeDef",
    "DataStoriesConfigurationsTypeDef",
    "DataStoriesSharingOptionTypeDef",
    "DatabricksParametersTypeDef",
    "DatasetMetadataOutputTypeDef",
    "DatasetMetadataTypeDef",
    "DatasetParameterOutputTypeDef",
    "DatasetParameterTypeDef",
    "DatasetParameterUnionTypeDef",
    "DateAxisOptionsTypeDef",
    "DateDimensionFieldTypeDef",
    "DateMeasureFieldTypeDef",
    "DateTimeDatasetParameterDefaultValuesOutputTypeDef",
    "DateTimeDatasetParameterDefaultValuesTypeDef",
    "DateTimeDatasetParameterDefaultValuesUnionTypeDef",
    "DateTimeDatasetParameterOutputTypeDef",
    "DateTimeDatasetParameterTypeDef",
    "DateTimeDatasetParameterUnionTypeDef",
    "DateTimeDefaultValuesOutputTypeDef",
    "DateTimeDefaultValuesTypeDef",
    "DateTimeFormatConfigurationTypeDef",
    "DateTimeHierarchyOutputTypeDef",
    "DateTimeHierarchyTypeDef",
    "DateTimeParameterDeclarationOutputTypeDef",
    "DateTimeParameterDeclarationTypeDef",
    "DateTimeParameterOutputTypeDef",
    "DateTimeParameterTypeDef",
    "DateTimePickerControlDisplayOptionsTypeDef",
    "DateTimeValueWhenUnsetConfigurationOutputTypeDef",
    "DateTimeValueWhenUnsetConfigurationTypeDef",
    "DecalSettingsConfigurationOutputTypeDef",
    "DecalSettingsConfigurationTypeDef",
    "DecalSettingsTypeDef",
    "DecimalDatasetParameterDefaultValuesOutputTypeDef",
    "DecimalDatasetParameterDefaultValuesTypeDef",
    "DecimalDatasetParameterDefaultValuesUnionTypeDef",
    "DecimalDatasetParameterOutputTypeDef",
    "DecimalDatasetParameterTypeDef",
    "DecimalDatasetParameterUnionTypeDef",
    "DecimalDefaultValuesOutputTypeDef",
    "DecimalDefaultValuesTypeDef",
    "DecimalParameterDeclarationOutputTypeDef",
    "DecimalParameterDeclarationTypeDef",
    "DecimalParameterOutputTypeDef",
    "DecimalParameterTypeDef",
    "DecimalPlacesConfigurationTypeDef",
    "DecimalValueWhenUnsetConfigurationTypeDef",
    "DefaultDateTimePickerControlOptionsTypeDef",
    "DefaultFilterControlConfigurationOutputTypeDef",
    "DefaultFilterControlConfigurationTypeDef",
    "DefaultFilterControlOptionsOutputTypeDef",
    "DefaultFilterControlOptionsTypeDef",
    "DefaultFilterDropDownControlOptionsOutputTypeDef",
    "DefaultFilterDropDownControlOptionsTypeDef",
    "DefaultFilterListControlOptionsOutputTypeDef",
    "DefaultFilterListControlOptionsTypeDef",
    "DefaultFormattingTypeDef",
    "DefaultFreeFormLayoutConfigurationTypeDef",
    "DefaultGridLayoutConfigurationTypeDef",
    "DefaultInteractiveLayoutConfigurationTypeDef",
    "DefaultNewSheetConfigurationTypeDef",
    "DefaultPaginatedLayoutConfigurationTypeDef",
    "DefaultRelativeDateTimeControlOptionsTypeDef",
    "DefaultSectionBasedLayoutConfigurationTypeDef",
    "DefaultSliderControlOptionsTypeDef",
    "DefaultTextAreaControlOptionsTypeDef",
    "DefaultTextFieldControlOptionsTypeDef",
    "DeleteAccountCustomPermissionRequestTypeDef",
    "DeleteAccountCustomPermissionResponseTypeDef",
    "DeleteAccountCustomizationRequestTypeDef",
    "DeleteAccountCustomizationResponseTypeDef",
    "DeleteAccountSubscriptionRequestTypeDef",
    "DeleteAccountSubscriptionResponseTypeDef",
    "DeleteActionConnectorRequestTypeDef",
    "DeleteActionConnectorResponseTypeDef",
    "DeleteAnalysisRequestTypeDef",
    "DeleteAnalysisResponseTypeDef",
    "DeleteBrandAssignmentRequestTypeDef",
    "DeleteBrandAssignmentResponseTypeDef",
    "DeleteBrandRequestTypeDef",
    "DeleteBrandResponseTypeDef",
    "DeleteCustomPermissionsRequestTypeDef",
    "DeleteCustomPermissionsResponseTypeDef",
    "DeleteDashboardRequestTypeDef",
    "DeleteDashboardResponseTypeDef",
    "DeleteDataSetRefreshPropertiesRequestTypeDef",
    "DeleteDataSetRefreshPropertiesResponseTypeDef",
    "DeleteDataSetRequestTypeDef",
    "DeleteDataSetResponseTypeDef",
    "DeleteDataSourceRequestTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteDefaultQBusinessApplicationRequestTypeDef",
    "DeleteDefaultQBusinessApplicationResponseTypeDef",
    "DeleteFolderMembershipRequestTypeDef",
    "DeleteFolderMembershipResponseTypeDef",
    "DeleteFolderRequestTypeDef",
    "DeleteFolderResponseTypeDef",
    "DeleteGroupMembershipRequestTypeDef",
    "DeleteGroupMembershipResponseTypeDef",
    "DeleteGroupRequestTypeDef",
    "DeleteGroupResponseTypeDef",
    "DeleteIAMPolicyAssignmentRequestTypeDef",
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    "DeleteIdentityPropagationConfigRequestTypeDef",
    "DeleteIdentityPropagationConfigResponseTypeDef",
    "DeleteNamespaceRequestTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteRefreshScheduleRequestTypeDef",
    "DeleteRefreshScheduleResponseTypeDef",
    "DeleteRoleCustomPermissionRequestTypeDef",
    "DeleteRoleCustomPermissionResponseTypeDef",
    "DeleteRoleMembershipRequestTypeDef",
    "DeleteRoleMembershipResponseTypeDef",
    "DeleteTemplateAliasRequestTypeDef",
    "DeleteTemplateAliasResponseTypeDef",
    "DeleteTemplateRequestTypeDef",
    "DeleteTemplateResponseTypeDef",
    "DeleteThemeAliasRequestTypeDef",
    "DeleteThemeAliasResponseTypeDef",
    "DeleteThemeRequestTypeDef",
    "DeleteThemeResponseTypeDef",
    "DeleteTopicRefreshScheduleRequestTypeDef",
    "DeleteTopicRefreshScheduleResponseTypeDef",
    "DeleteTopicRequestTypeDef",
    "DeleteTopicResponseTypeDef",
    "DeleteUserByPrincipalIdRequestTypeDef",
    "DeleteUserByPrincipalIdResponseTypeDef",
    "DeleteUserCustomPermissionRequestTypeDef",
    "DeleteUserCustomPermissionResponseTypeDef",
    "DeleteUserRequestTypeDef",
    "DeleteUserResponseTypeDef",
    "DeleteVPCConnectionRequestTypeDef",
    "DeleteVPCConnectionResponseTypeDef",
    "DescribeAccountCustomPermissionRequestTypeDef",
    "DescribeAccountCustomPermissionResponseTypeDef",
    "DescribeAccountCustomizationRequestTypeDef",
    "DescribeAccountCustomizationResponseTypeDef",
    "DescribeAccountSettingsRequestTypeDef",
    "DescribeAccountSettingsResponseTypeDef",
    "DescribeAccountSubscriptionRequestTypeDef",
    "DescribeAccountSubscriptionResponseTypeDef",
    "DescribeActionConnectorPermissionsRequestTypeDef",
    "DescribeActionConnectorPermissionsResponseTypeDef",
    "DescribeActionConnectorRequestTypeDef",
    "DescribeActionConnectorResponseTypeDef",
    "DescribeAnalysisDefinitionRequestTypeDef",
    "DescribeAnalysisDefinitionResponseTypeDef",
    "DescribeAnalysisPermissionsRequestTypeDef",
    "DescribeAnalysisPermissionsResponseTypeDef",
    "DescribeAnalysisRequestTypeDef",
    "DescribeAnalysisResponseTypeDef",
    "DescribeAssetBundleExportJobRequestTypeDef",
    "DescribeAssetBundleExportJobResponseTypeDef",
    "DescribeAssetBundleImportJobRequestTypeDef",
    "DescribeAssetBundleImportJobResponseTypeDef",
    "DescribeBrandAssignmentRequestTypeDef",
    "DescribeBrandAssignmentResponseTypeDef",
    "DescribeBrandPublishedVersionRequestTypeDef",
    "DescribeBrandPublishedVersionResponseTypeDef",
    "DescribeBrandRequestTypeDef",
    "DescribeBrandResponseTypeDef",
    "DescribeCustomPermissionsRequestTypeDef",
    "DescribeCustomPermissionsResponseTypeDef",
    "DescribeDashboardDefinitionRequestTypeDef",
    "DescribeDashboardDefinitionResponseTypeDef",
    "DescribeDashboardPermissionsRequestTypeDef",
    "DescribeDashboardPermissionsResponseTypeDef",
    "DescribeDashboardRequestTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeDashboardSnapshotJobRequestTypeDef",
    "DescribeDashboardSnapshotJobResponseTypeDef",
    "DescribeDashboardSnapshotJobResultRequestTypeDef",
    "DescribeDashboardSnapshotJobResultResponseTypeDef",
    "DescribeDashboardsQAConfigurationRequestTypeDef",
    "DescribeDashboardsQAConfigurationResponseTypeDef",
    "DescribeDataSetPermissionsRequestTypeDef",
    "DescribeDataSetPermissionsResponseTypeDef",
    "DescribeDataSetRefreshPropertiesRequestTypeDef",
    "DescribeDataSetRefreshPropertiesResponseTypeDef",
    "DescribeDataSetRequestTypeDef",
    "DescribeDataSetResponseTypeDef",
    "DescribeDataSourcePermissionsRequestTypeDef",
    "DescribeDataSourcePermissionsResponseTypeDef",
    "DescribeDataSourceRequestTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "DescribeDefaultQBusinessApplicationRequestTypeDef",
    "DescribeDefaultQBusinessApplicationResponseTypeDef",
    "DescribeFolderPermissionsRequestPaginateTypeDef",
    "DescribeFolderPermissionsRequestTypeDef",
    "DescribeFolderPermissionsResponseTypeDef",
    "DescribeFolderRequestTypeDef",
    "DescribeFolderResolvedPermissionsRequestPaginateTypeDef",
    "DescribeFolderResolvedPermissionsRequestTypeDef",
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    "DescribeFolderResponseTypeDef",
    "DescribeGroupMembershipRequestTypeDef",
    "DescribeGroupMembershipResponseTypeDef",
    "DescribeGroupRequestTypeDef",
    "DescribeGroupResponseTypeDef",
    "DescribeIAMPolicyAssignmentRequestTypeDef",
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    "DescribeIngestionRequestTypeDef",
    "DescribeIngestionResponseTypeDef",
    "DescribeIpRestrictionRequestTypeDef",
    "DescribeIpRestrictionResponseTypeDef",
    "DescribeKeyRegistrationRequestTypeDef",
    "DescribeKeyRegistrationResponseTypeDef",
    "DescribeNamespaceRequestTypeDef",
    "DescribeNamespaceResponseTypeDef",
    "DescribeQPersonalizationConfigurationRequestTypeDef",
    "DescribeQPersonalizationConfigurationResponseTypeDef",
    "DescribeQuickSightQSearchConfigurationRequestTypeDef",
    "DescribeQuickSightQSearchConfigurationResponseTypeDef",
    "DescribeRefreshScheduleRequestTypeDef",
    "DescribeRefreshScheduleResponseTypeDef",
    "DescribeRoleCustomPermissionRequestTypeDef",
    "DescribeRoleCustomPermissionResponseTypeDef",
    "DescribeSelfUpgradeConfigurationRequestTypeDef",
    "DescribeSelfUpgradeConfigurationResponseTypeDef",
    "DescribeTemplateAliasRequestTypeDef",
    "DescribeTemplateAliasResponseTypeDef",
    "DescribeTemplateDefinitionRequestTypeDef",
    "DescribeTemplateDefinitionResponseTypeDef",
    "DescribeTemplatePermissionsRequestTypeDef",
    "DescribeTemplatePermissionsResponseTypeDef",
    "DescribeTemplateRequestTypeDef",
    "DescribeTemplateResponseTypeDef",
    "DescribeThemeAliasRequestTypeDef",
    "DescribeThemeAliasResponseTypeDef",
    "DescribeThemePermissionsRequestTypeDef",
    "DescribeThemePermissionsResponseTypeDef",
    "DescribeThemeRequestTypeDef",
    "DescribeThemeResponseTypeDef",
    "DescribeTopicPermissionsRequestTypeDef",
    "DescribeTopicPermissionsResponseTypeDef",
    "DescribeTopicRefreshRequestTypeDef",
    "DescribeTopicRefreshResponseTypeDef",
    "DescribeTopicRefreshScheduleRequestTypeDef",
    "DescribeTopicRefreshScheduleResponseTypeDef",
    "DescribeTopicRequestTypeDef",
    "DescribeTopicResponseTypeDef",
    "DescribeUserRequestTypeDef",
    "DescribeUserResponseTypeDef",
    "DescribeVPCConnectionRequestTypeDef",
    "DescribeVPCConnectionResponseTypeDef",
    "DestinationParameterValueConfigurationOutputTypeDef",
    "DestinationParameterValueConfigurationTypeDef",
    "DestinationTableSourceTypeDef",
    "DestinationTableTypeDef",
    "DimensionFieldTypeDef",
    "DisplayFormatOptionsTypeDef",
    "DonutCenterOptionsTypeDef",
    "DonutOptionsTypeDef",
    "DrillDownFilterOutputTypeDef",
    "DrillDownFilterTypeDef",
    "DropDownControlDisplayOptionsTypeDef",
    "DynamicDefaultValueTypeDef",
    "EmptyVisualOutputTypeDef",
    "EmptyVisualTypeDef",
    "EntityTypeDef",
    "ErrorInfoTypeDef",
    "ExasolParametersTypeDef",
    "ExcludePeriodConfigurationTypeDef",
    "ExecutiveSummaryConfigurationsTypeDef",
    "ExecutiveSummaryOptionTypeDef",
    "ExplicitHierarchyOutputTypeDef",
    "ExplicitHierarchyTypeDef",
    "ExportHiddenFieldsOptionTypeDef",
    "ExportToCSVOptionTypeDef",
    "ExportWithHiddenFieldsOptionTypeDef",
    "FailedKeyRegistrationEntryTypeDef",
    "FieldBarSeriesItemTypeDef",
    "FieldBasedTooltipOutputTypeDef",
    "FieldBasedTooltipTypeDef",
    "FieldComboSeriesItemTypeDef",
    "FieldFolderOutputTypeDef",
    "FieldFolderTypeDef",
    "FieldFolderUnionTypeDef",
    "FieldLabelTypeTypeDef",
    "FieldSeriesItemTypeDef",
    "FieldSortOptionsTypeDef",
    "FieldSortTypeDef",
    "FieldTooltipItemTypeDef",
    "FilledMapAggregatedFieldWellsOutputTypeDef",
    "FilledMapAggregatedFieldWellsTypeDef",
    "FilledMapConditionalFormattingOptionOutputTypeDef",
    "FilledMapConditionalFormattingOptionTypeDef",
    "FilledMapConditionalFormattingOutputTypeDef",
    "FilledMapConditionalFormattingTypeDef",
    "FilledMapConfigurationOutputTypeDef",
    "FilledMapConfigurationTypeDef",
    "FilledMapFieldWellsOutputTypeDef",
    "FilledMapFieldWellsTypeDef",
    "FilledMapShapeConditionalFormattingOutputTypeDef",
    "FilledMapShapeConditionalFormattingTypeDef",
    "FilledMapSortConfigurationOutputTypeDef",
    "FilledMapSortConfigurationTypeDef",
    "FilledMapVisualOutputTypeDef",
    "FilledMapVisualTypeDef",
    "FilterAggMetricsTypeDef",
    "FilterControlOutputTypeDef",
    "FilterControlTypeDef",
    "FilterCrossSheetControlOutputTypeDef",
    "FilterCrossSheetControlTypeDef",
    "FilterDateTimePickerControlTypeDef",
    "FilterDropDownControlOutputTypeDef",
    "FilterDropDownControlTypeDef",
    "FilterGroupOutputTypeDef",
    "FilterGroupTypeDef",
    "FilterListConfigurationOutputTypeDef",
    "FilterListConfigurationTypeDef",
    "FilterListControlOutputTypeDef",
    "FilterListControlTypeDef",
    "FilterOperationOutputTypeDef",
    "FilterOperationSelectedFieldsConfigurationOutputTypeDef",
    "FilterOperationSelectedFieldsConfigurationTypeDef",
    "FilterOperationTargetVisualsConfigurationOutputTypeDef",
    "FilterOperationTargetVisualsConfigurationTypeDef",
    "FilterOperationTypeDef",
    "FilterOperationUnionTypeDef",
    "FilterOutputTypeDef",
    "FilterRelativeDateTimeControlTypeDef",
    "FilterScopeConfigurationOutputTypeDef",
    "FilterScopeConfigurationTypeDef",
    "FilterSelectableValuesOutputTypeDef",
    "FilterSelectableValuesTypeDef",
    "FilterSliderControlTypeDef",
    "FilterTextAreaControlTypeDef",
    "FilterTextFieldControlTypeDef",
    "FilterTypeDef",
    "FiltersOperationOutputTypeDef",
    "FiltersOperationTypeDef",
    "FlowSummaryTypeDef",
    "FolderMemberTypeDef",
    "FolderSearchFilterTypeDef",
    "FolderSummaryTypeDef",
    "FolderTypeDef",
    "FontConfigurationTypeDef",
    "FontSizeTypeDef",
    "FontTypeDef",
    "FontWeightTypeDef",
    "ForecastComputationTypeDef",
    "ForecastConfigurationOutputTypeDef",
    "ForecastConfigurationTypeDef",
    "ForecastScenarioOutputTypeDef",
    "ForecastScenarioTypeDef",
    "FormatConfigurationTypeDef",
    "FreeFormLayoutCanvasSizeOptionsTypeDef",
    "FreeFormLayoutConfigurationOutputTypeDef",
    "FreeFormLayoutConfigurationTypeDef",
    "FreeFormLayoutElementBackgroundStyleTypeDef",
    "FreeFormLayoutElementBorderStyleTypeDef",
    "FreeFormLayoutElementOutputTypeDef",
    "FreeFormLayoutElementTypeDef",
    "FreeFormLayoutScreenCanvasSizeOptionsTypeDef",
    "FreeFormSectionLayoutConfigurationOutputTypeDef",
    "FreeFormSectionLayoutConfigurationTypeDef",
    "FunnelChartAggregatedFieldWellsOutputTypeDef",
    "FunnelChartAggregatedFieldWellsTypeDef",
    "FunnelChartConfigurationOutputTypeDef",
    "FunnelChartConfigurationTypeDef",
    "FunnelChartDataLabelOptionsTypeDef",
    "FunnelChartFieldWellsOutputTypeDef",
    "FunnelChartFieldWellsTypeDef",
    "FunnelChartSortConfigurationOutputTypeDef",
    "FunnelChartSortConfigurationTypeDef",
    "FunnelChartVisualOutputTypeDef",
    "FunnelChartVisualTypeDef",
    "GaugeChartArcConditionalFormattingOutputTypeDef",
    "GaugeChartArcConditionalFormattingTypeDef",
    "GaugeChartColorConfigurationTypeDef",
    "GaugeChartConditionalFormattingOptionOutputTypeDef",
    "GaugeChartConditionalFormattingOptionTypeDef",
    "GaugeChartConditionalFormattingOutputTypeDef",
    "GaugeChartConditionalFormattingTypeDef",
    "GaugeChartConfigurationOutputTypeDef",
    "GaugeChartConfigurationTypeDef",
    "GaugeChartFieldWellsOutputTypeDef",
    "GaugeChartFieldWellsTypeDef",
    "GaugeChartOptionsTypeDef",
    "GaugeChartPrimaryValueConditionalFormattingOutputTypeDef",
    "GaugeChartPrimaryValueConditionalFormattingTypeDef",
    "GaugeChartVisualOutputTypeDef",
    "GaugeChartVisualTypeDef",
    "GenerateEmbedUrlForAnonymousUserRequestTypeDef",
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserRequestTypeDef",
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserWithIdentityRequestTypeDef",
    "GenerateEmbedUrlForRegisteredUserWithIdentityResponseTypeDef",
    "GeneratedAnswerResultTypeDef",
    "GenerativeAuthoringConfigurationsTypeDef",
    "GeoSpatialColumnGroupOutputTypeDef",
    "GeoSpatialColumnGroupTypeDef",
    "GeoSpatialColumnGroupUnionTypeDef",
    "GeocodePreferenceTypeDef",
    "GeocodePreferenceValueTypeDef",
    "GeocoderHierarchyTypeDef",
    "GeospatialCategoricalColorOutputTypeDef",
    "GeospatialCategoricalColorTypeDef",
    "GeospatialCategoricalDataColorTypeDef",
    "GeospatialCircleRadiusTypeDef",
    "GeospatialCircleSymbolStyleOutputTypeDef",
    "GeospatialCircleSymbolStyleTypeDef",
    "GeospatialColorOutputTypeDef",
    "GeospatialColorTypeDef",
    "GeospatialCoordinateBoundsTypeDef",
    "GeospatialDataSourceItemTypeDef",
    "GeospatialGradientColorOutputTypeDef",
    "GeospatialGradientColorTypeDef",
    "GeospatialGradientStepColorTypeDef",
    "GeospatialHeatmapColorScaleOutputTypeDef",
    "GeospatialHeatmapColorScaleTypeDef",
    "GeospatialHeatmapConfigurationOutputTypeDef",
    "GeospatialHeatmapConfigurationTypeDef",
    "GeospatialHeatmapDataColorTypeDef",
    "GeospatialLayerColorFieldOutputTypeDef",
    "GeospatialLayerColorFieldTypeDef",
    "GeospatialLayerDefinitionOutputTypeDef",
    "GeospatialLayerDefinitionTypeDef",
    "GeospatialLayerItemOutputTypeDef",
    "GeospatialLayerItemTypeDef",
    "GeospatialLayerJoinDefinitionOutputTypeDef",
    "GeospatialLayerJoinDefinitionTypeDef",
    "GeospatialLayerMapConfigurationOutputTypeDef",
    "GeospatialLayerMapConfigurationTypeDef",
    "GeospatialLineLayerOutputTypeDef",
    "GeospatialLineLayerTypeDef",
    "GeospatialLineStyleOutputTypeDef",
    "GeospatialLineStyleTypeDef",
    "GeospatialLineSymbolStyleOutputTypeDef",
    "GeospatialLineSymbolStyleTypeDef",
    "GeospatialLineWidthTypeDef",
    "GeospatialMapAggregatedFieldWellsOutputTypeDef",
    "GeospatialMapAggregatedFieldWellsTypeDef",
    "GeospatialMapConfigurationOutputTypeDef",
    "GeospatialMapConfigurationTypeDef",
    "GeospatialMapFieldWellsOutputTypeDef",
    "GeospatialMapFieldWellsTypeDef",
    "GeospatialMapStateTypeDef",
    "GeospatialMapStyleOptionsTypeDef",
    "GeospatialMapStyleTypeDef",
    "GeospatialMapVisualOutputTypeDef",
    "GeospatialMapVisualTypeDef",
    "GeospatialNullDataSettingsTypeDef",
    "GeospatialNullSymbolStyleTypeDef",
    "GeospatialPointLayerOutputTypeDef",
    "GeospatialPointLayerTypeDef",
    "GeospatialPointStyleOptionsOutputTypeDef",
    "GeospatialPointStyleOptionsTypeDef",
    "GeospatialPointStyleOutputTypeDef",
    "GeospatialPointStyleTypeDef",
    "GeospatialPolygonLayerOutputTypeDef",
    "GeospatialPolygonLayerTypeDef",
    "GeospatialPolygonStyleOutputTypeDef",
    "GeospatialPolygonStyleTypeDef",
    "GeospatialPolygonSymbolStyleOutputTypeDef",
    "GeospatialPolygonSymbolStyleTypeDef",
    "GeospatialSolidColorTypeDef",
    "GeospatialStaticFileSourceTypeDef",
    "GeospatialWindowOptionsTypeDef",
    "GetDashboardEmbedUrlRequestTypeDef",
    "GetDashboardEmbedUrlResponseTypeDef",
    "GetFlowMetadataInputTypeDef",
    "GetFlowMetadataOutputTypeDef",
    "GetFlowPermissionsInputTypeDef",
    "GetFlowPermissionsOutputTypeDef",
    "GetIdentityContextRequestTypeDef",
    "GetIdentityContextResponseTypeDef",
    "GetSessionEmbedUrlRequestTypeDef",
    "GetSessionEmbedUrlResponseTypeDef",
    "GlobalTableBorderOptionsTypeDef",
    "GradientColorOutputTypeDef",
    "GradientColorTypeDef",
    "GradientStopTypeDef",
    "GridLayoutCanvasSizeOptionsTypeDef",
    "GridLayoutConfigurationOutputTypeDef",
    "GridLayoutConfigurationTypeDef",
    "GridLayoutElementBackgroundStyleTypeDef",
    "GridLayoutElementBorderStyleTypeDef",
    "GridLayoutElementTypeDef",
    "GridLayoutScreenCanvasSizeOptionsTypeDef",
    "GroupMemberTypeDef",
    "GroupSearchFilterTypeDef",
    "GroupTypeDef",
    "GrowthRateComputationTypeDef",
    "GutterStyleTypeDef",
    "HeaderFooterSectionConfigurationOutputTypeDef",
    "HeaderFooterSectionConfigurationTypeDef",
    "HeatMapAggregatedFieldWellsOutputTypeDef",
    "HeatMapAggregatedFieldWellsTypeDef",
    "HeatMapConfigurationOutputTypeDef",
    "HeatMapConfigurationTypeDef",
    "HeatMapFieldWellsOutputTypeDef",
    "HeatMapFieldWellsTypeDef",
    "HeatMapSortConfigurationOutputTypeDef",
    "HeatMapSortConfigurationTypeDef",
    "HeatMapVisualOutputTypeDef",
    "HeatMapVisualTypeDef",
    "HistogramAggregatedFieldWellsOutputTypeDef",
    "HistogramAggregatedFieldWellsTypeDef",
    "HistogramBinOptionsTypeDef",
    "HistogramConfigurationOutputTypeDef",
    "HistogramConfigurationTypeDef",
    "HistogramFieldWellsOutputTypeDef",
    "HistogramFieldWellsTypeDef",
    "HistogramVisualOutputTypeDef",
    "HistogramVisualTypeDef",
    "IAMConnectionMetadataTypeDef",
    "IAMPolicyAssignmentSummaryTypeDef",
    "IAMPolicyAssignmentTypeDef",
    "IdentifierTypeDef",
    "IdentityCenterConfigurationTypeDef",
    "ImageConfigurationTypeDef",
    "ImageCustomActionOperationOutputTypeDef",
    "ImageCustomActionOperationTypeDef",
    "ImageCustomActionOutputTypeDef",
    "ImageCustomActionTypeDef",
    "ImageInteractionOptionsTypeDef",
    "ImageMenuOptionTypeDef",
    "ImageSetConfigurationTypeDef",
    "ImageSetTypeDef",
    "ImageSourceTypeDef",
    "ImageStaticFileTypeDef",
    "ImageTypeDef",
    "ImpalaParametersTypeDef",
    "ImportTableOperationOutputTypeDef",
    "ImportTableOperationSourceOutputTypeDef",
    "ImportTableOperationSourceTypeDef",
    "ImportTableOperationTypeDef",
    "IncrementalRefreshTypeDef",
    "IngestionTypeDef",
    "InnerFilterOutputTypeDef",
    "InnerFilterTypeDef",
    "InputColumnTypeDef",
    "InsightConfigurationOutputTypeDef",
    "InsightConfigurationTypeDef",
    "InsightVisualOutputTypeDef",
    "InsightVisualTypeDef",
    "IntegerDatasetParameterDefaultValuesOutputTypeDef",
    "IntegerDatasetParameterDefaultValuesTypeDef",
    "IntegerDatasetParameterDefaultValuesUnionTypeDef",
    "IntegerDatasetParameterOutputTypeDef",
    "IntegerDatasetParameterTypeDef",
    "IntegerDatasetParameterUnionTypeDef",
    "IntegerDefaultValuesOutputTypeDef",
    "IntegerDefaultValuesTypeDef",
    "IntegerParameterDeclarationOutputTypeDef",
    "IntegerParameterDeclarationTypeDef",
    "IntegerParameterOutputTypeDef",
    "IntegerParameterTypeDef",
    "IntegerValueWhenUnsetConfigurationTypeDef",
    "InvalidTopicReviewedAnswerTypeDef",
    "ItemsLimitConfigurationTypeDef",
    "JiraParametersTypeDef",
    "JoinInstructionTypeDef",
    "JoinKeyPropertiesTypeDef",
    "JoinOperandPropertiesOutputTypeDef",
    "JoinOperandPropertiesTypeDef",
    "JoinOperationOutputTypeDef",
    "JoinOperationTypeDef",
    "KPIActualValueConditionalFormattingOutputTypeDef",
    "KPIActualValueConditionalFormattingTypeDef",
    "KPIComparisonValueConditionalFormattingOutputTypeDef",
    "KPIComparisonValueConditionalFormattingTypeDef",
    "KPIConditionalFormattingOptionOutputTypeDef",
    "KPIConditionalFormattingOptionTypeDef",
    "KPIConditionalFormattingOutputTypeDef",
    "KPIConditionalFormattingTypeDef",
    "KPIConfigurationOutputTypeDef",
    "KPIConfigurationTypeDef",
    "KPIFieldWellsOutputTypeDef",
    "KPIFieldWellsTypeDef",
    "KPIOptionsTypeDef",
    "KPIPrimaryValueConditionalFormattingOutputTypeDef",
    "KPIPrimaryValueConditionalFormattingTypeDef",
    "KPIProgressBarConditionalFormattingOutputTypeDef",
    "KPIProgressBarConditionalFormattingTypeDef",
    "KPISortConfigurationOutputTypeDef",
    "KPISortConfigurationTypeDef",
    "KPISparklineOptionsTypeDef",
    "KPIVisualLayoutOptionsTypeDef",
    "KPIVisualOutputTypeDef",
    "KPIVisualStandardLayoutTypeDef",
    "KPIVisualTypeDef",
    "KeyPairCredentialsTypeDef",
    "LabelOptionsTypeDef",
    "LayerCustomActionOperationOutputTypeDef",
    "LayerCustomActionOperationTypeDef",
    "LayerCustomActionOutputTypeDef",
    "LayerCustomActionTypeDef",
    "LayerMapVisualOutputTypeDef",
    "LayerMapVisualTypeDef",
    "LayoutConfigurationOutputTypeDef",
    "LayoutConfigurationTypeDef",
    "LayoutOutputTypeDef",
    "LayoutTypeDef",
    "LegendOptionsTypeDef",
    "LineChartAggregatedFieldWellsOutputTypeDef",
    "LineChartAggregatedFieldWellsTypeDef",
    "LineChartConfigurationOutputTypeDef",
    "LineChartConfigurationTypeDef",
    "LineChartDefaultSeriesSettingsTypeDef",
    "LineChartFieldWellsOutputTypeDef",
    "LineChartFieldWellsTypeDef",
    "LineChartLineStyleSettingsTypeDef",
    "LineChartMarkerStyleSettingsTypeDef",
    "LineChartSeriesSettingsTypeDef",
    "LineChartSortConfigurationOutputTypeDef",
    "LineChartSortConfigurationTypeDef",
    "LineChartVisualOutputTypeDef",
    "LineChartVisualTypeDef",
    "LineSeriesAxisDisplayOptionsOutputTypeDef",
    "LineSeriesAxisDisplayOptionsTypeDef",
    "LinkSharingConfigurationOutputTypeDef",
    "LinkSharingConfigurationTypeDef",
    "LinkSharingConfigurationUnionTypeDef",
    "ListActionConnectorsRequestPaginateTypeDef",
    "ListActionConnectorsRequestTypeDef",
    "ListActionConnectorsResponseTypeDef",
    "ListAnalysesRequestPaginateTypeDef",
    "ListAnalysesRequestTypeDef",
    "ListAnalysesResponseTypeDef",
    "ListAssetBundleExportJobsRequestPaginateTypeDef",
    "ListAssetBundleExportJobsRequestTypeDef",
    "ListAssetBundleExportJobsResponseTypeDef",
    "ListAssetBundleImportJobsRequestPaginateTypeDef",
    "ListAssetBundleImportJobsRequestTypeDef",
    "ListAssetBundleImportJobsResponseTypeDef",
    "ListBrandsRequestPaginateTypeDef",
    "ListBrandsRequestTypeDef",
    "ListBrandsResponseTypeDef",
    "ListControlDisplayOptionsTypeDef",
    "ListControlSearchOptionsTypeDef",
    "ListControlSelectAllOptionsTypeDef",
    "ListCustomPermissionsRequestPaginateTypeDef",
    "ListCustomPermissionsRequestTypeDef",
    "ListCustomPermissionsResponseTypeDef",
    "ListDashboardVersionsRequestPaginateTypeDef",
    "ListDashboardVersionsRequestTypeDef",
    "ListDashboardVersionsResponseTypeDef",
    "ListDashboardsRequestPaginateTypeDef",
    "ListDashboardsRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "ListDataSetsRequestPaginateTypeDef",
    "ListDataSetsRequestTypeDef",
    "ListDataSetsResponseTypeDef",
    "ListDataSourcesRequestPaginateTypeDef",
    "ListDataSourcesRequestTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListFlowsInputPaginateTypeDef",
    "ListFlowsInputTypeDef",
    "ListFlowsOutputTypeDef",
    "ListFolderMembersRequestPaginateTypeDef",
    "ListFolderMembersRequestTypeDef",
    "ListFolderMembersResponseTypeDef",
    "ListFoldersForResourceRequestPaginateTypeDef",
    "ListFoldersForResourceRequestTypeDef",
    "ListFoldersForResourceResponseTypeDef",
    "ListFoldersRequestPaginateTypeDef",
    "ListFoldersRequestTypeDef",
    "ListFoldersResponseTypeDef",
    "ListGroupMembershipsRequestPaginateTypeDef",
    "ListGroupMembershipsRequestTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "ListGroupsRequestPaginateTypeDef",
    "ListGroupsRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestPaginateTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestTypeDef",
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    "ListIAMPolicyAssignmentsRequestPaginateTypeDef",
    "ListIAMPolicyAssignmentsRequestTypeDef",
    "ListIAMPolicyAssignmentsResponseTypeDef",
    "ListIdentityPropagationConfigsRequestTypeDef",
    "ListIdentityPropagationConfigsResponseTypeDef",
    "ListIngestionsRequestPaginateTypeDef",
    "ListIngestionsRequestTypeDef",
    "ListIngestionsResponseTypeDef",
    "ListNamespacesRequestPaginateTypeDef",
    "ListNamespacesRequestTypeDef",
    "ListNamespacesResponseTypeDef",
    "ListRefreshSchedulesRequestTypeDef",
    "ListRefreshSchedulesResponseTypeDef",
    "ListRoleMembershipsRequestPaginateTypeDef",
    "ListRoleMembershipsRequestTypeDef",
    "ListRoleMembershipsResponseTypeDef",
    "ListSelfUpgradesRequestTypeDef",
    "ListSelfUpgradesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateAliasesRequestPaginateTypeDef",
    "ListTemplateAliasesRequestTypeDef",
    "ListTemplateAliasesResponseTypeDef",
    "ListTemplateVersionsRequestPaginateTypeDef",
    "ListTemplateVersionsRequestTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "ListTemplatesRequestPaginateTypeDef",
    "ListTemplatesRequestTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListThemeAliasesRequestTypeDef",
    "ListThemeAliasesResponseTypeDef",
    "ListThemeVersionsRequestPaginateTypeDef",
    "ListThemeVersionsRequestTypeDef",
    "ListThemeVersionsResponseTypeDef",
    "ListThemesRequestPaginateTypeDef",
    "ListThemesRequestTypeDef",
    "ListThemesResponseTypeDef",
    "ListTopicRefreshSchedulesRequestTypeDef",
    "ListTopicRefreshSchedulesResponseTypeDef",
    "ListTopicReviewedAnswersRequestTypeDef",
    "ListTopicReviewedAnswersResponseTypeDef",
    "ListTopicsRequestTypeDef",
    "ListTopicsResponseTypeDef",
    "ListUserGroupsRequestPaginateTypeDef",
    "ListUserGroupsRequestTypeDef",
    "ListUserGroupsResponseTypeDef",
    "ListUsersRequestPaginateTypeDef",
    "ListUsersRequestTypeDef",
    "ListUsersResponseTypeDef",
    "ListVPCConnectionsRequestTypeDef",
    "ListVPCConnectionsResponseTypeDef",
    "LoadingAnimationTypeDef",
    "LocalNavigationConfigurationTypeDef",
    "LogicalTableOutputTypeDef",
    "LogicalTableSourceTypeDef",
    "LogicalTableTypeDef",
    "LogicalTableUnionTypeDef",
    "LogoConfigurationTypeDef",
    "LogoSetConfigurationTypeDef",
    "LogoSetTypeDef",
    "LogoTypeDef",
    "LongFormatTextTypeDef",
    "LookbackWindowTypeDef",
    "ManifestFileLocationTypeDef",
    "MappedDataSetParameterTypeDef",
    "MarginStyleTypeDef",
    "MariaDbParametersTypeDef",
    "MaximumLabelTypeTypeDef",
    "MaximumMinimumComputationTypeDef",
    "MeasureFieldTypeDef",
    "MemberIdArnPairTypeDef",
    "MetricComparisonComputationTypeDef",
    "MinimumLabelTypeTypeDef",
    "MissingDataConfigurationTypeDef",
    "MySqlParametersTypeDef",
    "NamedEntityDefinitionMetricOutputTypeDef",
    "NamedEntityDefinitionMetricTypeDef",
    "NamedEntityDefinitionOutputTypeDef",
    "NamedEntityDefinitionTypeDef",
    "NamedEntityRefTypeDef",
    "NamespaceErrorTypeDef",
    "NamespaceInfoV2TypeDef",
    "NavbarStyleTypeDef",
    "NegativeFormatTypeDef",
    "NegativeValueConfigurationTypeDef",
    "NestedFilterOutputTypeDef",
    "NestedFilterTypeDef",
    "NetworkInterfaceTypeDef",
    "NewDefaultValuesOutputTypeDef",
    "NewDefaultValuesTypeDef",
    "NewDefaultValuesUnionTypeDef",
    "NoneConnectionMetadataTypeDef",
    "NullValueFormatConfigurationTypeDef",
    "NumberDisplayFormatConfigurationTypeDef",
    "NumberFormatConfigurationTypeDef",
    "NumericAxisOptionsOutputTypeDef",
    "NumericAxisOptionsTypeDef",
    "NumericEqualityDrillDownFilterTypeDef",
    "NumericEqualityFilterOutputTypeDef",
    "NumericEqualityFilterTypeDef",
    "NumericFormatConfigurationTypeDef",
    "NumericRangeFilterOutputTypeDef",
    "NumericRangeFilterTypeDef",
    "NumericRangeFilterValueTypeDef",
    "NumericSeparatorConfigurationTypeDef",
    "NumericalAggregationFunctionTypeDef",
    "NumericalDimensionFieldTypeDef",
    "NumericalMeasureFieldTypeDef",
    "OAuthParametersTypeDef",
    "OracleParametersTypeDef",
    "OutputColumnNameOverrideTypeDef",
    "OutputColumnTypeDef",
    "OverrideDatasetParameterOperationOutputTypeDef",
    "OverrideDatasetParameterOperationTypeDef",
    "OverrideDatasetParameterOperationUnionTypeDef",
    "PaginationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PaletteTypeDef",
    "PanelConfigurationTypeDef",
    "PanelTitleOptionsTypeDef",
    "ParameterControlOutputTypeDef",
    "ParameterControlTypeDef",
    "ParameterDateTimePickerControlTypeDef",
    "ParameterDeclarationOutputTypeDef",
    "ParameterDeclarationTypeDef",
    "ParameterDropDownControlOutputTypeDef",
    "ParameterDropDownControlTypeDef",
    "ParameterListControlOutputTypeDef",
    "ParameterListControlTypeDef",
    "ParameterSelectableValuesOutputTypeDef",
    "ParameterSelectableValuesTypeDef",
    "ParameterSliderControlTypeDef",
    "ParameterTextAreaControlTypeDef",
    "ParameterTextFieldControlTypeDef",
    "ParametersOutputTypeDef",
    "ParametersTypeDef",
    "ParametersUnionTypeDef",
    "ParentDataSetOutputTypeDef",
    "ParentDataSetTypeDef",
    "PercentVisibleRangeTypeDef",
    "PercentageDisplayFormatConfigurationTypeDef",
    "PercentileAggregationTypeDef",
    "PerformanceConfigurationOutputTypeDef",
    "PerformanceConfigurationTypeDef",
    "PerformanceConfigurationUnionTypeDef",
    "PeriodOverPeriodComputationTypeDef",
    "PeriodToDateComputationTypeDef",
    "PermissionOutputTypeDef",
    "PermissionTypeDef",
    "PermissionUnionTypeDef",
    "PhysicalTableOutputTypeDef",
    "PhysicalTableTypeDef",
    "PhysicalTableUnionTypeDef",
    "PieChartAggregatedFieldWellsOutputTypeDef",
    "PieChartAggregatedFieldWellsTypeDef",
    "PieChartConfigurationOutputTypeDef",
    "PieChartConfigurationTypeDef",
    "PieChartFieldWellsOutputTypeDef",
    "PieChartFieldWellsTypeDef",
    "PieChartSortConfigurationOutputTypeDef",
    "PieChartSortConfigurationTypeDef",
    "PieChartVisualOutputTypeDef",
    "PieChartVisualTypeDef",
    "PivotConfigurationOutputTypeDef",
    "PivotConfigurationTypeDef",
    "PivotFieldSortOptionsOutputTypeDef",
    "PivotFieldSortOptionsTypeDef",
    "PivotOperationOutputTypeDef",
    "PivotOperationTypeDef",
    "PivotTableAggregatedFieldWellsOutputTypeDef",
    "PivotTableAggregatedFieldWellsTypeDef",
    "PivotTableCellConditionalFormattingOutputTypeDef",
    "PivotTableCellConditionalFormattingTypeDef",
    "PivotTableConditionalFormattingOptionOutputTypeDef",
    "PivotTableConditionalFormattingOptionTypeDef",
    "PivotTableConditionalFormattingOutputTypeDef",
    "PivotTableConditionalFormattingScopeTypeDef",
    "PivotTableConditionalFormattingTypeDef",
    "PivotTableConfigurationOutputTypeDef",
    "PivotTableConfigurationTypeDef",
    "PivotTableDataPathOptionOutputTypeDef",
    "PivotTableDataPathOptionTypeDef",
    "PivotTableFieldCollapseStateOptionOutputTypeDef",
    "PivotTableFieldCollapseStateOptionTypeDef",
    "PivotTableFieldCollapseStateTargetOutputTypeDef",
    "PivotTableFieldCollapseStateTargetTypeDef",
    "PivotTableFieldOptionTypeDef",
    "PivotTableFieldOptionsOutputTypeDef",
    "PivotTableFieldOptionsTypeDef",
    "PivotTableFieldSubtotalOptionsTypeDef",
    "PivotTableFieldWellsOutputTypeDef",
    "PivotTableFieldWellsTypeDef",
    "PivotTableOptionsOutputTypeDef",
    "PivotTableOptionsTypeDef",
    "PivotTablePaginatedReportOptionsTypeDef",
    "PivotTableRowsLabelOptionsTypeDef",
    "PivotTableSortByOutputTypeDef",
    "PivotTableSortByTypeDef",
    "PivotTableSortConfigurationOutputTypeDef",
    "PivotTableSortConfigurationTypeDef",
    "PivotTableTotalOptionsOutputTypeDef",
    "PivotTableTotalOptionsTypeDef",
    "PivotTableVisualOutputTypeDef",
    "PivotTableVisualTypeDef",
    "PivotTotalOptionsOutputTypeDef",
    "PivotTotalOptionsTypeDef",
    "PivotedLabelTypeDef",
    "PluginVisualConfigurationOutputTypeDef",
    "PluginVisualConfigurationTypeDef",
    "PluginVisualFieldWellOutputTypeDef",
    "PluginVisualFieldWellTypeDef",
    "PluginVisualItemsLimitConfigurationTypeDef",
    "PluginVisualOptionsOutputTypeDef",
    "PluginVisualOptionsTypeDef",
    "PluginVisualOutputTypeDef",
    "PluginVisualPropertyTypeDef",
    "PluginVisualSortConfigurationOutputTypeDef",
    "PluginVisualSortConfigurationTypeDef",
    "PluginVisualTableQuerySortOutputTypeDef",
    "PluginVisualTableQuerySortTypeDef",
    "PluginVisualTypeDef",
    "PostgreSqlParametersTypeDef",
    "PredefinedHierarchyOutputTypeDef",
    "PredefinedHierarchyTypeDef",
    "PredictQAResultsRequestTypeDef",
    "PredictQAResultsResponseTypeDef",
    "PrestoParametersTypeDef",
    "ProgressBarOptionsTypeDef",
    "ProjectOperationOutputTypeDef",
    "ProjectOperationTypeDef",
    "ProjectOperationUnionTypeDef",
    "PutDataSetRefreshPropertiesRequestTypeDef",
    "PutDataSetRefreshPropertiesResponseTypeDef",
    "QAResultTypeDef",
    "QBusinessParametersTypeDef",
    "QDataKeyTypeDef",
    "QueryExecutionOptionsTypeDef",
    "QueueInfoTypeDef",
    "QuickSuiteActionsOptionTypeDef",
    "RadarChartAggregatedFieldWellsOutputTypeDef",
    "RadarChartAggregatedFieldWellsTypeDef",
    "RadarChartAreaStyleSettingsTypeDef",
    "RadarChartConfigurationOutputTypeDef",
    "RadarChartConfigurationTypeDef",
    "RadarChartFieldWellsOutputTypeDef",
    "RadarChartFieldWellsTypeDef",
    "RadarChartSeriesSettingsTypeDef",
    "RadarChartSortConfigurationOutputTypeDef",
    "RadarChartSortConfigurationTypeDef",
    "RadarChartVisualOutputTypeDef",
    "RadarChartVisualTypeDef",
    "RangeConstantTypeDef",
    "RangeEndsLabelTypeTypeDef",
    "RdsParametersTypeDef",
    "ReadAPIKeyConnectionMetadataTypeDef",
    "ReadAuthConfigTypeDef",
    "ReadAuthenticationMetadataTypeDef",
    "ReadAuthorizationCodeGrantCredentialsDetailsTypeDef",
    "ReadAuthorizationCodeGrantDetailsTypeDef",
    "ReadAuthorizationCodeGrantMetadataTypeDef",
    "ReadBasicAuthConnectionMetadataTypeDef",
    "ReadClientCredentialsDetailsTypeDef",
    "ReadClientCredentialsGrantDetailsTypeDef",
    "ReadClientCredentialsGrantMetadataTypeDef",
    "ReadIamConnectionMetadataTypeDef",
    "ReadNoneConnectionMetadataTypeDef",
    "RecentSnapshotsConfigurationsTypeDef",
    "RedshiftIAMParametersOutputTypeDef",
    "RedshiftIAMParametersTypeDef",
    "RedshiftIAMParametersUnionTypeDef",
    "RedshiftParametersOutputTypeDef",
    "RedshiftParametersTypeDef",
    "RedshiftParametersUnionTypeDef",
    "ReferenceLineCustomLabelConfigurationTypeDef",
    "ReferenceLineDataConfigurationTypeDef",
    "ReferenceLineDynamicDataConfigurationTypeDef",
    "ReferenceLineLabelConfigurationTypeDef",
    "ReferenceLineStaticDataConfigurationTypeDef",
    "ReferenceLineStyleConfigurationTypeDef",
    "ReferenceLineTypeDef",
    "ReferenceLineValueLabelConfigurationTypeDef",
    "RefreshConfigurationTypeDef",
    "RefreshFailureConfigurationTypeDef",
    "RefreshFailureEmailAlertTypeDef",
    "RefreshFrequencyTypeDef",
    "RefreshScheduleOutputTypeDef",
    "RefreshScheduleTypeDef",
    "RefreshScheduleUnionTypeDef",
    "RegisterUserRequestTypeDef",
    "RegisterUserResponseTypeDef",
    "RegisteredCustomerManagedKeyTypeDef",
    "RegisteredUserConsoleFeatureConfigurationsTypeDef",
    "RegisteredUserDashboardEmbeddingConfigurationTypeDef",
    "RegisteredUserDashboardFeatureConfigurationsTypeDef",
    "RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef",
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    "RegisteredUserGenerativeQnAEmbeddingConfigurationTypeDef",
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    "RegisteredUserSnapshotJobResultTypeDef",
    "RelationalTableOutputTypeDef",
    "RelationalTableTypeDef",
    "RelationalTableUnionTypeDef",
    "RelativeDateTimeControlDisplayOptionsTypeDef",
    "RelativeDatesFilterOutputTypeDef",
    "RelativeDatesFilterTypeDef",
    "RenameColumnOperationTypeDef",
    "RenameColumnsOperationOutputTypeDef",
    "RenameColumnsOperationTypeDef",
    "ResourcePermissionOutputTypeDef",
    "ResourcePermissionTypeDef",
    "ResourcePermissionUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreAnalysisRequestTypeDef",
    "RestoreAnalysisResponseTypeDef",
    "RollingDateConfigurationTypeDef",
    "RowAlternateColorOptionsOutputTypeDef",
    "RowAlternateColorOptionsTypeDef",
    "RowInfoTypeDef",
    "RowLevelPermissionConfigurationOutputTypeDef",
    "RowLevelPermissionConfigurationTypeDef",
    "RowLevelPermissionDataSetTypeDef",
    "RowLevelPermissionTagConfigurationOutputTypeDef",
    "RowLevelPermissionTagConfigurationTypeDef",
    "RowLevelPermissionTagConfigurationUnionTypeDef",
    "RowLevelPermissionTagRuleTypeDef",
    "S3BucketConfigurationTypeDef",
    "S3KnowledgeBaseParametersTypeDef",
    "S3ParametersTypeDef",
    "S3SourceOutputTypeDef",
    "S3SourceTypeDef",
    "S3SourceUnionTypeDef",
    "SaaSTableOutputTypeDef",
    "SaaSTableTypeDef",
    "SaaSTableUnionTypeDef",
    "SameSheetTargetVisualConfigurationOutputTypeDef",
    "SameSheetTargetVisualConfigurationTypeDef",
    "SankeyDiagramAggregatedFieldWellsOutputTypeDef",
    "SankeyDiagramAggregatedFieldWellsTypeDef",
    "SankeyDiagramChartConfigurationOutputTypeDef",
    "SankeyDiagramChartConfigurationTypeDef",
    "SankeyDiagramFieldWellsOutputTypeDef",
    "SankeyDiagramFieldWellsTypeDef",
    "SankeyDiagramSortConfigurationOutputTypeDef",
    "SankeyDiagramSortConfigurationTypeDef",
    "SankeyDiagramVisualOutputTypeDef",
    "SankeyDiagramVisualTypeDef",
    "ScatterPlotCategoricallyAggregatedFieldWellsOutputTypeDef",
    "ScatterPlotCategoricallyAggregatedFieldWellsTypeDef",
    "ScatterPlotConfigurationOutputTypeDef",
    "ScatterPlotConfigurationTypeDef",
    "ScatterPlotFieldWellsOutputTypeDef",
    "ScatterPlotFieldWellsTypeDef",
    "ScatterPlotSortConfigurationTypeDef",
    "ScatterPlotUnaggregatedFieldWellsOutputTypeDef",
    "ScatterPlotUnaggregatedFieldWellsTypeDef",
    "ScatterPlotVisualOutputTypeDef",
    "ScatterPlotVisualTypeDef",
    "ScheduleRefreshOnEntityTypeDef",
    "SchedulesConfigurationsTypeDef",
    "ScrollBarOptionsTypeDef",
    "SearchActionConnectorsRequestPaginateTypeDef",
    "SearchActionConnectorsRequestTypeDef",
    "SearchActionConnectorsResponseTypeDef",
    "SearchAnalysesRequestPaginateTypeDef",
    "SearchAnalysesRequestTypeDef",
    "SearchAnalysesResponseTypeDef",
    "SearchDashboardsRequestPaginateTypeDef",
    "SearchDashboardsRequestTypeDef",
    "SearchDashboardsResponseTypeDef",
    "SearchDataSetsRequestPaginateTypeDef",
    "SearchDataSetsRequestTypeDef",
    "SearchDataSetsResponseTypeDef",
    "SearchDataSourcesRequestPaginateTypeDef",
    "SearchDataSourcesRequestTypeDef",
    "SearchDataSourcesResponseTypeDef",
    "SearchFlowsFilterTypeDef",
    "SearchFlowsInputPaginateTypeDef",
    "SearchFlowsInputTypeDef",
    "SearchFlowsOutputTypeDef",
    "SearchFoldersRequestPaginateTypeDef",
    "SearchFoldersRequestTypeDef",
    "SearchFoldersResponseTypeDef",
    "SearchGroupsRequestPaginateTypeDef",
    "SearchGroupsRequestTypeDef",
    "SearchGroupsResponseTypeDef",
    "SearchTopicsRequestPaginateTypeDef",
    "SearchTopicsRequestTypeDef",
    "SearchTopicsResponseTypeDef",
    "SecondaryValueOptionsTypeDef",
    "SectionAfterPageBreakTypeDef",
    "SectionBasedLayoutCanvasSizeOptionsTypeDef",
    "SectionBasedLayoutConfigurationOutputTypeDef",
    "SectionBasedLayoutConfigurationTypeDef",
    "SectionBasedLayoutPaperCanvasSizeOptionsTypeDef",
    "SectionLayoutConfigurationOutputTypeDef",
    "SectionLayoutConfigurationTypeDef",
    "SectionPageBreakConfigurationTypeDef",
    "SectionStyleTypeDef",
    "SelectedSheetsFilterScopeConfigurationOutputTypeDef",
    "SelectedSheetsFilterScopeConfigurationTypeDef",
    "SelfUpgradeConfigurationTypeDef",
    "SelfUpgradeRequestDetailTypeDef",
    "SemanticEntityTypeOutputTypeDef",
    "SemanticEntityTypeTypeDef",
    "SemanticModelConfigurationOutputTypeDef",
    "SemanticModelConfigurationTypeDef",
    "SemanticModelConfigurationUnionTypeDef",
    "SemanticTableOutputTypeDef",
    "SemanticTableTypeDef",
    "SemanticTypeOutputTypeDef",
    "SemanticTypeTypeDef",
    "SeriesItemTypeDef",
    "ServiceNowParametersTypeDef",
    "SessionTagTypeDef",
    "SetParameterValueConfigurationOutputTypeDef",
    "SetParameterValueConfigurationTypeDef",
    "ShapeConditionalFormatOutputTypeDef",
    "ShapeConditionalFormatTypeDef",
    "SharedViewConfigurationsTypeDef",
    "SheetBackgroundStyleTypeDef",
    "SheetControlInfoIconLabelOptionsTypeDef",
    "SheetControlLayoutConfigurationOutputTypeDef",
    "SheetControlLayoutConfigurationTypeDef",
    "SheetControlLayoutOutputTypeDef",
    "SheetControlLayoutTypeDef",
    "SheetControlsOptionTypeDef",
    "SheetDefinitionOutputTypeDef",
    "SheetDefinitionTypeDef",
    "SheetElementConfigurationOverridesTypeDef",
    "SheetElementRenderingRuleTypeDef",
    "SheetImageOutputTypeDef",
    "SheetImageScalingConfigurationTypeDef",
    "SheetImageSourceTypeDef",
    "SheetImageStaticFileSourceTypeDef",
    "SheetImageTooltipConfigurationTypeDef",
    "SheetImageTooltipTextTypeDef",
    "SheetImageTypeDef",
    "SheetLayoutElementMaximizationOptionTypeDef",
    "SheetLayoutGroupMemberTypeDef",
    "SheetLayoutGroupOutputTypeDef",
    "SheetLayoutGroupTypeDef",
    "SheetStyleTypeDef",
    "SheetTextBoxTypeDef",
    "SheetTypeDef",
    "SheetVisualScopingConfigurationOutputTypeDef",
    "SheetVisualScopingConfigurationTypeDef",
    "ShortFormatTextTypeDef",
    "SignupResponseTypeDef",
    "SimpleClusterMarkerTypeDef",
    "SingleAxisOptionsTypeDef",
    "SliderControlDisplayOptionsTypeDef",
    "SlotTypeDef",
    "SmallMultiplesAxisPropertiesTypeDef",
    "SmallMultiplesOptionsTypeDef",
    "SnapshotAnonymousUserRedactedTypeDef",
    "SnapshotAnonymousUserTypeDef",
    "SnapshotConfigurationOutputTypeDef",
    "SnapshotConfigurationTypeDef",
    "SnapshotConfigurationUnionTypeDef",
    "SnapshotDestinationConfigurationOutputTypeDef",
    "SnapshotDestinationConfigurationTypeDef",
    "SnapshotFileGroupOutputTypeDef",
    "SnapshotFileGroupTypeDef",
    "SnapshotFileOutputTypeDef",
    "SnapshotFileSheetSelectionOutputTypeDef",
    "SnapshotFileSheetSelectionTypeDef",
    "SnapshotFileTypeDef",
    "SnapshotJobErrorInfoTypeDef",
    "SnapshotJobResultErrorInfoTypeDef",
    "SnapshotJobResultFileGroupTypeDef",
    "SnapshotJobResultTypeDef",
    "SnapshotJobS3ResultTypeDef",
    "SnapshotS3DestinationConfigurationTypeDef",
    "SnapshotUserConfigurationRedactedTypeDef",
    "SnapshotUserConfigurationTypeDef",
    "SnowflakeParametersTypeDef",
    "SourceTableOutputTypeDef",
    "SourceTableTypeDef",
    "SpacingTypeDef",
    "SparkParametersTypeDef",
    "SpatialStaticFileTypeDef",
    "SqlServerParametersTypeDef",
    "SslPropertiesTypeDef",
    "StarburstParametersTypeDef",
    "StartAssetBundleExportJobRequestTypeDef",
    "StartAssetBundleExportJobResponseTypeDef",
    "StartAssetBundleImportJobRequestTypeDef",
    "StartAssetBundleImportJobResponseTypeDef",
    "StartDashboardSnapshotJobRequestTypeDef",
    "StartDashboardSnapshotJobResponseTypeDef",
    "StartDashboardSnapshotJobScheduleRequestTypeDef",
    "StartDashboardSnapshotJobScheduleResponseTypeDef",
    "StatePersistenceConfigurationsTypeDef",
    "StaticFileS3SourceOptionsTypeDef",
    "StaticFileSourceTypeDef",
    "StaticFileTypeDef",
    "StaticFileUrlSourceOptionsTypeDef",
    "StringDatasetParameterDefaultValuesOutputTypeDef",
    "StringDatasetParameterDefaultValuesTypeDef",
    "StringDatasetParameterDefaultValuesUnionTypeDef",
    "StringDatasetParameterOutputTypeDef",
    "StringDatasetParameterTypeDef",
    "StringDatasetParameterUnionTypeDef",
    "StringDefaultValuesOutputTypeDef",
    "StringDefaultValuesTypeDef",
    "StringFormatConfigurationTypeDef",
    "StringParameterDeclarationOutputTypeDef",
    "StringParameterDeclarationTypeDef",
    "StringParameterOutputTypeDef",
    "StringParameterTypeDef",
    "StringValueWhenUnsetConfigurationTypeDef",
    "SubtotalOptionsOutputTypeDef",
    "SubtotalOptionsTypeDef",
    "SucceededTopicReviewedAnswerTypeDef",
    "SuccessfulKeyRegistrationEntryTypeDef",
    "TableAggregatedFieldWellsOutputTypeDef",
    "TableAggregatedFieldWellsTypeDef",
    "TableBorderOptionsTypeDef",
    "TableCellConditionalFormattingOutputTypeDef",
    "TableCellConditionalFormattingTypeDef",
    "TableCellImageSizingConfigurationTypeDef",
    "TableCellStyleTypeDef",
    "TableConditionalFormattingOptionOutputTypeDef",
    "TableConditionalFormattingOptionTypeDef",
    "TableConditionalFormattingOutputTypeDef",
    "TableConditionalFormattingTypeDef",
    "TableConfigurationOutputTypeDef",
    "TableConfigurationTypeDef",
    "TableFieldCustomIconContentTypeDef",
    "TableFieldCustomTextContentTypeDef",
    "TableFieldImageConfigurationTypeDef",
    "TableFieldLinkConfigurationTypeDef",
    "TableFieldLinkContentConfigurationTypeDef",
    "TableFieldOptionTypeDef",
    "TableFieldOptionsOutputTypeDef",
    "TableFieldOptionsTypeDef",
    "TableFieldURLConfigurationTypeDef",
    "TableFieldWellsOutputTypeDef",
    "TableFieldWellsTypeDef",
    "TableInlineVisualizationTypeDef",
    "TableOptionsOutputTypeDef",
    "TableOptionsTypeDef",
    "TablePaginatedReportOptionsTypeDef",
    "TablePathElementTypeDef",
    "TablePinnedFieldOptionsOutputTypeDef",
    "TablePinnedFieldOptionsTypeDef",
    "TableRowConditionalFormattingOutputTypeDef",
    "TableRowConditionalFormattingTypeDef",
    "TableSideBorderOptionsTypeDef",
    "TableSortConfigurationOutputTypeDef",
    "TableSortConfigurationTypeDef",
    "TableStyleTargetTypeDef",
    "TableUnaggregatedFieldWellsOutputTypeDef",
    "TableUnaggregatedFieldWellsTypeDef",
    "TableVisualOutputTypeDef",
    "TableVisualTypeDef",
    "TagColumnOperationOutputTypeDef",
    "TagColumnOperationTypeDef",
    "TagColumnOperationUnionTypeDef",
    "TagResourceRequestTypeDef",
    "TagResourceResponseTypeDef",
    "TagTypeDef",
    "TemplateAliasTypeDef",
    "TemplateErrorTypeDef",
    "TemplateSourceAnalysisTypeDef",
    "TemplateSourceEntityTypeDef",
    "TemplateSourceTemplateTypeDef",
    "TemplateSummaryTypeDef",
    "TemplateTypeDef",
    "TemplateVersionDefinitionOutputTypeDef",
    "TemplateVersionDefinitionTypeDef",
    "TemplateVersionDefinitionUnionTypeDef",
    "TemplateVersionSummaryTypeDef",
    "TemplateVersionTypeDef",
    "TeradataParametersTypeDef",
    "TextAreaControlDisplayOptionsTypeDef",
    "TextBoxInteractionOptionsTypeDef",
    "TextBoxMenuOptionTypeDef",
    "TextConditionalFormatOutputTypeDef",
    "TextConditionalFormatTypeDef",
    "TextControlPlaceholderOptionsTypeDef",
    "TextFieldControlDisplayOptionsTypeDef",
    "ThemeAliasTypeDef",
    "ThemeConfigurationOutputTypeDef",
    "ThemeConfigurationTypeDef",
    "ThemeConfigurationUnionTypeDef",
    "ThemeErrorTypeDef",
    "ThemeSummaryTypeDef",
    "ThemeTypeDef",
    "ThemeVersionSummaryTypeDef",
    "ThemeVersionTypeDef",
    "ThousandSeparatorOptionsTypeDef",
    "ThresholdAlertsConfigurationsTypeDef",
    "TileLayoutStyleTypeDef",
    "TileStyleTypeDef",
    "TimeBasedForecastPropertiesTypeDef",
    "TimeEqualityFilterOutputTypeDef",
    "TimeEqualityFilterTypeDef",
    "TimeRangeDrillDownFilterOutputTypeDef",
    "TimeRangeDrillDownFilterTypeDef",
    "TimeRangeFilterOutputTypeDef",
    "TimeRangeFilterTypeDef",
    "TimeRangeFilterValueOutputTypeDef",
    "TimeRangeFilterValueTypeDef",
    "TimestampTypeDef",
    "TooltipItemTypeDef",
    "TooltipOptionsOutputTypeDef",
    "TooltipOptionsTypeDef",
    "TopBottomFilterOutputTypeDef",
    "TopBottomFilterTypeDef",
    "TopBottomMoversComputationTypeDef",
    "TopBottomRankedComputationTypeDef",
    "TopicCalculatedFieldOutputTypeDef",
    "TopicCalculatedFieldTypeDef",
    "TopicCategoryFilterConstantOutputTypeDef",
    "TopicCategoryFilterConstantTypeDef",
    "TopicCategoryFilterOutputTypeDef",
    "TopicCategoryFilterTypeDef",
    "TopicColumnOutputTypeDef",
    "TopicColumnTypeDef",
    "TopicConfigOptionsTypeDef",
    "TopicConstantValueOutputTypeDef",
    "TopicConstantValueTypeDef",
    "TopicConstantValueUnionTypeDef",
    "TopicDateRangeFilterTypeDef",
    "TopicDetailsOutputTypeDef",
    "TopicDetailsTypeDef",
    "TopicDetailsUnionTypeDef",
    "TopicFilterOutputTypeDef",
    "TopicFilterTypeDef",
    "TopicIRComparisonMethodTypeDef",
    "TopicIRContributionAnalysisOutputTypeDef",
    "TopicIRContributionAnalysisTypeDef",
    "TopicIRContributionAnalysisUnionTypeDef",
    "TopicIRFilterOptionOutputTypeDef",
    "TopicIRFilterOptionTypeDef",
    "TopicIRFilterOptionUnionTypeDef",
    "TopicIRGroupByTypeDef",
    "TopicIRMetricOutputTypeDef",
    "TopicIRMetricTypeDef",
    "TopicIRMetricUnionTypeDef",
    "TopicIROutputTypeDef",
    "TopicIRTypeDef",
    "TopicIRUnionTypeDef",
    "TopicNamedEntityOutputTypeDef",
    "TopicNamedEntityTypeDef",
    "TopicNullFilterTypeDef",
    "TopicNumericEqualityFilterTypeDef",
    "TopicNumericRangeFilterTypeDef",
    "TopicRangeFilterConstantTypeDef",
    "TopicRefreshDetailsTypeDef",
    "TopicRefreshScheduleOutputTypeDef",
    "TopicRefreshScheduleSummaryTypeDef",
    "TopicRefreshScheduleTypeDef",
    "TopicRefreshScheduleUnionTypeDef",
    "TopicRelativeDateFilterTypeDef",
    "TopicReviewedAnswerTypeDef",
    "TopicSearchFilterTypeDef",
    "TopicSingularFilterConstantTypeDef",
    "TopicSortClauseTypeDef",
    "TopicSummaryTypeDef",
    "TopicTemplateOutputTypeDef",
    "TopicTemplateTypeDef",
    "TopicTemplateUnionTypeDef",
    "TopicVisualOutputTypeDef",
    "TopicVisualTypeDef",
    "TopicVisualUnionTypeDef",
    "TotalAggregationComputationTypeDef",
    "TotalAggregationFunctionTypeDef",
    "TotalAggregationOptionTypeDef",
    "TotalOptionsOutputTypeDef",
    "TotalOptionsTypeDef",
    "TransformOperationOutputTypeDef",
    "TransformOperationSourceOutputTypeDef",
    "TransformOperationSourceTypeDef",
    "TransformOperationSourceUnionTypeDef",
    "TransformOperationTypeDef",
    "TransformOperationUnionTypeDef",
    "TransformStepOutputTypeDef",
    "TransformStepTypeDef",
    "TransposedTableOptionTypeDef",
    "TreeMapAggregatedFieldWellsOutputTypeDef",
    "TreeMapAggregatedFieldWellsTypeDef",
    "TreeMapConfigurationOutputTypeDef",
    "TreeMapConfigurationTypeDef",
    "TreeMapFieldWellsOutputTypeDef",
    "TreeMapFieldWellsTypeDef",
    "TreeMapSortConfigurationOutputTypeDef",
    "TreeMapSortConfigurationTypeDef",
    "TreeMapVisualOutputTypeDef",
    "TreeMapVisualTypeDef",
    "TrendArrowOptionsTypeDef",
    "TrinoParametersTypeDef",
    "TwitterParametersTypeDef",
    "TypographyOutputTypeDef",
    "TypographyTypeDef",
    "UIColorPaletteTypeDef",
    "UnaggregatedFieldTypeDef",
    "UniqueKeyOutputTypeDef",
    "UniqueKeyTypeDef",
    "UniqueValuesComputationTypeDef",
    "UnpivotOperationOutputTypeDef",
    "UnpivotOperationTypeDef",
    "UntagColumnOperationOutputTypeDef",
    "UntagColumnOperationTypeDef",
    "UntagColumnOperationUnionTypeDef",
    "UntagResourceRequestTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateAccountCustomPermissionRequestTypeDef",
    "UpdateAccountCustomPermissionResponseTypeDef",
    "UpdateAccountCustomizationRequestTypeDef",
    "UpdateAccountCustomizationResponseTypeDef",
    "UpdateAccountSettingsRequestTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "UpdateActionConnectorPermissionsRequestTypeDef",
    "UpdateActionConnectorPermissionsResponseTypeDef",
    "UpdateActionConnectorRequestTypeDef",
    "UpdateActionConnectorResponseTypeDef",
    "UpdateAnalysisPermissionsRequestTypeDef",
    "UpdateAnalysisPermissionsResponseTypeDef",
    "UpdateAnalysisRequestTypeDef",
    "UpdateAnalysisResponseTypeDef",
    "UpdateApplicationWithTokenExchangeGrantRequestTypeDef",
    "UpdateApplicationWithTokenExchangeGrantResponseTypeDef",
    "UpdateBrandAssignmentRequestTypeDef",
    "UpdateBrandAssignmentResponseTypeDef",
    "UpdateBrandPublishedVersionRequestTypeDef",
    "UpdateBrandPublishedVersionResponseTypeDef",
    "UpdateBrandRequestTypeDef",
    "UpdateBrandResponseTypeDef",
    "UpdateCustomPermissionsRequestTypeDef",
    "UpdateCustomPermissionsResponseTypeDef",
    "UpdateDashboardLinksRequestTypeDef",
    "UpdateDashboardLinksResponseTypeDef",
    "UpdateDashboardPermissionsRequestTypeDef",
    "UpdateDashboardPermissionsResponseTypeDef",
    "UpdateDashboardPublishedVersionRequestTypeDef",
    "UpdateDashboardPublishedVersionResponseTypeDef",
    "UpdateDashboardRequestTypeDef",
    "UpdateDashboardResponseTypeDef",
    "UpdateDashboardsQAConfigurationRequestTypeDef",
    "UpdateDashboardsQAConfigurationResponseTypeDef",
    "UpdateDataSetPermissionsRequestTypeDef",
    "UpdateDataSetPermissionsResponseTypeDef",
    "UpdateDataSetRequestTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateDataSourcePermissionsRequestTypeDef",
    "UpdateDataSourcePermissionsResponseTypeDef",
    "UpdateDataSourceRequestTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateDefaultQBusinessApplicationRequestTypeDef",
    "UpdateDefaultQBusinessApplicationResponseTypeDef",
    "UpdateFlowPermissionsInputTypeDef",
    "UpdateFlowPermissionsOutputTypeDef",
    "UpdateFolderPermissionsRequestTypeDef",
    "UpdateFolderPermissionsResponseTypeDef",
    "UpdateFolderRequestTypeDef",
    "UpdateFolderResponseTypeDef",
    "UpdateGroupRequestTypeDef",
    "UpdateGroupResponseTypeDef",
    "UpdateIAMPolicyAssignmentRequestTypeDef",
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    "UpdateIdentityPropagationConfigRequestTypeDef",
    "UpdateIdentityPropagationConfigResponseTypeDef",
    "UpdateIpRestrictionRequestTypeDef",
    "UpdateIpRestrictionResponseTypeDef",
    "UpdateKeyRegistrationRequestTypeDef",
    "UpdateKeyRegistrationResponseTypeDef",
    "UpdatePublicSharingSettingsRequestTypeDef",
    "UpdatePublicSharingSettingsResponseTypeDef",
    "UpdateQPersonalizationConfigurationRequestTypeDef",
    "UpdateQPersonalizationConfigurationResponseTypeDef",
    "UpdateQuickSightQSearchConfigurationRequestTypeDef",
    "UpdateQuickSightQSearchConfigurationResponseTypeDef",
    "UpdateRefreshScheduleRequestTypeDef",
    "UpdateRefreshScheduleResponseTypeDef",
    "UpdateRoleCustomPermissionRequestTypeDef",
    "UpdateRoleCustomPermissionResponseTypeDef",
    "UpdateSPICECapacityConfigurationRequestTypeDef",
    "UpdateSPICECapacityConfigurationResponseTypeDef",
    "UpdateSelfUpgradeConfigurationRequestTypeDef",
    "UpdateSelfUpgradeConfigurationResponseTypeDef",
    "UpdateSelfUpgradeRequestTypeDef",
    "UpdateSelfUpgradeResponseTypeDef",
    "UpdateTemplateAliasRequestTypeDef",
    "UpdateTemplateAliasResponseTypeDef",
    "UpdateTemplatePermissionsRequestTypeDef",
    "UpdateTemplatePermissionsResponseTypeDef",
    "UpdateTemplateRequestTypeDef",
    "UpdateTemplateResponseTypeDef",
    "UpdateThemeAliasRequestTypeDef",
    "UpdateThemeAliasResponseTypeDef",
    "UpdateThemePermissionsRequestTypeDef",
    "UpdateThemePermissionsResponseTypeDef",
    "UpdateThemeRequestTypeDef",
    "UpdateThemeResponseTypeDef",
    "UpdateTopicPermissionsRequestTypeDef",
    "UpdateTopicPermissionsResponseTypeDef",
    "UpdateTopicRefreshScheduleRequestTypeDef",
    "UpdateTopicRefreshScheduleResponseTypeDef",
    "UpdateTopicRequestTypeDef",
    "UpdateTopicResponseTypeDef",
    "UpdateUserCustomPermissionRequestTypeDef",
    "UpdateUserCustomPermissionResponseTypeDef",
    "UpdateUserRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateVPCConnectionRequestTypeDef",
    "UpdateVPCConnectionResponseTypeDef",
    "UploadSettingsTypeDef",
    "UserIdentifierTypeDef",
    "UserTypeDef",
    "VPCConnectionSummaryTypeDef",
    "VPCConnectionTypeDef",
    "ValidationStrategyTypeDef",
    "ValueColumnConfigurationTypeDef",
    "VisibleRangeOptionsTypeDef",
    "VisualAxisSortOptionTypeDef",
    "VisualCustomActionDefaultsTypeDef",
    "VisualCustomActionOperationOutputTypeDef",
    "VisualCustomActionOperationTypeDef",
    "VisualCustomActionOutputTypeDef",
    "VisualCustomActionTypeDef",
    "VisualCustomizationFieldsConfigurationOutputTypeDef",
    "VisualCustomizationFieldsConfigurationTypeDef",
    "VisualHighlightOperationTypeDef",
    "VisualInteractionOptionsTypeDef",
    "VisualMenuOptionTypeDef",
    "VisualOptionsTypeDef",
    "VisualOutputTypeDef",
    "VisualPaletteOutputTypeDef",
    "VisualPaletteTypeDef",
    "VisualSubtitleFontConfigurationTypeDef",
    "VisualSubtitleLabelOptionsTypeDef",
    "VisualTitleFontConfigurationTypeDef",
    "VisualTitleLabelOptionsTypeDef",
    "VisualTypeDef",
    "VpcConnectionPropertiesTypeDef",
    "WaterfallChartAggregatedFieldWellsOutputTypeDef",
    "WaterfallChartAggregatedFieldWellsTypeDef",
    "WaterfallChartColorConfigurationTypeDef",
    "WaterfallChartConfigurationOutputTypeDef",
    "WaterfallChartConfigurationTypeDef",
    "WaterfallChartFieldWellsOutputTypeDef",
    "WaterfallChartFieldWellsTypeDef",
    "WaterfallChartGroupColorConfigurationTypeDef",
    "WaterfallChartOptionsTypeDef",
    "WaterfallChartSortConfigurationOutputTypeDef",
    "WaterfallChartSortConfigurationTypeDef",
    "WaterfallVisualOutputTypeDef",
    "WaterfallVisualTypeDef",
    "WebCrawlerParametersTypeDef",
    "WebProxyCredentialsTypeDef",
    "WhatIfPointScenarioOutputTypeDef",
    "WhatIfPointScenarioTypeDef",
    "WhatIfRangeScenarioOutputTypeDef",
    "WhatIfRangeScenarioTypeDef",
    "WordCloudAggregatedFieldWellsOutputTypeDef",
    "WordCloudAggregatedFieldWellsTypeDef",
    "WordCloudChartConfigurationOutputTypeDef",
    "WordCloudChartConfigurationTypeDef",
    "WordCloudFieldWellsOutputTypeDef",
    "WordCloudFieldWellsTypeDef",
    "WordCloudOptionsTypeDef",
    "WordCloudSortConfigurationOutputTypeDef",
    "WordCloudSortConfigurationTypeDef",
    "WordCloudVisualOutputTypeDef",
    "WordCloudVisualTypeDef",
    "YAxisOptionsTypeDef",
)


class APIKeyConnectionMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    ApiKey: str
    Email: NotRequired[str]


class AccountCustomizationTypeDef(TypedDict):
    DefaultTheme: NotRequired[str]
    DefaultEmailCustomizationTemplate: NotRequired[str]


class AccountInfoTypeDef(TypedDict):
    AccountName: NotRequired[str]
    Edition: NotRequired[EditionType]
    NotificationEmail: NotRequired[str]
    AuthenticationType: NotRequired[str]
    AccountSubscriptionStatus: NotRequired[str]
    IAMIdentityCenterInstanceArn: NotRequired[str]


class AccountSettingsTypeDef(TypedDict):
    AccountName: NotRequired[str]
    Edition: NotRequired[EditionType]
    DefaultNamespace: NotRequired[str]
    NotificationEmail: NotRequired[str]
    PublicSharingEnabled: NotRequired[bool]
    TerminationProtectionEnabled: NotRequired[bool]


ActionConnectorErrorTypeDef = TypedDict(
    "ActionConnectorErrorTypeDef",
    {
        "Message": NotRequired[str],
        "Type": NotRequired[Literal["INTERNAL_FAILURE"]],
    },
)


class ActionConnectorSearchFilterTypeDef(TypedDict):
    Name: ActionConnectorSearchFilterNameEnumType
    Operator: FilterOperatorType
    Value: str


class ActiveIAMPolicyAssignmentTypeDef(TypedDict):
    AssignmentName: NotRequired[str]
    PolicyArn: NotRequired[str]


class AdHocFilteringOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class AggFunctionOutputTypeDef(TypedDict):
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[dict[str, str]]
    Period: NotRequired[TopicTimeGranularityType]
    PeriodField: NotRequired[str]


class AggFunctionTypeDef(TypedDict):
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[Mapping[str, str]]
    Period: NotRequired[TopicTimeGranularityType]
    PeriodField: NotRequired[str]


class AttributeAggregationFunctionTypeDef(TypedDict):
    SimpleAttributeAggregation: NotRequired[Literal["UNIQUE_VALUE"]]
    ValueForMultipleValues: NotRequired[str]


class AggregationPartitionByTypeDef(TypedDict):
    FieldName: NotRequired[str]
    TimeGranularity: NotRequired[TimeGranularityType]


class ColumnIdentifierTypeDef(TypedDict):
    DataSetIdentifier: str
    ColumnName: str


class AmazonElasticsearchParametersTypeDef(TypedDict):
    Domain: str


class AmazonOpenSearchParametersTypeDef(TypedDict):
    Domain: str


class DataQnAConfigurationsTypeDef(TypedDict):
    Enabled: bool


class DataStoriesConfigurationsTypeDef(TypedDict):
    Enabled: bool


class ExecutiveSummaryConfigurationsTypeDef(TypedDict):
    Enabled: bool


class GenerativeAuthoringConfigurationsTypeDef(TypedDict):
    Enabled: bool


class CalculatedFieldTypeDef(TypedDict):
    DataSetIdentifier: str
    Name: str
    Expression: str


class DataSetIdentifierDeclarationTypeDef(TypedDict):
    Identifier: str
    DataSetArn: str


class QueryExecutionOptionsTypeDef(TypedDict):
    QueryExecutionMode: NotRequired[QueryExecutionModeType]


class EntityTypeDef(TypedDict):
    Path: NotRequired[str]


class AnalysisSearchFilterTypeDef(TypedDict):
    Operator: NotRequired[FilterOperatorType]
    Name: NotRequired[AnalysisFilterAttributeType]
    Value: NotRequired[str]


class DataSetReferenceTypeDef(TypedDict):
    DataSetPlaceholder: str
    DataSetArn: str


class AnalysisSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    AnalysisId: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ResourceStatusType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class AnchorDateConfigurationTypeDef(TypedDict):
    AnchorOption: NotRequired[Literal["NOW"]]
    ParameterName: NotRequired[str]


class AnchorTypeDef(TypedDict):
    AnchorType: NotRequired[Literal["TODAY"]]
    TimeGranularity: NotRequired[TimeGranularityType]
    Offset: NotRequired[int]


class SharedViewConfigurationsTypeDef(TypedDict):
    Enabled: bool


class DashboardVisualIdTypeDef(TypedDict):
    DashboardId: str
    SheetId: str
    VisualId: str


class AnonymousUserGenerativeQnAEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: str


class AnonymousUserQSearchBarEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: str


class AppendedColumnTypeDef(TypedDict):
    ColumnName: str
    NewColumnId: str


class ArcAxisDisplayRangeTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class ArcConfigurationTypeDef(TypedDict):
    ArcAngle: NotRequired[float]
    ArcThickness: NotRequired[ArcThicknessOptionsType]


class ArcOptionsTypeDef(TypedDict):
    ArcThickness: NotRequired[ArcThicknessType]


class AssetBundleExportJobAnalysisOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[Literal["Name"]]


class AssetBundleExportJobDashboardOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[Literal["Name"]]


class AssetBundleExportJobDataSetOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[AssetBundleExportJobDataSetPropertyToOverrideType]


class AssetBundleExportJobDataSourceOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[AssetBundleExportJobDataSourcePropertyToOverrideType]


class AssetBundleExportJobFolderOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[AssetBundleExportJobFolderPropertyToOverrideType]


class AssetBundleExportJobRefreshScheduleOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[Literal["StartAfterDateTime"]]


class AssetBundleExportJobResourceIdOverrideConfigurationTypeDef(TypedDict):
    PrefixForAllResources: NotRequired[bool]


class AssetBundleExportJobThemeOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[Literal["Name"]]


class AssetBundleExportJobVPCConnectionOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: list[AssetBundleExportJobVPCConnectionPropertyToOverrideType]


class AssetBundleExportJobAnalysisOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["Name"]]


class AssetBundleExportJobDashboardOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["Name"]]


class AssetBundleExportJobDataSetOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[AssetBundleExportJobDataSetPropertyToOverrideType]


class AssetBundleExportJobDataSourceOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[AssetBundleExportJobDataSourcePropertyToOverrideType]


class AssetBundleExportJobFolderOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[AssetBundleExportJobFolderPropertyToOverrideType]


class AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["StartAfterDateTime"]]


class AssetBundleExportJobThemeOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["Name"]]


class AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[AssetBundleExportJobVPCConnectionPropertyToOverrideType]


AssetBundleExportJobErrorTypeDef = TypedDict(
    "AssetBundleExportJobErrorTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Message": NotRequired[str],
    },
)


class AssetBundleExportJobSummaryTypeDef(TypedDict):
    JobStatus: NotRequired[AssetBundleExportJobStatusType]
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    AssetBundleExportJobId: NotRequired[str]
    IncludeAllDependencies: NotRequired[bool]
    ExportFormat: NotRequired[AssetBundleExportFormatType]
    IncludePermissions: NotRequired[bool]
    IncludeTags: NotRequired[bool]


class AssetBundleExportJobValidationStrategyTypeDef(TypedDict):
    StrictModeForAllResources: NotRequired[bool]


class AssetBundleExportJobWarningTypeDef(TypedDict):
    Arn: NotRequired[str]
    Message: NotRequired[str]


class AssetBundleImportJobAnalysisOverrideParametersTypeDef(TypedDict):
    AnalysisId: str
    Name: NotRequired[str]


class AssetBundleResourcePermissionsOutputTypeDef(TypedDict):
    Principals: list[str]
    Actions: list[str]


class AssetBundleResourcePermissionsTypeDef(TypedDict):
    Principals: Sequence[str]
    Actions: Sequence[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class AssetBundleImportJobDashboardOverrideParametersTypeDef(TypedDict):
    DashboardId: str
    Name: NotRequired[str]


class AssetBundleImportJobDataSourceCredentialPairTypeDef(TypedDict):
    Username: str
    Password: str


class SslPropertiesTypeDef(TypedDict):
    DisableSsl: NotRequired[bool]


class VpcConnectionPropertiesTypeDef(TypedDict):
    VpcConnectionArn: str


AssetBundleImportJobErrorTypeDef = TypedDict(
    "AssetBundleImportJobErrorTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Message": NotRequired[str],
    },
)


class AssetBundleImportJobFolderOverrideParametersTypeDef(TypedDict):
    FolderId: str
    Name: NotRequired[str]
    ParentFolderArn: NotRequired[str]


class AssetBundleImportJobRefreshScheduleOverrideParametersOutputTypeDef(TypedDict):
    DataSetId: str
    ScheduleId: str
    StartAfterDateTime: NotRequired[datetime]


class AssetBundleImportJobResourceIdOverrideConfigurationTypeDef(TypedDict):
    PrefixForAllResources: NotRequired[str]


class AssetBundleImportJobThemeOverrideParametersTypeDef(TypedDict):
    ThemeId: str
    Name: NotRequired[str]


class AssetBundleImportJobVPCConnectionOverrideParametersOutputTypeDef(TypedDict):
    VPCConnectionId: str
    Name: NotRequired[str]
    SubnetIds: NotRequired[list[str]]
    SecurityGroupIds: NotRequired[list[str]]
    DnsResolvers: NotRequired[list[str]]
    RoleArn: NotRequired[str]


class AssetBundleImportJobVPCConnectionOverrideParametersTypeDef(TypedDict):
    VPCConnectionId: str
    Name: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    DnsResolvers: NotRequired[Sequence[str]]
    RoleArn: NotRequired[str]


class AssetBundleImportJobOverrideValidationStrategyTypeDef(TypedDict):
    StrictModeForAllResources: NotRequired[bool]


TimestampTypeDef = Union[datetime, str]


class AssetBundleImportJobSummaryTypeDef(TypedDict):
    JobStatus: NotRequired[AssetBundleImportJobStatusType]
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    AssetBundleImportJobId: NotRequired[str]
    FailureAction: NotRequired[AssetBundleImportFailureActionType]


class AssetBundleImportJobWarningTypeDef(TypedDict):
    Arn: NotRequired[str]
    Message: NotRequired[str]


class AssetBundleImportSourceDescriptionTypeDef(TypedDict):
    Body: NotRequired[str]
    S3Uri: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class IdentityCenterConfigurationTypeDef(TypedDict):
    EnableIdentityPropagation: NotRequired[bool]


class AuroraParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class AuroraPostgreSqlParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class BasicAuthConnectionMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    Username: str
    Password: str


class IAMConnectionMetadataTypeDef(TypedDict):
    RoleArn: str


class NoneConnectionMetadataTypeDef(TypedDict):
    BaseEndpoint: str


class AuthorizationCodeGrantDetailsTypeDef(TypedDict):
    ClientId: str
    ClientSecret: str
    TokenEndpoint: str
    AuthorizationEndpoint: str


class AuthorizedTargetsByServiceTypeDef(TypedDict):
    Service: NotRequired[ServiceTypeType]
    AuthorizedTargets: NotRequired[list[str]]


class AwsIotAnalyticsParametersTypeDef(TypedDict):
    DataSetName: str


class DateAxisOptionsTypeDef(TypedDict):
    MissingDateVisibility: NotRequired[VisibilityType]


class AxisDisplayMinMaxRangeTypeDef(TypedDict):
    Minimum: NotRequired[float]
    Maximum: NotRequired[float]


class AxisLinearScaleTypeDef(TypedDict):
    StepCount: NotRequired[int]
    StepSize: NotRequired[float]


class AxisLogarithmicScaleTypeDef(TypedDict):
    Base: NotRequired[float]


class BorderSettingsTypeDef(TypedDict):
    BorderVisibility: NotRequired[VisibilityType]
    BorderWidth: NotRequired[str]
    BorderColor: NotRequired[str]


class DecalSettingsTypeDef(TypedDict):
    ElementValue: NotRequired[str]
    DecalVisibility: NotRequired[VisibilityType]
    DecalColor: NotRequired[str]
    DecalPatternType: NotRequired[DecalPatternTypeType]
    DecalStyleType: NotRequired[DecalStyleTypeType]


class ItemsLimitConfigurationTypeDef(TypedDict):
    ItemsLimit: NotRequired[int]
    OtherCategories: NotRequired[OtherCategoriesType]


class InvalidTopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: NotRequired[str]
    Error: NotRequired[ReviewedAnswerErrorCodeType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SucceededTopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: NotRequired[str]


class BatchDeleteTopicReviewedAnswerRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    AnswerIds: NotRequired[Sequence[str]]


class BigQueryParametersTypeDef(TypedDict):
    ProjectId: str
    DataSetRegion: NotRequired[str]


class BinCountOptionsTypeDef(TypedDict):
    Value: NotRequired[int]


class BinWidthOptionsTypeDef(TypedDict):
    Value: NotRequired[float]
    BinCountLimit: NotRequired[int]


class SectionAfterPageBreakTypeDef(TypedDict):
    Status: NotRequired[SectionPageBreakStatusType]


class BookmarksConfigurationsTypeDef(TypedDict):
    Enabled: bool


class BorderStyleTypeDef(TypedDict):
    Color: NotRequired[str]
    Show: NotRequired[bool]
    Width: NotRequired[str]


class BoxPlotStyleOptionsTypeDef(TypedDict):
    FillStyle: NotRequired[BoxPlotFillStyleType]


class PaginationConfigurationTypeDef(TypedDict):
    PageSize: int
    PageNumber: int


class PaletteTypeDef(TypedDict):
    Foreground: NotRequired[str]
    Background: NotRequired[str]


class BrandSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    BrandId: NotRequired[str]
    BrandName: NotRequired[str]
    Description: NotRequired[str]
    BrandStatus: NotRequired[BrandStatusType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class CalculatedColumnTypeDef(TypedDict):
    ColumnName: str
    ColumnId: str
    Expression: str


class CalculatedMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Expression: str


class CancelIngestionRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    IngestionId: str


class CapabilitiesTypeDef(TypedDict):
    ExportToCsv: NotRequired[Literal["DENY"]]
    ExportToExcel: NotRequired[Literal["DENY"]]
    ExportToPdf: NotRequired[Literal["DENY"]]
    PrintReports: NotRequired[Literal["DENY"]]
    CreateAndUpdateThemes: NotRequired[Literal["DENY"]]
    AddOrRunAnomalyDetectionForAnalyses: NotRequired[Literal["DENY"]]
    ShareAnalyses: NotRequired[Literal["DENY"]]
    CreateAndUpdateDatasets: NotRequired[Literal["DENY"]]
    ShareDatasets: NotRequired[Literal["DENY"]]
    SubscribeDashboardEmailReports: NotRequired[Literal["DENY"]]
    CreateAndUpdateDashboardEmailReports: NotRequired[Literal["DENY"]]
    ShareDashboards: NotRequired[Literal["DENY"]]
    CreateAndUpdateThresholdAlerts: NotRequired[Literal["DENY"]]
    RenameSharedFolders: NotRequired[Literal["DENY"]]
    CreateSharedFolders: NotRequired[Literal["DENY"]]
    CreateAndUpdateDataSources: NotRequired[Literal["DENY"]]
    ShareDataSources: NotRequired[Literal["DENY"]]
    ViewAccountSPICECapacity: NotRequired[Literal["DENY"]]
    CreateSPICEDataset: NotRequired[Literal["DENY"]]
    ExportToPdfInScheduledReports: NotRequired[Literal["DENY"]]
    ExportToCsvInScheduledReports: NotRequired[Literal["DENY"]]
    ExportToExcelInScheduledReports: NotRequired[Literal["DENY"]]
    IncludeContentInScheduledReportsEmail: NotRequired[Literal["DENY"]]
    Dashboard: NotRequired[Literal["DENY"]]
    Analysis: NotRequired[Literal["DENY"]]
    Automate: NotRequired[Literal["DENY"]]
    Flow: NotRequired[Literal["DENY"]]
    PublishWithoutApproval: NotRequired[Literal["DENY"]]
    UseBedrockModels: NotRequired[Literal["DENY"]]
    PerformFlowUiTask: NotRequired[Literal["DENY"]]
    UseAgentWebSearch: NotRequired[Literal["DENY"]]
    KnowledgeBase: NotRequired[Literal["DENY"]]
    Action: NotRequired[Literal["DENY"]]
    GenericHTTPAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateGenericHTTPAction: NotRequired[Literal["DENY"]]
    ShareGenericHTTPAction: NotRequired[Literal["DENY"]]
    UseGenericHTTPAction: NotRequired[Literal["DENY"]]
    AsanaAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateAsanaAction: NotRequired[Literal["DENY"]]
    ShareAsanaAction: NotRequired[Literal["DENY"]]
    UseAsanaAction: NotRequired[Literal["DENY"]]
    SlackAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSlackAction: NotRequired[Literal["DENY"]]
    ShareSlackAction: NotRequired[Literal["DENY"]]
    UseSlackAction: NotRequired[Literal["DENY"]]
    ServiceNowAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateServiceNowAction: NotRequired[Literal["DENY"]]
    ShareServiceNowAction: NotRequired[Literal["DENY"]]
    UseServiceNowAction: NotRequired[Literal["DENY"]]
    SalesforceAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSalesforceAction: NotRequired[Literal["DENY"]]
    ShareSalesforceAction: NotRequired[Literal["DENY"]]
    UseSalesforceAction: NotRequired[Literal["DENY"]]
    MSExchangeAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateMSExchangeAction: NotRequired[Literal["DENY"]]
    ShareMSExchangeAction: NotRequired[Literal["DENY"]]
    UseMSExchangeAction: NotRequired[Literal["DENY"]]
    PagerDutyAction: NotRequired[Literal["DENY"]]
    CreateAndUpdatePagerDutyAction: NotRequired[Literal["DENY"]]
    SharePagerDutyAction: NotRequired[Literal["DENY"]]
    UsePagerDutyAction: NotRequired[Literal["DENY"]]
    JiraAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateJiraAction: NotRequired[Literal["DENY"]]
    ShareJiraAction: NotRequired[Literal["DENY"]]
    UseJiraAction: NotRequired[Literal["DENY"]]
    ConfluenceAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateConfluenceAction: NotRequired[Literal["DENY"]]
    ShareConfluenceAction: NotRequired[Literal["DENY"]]
    UseConfluenceAction: NotRequired[Literal["DENY"]]
    OneDriveAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateOneDriveAction: NotRequired[Literal["DENY"]]
    ShareOneDriveAction: NotRequired[Literal["DENY"]]
    UseOneDriveAction: NotRequired[Literal["DENY"]]
    SharePointAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSharePointAction: NotRequired[Literal["DENY"]]
    ShareSharePointAction: NotRequired[Literal["DENY"]]
    UseSharePointAction: NotRequired[Literal["DENY"]]
    MSTeamsAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateMSTeamsAction: NotRequired[Literal["DENY"]]
    ShareMSTeamsAction: NotRequired[Literal["DENY"]]
    UseMSTeamsAction: NotRequired[Literal["DENY"]]
    GoogleCalendarAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateGoogleCalendarAction: NotRequired[Literal["DENY"]]
    ShareGoogleCalendarAction: NotRequired[Literal["DENY"]]
    UseGoogleCalendarAction: NotRequired[Literal["DENY"]]
    ZendeskAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateZendeskAction: NotRequired[Literal["DENY"]]
    ShareZendeskAction: NotRequired[Literal["DENY"]]
    UseZendeskAction: NotRequired[Literal["DENY"]]
    SmartsheetAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSmartsheetAction: NotRequired[Literal["DENY"]]
    ShareSmartsheetAction: NotRequired[Literal["DENY"]]
    UseSmartsheetAction: NotRequired[Literal["DENY"]]
    SAPBusinessPartnerAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSAPBusinessPartnerAction: NotRequired[Literal["DENY"]]
    ShareSAPBusinessPartnerAction: NotRequired[Literal["DENY"]]
    UseSAPBusinessPartnerAction: NotRequired[Literal["DENY"]]
    SAPProductMasterDataAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSAPProductMasterDataAction: NotRequired[Literal["DENY"]]
    ShareSAPProductMasterDataAction: NotRequired[Literal["DENY"]]
    UseSAPProductMasterDataAction: NotRequired[Literal["DENY"]]
    SAPPhysicalInventoryAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSAPPhysicalInventoryAction: NotRequired[Literal["DENY"]]
    ShareSAPPhysicalInventoryAction: NotRequired[Literal["DENY"]]
    UseSAPPhysicalInventoryAction: NotRequired[Literal["DENY"]]
    SAPBillOfMaterialAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSAPBillOfMaterialAction: NotRequired[Literal["DENY"]]
    ShareSAPBillOfMaterialAction: NotRequired[Literal["DENY"]]
    UseSAPBillOfMaterialAction: NotRequired[Literal["DENY"]]
    SAPMaterialStockAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSAPMaterialStockAction: NotRequired[Literal["DENY"]]
    ShareSAPMaterialStockAction: NotRequired[Literal["DENY"]]
    UseSAPMaterialStockAction: NotRequired[Literal["DENY"]]
    FactSetAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateFactSetAction: NotRequired[Literal["DENY"]]
    ShareFactSetAction: NotRequired[Literal["DENY"]]
    UseFactSetAction: NotRequired[Literal["DENY"]]
    AmazonSThreeAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateAmazonSThreeAction: NotRequired[Literal["DENY"]]
    ShareAmazonSThreeAction: NotRequired[Literal["DENY"]]
    UseAmazonSThreeAction: NotRequired[Literal["DENY"]]
    TextractAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateTextractAction: NotRequired[Literal["DENY"]]
    ShareTextractAction: NotRequired[Literal["DENY"]]
    UseTextractAction: NotRequired[Literal["DENY"]]
    ComprehendAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateComprehendAction: NotRequired[Literal["DENY"]]
    ShareComprehendAction: NotRequired[Literal["DENY"]]
    UseComprehendAction: NotRequired[Literal["DENY"]]
    ComprehendMedicalAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateComprehendMedicalAction: NotRequired[Literal["DENY"]]
    ShareComprehendMedicalAction: NotRequired[Literal["DENY"]]
    UseComprehendMedicalAction: NotRequired[Literal["DENY"]]
    AmazonBedrockARSAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateAmazonBedrockARSAction: NotRequired[Literal["DENY"]]
    ShareAmazonBedrockARSAction: NotRequired[Literal["DENY"]]
    UseAmazonBedrockARSAction: NotRequired[Literal["DENY"]]
    AmazonBedrockFSAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateAmazonBedrockFSAction: NotRequired[Literal["DENY"]]
    ShareAmazonBedrockFSAction: NotRequired[Literal["DENY"]]
    UseAmazonBedrockFSAction: NotRequired[Literal["DENY"]]
    AmazonBedrockKRSAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateAmazonBedrockKRSAction: NotRequired[Literal["DENY"]]
    ShareAmazonBedrockKRSAction: NotRequired[Literal["DENY"]]
    UseAmazonBedrockKRSAction: NotRequired[Literal["DENY"]]
    MCPAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateMCPAction: NotRequired[Literal["DENY"]]
    ShareMCPAction: NotRequired[Literal["DENY"]]
    UseMCPAction: NotRequired[Literal["DENY"]]
    OpenAPIAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateOpenAPIAction: NotRequired[Literal["DENY"]]
    ShareOpenAPIAction: NotRequired[Literal["DENY"]]
    UseOpenAPIAction: NotRequired[Literal["DENY"]]
    SandPGMIAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSandPGMIAction: NotRequired[Literal["DENY"]]
    ShareSandPGMIAction: NotRequired[Literal["DENY"]]
    UseSandPGMIAction: NotRequired[Literal["DENY"]]
    SandPGlobalEnergyAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateSandPGlobalEnergyAction: NotRequired[Literal["DENY"]]
    ShareSandPGlobalEnergyAction: NotRequired[Literal["DENY"]]
    UseSandPGlobalEnergyAction: NotRequired[Literal["DENY"]]
    BambooHRAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateBambooHRAction: NotRequired[Literal["DENY"]]
    ShareBambooHRAction: NotRequired[Literal["DENY"]]
    UseBambooHRAction: NotRequired[Literal["DENY"]]
    BoxAgentAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateBoxAgentAction: NotRequired[Literal["DENY"]]
    ShareBoxAgentAction: NotRequired[Literal["DENY"]]
    UseBoxAgentAction: NotRequired[Literal["DENY"]]
    CanvaAgentAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateCanvaAgentAction: NotRequired[Literal["DENY"]]
    ShareCanvaAgentAction: NotRequired[Literal["DENY"]]
    UseCanvaAgentAction: NotRequired[Literal["DENY"]]
    GithubAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateGithubAction: NotRequired[Literal["DENY"]]
    ShareGithubAction: NotRequired[Literal["DENY"]]
    UseGithubAction: NotRequired[Literal["DENY"]]
    NotionAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateNotionAction: NotRequired[Literal["DENY"]]
    ShareNotionAction: NotRequired[Literal["DENY"]]
    UseNotionAction: NotRequired[Literal["DENY"]]
    LinearAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateLinearAction: NotRequired[Literal["DENY"]]
    ShareLinearAction: NotRequired[Literal["DENY"]]
    UseLinearAction: NotRequired[Literal["DENY"]]
    HuggingFaceAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateHuggingFaceAction: NotRequired[Literal["DENY"]]
    ShareHuggingFaceAction: NotRequired[Literal["DENY"]]
    UseHuggingFaceAction: NotRequired[Literal["DENY"]]
    MondayAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateMondayAction: NotRequired[Literal["DENY"]]
    ShareMondayAction: NotRequired[Literal["DENY"]]
    UseMondayAction: NotRequired[Literal["DENY"]]
    HubspotAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateHubspotAction: NotRequired[Literal["DENY"]]
    ShareHubspotAction: NotRequired[Literal["DENY"]]
    UseHubspotAction: NotRequired[Literal["DENY"]]
    IntercomAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateIntercomAction: NotRequired[Literal["DENY"]]
    ShareIntercomAction: NotRequired[Literal["DENY"]]
    UseIntercomAction: NotRequired[Literal["DENY"]]
    NewRelicAction: NotRequired[Literal["DENY"]]
    CreateAndUpdateNewRelicAction: NotRequired[Literal["DENY"]]
    ShareNewRelicAction: NotRequired[Literal["DENY"]]
    UseNewRelicAction: NotRequired[Literal["DENY"]]
    Space: NotRequired[Literal["DENY"]]
    ChatAgent: NotRequired[Literal["DENY"]]
    CreateChatAgents: NotRequired[Literal["DENY"]]
    Research: NotRequired[Literal["DENY"]]
    SelfUpgradeUserRole: NotRequired[Literal["DENY"]]


class CastColumnTypeOperationTypeDef(TypedDict):
    ColumnName: str
    NewColumnType: ColumnDataTypeType
    SubType: NotRequired[ColumnDataSubTypeType]
    Format: NotRequired[str]


class CustomFilterConfigurationTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    NullOption: FilterNullOptionType
    CategoryValue: NotRequired[str]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    ParameterName: NotRequired[str]


class CustomFilterListConfigurationOutputTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    NullOption: FilterNullOptionType
    CategoryValues: NotRequired[list[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]


class FilterListConfigurationOutputTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    CategoryValues: NotRequired[list[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    NullOption: NotRequired[FilterNullOptionType]


class CustomFilterListConfigurationTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    NullOption: FilterNullOptionType
    CategoryValues: NotRequired[Sequence[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]


class FilterListConfigurationTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    CategoryValues: NotRequired[Sequence[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    NullOption: NotRequired[FilterNullOptionType]


class CellValueSynonymOutputTypeDef(TypedDict):
    CellValue: NotRequired[str]
    Synonyms: NotRequired[list[str]]


class CellValueSynonymTypeDef(TypedDict):
    CellValue: NotRequired[str]
    Synonyms: NotRequired[Sequence[str]]


class ClientCredentialsGrantDetailsTypeDef(TypedDict):
    ClientId: str
    ClientSecret: str
    TokenEndpoint: str


class SimpleClusterMarkerTypeDef(TypedDict):
    Color: NotRequired[str]


class CollectiveConstantEntryTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    Value: NotRequired[str]


class CollectiveConstantOutputTypeDef(TypedDict):
    ValueList: NotRequired[list[str]]


class CollectiveConstantTypeDef(TypedDict):
    ValueList: NotRequired[Sequence[str]]


class DataColorTypeDef(TypedDict):
    Color: NotRequired[str]
    DataValue: NotRequired[float]


class CustomColorTypeDef(TypedDict):
    Color: str
    FieldValue: NotRequired[str]
    SpecialValue: NotRequired[SpecialValueType]


ColumnDescriptionTypeDef = TypedDict(
    "ColumnDescriptionTypeDef",
    {
        "Text": NotRequired[str],
    },
)


class ColumnGroupColumnSchemaTypeDef(TypedDict):
    Name: NotRequired[str]


class GeoSpatialColumnGroupOutputTypeDef(TypedDict):
    Name: str
    Columns: list[str]
    CountryCode: NotRequired[Literal["US"]]


class ColumnLevelPermissionRuleOutputTypeDef(TypedDict):
    Principals: NotRequired[list[str]]
    ColumnNames: NotRequired[list[str]]


class ColumnLevelPermissionRuleTypeDef(TypedDict):
    Principals: NotRequired[Sequence[str]]
    ColumnNames: NotRequired[Sequence[str]]


class ColumnSchemaTypeDef(TypedDict):
    Name: NotRequired[str]
    DataType: NotRequired[str]
    GeographicRole: NotRequired[str]


class ColumnToUnpivotTypeDef(TypedDict):
    ColumnName: NotRequired[str]
    NewValue: NotRequired[str]


class LineChartLineStyleSettingsTypeDef(TypedDict):
    LineVisibility: NotRequired[VisibilityType]
    LineInterpolation: NotRequired[LineInterpolationType]
    LineStyle: NotRequired[LineChartLineStyleType]
    LineWidth: NotRequired[str]


class LineChartMarkerStyleSettingsTypeDef(TypedDict):
    MarkerVisibility: NotRequired[VisibilityType]
    MarkerShape: NotRequired[LineChartMarkerShapeType]
    MarkerSize: NotRequired[str]
    MarkerColor: NotRequired[str]


class ComparativeOrderOutputTypeDef(TypedDict):
    UseOrdering: NotRequired[ColumnOrderingTypeType]
    SpecifedOrder: NotRequired[list[str]]
    TreatUndefinedSpecifiedValues: NotRequired[UndefinedSpecifiedValueTypeType]


class ComparativeOrderTypeDef(TypedDict):
    UseOrdering: NotRequired[ColumnOrderingTypeType]
    SpecifedOrder: NotRequired[Sequence[str]]
    TreatUndefinedSpecifiedValues: NotRequired[UndefinedSpecifiedValueTypeType]


class ConditionalFormattingSolidColorTypeDef(TypedDict):
    Expression: str
    Color: NotRequired[str]


class ConditionalFormattingCustomIconOptionsTypeDef(TypedDict):
    Icon: NotRequired[IconType]
    UnicodeIcon: NotRequired[str]


class ConditionalFormattingIconDisplayConfigurationTypeDef(TypedDict):
    IconDisplayOption: NotRequired[Literal["ICON_ONLY"]]


class ConditionalFormattingIconSetTypeDef(TypedDict):
    Expression: str
    IconSetType: NotRequired[ConditionalFormattingIconSetTypeType]


class ConfluenceParametersTypeDef(TypedDict):
    ConfluenceUrl: str


class ContextMenuOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class ContributionAnalysisFactorTypeDef(TypedDict):
    FieldName: NotRequired[str]


class CoordinateTypeDef(TypedDict):
    Latitude: float
    Longitude: float


class CreateAccountSubscriptionRequestTypeDef(TypedDict):
    AuthenticationMethod: AuthenticationMethodOptionType
    AwsAccountId: str
    AccountName: str
    NotificationEmail: str
    Edition: NotRequired[EditionType]
    ActiveDirectoryName: NotRequired[str]
    Realm: NotRequired[str]
    DirectoryId: NotRequired[str]
    AdminGroup: NotRequired[Sequence[str]]
    AuthorGroup: NotRequired[Sequence[str]]
    ReaderGroup: NotRequired[Sequence[str]]
    AdminProGroup: NotRequired[Sequence[str]]
    AuthorProGroup: NotRequired[Sequence[str]]
    ReaderProGroup: NotRequired[Sequence[str]]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    EmailAddress: NotRequired[str]
    ContactNumber: NotRequired[str]
    IAMIdentityCenterInstanceArn: NotRequired[str]


class SignupResponseTypeDef(TypedDict):
    IAMUser: NotRequired[bool]
    userLoginName: NotRequired[str]
    accountName: NotRequired[str]
    directoryType: NotRequired[str]


class ValidationStrategyTypeDef(TypedDict):
    Mode: ValidationStrategyModeType


class DataSetUsageConfigurationTypeDef(TypedDict):
    DisableUseAsDirectQuerySource: NotRequired[bool]
    DisableUseAsImportedSource: NotRequired[bool]


class RowLevelPermissionDataSetTypeDef(TypedDict):
    Arn: str
    PermissionPolicy: RowLevelPermissionPolicyType
    Namespace: NotRequired[str]
    FormatVersion: NotRequired[RowLevelPermissionFormatVersionType]
    Status: NotRequired[StatusType]


class CreateFolderMembershipRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    MemberId: str
    MemberType: MemberTypeType


class FolderMemberTypeDef(TypedDict):
    MemberId: NotRequired[str]
    MemberType: NotRequired[MemberTypeType]


class CreateGroupMembershipRequestTypeDef(TypedDict):
    MemberName: str
    GroupName: str
    AwsAccountId: str
    Namespace: str


class GroupMemberTypeDef(TypedDict):
    Arn: NotRequired[str]
    MemberName: NotRequired[str]


class CreateGroupRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    Description: NotRequired[str]


class GroupTypeDef(TypedDict):
    Arn: NotRequired[str]
    GroupName: NotRequired[str]
    Description: NotRequired[str]
    PrincipalId: NotRequired[str]


class CreateIAMPolicyAssignmentRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    AssignmentStatus: AssignmentStatusType
    Namespace: str
    PolicyArn: NotRequired[str]
    Identities: NotRequired[Mapping[str, Sequence[str]]]


class CreateIngestionRequestTypeDef(TypedDict):
    DataSetId: str
    IngestionId: str
    AwsAccountId: str
    IngestionType: NotRequired[IngestionTypeType]


class CreateRoleMembershipRequestTypeDef(TypedDict):
    MemberName: str
    AwsAccountId: str
    Namespace: str
    Role: RoleType


class CreateTemplateAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str
    TemplateVersionNumber: int


class TemplateAliasTypeDef(TypedDict):
    AliasName: NotRequired[str]
    Arn: NotRequired[str]
    TemplateVersionNumber: NotRequired[int]


class CreateThemeAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str
    ThemeVersionNumber: int


class ThemeAliasTypeDef(TypedDict):
    Arn: NotRequired[str]
    AliasName: NotRequired[str]
    ThemeVersionNumber: NotRequired[int]


class CustomInstructionsTypeDef(TypedDict):
    CustomInstructionsString: str


class DecimalPlacesConfigurationTypeDef(TypedDict):
    DecimalPlaces: int


class NegativeValueConfigurationTypeDef(TypedDict):
    DisplayMode: NegativeValueDisplayModeType


class NullValueFormatConfigurationTypeDef(TypedDict):
    NullString: str


class LocalNavigationConfigurationTypeDef(TypedDict):
    TargetSheetId: str


class CustomActionURLOperationTypeDef(TypedDict):
    URLTemplate: str
    URLTarget: URLTargetConfigurationType


class CustomConnectionParametersTypeDef(TypedDict):
    ConnectionType: NotRequired[str]


class CustomNarrativeOptionsTypeDef(TypedDict):
    Narrative: str


class CustomParameterValuesOutputTypeDef(TypedDict):
    StringValues: NotRequired[list[str]]
    IntegerValues: NotRequired[list[int]]
    DecimalValues: NotRequired[list[float]]
    DateTimeValues: NotRequired[list[datetime]]


InputColumnTypeDef = TypedDict(
    "InputColumnTypeDef",
    {
        "Name": str,
        "Type": InputColumnDataTypeType,
        "Id": NotRequired[str],
        "SubType": NotRequired[ColumnDataSubTypeType],
    },
)


class DataPointDrillUpDownOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DataPointMenuLabelOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DataPointTooltipOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DataQAEnabledOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DataStoriesSharingOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class ExecutiveSummaryOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class ExportToCSVOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class ExportWithHiddenFieldsOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class QuickSuiteActionsOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class SheetControlsOptionTypeDef(TypedDict):
    VisibilityState: NotRequired[DashboardUIStateType]


class SheetLayoutElementMaximizationOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class VisualAxisSortOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class VisualMenuOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DashboardSearchFilterTypeDef(TypedDict):
    Operator: FilterOperatorType
    Name: NotRequired[DashboardFilterAttributeType]
    Value: NotRequired[str]


class DashboardSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    DashboardId: NotRequired[str]
    Name: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    PublishedVersionNumber: NotRequired[int]
    LastPublishedTime: NotRequired[datetime]


class DashboardVersionSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    VersionNumber: NotRequired[int]
    Status: NotRequired[ResourceStatusType]
    SourceEntityArn: NotRequired[str]
    Description: NotRequired[str]


class ExportHiddenFieldsOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DashboardVisualResultTypeDef(TypedDict):
    DashboardId: NotRequired[str]
    DashboardName: NotRequired[str]
    SheetId: NotRequired[str]
    SheetName: NotRequired[str]
    VisualId: NotRequired[str]
    VisualTitle: NotRequired[str]
    VisualSubtitle: NotRequired[str]
    DashboardUrl: NotRequired[str]


class DataAggregationTypeDef(TypedDict):
    DatasetRowDateGranularity: NotRequired[TopicTimeGranularityType]
    DefaultDateColumnName: NotRequired[str]


class DataBarsOptionsTypeDef(TypedDict):
    FieldId: str
    PositiveColor: NotRequired[str]
    NegativeColor: NotRequired[str]


class DataColorPaletteOutputTypeDef(TypedDict):
    Colors: NotRequired[list[str]]
    MinMaxGradient: NotRequired[list[str]]
    EmptyFillColor: NotRequired[str]


class DataColorPaletteTypeDef(TypedDict):
    Colors: NotRequired[Sequence[str]]
    MinMaxGradient: NotRequired[Sequence[str]]
    EmptyFillColor: NotRequired[str]


class DataPathLabelTypeTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldValue: NotRequired[str]
    Visibility: NotRequired[VisibilityType]


class FieldLabelTypeTypeDef(TypedDict):
    FieldId: NotRequired[str]
    Visibility: NotRequired[VisibilityType]


class MaximumLabelTypeTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class MinimumLabelTypeTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class RangeEndsLabelTypeTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class DataPathTypeTypeDef(TypedDict):
    PivotTableDataPathType: NotRequired[PivotTableDataPathTypeType]


class DataPrepListAggregationFunctionTypeDef(TypedDict):
    Separator: str
    Distinct: bool
    InputColumnName: NotRequired[str]


class DataPrepSimpleAggregationFunctionTypeDef(TypedDict):
    FunctionType: DataPrepSimpleAggregationFunctionTypeType
    InputColumnName: NotRequired[str]


class DataSetColumnIdMappingTypeDef(TypedDict):
    SourceColumnId: str
    TargetColumnId: str


class DataSetDateFilterValueOutputTypeDef(TypedDict):
    StaticValue: NotRequired[datetime]


class DataSetNumericFilterValueTypeDef(TypedDict):
    StaticValue: NotRequired[float]


class DataSetSearchFilterTypeDef(TypedDict):
    Operator: FilterOperatorType
    Name: DataSetFilterAttributeType
    Value: str


class DataSetStringFilterValueTypeDef(TypedDict):
    StaticValue: NotRequired[str]


class DataSetStringListFilterValueOutputTypeDef(TypedDict):
    StaticValues: NotRequired[list[str]]


class DataSetStringListFilterValueTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[str]]


class FieldFolderOutputTypeDef(TypedDict):
    description: NotRequired[str]
    columns: NotRequired[list[str]]


OutputColumnTypeDef = TypedDict(
    "OutputColumnTypeDef",
    {
        "Name": NotRequired[str],
        "Id": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[ColumnDataTypeType],
        "SubType": NotRequired[ColumnDataSubTypeType],
    },
)


class KeyPairCredentialsTypeDef(TypedDict):
    KeyPairUsername: str
    PrivateKey: str
    PrivateKeyPassphrase: NotRequired[str]


class WebProxyCredentialsTypeDef(TypedDict):
    WebProxyUsername: str
    WebProxyPassword: str


DataSourceErrorInfoTypeDef = TypedDict(
    "DataSourceErrorInfoTypeDef",
    {
        "Type": NotRequired[DataSourceErrorInfoTypeType],
        "Message": NotRequired[str],
    },
)


class DatabricksParametersTypeDef(TypedDict):
    Host: str
    Port: int
    SqlEndpointPath: str


class ExasolParametersTypeDef(TypedDict):
    Host: str
    Port: int


class ImpalaParametersTypeDef(TypedDict):
    Host: str
    Port: int
    SqlEndpointPath: str
    Database: NotRequired[str]


class JiraParametersTypeDef(TypedDict):
    SiteBaseUrl: str


class MariaDbParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class MySqlParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class OracleParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str
    UseServiceName: NotRequired[bool]


class PostgreSqlParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class PrestoParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Catalog: str


class QBusinessParametersTypeDef(TypedDict):
    ApplicationArn: str


class RdsParametersTypeDef(TypedDict):
    InstanceId: str
    Database: str


class S3KnowledgeBaseParametersTypeDef(TypedDict):
    BucketUrl: str
    RoleArn: NotRequired[str]
    MetadataFilesLocation: NotRequired[str]


class ServiceNowParametersTypeDef(TypedDict):
    SiteBaseUrl: str


class SparkParametersTypeDef(TypedDict):
    Host: str
    Port: int


class SqlServerParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class TeradataParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class TrinoParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Catalog: str


class TwitterParametersTypeDef(TypedDict):
    Query: str
    MaxRows: int


class WebCrawlerParametersTypeDef(TypedDict):
    WebCrawlerAuthType: WebCrawlerAuthTypeType
    UsernameFieldXpath: NotRequired[str]
    PasswordFieldXpath: NotRequired[str]
    UsernameButtonXpath: NotRequired[str]
    PasswordButtonXpath: NotRequired[str]
    LoginPageUrl: NotRequired[str]
    WebProxyHostName: NotRequired[str]
    WebProxyPortNumber: NotRequired[int]


class DataSourceSearchFilterTypeDef(TypedDict):
    Operator: FilterOperatorType
    Name: DataSourceFilterAttributeType
    Value: str


DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSourceId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)


class DateTimeDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[list[datetime]]


class RollingDateConfigurationTypeDef(TypedDict):
    Expression: str
    DataSetIdentifier: NotRequired[str]


class DateTimeValueWhenUnsetConfigurationOutputTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[datetime]


class MappedDataSetParameterTypeDef(TypedDict):
    DataSetIdentifier: str
    DataSetParameterName: str


class DateTimeParameterOutputTypeDef(TypedDict):
    Name: str
    Values: list[datetime]


class SheetControlInfoIconLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    InfoIconText: NotRequired[str]


class DecimalDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[list[float]]


class DecimalDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[float]]


class DecimalValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[float]


class DecimalParameterOutputTypeDef(TypedDict):
    Name: str
    Values: list[float]


class DecimalParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[float]


class FilterSelectableValuesOutputTypeDef(TypedDict):
    Values: NotRequired[list[str]]


class FilterSelectableValuesTypeDef(TypedDict):
    Values: NotRequired[Sequence[str]]


class DeleteAccountCustomPermissionRequestTypeDef(TypedDict):
    AwsAccountId: str


class DeleteAccountCustomizationRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]


class DeleteAccountSubscriptionRequestTypeDef(TypedDict):
    AwsAccountId: str


class DeleteActionConnectorRequestTypeDef(TypedDict):
    AwsAccountId: str
    ActionConnectorId: str


class DeleteAnalysisRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    RecoveryWindowInDays: NotRequired[int]
    ForceDeleteWithoutRecovery: NotRequired[bool]


class DeleteBrandAssignmentRequestTypeDef(TypedDict):
    AwsAccountId: str


class DeleteBrandRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str


class DeleteCustomPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str


class DeleteDashboardRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: NotRequired[int]


class DeleteDataSetRefreshPropertiesRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DeleteDataSetRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DeleteDataSourceRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str


class DeleteDefaultQBusinessApplicationRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]


class DeleteFolderMembershipRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    MemberId: str
    MemberType: MemberTypeType


class DeleteFolderRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str


class DeleteGroupMembershipRequestTypeDef(TypedDict):
    MemberName: str
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DeleteGroupRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DeleteIAMPolicyAssignmentRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    Namespace: str


class DeleteIdentityPropagationConfigRequestTypeDef(TypedDict):
    AwsAccountId: str
    Service: ServiceTypeType


class DeleteNamespaceRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str


class DeleteRefreshScheduleRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    ScheduleId: str


class DeleteRoleCustomPermissionRequestTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class DeleteRoleMembershipRequestTypeDef(TypedDict):
    MemberName: str
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class DeleteTemplateAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str


class DeleteTemplateRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    VersionNumber: NotRequired[int]


class DeleteThemeAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str


class DeleteThemeRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    VersionNumber: NotRequired[int]


class DeleteTopicRefreshScheduleRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetId: str


class DeleteTopicRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class DeleteUserByPrincipalIdRequestTypeDef(TypedDict):
    PrincipalId: str
    AwsAccountId: str
    Namespace: str


class DeleteUserCustomPermissionRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str


class DeleteUserRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str


class DeleteVPCConnectionRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str


class DescribeAccountCustomPermissionRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeAccountCustomizationRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]
    Resolved: NotRequired[bool]


class DescribeAccountSettingsRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeAccountSubscriptionRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeActionConnectorPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    ActionConnectorId: str


class ResourcePermissionOutputTypeDef(TypedDict):
    Principal: str
    Actions: list[str]


class DescribeActionConnectorRequestTypeDef(TypedDict):
    AwsAccountId: str
    ActionConnectorId: str


class DescribeAnalysisDefinitionRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str


class DescribeAnalysisPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str


class DescribeAnalysisRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str


class DescribeAssetBundleExportJobRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleExportJobId: str


class DescribeAssetBundleImportJobRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleImportJobId: str


class DescribeBrandAssignmentRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeBrandPublishedVersionRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str


class DescribeBrandRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    VersionId: NotRequired[str]


class DescribeCustomPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str


class DescribeDashboardDefinitionRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeDashboardPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str


class DescribeDashboardRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeDashboardSnapshotJobRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str


class DescribeDashboardSnapshotJobResultRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str


class SnapshotJobErrorInfoTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]
    ErrorType: NotRequired[str]


class DescribeDashboardsQAConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeDataSetPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DescribeDataSetRefreshPropertiesRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DescribeDataSetRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DescribeDataSourcePermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str


class DescribeDataSourceRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str


class DescribeDefaultQBusinessApplicationRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeFolderPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeFolderRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str


class DescribeFolderResolvedPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class FolderTypeDef(TypedDict):
    FolderId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    FolderType: NotRequired[FolderTypeType]
    FolderPath: NotRequired[list[str]]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    SharingModel: NotRequired[SharingModelType]


class DescribeGroupMembershipRequestTypeDef(TypedDict):
    MemberName: str
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DescribeGroupRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DescribeIAMPolicyAssignmentRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    Namespace: str


class IAMPolicyAssignmentTypeDef(TypedDict):
    AwsAccountId: NotRequired[str]
    AssignmentId: NotRequired[str]
    AssignmentName: NotRequired[str]
    PolicyArn: NotRequired[str]
    Identities: NotRequired[dict[str, list[str]]]
    AssignmentStatus: NotRequired[AssignmentStatusType]


class DescribeIngestionRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    IngestionId: str


class DescribeIpRestrictionRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeKeyRegistrationRequestTypeDef(TypedDict):
    AwsAccountId: str
    DefaultKeyOnly: NotRequired[bool]


class QDataKeyTypeDef(TypedDict):
    QDataKeyArn: NotRequired[str]
    QDataKeyType: NotRequired[QDataKeyTypeType]


class RegisteredCustomerManagedKeyTypeDef(TypedDict):
    KeyArn: NotRequired[str]
    DefaultKey: NotRequired[bool]


class DescribeNamespaceRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str


class DescribeQPersonalizationConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeQuickSightQSearchConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeRefreshScheduleRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    ScheduleId: str


class DescribeRoleCustomPermissionRequestTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class DescribeSelfUpgradeConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str


class SelfUpgradeConfigurationTypeDef(TypedDict):
    SelfUpgradeStatus: NotRequired[SelfUpgradeStatusType]


class DescribeTemplateAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str


class DescribeTemplateDefinitionRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeTemplatePermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str


class DescribeTemplateRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeThemeAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str


class DescribeThemePermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str


class DescribeThemeRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeTopicPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class DescribeTopicRefreshRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    RefreshId: str


class TopicRefreshDetailsTypeDef(TypedDict):
    RefreshArn: NotRequired[str]
    RefreshId: NotRequired[str]
    RefreshStatus: NotRequired[TopicRefreshStatusType]


class DescribeTopicRefreshScheduleRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetId: str


class TopicRefreshScheduleOutputTypeDef(TypedDict):
    IsEnabled: bool
    BasedOnSpiceSchedule: bool
    StartingAt: NotRequired[datetime]
    Timezone: NotRequired[str]
    RepeatAt: NotRequired[str]
    TopicScheduleType: NotRequired[TopicScheduleTypeType]


class DescribeTopicRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class DescribeUserRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str


class UserTypeDef(TypedDict):
    Arn: NotRequired[str]
    UserName: NotRequired[str]
    Email: NotRequired[str]
    Role: NotRequired[UserRoleType]
    IdentityType: NotRequired[IdentityTypeType]
    Active: NotRequired[bool]
    PrincipalId: NotRequired[str]
    CustomPermissionsName: NotRequired[str]
    ExternalLoginFederationProviderType: NotRequired[str]
    ExternalLoginFederationProviderUrl: NotRequired[str]
    ExternalLoginId: NotRequired[str]


class DescribeVPCConnectionRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str


class DestinationTableSourceTypeDef(TypedDict):
    TransformOperationId: str


class NegativeFormatTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]


class DonutCenterOptionsTypeDef(TypedDict):
    LabelVisibility: NotRequired[VisibilityType]


class ListControlSelectAllOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "Type": NotRequired[IngestionErrorTypeType],
        "Message": NotRequired[str],
    },
)


class ExcludePeriodConfigurationTypeDef(TypedDict):
    Amount: int
    Granularity: TimeGranularityType
    Status: NotRequired[WidgetStatusType]


class FailedKeyRegistrationEntryTypeDef(TypedDict):
    Message: str
    StatusCode: int
    SenderFault: bool
    KeyArn: NotRequired[str]


class FieldFolderTypeDef(TypedDict):
    description: NotRequired[str]
    columns: NotRequired[Sequence[str]]


class FieldSortTypeDef(TypedDict):
    FieldId: str
    Direction: SortDirectionType


class FieldTooltipItemTypeDef(TypedDict):
    FieldId: str
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    TooltipTarget: NotRequired[TooltipTargetType]


class GeospatialMapStyleOptionsTypeDef(TypedDict):
    BaseMapStyle: NotRequired[BaseMapStyleTypeType]


class IdentifierTypeDef(TypedDict):
    Identity: str


class SameSheetTargetVisualConfigurationOutputTypeDef(TypedDict):
    TargetVisuals: NotRequired[list[str]]
    TargetVisualOptions: NotRequired[Literal["ALL_VISUALS"]]


class SameSheetTargetVisualConfigurationTypeDef(TypedDict):
    TargetVisuals: NotRequired[Sequence[str]]
    TargetVisualOptions: NotRequired[Literal["ALL_VISUALS"]]


class FlowSummaryTypeDef(TypedDict):
    Arn: str
    FlowId: str
    Name: str
    CreatedTime: datetime
    Description: NotRequired[str]
    CreatedBy: NotRequired[str]
    LastUpdatedTime: NotRequired[datetime]
    LastUpdatedBy: NotRequired[str]
    PublishState: NotRequired[FlowPublishStateType]
    RunCount: NotRequired[int]
    UserCount: NotRequired[int]
    LastPublishedBy: NotRequired[str]
    LastPublishedAt: NotRequired[datetime]


class FolderSearchFilterTypeDef(TypedDict):
    Operator: NotRequired[FilterOperatorType]
    Name: NotRequired[FolderFilterAttributeType]
    Value: NotRequired[str]


class FolderSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    FolderId: NotRequired[str]
    Name: NotRequired[str]
    FolderType: NotRequired[FolderTypeType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    SharingModel: NotRequired[SharingModelType]


class FontSizeTypeDef(TypedDict):
    Relative: NotRequired[RelativeFontSizeType]
    Absolute: NotRequired[str]


class FontWeightTypeDef(TypedDict):
    Name: NotRequired[FontWeightNameType]


class FontTypeDef(TypedDict):
    FontFamily: NotRequired[str]


class TimeBasedForecastPropertiesTypeDef(TypedDict):
    PeriodsForward: NotRequired[int]
    PeriodsBackward: NotRequired[int]
    UpperBoundary: NotRequired[float]
    LowerBoundary: NotRequired[float]
    PredictionInterval: NotRequired[int]
    Seasonality: NotRequired[int]


class WhatIfPointScenarioOutputTypeDef(TypedDict):
    Date: datetime
    Value: float


class WhatIfRangeScenarioOutputTypeDef(TypedDict):
    StartDate: datetime
    EndDate: datetime
    Value: float


class FreeFormLayoutScreenCanvasSizeOptionsTypeDef(TypedDict):
    OptimizedViewPortWidth: str


class FreeFormLayoutElementBackgroundStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Color: NotRequired[str]


class FreeFormLayoutElementBorderStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Color: NotRequired[str]
    Width: NotRequired[str]


class LoadingAnimationTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class GaugeChartColorConfigurationTypeDef(TypedDict):
    ForegroundColor: NotRequired[str]
    BackgroundColor: NotRequired[str]


class SessionTagTypeDef(TypedDict):
    Key: str
    Value: str


class GeneratedAnswerResultTypeDef(TypedDict):
    QuestionText: NotRequired[str]
    AnswerStatus: NotRequired[GeneratedAnswerStatusType]
    TopicId: NotRequired[str]
    TopicName: NotRequired[str]
    Restatement: NotRequired[str]
    QuestionId: NotRequired[str]
    AnswerId: NotRequired[str]
    QuestionUrl: NotRequired[str]


class GeoSpatialColumnGroupTypeDef(TypedDict):
    Name: str
    Columns: Sequence[str]
    CountryCode: NotRequired[Literal["US"]]


class GeocoderHierarchyTypeDef(TypedDict):
    Country: NotRequired[str]
    State: NotRequired[str]
    County: NotRequired[str]
    City: NotRequired[str]
    PostCode: NotRequired[str]


class GeospatialCategoricalDataColorTypeDef(TypedDict):
    Color: str
    DataValue: str


class GeospatialCircleRadiusTypeDef(TypedDict):
    Radius: NotRequired[float]


class GeospatialLineWidthTypeDef(TypedDict):
    LineWidth: NotRequired[float]


class GeospatialSolidColorTypeDef(TypedDict):
    Color: str
    State: NotRequired[GeospatialColorStateType]


class GeospatialCoordinateBoundsTypeDef(TypedDict):
    North: float
    South: float
    West: float
    East: float


class GeospatialStaticFileSourceTypeDef(TypedDict):
    StaticFileId: str


class GeospatialGradientStepColorTypeDef(TypedDict):
    Color: str
    DataValue: float


class GeospatialHeatmapDataColorTypeDef(TypedDict):
    Color: str


class GeospatialMapStyleTypeDef(TypedDict):
    BaseMapStyle: NotRequired[BaseMapStyleTypeType]
    BackgroundColor: NotRequired[str]
    BaseMapVisibility: NotRequired[VisibilityType]


class GeospatialNullSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[str]
    StrokeColor: NotRequired[str]
    StrokeWidth: NotRequired[float]


class GetDashboardEmbedUrlRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    IdentityType: EmbeddingIdentityTypeType
    SessionLifetimeInMinutes: NotRequired[int]
    UndoRedoDisabled: NotRequired[bool]
    ResetDisabled: NotRequired[bool]
    StatePersistenceEnabled: NotRequired[bool]
    UserArn: NotRequired[str]
    Namespace: NotRequired[str]
    AdditionalDashboardIds: NotRequired[Sequence[str]]


class GetFlowMetadataInputTypeDef(TypedDict):
    AwsAccountId: str
    FlowId: str


class GetFlowPermissionsInputTypeDef(TypedDict):
    AwsAccountId: str
    FlowId: str


class PermissionOutputTypeDef(TypedDict):
    Actions: list[str]
    Principal: str


class UserIdentifierTypeDef(TypedDict):
    UserName: NotRequired[str]
    Email: NotRequired[str]
    UserArn: NotRequired[str]


class GetSessionEmbedUrlRequestTypeDef(TypedDict):
    AwsAccountId: str
    EntryPoint: NotRequired[str]
    SessionLifetimeInMinutes: NotRequired[int]
    UserArn: NotRequired[str]


class TableBorderOptionsTypeDef(TypedDict):
    Color: NotRequired[str]
    Thickness: NotRequired[int]
    Style: NotRequired[TableBorderStyleType]


class GradientStopTypeDef(TypedDict):
    GradientOffset: float
    DataValue: NotRequired[float]
    Color: NotRequired[str]


class GridLayoutScreenCanvasSizeOptionsTypeDef(TypedDict):
    ResizeOption: ResizeOptionType
    OptimizedViewPortWidth: NotRequired[str]


class GridLayoutElementBackgroundStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Color: NotRequired[str]


class GridLayoutElementBorderStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Color: NotRequired[str]
    Width: NotRequired[str]


class GroupSearchFilterTypeDef(TypedDict):
    Operator: Literal["StartsWith"]
    Name: Literal["GROUP_NAME"]
    Value: str


class GutterStyleTypeDef(TypedDict):
    Show: NotRequired[bool]


class IAMPolicyAssignmentSummaryTypeDef(TypedDict):
    AssignmentName: NotRequired[str]
    AssignmentStatus: NotRequired[AssignmentStatusType]


class ImageSourceTypeDef(TypedDict):
    PublicUrl: NotRequired[str]
    S3Uri: NotRequired[str]


class ImageMenuOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class LookbackWindowTypeDef(TypedDict):
    ColumnName: str
    Size: int
    SizeUnit: LookbackWindowSizeUnitType


class QueueInfoTypeDef(TypedDict):
    WaitingOnIngestion: str
    QueuedIngestion: str


class RowInfoTypeDef(TypedDict):
    RowsIngested: NotRequired[int]
    RowsDropped: NotRequired[int]
    TotalRowsInDataset: NotRequired[int]


class IntegerDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[list[int]]


class IntegerDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[int]]


class IntegerValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[int]


class IntegerParameterOutputTypeDef(TypedDict):
    Name: str
    Values: list[int]


class IntegerParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[int]


class JoinKeyPropertiesTypeDef(TypedDict):
    UniqueKey: NotRequired[bool]


class OutputColumnNameOverrideTypeDef(TypedDict):
    OutputColumnName: str
    SourceColumnName: NotRequired[str]


KPISparklineOptionsTypeDef = TypedDict(
    "KPISparklineOptionsTypeDef",
    {
        "Type": KPISparklineTypeType,
        "Visibility": NotRequired[VisibilityType],
        "Color": NotRequired[str],
        "TooltipVisibility": NotRequired[VisibilityType],
    },
)


class ProgressBarOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class SecondaryValueOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class TrendArrowOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


KPIVisualStandardLayoutTypeDef = TypedDict(
    "KPIVisualStandardLayoutTypeDef",
    {
        "Type": KPIVisualStandardLayoutTypeType,
    },
)


class MissingDataConfigurationTypeDef(TypedDict):
    TreatmentOption: NotRequired[MissingDataTreatmentOptionType]


class ResourcePermissionTypeDef(TypedDict):
    Principal: str
    Actions: Sequence[str]


class ListActionConnectorsRequestTypeDef(TypedDict):
    AwsAccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAnalysesRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAssetBundleExportJobsRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAssetBundleImportJobsRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListBrandsRequestTypeDef(TypedDict):
    AwsAccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListControlSearchOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class ListCustomPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDashboardVersionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDashboardsRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDataSetsRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDataSourcesRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFlowsInputTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFolderMembersRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MemberIdArnPairTypeDef(TypedDict):
    MemberId: NotRequired[str]
    MemberArn: NotRequired[str]


class ListFoldersForResourceRequestTypeDef(TypedDict):
    AwsAccountId: str
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFoldersRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListGroupMembershipsRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListGroupsRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIAMPolicyAssignmentsForUserRequestTypeDef(TypedDict):
    AwsAccountId: str
    UserName: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIAMPolicyAssignmentsRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    AssignmentStatus: NotRequired[AssignmentStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIdentityPropagationConfigsRequestTypeDef(TypedDict):
    AwsAccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListIngestionsRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListNamespacesRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListRefreshSchedulesRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class ListRoleMembershipsRequestTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListSelfUpgradesRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SelfUpgradeRequestDetailTypeDef(TypedDict):
    UpgradeRequestId: NotRequired[str]
    UserName: NotRequired[str]
    OriginalRole: NotRequired[UserRoleType]
    RequestedRole: NotRequired[UserRoleType]
    RequestNote: NotRequired[str]
    CreationTime: NotRequired[int]
    RequestStatus: NotRequired[SelfUpgradeRequestStatusType]
    lastUpdateAttemptTime: NotRequired[int]
    lastUpdateFailureReason: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


class ListTemplateAliasesRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTemplateVersionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TemplateVersionSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    VersionNumber: NotRequired[int]
    CreatedTime: NotRequired[datetime]
    Status: NotRequired[ResourceStatusType]
    Description: NotRequired[str]


class ListTemplatesRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TemplateSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    TemplateId: NotRequired[str]
    Name: NotRequired[str]
    LatestVersionNumber: NotRequired[int]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class ListThemeAliasesRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListThemeVersionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ThemeVersionSummaryTypeDef(TypedDict):
    VersionNumber: NotRequired[int]
    Arn: NotRequired[str]
    Description: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Status: NotRequired[ResourceStatusType]


ListThemesRequestTypeDef = TypedDict(
    "ListThemesRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Type": NotRequired[ThemeTypeType],
    },
)


class ThemeSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    ThemeId: NotRequired[str]
    LatestVersionNumber: NotRequired[int]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class ListTopicRefreshSchedulesRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class ListTopicReviewedAnswersRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class ListTopicsRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TopicSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    TopicId: NotRequired[str]
    Name: NotRequired[str]
    UserExperienceVersion: NotRequired[TopicUserExperienceVersionType]


class ListUserGroupsRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListUsersRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListVPCConnectionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class LongFormatTextTypeDef(TypedDict):
    PlainText: NotRequired[str]
    RichText: NotRequired[str]


class ManifestFileLocationTypeDef(TypedDict):
    Bucket: str
    Key: str


class MarginStyleTypeDef(TypedDict):
    Show: NotRequired[bool]


class NamedEntityDefinitionMetricOutputTypeDef(TypedDict):
    Aggregation: NotRequired[NamedEntityAggTypeType]
    AggregationFunctionParameters: NotRequired[dict[str, str]]


class NamedEntityDefinitionMetricTypeDef(TypedDict):
    Aggregation: NotRequired[NamedEntityAggTypeType]
    AggregationFunctionParameters: NotRequired[Mapping[str, str]]


class NamedEntityRefTypeDef(TypedDict):
    NamedEntityName: NotRequired[str]


NamespaceErrorTypeDef = TypedDict(
    "NamespaceErrorTypeDef",
    {
        "Type": NotRequired[NamespaceErrorTypeType],
        "Message": NotRequired[str],
    },
)


class NetworkInterfaceTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    ErrorMessage: NotRequired[str]
    Status: NotRequired[NetworkInterfaceStatusType]
    NetworkInterfaceId: NotRequired[str]


class NewDefaultValuesOutputTypeDef(TypedDict):
    StringStaticValues: NotRequired[list[str]]
    DecimalStaticValues: NotRequired[list[float]]
    DateTimeStaticValues: NotRequired[list[datetime]]
    IntegerStaticValues: NotRequired[list[int]]


class NumericRangeFilterValueTypeDef(TypedDict):
    StaticValue: NotRequired[float]
    Parameter: NotRequired[str]


class ThousandSeparatorOptionsTypeDef(TypedDict):
    Symbol: NotRequired[NumericSeparatorSymbolType]
    Visibility: NotRequired[VisibilityType]
    GroupingStyle: NotRequired[DigitGroupingStyleType]


class PercentileAggregationTypeDef(TypedDict):
    PercentileValue: NotRequired[float]


class StringParameterOutputTypeDef(TypedDict):
    Name: str
    Values: list[str]


class StringParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class PercentVisibleRangeTypeDef(TypedDict):
    From: NotRequired[float]
    To: NotRequired[float]


class UniqueKeyOutputTypeDef(TypedDict):
    ColumnNames: list[str]


class UniqueKeyTypeDef(TypedDict):
    ColumnNames: Sequence[str]


class PermissionTypeDef(TypedDict):
    Actions: Sequence[str]
    Principal: str


class PivotedLabelTypeDef(TypedDict):
    LabelName: str
    NewColumnName: str
    NewColumnId: str


class PivotTableConditionalFormattingScopeTypeDef(TypedDict):
    Role: NotRequired[PivotTableConditionalFormattingScopeRoleType]


class PivotTablePaginatedReportOptionsTypeDef(TypedDict):
    VerticalOverflowVisibility: NotRequired[VisibilityType]
    OverflowColumnHeaderVisibility: NotRequired[VisibilityType]


class PivotTableFieldOptionTypeDef(TypedDict):
    FieldId: str
    CustomLabel: NotRequired[str]
    Visibility: NotRequired[VisibilityType]


class PivotTableFieldSubtotalOptionsTypeDef(TypedDict):
    FieldId: NotRequired[str]


class PivotTableRowsLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CustomLabel: NotRequired[str]


class RowAlternateColorOptionsOutputTypeDef(TypedDict):
    Status: NotRequired[WidgetStatusType]
    RowAlternateColors: NotRequired[list[str]]
    UsePrimaryBackgroundColor: NotRequired[WidgetStatusType]


class RowAlternateColorOptionsTypeDef(TypedDict):
    Status: NotRequired[WidgetStatusType]
    RowAlternateColors: NotRequired[Sequence[str]]
    UsePrimaryBackgroundColor: NotRequired[WidgetStatusType]


class PluginVisualItemsLimitConfigurationTypeDef(TypedDict):
    ItemsLimit: NotRequired[int]


class PluginVisualPropertyTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class PredictQAResultsRequestTypeDef(TypedDict):
    AwsAccountId: str
    QueryText: str
    IncludeQuickSightQIndex: NotRequired[IncludeQuickSightQIndexType]
    IncludeGeneratedAnswer: NotRequired[IncludeGeneratedAnswerType]
    MaxTopicsToConsider: NotRequired[int]


class RadarChartAreaStyleSettingsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class RangeConstantTypeDef(TypedDict):
    Minimum: NotRequired[str]
    Maximum: NotRequired[str]


class ReadAPIKeyConnectionMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    Email: NotRequired[str]


class ReadBasicAuthConnectionMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    Username: str


class ReadIamConnectionMetadataTypeDef(TypedDict):
    RoleArn: str
    SourceArn: str


class ReadNoneConnectionMetadataTypeDef(TypedDict):
    BaseEndpoint: str


class ReadAuthorizationCodeGrantDetailsTypeDef(TypedDict):
    ClientId: str
    TokenEndpoint: str
    AuthorizationEndpoint: str


class ReadClientCredentialsGrantDetailsTypeDef(TypedDict):
    ClientId: str
    TokenEndpoint: str


class RecentSnapshotsConfigurationsTypeDef(TypedDict):
    Enabled: bool


class RedshiftIAMParametersOutputTypeDef(TypedDict):
    RoleArn: str
    DatabaseUser: NotRequired[str]
    DatabaseGroups: NotRequired[list[str]]
    AutoCreateDatabaseUser: NotRequired[bool]


class RedshiftIAMParametersTypeDef(TypedDict):
    RoleArn: str
    DatabaseUser: NotRequired[str]
    DatabaseGroups: NotRequired[Sequence[str]]
    AutoCreateDatabaseUser: NotRequired[bool]


class ReferenceLineCustomLabelConfigurationTypeDef(TypedDict):
    CustomLabel: str


class ReferenceLineStaticDataConfigurationTypeDef(TypedDict):
    Value: float


ReferenceLineStyleConfigurationTypeDef = TypedDict(
    "ReferenceLineStyleConfigurationTypeDef",
    {
        "Pattern": NotRequired[ReferenceLinePatternTypeType],
        "Color": NotRequired[str],
    },
)


class RefreshFailureEmailAlertTypeDef(TypedDict):
    AlertStatus: NotRequired[RefreshFailureAlertStatusType]


class ScheduleRefreshOnEntityTypeDef(TypedDict):
    DayOfWeek: NotRequired[DayOfWeekType]
    DayOfMonth: NotRequired[str]


class SchedulesConfigurationsTypeDef(TypedDict):
    Enabled: bool


class StatePersistenceConfigurationsTypeDef(TypedDict):
    Enabled: bool


class ThresholdAlertsConfigurationsTypeDef(TypedDict):
    Enabled: bool


class RegisteredUserGenerativeQnAEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: NotRequired[str]


class RegisteredUserQSearchBarEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: NotRequired[str]


class RenameColumnOperationTypeDef(TypedDict):
    ColumnName: str
    NewColumnName: str


class RestoreAnalysisRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    RestoreToFolders: NotRequired[bool]


class RowLevelPermissionTagRuleTypeDef(TypedDict):
    TagKey: str
    ColumnName: str
    TagMultiValueDelimiter: NotRequired[str]
    MatchAllValue: NotRequired[str]


class S3BucketConfigurationTypeDef(TypedDict):
    BucketName: str
    BucketPrefix: str
    BucketRegion: str


class UploadSettingsTypeDef(TypedDict):
    Format: NotRequired[FileFormatType]
    StartFromRow: NotRequired[int]
    ContainsHeader: NotRequired[bool]
    TextQualifier: NotRequired[TextQualifierType]
    Delimiter: NotRequired[str]
    CustomCellAddressRange: NotRequired[str]


class TablePathElementTypeDef(TypedDict):
    Name: NotRequired[str]
    Id: NotRequired[str]


class SearchFlowsFilterTypeDef(TypedDict):
    Name: FieldNameType
    Operator: SearchFilterOperatorType
    Value: str


class TopicSearchFilterTypeDef(TypedDict):
    Operator: TopicFilterOperatorType
    Name: TopicFilterAttributeType
    Value: str


class SpacingTypeDef(TypedDict):
    Top: NotRequired[str]
    Bottom: NotRequired[str]
    Left: NotRequired[str]
    Right: NotRequired[str]


class SheetVisualScopingConfigurationOutputTypeDef(TypedDict):
    SheetId: str
    Scope: FilterVisualScopeType
    VisualIds: NotRequired[list[str]]


class SheetVisualScopingConfigurationTypeDef(TypedDict):
    SheetId: str
    Scope: FilterVisualScopeType
    VisualIds: NotRequired[Sequence[str]]


class SemanticEntityTypeOutputTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[dict[str, str]]


class SemanticEntityTypeTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[Mapping[str, str]]


class SemanticTypeOutputTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[dict[str, str]]
    TruthyCellValue: NotRequired[str]
    TruthyCellValueSynonyms: NotRequired[list[str]]
    FalseyCellValue: NotRequired[str]
    FalseyCellValueSynonyms: NotRequired[list[str]]


class SemanticTypeTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[Mapping[str, str]]
    TruthyCellValue: NotRequired[str]
    TruthyCellValueSynonyms: NotRequired[Sequence[str]]
    FalseyCellValue: NotRequired[str]
    FalseyCellValueSynonyms: NotRequired[Sequence[str]]


class SheetBackgroundStyleTypeDef(TypedDict):
    Color: NotRequired[str]
    Gradient: NotRequired[str]


class SheetElementConfigurationOverridesTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class SheetImageScalingConfigurationTypeDef(TypedDict):
    ScalingType: NotRequired[SheetImageScalingTypeType]


class SheetImageStaticFileSourceTypeDef(TypedDict):
    StaticFileId: str


class SheetImageTooltipTextTypeDef(TypedDict):
    PlainText: NotRequired[str]


SheetLayoutGroupMemberTypeDef = TypedDict(
    "SheetLayoutGroupMemberTypeDef",
    {
        "Id": str,
        "Type": SheetLayoutGroupMemberTypeType,
    },
)


class ShortFormatTextTypeDef(TypedDict):
    PlainText: NotRequired[str]
    RichText: NotRequired[str]


class YAxisOptionsTypeDef(TypedDict):
    YAxis: Literal["PRIMARY_Y_AXIS"]


class SlotTypeDef(TypedDict):
    SlotId: NotRequired[str]
    VisualId: NotRequired[str]


class SmallMultiplesAxisPropertiesTypeDef(TypedDict):
    Scale: NotRequired[SmallMultiplesAxisScaleType]
    Placement: NotRequired[SmallMultiplesAxisPlacementType]


class SnapshotAnonymousUserRedactedTypeDef(TypedDict):
    RowLevelPermissionTagKeys: NotRequired[list[str]]


class SnapshotFileSheetSelectionOutputTypeDef(TypedDict):
    SheetId: str
    SelectionScope: SnapshotFileSheetSelectionScopeType
    VisualIds: NotRequired[list[str]]


class SnapshotFileSheetSelectionTypeDef(TypedDict):
    SheetId: str
    SelectionScope: SnapshotFileSheetSelectionScopeType
    VisualIds: NotRequired[Sequence[str]]


class SnapshotJobResultErrorInfoTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]
    ErrorType: NotRequired[str]


class StartDashboardSnapshotJobScheduleRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    ScheduleId: str


class StaticFileS3SourceOptionsTypeDef(TypedDict):
    BucketName: str
    ObjectKey: str
    Region: str


class StaticFileUrlSourceOptionsTypeDef(TypedDict):
    Url: str


class StringDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[list[str]]


class StringDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[str]]


class StringValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[str]


class TableStyleTargetTypeDef(TypedDict):
    CellType: StyledCellTypeType


class SuccessfulKeyRegistrationEntryTypeDef(TypedDict):
    KeyArn: str
    StatusCode: int


class TableCellImageSizingConfigurationTypeDef(TypedDict):
    TableCellImageScalingConfiguration: NotRequired[TableCellImageScalingConfigurationType]


class TablePaginatedReportOptionsTypeDef(TypedDict):
    VerticalOverflowVisibility: NotRequired[VisibilityType]
    OverflowColumnHeaderVisibility: NotRequired[VisibilityType]


class TableFieldCustomIconContentTypeDef(TypedDict):
    Icon: NotRequired[Literal["LINK"]]


class TablePinnedFieldOptionsOutputTypeDef(TypedDict):
    PinnedLeftFields: NotRequired[list[str]]


class TransposedTableOptionTypeDef(TypedDict):
    ColumnType: TransposedColumnTypeType
    ColumnIndex: NotRequired[int]
    ColumnWidth: NotRequired[str]


class TablePinnedFieldOptionsTypeDef(TypedDict):
    PinnedLeftFields: NotRequired[Sequence[str]]


class TemplateSourceTemplateTypeDef(TypedDict):
    Arn: str


class TextControlPlaceholderOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class TextBoxMenuOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


UIColorPaletteTypeDef = TypedDict(
    "UIColorPaletteTypeDef",
    {
        "PrimaryForeground": NotRequired[str],
        "PrimaryBackground": NotRequired[str],
        "SecondaryForeground": NotRequired[str],
        "SecondaryBackground": NotRequired[str],
        "Accent": NotRequired[str],
        "AccentForeground": NotRequired[str],
        "Danger": NotRequired[str],
        "DangerForeground": NotRequired[str],
        "Warning": NotRequired[str],
        "WarningForeground": NotRequired[str],
        "Success": NotRequired[str],
        "SuccessForeground": NotRequired[str],
        "Dimension": NotRequired[str],
        "DimensionForeground": NotRequired[str],
        "Measure": NotRequired[str],
        "MeasureForeground": NotRequired[str],
    },
)
ThemeErrorTypeDef = TypedDict(
    "ThemeErrorTypeDef",
    {
        "Type": NotRequired[Literal["INTERNAL_FAILURE"]],
        "Message": NotRequired[str],
    },
)


class TopicConfigOptionsTypeDef(TypedDict):
    QBusinessInsightsEnabled: NotRequired[bool]


TopicIRComparisonMethodTypeDef = TypedDict(
    "TopicIRComparisonMethodTypeDef",
    {
        "Type": NotRequired[ComparisonMethodTypeType],
        "Period": NotRequired[TopicTimeGranularityType],
        "WindowSize": NotRequired[int],
    },
)
VisualOptionsTypeDef = TypedDict(
    "VisualOptionsTypeDef",
    {
        "type": NotRequired[str],
    },
)


class TopicSingularFilterConstantTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    SingularConstant: NotRequired[str]


class TotalAggregationFunctionTypeDef(TypedDict):
    SimpleTotalAggregationFunction: NotRequired[SimpleTotalAggregationFunctionType]


class UntagColumnOperationOutputTypeDef(TypedDict):
    ColumnName: str
    TagNames: list[ColumnTagNameType]


class UntagColumnOperationTypeDef(TypedDict):
    ColumnName: str
    TagNames: Sequence[ColumnTagNameType]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateAccountCustomPermissionRequestTypeDef(TypedDict):
    CustomPermissionsName: str
    AwsAccountId: str


class UpdateAccountSettingsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DefaultNamespace: str
    NotificationEmail: NotRequired[str]
    TerminationProtectionEnabled: NotRequired[bool]


class UpdateApplicationWithTokenExchangeGrantRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str


class UpdateBrandAssignmentRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandArn: str


class UpdateBrandPublishedVersionRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    VersionId: str


class UpdateDashboardLinksRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    LinkEntities: Sequence[str]


class UpdateDashboardPublishedVersionRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: int


class UpdateDashboardsQAConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardsQAStatus: DashboardsQAStatusType


class UpdateDefaultQBusinessApplicationRequestTypeDef(TypedDict):
    AwsAccountId: str
    ApplicationId: str
    Namespace: NotRequired[str]


class UpdateFolderRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Name: str


class UpdateGroupRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    Description: NotRequired[str]


class UpdateIAMPolicyAssignmentRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    Namespace: str
    AssignmentStatus: NotRequired[AssignmentStatusType]
    PolicyArn: NotRequired[str]
    Identities: NotRequired[Mapping[str, Sequence[str]]]


class UpdateIdentityPropagationConfigRequestTypeDef(TypedDict):
    AwsAccountId: str
    Service: ServiceTypeType
    AuthorizedTargets: NotRequired[Sequence[str]]


class UpdateIpRestrictionRequestTypeDef(TypedDict):
    AwsAccountId: str
    IpRestrictionRuleMap: NotRequired[Mapping[str, str]]
    VpcIdRestrictionRuleMap: NotRequired[Mapping[str, str]]
    VpcEndpointIdRestrictionRuleMap: NotRequired[Mapping[str, str]]
    Enabled: NotRequired[bool]


class UpdatePublicSharingSettingsRequestTypeDef(TypedDict):
    AwsAccountId: str
    PublicSharingEnabled: NotRequired[bool]


class UpdateQPersonalizationConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str
    PersonalizationMode: PersonalizationModeType


class UpdateQuickSightQSearchConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str
    QSearchStatus: QSearchStatusType


class UpdateRoleCustomPermissionRequestTypeDef(TypedDict):
    CustomPermissionsName: str
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class UpdateSPICECapacityConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str
    PurchaseMode: PurchaseModeType


class UpdateSelfUpgradeConfigurationRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    SelfUpgradeStatus: SelfUpgradeStatusType


class UpdateSelfUpgradeRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    UpgradeRequestId: str
    Action: SelfUpgradeAdminActionType


class UpdateTemplateAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str
    TemplateVersionNumber: int


class UpdateThemeAliasRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str
    ThemeVersionNumber: int


class UpdateUserCustomPermissionRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    CustomPermissionsName: str


class UpdateUserRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    Email: str
    Role: UserRoleType
    CustomPermissionsName: NotRequired[str]
    UnapplyCustomPermissions: NotRequired[bool]
    ExternalLoginFederationProviderType: NotRequired[str]
    CustomFederationProviderUrl: NotRequired[str]
    ExternalLoginId: NotRequired[str]


class UpdateVPCConnectionRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str
    Name: str
    SubnetIds: Sequence[str]
    SecurityGroupIds: Sequence[str]
    RoleArn: str
    DnsResolvers: NotRequired[Sequence[str]]


class VisualHighlightOperationTypeDef(TypedDict):
    Trigger: VisualHighlightTriggerType


class WaterfallChartGroupColorConfigurationTypeDef(TypedDict):
    PositiveBarColor: NotRequired[str]
    NegativeBarColor: NotRequired[str]
    TotalBarColor: NotRequired[str]


class WaterfallChartOptionsTypeDef(TypedDict):
    TotalBarLabel: NotRequired[str]


class WordCloudOptionsTypeDef(TypedDict):
    WordOrientation: NotRequired[WordCloudWordOrientationType]
    WordScaling: NotRequired[WordCloudWordScalingType]
    CloudLayout: NotRequired[WordCloudCloudLayoutType]
    WordCasing: NotRequired[WordCloudWordCasingType]
    WordPadding: NotRequired[WordCloudWordPaddingType]
    MaximumStringLength: NotRequired[int]


class UpdateAccountCustomizationRequestTypeDef(TypedDict):
    AwsAccountId: str
    AccountCustomization: AccountCustomizationTypeDef
    Namespace: NotRequired[str]


ActionConnectorSummaryTypeDef = TypedDict(
    "ActionConnectorSummaryTypeDef",
    {
        "Arn": str,
        "ActionConnectorId": str,
        "Type": ActionConnectorTypeType,
        "Name": str,
        "LastUpdatedTime": datetime,
        "CreatedTime": NotRequired[datetime],
        "Status": NotRequired[ResourceStatusType],
        "Error": NotRequired[ActionConnectorErrorTypeDef],
    },
)


class SearchActionConnectorsRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[ActionConnectorSearchFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


AggFunctionUnionTypeDef = Union[AggFunctionTypeDef, AggFunctionOutputTypeDef]


class AxisLabelReferenceOptionsTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef


class CascadingControlSourceTypeDef(TypedDict):
    SourceSheetControlId: NotRequired[str]
    ColumnToMatch: NotRequired[ColumnIdentifierTypeDef]


class CategoryDrillDownFilterOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    CategoryValues: list[str]


class CategoryDrillDownFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    CategoryValues: Sequence[str]


class ContributionAnalysisDefaultOutputTypeDef(TypedDict):
    MeasureFieldId: str
    ContributorDimensions: list[ColumnIdentifierTypeDef]


class ContributionAnalysisDefaultTypeDef(TypedDict):
    MeasureFieldId: str
    ContributorDimensions: Sequence[ColumnIdentifierTypeDef]


class DynamicDefaultValueTypeDef(TypedDict):
    DefaultValueColumn: ColumnIdentifierTypeDef
    UserNameColumn: NotRequired[ColumnIdentifierTypeDef]
    GroupNameColumn: NotRequired[ColumnIdentifierTypeDef]


class FilterOperationSelectedFieldsConfigurationOutputTypeDef(TypedDict):
    SelectedFields: NotRequired[list[str]]
    SelectedFieldOptions: NotRequired[Literal["ALL_FIELDS"]]
    SelectedColumns: NotRequired[list[ColumnIdentifierTypeDef]]


class FilterOperationSelectedFieldsConfigurationTypeDef(TypedDict):
    SelectedFields: NotRequired[Sequence[str]]
    SelectedFieldOptions: NotRequired[Literal["ALL_FIELDS"]]
    SelectedColumns: NotRequired[Sequence[ColumnIdentifierTypeDef]]


class NumericEqualityDrillDownFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Value: float


class ParameterSelectableValuesOutputTypeDef(TypedDict):
    Values: NotRequired[list[str]]
    LinkToDataSetColumn: NotRequired[ColumnIdentifierTypeDef]


class ParameterSelectableValuesTypeDef(TypedDict):
    Values: NotRequired[Sequence[str]]
    LinkToDataSetColumn: NotRequired[ColumnIdentifierTypeDef]


class TimeRangeDrillDownFilterOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    RangeMinimum: datetime
    RangeMaximum: datetime
    TimeGranularity: TimeGranularityType


class VisualCustomizationFieldsConfigurationOutputTypeDef(TypedDict):
    Status: NotRequired[DashboardCustomizationStatusType]
    AdditionalFields: NotRequired[list[ColumnIdentifierTypeDef]]


class VisualCustomizationFieldsConfigurationTypeDef(TypedDict):
    Status: NotRequired[DashboardCustomizationStatusType]
    AdditionalFields: NotRequired[Sequence[ColumnIdentifierTypeDef]]


class AmazonQInQuickSightDashboardConfigurationsTypeDef(TypedDict):
    ExecutiveSummary: NotRequired[ExecutiveSummaryConfigurationsTypeDef]


class AmazonQInQuickSightConsoleConfigurationsTypeDef(TypedDict):
    DataQnA: NotRequired[DataQnAConfigurationsTypeDef]
    GenerativeAuthoring: NotRequired[GenerativeAuthoringConfigurationsTypeDef]
    ExecutiveSummary: NotRequired[ExecutiveSummaryConfigurationsTypeDef]
    DataStories: NotRequired[DataStoriesConfigurationsTypeDef]


AnalysisErrorTypeDef = TypedDict(
    "AnalysisErrorTypeDef",
    {
        "Type": NotRequired[AnalysisErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[list[EntityTypeDef]],
    },
)
DashboardErrorTypeDef = TypedDict(
    "DashboardErrorTypeDef",
    {
        "Type": NotRequired[DashboardErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[list[EntityTypeDef]],
    },
)
TemplateErrorTypeDef = TypedDict(
    "TemplateErrorTypeDef",
    {
        "Type": NotRequired[TemplateErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[list[EntityTypeDef]],
    },
)


class SearchAnalysesRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[AnalysisSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class AnalysisSourceTemplateTypeDef(TypedDict):
    DataSetReferences: Sequence[DataSetReferenceTypeDef]
    Arn: str


class DashboardSourceTemplateTypeDef(TypedDict):
    DataSetReferences: Sequence[DataSetReferenceTypeDef]
    Arn: str


class TemplateSourceAnalysisTypeDef(TypedDict):
    Arn: str
    DataSetReferences: Sequence[DataSetReferenceTypeDef]


class AnonymousUserDashboardFeatureConfigurationsTypeDef(TypedDict):
    SharedView: NotRequired[SharedViewConfigurationsTypeDef]


class AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardVisualId: DashboardVisualIdTypeDef


class RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardVisualId: DashboardVisualIdTypeDef


class ArcAxisConfigurationTypeDef(TypedDict):
    Range: NotRequired[ArcAxisDisplayRangeTypeDef]
    ReserveRange: NotRequired[int]


class AssetBundleCloudFormationOverridePropertyConfigurationOutputTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleExportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        list[AssetBundleExportJobVPCConnectionOverridePropertiesOutputTypeDef]
    ]
    RefreshSchedules: NotRequired[
        list[AssetBundleExportJobRefreshScheduleOverridePropertiesOutputTypeDef]
    ]
    DataSources: NotRequired[list[AssetBundleExportJobDataSourceOverridePropertiesOutputTypeDef]]
    DataSets: NotRequired[list[AssetBundleExportJobDataSetOverridePropertiesOutputTypeDef]]
    Themes: NotRequired[list[AssetBundleExportJobThemeOverridePropertiesOutputTypeDef]]
    Analyses: NotRequired[list[AssetBundleExportJobAnalysisOverridePropertiesOutputTypeDef]]
    Dashboards: NotRequired[list[AssetBundleExportJobDashboardOverridePropertiesOutputTypeDef]]
    Folders: NotRequired[list[AssetBundleExportJobFolderOverridePropertiesOutputTypeDef]]


class AssetBundleCloudFormationOverridePropertyConfigurationTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleExportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        Sequence[AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef]
    ]
    RefreshSchedules: NotRequired[
        Sequence[AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef]
    ]
    DataSources: NotRequired[Sequence[AssetBundleExportJobDataSourceOverridePropertiesTypeDef]]
    DataSets: NotRequired[Sequence[AssetBundleExportJobDataSetOverridePropertiesTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleExportJobThemeOverridePropertiesTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleExportJobAnalysisOverridePropertiesTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleExportJobDashboardOverridePropertiesTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleExportJobFolderOverridePropertiesTypeDef]]


class AssetBundleImportJobAnalysisOverridePermissionsOutputTypeDef(TypedDict):
    AnalysisIds: list[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleImportJobDataSetOverridePermissionsOutputTypeDef(TypedDict):
    DataSetIds: list[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleImportJobDataSourceOverridePermissionsOutputTypeDef(TypedDict):
    DataSourceIds: list[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleImportJobFolderOverridePermissionsOutputTypeDef(TypedDict):
    FolderIds: list[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsOutputTypeDef]


class AssetBundleImportJobThemeOverridePermissionsOutputTypeDef(TypedDict):
    ThemeIds: list[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleResourceLinkSharingConfigurationOutputTypeDef(TypedDict):
    Permissions: NotRequired[AssetBundleResourcePermissionsOutputTypeDef]


class AssetBundleImportJobAnalysisOverridePermissionsTypeDef(TypedDict):
    AnalysisIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsTypeDef


class AssetBundleImportJobDataSetOverridePermissionsTypeDef(TypedDict):
    DataSetIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsTypeDef


class AssetBundleImportJobDataSourceOverridePermissionsTypeDef(TypedDict):
    DataSourceIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsTypeDef


class AssetBundleImportJobFolderOverridePermissionsTypeDef(TypedDict):
    FolderIds: Sequence[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsTypeDef]


class AssetBundleImportJobThemeOverridePermissionsTypeDef(TypedDict):
    ThemeIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsTypeDef


class AssetBundleResourceLinkSharingConfigurationTypeDef(TypedDict):
    Permissions: NotRequired[AssetBundleResourcePermissionsTypeDef]


class AssetBundleImportJobAnalysisOverrideTagsOutputTypeDef(TypedDict):
    AnalysisIds: list[str]
    Tags: list[TagTypeDef]


class AssetBundleImportJobAnalysisOverrideTagsTypeDef(TypedDict):
    AnalysisIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDashboardOverrideTagsOutputTypeDef(TypedDict):
    DashboardIds: list[str]
    Tags: list[TagTypeDef]


class AssetBundleImportJobDashboardOverrideTagsTypeDef(TypedDict):
    DashboardIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDataSetOverrideTagsOutputTypeDef(TypedDict):
    DataSetIds: list[str]
    Tags: list[TagTypeDef]


class AssetBundleImportJobDataSetOverrideTagsTypeDef(TypedDict):
    DataSetIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDataSourceOverrideTagsOutputTypeDef(TypedDict):
    DataSourceIds: list[str]
    Tags: list[TagTypeDef]


class AssetBundleImportJobDataSourceOverrideTagsTypeDef(TypedDict):
    DataSourceIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobFolderOverrideTagsOutputTypeDef(TypedDict):
    FolderIds: list[str]
    Tags: list[TagTypeDef]


class AssetBundleImportJobFolderOverrideTagsTypeDef(TypedDict):
    FolderIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobThemeOverrideTagsOutputTypeDef(TypedDict):
    ThemeIds: list[str]
    Tags: list[TagTypeDef]


class AssetBundleImportJobThemeOverrideTagsTypeDef(TypedDict):
    ThemeIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobVPCConnectionOverrideTagsOutputTypeDef(TypedDict):
    VPCConnectionIds: list[str]
    Tags: list[TagTypeDef]


class AssetBundleImportJobVPCConnectionOverrideTagsTypeDef(TypedDict):
    VPCConnectionIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class CreateAccountCustomizationRequestTypeDef(TypedDict):
    AwsAccountId: str
    AccountCustomization: AccountCustomizationTypeDef
    Namespace: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateNamespaceRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    IdentityStore: Literal["QUICKSIGHT"]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateVPCConnectionRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str
    Name: str
    SubnetIds: Sequence[str]
    SecurityGroupIds: Sequence[str]
    RoleArn: str
    DnsResolvers: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class RegisterUserRequestTypeDef(TypedDict):
    IdentityType: IdentityTypeType
    Email: str
    UserRole: UserRoleType
    AwsAccountId: str
    Namespace: str
    IamArn: NotRequired[str]
    SessionName: NotRequired[str]
    UserName: NotRequired[str]
    CustomPermissionsName: NotRequired[str]
    ExternalLoginFederationProviderType: NotRequired[str]
    CustomFederationProviderUrl: NotRequired[str]
    ExternalLoginId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDataSourceCredentialsTypeDef(TypedDict):
    CredentialPair: NotRequired[AssetBundleImportJobDataSourceCredentialPairTypeDef]
    SecretArn: NotRequired[str]


class OAuthParametersTypeDef(TypedDict):
    TokenProviderUrl: str
    OAuthScope: NotRequired[str]
    IdentityProviderVpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    IdentityProviderResourceUri: NotRequired[str]


class AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef(TypedDict):
    DataSetId: str
    ScheduleId: str
    StartAfterDateTime: NotRequired[TimestampTypeDef]


class CustomParameterValuesTypeDef(TypedDict):
    StringValues: NotRequired[Sequence[str]]
    IntegerValues: NotRequired[Sequence[int]]
    DecimalValues: NotRequired[Sequence[float]]
    DateTimeValues: NotRequired[Sequence[TimestampTypeDef]]


class DataSetDateFilterValueTypeDef(TypedDict):
    StaticValue: NotRequired[TimestampTypeDef]


class DateTimeDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[TimestampTypeDef]]


class DateTimeParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[TimestampTypeDef]


class DateTimeValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[TimestampTypeDef]


class NewDefaultValuesTypeDef(TypedDict):
    StringStaticValues: NotRequired[Sequence[str]]
    DecimalStaticValues: NotRequired[Sequence[float]]
    DateTimeStaticValues: NotRequired[Sequence[TimestampTypeDef]]
    IntegerStaticValues: NotRequired[Sequence[int]]


class TimeRangeDrillDownFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    RangeMinimum: TimestampTypeDef
    RangeMaximum: TimestampTypeDef
    TimeGranularity: TimeGranularityType


class TopicRefreshScheduleTypeDef(TypedDict):
    IsEnabled: bool
    BasedOnSpiceSchedule: bool
    StartingAt: NotRequired[TimestampTypeDef]
    Timezone: NotRequired[str]
    RepeatAt: NotRequired[str]
    TopicScheduleType: NotRequired[TopicScheduleTypeType]


class WhatIfPointScenarioTypeDef(TypedDict):
    Date: TimestampTypeDef
    Value: float


class WhatIfRangeScenarioTypeDef(TypedDict):
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef
    Value: float


class AssetBundleImportSourceTypeDef(TypedDict):
    Body: NotRequired[BlobTypeDef]
    S3Uri: NotRequired[str]


class AthenaParametersTypeDef(TypedDict):
    WorkGroup: NotRequired[str]
    RoleArn: NotRequired[str]
    IdentityCenterConfiguration: NotRequired[IdentityCenterConfigurationTypeDef]


class AuthorizationCodeGrantCredentialsDetailsTypeDef(TypedDict):
    AuthorizationCodeGrantDetails: NotRequired[AuthorizationCodeGrantDetailsTypeDef]


class AxisDisplayRangeOutputTypeDef(TypedDict):
    MinMax: NotRequired[AxisDisplayMinMaxRangeTypeDef]
    DataDriven: NotRequired[dict[str, Any]]


class AxisDisplayRangeTypeDef(TypedDict):
    MinMax: NotRequired[AxisDisplayMinMaxRangeTypeDef]
    DataDriven: NotRequired[Mapping[str, Any]]


class AxisScaleTypeDef(TypedDict):
    Linear: NotRequired[AxisLinearScaleTypeDef]
    Logarithmic: NotRequired[AxisLogarithmicScaleTypeDef]


class BarChartDefaultSeriesSettingsTypeDef(TypedDict):
    DecalSettings: NotRequired[DecalSettingsTypeDef]
    BorderSettings: NotRequired[BorderSettingsTypeDef]


class BarChartSeriesSettingsTypeDef(TypedDict):
    DecalSettings: NotRequired[DecalSettingsTypeDef]
    BorderSettings: NotRequired[BorderSettingsTypeDef]


class DecalSettingsConfigurationOutputTypeDef(TypedDict):
    CustomDecalSettings: NotRequired[list[DecalSettingsTypeDef]]


class DecalSettingsConfigurationTypeDef(TypedDict):
    CustomDecalSettings: NotRequired[Sequence[DecalSettingsTypeDef]]


class ScatterPlotSortConfigurationTypeDef(TypedDict):
    ScatterPlotLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class CancelIngestionResponseTypeDef(TypedDict):
    Arn: str
    IngestionId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAccountCustomizationResponseTypeDef(TypedDict):
    Arn: str
    AwsAccountId: str
    Namespace: str
    AccountCustomization: AccountCustomizationTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateActionConnectorResponseTypeDef(TypedDict):
    Arn: str
    CreationStatus: ResourceStatusType
    ActionConnectorId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAnalysisResponseTypeDef(TypedDict):
    Arn: str
    AnalysisId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDashboardResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    DashboardId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSetResponseTypeDef(TypedDict):
    Arn: str
    DataSetId: str
    IngestionArn: str
    IngestionId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSourceResponseTypeDef(TypedDict):
    Arn: str
    DataSourceId: str
    CreationStatus: ResourceStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFolderResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIAMPolicyAssignmentResponseTypeDef(TypedDict):
    AssignmentName: str
    AssignmentId: str
    AssignmentStatus: AssignmentStatusType
    PolicyArn: str
    Identities: dict[str, list[str]]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIngestionResponseTypeDef(TypedDict):
    Arn: str
    IngestionId: str
    IngestionStatus: IngestionStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNamespaceResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    CapacityRegion: str
    CreationStatus: NamespaceStatusType
    IdentityStore: Literal["QUICKSIGHT"]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRefreshScheduleResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ScheduleId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRoleMembershipResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTemplateResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    TemplateId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThemeResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    ThemeId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTopicResponseTypeDef(TypedDict):
    Arn: str
    TopicId: str
    RefreshArn: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVPCConnectionResponseTypeDef(TypedDict):
    Arn: str
    VPCConnectionId: str
    CreationStatus: VPCConnectionResourceStatusType
    AvailabilityStatus: VPCConnectionAvailabilityStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAccountCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAccountCustomizationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAccountSubscriptionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteActionConnectorResponseTypeDef(TypedDict):
    Arn: str
    ActionConnectorId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAnalysisResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    AnalysisId: str
    DeletionTime: datetime
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBrandAssignmentResponseTypeDef(TypedDict):
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBrandResponseTypeDef(TypedDict):
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDashboardResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    DashboardId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataSetRefreshPropertiesResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataSetResponseTypeDef(TypedDict):
    Arn: str
    DataSetId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataSourceResponseTypeDef(TypedDict):
    Arn: str
    DataSourceId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDefaultQBusinessApplicationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFolderMembershipResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFolderResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGroupMembershipResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGroupResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIAMPolicyAssignmentResponseTypeDef(TypedDict):
    AssignmentName: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIdentityPropagationConfigResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNamespaceResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRefreshScheduleResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ScheduleId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRoleCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRoleMembershipResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTemplateAliasResponseTypeDef(TypedDict):
    Status: int
    TemplateId: str
    AliasName: str
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTemplateResponseTypeDef(TypedDict):
    RequestId: str
    Arn: str
    TemplateId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteThemeAliasResponseTypeDef(TypedDict):
    AliasName: str
    Arn: str
    RequestId: str
    Status: int
    ThemeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteThemeResponseTypeDef(TypedDict):
    Arn: str
    RequestId: str
    Status: int
    ThemeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTopicResponseTypeDef(TypedDict):
    Arn: str
    TopicId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserByPrincipalIdResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVPCConnectionResponseTypeDef(TypedDict):
    Arn: str
    VPCConnectionId: str
    DeletionStatus: VPCConnectionResourceStatusType
    AvailabilityStatus: VPCConnectionAvailabilityStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountCustomPermissionResponseTypeDef(TypedDict):
    CustomPermissionsName: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountCustomizationResponseTypeDef(TypedDict):
    Arn: str
    AwsAccountId: str
    Namespace: str
    AccountCustomization: AccountCustomizationTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountSettingsResponseTypeDef(TypedDict):
    AccountSettings: AccountSettingsTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountSubscriptionResponseTypeDef(TypedDict):
    AccountInfo: AccountInfoTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBrandAssignmentResponseTypeDef(TypedDict):
    RequestId: str
    BrandArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDashboardsQAConfigurationResponseTypeDef(TypedDict):
    DashboardsQAStatus: DashboardsQAStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDefaultQBusinessApplicationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ApplicationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpRestrictionResponseTypeDef(TypedDict):
    AwsAccountId: str
    IpRestrictionRuleMap: dict[str, str]
    VpcIdRestrictionRuleMap: dict[str, str]
    VpcEndpointIdRestrictionRuleMap: dict[str, str]
    Enabled: bool
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeQPersonalizationConfigurationResponseTypeDef(TypedDict):
    PersonalizationMode: PersonalizationModeType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeQuickSightQSearchConfigurationResponseTypeDef(TypedDict):
    QSearchStatus: QSearchStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRoleCustomPermissionResponseTypeDef(TypedDict):
    CustomPermissionsName: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateEmbedUrlForAnonymousUserResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    AnonymousUserArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateEmbedUrlForRegisteredUserResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateEmbedUrlForRegisteredUserWithIdentityResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDashboardEmbedUrlResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetFlowMetadataOutputTypeDef(TypedDict):
    Arn: str
    FlowId: str
    Name: str
    Description: str
    PublishState: FlowPublishStateType
    UserCount: int
    RunCount: int
    CreatedTime: datetime
    LastUpdatedTime: datetime
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetIdentityContextResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    Context: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSessionEmbedUrlResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAnalysesResponseTypeDef(TypedDict):
    AnalysisSummaryList: list[AnalysisSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAssetBundleExportJobsResponseTypeDef(TypedDict):
    AssetBundleExportJobSummaryList: list[AssetBundleExportJobSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAssetBundleImportJobsResponseTypeDef(TypedDict):
    AssetBundleImportJobSummaryList: list[AssetBundleImportJobSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFoldersForResourceResponseTypeDef(TypedDict):
    Status: int
    Folders: list[str]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIAMPolicyAssignmentsForUserResponseTypeDef(TypedDict):
    ActiveAssignments: list[ActiveIAMPolicyAssignmentTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIdentityPropagationConfigsResponseTypeDef(TypedDict):
    Services: list[AuthorizedTargetsByServiceTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRoleMembershipsResponseTypeDef(TypedDict):
    MembersList: list[str]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class PutDataSetRefreshPropertiesResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreAnalysisResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    AnalysisId: str
    RequestId: str
    RestorationFailedFolderArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class SearchAnalysesResponseTypeDef(TypedDict):
    AnalysisSummaryList: list[AnalysisSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartAssetBundleExportJobResponseTypeDef(TypedDict):
    Arn: str
    AssetBundleExportJobId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class StartAssetBundleImportJobResponseTypeDef(TypedDict):
    Arn: str
    AssetBundleImportJobId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class StartDashboardSnapshotJobResponseTypeDef(TypedDict):
    Arn: str
    SnapshotJobId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class StartDashboardSnapshotJobScheduleResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UntagResourceResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountCustomizationResponseTypeDef(TypedDict):
    Arn: str
    AwsAccountId: str
    Namespace: str
    AccountCustomization: AccountCustomizationTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountSettingsResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateActionConnectorResponseTypeDef(TypedDict):
    Arn: str
    ActionConnectorId: str
    RequestId: str
    UpdateStatus: ResourceStatusType
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAnalysisResponseTypeDef(TypedDict):
    Arn: str
    AnalysisId: str
    UpdateStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationWithTokenExchangeGrantResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandAssignmentResponseTypeDef(TypedDict):
    RequestId: str
    BrandArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandPublishedVersionResponseTypeDef(TypedDict):
    RequestId: str
    VersionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardLinksResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    DashboardArn: str
    LinkEntities: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardPublishedVersionResponseTypeDef(TypedDict):
    DashboardId: str
    DashboardArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    DashboardId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardsQAConfigurationResponseTypeDef(TypedDict):
    DashboardsQAStatus: DashboardsQAStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSetPermissionsResponseTypeDef(TypedDict):
    DataSetArn: str
    DataSetId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSetResponseTypeDef(TypedDict):
    Arn: str
    DataSetId: str
    IngestionArn: str
    IngestionId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSourcePermissionsResponseTypeDef(TypedDict):
    DataSourceArn: str
    DataSourceId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSourceResponseTypeDef(TypedDict):
    Arn: str
    DataSourceId: str
    UpdateStatus: ResourceStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDefaultQBusinessApplicationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFolderResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIAMPolicyAssignmentResponseTypeDef(TypedDict):
    AssignmentName: str
    AssignmentId: str
    PolicyArn: str
    Identities: dict[str, list[str]]
    AssignmentStatus: AssignmentStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIdentityPropagationConfigResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIpRestrictionResponseTypeDef(TypedDict):
    AwsAccountId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePublicSharingSettingsResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQPersonalizationConfigurationResponseTypeDef(TypedDict):
    PersonalizationMode: PersonalizationModeType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQuickSightQSearchConfigurationResponseTypeDef(TypedDict):
    QSearchStatus: QSearchStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRefreshScheduleResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ScheduleId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRoleCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSPICECapacityConfigurationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSelfUpgradeConfigurationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTemplateResponseTypeDef(TypedDict):
    TemplateId: str
    Arn: str
    VersionArn: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateThemeResponseTypeDef(TypedDict):
    ThemeId: str
    Arn: str
    VersionArn: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTopicResponseTypeDef(TypedDict):
    TopicId: str
    Arn: str
    RefreshArn: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVPCConnectionResponseTypeDef(TypedDict):
    Arn: str
    VPCConnectionId: str
    UpdateStatus: VPCConnectionResourceStatusType
    AvailabilityStatus: VPCConnectionAvailabilityStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class BatchCreateTopicReviewedAnswerResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    SucceededAnswers: list[SucceededTopicReviewedAnswerTypeDef]
    InvalidAnswers: list[InvalidTopicReviewedAnswerTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteTopicReviewedAnswerResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    SucceededAnswers: list[SucceededTopicReviewedAnswerTypeDef]
    InvalidAnswers: list[InvalidTopicReviewedAnswerTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class HistogramBinOptionsTypeDef(TypedDict):
    SelectedBinType: NotRequired[HistogramBinTypeType]
    BinCount: NotRequired[BinCountOptionsTypeDef]
    BinWidth: NotRequired[BinWidthOptionsTypeDef]
    StartValue: NotRequired[float]


class BodySectionRepeatPageBreakConfigurationTypeDef(TypedDict):
    After: NotRequired[SectionAfterPageBreakTypeDef]


class SectionPageBreakConfigurationTypeDef(TypedDict):
    After: NotRequired[SectionAfterPageBreakTypeDef]


class TileStyleTypeDef(TypedDict):
    BackgroundColor: NotRequired[str]
    Border: NotRequired[BorderStyleTypeDef]
    BorderRadius: NotRequired[str]
    Padding: NotRequired[str]


class BoxPlotOptionsTypeDef(TypedDict):
    StyleOptions: NotRequired[BoxPlotStyleOptionsTypeDef]
    OutlierVisibility: NotRequired[VisibilityType]
    AllDataPointsVisibility: NotRequired[VisibilityType]


BrandColorPaletteTypeDef = TypedDict(
    "BrandColorPaletteTypeDef",
    {
        "Primary": NotRequired[PaletteTypeDef],
        "Secondary": NotRequired[PaletteTypeDef],
        "Accent": NotRequired[PaletteTypeDef],
        "Measure": NotRequired[PaletteTypeDef],
        "Dimension": NotRequired[PaletteTypeDef],
        "Success": NotRequired[PaletteTypeDef],
        "Info": NotRequired[PaletteTypeDef],
        "Warning": NotRequired[PaletteTypeDef],
        "Danger": NotRequired[PaletteTypeDef],
    },
)


class ContextualAccentPaletteTypeDef(TypedDict):
    Connection: NotRequired[PaletteTypeDef]
    Visualization: NotRequired[PaletteTypeDef]
    Insight: NotRequired[PaletteTypeDef]
    Automation: NotRequired[PaletteTypeDef]


class NavbarStyleTypeDef(TypedDict):
    GlobalNavbar: NotRequired[PaletteTypeDef]
    ContextualNavbar: NotRequired[PaletteTypeDef]


class ListBrandsResponseTypeDef(TypedDict):
    Brands: list[BrandSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCustomPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str
    Capabilities: NotRequired[CapabilitiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CustomPermissionsTypeDef(TypedDict):
    Arn: NotRequired[str]
    CustomPermissionsName: NotRequired[str]
    Capabilities: NotRequired[CapabilitiesTypeDef]


class UpdateCustomPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str
    Capabilities: NotRequired[CapabilitiesTypeDef]


class CategoryFilterConfigurationOutputTypeDef(TypedDict):
    FilterListConfiguration: NotRequired[FilterListConfigurationOutputTypeDef]
    CustomFilterListConfiguration: NotRequired[CustomFilterListConfigurationOutputTypeDef]
    CustomFilterConfiguration: NotRequired[CustomFilterConfigurationTypeDef]


class CategoryFilterConfigurationTypeDef(TypedDict):
    FilterListConfiguration: NotRequired[FilterListConfigurationTypeDef]
    CustomFilterListConfiguration: NotRequired[CustomFilterListConfigurationTypeDef]
    CustomFilterConfiguration: NotRequired[CustomFilterConfigurationTypeDef]


class ClientCredentialsDetailsTypeDef(TypedDict):
    ClientCredentialsGrantDetails: NotRequired[ClientCredentialsGrantDetailsTypeDef]


class ClusterMarkerTypeDef(TypedDict):
    SimpleClusterMarker: NotRequired[SimpleClusterMarkerTypeDef]


class TopicConstantValueOutputTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    Value: NotRequired[str]
    Minimum: NotRequired[str]
    Maximum: NotRequired[str]
    ValueList: NotRequired[list[CollectiveConstantEntryTypeDef]]


class TopicConstantValueTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    Value: NotRequired[str]
    Minimum: NotRequired[str]
    Maximum: NotRequired[str]
    ValueList: NotRequired[Sequence[CollectiveConstantEntryTypeDef]]


class TopicCategoryFilterConstantOutputTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    SingularConstant: NotRequired[str]
    CollectiveConstant: NotRequired[CollectiveConstantOutputTypeDef]


class TopicCategoryFilterConstantTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    SingularConstant: NotRequired[str]
    CollectiveConstant: NotRequired[CollectiveConstantTypeDef]


class ColorScaleOutputTypeDef(TypedDict):
    Colors: list[DataColorTypeDef]
    ColorFillType: ColorFillTypeType
    NullValueColor: NotRequired[DataColorTypeDef]


class ColorScaleTypeDef(TypedDict):
    Colors: Sequence[DataColorTypeDef]
    ColorFillType: ColorFillTypeType
    NullValueColor: NotRequired[DataColorTypeDef]


class ColorsConfigurationOutputTypeDef(TypedDict):
    CustomColors: NotRequired[list[CustomColorTypeDef]]


class ColorsConfigurationTypeDef(TypedDict):
    CustomColors: NotRequired[Sequence[CustomColorTypeDef]]


class ColumnTagTypeDef(TypedDict):
    ColumnGeographicRole: NotRequired[GeoSpatialDataRoleType]
    ColumnDescription: NotRequired[ColumnDescriptionTypeDef]


class ColumnGroupSchemaOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    ColumnGroupColumnSchemaList: NotRequired[list[ColumnGroupColumnSchemaTypeDef]]


class ColumnGroupSchemaTypeDef(TypedDict):
    Name: NotRequired[str]
    ColumnGroupColumnSchemaList: NotRequired[Sequence[ColumnGroupColumnSchemaTypeDef]]


class ColumnGroupOutputTypeDef(TypedDict):
    GeoSpatialColumnGroup: NotRequired[GeoSpatialColumnGroupOutputTypeDef]


ColumnLevelPermissionRuleUnionTypeDef = Union[
    ColumnLevelPermissionRuleTypeDef, ColumnLevelPermissionRuleOutputTypeDef
]


class DataSetSchemaOutputTypeDef(TypedDict):
    ColumnSchemaList: NotRequired[list[ColumnSchemaTypeDef]]


class DataSetSchemaTypeDef(TypedDict):
    ColumnSchemaList: NotRequired[Sequence[ColumnSchemaTypeDef]]


class ComboChartDefaultSeriesSettingsTypeDef(TypedDict):
    LineStyleSettings: NotRequired[LineChartLineStyleSettingsTypeDef]
    MarkerStyleSettings: NotRequired[LineChartMarkerStyleSettingsTypeDef]
    DecalSettings: NotRequired[DecalSettingsTypeDef]
    BorderSettings: NotRequired[BorderSettingsTypeDef]


class ComboChartSeriesSettingsTypeDef(TypedDict):
    LineStyleSettings: NotRequired[LineChartLineStyleSettingsTypeDef]
    MarkerStyleSettings: NotRequired[LineChartMarkerStyleSettingsTypeDef]
    DecalSettings: NotRequired[DecalSettingsTypeDef]
    BorderSettings: NotRequired[BorderSettingsTypeDef]


class LineChartDefaultSeriesSettingsTypeDef(TypedDict):
    AxisBinding: NotRequired[AxisBindingType]
    LineStyleSettings: NotRequired[LineChartLineStyleSettingsTypeDef]
    MarkerStyleSettings: NotRequired[LineChartMarkerStyleSettingsTypeDef]
    DecalSettings: NotRequired[DecalSettingsTypeDef]


class LineChartSeriesSettingsTypeDef(TypedDict):
    LineStyleSettings: NotRequired[LineChartLineStyleSettingsTypeDef]
    MarkerStyleSettings: NotRequired[LineChartMarkerStyleSettingsTypeDef]
    DecalSettings: NotRequired[DecalSettingsTypeDef]


class ConditionalFormattingCustomIconConditionTypeDef(TypedDict):
    Expression: str
    IconOptions: ConditionalFormattingCustomIconOptionsTypeDef
    Color: NotRequired[str]
    DisplayConfiguration: NotRequired[ConditionalFormattingIconDisplayConfigurationTypeDef]


class CreateAccountSubscriptionResponseTypeDef(TypedDict):
    SignupResponse: SignupResponseTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DataSetSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    DataSetId: NotRequired[str]
    Name: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    ImportMode: NotRequired[DataSetImportModeType]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionDataSetMap: NotRequired[dict[str, RowLevelPermissionDataSetTypeDef]]
    RowLevelPermissionTagConfigurationApplied: NotRequired[bool]
    ColumnLevelPermissionRulesApplied: NotRequired[bool]
    UseAs: NotRequired[Literal["RLS_RULES"]]


class CreateFolderMembershipResponseTypeDef(TypedDict):
    Status: int
    FolderMember: FolderMemberTypeDef
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGroupMembershipResponseTypeDef(TypedDict):
    GroupMember: GroupMemberTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGroupMembershipResponseTypeDef(TypedDict):
    GroupMember: GroupMemberTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupMembershipsResponseTypeDef(TypedDict):
    GroupMemberList: list[GroupMemberTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupsResponseTypeDef(TypedDict):
    GroupList: list[GroupTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUserGroupsResponseTypeDef(TypedDict):
    GroupList: list[GroupTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchGroupsResponseTypeDef(TypedDict):
    GroupList: list[GroupTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTemplateAliasResponseTypeDef(TypedDict):
    TemplateAlias: TemplateAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTemplateAliasResponseTypeDef(TypedDict):
    TemplateAlias: TemplateAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTemplateAliasesResponseTypeDef(TypedDict):
    TemplateAliasList: list[TemplateAliasTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateTemplateAliasResponseTypeDef(TypedDict):
    TemplateAlias: TemplateAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThemeAliasResponseTypeDef(TypedDict):
    ThemeAlias: ThemeAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThemeAliasResponseTypeDef(TypedDict):
    ThemeAlias: ThemeAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListThemeAliasesResponseTypeDef(TypedDict):
    ThemeAliasList: list[ThemeAliasTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateThemeAliasResponseTypeDef(TypedDict):
    ThemeAlias: ThemeAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CustomActionNavigationOperationTypeDef(TypedDict):
    LocalNavigationConfiguration: NotRequired[LocalNavigationConfigurationTypeDef]


class CustomValuesConfigurationOutputTypeDef(TypedDict):
    CustomValues: CustomParameterValuesOutputTypeDef
    IncludeNullValue: NotRequired[bool]


class CustomSqlOutputTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    SqlQuery: str
    Columns: NotRequired[list[InputColumnTypeDef]]


class CustomSqlTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    SqlQuery: str
    Columns: NotRequired[Sequence[InputColumnTypeDef]]


class ParentDataSetOutputTypeDef(TypedDict):
    DataSetArn: str
    InputColumns: list[InputColumnTypeDef]


class ParentDataSetTypeDef(TypedDict):
    DataSetArn: str
    InputColumns: Sequence[InputColumnTypeDef]


class RelationalTableOutputTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    InputColumns: list[InputColumnTypeDef]
    Catalog: NotRequired[str]
    Schema: NotRequired[str]


class RelationalTableTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    InputColumns: Sequence[InputColumnTypeDef]
    Catalog: NotRequired[str]
    Schema: NotRequired[str]


class VisualInteractionOptionsTypeDef(TypedDict):
    VisualMenuOption: NotRequired[VisualMenuOptionTypeDef]
    ContextMenuOption: NotRequired[ContextMenuOptionTypeDef]


class SearchDashboardsRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DashboardSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDashboardsResponseTypeDef(TypedDict):
    DashboardSummaryList: list[DashboardSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchDashboardsResponseTypeDef(TypedDict):
    DashboardSummaryList: list[DashboardSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDashboardVersionsResponseTypeDef(TypedDict):
    DashboardVersionSummaryList: list[DashboardVersionSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DashboardVisualPublishOptionsTypeDef(TypedDict):
    ExportHiddenFieldsOption: NotRequired[ExportHiddenFieldsOptionTypeDef]


class TableInlineVisualizationTypeDef(TypedDict):
    DataBars: NotRequired[DataBarsOptionsTypeDef]


class DataLabelTypeTypeDef(TypedDict):
    FieldLabelType: NotRequired[FieldLabelTypeTypeDef]
    DataPathLabelType: NotRequired[DataPathLabelTypeTypeDef]
    RangeEndsLabelType: NotRequired[RangeEndsLabelTypeTypeDef]
    MinimumLabelType: NotRequired[MinimumLabelTypeTypeDef]
    MaximumLabelType: NotRequired[MaximumLabelTypeTypeDef]


class DataPathValueTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldValue: NotRequired[str]
    DataPathType: NotRequired[DataPathTypeTypeDef]


class DataPrepAggregationFunctionTypeDef(TypedDict):
    SimpleAggregation: NotRequired[DataPrepSimpleAggregationFunctionTypeDef]
    ListAggregation: NotRequired[DataPrepListAggregationFunctionTypeDef]


class ImportTableOperationSourceOutputTypeDef(TypedDict):
    SourceTableId: str
    ColumnIdMappings: NotRequired[list[DataSetColumnIdMappingTypeDef]]


class ImportTableOperationSourceTypeDef(TypedDict):
    SourceTableId: str
    ColumnIdMappings: NotRequired[Sequence[DataSetColumnIdMappingTypeDef]]


class TransformOperationSourceOutputTypeDef(TypedDict):
    TransformOperationId: str
    ColumnIdMappings: NotRequired[list[DataSetColumnIdMappingTypeDef]]


class TransformOperationSourceTypeDef(TypedDict):
    TransformOperationId: str
    ColumnIdMappings: NotRequired[Sequence[DataSetColumnIdMappingTypeDef]]


class DataSetDateComparisonFilterConditionOutputTypeDef(TypedDict):
    Operator: DataSetDateComparisonFilterOperatorType
    Value: NotRequired[DataSetDateFilterValueOutputTypeDef]


class DataSetDateRangeFilterConditionOutputTypeDef(TypedDict):
    RangeMinimum: NotRequired[DataSetDateFilterValueOutputTypeDef]
    RangeMaximum: NotRequired[DataSetDateFilterValueOutputTypeDef]
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]


class DataSetNumericComparisonFilterConditionTypeDef(TypedDict):
    Operator: DataSetNumericComparisonFilterOperatorType
    Value: NotRequired[DataSetNumericFilterValueTypeDef]


class DataSetNumericRangeFilterConditionTypeDef(TypedDict):
    RangeMinimum: NotRequired[DataSetNumericFilterValueTypeDef]
    RangeMaximum: NotRequired[DataSetNumericFilterValueTypeDef]
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]


class SearchDataSetsRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSetSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DataSetStringComparisonFilterConditionTypeDef(TypedDict):
    Operator: DataSetStringComparisonFilterOperatorType
    Value: NotRequired[DataSetStringFilterValueTypeDef]


class DataSetStringListFilterConditionOutputTypeDef(TypedDict):
    Operator: DataSetStringListFilterOperatorType
    Values: NotRequired[DataSetStringListFilterValueOutputTypeDef]


DataSetStringListFilterValueUnionTypeDef = Union[
    DataSetStringListFilterValueTypeDef, DataSetStringListFilterValueOutputTypeDef
]


class SearchDataSourcesRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSourceSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchDataSourcesResponseTypeDef(TypedDict):
    DataSourceSummaries: list[DataSourceSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DateTimeDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultValues: NotRequired[DateTimeDatasetParameterDefaultValuesOutputTypeDef]


class TimeRangeFilterValueOutputTypeDef(TypedDict):
    StaticValue: NotRequired[datetime]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    Parameter: NotRequired[str]


class TimeRangeFilterValueTypeDef(TypedDict):
    StaticValue: NotRequired[TimestampTypeDef]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    Parameter: NotRequired[str]


class DecimalDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[DecimalDatasetParameterDefaultValuesOutputTypeDef]


DecimalDatasetParameterDefaultValuesUnionTypeDef = Union[
    DecimalDatasetParameterDefaultValuesTypeDef, DecimalDatasetParameterDefaultValuesOutputTypeDef
]


class DescribeActionConnectorPermissionsResponseTypeDef(TypedDict):
    Arn: str
    ActionConnectorId: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAnalysisPermissionsResponseTypeDef(TypedDict):
    AnalysisId: str
    AnalysisArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDataSetPermissionsResponseTypeDef(TypedDict):
    DataSetArn: str
    DataSetId: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDataSourcePermissionsResponseTypeDef(TypedDict):
    DataSourceArn: str
    DataSourceId: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFolderPermissionsResponseTypeDef(TypedDict):
    Status: int
    FolderId: str
    Arn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeFolderResolvedPermissionsResponseTypeDef(TypedDict):
    Status: int
    FolderId: str
    Arn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeTemplatePermissionsResponseTypeDef(TypedDict):
    TemplateId: str
    TemplateArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThemePermissionsResponseTypeDef(TypedDict):
    ThemeId: str
    ThemeArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTopicPermissionsResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class LinkSharingConfigurationOutputTypeDef(TypedDict):
    Permissions: NotRequired[list[ResourcePermissionOutputTypeDef]]


class UpdateActionConnectorPermissionsResponseTypeDef(TypedDict):
    Arn: str
    ActionConnectorId: str
    RequestId: str
    Status: int
    Permissions: list[ResourcePermissionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAnalysisPermissionsResponseTypeDef(TypedDict):
    AnalysisArn: str
    AnalysisId: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFolderPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTemplatePermissionsResponseTypeDef(TypedDict):
    TemplateId: str
    TemplateArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateThemePermissionsResponseTypeDef(TypedDict):
    ThemeId: str
    ThemeArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTopicPermissionsResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFolderPermissionsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFolderResolvedPermissionsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListActionConnectorsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAnalysesRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetBundleExportJobsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetBundleImportJobsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBrandsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCustomPermissionsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDashboardVersionsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDashboardsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSetsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourcesRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFlowsInputPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFolderMembersRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFoldersForResourceRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFoldersRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupMembershipsRequestPaginateTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIAMPolicyAssignmentsForUserRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    UserName: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIAMPolicyAssignmentsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    AssignmentStatus: NotRequired[AssignmentStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIngestionsRequestPaginateTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNamespacesRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRoleMembershipsRequestPaginateTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplateAliasesRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplateVersionsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplatesRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThemeVersionsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListThemesRequestPaginateTypeDef = TypedDict(
    "ListThemesRequestPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Type": NotRequired[ThemeTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListUserGroupsRequestPaginateTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchActionConnectorsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[ActionConnectorSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchAnalysesRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[AnalysisSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchDashboardsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DashboardSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchDataSetsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSetSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchDataSourcesRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSourceSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFolderResponseTypeDef(TypedDict):
    Status: int
    Folder: FolderTypeDef
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIAMPolicyAssignmentResponseTypeDef(TypedDict):
    IAMPolicyAssignment: IAMPolicyAssignmentTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeKeyRegistrationResponseTypeDef(TypedDict):
    AwsAccountId: str
    KeyRegistration: list[RegisteredCustomerManagedKeyTypeDef]
    QDataKey: QDataKeyTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateKeyRegistrationRequestTypeDef(TypedDict):
    AwsAccountId: str
    KeyRegistration: Sequence[RegisteredCustomerManagedKeyTypeDef]


class DescribeSelfUpgradeConfigurationResponseTypeDef(TypedDict):
    SelfUpgradeConfiguration: SelfUpgradeConfigurationTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTopicRefreshResponseTypeDef(TypedDict):
    RefreshDetails: TopicRefreshDetailsTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    RefreshSchedule: TopicRefreshScheduleOutputTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TopicRefreshScheduleSummaryTypeDef(TypedDict):
    DatasetId: NotRequired[str]
    DatasetArn: NotRequired[str]
    DatasetName: NotRequired[str]
    RefreshSchedule: NotRequired[TopicRefreshScheduleOutputTypeDef]


class DescribeUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListUsersResponseTypeDef(TypedDict):
    UserList: list[UserTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RegisterUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    UserInvitationUrl: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DestinationTableTypeDef(TypedDict):
    Alias: str
    Source: DestinationTableSourceTypeDef


class DisplayFormatOptionsTypeDef(TypedDict):
    UseBlankCellFormat: NotRequired[bool]
    BlankCellFormat: NotRequired[str]
    DateFormat: NotRequired[str]
    DecimalSeparator: NotRequired[TopicNumericSeparatorSymbolType]
    GroupingSeparator: NotRequired[str]
    UseGrouping: NotRequired[bool]
    FractionDigits: NotRequired[int]
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    UnitScaler: NotRequired[NumberScaleType]
    NegativeFormat: NotRequired[NegativeFormatTypeDef]
    CurrencySymbol: NotRequired[str]


class DonutOptionsTypeDef(TypedDict):
    ArcOptions: NotRequired[ArcOptionsTypeDef]
    DonutCenterOptions: NotRequired[DonutCenterOptionsTypeDef]


FieldFolderUnionTypeDef = Union[FieldFolderTypeDef, FieldFolderOutputTypeDef]


class FilterAggMetricsTypeDef(TypedDict):
    MetricOperand: NotRequired[IdentifierTypeDef]
    Function: NotRequired[AggTypeType]
    SortDirection: NotRequired[TopicSortDirectionType]


class TopicSortClauseTypeDef(TypedDict):
    Operand: NotRequired[IdentifierTypeDef]
    SortDirection: NotRequired[TopicSortDirectionType]


class FilterOperationTargetVisualsConfigurationOutputTypeDef(TypedDict):
    SameSheetTargetVisualConfiguration: NotRequired[SameSheetTargetVisualConfigurationOutputTypeDef]


class FilterOperationTargetVisualsConfigurationTypeDef(TypedDict):
    SameSheetTargetVisualConfiguration: NotRequired[SameSheetTargetVisualConfigurationTypeDef]


class ListFlowsOutputTypeDef(TypedDict):
    FlowSummaryList: list[FlowSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchFlowsOutputTypeDef(TypedDict):
    FlowSummaryList: list[FlowSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchFoldersRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[FolderSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchFoldersRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[FolderSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFoldersResponseTypeDef(TypedDict):
    Status: int
    FolderSummaryList: list[FolderSummaryTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchFoldersResponseTypeDef(TypedDict):
    Status: int
    FolderSummaryList: list[FolderSummaryTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FontConfigurationTypeDef(TypedDict):
    FontSize: NotRequired[FontSizeTypeDef]
    FontDecoration: NotRequired[FontDecorationType]
    FontColor: NotRequired[str]
    FontWeight: NotRequired[FontWeightTypeDef]
    FontStyle: NotRequired[FontStyleType]
    FontFamily: NotRequired[str]


class ForecastScenarioOutputTypeDef(TypedDict):
    WhatIfPointScenario: NotRequired[WhatIfPointScenarioOutputTypeDef]
    WhatIfRangeScenario: NotRequired[WhatIfRangeScenarioOutputTypeDef]


class FreeFormLayoutCanvasSizeOptionsTypeDef(TypedDict):
    ScreenCanvasSizeOptions: NotRequired[FreeFormLayoutScreenCanvasSizeOptionsTypeDef]


class SnapshotAnonymousUserTypeDef(TypedDict):
    RowLevelPermissionTags: NotRequired[Sequence[SessionTagTypeDef]]


class QAResultTypeDef(TypedDict):
    ResultType: NotRequired[QAResultTypeType]
    DashboardVisual: NotRequired[DashboardVisualResultTypeDef]
    GeneratedAnswer: NotRequired[GeneratedAnswerResultTypeDef]


GeoSpatialColumnGroupUnionTypeDef = Union[
    GeoSpatialColumnGroupTypeDef, GeoSpatialColumnGroupOutputTypeDef
]


class GeocodePreferenceValueTypeDef(TypedDict):
    GeocoderHierarchy: NotRequired[GeocoderHierarchyTypeDef]
    Coordinate: NotRequired[CoordinateTypeDef]


class GeospatialMapStateTypeDef(TypedDict):
    Bounds: NotRequired[GeospatialCoordinateBoundsTypeDef]
    MapNavigation: NotRequired[GeospatialMapNavigationType]


class GeospatialWindowOptionsTypeDef(TypedDict):
    Bounds: NotRequired[GeospatialCoordinateBoundsTypeDef]
    MapZoomMode: NotRequired[MapZoomModeType]


class GeospatialDataSourceItemTypeDef(TypedDict):
    StaticFileDataSource: NotRequired[GeospatialStaticFileSourceTypeDef]


class GeospatialHeatmapColorScaleOutputTypeDef(TypedDict):
    Colors: NotRequired[list[GeospatialHeatmapDataColorTypeDef]]


class GeospatialHeatmapColorScaleTypeDef(TypedDict):
    Colors: NotRequired[Sequence[GeospatialHeatmapDataColorTypeDef]]


class GeospatialNullDataSettingsTypeDef(TypedDict):
    SymbolStyle: GeospatialNullSymbolStyleTypeDef


class GetFlowPermissionsOutputTypeDef(TypedDict):
    Arn: str
    FlowId: str
    Permissions: list[PermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFlowPermissionsOutputTypeDef(TypedDict):
    Status: int
    Arn: str
    Permissions: list[PermissionOutputTypeDef]
    RequestId: str
    FlowId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetIdentityContextRequestTypeDef(TypedDict):
    AwsAccountId: str
    UserIdentifier: UserIdentifierTypeDef
    Namespace: NotRequired[str]
    SessionExpiresAt: NotRequired[TimestampTypeDef]


class TableSideBorderOptionsTypeDef(TypedDict):
    InnerVertical: NotRequired[TableBorderOptionsTypeDef]
    InnerHorizontal: NotRequired[TableBorderOptionsTypeDef]
    Left: NotRequired[TableBorderOptionsTypeDef]
    Right: NotRequired[TableBorderOptionsTypeDef]
    Top: NotRequired[TableBorderOptionsTypeDef]
    Bottom: NotRequired[TableBorderOptionsTypeDef]


class GradientColorOutputTypeDef(TypedDict):
    Stops: NotRequired[list[GradientStopTypeDef]]


class GradientColorTypeDef(TypedDict):
    Stops: NotRequired[Sequence[GradientStopTypeDef]]


class GridLayoutCanvasSizeOptionsTypeDef(TypedDict):
    ScreenCanvasSizeOptions: NotRequired[GridLayoutScreenCanvasSizeOptionsTypeDef]


class GridLayoutElementTypeDef(TypedDict):
    ElementId: str
    ElementType: LayoutElementTypeType
    ColumnSpan: int
    RowSpan: int
    ColumnIndex: NotRequired[int]
    RowIndex: NotRequired[int]
    BorderStyle: NotRequired[GridLayoutElementBorderStyleTypeDef]
    SelectedBorderStyle: NotRequired[GridLayoutElementBorderStyleTypeDef]
    BackgroundStyle: NotRequired[GridLayoutElementBackgroundStyleTypeDef]
    LoadingAnimation: NotRequired[LoadingAnimationTypeDef]
    BorderRadius: NotRequired[str]
    Padding: NotRequired[str]


class SearchGroupsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    Filters: Sequence[GroupSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchGroupsRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    Filters: Sequence[GroupSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIAMPolicyAssignmentsResponseTypeDef(TypedDict):
    IAMPolicyAssignments: list[IAMPolicyAssignmentSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ImageConfigurationTypeDef(TypedDict):
    Source: NotRequired[ImageSourceTypeDef]


class ImageTypeDef(TypedDict):
    Source: NotRequired[ImageSourceTypeDef]
    GeneratedImageUrl: NotRequired[str]


class ImageInteractionOptionsTypeDef(TypedDict):
    ImageMenuOption: NotRequired[ImageMenuOptionTypeDef]


class IncrementalRefreshTypeDef(TypedDict):
    LookbackWindow: LookbackWindowTypeDef


class IngestionTypeDef(TypedDict):
    Arn: str
    IngestionStatus: IngestionStatusType
    CreatedTime: datetime
    IngestionId: NotRequired[str]
    ErrorInfo: NotRequired[ErrorInfoTypeDef]
    RowInfo: NotRequired[RowInfoTypeDef]
    QueueInfo: NotRequired[QueueInfoTypeDef]
    IngestionTimeInSeconds: NotRequired[int]
    IngestionSizeInBytes: NotRequired[int]
    RequestSource: NotRequired[IngestionRequestSourceType]
    RequestType: NotRequired[IngestionRequestTypeType]


class IntegerDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[IntegerDatasetParameterDefaultValuesOutputTypeDef]


IntegerDatasetParameterDefaultValuesUnionTypeDef = Union[
    IntegerDatasetParameterDefaultValuesTypeDef, IntegerDatasetParameterDefaultValuesOutputTypeDef
]
JoinInstructionTypeDef = TypedDict(
    "JoinInstructionTypeDef",
    {
        "LeftOperand": str,
        "RightOperand": str,
        "Type": JoinTypeType,
        "OnClause": str,
        "LeftJoinKeyProperties": NotRequired[JoinKeyPropertiesTypeDef],
        "RightJoinKeyProperties": NotRequired[JoinKeyPropertiesTypeDef],
    },
)


class JoinOperandPropertiesOutputTypeDef(TypedDict):
    OutputColumnNameOverrides: list[OutputColumnNameOverrideTypeDef]


class JoinOperandPropertiesTypeDef(TypedDict):
    OutputColumnNameOverrides: Sequence[OutputColumnNameOverrideTypeDef]


class KPIVisualLayoutOptionsTypeDef(TypedDict):
    StandardLayout: NotRequired[KPIVisualStandardLayoutTypeDef]


class LinkSharingConfigurationTypeDef(TypedDict):
    Permissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


ResourcePermissionUnionTypeDef = Union[ResourcePermissionTypeDef, ResourcePermissionOutputTypeDef]


class ListFolderMembersResponseTypeDef(TypedDict):
    Status: int
    FolderMemberList: list[MemberIdArnPairTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSelfUpgradesResponseTypeDef(TypedDict):
    SelfUpgradeRequestDetails: list[SelfUpgradeRequestDetailTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateSelfUpgradeResponseTypeDef(TypedDict):
    SelfUpgradeRequestDetail: SelfUpgradeRequestDetailTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListTemplateVersionsResponseTypeDef(TypedDict):
    TemplateVersionSummaryList: list[TemplateVersionSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTemplatesResponseTypeDef(TypedDict):
    TemplateSummaryList: list[TemplateSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListThemeVersionsResponseTypeDef(TypedDict):
    ThemeVersionSummaryList: list[ThemeVersionSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListThemesResponseTypeDef(TypedDict):
    ThemeSummaryList: list[ThemeSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTopicsResponseTypeDef(TypedDict):
    TopicsSummaries: list[TopicSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchTopicsResponseTypeDef(TypedDict):
    TopicSummaryList: list[TopicSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class VisualSubtitleLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FormatText: NotRequired[LongFormatTextTypeDef]


class S3ParametersTypeDef(TypedDict):
    ManifestFileLocation: ManifestFileLocationTypeDef
    RoleArn: NotRequired[str]


class TileLayoutStyleTypeDef(TypedDict):
    Gutter: NotRequired[GutterStyleTypeDef]
    Margin: NotRequired[MarginStyleTypeDef]


class NamedEntityDefinitionOutputTypeDef(TypedDict):
    FieldName: NotRequired[str]
    PropertyName: NotRequired[str]
    PropertyRole: NotRequired[PropertyRoleType]
    PropertyUsage: NotRequired[PropertyUsageType]
    Metric: NotRequired[NamedEntityDefinitionMetricOutputTypeDef]


class NamedEntityDefinitionTypeDef(TypedDict):
    FieldName: NotRequired[str]
    PropertyName: NotRequired[str]
    PropertyRole: NotRequired[PropertyRoleType]
    PropertyUsage: NotRequired[PropertyUsageType]
    Metric: NotRequired[NamedEntityDefinitionMetricTypeDef]


class NamespaceInfoV2TypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]
    CapacityRegion: NotRequired[str]
    CreationStatus: NotRequired[NamespaceStatusType]
    IdentityStore: NotRequired[Literal["QUICKSIGHT"]]
    NamespaceError: NotRequired[NamespaceErrorTypeDef]
    IamIdentityCenterApplicationArn: NotRequired[str]
    IamIdentityCenterInstanceArn: NotRequired[str]


class VPCConnectionSummaryTypeDef(TypedDict):
    VPCConnectionId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    VPCId: NotRequired[str]
    SecurityGroupIds: NotRequired[list[str]]
    DnsResolvers: NotRequired[list[str]]
    Status: NotRequired[VPCConnectionResourceStatusType]
    AvailabilityStatus: NotRequired[VPCConnectionAvailabilityStatusType]
    NetworkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]
    RoleArn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class VPCConnectionTypeDef(TypedDict):
    VPCConnectionId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    VPCId: NotRequired[str]
    SecurityGroupIds: NotRequired[list[str]]
    DnsResolvers: NotRequired[list[str]]
    Status: NotRequired[VPCConnectionResourceStatusType]
    AvailabilityStatus: NotRequired[VPCConnectionAvailabilityStatusType]
    NetworkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]
    RoleArn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class OverrideDatasetParameterOperationOutputTypeDef(TypedDict):
    ParameterName: str
    NewParameterName: NotRequired[str]
    NewDefaultValues: NotRequired[NewDefaultValuesOutputTypeDef]


class NumericSeparatorConfigurationTypeDef(TypedDict):
    DecimalSeparator: NotRequired[NumericSeparatorSymbolType]
    ThousandsSeparator: NotRequired[ThousandSeparatorOptionsTypeDef]


class NumericalAggregationFunctionTypeDef(TypedDict):
    SimpleNumericalAggregation: NotRequired[SimpleNumericalAggregationFunctionType]
    PercentileAggregation: NotRequired[PercentileAggregationTypeDef]


class ParametersOutputTypeDef(TypedDict):
    StringParameters: NotRequired[list[StringParameterOutputTypeDef]]
    IntegerParameters: NotRequired[list[IntegerParameterOutputTypeDef]]
    DecimalParameters: NotRequired[list[DecimalParameterOutputTypeDef]]
    DateTimeParameters: NotRequired[list[DateTimeParameterOutputTypeDef]]


class VisibleRangeOptionsTypeDef(TypedDict):
    PercentRange: NotRequired[PercentVisibleRangeTypeDef]


class PerformanceConfigurationOutputTypeDef(TypedDict):
    UniqueKeys: NotRequired[list[UniqueKeyOutputTypeDef]]


class PerformanceConfigurationTypeDef(TypedDict):
    UniqueKeys: NotRequired[Sequence[UniqueKeyTypeDef]]


PermissionUnionTypeDef = Union[PermissionTypeDef, PermissionOutputTypeDef]


class PivotConfigurationOutputTypeDef(TypedDict):
    PivotedLabels: list[PivotedLabelTypeDef]
    LabelColumnName: NotRequired[str]


class PivotConfigurationTypeDef(TypedDict):
    PivotedLabels: Sequence[PivotedLabelTypeDef]
    LabelColumnName: NotRequired[str]


class PluginVisualOptionsOutputTypeDef(TypedDict):
    VisualProperties: NotRequired[list[PluginVisualPropertyTypeDef]]


class PluginVisualOptionsTypeDef(TypedDict):
    VisualProperties: NotRequired[Sequence[PluginVisualPropertyTypeDef]]


class RadarChartSeriesSettingsTypeDef(TypedDict):
    AreaStyleSettings: NotRequired[RadarChartAreaStyleSettingsTypeDef]


class TopicRangeFilterConstantTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    RangeConstant: NotRequired[RangeConstantTypeDef]


class ReadAuthorizationCodeGrantCredentialsDetailsTypeDef(TypedDict):
    ReadAuthorizationCodeGrantDetails: NotRequired[ReadAuthorizationCodeGrantDetailsTypeDef]


class ReadClientCredentialsDetailsTypeDef(TypedDict):
    ReadClientCredentialsGrantDetails: NotRequired[ReadClientCredentialsGrantDetailsTypeDef]


class RedshiftParametersOutputTypeDef(TypedDict):
    Database: str
    Host: NotRequired[str]
    Port: NotRequired[int]
    ClusterId: NotRequired[str]
    IAMParameters: NotRequired[RedshiftIAMParametersOutputTypeDef]
    IdentityCenterConfiguration: NotRequired[IdentityCenterConfigurationTypeDef]


RedshiftIAMParametersUnionTypeDef = Union[
    RedshiftIAMParametersTypeDef, RedshiftIAMParametersOutputTypeDef
]


class RefreshFailureConfigurationTypeDef(TypedDict):
    EmailAlert: NotRequired[RefreshFailureEmailAlertTypeDef]


class RefreshFrequencyTypeDef(TypedDict):
    Interval: RefreshIntervalType
    RefreshOnDay: NotRequired[ScheduleRefreshOnEntityTypeDef]
    Timezone: NotRequired[str]
    TimeOfTheDay: NotRequired[str]


class RowLevelPermissionTagConfigurationOutputTypeDef(TypedDict):
    TagRules: list[RowLevelPermissionTagRuleTypeDef]
    Status: NotRequired[StatusType]
    TagRuleConfigurations: NotRequired[list[list[str]]]


class RowLevelPermissionTagConfigurationTypeDef(TypedDict):
    TagRules: Sequence[RowLevelPermissionTagRuleTypeDef]
    Status: NotRequired[StatusType]
    TagRuleConfigurations: NotRequired[Sequence[Sequence[str]]]


class SnapshotS3DestinationConfigurationTypeDef(TypedDict):
    BucketConfiguration: S3BucketConfigurationTypeDef


class S3SourceOutputTypeDef(TypedDict):
    DataSourceArn: str
    InputColumns: list[InputColumnTypeDef]
    UploadSettings: NotRequired[UploadSettingsTypeDef]


class S3SourceTypeDef(TypedDict):
    DataSourceArn: str
    InputColumns: Sequence[InputColumnTypeDef]
    UploadSettings: NotRequired[UploadSettingsTypeDef]


class SaaSTableOutputTypeDef(TypedDict):
    DataSourceArn: str
    TablePath: list[TablePathElementTypeDef]
    InputColumns: list[InputColumnTypeDef]


class SaaSTableTypeDef(TypedDict):
    DataSourceArn: str
    TablePath: Sequence[TablePathElementTypeDef]
    InputColumns: Sequence[InputColumnTypeDef]


class SearchFlowsInputPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[SearchFlowsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchFlowsInputTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[SearchFlowsFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchTopicsRequestPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[TopicSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchTopicsRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[TopicSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SectionBasedLayoutPaperCanvasSizeOptionsTypeDef(TypedDict):
    PaperSize: NotRequired[PaperSizeType]
    PaperOrientation: NotRequired[PaperOrientationType]
    PaperMargin: NotRequired[SpacingTypeDef]


class SectionStyleTypeDef(TypedDict):
    Height: NotRequired[str]
    Padding: NotRequired[SpacingTypeDef]


class SelectedSheetsFilterScopeConfigurationOutputTypeDef(TypedDict):
    SheetVisualScopingConfigurations: NotRequired[
        list[SheetVisualScopingConfigurationOutputTypeDef]
    ]


class SelectedSheetsFilterScopeConfigurationTypeDef(TypedDict):
    SheetVisualScopingConfigurations: NotRequired[Sequence[SheetVisualScopingConfigurationTypeDef]]


class SheetElementRenderingRuleTypeDef(TypedDict):
    Expression: str
    ConfigurationOverrides: SheetElementConfigurationOverridesTypeDef


class SheetImageSourceTypeDef(TypedDict):
    SheetImageStaticFileSource: NotRequired[SheetImageStaticFileSourceTypeDef]


class SheetImageTooltipConfigurationTypeDef(TypedDict):
    TooltipText: NotRequired[SheetImageTooltipTextTypeDef]
    Visibility: NotRequired[VisibilityType]


class SheetLayoutGroupOutputTypeDef(TypedDict):
    Id: str
    Members: list[SheetLayoutGroupMemberTypeDef]


class SheetLayoutGroupTypeDef(TypedDict):
    Id: str
    Members: Sequence[SheetLayoutGroupMemberTypeDef]


class VisualTitleLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FormatText: NotRequired[ShortFormatTextTypeDef]


class SingleAxisOptionsTypeDef(TypedDict):
    YAxisOptions: NotRequired[YAxisOptionsTypeDef]


class TopicTemplateOutputTypeDef(TypedDict):
    TemplateType: NotRequired[str]
    Slots: NotRequired[list[SlotTypeDef]]


class TopicTemplateTypeDef(TypedDict):
    TemplateType: NotRequired[str]
    Slots: NotRequired[Sequence[SlotTypeDef]]


class SnapshotUserConfigurationRedactedTypeDef(TypedDict):
    AnonymousUsers: NotRequired[list[SnapshotAnonymousUserRedactedTypeDef]]


class SnapshotFileOutputTypeDef(TypedDict):
    SheetSelections: list[SnapshotFileSheetSelectionOutputTypeDef]
    FormatType: SnapshotFileFormatTypeType


class SnapshotFileTypeDef(TypedDict):
    SheetSelections: Sequence[SnapshotFileSheetSelectionTypeDef]
    FormatType: SnapshotFileFormatTypeType


class StaticFileSourceTypeDef(TypedDict):
    UrlOptions: NotRequired[StaticFileUrlSourceOptionsTypeDef]
    S3Options: NotRequired[StaticFileS3SourceOptionsTypeDef]


class StringDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[StringDatasetParameterDefaultValuesOutputTypeDef]


StringDatasetParameterDefaultValuesUnionTypeDef = Union[
    StringDatasetParameterDefaultValuesTypeDef, StringDatasetParameterDefaultValuesOutputTypeDef
]


class UpdateKeyRegistrationResponseTypeDef(TypedDict):
    FailedKeyRegistration: list[FailedKeyRegistrationEntryTypeDef]
    SuccessfulKeyRegistration: list[SuccessfulKeyRegistrationEntryTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TableFieldImageConfigurationTypeDef(TypedDict):
    SizingOptions: NotRequired[TableCellImageSizingConfigurationTypeDef]


class TextBoxInteractionOptionsTypeDef(TypedDict):
    TextBoxMenuOption: NotRequired[TextBoxMenuOptionTypeDef]


class TopicNullFilterTypeDef(TypedDict):
    NullFilterType: NotRequired[NullFilterTypeType]
    Constant: NotRequired[TopicSingularFilterConstantTypeDef]
    Inverse: NotRequired[bool]


class TopicNumericEqualityFilterTypeDef(TypedDict):
    Constant: NotRequired[TopicSingularFilterConstantTypeDef]
    Aggregation: NotRequired[NamedFilterAggTypeType]


class TopicRelativeDateFilterTypeDef(TypedDict):
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    RelativeDateFilterFunction: NotRequired[TopicRelativeDateFilterFunctionType]
    Constant: NotRequired[TopicSingularFilterConstantTypeDef]


class TotalAggregationOptionTypeDef(TypedDict):
    FieldId: str
    TotalAggregationFunction: TotalAggregationFunctionTypeDef


UntagColumnOperationUnionTypeDef = Union[
    UntagColumnOperationTypeDef, UntagColumnOperationOutputTypeDef
]


class VisualCustomActionDefaultsTypeDef(TypedDict):
    highlightOperation: NotRequired[VisualHighlightOperationTypeDef]


class WaterfallChartColorConfigurationTypeDef(TypedDict):
    GroupColorConfiguration: NotRequired[WaterfallChartGroupColorConfigurationTypeDef]


class ListActionConnectorsResponseTypeDef(TypedDict):
    ActionConnectorSummaries: list[ActionConnectorSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchActionConnectorsResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ActionConnectorSummaries: list[ActionConnectorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CascadingControlConfigurationOutputTypeDef(TypedDict):
    SourceControls: NotRequired[list[CascadingControlSourceTypeDef]]


class CascadingControlConfigurationTypeDef(TypedDict):
    SourceControls: NotRequired[Sequence[CascadingControlSourceTypeDef]]


class DateTimeDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[list[datetime]]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]


class DateTimeDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[TimestampTypeDef]]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]


class DecimalDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[list[float]]


class DecimalDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[float]]


class IntegerDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[list[int]]


class IntegerDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[int]]


class StringDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[list[str]]


class StringDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[str]]


class DrillDownFilterOutputTypeDef(TypedDict):
    NumericEqualityFilter: NotRequired[NumericEqualityDrillDownFilterTypeDef]
    CategoryFilter: NotRequired[CategoryDrillDownFilterOutputTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeDrillDownFilterOutputTypeDef]


class DashboardCustomizationVisualOptionsOutputTypeDef(TypedDict):
    FieldsConfiguration: NotRequired[VisualCustomizationFieldsConfigurationOutputTypeDef]


class DashboardCustomizationVisualOptionsTypeDef(TypedDict):
    FieldsConfiguration: NotRequired[VisualCustomizationFieldsConfigurationTypeDef]


class RegisteredUserDashboardFeatureConfigurationsTypeDef(TypedDict):
    StatePersistence: NotRequired[StatePersistenceConfigurationsTypeDef]
    Bookmarks: NotRequired[BookmarksConfigurationsTypeDef]
    SharedView: NotRequired[SharedViewConfigurationsTypeDef]
    AmazonQInQuickSight: NotRequired[AmazonQInQuickSightDashboardConfigurationsTypeDef]
    Schedules: NotRequired[SchedulesConfigurationsTypeDef]
    RecentSnapshots: NotRequired[RecentSnapshotsConfigurationsTypeDef]
    ThresholdAlerts: NotRequired[ThresholdAlertsConfigurationsTypeDef]


class RegisteredUserConsoleFeatureConfigurationsTypeDef(TypedDict):
    StatePersistence: NotRequired[StatePersistenceConfigurationsTypeDef]
    SharedView: NotRequired[SharedViewConfigurationsTypeDef]
    AmazonQInQuickSight: NotRequired[AmazonQInQuickSightConsoleConfigurationsTypeDef]
    Schedules: NotRequired[SchedulesConfigurationsTypeDef]
    RecentSnapshots: NotRequired[RecentSnapshotsConfigurationsTypeDef]
    ThresholdAlerts: NotRequired[ThresholdAlertsConfigurationsTypeDef]


class AnalysisSourceEntityTypeDef(TypedDict):
    SourceTemplate: NotRequired[AnalysisSourceTemplateTypeDef]


class DashboardSourceEntityTypeDef(TypedDict):
    SourceTemplate: NotRequired[DashboardSourceTemplateTypeDef]


class TemplateSourceEntityTypeDef(TypedDict):
    SourceAnalysis: NotRequired[TemplateSourceAnalysisTypeDef]
    SourceTemplate: NotRequired[TemplateSourceTemplateTypeDef]


class AnonymousUserDashboardEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardId: str
    EnabledFeatures: NotRequired[Sequence[Literal["SHARED_VIEW"]]]
    DisabledFeatures: NotRequired[Sequence[Literal["SHARED_VIEW"]]]
    FeatureConfigurations: NotRequired[AnonymousUserDashboardFeatureConfigurationsTypeDef]


class DescribeAssetBundleExportJobResponseTypeDef(TypedDict):
    JobStatus: AssetBundleExportJobStatusType
    DownloadUrl: str
    Errors: list[AssetBundleExportJobErrorTypeDef]
    Arn: str
    CreatedTime: datetime
    AssetBundleExportJobId: str
    AwsAccountId: str
    ResourceArns: list[str]
    IncludeAllDependencies: bool
    ExportFormat: AssetBundleExportFormatType
    CloudFormationOverridePropertyConfiguration: (
        AssetBundleCloudFormationOverridePropertyConfigurationOutputTypeDef
    )
    RequestId: str
    Status: int
    IncludePermissions: bool
    IncludeTags: bool
    ValidationStrategy: AssetBundleExportJobValidationStrategyTypeDef
    Warnings: list[AssetBundleExportJobWarningTypeDef]
    IncludeFolderMemberships: bool
    IncludeFolderMembers: IncludeFolderMembersType
    ResponseMetadata: ResponseMetadataTypeDef


AssetBundleCloudFormationOverridePropertyConfigurationUnionTypeDef = Union[
    AssetBundleCloudFormationOverridePropertyConfigurationTypeDef,
    AssetBundleCloudFormationOverridePropertyConfigurationOutputTypeDef,
]


class AssetBundleImportJobDashboardOverridePermissionsOutputTypeDef(TypedDict):
    DashboardIds: list[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsOutputTypeDef]
    LinkSharingConfiguration: NotRequired[AssetBundleResourceLinkSharingConfigurationOutputTypeDef]


class AssetBundleImportJobDashboardOverridePermissionsTypeDef(TypedDict):
    DashboardIds: Sequence[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsTypeDef]
    LinkSharingConfiguration: NotRequired[AssetBundleResourceLinkSharingConfigurationTypeDef]


class AssetBundleImportJobOverrideTagsOutputTypeDef(TypedDict):
    VPCConnections: NotRequired[list[AssetBundleImportJobVPCConnectionOverrideTagsOutputTypeDef]]
    DataSources: NotRequired[list[AssetBundleImportJobDataSourceOverrideTagsOutputTypeDef]]
    DataSets: NotRequired[list[AssetBundleImportJobDataSetOverrideTagsOutputTypeDef]]
    Themes: NotRequired[list[AssetBundleImportJobThemeOverrideTagsOutputTypeDef]]
    Analyses: NotRequired[list[AssetBundleImportJobAnalysisOverrideTagsOutputTypeDef]]
    Dashboards: NotRequired[list[AssetBundleImportJobDashboardOverrideTagsOutputTypeDef]]
    Folders: NotRequired[list[AssetBundleImportJobFolderOverrideTagsOutputTypeDef]]


class AssetBundleImportJobOverrideTagsTypeDef(TypedDict):
    VPCConnections: NotRequired[Sequence[AssetBundleImportJobVPCConnectionOverrideTagsTypeDef]]
    DataSources: NotRequired[Sequence[AssetBundleImportJobDataSourceOverrideTagsTypeDef]]
    DataSets: NotRequired[Sequence[AssetBundleImportJobDataSetOverrideTagsTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleImportJobThemeOverrideTagsTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleImportJobAnalysisOverrideTagsTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleImportJobDashboardOverrideTagsTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleImportJobFolderOverrideTagsTypeDef]]


class SnowflakeParametersTypeDef(TypedDict):
    Host: str
    Database: str
    Warehouse: str
    AuthenticationType: NotRequired[AuthenticationTypeType]
    DatabaseAccessControlRole: NotRequired[str]
    OAuthParameters: NotRequired[OAuthParametersTypeDef]


class StarburstParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Catalog: str
    ProductType: NotRequired[StarburstProductTypeType]
    DatabaseAccessControlRole: NotRequired[str]
    AuthenticationType: NotRequired[AuthenticationTypeType]
    OAuthParameters: NotRequired[OAuthParametersTypeDef]


class CustomValuesConfigurationTypeDef(TypedDict):
    CustomValues: CustomParameterValuesTypeDef
    IncludeNullValue: NotRequired[bool]


DataSetDateFilterValueUnionTypeDef = Union[
    DataSetDateFilterValueTypeDef, DataSetDateFilterValueOutputTypeDef
]
DateTimeDatasetParameterDefaultValuesUnionTypeDef = Union[
    DateTimeDatasetParameterDefaultValuesTypeDef, DateTimeDatasetParameterDefaultValuesOutputTypeDef
]


class ParametersTypeDef(TypedDict):
    StringParameters: NotRequired[Sequence[StringParameterTypeDef]]
    IntegerParameters: NotRequired[Sequence[IntegerParameterTypeDef]]
    DecimalParameters: NotRequired[Sequence[DecimalParameterTypeDef]]
    DateTimeParameters: NotRequired[Sequence[DateTimeParameterTypeDef]]


NewDefaultValuesUnionTypeDef = Union[NewDefaultValuesTypeDef, NewDefaultValuesOutputTypeDef]


class DrillDownFilterTypeDef(TypedDict):
    NumericEqualityFilter: NotRequired[NumericEqualityDrillDownFilterTypeDef]
    CategoryFilter: NotRequired[CategoryDrillDownFilterTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeDrillDownFilterTypeDef]


TopicRefreshScheduleUnionTypeDef = Union[
    TopicRefreshScheduleTypeDef, TopicRefreshScheduleOutputTypeDef
]


class ForecastScenarioTypeDef(TypedDict):
    WhatIfPointScenario: NotRequired[WhatIfPointScenarioTypeDef]
    WhatIfRangeScenario: NotRequired[WhatIfRangeScenarioTypeDef]


class AuthorizationCodeGrantMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    RedirectUrl: str
    AuthorizationCodeGrantCredentialsSource: NotRequired[Literal["PLAIN_CREDENTIALS"]]
    AuthorizationCodeGrantCredentialsDetails: NotRequired[
        AuthorizationCodeGrantCredentialsDetailsTypeDef
    ]


class NumericAxisOptionsOutputTypeDef(TypedDict):
    Scale: NotRequired[AxisScaleTypeDef]
    Range: NotRequired[AxisDisplayRangeOutputTypeDef]


class NumericAxisOptionsTypeDef(TypedDict):
    Scale: NotRequired[AxisScaleTypeDef]
    Range: NotRequired[AxisDisplayRangeTypeDef]


class DataFieldBarSeriesItemTypeDef(TypedDict):
    FieldId: str
    FieldValue: NotRequired[str]
    Settings: NotRequired[BarChartSeriesSettingsTypeDef]


class FieldBarSeriesItemTypeDef(TypedDict):
    FieldId: str
    Settings: NotRequired[BarChartSeriesSettingsTypeDef]


class BrandElementStyleTypeDef(TypedDict):
    NavbarStyle: NotRequired[NavbarStyleTypeDef]


class DescribeCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    CustomPermissions: CustomPermissionsTypeDef
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    CustomPermissionsList: list[CustomPermissionsTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClientCredentialsGrantMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    ClientCredentialsSource: NotRequired[Literal["PLAIN_CREDENTIALS"]]
    ClientCredentialsDetails: NotRequired[ClientCredentialsDetailsTypeDef]


class ClusterMarkerConfigurationTypeDef(TypedDict):
    ClusterMarker: NotRequired[ClusterMarkerTypeDef]


TopicConstantValueUnionTypeDef = Union[TopicConstantValueTypeDef, TopicConstantValueOutputTypeDef]


class TopicCategoryFilterOutputTypeDef(TypedDict):
    CategoryFilterFunction: NotRequired[CategoryFilterFunctionType]
    CategoryFilterType: NotRequired[CategoryFilterTypeType]
    Constant: NotRequired[TopicCategoryFilterConstantOutputTypeDef]
    Inverse: NotRequired[bool]


class TopicCategoryFilterTypeDef(TypedDict):
    CategoryFilterFunction: NotRequired[CategoryFilterFunctionType]
    CategoryFilterType: NotRequired[CategoryFilterTypeType]
    Constant: NotRequired[TopicCategoryFilterConstantTypeDef]
    Inverse: NotRequired[bool]


class TagColumnOperationOutputTypeDef(TypedDict):
    ColumnName: str
    Tags: list[ColumnTagTypeDef]


class TagColumnOperationTypeDef(TypedDict):
    ColumnName: str
    Tags: Sequence[ColumnTagTypeDef]


class DataSetConfigurationOutputTypeDef(TypedDict):
    Placeholder: NotRequired[str]
    DataSetSchema: NotRequired[DataSetSchemaOutputTypeDef]
    ColumnGroupSchemaList: NotRequired[list[ColumnGroupSchemaOutputTypeDef]]


class DataSetConfigurationTypeDef(TypedDict):
    Placeholder: NotRequired[str]
    DataSetSchema: NotRequired[DataSetSchemaTypeDef]
    ColumnGroupSchemaList: NotRequired[Sequence[ColumnGroupSchemaTypeDef]]


class DataFieldComboSeriesItemTypeDef(TypedDict):
    FieldId: str
    FieldValue: NotRequired[str]
    Settings: NotRequired[ComboChartSeriesSettingsTypeDef]


class FieldComboSeriesItemTypeDef(TypedDict):
    FieldId: str
    Settings: NotRequired[ComboChartSeriesSettingsTypeDef]


class DataFieldSeriesItemTypeDef(TypedDict):
    FieldId: str
    AxisBinding: AxisBindingType
    FieldValue: NotRequired[str]
    Settings: NotRequired[LineChartSeriesSettingsTypeDef]


class FieldSeriesItemTypeDef(TypedDict):
    FieldId: str
    AxisBinding: AxisBindingType
    Settings: NotRequired[LineChartSeriesSettingsTypeDef]


class ConditionalFormattingIconTypeDef(TypedDict):
    IconSet: NotRequired[ConditionalFormattingIconSetTypeDef]
    CustomCondition: NotRequired[ConditionalFormattingCustomIconConditionTypeDef]


class ListDataSetsResponseTypeDef(TypedDict):
    DataSetSummaries: list[DataSetSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchDataSetsResponseTypeDef(TypedDict):
    DataSetSummaries: list[DataSetSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DestinationParameterValueConfigurationOutputTypeDef(TypedDict):
    CustomValuesConfiguration: NotRequired[CustomValuesConfigurationOutputTypeDef]
    SelectAllValueOptions: NotRequired[Literal["ALL_VALUES"]]
    SourceParameterName: NotRequired[str]
    SourceField: NotRequired[str]
    SourceColumn: NotRequired[ColumnIdentifierTypeDef]


CustomSqlUnionTypeDef = Union[CustomSqlTypeDef, CustomSqlOutputTypeDef]


class SourceTableOutputTypeDef(TypedDict):
    PhysicalTableId: NotRequired[str]
    DataSet: NotRequired[ParentDataSetOutputTypeDef]


class SourceTableTypeDef(TypedDict):
    PhysicalTableId: NotRequired[str]
    DataSet: NotRequired[ParentDataSetTypeDef]


RelationalTableUnionTypeDef = Union[RelationalTableTypeDef, RelationalTableOutputTypeDef]


class CustomContentConfigurationTypeDef(TypedDict):
    ContentUrl: NotRequired[str]
    ContentType: NotRequired[CustomContentTypeType]
    ImageScaling: NotRequired[CustomContentImageScalingConfigurationType]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class DashboardPublishOptionsTypeDef(TypedDict):
    AdHocFilteringOption: NotRequired[AdHocFilteringOptionTypeDef]
    ExportToCSVOption: NotRequired[ExportToCSVOptionTypeDef]
    SheetControlsOption: NotRequired[SheetControlsOptionTypeDef]
    VisualPublishOptions: NotRequired[DashboardVisualPublishOptionsTypeDef]
    SheetLayoutElementMaximizationOption: NotRequired[SheetLayoutElementMaximizationOptionTypeDef]
    VisualMenuOption: NotRequired[VisualMenuOptionTypeDef]
    VisualAxisSortOption: NotRequired[VisualAxisSortOptionTypeDef]
    ExportWithHiddenFieldsOption: NotRequired[ExportWithHiddenFieldsOptionTypeDef]
    DataPointDrillUpDownOption: NotRequired[DataPointDrillUpDownOptionTypeDef]
    DataPointMenuLabelOption: NotRequired[DataPointMenuLabelOptionTypeDef]
    DataPointTooltipOption: NotRequired[DataPointTooltipOptionTypeDef]
    DataQAEnabledOption: NotRequired[DataQAEnabledOptionTypeDef]
    QuickSuiteActionsOption: NotRequired[QuickSuiteActionsOptionTypeDef]
    ExecutiveSummaryOption: NotRequired[ExecutiveSummaryOptionTypeDef]
    DataStoriesSharingOption: NotRequired[DataStoriesSharingOptionTypeDef]


class DataPathColorTypeDef(TypedDict):
    Element: DataPathValueTypeDef
    Color: str
    TimeGranularity: NotRequired[TimeGranularityType]


class DataPathSortOutputTypeDef(TypedDict):
    Direction: SortDirectionType
    SortPaths: list[DataPathValueTypeDef]


class DataPathSortTypeDef(TypedDict):
    Direction: SortDirectionType
    SortPaths: Sequence[DataPathValueTypeDef]


class PivotTableDataPathOptionOutputTypeDef(TypedDict):
    DataPathList: list[DataPathValueTypeDef]
    Width: NotRequired[str]


class PivotTableDataPathOptionTypeDef(TypedDict):
    DataPathList: Sequence[DataPathValueTypeDef]
    Width: NotRequired[str]


class PivotTableFieldCollapseStateTargetOutputTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldDataPathValues: NotRequired[list[DataPathValueTypeDef]]


class PivotTableFieldCollapseStateTargetTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldDataPathValues: NotRequired[Sequence[DataPathValueTypeDef]]


class AggregationTypeDef(TypedDict):
    AggregationFunction: DataPrepAggregationFunctionTypeDef
    NewColumnName: str
    NewColumnId: str


class ValueColumnConfigurationTypeDef(TypedDict):
    AggregationFunction: NotRequired[DataPrepAggregationFunctionTypeDef]


class ImportTableOperationOutputTypeDef(TypedDict):
    Alias: str
    Source: ImportTableOperationSourceOutputTypeDef


class ImportTableOperationTypeDef(TypedDict):
    Alias: str
    Source: ImportTableOperationSourceTypeDef


class AppendOperationOutputTypeDef(TypedDict):
    Alias: str
    AppendedColumns: list[AppendedColumnTypeDef]
    FirstSource: NotRequired[TransformOperationSourceOutputTypeDef]
    SecondSource: NotRequired[TransformOperationSourceOutputTypeDef]


class CastColumnTypesOperationOutputTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceOutputTypeDef
    CastColumnTypeOperations: list[CastColumnTypeOperationTypeDef]


class CreateColumnsOperationOutputTypeDef(TypedDict):
    Columns: list[CalculatedColumnTypeDef]
    Alias: NotRequired[str]
    Source: NotRequired[TransformOperationSourceOutputTypeDef]


class ProjectOperationOutputTypeDef(TypedDict):
    ProjectedColumns: list[str]
    Alias: NotRequired[str]
    Source: NotRequired[TransformOperationSourceOutputTypeDef]


class RenameColumnsOperationOutputTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceOutputTypeDef
    RenameColumnOperations: list[RenameColumnOperationTypeDef]


class UnpivotOperationOutputTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceOutputTypeDef
    ColumnsToUnpivot: list[ColumnToUnpivotTypeDef]
    UnpivotedLabelColumnName: str
    UnpivotedLabelColumnId: str
    UnpivotedValueColumnName: str
    UnpivotedValueColumnId: str


class AppendOperationTypeDef(TypedDict):
    Alias: str
    AppendedColumns: Sequence[AppendedColumnTypeDef]
    FirstSource: NotRequired[TransformOperationSourceTypeDef]
    SecondSource: NotRequired[TransformOperationSourceTypeDef]


class CastColumnTypesOperationTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceTypeDef
    CastColumnTypeOperations: Sequence[CastColumnTypeOperationTypeDef]


class RenameColumnsOperationTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceTypeDef
    RenameColumnOperations: Sequence[RenameColumnOperationTypeDef]


TransformOperationSourceUnionTypeDef = Union[
    TransformOperationSourceTypeDef, TransformOperationSourceOutputTypeDef
]


class UnpivotOperationTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceTypeDef
    ColumnsToUnpivot: Sequence[ColumnToUnpivotTypeDef]
    UnpivotedLabelColumnName: str
    UnpivotedLabelColumnId: str
    UnpivotedValueColumnName: str
    UnpivotedValueColumnId: str


class DataSetDateFilterConditionOutputTypeDef(TypedDict):
    ColumnName: NotRequired[str]
    ComparisonFilterCondition: NotRequired[DataSetDateComparisonFilterConditionOutputTypeDef]
    RangeFilterCondition: NotRequired[DataSetDateRangeFilterConditionOutputTypeDef]


class DataSetNumericFilterConditionTypeDef(TypedDict):
    ColumnName: NotRequired[str]
    ComparisonFilterCondition: NotRequired[DataSetNumericComparisonFilterConditionTypeDef]
    RangeFilterCondition: NotRequired[DataSetNumericRangeFilterConditionTypeDef]


class DataSetStringFilterConditionOutputTypeDef(TypedDict):
    ColumnName: NotRequired[str]
    ComparisonFilterCondition: NotRequired[DataSetStringComparisonFilterConditionTypeDef]
    ListFilterCondition: NotRequired[DataSetStringListFilterConditionOutputTypeDef]


class DataSetStringListFilterConditionTypeDef(TypedDict):
    Operator: DataSetStringListFilterOperatorType
    Values: NotRequired[DataSetStringListFilterValueUnionTypeDef]


class DecimalDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[DecimalDatasetParameterDefaultValuesUnionTypeDef]


class DescribeDashboardPermissionsResponseTypeDef(TypedDict):
    DashboardId: str
    DashboardArn: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    LinkSharingConfiguration: LinkSharingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardPermissionsResponseTypeDef(TypedDict):
    DashboardArn: str
    DashboardId: str
    Permissions: list[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    LinkSharingConfiguration: LinkSharingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTopicRefreshSchedulesResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    RefreshSchedules: list[TopicRefreshScheduleSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DefaultFormattingTypeDef(TypedDict):
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]


class TopicIRMetricOutputTypeDef(TypedDict):
    MetricId: NotRequired[IdentifierTypeDef]
    Function: NotRequired[AggFunctionOutputTypeDef]
    Operands: NotRequired[list[IdentifierTypeDef]]
    ComparisonMethod: NotRequired[TopicIRComparisonMethodTypeDef]
    Expression: NotRequired[str]
    CalculatedFieldReferences: NotRequired[list[IdentifierTypeDef]]
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]
    NamedEntity: NotRequired[NamedEntityRefTypeDef]


class TopicIRMetricTypeDef(TypedDict):
    MetricId: NotRequired[IdentifierTypeDef]
    Function: NotRequired[AggFunctionUnionTypeDef]
    Operands: NotRequired[Sequence[IdentifierTypeDef]]
    ComparisonMethod: NotRequired[TopicIRComparisonMethodTypeDef]
    Expression: NotRequired[str]
    CalculatedFieldReferences: NotRequired[Sequence[IdentifierTypeDef]]
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]
    NamedEntity: NotRequired[NamedEntityRefTypeDef]


class TopicIRFilterOptionOutputTypeDef(TypedDict):
    FilterType: NotRequired[TopicIRFilterTypeType]
    FilterClass: NotRequired[FilterClassType]
    OperandField: NotRequired[IdentifierTypeDef]
    Function: NotRequired[TopicIRFilterFunctionType]
    Constant: NotRequired[TopicConstantValueOutputTypeDef]
    Inverse: NotRequired[bool]
    NullFilter: NotRequired[NullFilterOptionType]
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[dict[str, str]]
    AggregationPartitionBy: NotRequired[list[AggregationPartitionByTypeDef]]
    Range: NotRequired[TopicConstantValueOutputTypeDef]
    Inclusive: NotRequired[bool]
    TimeGranularity: NotRequired[TimeGranularityType]
    LastNextOffset: NotRequired[TopicConstantValueOutputTypeDef]
    AggMetrics: NotRequired[list[FilterAggMetricsTypeDef]]
    TopBottomLimit: NotRequired[TopicConstantValueOutputTypeDef]
    SortDirection: NotRequired[TopicSortDirectionType]
    Anchor: NotRequired[AnchorTypeDef]


class TopicIRGroupByTypeDef(TypedDict):
    FieldName: NotRequired[IdentifierTypeDef]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    Sort: NotRequired[TopicSortClauseTypeDef]
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]
    NamedEntity: NotRequired[NamedEntityRefTypeDef]


class CustomActionFilterOperationOutputTypeDef(TypedDict):
    SelectedFieldsConfiguration: FilterOperationSelectedFieldsConfigurationOutputTypeDef
    TargetVisualsConfiguration: FilterOperationTargetVisualsConfigurationOutputTypeDef


class CustomActionFilterOperationTypeDef(TypedDict):
    SelectedFieldsConfiguration: FilterOperationSelectedFieldsConfigurationTypeDef
    TargetVisualsConfiguration: FilterOperationTargetVisualsConfigurationTypeDef


class AxisLabelOptionsTypeDef(TypedDict):
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    CustomLabel: NotRequired[str]
    ApplyTo: NotRequired[AxisLabelReferenceOptionsTypeDef]


class DataLabelOptionsOutputTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CategoryLabelVisibility: NotRequired[VisibilityType]
    MeasureLabelVisibility: NotRequired[VisibilityType]
    DataLabelTypes: NotRequired[list[DataLabelTypeTypeDef]]
    Position: NotRequired[DataLabelPositionType]
    LabelContent: NotRequired[DataLabelContentType]
    LabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LabelColor: NotRequired[str]
    Overlap: NotRequired[DataLabelOverlapType]
    TotalsVisibility: NotRequired[VisibilityType]


class DataLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CategoryLabelVisibility: NotRequired[VisibilityType]
    MeasureLabelVisibility: NotRequired[VisibilityType]
    DataLabelTypes: NotRequired[Sequence[DataLabelTypeTypeDef]]
    Position: NotRequired[DataLabelPositionType]
    LabelContent: NotRequired[DataLabelContentType]
    LabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LabelColor: NotRequired[str]
    Overlap: NotRequired[DataLabelOverlapType]
    TotalsVisibility: NotRequired[VisibilityType]


class FunnelChartDataLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CategoryLabelVisibility: NotRequired[VisibilityType]
    MeasureLabelVisibility: NotRequired[VisibilityType]
    Position: NotRequired[DataLabelPositionType]
    LabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LabelColor: NotRequired[str]
    MeasureDataLabelStyle: NotRequired[FunnelChartMeasureDataLabelStyleType]


class LabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    CustomLabel: NotRequired[str]


class PanelTitleOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    HorizontalTextAlignment: NotRequired[HorizontalTextAlignmentType]


class TableFieldCustomTextContentTypeDef(TypedDict):
    FontConfiguration: FontConfigurationTypeDef
    Value: NotRequired[str]


class VisualSubtitleFontConfigurationTypeDef(TypedDict):
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    TextAlignment: NotRequired[HorizontalTextAlignmentType]
    TextTransform: NotRequired[Literal["CAPITALIZE"]]


class VisualTitleFontConfigurationTypeDef(TypedDict):
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    TextAlignment: NotRequired[HorizontalTextAlignmentType]
    TextTransform: NotRequired[Literal["CAPITALIZE"]]


class ForecastConfigurationOutputTypeDef(TypedDict):
    ForecastProperties: NotRequired[TimeBasedForecastPropertiesTypeDef]
    Scenario: NotRequired[ForecastScenarioOutputTypeDef]


class DefaultFreeFormLayoutConfigurationTypeDef(TypedDict):
    CanvasSizeOptions: FreeFormLayoutCanvasSizeOptionsTypeDef


class SnapshotUserConfigurationTypeDef(TypedDict):
    AnonymousUsers: NotRequired[Sequence[SnapshotAnonymousUserTypeDef]]


class PredictQAResultsResponseTypeDef(TypedDict):
    PrimaryResult: QAResultTypeDef
    AdditionalResults: list[QAResultTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ColumnGroupTypeDef(TypedDict):
    GeoSpatialColumnGroup: NotRequired[GeoSpatialColumnGroupUnionTypeDef]


class GeocodePreferenceTypeDef(TypedDict):
    RequestKey: GeocoderHierarchyTypeDef
    Preference: GeocodePreferenceValueTypeDef


class GeospatialHeatmapConfigurationOutputTypeDef(TypedDict):
    HeatmapColor: NotRequired[GeospatialHeatmapColorScaleOutputTypeDef]


class GeospatialHeatmapConfigurationTypeDef(TypedDict):
    HeatmapColor: NotRequired[GeospatialHeatmapColorScaleTypeDef]


class GeospatialCategoricalColorOutputTypeDef(TypedDict):
    CategoryDataColors: list[GeospatialCategoricalDataColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GeospatialCategoricalColorTypeDef(TypedDict):
    CategoryDataColors: Sequence[GeospatialCategoricalDataColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GeospatialGradientColorOutputTypeDef(TypedDict):
    StepColors: list[GeospatialGradientStepColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GeospatialGradientColorTypeDef(TypedDict):
    StepColors: Sequence[GeospatialGradientStepColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GlobalTableBorderOptionsTypeDef(TypedDict):
    UniformBorder: NotRequired[TableBorderOptionsTypeDef]
    SideSpecificBorder: NotRequired[TableSideBorderOptionsTypeDef]


class ConditionalFormattingGradientColorOutputTypeDef(TypedDict):
    Expression: str
    Color: GradientColorOutputTypeDef


class ConditionalFormattingGradientColorTypeDef(TypedDict):
    Expression: str
    Color: GradientColorTypeDef


class DefaultGridLayoutConfigurationTypeDef(TypedDict):
    CanvasSizeOptions: GridLayoutCanvasSizeOptionsTypeDef


class GridLayoutConfigurationOutputTypeDef(TypedDict):
    Elements: list[GridLayoutElementTypeDef]
    CanvasSizeOptions: NotRequired[GridLayoutCanvasSizeOptionsTypeDef]


class GridLayoutConfigurationTypeDef(TypedDict):
    Elements: Sequence[GridLayoutElementTypeDef]
    CanvasSizeOptions: NotRequired[GridLayoutCanvasSizeOptionsTypeDef]


class ImageSetConfigurationTypeDef(TypedDict):
    Original: ImageConfigurationTypeDef


class ImageSetTypeDef(TypedDict):
    Original: ImageTypeDef
    Height64: NotRequired[ImageTypeDef]
    Height32: NotRequired[ImageTypeDef]


class RefreshConfigurationTypeDef(TypedDict):
    IncrementalRefresh: IncrementalRefreshTypeDef


class DescribeIngestionResponseTypeDef(TypedDict):
    Ingestion: IngestionTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListIngestionsResponseTypeDef(TypedDict):
    Ingestions: list[IngestionTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class IntegerDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[IntegerDatasetParameterDefaultValuesUnionTypeDef]


class LogicalTableSourceTypeDef(TypedDict):
    JoinInstruction: NotRequired[JoinInstructionTypeDef]
    PhysicalTableId: NotRequired[str]
    DataSetArn: NotRequired[str]


JoinOperationOutputTypeDef = TypedDict(
    "JoinOperationOutputTypeDef",
    {
        "Alias": str,
        "LeftOperand": TransformOperationSourceOutputTypeDef,
        "RightOperand": TransformOperationSourceOutputTypeDef,
        "Type": JoinOperationTypeType,
        "OnClause": str,
        "LeftOperandProperties": NotRequired[JoinOperandPropertiesOutputTypeDef],
        "RightOperandProperties": NotRequired[JoinOperandPropertiesOutputTypeDef],
    },
)
JoinOperationTypeDef = TypedDict(
    "JoinOperationTypeDef",
    {
        "Alias": str,
        "LeftOperand": TransformOperationSourceTypeDef,
        "RightOperand": TransformOperationSourceTypeDef,
        "Type": JoinOperationTypeType,
        "OnClause": str,
        "LeftOperandProperties": NotRequired[JoinOperandPropertiesTypeDef],
        "RightOperandProperties": NotRequired[JoinOperandPropertiesTypeDef],
    },
)
LinkSharingConfigurationUnionTypeDef = Union[
    LinkSharingConfigurationTypeDef, LinkSharingConfigurationOutputTypeDef
]


class CreateFolderRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Name: NotRequired[str]
    FolderType: NotRequired[FolderTypeType]
    ParentFolderArn: NotRequired[str]
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SharingModel: NotRequired[SharingModelType]


class UpdateActionConnectorPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    ActionConnectorId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateAnalysisPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateDashboardPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    GrantLinkPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokeLinkPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateDataSetPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateDataSourcePermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateFolderPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateTemplatePermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateThemePermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class UpdateTopicPermissionsRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class SheetStyleTypeDef(TypedDict):
    Tile: NotRequired[TileStyleTypeDef]
    TileLayout: NotRequired[TileLayoutStyleTypeDef]
    Background: NotRequired[SheetBackgroundStyleTypeDef]


class TopicNamedEntityOutputTypeDef(TypedDict):
    EntityName: str
    EntityDescription: NotRequired[str]
    EntitySynonyms: NotRequired[list[str]]
    SemanticEntityType: NotRequired[SemanticEntityTypeOutputTypeDef]
    Definition: NotRequired[list[NamedEntityDefinitionOutputTypeDef]]


class TopicNamedEntityTypeDef(TypedDict):
    EntityName: str
    EntityDescription: NotRequired[str]
    EntitySynonyms: NotRequired[Sequence[str]]
    SemanticEntityType: NotRequired[SemanticEntityTypeTypeDef]
    Definition: NotRequired[Sequence[NamedEntityDefinitionTypeDef]]


class DescribeNamespaceResponseTypeDef(TypedDict):
    Namespace: NamespaceInfoV2TypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListNamespacesResponseTypeDef(TypedDict):
    Namespaces: list[NamespaceInfoV2TypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListVPCConnectionsResponseTypeDef(TypedDict):
    VPCConnectionSummaries: list[VPCConnectionSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeVPCConnectionResponseTypeDef(TypedDict):
    VPCConnection: VPCConnectionTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CurrencyDisplayFormatConfigurationTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    SeparatorConfiguration: NotRequired[NumericSeparatorConfigurationTypeDef]
    Symbol: NotRequired[str]
    DecimalPlacesConfiguration: NotRequired[DecimalPlacesConfigurationTypeDef]
    NumberScale: NotRequired[NumberScaleType]
    NegativeValueConfiguration: NotRequired[NegativeValueConfigurationTypeDef]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]


class NumberDisplayFormatConfigurationTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    SeparatorConfiguration: NotRequired[NumericSeparatorConfigurationTypeDef]
    DecimalPlacesConfiguration: NotRequired[DecimalPlacesConfigurationTypeDef]
    NumberScale: NotRequired[NumberScaleType]
    NegativeValueConfiguration: NotRequired[NegativeValueConfigurationTypeDef]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]


class PercentageDisplayFormatConfigurationTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    SeparatorConfiguration: NotRequired[NumericSeparatorConfigurationTypeDef]
    DecimalPlacesConfiguration: NotRequired[DecimalPlacesConfigurationTypeDef]
    NegativeValueConfiguration: NotRequired[NegativeValueConfigurationTypeDef]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]


class AggregationFunctionTypeDef(TypedDict):
    NumericalAggregationFunction: NotRequired[NumericalAggregationFunctionTypeDef]
    CategoricalAggregationFunction: NotRequired[CategoricalAggregationFunctionType]
    DateAggregationFunction: NotRequired[DateAggregationFunctionType]
    AttributeAggregationFunction: NotRequired[AttributeAggregationFunctionTypeDef]


class ScrollBarOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    VisibleRange: NotRequired[VisibleRangeOptionsTypeDef]


PerformanceConfigurationUnionTypeDef = Union[
    PerformanceConfigurationTypeDef, PerformanceConfigurationOutputTypeDef
]


class UpdateFlowPermissionsInputTypeDef(TypedDict):
    AwsAccountId: str
    FlowId: str
    GrantPermissions: NotRequired[Sequence[PermissionUnionTypeDef]]
    RevokePermissions: NotRequired[Sequence[PermissionUnionTypeDef]]


class TopicDateRangeFilterTypeDef(TypedDict):
    Inclusive: NotRequired[bool]
    Constant: NotRequired[TopicRangeFilterConstantTypeDef]


class TopicNumericRangeFilterTypeDef(TypedDict):
    Inclusive: NotRequired[bool]
    Constant: NotRequired[TopicRangeFilterConstantTypeDef]
    Aggregation: NotRequired[NamedFilterAggTypeType]


class ReadAuthorizationCodeGrantMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    RedirectUrl: str
    ReadAuthorizationCodeGrantCredentialsDetails: NotRequired[
        ReadAuthorizationCodeGrantCredentialsDetailsTypeDef
    ]
    AuthorizationCodeGrantCredentialsSource: NotRequired[Literal["PLAIN_CREDENTIALS"]]


class ReadClientCredentialsGrantMetadataTypeDef(TypedDict):
    BaseEndpoint: str
    ReadClientCredentialsDetails: NotRequired[ReadClientCredentialsDetailsTypeDef]
    ClientCredentialsSource: NotRequired[Literal["PLAIN_CREDENTIALS"]]


class RedshiftParametersTypeDef(TypedDict):
    Database: str
    Host: NotRequired[str]
    Port: NotRequired[int]
    ClusterId: NotRequired[str]
    IAMParameters: NotRequired[RedshiftIAMParametersUnionTypeDef]
    IdentityCenterConfiguration: NotRequired[IdentityCenterConfigurationTypeDef]


class RefreshScheduleOutputTypeDef(TypedDict):
    ScheduleId: str
    ScheduleFrequency: RefreshFrequencyTypeDef
    RefreshType: IngestionTypeType
    StartAfterDateTime: NotRequired[datetime]
    Arn: NotRequired[str]


class RefreshScheduleTypeDef(TypedDict):
    ScheduleId: str
    ScheduleFrequency: RefreshFrequencyTypeDef
    RefreshType: IngestionTypeType
    StartAfterDateTime: NotRequired[TimestampTypeDef]
    Arn: NotRequired[str]


class RowLevelPermissionConfigurationOutputTypeDef(TypedDict):
    TagConfiguration: NotRequired[RowLevelPermissionTagConfigurationOutputTypeDef]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]


class RowLevelPermissionConfigurationTypeDef(TypedDict):
    TagConfiguration: NotRequired[RowLevelPermissionTagConfigurationTypeDef]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]


RowLevelPermissionTagConfigurationUnionTypeDef = Union[
    RowLevelPermissionTagConfigurationTypeDef, RowLevelPermissionTagConfigurationOutputTypeDef
]


class SnapshotDestinationConfigurationOutputTypeDef(TypedDict):
    S3Destinations: NotRequired[list[SnapshotS3DestinationConfigurationTypeDef]]


class SnapshotDestinationConfigurationTypeDef(TypedDict):
    S3Destinations: NotRequired[Sequence[SnapshotS3DestinationConfigurationTypeDef]]


class SnapshotJobS3ResultTypeDef(TypedDict):
    S3DestinationConfiguration: NotRequired[SnapshotS3DestinationConfigurationTypeDef]
    S3Uri: NotRequired[str]
    ErrorInfo: NotRequired[list[SnapshotJobResultErrorInfoTypeDef]]


S3SourceUnionTypeDef = Union[S3SourceTypeDef, S3SourceOutputTypeDef]


class PhysicalTableOutputTypeDef(TypedDict):
    RelationalTable: NotRequired[RelationalTableOutputTypeDef]
    CustomSql: NotRequired[CustomSqlOutputTypeDef]
    S3Source: NotRequired[S3SourceOutputTypeDef]
    SaaSTable: NotRequired[SaaSTableOutputTypeDef]


SaaSTableUnionTypeDef = Union[SaaSTableTypeDef, SaaSTableOutputTypeDef]


class SectionBasedLayoutCanvasSizeOptionsTypeDef(TypedDict):
    PaperCanvasSizeOptions: NotRequired[SectionBasedLayoutPaperCanvasSizeOptionsTypeDef]


class FilterScopeConfigurationOutputTypeDef(TypedDict):
    SelectedSheets: NotRequired[SelectedSheetsFilterScopeConfigurationOutputTypeDef]
    AllSheets: NotRequired[dict[str, Any]]


class FilterScopeConfigurationTypeDef(TypedDict):
    SelectedSheets: NotRequired[SelectedSheetsFilterScopeConfigurationTypeDef]
    AllSheets: NotRequired[Mapping[str, Any]]


class FreeFormLayoutElementOutputTypeDef(TypedDict):
    ElementId: str
    ElementType: LayoutElementTypeType
    XAxisLocation: str
    YAxisLocation: str
    Width: str
    Height: str
    Visibility: NotRequired[VisibilityType]
    RenderingRules: NotRequired[list[SheetElementRenderingRuleTypeDef]]
    BorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    SelectedBorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    BackgroundStyle: NotRequired[FreeFormLayoutElementBackgroundStyleTypeDef]
    LoadingAnimation: NotRequired[LoadingAnimationTypeDef]
    BorderRadius: NotRequired[str]
    Padding: NotRequired[str]


class FreeFormLayoutElementTypeDef(TypedDict):
    ElementId: str
    ElementType: LayoutElementTypeType
    XAxisLocation: str
    YAxisLocation: str
    Width: str
    Height: str
    Visibility: NotRequired[VisibilityType]
    RenderingRules: NotRequired[Sequence[SheetElementRenderingRuleTypeDef]]
    BorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    SelectedBorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    BackgroundStyle: NotRequired[FreeFormLayoutElementBackgroundStyleTypeDef]
    LoadingAnimation: NotRequired[LoadingAnimationTypeDef]
    BorderRadius: NotRequired[str]
    Padding: NotRequired[str]


TopicTemplateUnionTypeDef = Union[TopicTemplateTypeDef, TopicTemplateOutputTypeDef]


class SnapshotFileGroupOutputTypeDef(TypedDict):
    Files: NotRequired[list[SnapshotFileOutputTypeDef]]


class SnapshotFileGroupTypeDef(TypedDict):
    Files: NotRequired[Sequence[SnapshotFileTypeDef]]


class ImageStaticFileTypeDef(TypedDict):
    StaticFileId: str
    Source: NotRequired[StaticFileSourceTypeDef]


class SpatialStaticFileTypeDef(TypedDict):
    StaticFileId: str
    Source: NotRequired[StaticFileSourceTypeDef]


class DatasetParameterOutputTypeDef(TypedDict):
    StringDatasetParameter: NotRequired[StringDatasetParameterOutputTypeDef]
    DecimalDatasetParameter: NotRequired[DecimalDatasetParameterOutputTypeDef]
    IntegerDatasetParameter: NotRequired[IntegerDatasetParameterOutputTypeDef]
    DateTimeDatasetParameter: NotRequired[DateTimeDatasetParameterOutputTypeDef]


class StringDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[StringDatasetParameterDefaultValuesUnionTypeDef]


class SheetTextBoxTypeDef(TypedDict):
    SheetTextBoxId: str
    Content: NotRequired[str]
    Interactions: NotRequired[TextBoxInteractionOptionsTypeDef]


class AssetOptionsOutputTypeDef(TypedDict):
    Timezone: NotRequired[str]
    WeekStart: NotRequired[DayOfTheWeekType]
    QBusinessInsightsStatus: NotRequired[QBusinessInsightsStatusType]
    ExcludedDataSetArns: NotRequired[list[str]]
    CustomActionDefaults: NotRequired[VisualCustomActionDefaultsTypeDef]


class AssetOptionsTypeDef(TypedDict):
    Timezone: NotRequired[str]
    WeekStart: NotRequired[DayOfTheWeekType]
    QBusinessInsightsStatus: NotRequired[QBusinessInsightsStatusType]
    ExcludedDataSetArns: NotRequired[Sequence[str]]
    CustomActionDefaults: NotRequired[VisualCustomActionDefaultsTypeDef]


class FilterCrossSheetControlOutputTypeDef(TypedDict):
    FilterControlId: str
    SourceFilterId: str
    CascadingControlConfiguration: NotRequired[CascadingControlConfigurationOutputTypeDef]


class FilterCrossSheetControlTypeDef(TypedDict):
    FilterControlId: str
    SourceFilterId: str
    CascadingControlConfiguration: NotRequired[CascadingControlConfigurationTypeDef]


class DateTimeParameterDeclarationOutputTypeDef(TypedDict):
    Name: str
    DefaultValues: NotRequired[DateTimeDefaultValuesOutputTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    ValueWhenUnset: NotRequired[DateTimeValueWhenUnsetConfigurationOutputTypeDef]
    MappedDataSetParameters: NotRequired[list[MappedDataSetParameterTypeDef]]


class DateTimeParameterDeclarationTypeDef(TypedDict):
    Name: str
    DefaultValues: NotRequired[DateTimeDefaultValuesTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    ValueWhenUnset: NotRequired[DateTimeValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class DecimalParameterDeclarationOutputTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[DecimalDefaultValuesOutputTypeDef]
    ValueWhenUnset: NotRequired[DecimalValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[list[MappedDataSetParameterTypeDef]]


class DecimalParameterDeclarationTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[DecimalDefaultValuesTypeDef]
    ValueWhenUnset: NotRequired[DecimalValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class IntegerParameterDeclarationOutputTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[IntegerDefaultValuesOutputTypeDef]
    ValueWhenUnset: NotRequired[IntegerValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[list[MappedDataSetParameterTypeDef]]


class IntegerParameterDeclarationTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[IntegerDefaultValuesTypeDef]
    ValueWhenUnset: NotRequired[IntegerValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class StringParameterDeclarationOutputTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[StringDefaultValuesOutputTypeDef]
    ValueWhenUnset: NotRequired[StringValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[list[MappedDataSetParameterTypeDef]]


class StringParameterDeclarationTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[StringDefaultValuesTypeDef]
    ValueWhenUnset: NotRequired[StringValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class DateTimeHierarchyOutputTypeDef(TypedDict):
    HierarchyId: str
    DrillDownFilters: NotRequired[list[DrillDownFilterOutputTypeDef]]


class ExplicitHierarchyOutputTypeDef(TypedDict):
    HierarchyId: str
    Columns: list[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[list[DrillDownFilterOutputTypeDef]]


class PredefinedHierarchyOutputTypeDef(TypedDict):
    HierarchyId: str
    Columns: list[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[list[DrillDownFilterOutputTypeDef]]


class RegisteredUserDashboardEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardId: str
    FeatureConfigurations: NotRequired[RegisteredUserDashboardFeatureConfigurationsTypeDef]


class RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef(TypedDict):
    InitialPath: NotRequired[str]
    FeatureConfigurations: NotRequired[RegisteredUserConsoleFeatureConfigurationsTypeDef]


class AnonymousUserEmbeddingExperienceConfigurationTypeDef(TypedDict):
    Dashboard: NotRequired[AnonymousUserDashboardEmbeddingConfigurationTypeDef]
    DashboardVisual: NotRequired[AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef]
    QSearchBar: NotRequired[AnonymousUserQSearchBarEmbeddingConfigurationTypeDef]
    GenerativeQnA: NotRequired[AnonymousUserGenerativeQnAEmbeddingConfigurationTypeDef]


class StartAssetBundleExportJobRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleExportJobId: str
    ResourceArns: Sequence[str]
    ExportFormat: AssetBundleExportFormatType
    IncludeAllDependencies: NotRequired[bool]
    CloudFormationOverridePropertyConfiguration: NotRequired[
        AssetBundleCloudFormationOverridePropertyConfigurationUnionTypeDef
    ]
    IncludePermissions: NotRequired[bool]
    IncludeTags: NotRequired[bool]
    ValidationStrategy: NotRequired[AssetBundleExportJobValidationStrategyTypeDef]
    IncludeFolderMemberships: NotRequired[bool]
    IncludeFolderMembers: NotRequired[IncludeFolderMembersType]


class AssetBundleImportJobOverridePermissionsOutputTypeDef(TypedDict):
    DataSources: NotRequired[list[AssetBundleImportJobDataSourceOverridePermissionsOutputTypeDef]]
    DataSets: NotRequired[list[AssetBundleImportJobDataSetOverridePermissionsOutputTypeDef]]
    Themes: NotRequired[list[AssetBundleImportJobThemeOverridePermissionsOutputTypeDef]]
    Analyses: NotRequired[list[AssetBundleImportJobAnalysisOverridePermissionsOutputTypeDef]]
    Dashboards: NotRequired[list[AssetBundleImportJobDashboardOverridePermissionsOutputTypeDef]]
    Folders: NotRequired[list[AssetBundleImportJobFolderOverridePermissionsOutputTypeDef]]


class AssetBundleImportJobOverridePermissionsTypeDef(TypedDict):
    DataSources: NotRequired[Sequence[AssetBundleImportJobDataSourceOverridePermissionsTypeDef]]
    DataSets: NotRequired[Sequence[AssetBundleImportJobDataSetOverridePermissionsTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleImportJobThemeOverridePermissionsTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleImportJobAnalysisOverridePermissionsTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleImportJobDashboardOverridePermissionsTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleImportJobFolderOverridePermissionsTypeDef]]


AssetBundleImportJobOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobOverrideTagsTypeDef, AssetBundleImportJobOverrideTagsOutputTypeDef
]


class DataSourceParametersOutputTypeDef(TypedDict):
    AmazonElasticsearchParameters: NotRequired[AmazonElasticsearchParametersTypeDef]
    AthenaParameters: NotRequired[AthenaParametersTypeDef]
    AuroraParameters: NotRequired[AuroraParametersTypeDef]
    AuroraPostgreSqlParameters: NotRequired[AuroraPostgreSqlParametersTypeDef]
    AwsIotAnalyticsParameters: NotRequired[AwsIotAnalyticsParametersTypeDef]
    JiraParameters: NotRequired[JiraParametersTypeDef]
    MariaDbParameters: NotRequired[MariaDbParametersTypeDef]
    MySqlParameters: NotRequired[MySqlParametersTypeDef]
    OracleParameters: NotRequired[OracleParametersTypeDef]
    PostgreSqlParameters: NotRequired[PostgreSqlParametersTypeDef]
    PrestoParameters: NotRequired[PrestoParametersTypeDef]
    RdsParameters: NotRequired[RdsParametersTypeDef]
    RedshiftParameters: NotRequired[RedshiftParametersOutputTypeDef]
    S3Parameters: NotRequired[S3ParametersTypeDef]
    S3KnowledgeBaseParameters: NotRequired[S3KnowledgeBaseParametersTypeDef]
    ServiceNowParameters: NotRequired[ServiceNowParametersTypeDef]
    SnowflakeParameters: NotRequired[SnowflakeParametersTypeDef]
    SparkParameters: NotRequired[SparkParametersTypeDef]
    SqlServerParameters: NotRequired[SqlServerParametersTypeDef]
    TeradataParameters: NotRequired[TeradataParametersTypeDef]
    TwitterParameters: NotRequired[TwitterParametersTypeDef]
    AmazonOpenSearchParameters: NotRequired[AmazonOpenSearchParametersTypeDef]
    ExasolParameters: NotRequired[ExasolParametersTypeDef]
    DatabricksParameters: NotRequired[DatabricksParametersTypeDef]
    StarburstParameters: NotRequired[StarburstParametersTypeDef]
    TrinoParameters: NotRequired[TrinoParametersTypeDef]
    BigQueryParameters: NotRequired[BigQueryParametersTypeDef]
    ImpalaParameters: NotRequired[ImpalaParametersTypeDef]
    CustomConnectionParameters: NotRequired[CustomConnectionParametersTypeDef]
    WebCrawlerParameters: NotRequired[WebCrawlerParametersTypeDef]
    ConfluenceParameters: NotRequired[ConfluenceParametersTypeDef]
    QBusinessParameters: NotRequired[QBusinessParametersTypeDef]


class DestinationParameterValueConfigurationTypeDef(TypedDict):
    CustomValuesConfiguration: NotRequired[CustomValuesConfigurationTypeDef]
    SelectAllValueOptions: NotRequired[Literal["ALL_VALUES"]]
    SourceParameterName: NotRequired[str]
    SourceField: NotRequired[str]
    SourceColumn: NotRequired[ColumnIdentifierTypeDef]


class DataSetDateComparisonFilterConditionTypeDef(TypedDict):
    Operator: DataSetDateComparisonFilterOperatorType
    Value: NotRequired[DataSetDateFilterValueUnionTypeDef]


class DataSetDateRangeFilterConditionTypeDef(TypedDict):
    RangeMinimum: NotRequired[DataSetDateFilterValueUnionTypeDef]
    RangeMaximum: NotRequired[DataSetDateFilterValueUnionTypeDef]
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]


class DateTimeDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultValues: NotRequired[DateTimeDatasetParameterDefaultValuesUnionTypeDef]


ParametersUnionTypeDef = Union[ParametersTypeDef, ParametersOutputTypeDef]


class OverrideDatasetParameterOperationTypeDef(TypedDict):
    ParameterName: str
    NewParameterName: NotRequired[str]
    NewDefaultValues: NotRequired[NewDefaultValuesUnionTypeDef]


class DateTimeHierarchyTypeDef(TypedDict):
    HierarchyId: str
    DrillDownFilters: NotRequired[Sequence[DrillDownFilterTypeDef]]


class ExplicitHierarchyTypeDef(TypedDict):
    HierarchyId: str
    Columns: Sequence[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[Sequence[DrillDownFilterTypeDef]]


class PredefinedHierarchyTypeDef(TypedDict):
    HierarchyId: str
    Columns: Sequence[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[Sequence[DrillDownFilterTypeDef]]


class CreateTopicRefreshScheduleRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetArn: str
    RefreshSchedule: TopicRefreshScheduleUnionTypeDef
    DatasetName: NotRequired[str]


class UpdateTopicRefreshScheduleRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetId: str
    RefreshSchedule: TopicRefreshScheduleUnionTypeDef


class ForecastConfigurationTypeDef(TypedDict):
    ForecastProperties: NotRequired[TimeBasedForecastPropertiesTypeDef]
    Scenario: NotRequired[ForecastScenarioTypeDef]


class AxisDataOptionsOutputTypeDef(TypedDict):
    NumericAxisOptions: NotRequired[NumericAxisOptionsOutputTypeDef]
    DateAxisOptions: NotRequired[DateAxisOptionsTypeDef]


class AxisDataOptionsTypeDef(TypedDict):
    NumericAxisOptions: NotRequired[NumericAxisOptionsTypeDef]
    DateAxisOptions: NotRequired[DateAxisOptionsTypeDef]


class BarSeriesItemTypeDef(TypedDict):
    FieldBarSeriesItem: NotRequired[FieldBarSeriesItemTypeDef]
    DataFieldBarSeriesItem: NotRequired[DataFieldBarSeriesItemTypeDef]


class ApplicationThemeTypeDef(TypedDict):
    BrandColorPalette: NotRequired[BrandColorPaletteTypeDef]
    ContextualAccentPalette: NotRequired[ContextualAccentPaletteTypeDef]
    BrandElementStyle: NotRequired[BrandElementStyleTypeDef]


class AuthenticationMetadataTypeDef(TypedDict):
    AuthorizationCodeGrantMetadata: NotRequired[AuthorizationCodeGrantMetadataTypeDef]
    ClientCredentialsGrantMetadata: NotRequired[ClientCredentialsGrantMetadataTypeDef]
    BasicAuthConnectionMetadata: NotRequired[BasicAuthConnectionMetadataTypeDef]
    ApiKeyConnectionMetadata: NotRequired[APIKeyConnectionMetadataTypeDef]
    NoneConnectionMetadata: NotRequired[NoneConnectionMetadataTypeDef]
    IamConnectionMetadata: NotRequired[IAMConnectionMetadataTypeDef]


class TopicIRFilterOptionTypeDef(TypedDict):
    FilterType: NotRequired[TopicIRFilterTypeType]
    FilterClass: NotRequired[FilterClassType]
    OperandField: NotRequired[IdentifierTypeDef]
    Function: NotRequired[TopicIRFilterFunctionType]
    Constant: NotRequired[TopicConstantValueUnionTypeDef]
    Inverse: NotRequired[bool]
    NullFilter: NotRequired[NullFilterOptionType]
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[Mapping[str, str]]
    AggregationPartitionBy: NotRequired[Sequence[AggregationPartitionByTypeDef]]
    Range: NotRequired[TopicConstantValueUnionTypeDef]
    Inclusive: NotRequired[bool]
    TimeGranularity: NotRequired[TimeGranularityType]
    LastNextOffset: NotRequired[TopicConstantValueUnionTypeDef]
    AggMetrics: NotRequired[Sequence[FilterAggMetricsTypeDef]]
    TopBottomLimit: NotRequired[TopicConstantValueUnionTypeDef]
    SortDirection: NotRequired[TopicSortDirectionType]
    Anchor: NotRequired[AnchorTypeDef]


TagColumnOperationUnionTypeDef = Union[TagColumnOperationTypeDef, TagColumnOperationOutputTypeDef]


class ComboSeriesItemTypeDef(TypedDict):
    FieldComboSeriesItem: NotRequired[FieldComboSeriesItemTypeDef]
    DataFieldComboSeriesItem: NotRequired[DataFieldComboSeriesItemTypeDef]


class SeriesItemTypeDef(TypedDict):
    FieldSeriesItem: NotRequired[FieldSeriesItemTypeDef]
    DataFieldSeriesItem: NotRequired[DataFieldSeriesItemTypeDef]


class SetParameterValueConfigurationOutputTypeDef(TypedDict):
    DestinationParameterName: str
    Value: DestinationParameterValueConfigurationOutputTypeDef


class VisualPaletteOutputTypeDef(TypedDict):
    ChartColor: NotRequired[str]
    ColorMap: NotRequired[list[DataPathColorTypeDef]]


class VisualPaletteTypeDef(TypedDict):
    ChartColor: NotRequired[str]
    ColorMap: NotRequired[Sequence[DataPathColorTypeDef]]


class PivotTableFieldCollapseStateOptionOutputTypeDef(TypedDict):
    Target: PivotTableFieldCollapseStateTargetOutputTypeDef
    State: NotRequired[PivotTableFieldCollapseStateType]


class PivotTableFieldCollapseStateOptionTypeDef(TypedDict):
    Target: PivotTableFieldCollapseStateTargetTypeDef
    State: NotRequired[PivotTableFieldCollapseStateType]


class AggregateOperationOutputTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceOutputTypeDef
    Aggregations: list[AggregationTypeDef]
    GroupByColumnNames: NotRequired[list[str]]


class AggregateOperationTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceTypeDef
    Aggregations: Sequence[AggregationTypeDef]
    GroupByColumnNames: NotRequired[Sequence[str]]


class PivotOperationOutputTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceOutputTypeDef
    ValueColumnConfiguration: ValueColumnConfigurationTypeDef
    PivotConfiguration: PivotConfigurationOutputTypeDef
    GroupByColumnNames: NotRequired[list[str]]


class PivotOperationTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceTypeDef
    ValueColumnConfiguration: ValueColumnConfigurationTypeDef
    PivotConfiguration: PivotConfigurationTypeDef
    GroupByColumnNames: NotRequired[Sequence[str]]


class CreateColumnsOperationTypeDef(TypedDict):
    Columns: Sequence[CalculatedColumnTypeDef]
    Alias: NotRequired[str]
    Source: NotRequired[TransformOperationSourceUnionTypeDef]


class ProjectOperationTypeDef(TypedDict):
    ProjectedColumns: Sequence[str]
    Alias: NotRequired[str]
    Source: NotRequired[TransformOperationSourceUnionTypeDef]


class FilterOperationOutputTypeDef(TypedDict):
    ConditionExpression: NotRequired[str]
    StringFilterCondition: NotRequired[DataSetStringFilterConditionOutputTypeDef]
    NumericFilterCondition: NotRequired[DataSetNumericFilterConditionTypeDef]
    DateFilterCondition: NotRequired[DataSetDateFilterConditionOutputTypeDef]


DataSetStringListFilterConditionUnionTypeDef = Union[
    DataSetStringListFilterConditionTypeDef, DataSetStringListFilterConditionOutputTypeDef
]
DecimalDatasetParameterUnionTypeDef = Union[
    DecimalDatasetParameterTypeDef, DecimalDatasetParameterOutputTypeDef
]


class TopicCalculatedFieldOutputTypeDef(TypedDict):
    CalculatedFieldName: str
    Expression: str
    CalculatedFieldDescription: NotRequired[str]
    CalculatedFieldSynonyms: NotRequired[list[str]]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    Aggregation: NotRequired[DefaultAggregationType]
    ComparativeOrder: NotRequired[ComparativeOrderOutputTypeDef]
    SemanticType: NotRequired[SemanticTypeOutputTypeDef]
    AllowedAggregations: NotRequired[list[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[list[AuthorSpecifiedAggregationType]]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[list[CellValueSynonymOutputTypeDef]]
    NonAdditive: NotRequired[bool]


class TopicCalculatedFieldTypeDef(TypedDict):
    CalculatedFieldName: str
    Expression: str
    CalculatedFieldDescription: NotRequired[str]
    CalculatedFieldSynonyms: NotRequired[Sequence[str]]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    Aggregation: NotRequired[DefaultAggregationType]
    ComparativeOrder: NotRequired[ComparativeOrderTypeDef]
    SemanticType: NotRequired[SemanticTypeTypeDef]
    AllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[Sequence[CellValueSynonymTypeDef]]
    NonAdditive: NotRequired[bool]


class TopicColumnOutputTypeDef(TypedDict):
    ColumnName: str
    ColumnFriendlyName: NotRequired[str]
    ColumnDescription: NotRequired[str]
    ColumnSynonyms: NotRequired[list[str]]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    Aggregation: NotRequired[DefaultAggregationType]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ComparativeOrder: NotRequired[ComparativeOrderOutputTypeDef]
    SemanticType: NotRequired[SemanticTypeOutputTypeDef]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    AllowedAggregations: NotRequired[list[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[list[AuthorSpecifiedAggregationType]]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[list[CellValueSynonymOutputTypeDef]]
    NonAdditive: NotRequired[bool]


class TopicColumnTypeDef(TypedDict):
    ColumnName: str
    ColumnFriendlyName: NotRequired[str]
    ColumnDescription: NotRequired[str]
    ColumnSynonyms: NotRequired[Sequence[str]]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    Aggregation: NotRequired[DefaultAggregationType]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ComparativeOrder: NotRequired[ComparativeOrderTypeDef]
    SemanticType: NotRequired[SemanticTypeTypeDef]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    AllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[Sequence[CellValueSynonymTypeDef]]
    NonAdditive: NotRequired[bool]


TopicIRMetricUnionTypeDef = Union[TopicIRMetricTypeDef, TopicIRMetricOutputTypeDef]


class ContributionAnalysisTimeRangesOutputTypeDef(TypedDict):
    StartRange: NotRequired[TopicIRFilterOptionOutputTypeDef]
    EndRange: NotRequired[TopicIRFilterOptionOutputTypeDef]


class ChartAxisLabelOptionsOutputTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    SortIconVisibility: NotRequired[VisibilityType]
    AxisLabelOptions: NotRequired[list[AxisLabelOptionsTypeDef]]


class ChartAxisLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    SortIconVisibility: NotRequired[VisibilityType]
    AxisLabelOptions: NotRequired[Sequence[AxisLabelOptionsTypeDef]]


class AxisTickLabelOptionsTypeDef(TypedDict):
    LabelOptions: NotRequired[LabelOptionsTypeDef]
    RotationAngle: NotRequired[float]


class DateTimePickerControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    DateTimeFormat: NotRequired[str]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]
    HelperTextVisibility: NotRequired[VisibilityType]
    DateIconVisibility: NotRequired[VisibilityType]


class DropDownControlDisplayOptionsTypeDef(TypedDict):
    SelectAllOptions: NotRequired[ListControlSelectAllOptionsTypeDef]
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class LegendOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Title: NotRequired[LabelOptionsTypeDef]
    Position: NotRequired[LegendPositionType]
    Width: NotRequired[str]
    Height: NotRequired[str]
    ValueFontConfiguration: NotRequired[FontConfigurationTypeDef]


class ListControlDisplayOptionsTypeDef(TypedDict):
    SearchOptions: NotRequired[ListControlSearchOptionsTypeDef]
    SelectAllOptions: NotRequired[ListControlSelectAllOptionsTypeDef]
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class RelativeDateTimeControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    DateTimeFormat: NotRequired[str]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class SliderControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class TextAreaControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    PlaceholderOptions: NotRequired[TextControlPlaceholderOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class TextFieldControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    PlaceholderOptions: NotRequired[TextControlPlaceholderOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class PanelConfigurationTypeDef(TypedDict):
    Title: NotRequired[PanelTitleOptionsTypeDef]
    BorderVisibility: NotRequired[VisibilityType]
    BorderThickness: NotRequired[str]
    BorderStyle: NotRequired[PanelBorderStyleType]
    BorderColor: NotRequired[str]
    GutterVisibility: NotRequired[VisibilityType]
    GutterSpacing: NotRequired[str]
    BackgroundVisibility: NotRequired[VisibilityType]
    BackgroundColor: NotRequired[str]


class TableFieldLinkContentConfigurationTypeDef(TypedDict):
    CustomTextContent: NotRequired[TableFieldCustomTextContentTypeDef]
    CustomIconContent: NotRequired[TableFieldCustomIconContentTypeDef]


class TypographyOutputTypeDef(TypedDict):
    FontFamilies: NotRequired[list[FontTypeDef]]
    AxisTitleFontConfiguration: NotRequired[FontConfigurationTypeDef]
    AxisLabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LegendTitleFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LegendValueFontConfiguration: NotRequired[FontConfigurationTypeDef]
    DataLabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    VisualTitleFontConfiguration: NotRequired[VisualTitleFontConfigurationTypeDef]
    VisualSubtitleFontConfiguration: NotRequired[VisualSubtitleFontConfigurationTypeDef]


class TypographyTypeDef(TypedDict):
    FontFamilies: NotRequired[Sequence[FontTypeDef]]
    AxisTitleFontConfiguration: NotRequired[FontConfigurationTypeDef]
    AxisLabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LegendTitleFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LegendValueFontConfiguration: NotRequired[FontConfigurationTypeDef]
    DataLabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    VisualTitleFontConfiguration: NotRequired[VisualTitleFontConfigurationTypeDef]
    VisualSubtitleFontConfiguration: NotRequired[VisualSubtitleFontConfigurationTypeDef]


ColumnGroupUnionTypeDef = Union[ColumnGroupTypeDef, ColumnGroupOutputTypeDef]


class GeospatialPointStyleOptionsOutputTypeDef(TypedDict):
    SelectedPointStyle: NotRequired[GeospatialSelectedPointStyleType]
    ClusterMarkerConfiguration: NotRequired[ClusterMarkerConfigurationTypeDef]
    HeatmapConfiguration: NotRequired[GeospatialHeatmapConfigurationOutputTypeDef]


class GeospatialPointStyleOptionsTypeDef(TypedDict):
    SelectedPointStyle: NotRequired[GeospatialSelectedPointStyleType]
    ClusterMarkerConfiguration: NotRequired[ClusterMarkerConfigurationTypeDef]
    HeatmapConfiguration: NotRequired[GeospatialHeatmapConfigurationTypeDef]


class GeospatialColorOutputTypeDef(TypedDict):
    Solid: NotRequired[GeospatialSolidColorTypeDef]
    Gradient: NotRequired[GeospatialGradientColorOutputTypeDef]
    Categorical: NotRequired[GeospatialCategoricalColorOutputTypeDef]


class GeospatialColorTypeDef(TypedDict):
    Solid: NotRequired[GeospatialSolidColorTypeDef]
    Gradient: NotRequired[GeospatialGradientColorTypeDef]
    Categorical: NotRequired[GeospatialCategoricalColorTypeDef]


class TableCellStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    TextWrap: NotRequired[TextWrapType]
    HorizontalTextAlignment: NotRequired[HorizontalTextAlignmentType]
    VerticalTextAlignment: NotRequired[VerticalTextAlignmentType]
    BackgroundColor: NotRequired[str]
    Height: NotRequired[int]
    Border: NotRequired[GlobalTableBorderOptionsTypeDef]


class ConditionalFormattingColorOutputTypeDef(TypedDict):
    Solid: NotRequired[ConditionalFormattingSolidColorTypeDef]
    Gradient: NotRequired[ConditionalFormattingGradientColorOutputTypeDef]


class ConditionalFormattingColorTypeDef(TypedDict):
    Solid: NotRequired[ConditionalFormattingSolidColorTypeDef]
    Gradient: NotRequired[ConditionalFormattingGradientColorTypeDef]


class DefaultInteractiveLayoutConfigurationTypeDef(TypedDict):
    Grid: NotRequired[DefaultGridLayoutConfigurationTypeDef]
    FreeForm: NotRequired[DefaultFreeFormLayoutConfigurationTypeDef]


class SheetControlLayoutConfigurationOutputTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationOutputTypeDef]


class SheetControlLayoutConfigurationTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationTypeDef]


class LogoSetConfigurationTypeDef(TypedDict):
    Primary: ImageSetConfigurationTypeDef
    Favicon: NotRequired[ImageSetConfigurationTypeDef]


class LogoSetTypeDef(TypedDict):
    Primary: ImageSetTypeDef
    Favicon: NotRequired[ImageSetTypeDef]


class DataSetRefreshPropertiesTypeDef(TypedDict):
    RefreshConfiguration: NotRequired[RefreshConfigurationTypeDef]
    FailureConfiguration: NotRequired[RefreshFailureConfigurationTypeDef]


IntegerDatasetParameterUnionTypeDef = Union[
    IntegerDatasetParameterTypeDef, IntegerDatasetParameterOutputTypeDef
]


class ComparisonFormatConfigurationTypeDef(TypedDict):
    NumberDisplayFormatConfiguration: NotRequired[NumberDisplayFormatConfigurationTypeDef]
    PercentageDisplayFormatConfiguration: NotRequired[PercentageDisplayFormatConfigurationTypeDef]


class NumericFormatConfigurationTypeDef(TypedDict):
    NumberDisplayFormatConfiguration: NotRequired[NumberDisplayFormatConfigurationTypeDef]
    CurrencyDisplayFormatConfiguration: NotRequired[CurrencyDisplayFormatConfigurationTypeDef]
    PercentageDisplayFormatConfiguration: NotRequired[PercentageDisplayFormatConfigurationTypeDef]


class AggregationSortConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    SortDirection: SortDirectionType
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]


class ColumnSortTypeDef(TypedDict):
    SortBy: ColumnIdentifierTypeDef
    Direction: SortDirectionType
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]


class ColumnTooltipItemTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    Aggregation: NotRequired[AggregationFunctionTypeDef]
    TooltipTarget: NotRequired[TooltipTargetType]


class ReferenceLineDynamicDataConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Calculation: NumericalAggregationFunctionTypeDef
    MeasureAggregationFunction: NotRequired[AggregationFunctionTypeDef]


class TopicFilterOutputTypeDef(TypedDict):
    FilterName: str
    OperandFieldName: str
    FilterDescription: NotRequired[str]
    FilterClass: NotRequired[FilterClassType]
    FilterSynonyms: NotRequired[list[str]]
    FilterType: NotRequired[NamedFilterTypeType]
    CategoryFilter: NotRequired[TopicCategoryFilterOutputTypeDef]
    NumericEqualityFilter: NotRequired[TopicNumericEqualityFilterTypeDef]
    NumericRangeFilter: NotRequired[TopicNumericRangeFilterTypeDef]
    DateRangeFilter: NotRequired[TopicDateRangeFilterTypeDef]
    RelativeDateFilter: NotRequired[TopicRelativeDateFilterTypeDef]
    NullFilter: NotRequired[TopicNullFilterTypeDef]


class TopicFilterTypeDef(TypedDict):
    FilterName: str
    OperandFieldName: str
    FilterDescription: NotRequired[str]
    FilterClass: NotRequired[FilterClassType]
    FilterSynonyms: NotRequired[Sequence[str]]
    FilterType: NotRequired[NamedFilterTypeType]
    CategoryFilter: NotRequired[TopicCategoryFilterTypeDef]
    NumericEqualityFilter: NotRequired[TopicNumericEqualityFilterTypeDef]
    NumericRangeFilter: NotRequired[TopicNumericRangeFilterTypeDef]
    DateRangeFilter: NotRequired[TopicDateRangeFilterTypeDef]
    RelativeDateFilter: NotRequired[TopicRelativeDateFilterTypeDef]
    NullFilter: NotRequired[TopicNullFilterTypeDef]


class ReadAuthenticationMetadataTypeDef(TypedDict):
    AuthorizationCodeGrantMetadata: NotRequired[ReadAuthorizationCodeGrantMetadataTypeDef]
    ClientCredentialsGrantMetadata: NotRequired[ReadClientCredentialsGrantMetadataTypeDef]
    BasicAuthConnectionMetadata: NotRequired[ReadBasicAuthConnectionMetadataTypeDef]
    ApiKeyConnectionMetadata: NotRequired[ReadAPIKeyConnectionMetadataTypeDef]
    NoneConnectionMetadata: NotRequired[ReadNoneConnectionMetadataTypeDef]
    IamConnectionMetadata: NotRequired[ReadIamConnectionMetadataTypeDef]


RedshiftParametersUnionTypeDef = Union[RedshiftParametersTypeDef, RedshiftParametersOutputTypeDef]


class DescribeRefreshScheduleResponseTypeDef(TypedDict):
    RefreshSchedule: RefreshScheduleOutputTypeDef
    Status: int
    RequestId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListRefreshSchedulesResponseTypeDef(TypedDict):
    RefreshSchedules: list[RefreshScheduleOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


RefreshScheduleUnionTypeDef = Union[RefreshScheduleTypeDef, RefreshScheduleOutputTypeDef]


class SemanticTableOutputTypeDef(TypedDict):
    Alias: str
    DestinationTableId: str
    RowLevelPermissionConfiguration: NotRequired[RowLevelPermissionConfigurationOutputTypeDef]


class SemanticTableTypeDef(TypedDict):
    Alias: str
    DestinationTableId: str
    RowLevelPermissionConfiguration: NotRequired[RowLevelPermissionConfigurationTypeDef]


class SnapshotJobResultFileGroupTypeDef(TypedDict):
    Files: NotRequired[list[SnapshotFileOutputTypeDef]]
    S3Results: NotRequired[list[SnapshotJobS3ResultTypeDef]]


class PhysicalTableTypeDef(TypedDict):
    RelationalTable: NotRequired[RelationalTableUnionTypeDef]
    CustomSql: NotRequired[CustomSqlUnionTypeDef]
    S3Source: NotRequired[S3SourceUnionTypeDef]
    SaaSTable: NotRequired[SaaSTableUnionTypeDef]


class DefaultSectionBasedLayoutConfigurationTypeDef(TypedDict):
    CanvasSizeOptions: SectionBasedLayoutCanvasSizeOptionsTypeDef


class FreeFormLayoutConfigurationOutputTypeDef(TypedDict):
    Elements: list[FreeFormLayoutElementOutputTypeDef]
    CanvasSizeOptions: NotRequired[FreeFormLayoutCanvasSizeOptionsTypeDef]
    Groups: NotRequired[list[SheetLayoutGroupOutputTypeDef]]


class FreeFormSectionLayoutConfigurationOutputTypeDef(TypedDict):
    Elements: list[FreeFormLayoutElementOutputTypeDef]


class FreeFormLayoutConfigurationTypeDef(TypedDict):
    Elements: Sequence[FreeFormLayoutElementTypeDef]
    CanvasSizeOptions: NotRequired[FreeFormLayoutCanvasSizeOptionsTypeDef]
    Groups: NotRequired[Sequence[SheetLayoutGroupTypeDef]]


class FreeFormSectionLayoutConfigurationTypeDef(TypedDict):
    Elements: Sequence[FreeFormLayoutElementTypeDef]


class SnapshotConfigurationOutputTypeDef(TypedDict):
    FileGroups: list[SnapshotFileGroupOutputTypeDef]
    DestinationConfiguration: NotRequired[SnapshotDestinationConfigurationOutputTypeDef]
    Parameters: NotRequired[ParametersOutputTypeDef]


class SnapshotConfigurationTypeDef(TypedDict):
    FileGroups: Sequence[SnapshotFileGroupTypeDef]
    DestinationConfiguration: NotRequired[SnapshotDestinationConfigurationTypeDef]
    Parameters: NotRequired[ParametersTypeDef]


class StaticFileTypeDef(TypedDict):
    ImageStaticFile: NotRequired[ImageStaticFileTypeDef]
    SpatialStaticFile: NotRequired[SpatialStaticFileTypeDef]


StringDatasetParameterUnionTypeDef = Union[
    StringDatasetParameterTypeDef, StringDatasetParameterOutputTypeDef
]


class ParameterDeclarationOutputTypeDef(TypedDict):
    StringParameterDeclaration: NotRequired[StringParameterDeclarationOutputTypeDef]
    DecimalParameterDeclaration: NotRequired[DecimalParameterDeclarationOutputTypeDef]
    IntegerParameterDeclaration: NotRequired[IntegerParameterDeclarationOutputTypeDef]
    DateTimeParameterDeclaration: NotRequired[DateTimeParameterDeclarationOutputTypeDef]


class ParameterDeclarationTypeDef(TypedDict):
    StringParameterDeclaration: NotRequired[StringParameterDeclarationTypeDef]
    DecimalParameterDeclaration: NotRequired[DecimalParameterDeclarationTypeDef]
    IntegerParameterDeclaration: NotRequired[IntegerParameterDeclarationTypeDef]
    DateTimeParameterDeclaration: NotRequired[DateTimeParameterDeclarationTypeDef]


class ColumnHierarchyOutputTypeDef(TypedDict):
    ExplicitHierarchy: NotRequired[ExplicitHierarchyOutputTypeDef]
    DateTimeHierarchy: NotRequired[DateTimeHierarchyOutputTypeDef]
    PredefinedHierarchy: NotRequired[PredefinedHierarchyOutputTypeDef]


class RegisteredUserEmbeddingExperienceConfigurationTypeDef(TypedDict):
    Dashboard: NotRequired[RegisteredUserDashboardEmbeddingConfigurationTypeDef]
    QuickSightConsole: NotRequired[RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef]
    QSearchBar: NotRequired[RegisteredUserQSearchBarEmbeddingConfigurationTypeDef]
    DashboardVisual: NotRequired[RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef]
    GenerativeQnA: NotRequired[RegisteredUserGenerativeQnAEmbeddingConfigurationTypeDef]
    QuickChat: NotRequired[Mapping[str, Any]]


class GenerateEmbedUrlForAnonymousUserRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    AuthorizedResourceArns: Sequence[str]
    ExperienceConfiguration: AnonymousUserEmbeddingExperienceConfigurationTypeDef
    SessionLifetimeInMinutes: NotRequired[int]
    SessionTags: NotRequired[Sequence[SessionTagTypeDef]]
    AllowedDomains: NotRequired[Sequence[str]]


AssetBundleImportJobOverridePermissionsUnionTypeDef = Union[
    AssetBundleImportJobOverridePermissionsTypeDef,
    AssetBundleImportJobOverridePermissionsOutputTypeDef,
]


class AssetBundleImportJobDataSourceOverrideParametersOutputTypeDef(TypedDict):
    DataSourceId: str
    Name: NotRequired[str]
    DataSourceParameters: NotRequired[DataSourceParametersOutputTypeDef]
    VpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    SslProperties: NotRequired[SslPropertiesTypeDef]
    Credentials: NotRequired[AssetBundleImportJobDataSourceCredentialsTypeDef]


DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSourceId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "Status": NotRequired[ResourceStatusType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "DataSourceParameters": NotRequired[DataSourceParametersOutputTypeDef],
        "AlternateDataSourceParameters": NotRequired[list[DataSourceParametersOutputTypeDef]],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "ErrorInfo": NotRequired[DataSourceErrorInfoTypeDef],
        "SecretArn": NotRequired[str],
    },
)


class SetParameterValueConfigurationTypeDef(TypedDict):
    DestinationParameterName: str
    Value: DestinationParameterValueConfigurationTypeDef


DataSetDateComparisonFilterConditionUnionTypeDef = Union[
    DataSetDateComparisonFilterConditionTypeDef, DataSetDateComparisonFilterConditionOutputTypeDef
]
DataSetDateRangeFilterConditionUnionTypeDef = Union[
    DataSetDateRangeFilterConditionTypeDef, DataSetDateRangeFilterConditionOutputTypeDef
]
DateTimeDatasetParameterUnionTypeDef = Union[
    DateTimeDatasetParameterTypeDef, DateTimeDatasetParameterOutputTypeDef
]
OverrideDatasetParameterOperationUnionTypeDef = Union[
    OverrideDatasetParameterOperationTypeDef, OverrideDatasetParameterOperationOutputTypeDef
]


class ColumnHierarchyTypeDef(TypedDict):
    ExplicitHierarchy: NotRequired[ExplicitHierarchyTypeDef]
    DateTimeHierarchy: NotRequired[DateTimeHierarchyTypeDef]
    PredefinedHierarchy: NotRequired[PredefinedHierarchyTypeDef]


class AuthConfigTypeDef(TypedDict):
    AuthenticationType: ConnectionAuthTypeType
    AuthenticationMetadata: AuthenticationMetadataTypeDef


TopicIRFilterOptionUnionTypeDef = Union[
    TopicIRFilterOptionTypeDef, TopicIRFilterOptionOutputTypeDef
]


class CustomActionSetParametersOperationOutputTypeDef(TypedDict):
    ParameterValueConfigurations: list[SetParameterValueConfigurationOutputTypeDef]


class PivotTableFieldOptionsOutputTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[list[PivotTableFieldOptionTypeDef]]
    DataPathOptions: NotRequired[list[PivotTableDataPathOptionOutputTypeDef]]
    CollapseStateOptions: NotRequired[list[PivotTableFieldCollapseStateOptionOutputTypeDef]]


class PivotTableFieldOptionsTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[Sequence[PivotTableFieldOptionTypeDef]]
    DataPathOptions: NotRequired[Sequence[PivotTableDataPathOptionTypeDef]]
    CollapseStateOptions: NotRequired[Sequence[PivotTableFieldCollapseStateOptionTypeDef]]


CreateColumnsOperationUnionTypeDef = Union[
    CreateColumnsOperationTypeDef, CreateColumnsOperationOutputTypeDef
]
ProjectOperationUnionTypeDef = Union[ProjectOperationTypeDef, ProjectOperationOutputTypeDef]


class FiltersOperationOutputTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceOutputTypeDef
    FilterOperations: list[FilterOperationOutputTypeDef]


class TransformOperationOutputTypeDef(TypedDict):
    ProjectOperation: NotRequired[ProjectOperationOutputTypeDef]
    FilterOperation: NotRequired[FilterOperationOutputTypeDef]
    CreateColumnsOperation: NotRequired[CreateColumnsOperationOutputTypeDef]
    RenameColumnOperation: NotRequired[RenameColumnOperationTypeDef]
    CastColumnTypeOperation: NotRequired[CastColumnTypeOperationTypeDef]
    TagColumnOperation: NotRequired[TagColumnOperationOutputTypeDef]
    UntagColumnOperation: NotRequired[UntagColumnOperationOutputTypeDef]
    OverrideDatasetParameterOperation: NotRequired[OverrideDatasetParameterOperationOutputTypeDef]


class DataSetStringFilterConditionTypeDef(TypedDict):
    ColumnName: NotRequired[str]
    ComparisonFilterCondition: NotRequired[DataSetStringComparisonFilterConditionTypeDef]
    ListFilterCondition: NotRequired[DataSetStringListFilterConditionUnionTypeDef]


class TopicIRContributionAnalysisOutputTypeDef(TypedDict):
    Factors: NotRequired[list[ContributionAnalysisFactorTypeDef]]
    TimeRanges: NotRequired[ContributionAnalysisTimeRangesOutputTypeDef]
    Direction: NotRequired[ContributionAnalysisDirectionType]
    SortType: NotRequired[ContributionAnalysisSortTypeType]


class AxisDisplayOptionsOutputTypeDef(TypedDict):
    TickLabelOptions: NotRequired[AxisTickLabelOptionsTypeDef]
    AxisLineVisibility: NotRequired[VisibilityType]
    GridLineVisibility: NotRequired[VisibilityType]
    DataOptions: NotRequired[AxisDataOptionsOutputTypeDef]
    ScrollbarOptions: NotRequired[ScrollBarOptionsTypeDef]
    AxisOffset: NotRequired[str]


class AxisDisplayOptionsTypeDef(TypedDict):
    TickLabelOptions: NotRequired[AxisTickLabelOptionsTypeDef]
    AxisLineVisibility: NotRequired[VisibilityType]
    GridLineVisibility: NotRequired[VisibilityType]
    DataOptions: NotRequired[AxisDataOptionsTypeDef]
    ScrollbarOptions: NotRequired[ScrollBarOptionsTypeDef]
    AxisOffset: NotRequired[str]


DefaultDateTimePickerControlOptionsTypeDef = TypedDict(
    "DefaultDateTimePickerControlOptionsTypeDef",
    {
        "Type": NotRequired[SheetControlDateTimePickerTypeType],
        "DisplayOptions": NotRequired[DateTimePickerControlDisplayOptionsTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
FilterDateTimePickerControlTypeDef = TypedDict(
    "FilterDateTimePickerControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DateTimePickerControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlDateTimePickerTypeType],
        "CommitMode": NotRequired[CommitModeType],
    },
)


class ParameterDateTimePickerControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    DisplayOptions: NotRequired[DateTimePickerControlDisplayOptionsTypeDef]


DefaultFilterDropDownControlOptionsOutputTypeDef = TypedDict(
    "DefaultFilterDropDownControlOptionsOutputTypeDef",
    {
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
DefaultFilterDropDownControlOptionsTypeDef = TypedDict(
    "DefaultFilterDropDownControlOptionsTypeDef",
    {
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
FilterDropDownControlOutputTypeDef = TypedDict(
    "FilterDropDownControlOutputTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
FilterDropDownControlTypeDef = TypedDict(
    "FilterDropDownControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
ParameterDropDownControlOutputTypeDef = TypedDict(
    "ParameterDropDownControlOutputTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
ParameterDropDownControlTypeDef = TypedDict(
    "ParameterDropDownControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
DefaultFilterListControlOptionsOutputTypeDef = TypedDict(
    "DefaultFilterListControlOptionsOutputTypeDef",
    {
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
    },
)
DefaultFilterListControlOptionsTypeDef = TypedDict(
    "DefaultFilterListControlOptionsTypeDef",
    {
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesTypeDef],
    },
)
FilterListControlOutputTypeDef = TypedDict(
    "FilterListControlOutputTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
    },
)
FilterListControlTypeDef = TypedDict(
    "FilterListControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
    },
)
ParameterListControlOutputTypeDef = TypedDict(
    "ParameterListControlOutputTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
    },
)
ParameterListControlTypeDef = TypedDict(
    "ParameterListControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationTypeDef],
    },
)


class DefaultRelativeDateTimeControlOptionsTypeDef(TypedDict):
    DisplayOptions: NotRequired[RelativeDateTimeControlDisplayOptionsTypeDef]
    CommitMode: NotRequired[CommitModeType]


class FilterRelativeDateTimeControlTypeDef(TypedDict):
    FilterControlId: str
    Title: str
    SourceFilterId: str
    DisplayOptions: NotRequired[RelativeDateTimeControlDisplayOptionsTypeDef]
    CommitMode: NotRequired[CommitModeType]


DefaultSliderControlOptionsTypeDef = TypedDict(
    "DefaultSliderControlOptionsTypeDef",
    {
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
        "DisplayOptions": NotRequired[SliderControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlSliderTypeType],
    },
)
FilterSliderControlTypeDef = TypedDict(
    "FilterSliderControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
        "DisplayOptions": NotRequired[SliderControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlSliderTypeType],
    },
)


class ParameterSliderControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    MaximumValue: float
    MinimumValue: float
    StepSize: float
    DisplayOptions: NotRequired[SliderControlDisplayOptionsTypeDef]


class DefaultTextAreaControlOptionsTypeDef(TypedDict):
    Delimiter: NotRequired[str]
    DisplayOptions: NotRequired[TextAreaControlDisplayOptionsTypeDef]


class FilterTextAreaControlTypeDef(TypedDict):
    FilterControlId: str
    Title: str
    SourceFilterId: str
    Delimiter: NotRequired[str]
    DisplayOptions: NotRequired[TextAreaControlDisplayOptionsTypeDef]


class ParameterTextAreaControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    Delimiter: NotRequired[str]
    DisplayOptions: NotRequired[TextAreaControlDisplayOptionsTypeDef]


class DefaultTextFieldControlOptionsTypeDef(TypedDict):
    DisplayOptions: NotRequired[TextFieldControlDisplayOptionsTypeDef]


class FilterTextFieldControlTypeDef(TypedDict):
    FilterControlId: str
    Title: str
    SourceFilterId: str
    DisplayOptions: NotRequired[TextFieldControlDisplayOptionsTypeDef]


class ParameterTextFieldControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    DisplayOptions: NotRequired[TextFieldControlDisplayOptionsTypeDef]


class SmallMultiplesOptionsTypeDef(TypedDict):
    MaxVisibleRows: NotRequired[int]
    MaxVisibleColumns: NotRequired[int]
    PanelConfiguration: NotRequired[PanelConfigurationTypeDef]
    XAxis: NotRequired[SmallMultiplesAxisPropertiesTypeDef]
    YAxis: NotRequired[SmallMultiplesAxisPropertiesTypeDef]


class TableFieldLinkConfigurationTypeDef(TypedDict):
    Target: URLTargetConfigurationType
    Content: TableFieldLinkContentConfigurationTypeDef


class ThemeConfigurationOutputTypeDef(TypedDict):
    DataColorPalette: NotRequired[DataColorPaletteOutputTypeDef]
    UIColorPalette: NotRequired[UIColorPaletteTypeDef]
    Sheet: NotRequired[SheetStyleTypeDef]
    Typography: NotRequired[TypographyOutputTypeDef]


class ThemeConfigurationTypeDef(TypedDict):
    DataColorPalette: NotRequired[DataColorPaletteTypeDef]
    UIColorPalette: NotRequired[UIColorPaletteTypeDef]
    Sheet: NotRequired[SheetStyleTypeDef]
    Typography: NotRequired[TypographyTypeDef]


class GeospatialCircleSymbolStyleOutputTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]
    CircleRadius: NotRequired[GeospatialCircleRadiusTypeDef]


class GeospatialLineSymbolStyleOutputTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorOutputTypeDef]
    LineWidth: NotRequired[GeospatialLineWidthTypeDef]


class GeospatialPolygonSymbolStyleOutputTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]


class GeospatialCircleSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorTypeDef]
    StrokeColor: NotRequired[GeospatialColorTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]
    CircleRadius: NotRequired[GeospatialCircleRadiusTypeDef]


class GeospatialLineSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorTypeDef]
    LineWidth: NotRequired[GeospatialLineWidthTypeDef]


class GeospatialPolygonSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorTypeDef]
    StrokeColor: NotRequired[GeospatialColorTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]


class PivotTableOptionsOutputTypeDef(TypedDict):
    MetricPlacement: NotRequired[PivotTableMetricPlacementType]
    SingleMetricVisibility: NotRequired[VisibilityType]
    ColumnNamesVisibility: NotRequired[VisibilityType]
    ToggleButtonsVisibility: NotRequired[VisibilityType]
    ColumnHeaderStyle: NotRequired[TableCellStyleTypeDef]
    RowHeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowFieldNamesStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsOutputTypeDef]
    CollapsedRowDimensionsVisibility: NotRequired[VisibilityType]
    RowsLayout: NotRequired[PivotTableRowsLayoutType]
    RowsLabelOptions: NotRequired[PivotTableRowsLabelOptionsTypeDef]
    DefaultCellWidth: NotRequired[str]


class PivotTableOptionsTypeDef(TypedDict):
    MetricPlacement: NotRequired[PivotTableMetricPlacementType]
    SingleMetricVisibility: NotRequired[VisibilityType]
    ColumnNamesVisibility: NotRequired[VisibilityType]
    ToggleButtonsVisibility: NotRequired[VisibilityType]
    ColumnHeaderStyle: NotRequired[TableCellStyleTypeDef]
    RowHeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowFieldNamesStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsTypeDef]
    CollapsedRowDimensionsVisibility: NotRequired[VisibilityType]
    RowsLayout: NotRequired[PivotTableRowsLayoutType]
    RowsLabelOptions: NotRequired[PivotTableRowsLabelOptionsTypeDef]
    DefaultCellWidth: NotRequired[str]


class PivotTotalOptionsOutputTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[list[TotalAggregationOptionTypeDef]]


class PivotTotalOptionsTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[Sequence[TotalAggregationOptionTypeDef]]


class SubtotalOptionsOutputTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    CustomLabel: NotRequired[str]
    FieldLevel: NotRequired[PivotTableSubtotalLevelType]
    FieldLevelOptions: NotRequired[list[PivotTableFieldSubtotalOptionsTypeDef]]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    StyleTargets: NotRequired[list[TableStyleTargetTypeDef]]


class SubtotalOptionsTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    CustomLabel: NotRequired[str]
    FieldLevel: NotRequired[PivotTableSubtotalLevelType]
    FieldLevelOptions: NotRequired[Sequence[PivotTableFieldSubtotalOptionsTypeDef]]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    StyleTargets: NotRequired[Sequence[TableStyleTargetTypeDef]]


class TableOptionsOutputTypeDef(TypedDict):
    Orientation: NotRequired[TableOrientationType]
    HeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsOutputTypeDef]


class TableOptionsTypeDef(TypedDict):
    Orientation: NotRequired[TableOrientationType]
    HeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsTypeDef]


class TotalOptionsOutputTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[list[TotalAggregationOptionTypeDef]]


class TotalOptionsTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[Sequence[TotalAggregationOptionTypeDef]]


class GaugeChartArcConditionalFormattingOutputTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]


class GaugeChartPrimaryValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIActualValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIComparisonValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIPrimaryValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIProgressBarConditionalFormattingOutputTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]


class ShapeConditionalFormatOutputTypeDef(TypedDict):
    BackgroundColor: ConditionalFormattingColorOutputTypeDef


class TableRowConditionalFormattingOutputTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]


class TextConditionalFormatOutputTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class GaugeChartArcConditionalFormattingTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorTypeDef]


class GaugeChartPrimaryValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIActualValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIComparisonValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIPrimaryValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIProgressBarConditionalFormattingTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorTypeDef]


class ShapeConditionalFormatTypeDef(TypedDict):
    BackgroundColor: ConditionalFormattingColorTypeDef


class TableRowConditionalFormattingTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorTypeDef]


class TextConditionalFormatTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class SheetControlLayoutOutputTypeDef(TypedDict):
    Configuration: SheetControlLayoutConfigurationOutputTypeDef


class SheetControlLayoutTypeDef(TypedDict):
    Configuration: SheetControlLayoutConfigurationTypeDef


class LogoConfigurationTypeDef(TypedDict):
    AltText: str
    LogoSet: LogoSetConfigurationTypeDef


class LogoTypeDef(TypedDict):
    AltText: str
    LogoSet: LogoSetTypeDef


class AssetBundleImportJobDataSetOverrideParametersTypeDef(TypedDict):
    DataSetId: str
    Name: NotRequired[str]
    DataSetRefreshProperties: NotRequired[DataSetRefreshPropertiesTypeDef]


class DescribeDataSetRefreshPropertiesResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    DataSetRefreshProperties: DataSetRefreshPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutDataSetRefreshPropertiesRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    DataSetRefreshProperties: DataSetRefreshPropertiesTypeDef


class ComparisonConfigurationTypeDef(TypedDict):
    ComparisonMethod: NotRequired[ComparisonMethodType]
    ComparisonFormat: NotRequired[ComparisonFormatConfigurationTypeDef]


class DateTimeFormatConfigurationTypeDef(TypedDict):
    DateTimeFormat: NotRequired[str]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]
    NumericFormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class NumberFormatConfigurationTypeDef(TypedDict):
    FormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class ReferenceLineValueLabelConfigurationTypeDef(TypedDict):
    RelativePosition: NotRequired[ReferenceLineValueLabelRelativePositionType]
    FormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class StringFormatConfigurationTypeDef(TypedDict):
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]
    NumericFormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class BodySectionDynamicCategoryDimensionConfigurationOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[list[ColumnSortTypeDef]]


class BodySectionDynamicCategoryDimensionConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[Sequence[ColumnSortTypeDef]]


class BodySectionDynamicNumericDimensionConfigurationOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[list[ColumnSortTypeDef]]


class BodySectionDynamicNumericDimensionConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[Sequence[ColumnSortTypeDef]]


class FieldSortOptionsTypeDef(TypedDict):
    FieldSort: NotRequired[FieldSortTypeDef]
    ColumnSort: NotRequired[ColumnSortTypeDef]


class PivotTableSortByOutputTypeDef(TypedDict):
    Field: NotRequired[FieldSortTypeDef]
    Column: NotRequired[ColumnSortTypeDef]
    DataPath: NotRequired[DataPathSortOutputTypeDef]


class PivotTableSortByTypeDef(TypedDict):
    Field: NotRequired[FieldSortTypeDef]
    Column: NotRequired[ColumnSortTypeDef]
    DataPath: NotRequired[DataPathSortTypeDef]


class TooltipItemTypeDef(TypedDict):
    FieldTooltipItem: NotRequired[FieldTooltipItemTypeDef]
    ColumnTooltipItem: NotRequired[ColumnTooltipItemTypeDef]


class ReferenceLineDataConfigurationTypeDef(TypedDict):
    StaticConfiguration: NotRequired[ReferenceLineStaticDataConfigurationTypeDef]
    DynamicConfiguration: NotRequired[ReferenceLineDynamicDataConfigurationTypeDef]
    AxisBinding: NotRequired[AxisBindingType]
    SeriesType: NotRequired[ReferenceLineSeriesTypeType]


class DatasetMetadataOutputTypeDef(TypedDict):
    DatasetArn: str
    DatasetName: NotRequired[str]
    DatasetDescription: NotRequired[str]
    DataAggregation: NotRequired[DataAggregationTypeDef]
    Filters: NotRequired[list[TopicFilterOutputTypeDef]]
    Columns: NotRequired[list[TopicColumnOutputTypeDef]]
    CalculatedFields: NotRequired[list[TopicCalculatedFieldOutputTypeDef]]
    NamedEntities: NotRequired[list[TopicNamedEntityOutputTypeDef]]


class DatasetMetadataTypeDef(TypedDict):
    DatasetArn: str
    DatasetName: NotRequired[str]
    DatasetDescription: NotRequired[str]
    DataAggregation: NotRequired[DataAggregationTypeDef]
    Filters: NotRequired[Sequence[TopicFilterTypeDef]]
    Columns: NotRequired[Sequence[TopicColumnTypeDef]]
    CalculatedFields: NotRequired[Sequence[TopicCalculatedFieldTypeDef]]
    NamedEntities: NotRequired[Sequence[TopicNamedEntityTypeDef]]


class ReadAuthConfigTypeDef(TypedDict):
    AuthenticationType: ConnectionAuthTypeType
    AuthenticationMetadata: ReadAuthenticationMetadataTypeDef


class DataSourceParametersTypeDef(TypedDict):
    AmazonElasticsearchParameters: NotRequired[AmazonElasticsearchParametersTypeDef]
    AthenaParameters: NotRequired[AthenaParametersTypeDef]
    AuroraParameters: NotRequired[AuroraParametersTypeDef]
    AuroraPostgreSqlParameters: NotRequired[AuroraPostgreSqlParametersTypeDef]
    AwsIotAnalyticsParameters: NotRequired[AwsIotAnalyticsParametersTypeDef]
    JiraParameters: NotRequired[JiraParametersTypeDef]
    MariaDbParameters: NotRequired[MariaDbParametersTypeDef]
    MySqlParameters: NotRequired[MySqlParametersTypeDef]
    OracleParameters: NotRequired[OracleParametersTypeDef]
    PostgreSqlParameters: NotRequired[PostgreSqlParametersTypeDef]
    PrestoParameters: NotRequired[PrestoParametersTypeDef]
    RdsParameters: NotRequired[RdsParametersTypeDef]
    RedshiftParameters: NotRequired[RedshiftParametersUnionTypeDef]
    S3Parameters: NotRequired[S3ParametersTypeDef]
    S3KnowledgeBaseParameters: NotRequired[S3KnowledgeBaseParametersTypeDef]
    ServiceNowParameters: NotRequired[ServiceNowParametersTypeDef]
    SnowflakeParameters: NotRequired[SnowflakeParametersTypeDef]
    SparkParameters: NotRequired[SparkParametersTypeDef]
    SqlServerParameters: NotRequired[SqlServerParametersTypeDef]
    TeradataParameters: NotRequired[TeradataParametersTypeDef]
    TwitterParameters: NotRequired[TwitterParametersTypeDef]
    AmazonOpenSearchParameters: NotRequired[AmazonOpenSearchParametersTypeDef]
    ExasolParameters: NotRequired[ExasolParametersTypeDef]
    DatabricksParameters: NotRequired[DatabricksParametersTypeDef]
    StarburstParameters: NotRequired[StarburstParametersTypeDef]
    TrinoParameters: NotRequired[TrinoParametersTypeDef]
    BigQueryParameters: NotRequired[BigQueryParametersTypeDef]
    ImpalaParameters: NotRequired[ImpalaParametersTypeDef]
    CustomConnectionParameters: NotRequired[CustomConnectionParametersTypeDef]
    WebCrawlerParameters: NotRequired[WebCrawlerParametersTypeDef]
    ConfluenceParameters: NotRequired[ConfluenceParametersTypeDef]
    QBusinessParameters: NotRequired[QBusinessParametersTypeDef]


class CreateRefreshScheduleRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    Schedule: RefreshScheduleUnionTypeDef


class UpdateRefreshScheduleRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    Schedule: RefreshScheduleUnionTypeDef


class SemanticModelConfigurationOutputTypeDef(TypedDict):
    TableMap: NotRequired[dict[str, SemanticTableOutputTypeDef]]


class SemanticModelConfigurationTypeDef(TypedDict):
    TableMap: NotRequired[Mapping[str, SemanticTableTypeDef]]


class AnonymousUserSnapshotJobResultTypeDef(TypedDict):
    FileGroups: NotRequired[list[SnapshotJobResultFileGroupTypeDef]]


class RegisteredUserSnapshotJobResultTypeDef(TypedDict):
    FileGroups: NotRequired[list[SnapshotJobResultFileGroupTypeDef]]


PhysicalTableUnionTypeDef = Union[PhysicalTableTypeDef, PhysicalTableOutputTypeDef]


class DefaultPaginatedLayoutConfigurationTypeDef(TypedDict):
    SectionBased: NotRequired[DefaultSectionBasedLayoutConfigurationTypeDef]


class SectionLayoutConfigurationOutputTypeDef(TypedDict):
    FreeFormLayout: FreeFormSectionLayoutConfigurationOutputTypeDef


class SectionLayoutConfigurationTypeDef(TypedDict):
    FreeFormLayout: FreeFormSectionLayoutConfigurationTypeDef


class DescribeDashboardSnapshotJobResponseTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str
    UserConfiguration: SnapshotUserConfigurationRedactedTypeDef
    SnapshotConfiguration: SnapshotConfigurationOutputTypeDef
    Arn: str
    JobStatus: SnapshotJobStatusType
    CreatedTime: datetime
    LastUpdatedTime: datetime
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


SnapshotConfigurationUnionTypeDef = Union[
    SnapshotConfigurationTypeDef, SnapshotConfigurationOutputTypeDef
]


class GenerateEmbedUrlForRegisteredUserRequestTypeDef(TypedDict):
    AwsAccountId: str
    UserArn: str
    ExperienceConfiguration: RegisteredUserEmbeddingExperienceConfigurationTypeDef
    SessionLifetimeInMinutes: NotRequired[int]
    AllowedDomains: NotRequired[Sequence[str]]


class GenerateEmbedUrlForRegisteredUserWithIdentityRequestTypeDef(TypedDict):
    AwsAccountId: str
    ExperienceConfiguration: RegisteredUserEmbeddingExperienceConfigurationTypeDef
    SessionLifetimeInMinutes: NotRequired[int]
    AllowedDomains: NotRequired[Sequence[str]]


class DescribeDataSourceResponseTypeDef(TypedDict):
    DataSource: DataSourceTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListDataSourcesResponseTypeDef(TypedDict):
    DataSources: list[DataSourceTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CustomActionSetParametersOperationTypeDef(TypedDict):
    ParameterValueConfigurations: Sequence[SetParameterValueConfigurationTypeDef]


class DataSetDateFilterConditionTypeDef(TypedDict):
    ColumnName: NotRequired[str]
    ComparisonFilterCondition: NotRequired[DataSetDateComparisonFilterConditionUnionTypeDef]
    RangeFilterCondition: NotRequired[DataSetDateRangeFilterConditionUnionTypeDef]


class DatasetParameterTypeDef(TypedDict):
    StringDatasetParameter: NotRequired[StringDatasetParameterUnionTypeDef]
    DecimalDatasetParameter: NotRequired[DecimalDatasetParameterUnionTypeDef]
    IntegerDatasetParameter: NotRequired[IntegerDatasetParameterUnionTypeDef]
    DateTimeDatasetParameter: NotRequired[DateTimeDatasetParameterUnionTypeDef]


CreateActionConnectorRequestTypeDef = TypedDict(
    "CreateActionConnectorRequestTypeDef",
    {
        "AwsAccountId": str,
        "ActionConnectorId": str,
        "Name": str,
        "Type": ActionConnectorTypeType,
        "AuthenticationConfig": AuthConfigTypeDef,
        "Description": NotRequired[str],
        "Permissions": NotRequired[Sequence[ResourcePermissionUnionTypeDef]],
        "VpcConnectionArn": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class UpdateActionConnectorRequestTypeDef(TypedDict):
    AwsAccountId: str
    ActionConnectorId: str
    Name: str
    AuthenticationConfig: AuthConfigTypeDef
    Description: NotRequired[str]
    VpcConnectionArn: NotRequired[str]


class ContributionAnalysisTimeRangesTypeDef(TypedDict):
    StartRange: NotRequired[TopicIRFilterOptionUnionTypeDef]
    EndRange: NotRequired[TopicIRFilterOptionUnionTypeDef]


class ImageCustomActionOperationOutputTypeDef(TypedDict):
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationOutputTypeDef]


class LayerCustomActionOperationOutputTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationOutputTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationOutputTypeDef]


class VisualCustomActionOperationOutputTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationOutputTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationOutputTypeDef]


class TransformStepOutputTypeDef(TypedDict):
    ImportTableStep: NotRequired[ImportTableOperationOutputTypeDef]
    ProjectStep: NotRequired[ProjectOperationOutputTypeDef]
    FiltersStep: NotRequired[FiltersOperationOutputTypeDef]
    CreateColumnsStep: NotRequired[CreateColumnsOperationOutputTypeDef]
    RenameColumnsStep: NotRequired[RenameColumnsOperationOutputTypeDef]
    CastColumnTypesStep: NotRequired[CastColumnTypesOperationOutputTypeDef]
    JoinStep: NotRequired[JoinOperationOutputTypeDef]
    AggregateStep: NotRequired[AggregateOperationOutputTypeDef]
    PivotStep: NotRequired[PivotOperationOutputTypeDef]
    UnpivotStep: NotRequired[UnpivotOperationOutputTypeDef]
    AppendStep: NotRequired[AppendOperationOutputTypeDef]


class LogicalTableOutputTypeDef(TypedDict):
    Alias: str
    Source: LogicalTableSourceTypeDef
    DataTransforms: NotRequired[list[TransformOperationOutputTypeDef]]


DataSetStringFilterConditionUnionTypeDef = Union[
    DataSetStringFilterConditionTypeDef, DataSetStringFilterConditionOutputTypeDef
]


class TopicIROutputTypeDef(TypedDict):
    Metrics: NotRequired[list[TopicIRMetricOutputTypeDef]]
    GroupByList: NotRequired[list[TopicIRGroupByTypeDef]]
    Filters: NotRequired[list[list[TopicIRFilterOptionOutputTypeDef]]]
    Sort: NotRequired[TopicSortClauseTypeDef]
    ContributionAnalysis: NotRequired[TopicIRContributionAnalysisOutputTypeDef]
    Visual: NotRequired[VisualOptionsTypeDef]


class LineSeriesAxisDisplayOptionsOutputTypeDef(TypedDict):
    AxisOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    MissingDataConfigurations: NotRequired[list[MissingDataConfigurationTypeDef]]


class LineSeriesAxisDisplayOptionsTypeDef(TypedDict):
    AxisOptions: NotRequired[AxisDisplayOptionsTypeDef]
    MissingDataConfigurations: NotRequired[Sequence[MissingDataConfigurationTypeDef]]


class DefaultFilterControlOptionsOutputTypeDef(TypedDict):
    DefaultDateTimePickerOptions: NotRequired[DefaultDateTimePickerControlOptionsTypeDef]
    DefaultListOptions: NotRequired[DefaultFilterListControlOptionsOutputTypeDef]
    DefaultDropdownOptions: NotRequired[DefaultFilterDropDownControlOptionsOutputTypeDef]
    DefaultTextFieldOptions: NotRequired[DefaultTextFieldControlOptionsTypeDef]
    DefaultTextAreaOptions: NotRequired[DefaultTextAreaControlOptionsTypeDef]
    DefaultSliderOptions: NotRequired[DefaultSliderControlOptionsTypeDef]
    DefaultRelativeDateTimeOptions: NotRequired[DefaultRelativeDateTimeControlOptionsTypeDef]


class DefaultFilterControlOptionsTypeDef(TypedDict):
    DefaultDateTimePickerOptions: NotRequired[DefaultDateTimePickerControlOptionsTypeDef]
    DefaultListOptions: NotRequired[DefaultFilterListControlOptionsTypeDef]
    DefaultDropdownOptions: NotRequired[DefaultFilterDropDownControlOptionsTypeDef]
    DefaultTextFieldOptions: NotRequired[DefaultTextFieldControlOptionsTypeDef]
    DefaultTextAreaOptions: NotRequired[DefaultTextAreaControlOptionsTypeDef]
    DefaultSliderOptions: NotRequired[DefaultSliderControlOptionsTypeDef]
    DefaultRelativeDateTimeOptions: NotRequired[DefaultRelativeDateTimeControlOptionsTypeDef]


FilterControlOutputTypeDef = TypedDict(
    "FilterControlOutputTypeDef",
    {
        "DateTimePicker": NotRequired[FilterDateTimePickerControlTypeDef],
        "List": NotRequired[FilterListControlOutputTypeDef],
        "Dropdown": NotRequired[FilterDropDownControlOutputTypeDef],
        "TextField": NotRequired[FilterTextFieldControlTypeDef],
        "TextArea": NotRequired[FilterTextAreaControlTypeDef],
        "Slider": NotRequired[FilterSliderControlTypeDef],
        "RelativeDateTime": NotRequired[FilterRelativeDateTimeControlTypeDef],
        "CrossSheet": NotRequired[FilterCrossSheetControlOutputTypeDef],
    },
)
FilterControlTypeDef = TypedDict(
    "FilterControlTypeDef",
    {
        "DateTimePicker": NotRequired[FilterDateTimePickerControlTypeDef],
        "List": NotRequired[FilterListControlTypeDef],
        "Dropdown": NotRequired[FilterDropDownControlTypeDef],
        "TextField": NotRequired[FilterTextFieldControlTypeDef],
        "TextArea": NotRequired[FilterTextAreaControlTypeDef],
        "Slider": NotRequired[FilterSliderControlTypeDef],
        "RelativeDateTime": NotRequired[FilterRelativeDateTimeControlTypeDef],
        "CrossSheet": NotRequired[FilterCrossSheetControlTypeDef],
    },
)
ParameterControlOutputTypeDef = TypedDict(
    "ParameterControlOutputTypeDef",
    {
        "DateTimePicker": NotRequired[ParameterDateTimePickerControlTypeDef],
        "List": NotRequired[ParameterListControlOutputTypeDef],
        "Dropdown": NotRequired[ParameterDropDownControlOutputTypeDef],
        "TextField": NotRequired[ParameterTextFieldControlTypeDef],
        "TextArea": NotRequired[ParameterTextAreaControlTypeDef],
        "Slider": NotRequired[ParameterSliderControlTypeDef],
    },
)
ParameterControlTypeDef = TypedDict(
    "ParameterControlTypeDef",
    {
        "DateTimePicker": NotRequired[ParameterDateTimePickerControlTypeDef],
        "List": NotRequired[ParameterListControlTypeDef],
        "Dropdown": NotRequired[ParameterDropDownControlTypeDef],
        "TextField": NotRequired[ParameterTextFieldControlTypeDef],
        "TextArea": NotRequired[ParameterTextAreaControlTypeDef],
        "Slider": NotRequired[ParameterSliderControlTypeDef],
    },
)


class TableFieldURLConfigurationTypeDef(TypedDict):
    LinkConfiguration: NotRequired[TableFieldLinkConfigurationTypeDef]
    ImageConfiguration: NotRequired[TableFieldImageConfigurationTypeDef]


class ThemeVersionTypeDef(TypedDict):
    VersionNumber: NotRequired[int]
    Arn: NotRequired[str]
    Description: NotRequired[str]
    BaseThemeId: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Configuration: NotRequired[ThemeConfigurationOutputTypeDef]
    Errors: NotRequired[list[ThemeErrorTypeDef]]
    Status: NotRequired[ResourceStatusType]


ThemeConfigurationUnionTypeDef = Union[ThemeConfigurationTypeDef, ThemeConfigurationOutputTypeDef]


class GeospatialPointStyleOutputTypeDef(TypedDict):
    CircleSymbolStyle: NotRequired[GeospatialCircleSymbolStyleOutputTypeDef]


class GeospatialLineStyleOutputTypeDef(TypedDict):
    LineSymbolStyle: NotRequired[GeospatialLineSymbolStyleOutputTypeDef]


class GeospatialPolygonStyleOutputTypeDef(TypedDict):
    PolygonSymbolStyle: NotRequired[GeospatialPolygonSymbolStyleOutputTypeDef]


class GeospatialPointStyleTypeDef(TypedDict):
    CircleSymbolStyle: NotRequired[GeospatialCircleSymbolStyleTypeDef]


class GeospatialLineStyleTypeDef(TypedDict):
    LineSymbolStyle: NotRequired[GeospatialLineSymbolStyleTypeDef]


class GeospatialPolygonStyleTypeDef(TypedDict):
    PolygonSymbolStyle: NotRequired[GeospatialPolygonSymbolStyleTypeDef]


class PivotTableTotalOptionsOutputTypeDef(TypedDict):
    RowSubtotalOptions: NotRequired[SubtotalOptionsOutputTypeDef]
    ColumnSubtotalOptions: NotRequired[SubtotalOptionsOutputTypeDef]
    RowTotalOptions: NotRequired[PivotTotalOptionsOutputTypeDef]
    ColumnTotalOptions: NotRequired[PivotTotalOptionsOutputTypeDef]


class PivotTableTotalOptionsTypeDef(TypedDict):
    RowSubtotalOptions: NotRequired[SubtotalOptionsTypeDef]
    ColumnSubtotalOptions: NotRequired[SubtotalOptionsTypeDef]
    RowTotalOptions: NotRequired[PivotTotalOptionsTypeDef]
    ColumnTotalOptions: NotRequired[PivotTotalOptionsTypeDef]


class GaugeChartConditionalFormattingOptionOutputTypeDef(TypedDict):
    PrimaryValue: NotRequired[GaugeChartPrimaryValueConditionalFormattingOutputTypeDef]
    Arc: NotRequired[GaugeChartArcConditionalFormattingOutputTypeDef]


class KPIConditionalFormattingOptionOutputTypeDef(TypedDict):
    PrimaryValue: NotRequired[KPIPrimaryValueConditionalFormattingOutputTypeDef]
    ProgressBar: NotRequired[KPIProgressBarConditionalFormattingOutputTypeDef]
    ActualValue: NotRequired[KPIActualValueConditionalFormattingOutputTypeDef]
    ComparisonValue: NotRequired[KPIComparisonValueConditionalFormattingOutputTypeDef]


class FilledMapShapeConditionalFormattingOutputTypeDef(TypedDict):
    FieldId: str
    Format: NotRequired[ShapeConditionalFormatOutputTypeDef]


class PivotTableCellConditionalFormattingOutputTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatOutputTypeDef]
    Scope: NotRequired[PivotTableConditionalFormattingScopeTypeDef]
    Scopes: NotRequired[list[PivotTableConditionalFormattingScopeTypeDef]]


class TableCellConditionalFormattingOutputTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatOutputTypeDef]


class GaugeChartConditionalFormattingOptionTypeDef(TypedDict):
    PrimaryValue: NotRequired[GaugeChartPrimaryValueConditionalFormattingTypeDef]
    Arc: NotRequired[GaugeChartArcConditionalFormattingTypeDef]


class KPIConditionalFormattingOptionTypeDef(TypedDict):
    PrimaryValue: NotRequired[KPIPrimaryValueConditionalFormattingTypeDef]
    ProgressBar: NotRequired[KPIProgressBarConditionalFormattingTypeDef]
    ActualValue: NotRequired[KPIActualValueConditionalFormattingTypeDef]
    ComparisonValue: NotRequired[KPIComparisonValueConditionalFormattingTypeDef]


class FilledMapShapeConditionalFormattingTypeDef(TypedDict):
    FieldId: str
    Format: NotRequired[ShapeConditionalFormatTypeDef]


class PivotTableCellConditionalFormattingTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatTypeDef]
    Scope: NotRequired[PivotTableConditionalFormattingScopeTypeDef]
    Scopes: NotRequired[Sequence[PivotTableConditionalFormattingScopeTypeDef]]


class TableCellConditionalFormattingTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatTypeDef]


class BrandDefinitionTypeDef(TypedDict):
    BrandName: str
    Description: NotRequired[str]
    ApplicationTheme: NotRequired[ApplicationThemeTypeDef]
    LogoConfiguration: NotRequired[LogoConfigurationTypeDef]


class BrandDetailTypeDef(TypedDict):
    BrandId: str
    Arn: NotRequired[str]
    BrandStatus: NotRequired[BrandStatusType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    VersionId: NotRequired[str]
    VersionStatus: NotRequired[BrandVersionStatusType]
    Errors: NotRequired[list[str]]
    Logo: NotRequired[LogoTypeDef]


class AssetBundleImportJobOverrideParametersOutputTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleImportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        list[AssetBundleImportJobVPCConnectionOverrideParametersOutputTypeDef]
    ]
    RefreshSchedules: NotRequired[
        list[AssetBundleImportJobRefreshScheduleOverrideParametersOutputTypeDef]
    ]
    DataSources: NotRequired[list[AssetBundleImportJobDataSourceOverrideParametersOutputTypeDef]]
    DataSets: NotRequired[list[AssetBundleImportJobDataSetOverrideParametersTypeDef]]
    Themes: NotRequired[list[AssetBundleImportJobThemeOverrideParametersTypeDef]]
    Analyses: NotRequired[list[AssetBundleImportJobAnalysisOverrideParametersTypeDef]]
    Dashboards: NotRequired[list[AssetBundleImportJobDashboardOverrideParametersTypeDef]]
    Folders: NotRequired[list[AssetBundleImportJobFolderOverrideParametersTypeDef]]


class GaugeChartOptionsTypeDef(TypedDict):
    PrimaryValueDisplayType: NotRequired[PrimaryValueDisplayTypeType]
    Comparison: NotRequired[ComparisonConfigurationTypeDef]
    ArcAxis: NotRequired[ArcAxisConfigurationTypeDef]
    Arc: NotRequired[ArcConfigurationTypeDef]
    PrimaryValueFontConfiguration: NotRequired[FontConfigurationTypeDef]


class KPIOptionsTypeDef(TypedDict):
    ProgressBar: NotRequired[ProgressBarOptionsTypeDef]
    TrendArrows: NotRequired[TrendArrowOptionsTypeDef]
    SecondaryValue: NotRequired[SecondaryValueOptionsTypeDef]
    Comparison: NotRequired[ComparisonConfigurationTypeDef]
    PrimaryValueDisplayType: NotRequired[PrimaryValueDisplayTypeType]
    PrimaryValueFontConfiguration: NotRequired[FontConfigurationTypeDef]
    SecondaryValueFontConfiguration: NotRequired[FontConfigurationTypeDef]
    Sparkline: NotRequired[KPISparklineOptionsTypeDef]
    VisualLayoutOptions: NotRequired[KPIVisualLayoutOptionsTypeDef]


class DateDimensionFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    DateGranularity: NotRequired[TimeGranularityType]
    HierarchyId: NotRequired[str]
    FormatConfiguration: NotRequired[DateTimeFormatConfigurationTypeDef]


class DateMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    AggregationFunction: NotRequired[DateAggregationFunctionType]
    FormatConfiguration: NotRequired[DateTimeFormatConfigurationTypeDef]


class NumericalDimensionFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    HierarchyId: NotRequired[str]
    FormatConfiguration: NotRequired[NumberFormatConfigurationTypeDef]


class NumericalMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    AggregationFunction: NotRequired[NumericalAggregationFunctionTypeDef]
    FormatConfiguration: NotRequired[NumberFormatConfigurationTypeDef]


class ReferenceLineLabelConfigurationTypeDef(TypedDict):
    ValueLabelConfiguration: NotRequired[ReferenceLineValueLabelConfigurationTypeDef]
    CustomLabelConfiguration: NotRequired[ReferenceLineCustomLabelConfigurationTypeDef]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    FontColor: NotRequired[str]
    HorizontalPosition: NotRequired[ReferenceLineLabelHorizontalPositionType]
    VerticalPosition: NotRequired[ReferenceLineLabelVerticalPositionType]


class CategoricalDimensionFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    HierarchyId: NotRequired[str]
    FormatConfiguration: NotRequired[StringFormatConfigurationTypeDef]


class CategoricalMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    AggregationFunction: NotRequired[CategoricalAggregationFunctionType]
    FormatConfiguration: NotRequired[StringFormatConfigurationTypeDef]


class FormatConfigurationTypeDef(TypedDict):
    StringFormatConfiguration: NotRequired[StringFormatConfigurationTypeDef]
    NumberFormatConfiguration: NotRequired[NumberFormatConfigurationTypeDef]
    DateTimeFormatConfiguration: NotRequired[DateTimeFormatConfigurationTypeDef]


class BodySectionRepeatDimensionConfigurationOutputTypeDef(TypedDict):
    DynamicCategoryDimensionConfiguration: NotRequired[
        BodySectionDynamicCategoryDimensionConfigurationOutputTypeDef
    ]
    DynamicNumericDimensionConfiguration: NotRequired[
        BodySectionDynamicNumericDimensionConfigurationOutputTypeDef
    ]


class BodySectionRepeatDimensionConfigurationTypeDef(TypedDict):
    DynamicCategoryDimensionConfiguration: NotRequired[
        BodySectionDynamicCategoryDimensionConfigurationTypeDef
    ]
    DynamicNumericDimensionConfiguration: NotRequired[
        BodySectionDynamicNumericDimensionConfigurationTypeDef
    ]


class BarChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[list[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[list[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class BarChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class BoxPlotSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class BoxPlotSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class ComboChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[list[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class ComboChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class FilledMapSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]


class FilledMapSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]


class FunnelChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class FunnelChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class HeatMapSortConfigurationOutputTypeDef(TypedDict):
    HeatMapRowSort: NotRequired[list[FieldSortOptionsTypeDef]]
    HeatMapColumnSort: NotRequired[list[FieldSortOptionsTypeDef]]
    HeatMapRowItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    HeatMapColumnItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class HeatMapSortConfigurationTypeDef(TypedDict):
    HeatMapRowSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    HeatMapColumnSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    HeatMapRowItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    HeatMapColumnItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class KPISortConfigurationOutputTypeDef(TypedDict):
    TrendGroupSort: NotRequired[list[FieldSortOptionsTypeDef]]


class KPISortConfigurationTypeDef(TypedDict):
    TrendGroupSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]


class LineChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    CategoryItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[list[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class LineChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class PieChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[list[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class PieChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class PluginVisualTableQuerySortOutputTypeDef(TypedDict):
    RowSort: NotRequired[list[FieldSortOptionsTypeDef]]
    ItemsLimitConfiguration: NotRequired[PluginVisualItemsLimitConfigurationTypeDef]


class PluginVisualTableQuerySortTypeDef(TypedDict):
    RowSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ItemsLimitConfiguration: NotRequired[PluginVisualItemsLimitConfigurationTypeDef]


class RadarChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[list[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class RadarChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class SankeyDiagramSortConfigurationOutputTypeDef(TypedDict):
    WeightSort: NotRequired[list[FieldSortOptionsTypeDef]]
    SourceItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    DestinationItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class SankeyDiagramSortConfigurationTypeDef(TypedDict):
    WeightSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SourceItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    DestinationItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class TableSortConfigurationOutputTypeDef(TypedDict):
    RowSort: NotRequired[list[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class TableSortConfigurationTypeDef(TypedDict):
    RowSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class TreeMapSortConfigurationOutputTypeDef(TypedDict):
    TreeMapSort: NotRequired[list[FieldSortOptionsTypeDef]]
    TreeMapGroupItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class TreeMapSortConfigurationTypeDef(TypedDict):
    TreeMapSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    TreeMapGroupItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class WaterfallChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]
    BreakdownItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class WaterfallChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    BreakdownItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class WordCloudSortConfigurationOutputTypeDef(TypedDict):
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    CategorySort: NotRequired[list[FieldSortOptionsTypeDef]]


class WordCloudSortConfigurationTypeDef(TypedDict):
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]


class PivotFieldSortOptionsOutputTypeDef(TypedDict):
    FieldId: str
    SortBy: PivotTableSortByOutputTypeDef


class PivotFieldSortOptionsTypeDef(TypedDict):
    FieldId: str
    SortBy: PivotTableSortByTypeDef


class FieldBasedTooltipOutputTypeDef(TypedDict):
    AggregationVisibility: NotRequired[VisibilityType]
    TooltipTitleType: NotRequired[TooltipTitleTypeType]
    TooltipFields: NotRequired[list[TooltipItemTypeDef]]


class FieldBasedTooltipTypeDef(TypedDict):
    AggregationVisibility: NotRequired[VisibilityType]
    TooltipTitleType: NotRequired[TooltipTitleTypeType]
    TooltipFields: NotRequired[Sequence[TooltipItemTypeDef]]


class TopicDetailsOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    UserExperienceVersion: NotRequired[TopicUserExperienceVersionType]
    DataSets: NotRequired[list[DatasetMetadataOutputTypeDef]]
    ConfigOptions: NotRequired[TopicConfigOptionsTypeDef]


class TopicDetailsTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    UserExperienceVersion: NotRequired[TopicUserExperienceVersionType]
    DataSets: NotRequired[Sequence[DatasetMetadataTypeDef]]
    ConfigOptions: NotRequired[TopicConfigOptionsTypeDef]


ActionConnectorTypeDef = TypedDict(
    "ActionConnectorTypeDef",
    {
        "Arn": str,
        "ActionConnectorId": str,
        "Type": ActionConnectorTypeType,
        "Name": str,
        "LastUpdatedTime": datetime,
        "CreatedTime": NotRequired[datetime],
        "Status": NotRequired[ResourceStatusType],
        "Error": NotRequired[ActionConnectorErrorTypeDef],
        "Description": NotRequired[str],
        "AuthenticationConfig": NotRequired[ReadAuthConfigTypeDef],
        "EnabledActions": NotRequired[list[str]],
        "VpcConnectionArn": NotRequired[str],
    },
)


class AssetBundleImportJobDataSourceOverrideParametersTypeDef(TypedDict):
    DataSourceId: str
    Name: NotRequired[str]
    DataSourceParameters: NotRequired[DataSourceParametersTypeDef]
    VpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    SslProperties: NotRequired[SslPropertiesTypeDef]
    Credentials: NotRequired[AssetBundleImportJobDataSourceCredentialsTypeDef]


DataSourceParametersUnionTypeDef = Union[
    DataSourceParametersTypeDef, DataSourceParametersOutputTypeDef
]
SemanticModelConfigurationUnionTypeDef = Union[
    SemanticModelConfigurationTypeDef, SemanticModelConfigurationOutputTypeDef
]


class SnapshotJobResultTypeDef(TypedDict):
    AnonymousUsers: NotRequired[list[AnonymousUserSnapshotJobResultTypeDef]]
    RegisteredUsers: NotRequired[list[RegisteredUserSnapshotJobResultTypeDef]]


class DefaultNewSheetConfigurationTypeDef(TypedDict):
    InteractiveLayoutConfiguration: NotRequired[DefaultInteractiveLayoutConfigurationTypeDef]
    PaginatedLayoutConfiguration: NotRequired[DefaultPaginatedLayoutConfigurationTypeDef]
    SheetContentType: NotRequired[SheetContentTypeType]


class BodySectionContentOutputTypeDef(TypedDict):
    Layout: NotRequired[SectionLayoutConfigurationOutputTypeDef]


class HeaderFooterSectionConfigurationOutputTypeDef(TypedDict):
    SectionId: str
    Layout: SectionLayoutConfigurationOutputTypeDef
    Style: NotRequired[SectionStyleTypeDef]


class BodySectionContentTypeDef(TypedDict):
    Layout: NotRequired[SectionLayoutConfigurationTypeDef]


class HeaderFooterSectionConfigurationTypeDef(TypedDict):
    SectionId: str
    Layout: SectionLayoutConfigurationTypeDef
    Style: NotRequired[SectionStyleTypeDef]


class StartDashboardSnapshotJobRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str
    SnapshotConfiguration: SnapshotConfigurationUnionTypeDef
    UserConfiguration: NotRequired[SnapshotUserConfigurationTypeDef]


class ImageCustomActionOperationTypeDef(TypedDict):
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationTypeDef]


class LayerCustomActionOperationTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationTypeDef]


class VisualCustomActionOperationTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationTypeDef]


DataSetDateFilterConditionUnionTypeDef = Union[
    DataSetDateFilterConditionTypeDef, DataSetDateFilterConditionOutputTypeDef
]
DatasetParameterUnionTypeDef = Union[DatasetParameterTypeDef, DatasetParameterOutputTypeDef]
ContributionAnalysisTimeRangesUnionTypeDef = Union[
    ContributionAnalysisTimeRangesTypeDef, ContributionAnalysisTimeRangesOutputTypeDef
]


class ImageCustomActionOutputTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: ImageCustomActionTriggerType
    ActionOperations: list[ImageCustomActionOperationOutputTypeDef]
    Status: NotRequired[WidgetStatusType]


class LayerCustomActionOutputTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: LayerCustomActionTriggerType
    ActionOperations: list[LayerCustomActionOperationOutputTypeDef]
    Status: NotRequired[WidgetStatusType]


class VisualCustomActionOutputTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: VisualCustomActionTriggerType
    ActionOperations: list[VisualCustomActionOperationOutputTypeDef]
    Status: NotRequired[WidgetStatusType]


class DataPrepConfigurationOutputTypeDef(TypedDict):
    SourceTableMap: dict[str, SourceTableOutputTypeDef]
    TransformStepMap: dict[str, TransformStepOutputTypeDef]
    DestinationTableMap: dict[str, DestinationTableTypeDef]


class TopicVisualOutputTypeDef(TypedDict):
    VisualId: NotRequired[str]
    Role: NotRequired[VisualRoleType]
    Ir: NotRequired[TopicIROutputTypeDef]
    SupportingVisuals: NotRequired[list[dict[str, Any]]]


class DefaultFilterControlConfigurationOutputTypeDef(TypedDict):
    Title: str
    ControlOptions: DefaultFilterControlOptionsOutputTypeDef


class DefaultFilterControlConfigurationTypeDef(TypedDict):
    Title: str
    ControlOptions: DefaultFilterControlOptionsTypeDef


class TableFieldOptionTypeDef(TypedDict):
    FieldId: str
    Width: NotRequired[str]
    CustomLabel: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    URLStyling: NotRequired[TableFieldURLConfigurationTypeDef]


ThemeTypeDef = TypedDict(
    "ThemeTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "ThemeId": NotRequired[str],
        "Version": NotRequired[ThemeVersionTypeDef],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "Type": NotRequired[ThemeTypeType],
    },
)


class CreateThemeRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    Name: str
    BaseThemeId: str
    Configuration: ThemeConfigurationUnionTypeDef
    VersionDescription: NotRequired[str]
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateThemeRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    BaseThemeId: str
    Name: NotRequired[str]
    VersionDescription: NotRequired[str]
    Configuration: NotRequired[ThemeConfigurationUnionTypeDef]


class GeospatialPointLayerOutputTypeDef(TypedDict):
    Style: GeospatialPointStyleOutputTypeDef


class GeospatialLineLayerOutputTypeDef(TypedDict):
    Style: GeospatialLineStyleOutputTypeDef


class GeospatialPolygonLayerOutputTypeDef(TypedDict):
    Style: GeospatialPolygonStyleOutputTypeDef


class GeospatialPointLayerTypeDef(TypedDict):
    Style: GeospatialPointStyleTypeDef


class GeospatialLineLayerTypeDef(TypedDict):
    Style: GeospatialLineStyleTypeDef


class GeospatialPolygonLayerTypeDef(TypedDict):
    Style: GeospatialPolygonStyleTypeDef


class GaugeChartConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        list[GaugeChartConditionalFormattingOptionOutputTypeDef]
    ]


class KPIConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[list[KPIConditionalFormattingOptionOutputTypeDef]]


class FilledMapConditionalFormattingOptionOutputTypeDef(TypedDict):
    Shape: FilledMapShapeConditionalFormattingOutputTypeDef


class PivotTableConditionalFormattingOptionOutputTypeDef(TypedDict):
    Cell: NotRequired[PivotTableCellConditionalFormattingOutputTypeDef]


class TableConditionalFormattingOptionOutputTypeDef(TypedDict):
    Cell: NotRequired[TableCellConditionalFormattingOutputTypeDef]
    Row: NotRequired[TableRowConditionalFormattingOutputTypeDef]


class GaugeChartConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        Sequence[GaugeChartConditionalFormattingOptionTypeDef]
    ]


class KPIConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[Sequence[KPIConditionalFormattingOptionTypeDef]]


class FilledMapConditionalFormattingOptionTypeDef(TypedDict):
    Shape: FilledMapShapeConditionalFormattingTypeDef


class PivotTableConditionalFormattingOptionTypeDef(TypedDict):
    Cell: NotRequired[PivotTableCellConditionalFormattingTypeDef]


class TableConditionalFormattingOptionTypeDef(TypedDict):
    Cell: NotRequired[TableCellConditionalFormattingTypeDef]
    Row: NotRequired[TableRowConditionalFormattingTypeDef]


class CreateBrandRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    BrandDefinition: NotRequired[BrandDefinitionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateBrandRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    BrandDefinition: NotRequired[BrandDefinitionTypeDef]


class CreateBrandResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBrandPublishedVersionResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBrandResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAssetBundleImportJobResponseTypeDef(TypedDict):
    JobStatus: AssetBundleImportJobStatusType
    Errors: list[AssetBundleImportJobErrorTypeDef]
    RollbackErrors: list[AssetBundleImportJobErrorTypeDef]
    Arn: str
    CreatedTime: datetime
    AssetBundleImportJobId: str
    AwsAccountId: str
    AssetBundleImportSource: AssetBundleImportSourceDescriptionTypeDef
    OverrideParameters: AssetBundleImportJobOverrideParametersOutputTypeDef
    FailureAction: AssetBundleImportFailureActionType
    RequestId: str
    Status: int
    OverridePermissions: AssetBundleImportJobOverridePermissionsOutputTypeDef
    OverrideTags: AssetBundleImportJobOverrideTagsOutputTypeDef
    OverrideValidationStrategy: AssetBundleImportJobOverrideValidationStrategyTypeDef
    Warnings: list[AssetBundleImportJobWarningTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ReferenceLineTypeDef(TypedDict):
    DataConfiguration: ReferenceLineDataConfigurationTypeDef
    Status: NotRequired[WidgetStatusType]
    StyleConfiguration: NotRequired[ReferenceLineStyleConfigurationTypeDef]
    LabelConfiguration: NotRequired[ReferenceLineLabelConfigurationTypeDef]


class DimensionFieldTypeDef(TypedDict):
    NumericalDimensionField: NotRequired[NumericalDimensionFieldTypeDef]
    CategoricalDimensionField: NotRequired[CategoricalDimensionFieldTypeDef]
    DateDimensionField: NotRequired[DateDimensionFieldTypeDef]


class MeasureFieldTypeDef(TypedDict):
    NumericalMeasureField: NotRequired[NumericalMeasureFieldTypeDef]
    CategoricalMeasureField: NotRequired[CategoricalMeasureFieldTypeDef]
    DateMeasureField: NotRequired[DateMeasureFieldTypeDef]
    CalculatedMeasureField: NotRequired[CalculatedMeasureFieldTypeDef]


class ColumnConfigurationOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    FormatConfiguration: NotRequired[FormatConfigurationTypeDef]
    Role: NotRequired[ColumnRoleType]
    ColorsConfiguration: NotRequired[ColorsConfigurationOutputTypeDef]
    DecalSettingsConfiguration: NotRequired[DecalSettingsConfigurationOutputTypeDef]


class ColumnConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    FormatConfiguration: NotRequired[FormatConfigurationTypeDef]
    Role: NotRequired[ColumnRoleType]
    ColorsConfiguration: NotRequired[ColorsConfigurationTypeDef]
    DecalSettingsConfiguration: NotRequired[DecalSettingsConfigurationTypeDef]


class UnaggregatedFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    FormatConfiguration: NotRequired[FormatConfigurationTypeDef]


class BodySectionRepeatConfigurationOutputTypeDef(TypedDict):
    DimensionConfigurations: NotRequired[list[BodySectionRepeatDimensionConfigurationOutputTypeDef]]
    PageBreakConfiguration: NotRequired[BodySectionRepeatPageBreakConfigurationTypeDef]
    NonRepeatingVisuals: NotRequired[list[str]]


class BodySectionRepeatConfigurationTypeDef(TypedDict):
    DimensionConfigurations: NotRequired[Sequence[BodySectionRepeatDimensionConfigurationTypeDef]]
    PageBreakConfiguration: NotRequired[BodySectionRepeatPageBreakConfigurationTypeDef]
    NonRepeatingVisuals: NotRequired[Sequence[str]]


class PluginVisualSortConfigurationOutputTypeDef(TypedDict):
    PluginVisualTableQuerySort: NotRequired[PluginVisualTableQuerySortOutputTypeDef]


class PluginVisualSortConfigurationTypeDef(TypedDict):
    PluginVisualTableQuerySort: NotRequired[PluginVisualTableQuerySortTypeDef]


class PivotTableSortConfigurationOutputTypeDef(TypedDict):
    FieldSortOptions: NotRequired[list[PivotFieldSortOptionsOutputTypeDef]]


class PivotTableSortConfigurationTypeDef(TypedDict):
    FieldSortOptions: NotRequired[Sequence[PivotFieldSortOptionsTypeDef]]


class TooltipOptionsOutputTypeDef(TypedDict):
    TooltipVisibility: NotRequired[VisibilityType]
    SelectedTooltipType: NotRequired[SelectedTooltipTypeType]
    FieldBasedTooltip: NotRequired[FieldBasedTooltipOutputTypeDef]


class TooltipOptionsTypeDef(TypedDict):
    TooltipVisibility: NotRequired[VisibilityType]
    SelectedTooltipType: NotRequired[SelectedTooltipTypeType]
    FieldBasedTooltip: NotRequired[FieldBasedTooltipTypeDef]


class DescribeTopicResponseTypeDef(TypedDict):
    Arn: str
    TopicId: str
    Topic: TopicDetailsOutputTypeDef
    RequestId: str
    Status: int
    CustomInstructions: CustomInstructionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


TopicDetailsUnionTypeDef = Union[TopicDetailsTypeDef, TopicDetailsOutputTypeDef]


class DescribeActionConnectorResponseTypeDef(TypedDict):
    ActionConnector: ActionConnectorTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class AssetBundleImportJobOverrideParametersTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleImportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        Sequence[AssetBundleImportJobVPCConnectionOverrideParametersTypeDef]
    ]
    RefreshSchedules: NotRequired[
        Sequence[AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef]
    ]
    DataSources: NotRequired[Sequence[AssetBundleImportJobDataSourceOverrideParametersTypeDef]]
    DataSets: NotRequired[Sequence[AssetBundleImportJobDataSetOverrideParametersTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleImportJobThemeOverrideParametersTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleImportJobAnalysisOverrideParametersTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleImportJobDashboardOverrideParametersTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleImportJobFolderOverrideParametersTypeDef]]


class CredentialPairTypeDef(TypedDict):
    Username: str
    Password: str
    AlternateDataSourceParameters: NotRequired[Sequence[DataSourceParametersUnionTypeDef]]


class DescribeDashboardSnapshotJobResultResponseTypeDef(TypedDict):
    Arn: str
    JobStatus: SnapshotJobStatusType
    CreatedTime: datetime
    LastUpdatedTime: datetime
    Result: SnapshotJobResultTypeDef
    ErrorInfo: SnapshotJobErrorInfoTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class AnalysisDefaultsTypeDef(TypedDict):
    DefaultNewSheetConfiguration: DefaultNewSheetConfigurationTypeDef


class ImageCustomActionTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: ImageCustomActionTriggerType
    ActionOperations: Sequence[ImageCustomActionOperationTypeDef]
    Status: NotRequired[WidgetStatusType]


class LayerCustomActionTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: LayerCustomActionTriggerType
    ActionOperations: Sequence[LayerCustomActionOperationTypeDef]
    Status: NotRequired[WidgetStatusType]


class VisualCustomActionTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: VisualCustomActionTriggerType
    ActionOperations: Sequence[VisualCustomActionOperationTypeDef]
    Status: NotRequired[WidgetStatusType]


class FilterOperationTypeDef(TypedDict):
    ConditionExpression: NotRequired[str]
    StringFilterCondition: NotRequired[DataSetStringFilterConditionUnionTypeDef]
    NumericFilterCondition: NotRequired[DataSetNumericFilterConditionTypeDef]
    DateFilterCondition: NotRequired[DataSetDateFilterConditionUnionTypeDef]


class TopicIRContributionAnalysisTypeDef(TypedDict):
    Factors: NotRequired[Sequence[ContributionAnalysisFactorTypeDef]]
    TimeRanges: NotRequired[ContributionAnalysisTimeRangesUnionTypeDef]
    Direction: NotRequired[ContributionAnalysisDirectionType]
    SortType: NotRequired[ContributionAnalysisSortTypeType]


class SheetImageOutputTypeDef(TypedDict):
    SheetImageId: str
    Source: SheetImageSourceTypeDef
    Scaling: NotRequired[SheetImageScalingConfigurationTypeDef]
    Tooltip: NotRequired[SheetImageTooltipConfigurationTypeDef]
    ImageContentAltText: NotRequired[str]
    Interactions: NotRequired[ImageInteractionOptionsTypeDef]
    Actions: NotRequired[list[ImageCustomActionOutputTypeDef]]


class CustomContentVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[CustomContentConfigurationTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class EmptyVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]


class DataSetTypeDef(TypedDict):
    Arn: NotRequired[str]
    DataSetId: NotRequired[str]
    Name: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    PhysicalTableMap: NotRequired[dict[str, PhysicalTableOutputTypeDef]]
    LogicalTableMap: NotRequired[dict[str, LogicalTableOutputTypeDef]]
    OutputColumns: NotRequired[list[OutputColumnTypeDef]]
    ImportMode: NotRequired[DataSetImportModeType]
    ConsumedSpiceCapacityInBytes: NotRequired[int]
    ColumnGroups: NotRequired[list[ColumnGroupOutputTypeDef]]
    FieldFolders: NotRequired[dict[str, FieldFolderOutputTypeDef]]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionTagConfiguration: NotRequired[RowLevelPermissionTagConfigurationOutputTypeDef]
    ColumnLevelPermissionRules: NotRequired[list[ColumnLevelPermissionRuleOutputTypeDef]]
    DataSetUsageConfiguration: NotRequired[DataSetUsageConfigurationTypeDef]
    DatasetParameters: NotRequired[list[DatasetParameterOutputTypeDef]]
    PerformanceConfiguration: NotRequired[PerformanceConfigurationOutputTypeDef]
    UseAs: NotRequired[Literal["RLS_RULES"]]
    DataPrepConfiguration: NotRequired[DataPrepConfigurationOutputTypeDef]
    SemanticModelConfiguration: NotRequired[SemanticModelConfigurationOutputTypeDef]


class TopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: str
    DatasetArn: str
    Question: str
    Arn: NotRequired[str]
    Mir: NotRequired[TopicIROutputTypeDef]
    PrimaryVisual: NotRequired[TopicVisualOutputTypeDef]
    Template: NotRequired[TopicTemplateOutputTypeDef]


class CategoryFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationOutputTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class CategoryInnerFilterOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationOutputTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class NumericEqualityFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    MatchOperator: NumericEqualityMatchOperatorType
    NullOption: FilterNullOptionType
    Value: NotRequired[float]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class NumericRangeFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimum: NotRequired[NumericRangeFilterValueTypeDef]
    RangeMaximum: NotRequired[NumericRangeFilterValueTypeDef]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class RelativeDatesFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AnchorDateConfiguration: AnchorDateConfigurationTypeDef
    TimeGranularity: TimeGranularityType
    RelativeDateType: RelativeDateTypeType
    NullOption: FilterNullOptionType
    MinimumGranularity: NotRequired[TimeGranularityType]
    RelativeDateValue: NotRequired[int]
    ParameterName: NotRequired[str]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class TimeEqualityFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Value: NotRequired[datetime]
    ParameterName: NotRequired[str]
    TimeGranularity: NotRequired[TimeGranularityType]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class TimeRangeFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimumValue: NotRequired[TimeRangeFilterValueOutputTypeDef]
    RangeMaximumValue: NotRequired[TimeRangeFilterValueOutputTypeDef]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class TopBottomFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AggregationSortConfigurations: list[AggregationSortConfigurationTypeDef]
    Limit: NotRequired[int]
    TimeGranularity: NotRequired[TimeGranularityType]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class CategoryFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class CategoryInnerFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class NumericEqualityFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    MatchOperator: NumericEqualityMatchOperatorType
    NullOption: FilterNullOptionType
    Value: NotRequired[float]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class NumericRangeFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimum: NotRequired[NumericRangeFilterValueTypeDef]
    RangeMaximum: NotRequired[NumericRangeFilterValueTypeDef]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class RelativeDatesFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AnchorDateConfiguration: AnchorDateConfigurationTypeDef
    TimeGranularity: TimeGranularityType
    RelativeDateType: RelativeDateTypeType
    NullOption: FilterNullOptionType
    MinimumGranularity: NotRequired[TimeGranularityType]
    RelativeDateValue: NotRequired[int]
    ParameterName: NotRequired[str]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class TimeEqualityFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Value: NotRequired[TimestampTypeDef]
    ParameterName: NotRequired[str]
    TimeGranularity: NotRequired[TimeGranularityType]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class TimeRangeFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimumValue: NotRequired[TimeRangeFilterValueTypeDef]
    RangeMaximumValue: NotRequired[TimeRangeFilterValueTypeDef]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class TopBottomFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AggregationSortConfigurations: Sequence[AggregationSortConfigurationTypeDef]
    Limit: NotRequired[int]
    TimeGranularity: NotRequired[TimeGranularityType]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationTypeDef]


class TableFieldOptionsOutputTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[list[TableFieldOptionTypeDef]]
    Order: NotRequired[list[str]]
    PinnedFieldOptions: NotRequired[TablePinnedFieldOptionsOutputTypeDef]
    TransposedTableOptions: NotRequired[list[TransposedTableOptionTypeDef]]


class TableFieldOptionsTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[Sequence[TableFieldOptionTypeDef]]
    Order: NotRequired[Sequence[str]]
    PinnedFieldOptions: NotRequired[TablePinnedFieldOptionsTypeDef]
    TransposedTableOptions: NotRequired[Sequence[TransposedTableOptionTypeDef]]


class DescribeThemeResponseTypeDef(TypedDict):
    Theme: ThemeTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GeospatialLayerDefinitionOutputTypeDef(TypedDict):
    PointLayer: NotRequired[GeospatialPointLayerOutputTypeDef]
    LineLayer: NotRequired[GeospatialLineLayerOutputTypeDef]
    PolygonLayer: NotRequired[GeospatialPolygonLayerOutputTypeDef]


class GeospatialLayerDefinitionTypeDef(TypedDict):
    PointLayer: NotRequired[GeospatialPointLayerTypeDef]
    LineLayer: NotRequired[GeospatialLineLayerTypeDef]
    PolygonLayer: NotRequired[GeospatialPolygonLayerTypeDef]


class FilledMapConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: list[FilledMapConditionalFormattingOptionOutputTypeDef]


class PivotTableConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        list[PivotTableConditionalFormattingOptionOutputTypeDef]
    ]


class TableConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[list[TableConditionalFormattingOptionOutputTypeDef]]


class FilledMapConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: Sequence[FilledMapConditionalFormattingOptionTypeDef]


class PivotTableConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        Sequence[PivotTableConditionalFormattingOptionTypeDef]
    ]


class TableConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[Sequence[TableConditionalFormattingOptionTypeDef]]


class UniqueValuesComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Category: NotRequired[DimensionFieldTypeDef]


class BarChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]
    Colors: NotRequired[list[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[list[DimensionFieldTypeDef]]


class BarChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[Sequence[DimensionFieldTypeDef]]


class BoxPlotAggregatedFieldWellsOutputTypeDef(TypedDict):
    GroupBy: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]


class BoxPlotAggregatedFieldWellsTypeDef(TypedDict):
    GroupBy: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class ComboChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[list[DimensionFieldTypeDef]]
    BarValues: NotRequired[list[MeasureFieldTypeDef]]
    Colors: NotRequired[list[DimensionFieldTypeDef]]
    LineValues: NotRequired[list[MeasureFieldTypeDef]]


class ComboChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    BarValues: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]
    LineValues: NotRequired[Sequence[MeasureFieldTypeDef]]


class FilledMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Geospatial: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]


class FilledMapAggregatedFieldWellsTypeDef(TypedDict):
    Geospatial: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class ForecastComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]
    PeriodsForward: NotRequired[int]
    PeriodsBackward: NotRequired[int]
    UpperBoundary: NotRequired[float]
    LowerBoundary: NotRequired[float]
    PredictionInterval: NotRequired[int]
    Seasonality: NotRequired[ForecastComputationSeasonalityType]
    CustomSeasonalityValue: NotRequired[int]


class FunnelChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]


class FunnelChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class GaugeChartFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[list[MeasureFieldTypeDef]]
    TargetValues: NotRequired[list[MeasureFieldTypeDef]]


class GaugeChartFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    TargetValues: NotRequired[Sequence[MeasureFieldTypeDef]]


class GeospatialLayerColorFieldOutputTypeDef(TypedDict):
    ColorDimensionsFields: NotRequired[list[DimensionFieldTypeDef]]
    ColorValuesFields: NotRequired[list[MeasureFieldTypeDef]]


class GeospatialLayerColorFieldTypeDef(TypedDict):
    ColorDimensionsFields: NotRequired[Sequence[DimensionFieldTypeDef]]
    ColorValuesFields: NotRequired[Sequence[MeasureFieldTypeDef]]


class GeospatialMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Geospatial: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]
    Colors: NotRequired[list[DimensionFieldTypeDef]]


class GeospatialMapAggregatedFieldWellsTypeDef(TypedDict):
    Geospatial: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]


class GrowthRateComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]
    PeriodSize: NotRequired[int]


class HeatMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Rows: NotRequired[list[DimensionFieldTypeDef]]
    Columns: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]


class HeatMapAggregatedFieldWellsTypeDef(TypedDict):
    Rows: NotRequired[Sequence[DimensionFieldTypeDef]]
    Columns: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class HistogramAggregatedFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[list[MeasureFieldTypeDef]]


class HistogramAggregatedFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class KPIFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[list[MeasureFieldTypeDef]]
    TargetValues: NotRequired[list[MeasureFieldTypeDef]]
    TrendGroups: NotRequired[list[DimensionFieldTypeDef]]


class KPIFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    TargetValues: NotRequired[Sequence[MeasureFieldTypeDef]]
    TrendGroups: NotRequired[Sequence[DimensionFieldTypeDef]]


class LineChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]
    Colors: NotRequired[list[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[list[DimensionFieldTypeDef]]


class LineChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[Sequence[DimensionFieldTypeDef]]


MaximumMinimumComputationTypeDef = TypedDict(
    "MaximumMinimumComputationTypeDef",
    {
        "ComputationId": str,
        "Type": MaximumMinimumComputationTypeType,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
    },
)


class MetricComparisonComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    FromValue: NotRequired[MeasureFieldTypeDef]
    TargetValue: NotRequired[MeasureFieldTypeDef]


class PeriodOverPeriodComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]


class PeriodToDateComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]
    PeriodTimeGranularity: NotRequired[TimeGranularityType]


class PieChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]
    SmallMultiples: NotRequired[list[DimensionFieldTypeDef]]


class PieChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    SmallMultiples: NotRequired[Sequence[DimensionFieldTypeDef]]


class PivotTableAggregatedFieldWellsOutputTypeDef(TypedDict):
    Rows: NotRequired[list[DimensionFieldTypeDef]]
    Columns: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]


class PivotTableAggregatedFieldWellsTypeDef(TypedDict):
    Rows: NotRequired[Sequence[DimensionFieldTypeDef]]
    Columns: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class RadarChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[list[DimensionFieldTypeDef]]
    Color: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]


class RadarChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Color: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class SankeyDiagramAggregatedFieldWellsOutputTypeDef(TypedDict):
    Source: NotRequired[list[DimensionFieldTypeDef]]
    Destination: NotRequired[list[DimensionFieldTypeDef]]
    Weight: NotRequired[list[MeasureFieldTypeDef]]


class SankeyDiagramAggregatedFieldWellsTypeDef(TypedDict):
    Source: NotRequired[Sequence[DimensionFieldTypeDef]]
    Destination: NotRequired[Sequence[DimensionFieldTypeDef]]
    Weight: NotRequired[Sequence[MeasureFieldTypeDef]]


class ScatterPlotCategoricallyAggregatedFieldWellsOutputTypeDef(TypedDict):
    XAxis: NotRequired[list[MeasureFieldTypeDef]]
    YAxis: NotRequired[list[MeasureFieldTypeDef]]
    Category: NotRequired[list[DimensionFieldTypeDef]]
    Size: NotRequired[list[MeasureFieldTypeDef]]
    Label: NotRequired[list[DimensionFieldTypeDef]]


class ScatterPlotCategoricallyAggregatedFieldWellsTypeDef(TypedDict):
    XAxis: NotRequired[Sequence[MeasureFieldTypeDef]]
    YAxis: NotRequired[Sequence[MeasureFieldTypeDef]]
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Size: NotRequired[Sequence[MeasureFieldTypeDef]]
    Label: NotRequired[Sequence[DimensionFieldTypeDef]]


class ScatterPlotUnaggregatedFieldWellsOutputTypeDef(TypedDict):
    XAxis: NotRequired[list[DimensionFieldTypeDef]]
    YAxis: NotRequired[list[DimensionFieldTypeDef]]
    Size: NotRequired[list[MeasureFieldTypeDef]]
    Category: NotRequired[list[DimensionFieldTypeDef]]
    Label: NotRequired[list[DimensionFieldTypeDef]]


class ScatterPlotUnaggregatedFieldWellsTypeDef(TypedDict):
    XAxis: NotRequired[Sequence[DimensionFieldTypeDef]]
    YAxis: NotRequired[Sequence[DimensionFieldTypeDef]]
    Size: NotRequired[Sequence[MeasureFieldTypeDef]]
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Label: NotRequired[Sequence[DimensionFieldTypeDef]]


class TableAggregatedFieldWellsOutputTypeDef(TypedDict):
    GroupBy: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]


class TableAggregatedFieldWellsTypeDef(TypedDict):
    GroupBy: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


TopBottomMoversComputationTypeDef = TypedDict(
    "TopBottomMoversComputationTypeDef",
    {
        "ComputationId": str,
        "Type": TopBottomComputationTypeType,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Category": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "MoverSize": NotRequired[int],
        "SortOrder": NotRequired[TopBottomSortOrderType],
    },
)
TopBottomRankedComputationTypeDef = TypedDict(
    "TopBottomRankedComputationTypeDef",
    {
        "ComputationId": str,
        "Type": TopBottomComputationTypeType,
        "Name": NotRequired[str],
        "Category": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "ResultSize": NotRequired[int],
    },
)


class TotalAggregationComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Value: NotRequired[MeasureFieldTypeDef]


class TreeMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Groups: NotRequired[list[DimensionFieldTypeDef]]
    Sizes: NotRequired[list[MeasureFieldTypeDef]]
    Colors: NotRequired[list[MeasureFieldTypeDef]]


class TreeMapAggregatedFieldWellsTypeDef(TypedDict):
    Groups: NotRequired[Sequence[DimensionFieldTypeDef]]
    Sizes: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[MeasureFieldTypeDef]]


class WaterfallChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Categories: NotRequired[list[DimensionFieldTypeDef]]
    Values: NotRequired[list[MeasureFieldTypeDef]]
    Breakdowns: NotRequired[list[DimensionFieldTypeDef]]


class WaterfallChartAggregatedFieldWellsTypeDef(TypedDict):
    Categories: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Breakdowns: NotRequired[Sequence[DimensionFieldTypeDef]]


class WordCloudAggregatedFieldWellsOutputTypeDef(TypedDict):
    GroupBy: NotRequired[list[DimensionFieldTypeDef]]
    Size: NotRequired[list[MeasureFieldTypeDef]]


class WordCloudAggregatedFieldWellsTypeDef(TypedDict):
    GroupBy: NotRequired[Sequence[DimensionFieldTypeDef]]
    Size: NotRequired[Sequence[MeasureFieldTypeDef]]


class PluginVisualFieldWellOutputTypeDef(TypedDict):
    AxisName: NotRequired[PluginVisualAxisNameType]
    Dimensions: NotRequired[list[DimensionFieldTypeDef]]
    Measures: NotRequired[list[MeasureFieldTypeDef]]
    Unaggregated: NotRequired[list[UnaggregatedFieldTypeDef]]


class PluginVisualFieldWellTypeDef(TypedDict):
    AxisName: NotRequired[PluginVisualAxisNameType]
    Dimensions: NotRequired[Sequence[DimensionFieldTypeDef]]
    Measures: NotRequired[Sequence[MeasureFieldTypeDef]]
    Unaggregated: NotRequired[Sequence[UnaggregatedFieldTypeDef]]


class TableUnaggregatedFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[list[UnaggregatedFieldTypeDef]]


class TableUnaggregatedFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[UnaggregatedFieldTypeDef]]


class BodySectionConfigurationOutputTypeDef(TypedDict):
    SectionId: str
    Content: BodySectionContentOutputTypeDef
    Style: NotRequired[SectionStyleTypeDef]
    PageBreakConfiguration: NotRequired[SectionPageBreakConfigurationTypeDef]
    RepeatConfiguration: NotRequired[BodySectionRepeatConfigurationOutputTypeDef]


class BodySectionConfigurationTypeDef(TypedDict):
    SectionId: str
    Content: BodySectionContentTypeDef
    Style: NotRequired[SectionStyleTypeDef]
    PageBreakConfiguration: NotRequired[SectionPageBreakConfigurationTypeDef]
    RepeatConfiguration: NotRequired[BodySectionRepeatConfigurationTypeDef]


class CreateTopicRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    Topic: TopicDetailsUnionTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]
    FolderArns: NotRequired[Sequence[str]]
    CustomInstructions: NotRequired[CustomInstructionsTypeDef]


class UpdateTopicRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    Topic: TopicDetailsUnionTypeDef
    CustomInstructions: NotRequired[CustomInstructionsTypeDef]


AssetBundleImportJobOverrideParametersUnionTypeDef = Union[
    AssetBundleImportJobOverrideParametersTypeDef,
    AssetBundleImportJobOverrideParametersOutputTypeDef,
]


class DataSourceCredentialsTypeDef(TypedDict):
    CredentialPair: NotRequired[CredentialPairTypeDef]
    CopySourceArn: NotRequired[str]
    SecretArn: NotRequired[str]
    KeyPairCredentials: NotRequired[KeyPairCredentialsTypeDef]
    WebProxyCredentials: NotRequired[WebProxyCredentialsTypeDef]


class SheetImageTypeDef(TypedDict):
    SheetImageId: str
    Source: SheetImageSourceTypeDef
    Scaling: NotRequired[SheetImageScalingConfigurationTypeDef]
    Tooltip: NotRequired[SheetImageTooltipConfigurationTypeDef]
    ImageContentAltText: NotRequired[str]
    Interactions: NotRequired[ImageInteractionOptionsTypeDef]
    Actions: NotRequired[Sequence[ImageCustomActionTypeDef]]


class CustomContentVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[CustomContentConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class EmptyVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]


FilterOperationUnionTypeDef = Union[FilterOperationTypeDef, FilterOperationOutputTypeDef]


class FiltersOperationTypeDef(TypedDict):
    Alias: str
    Source: TransformOperationSourceTypeDef
    FilterOperations: Sequence[FilterOperationTypeDef]


TopicIRContributionAnalysisUnionTypeDef = Union[
    TopicIRContributionAnalysisTypeDef, TopicIRContributionAnalysisOutputTypeDef
]


class SheetTypeDef(TypedDict):
    SheetId: NotRequired[str]
    Name: NotRequired[str]
    Images: NotRequired[list[SheetImageOutputTypeDef]]


class DescribeDataSetResponseTypeDef(TypedDict):
    DataSet: DataSetTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListTopicReviewedAnswersResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    Answers: list[TopicReviewedAnswerTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class InnerFilterOutputTypeDef(TypedDict):
    CategoryInnerFilter: NotRequired[CategoryInnerFilterOutputTypeDef]


class InnerFilterTypeDef(TypedDict):
    CategoryInnerFilter: NotRequired[CategoryInnerFilterTypeDef]


class BarChartFieldWellsOutputTypeDef(TypedDict):
    BarChartAggregatedFieldWells: NotRequired[BarChartAggregatedFieldWellsOutputTypeDef]


class BarChartFieldWellsTypeDef(TypedDict):
    BarChartAggregatedFieldWells: NotRequired[BarChartAggregatedFieldWellsTypeDef]


class BoxPlotFieldWellsOutputTypeDef(TypedDict):
    BoxPlotAggregatedFieldWells: NotRequired[BoxPlotAggregatedFieldWellsOutputTypeDef]


class BoxPlotFieldWellsTypeDef(TypedDict):
    BoxPlotAggregatedFieldWells: NotRequired[BoxPlotAggregatedFieldWellsTypeDef]


class ComboChartFieldWellsOutputTypeDef(TypedDict):
    ComboChartAggregatedFieldWells: NotRequired[ComboChartAggregatedFieldWellsOutputTypeDef]


class ComboChartFieldWellsTypeDef(TypedDict):
    ComboChartAggregatedFieldWells: NotRequired[ComboChartAggregatedFieldWellsTypeDef]


class FilledMapFieldWellsOutputTypeDef(TypedDict):
    FilledMapAggregatedFieldWells: NotRequired[FilledMapAggregatedFieldWellsOutputTypeDef]


class FilledMapFieldWellsTypeDef(TypedDict):
    FilledMapAggregatedFieldWells: NotRequired[FilledMapAggregatedFieldWellsTypeDef]


class FunnelChartFieldWellsOutputTypeDef(TypedDict):
    FunnelChartAggregatedFieldWells: NotRequired[FunnelChartAggregatedFieldWellsOutputTypeDef]


class FunnelChartFieldWellsTypeDef(TypedDict):
    FunnelChartAggregatedFieldWells: NotRequired[FunnelChartAggregatedFieldWellsTypeDef]


class GaugeChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[GaugeChartFieldWellsOutputTypeDef]
    GaugeChartOptions: NotRequired[GaugeChartOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    TooltipOptions: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    ColorConfiguration: NotRequired[GaugeChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class GaugeChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[GaugeChartFieldWellsTypeDef]
    GaugeChartOptions: NotRequired[GaugeChartOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    TooltipOptions: NotRequired[TooltipOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    ColorConfiguration: NotRequired[GaugeChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class GeospatialLayerJoinDefinitionOutputTypeDef(TypedDict):
    ShapeKeyField: NotRequired[str]
    DatasetKeyField: NotRequired[UnaggregatedFieldTypeDef]
    ColorField: NotRequired[GeospatialLayerColorFieldOutputTypeDef]


class GeospatialLayerJoinDefinitionTypeDef(TypedDict):
    ShapeKeyField: NotRequired[str]
    DatasetKeyField: NotRequired[UnaggregatedFieldTypeDef]
    ColorField: NotRequired[GeospatialLayerColorFieldTypeDef]


class GeospatialMapFieldWellsOutputTypeDef(TypedDict):
    GeospatialMapAggregatedFieldWells: NotRequired[GeospatialMapAggregatedFieldWellsOutputTypeDef]


class GeospatialMapFieldWellsTypeDef(TypedDict):
    GeospatialMapAggregatedFieldWells: NotRequired[GeospatialMapAggregatedFieldWellsTypeDef]


class HeatMapFieldWellsOutputTypeDef(TypedDict):
    HeatMapAggregatedFieldWells: NotRequired[HeatMapAggregatedFieldWellsOutputTypeDef]


class HeatMapFieldWellsTypeDef(TypedDict):
    HeatMapAggregatedFieldWells: NotRequired[HeatMapAggregatedFieldWellsTypeDef]


class HistogramFieldWellsOutputTypeDef(TypedDict):
    HistogramAggregatedFieldWells: NotRequired[HistogramAggregatedFieldWellsOutputTypeDef]


class HistogramFieldWellsTypeDef(TypedDict):
    HistogramAggregatedFieldWells: NotRequired[HistogramAggregatedFieldWellsTypeDef]


class KPIConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[KPIFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[KPISortConfigurationOutputTypeDef]
    KPIOptions: NotRequired[KPIOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class KPIConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[KPIFieldWellsTypeDef]
    SortConfiguration: NotRequired[KPISortConfigurationTypeDef]
    KPIOptions: NotRequired[KPIOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class LineChartFieldWellsOutputTypeDef(TypedDict):
    LineChartAggregatedFieldWells: NotRequired[LineChartAggregatedFieldWellsOutputTypeDef]


class LineChartFieldWellsTypeDef(TypedDict):
    LineChartAggregatedFieldWells: NotRequired[LineChartAggregatedFieldWellsTypeDef]


class PieChartFieldWellsOutputTypeDef(TypedDict):
    PieChartAggregatedFieldWells: NotRequired[PieChartAggregatedFieldWellsOutputTypeDef]


class PieChartFieldWellsTypeDef(TypedDict):
    PieChartAggregatedFieldWells: NotRequired[PieChartAggregatedFieldWellsTypeDef]


class PivotTableFieldWellsOutputTypeDef(TypedDict):
    PivotTableAggregatedFieldWells: NotRequired[PivotTableAggregatedFieldWellsOutputTypeDef]


class PivotTableFieldWellsTypeDef(TypedDict):
    PivotTableAggregatedFieldWells: NotRequired[PivotTableAggregatedFieldWellsTypeDef]


class RadarChartFieldWellsOutputTypeDef(TypedDict):
    RadarChartAggregatedFieldWells: NotRequired[RadarChartAggregatedFieldWellsOutputTypeDef]


class RadarChartFieldWellsTypeDef(TypedDict):
    RadarChartAggregatedFieldWells: NotRequired[RadarChartAggregatedFieldWellsTypeDef]


class SankeyDiagramFieldWellsOutputTypeDef(TypedDict):
    SankeyDiagramAggregatedFieldWells: NotRequired[SankeyDiagramAggregatedFieldWellsOutputTypeDef]


class SankeyDiagramFieldWellsTypeDef(TypedDict):
    SankeyDiagramAggregatedFieldWells: NotRequired[SankeyDiagramAggregatedFieldWellsTypeDef]


class ScatterPlotFieldWellsOutputTypeDef(TypedDict):
    ScatterPlotCategoricallyAggregatedFieldWells: NotRequired[
        ScatterPlotCategoricallyAggregatedFieldWellsOutputTypeDef
    ]
    ScatterPlotUnaggregatedFieldWells: NotRequired[ScatterPlotUnaggregatedFieldWellsOutputTypeDef]


class ScatterPlotFieldWellsTypeDef(TypedDict):
    ScatterPlotCategoricallyAggregatedFieldWells: NotRequired[
        ScatterPlotCategoricallyAggregatedFieldWellsTypeDef
    ]
    ScatterPlotUnaggregatedFieldWells: NotRequired[ScatterPlotUnaggregatedFieldWellsTypeDef]


class ComputationTypeDef(TypedDict):
    TopBottomRanked: NotRequired[TopBottomRankedComputationTypeDef]
    TopBottomMovers: NotRequired[TopBottomMoversComputationTypeDef]
    TotalAggregation: NotRequired[TotalAggregationComputationTypeDef]
    MaximumMinimum: NotRequired[MaximumMinimumComputationTypeDef]
    MetricComparison: NotRequired[MetricComparisonComputationTypeDef]
    PeriodOverPeriod: NotRequired[PeriodOverPeriodComputationTypeDef]
    PeriodToDate: NotRequired[PeriodToDateComputationTypeDef]
    GrowthRate: NotRequired[GrowthRateComputationTypeDef]
    UniqueValues: NotRequired[UniqueValuesComputationTypeDef]
    Forecast: NotRequired[ForecastComputationTypeDef]


class TreeMapFieldWellsOutputTypeDef(TypedDict):
    TreeMapAggregatedFieldWells: NotRequired[TreeMapAggregatedFieldWellsOutputTypeDef]


class TreeMapFieldWellsTypeDef(TypedDict):
    TreeMapAggregatedFieldWells: NotRequired[TreeMapAggregatedFieldWellsTypeDef]


class WaterfallChartFieldWellsOutputTypeDef(TypedDict):
    WaterfallChartAggregatedFieldWells: NotRequired[WaterfallChartAggregatedFieldWellsOutputTypeDef]


class WaterfallChartFieldWellsTypeDef(TypedDict):
    WaterfallChartAggregatedFieldWells: NotRequired[WaterfallChartAggregatedFieldWellsTypeDef]


class WordCloudFieldWellsOutputTypeDef(TypedDict):
    WordCloudAggregatedFieldWells: NotRequired[WordCloudAggregatedFieldWellsOutputTypeDef]


class WordCloudFieldWellsTypeDef(TypedDict):
    WordCloudAggregatedFieldWells: NotRequired[WordCloudAggregatedFieldWellsTypeDef]


class PluginVisualConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[list[PluginVisualFieldWellOutputTypeDef]]
    VisualOptions: NotRequired[PluginVisualOptionsOutputTypeDef]
    SortConfiguration: NotRequired[PluginVisualSortConfigurationOutputTypeDef]


class PluginVisualConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[Sequence[PluginVisualFieldWellTypeDef]]
    VisualOptions: NotRequired[PluginVisualOptionsTypeDef]
    SortConfiguration: NotRequired[PluginVisualSortConfigurationTypeDef]


class TableFieldWellsOutputTypeDef(TypedDict):
    TableAggregatedFieldWells: NotRequired[TableAggregatedFieldWellsOutputTypeDef]
    TableUnaggregatedFieldWells: NotRequired[TableUnaggregatedFieldWellsOutputTypeDef]


class TableFieldWellsTypeDef(TypedDict):
    TableAggregatedFieldWells: NotRequired[TableAggregatedFieldWellsTypeDef]
    TableUnaggregatedFieldWells: NotRequired[TableUnaggregatedFieldWellsTypeDef]


class SectionBasedLayoutConfigurationOutputTypeDef(TypedDict):
    HeaderSections: list[HeaderFooterSectionConfigurationOutputTypeDef]
    BodySections: list[BodySectionConfigurationOutputTypeDef]
    FooterSections: list[HeaderFooterSectionConfigurationOutputTypeDef]
    CanvasSizeOptions: SectionBasedLayoutCanvasSizeOptionsTypeDef


class SectionBasedLayoutConfigurationTypeDef(TypedDict):
    HeaderSections: Sequence[HeaderFooterSectionConfigurationTypeDef]
    BodySections: Sequence[BodySectionConfigurationTypeDef]
    FooterSections: Sequence[HeaderFooterSectionConfigurationTypeDef]
    CanvasSizeOptions: SectionBasedLayoutCanvasSizeOptionsTypeDef


class StartAssetBundleImportJobRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleImportJobId: str
    AssetBundleImportSource: AssetBundleImportSourceTypeDef
    OverrideParameters: NotRequired[AssetBundleImportJobOverrideParametersUnionTypeDef]
    FailureAction: NotRequired[AssetBundleImportFailureActionType]
    OverridePermissions: NotRequired[AssetBundleImportJobOverridePermissionsUnionTypeDef]
    OverrideTags: NotRequired[AssetBundleImportJobOverrideTagsUnionTypeDef]
    OverrideValidationStrategy: NotRequired[AssetBundleImportJobOverrideValidationStrategyTypeDef]


CreateDataSourceRequestTypeDef = TypedDict(
    "CreateDataSourceRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "DataSourceParameters": NotRequired[DataSourceParametersUnionTypeDef],
        "Credentials": NotRequired[DataSourceCredentialsTypeDef],
        "Permissions": NotRequired[Sequence[ResourcePermissionUnionTypeDef]],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "FolderArns": NotRequired[Sequence[str]],
    },
)


class UpdateDataSourceRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str
    Name: str
    DataSourceParameters: NotRequired[DataSourceParametersUnionTypeDef]
    Credentials: NotRequired[DataSourceCredentialsTypeDef]
    VpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    SslProperties: NotRequired[SslPropertiesTypeDef]


class TransformOperationTypeDef(TypedDict):
    ProjectOperation: NotRequired[ProjectOperationUnionTypeDef]
    FilterOperation: NotRequired[FilterOperationUnionTypeDef]
    CreateColumnsOperation: NotRequired[CreateColumnsOperationUnionTypeDef]
    RenameColumnOperation: NotRequired[RenameColumnOperationTypeDef]
    CastColumnTypeOperation: NotRequired[CastColumnTypeOperationTypeDef]
    TagColumnOperation: NotRequired[TagColumnOperationUnionTypeDef]
    UntagColumnOperation: NotRequired[UntagColumnOperationUnionTypeDef]
    OverrideDatasetParameterOperation: NotRequired[OverrideDatasetParameterOperationUnionTypeDef]


class TransformStepTypeDef(TypedDict):
    ImportTableStep: NotRequired[ImportTableOperationTypeDef]
    ProjectStep: NotRequired[ProjectOperationTypeDef]
    FiltersStep: NotRequired[FiltersOperationTypeDef]
    CreateColumnsStep: NotRequired[CreateColumnsOperationTypeDef]
    RenameColumnsStep: NotRequired[RenameColumnsOperationTypeDef]
    CastColumnTypesStep: NotRequired[CastColumnTypesOperationTypeDef]
    JoinStep: NotRequired[JoinOperationTypeDef]
    AggregateStep: NotRequired[AggregateOperationTypeDef]
    PivotStep: NotRequired[PivotOperationTypeDef]
    UnpivotStep: NotRequired[UnpivotOperationTypeDef]
    AppendStep: NotRequired[AppendOperationTypeDef]


class TopicIRTypeDef(TypedDict):
    Metrics: NotRequired[Sequence[TopicIRMetricUnionTypeDef]]
    GroupByList: NotRequired[Sequence[TopicIRGroupByTypeDef]]
    Filters: NotRequired[Sequence[Sequence[TopicIRFilterOptionUnionTypeDef]]]
    Sort: NotRequired[TopicSortClauseTypeDef]
    ContributionAnalysis: NotRequired[TopicIRContributionAnalysisUnionTypeDef]
    Visual: NotRequired[VisualOptionsTypeDef]


class AnalysisTypeDef(TypedDict):
    AnalysisId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ResourceStatusType]
    Errors: NotRequired[list[AnalysisErrorTypeDef]]
    DataSetArns: NotRequired[list[str]]
    ThemeArn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    Sheets: NotRequired[list[SheetTypeDef]]


class DashboardVersionTypeDef(TypedDict):
    CreatedTime: NotRequired[datetime]
    Errors: NotRequired[list[DashboardErrorTypeDef]]
    VersionNumber: NotRequired[int]
    Status: NotRequired[ResourceStatusType]
    Arn: NotRequired[str]
    SourceEntityArn: NotRequired[str]
    DataSetArns: NotRequired[list[str]]
    Description: NotRequired[str]
    ThemeArn: NotRequired[str]
    Sheets: NotRequired[list[SheetTypeDef]]


class TemplateVersionTypeDef(TypedDict):
    CreatedTime: NotRequired[datetime]
    Errors: NotRequired[list[TemplateErrorTypeDef]]
    VersionNumber: NotRequired[int]
    Status: NotRequired[ResourceStatusType]
    DataSetConfigurations: NotRequired[list[DataSetConfigurationOutputTypeDef]]
    Description: NotRequired[str]
    SourceEntityArn: NotRequired[str]
    ThemeArn: NotRequired[str]
    Sheets: NotRequired[list[SheetTypeDef]]


class NestedFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    IncludeInnerSet: bool
    InnerFilter: InnerFilterOutputTypeDef


class NestedFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    IncludeInnerSet: bool
    InnerFilter: InnerFilterTypeDef


class BarChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[BarChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[BarChartSortConfigurationOutputTypeDef]
    Orientation: NotRequired[BarChartOrientationType]
    BarsArrangement: NotRequired[BarsArrangementType]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ValueAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    DefaultSeriesSettings: NotRequired[BarChartDefaultSeriesSettingsTypeDef]
    Series: NotRequired[list[BarSeriesItemTypeDef]]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    ReferenceLines: NotRequired[list[ReferenceLineTypeDef]]
    ContributionAnalysisDefaults: NotRequired[list[ContributionAnalysisDefaultOutputTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class BarChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[BarChartFieldWellsTypeDef]
    SortConfiguration: NotRequired[BarChartSortConfigurationTypeDef]
    Orientation: NotRequired[BarChartOrientationType]
    BarsArrangement: NotRequired[BarsArrangementType]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ValueAxis: NotRequired[AxisDisplayOptionsTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    DefaultSeriesSettings: NotRequired[BarChartDefaultSeriesSettingsTypeDef]
    Series: NotRequired[Sequence[BarSeriesItemTypeDef]]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    ReferenceLines: NotRequired[Sequence[ReferenceLineTypeDef]]
    ContributionAnalysisDefaults: NotRequired[Sequence[ContributionAnalysisDefaultTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class BoxPlotChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[BoxPlotFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[BoxPlotSortConfigurationOutputTypeDef]
    BoxPlotOptions: NotRequired[BoxPlotOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    ReferenceLines: NotRequired[list[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class BoxPlotChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[BoxPlotFieldWellsTypeDef]
    SortConfiguration: NotRequired[BoxPlotSortConfigurationTypeDef]
    BoxPlotOptions: NotRequired[BoxPlotOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    ReferenceLines: NotRequired[Sequence[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ComboChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[ComboChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[ComboChartSortConfigurationOutputTypeDef]
    BarsArrangement: NotRequired[BarsArrangementType]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    SecondaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    SecondaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    SingleAxisOptions: NotRequired[SingleAxisOptionsTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    DefaultSeriesSettings: NotRequired[ComboChartDefaultSeriesSettingsTypeDef]
    Series: NotRequired[list[ComboSeriesItemTypeDef]]
    Legend: NotRequired[LegendOptionsTypeDef]
    BarDataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    LineDataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    ReferenceLines: NotRequired[list[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ComboChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[ComboChartFieldWellsTypeDef]
    SortConfiguration: NotRequired[ComboChartSortConfigurationTypeDef]
    BarsArrangement: NotRequired[BarsArrangementType]
    CategoryAxis: NotRequired[AxisDisplayOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    SecondaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    SecondaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    SingleAxisOptions: NotRequired[SingleAxisOptionsTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    DefaultSeriesSettings: NotRequired[ComboChartDefaultSeriesSettingsTypeDef]
    Series: NotRequired[Sequence[ComboSeriesItemTypeDef]]
    Legend: NotRequired[LegendOptionsTypeDef]
    BarDataLabels: NotRequired[DataLabelOptionsTypeDef]
    LineDataLabels: NotRequired[DataLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    ReferenceLines: NotRequired[Sequence[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FilledMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[FilledMapFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[FilledMapSortConfigurationOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FilledMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[FilledMapFieldWellsTypeDef]
    SortConfiguration: NotRequired[FilledMapSortConfigurationTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FunnelChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[FunnelChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[FunnelChartSortConfigurationOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    DataLabelOptions: NotRequired[FunnelChartDataLabelOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FunnelChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[FunnelChartFieldWellsTypeDef]
    SortConfiguration: NotRequired[FunnelChartSortConfigurationTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    DataLabelOptions: NotRequired[FunnelChartDataLabelOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class GaugeChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GaugeChartConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[GaugeChartConditionalFormattingOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class GaugeChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GaugeChartConfigurationTypeDef]
    ConditionalFormatting: NotRequired[GaugeChartConditionalFormattingTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class GeospatialLayerItemOutputTypeDef(TypedDict):
    LayerId: str
    LayerType: NotRequired[GeospatialLayerTypeType]
    DataSource: NotRequired[GeospatialDataSourceItemTypeDef]
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    LayerDefinition: NotRequired[GeospatialLayerDefinitionOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    JoinDefinition: NotRequired[GeospatialLayerJoinDefinitionOutputTypeDef]
    Actions: NotRequired[list[LayerCustomActionOutputTypeDef]]


class GeospatialLayerItemTypeDef(TypedDict):
    LayerId: str
    LayerType: NotRequired[GeospatialLayerTypeType]
    DataSource: NotRequired[GeospatialDataSourceItemTypeDef]
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    LayerDefinition: NotRequired[GeospatialLayerDefinitionTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    JoinDefinition: NotRequired[GeospatialLayerJoinDefinitionTypeDef]
    Actions: NotRequired[Sequence[LayerCustomActionTypeDef]]


class GeospatialMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[GeospatialMapFieldWellsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    PointStyleOptions: NotRequired[GeospatialPointStyleOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class GeospatialMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[GeospatialMapFieldWellsTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    PointStyleOptions: NotRequired[GeospatialPointStyleOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HeatMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[HeatMapFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[HeatMapSortConfigurationOutputTypeDef]
    RowAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    RowLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColumnAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    ColumnLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorScale: NotRequired[ColorScaleOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HeatMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[HeatMapFieldWellsTypeDef]
    SortConfiguration: NotRequired[HeatMapSortConfigurationTypeDef]
    RowAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    RowLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ColumnAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    ColumnLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ColorScale: NotRequired[ColorScaleTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HistogramConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[HistogramFieldWellsOutputTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    BinOptions: NotRequired[HistogramBinOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HistogramConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[HistogramFieldWellsTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    BinOptions: NotRequired[HistogramBinOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class KPIVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[KPIConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[KPIConditionalFormattingOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class KPIVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[KPIConfigurationTypeDef]
    ConditionalFormatting: NotRequired[KPIConditionalFormattingTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


LineChartConfigurationOutputTypeDef = TypedDict(
    "LineChartConfigurationOutputTypeDef",
    {
        "FieldWells": NotRequired[LineChartFieldWellsOutputTypeDef],
        "SortConfiguration": NotRequired[LineChartSortConfigurationOutputTypeDef],
        "ForecastConfigurations": NotRequired[list[ForecastConfigurationOutputTypeDef]],
        "Type": NotRequired[LineChartTypeType],
        "SmallMultiplesOptions": NotRequired[SmallMultiplesOptionsTypeDef],
        "XAxisDisplayOptions": NotRequired[AxisDisplayOptionsOutputTypeDef],
        "XAxisLabelOptions": NotRequired[ChartAxisLabelOptionsOutputTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsOutputTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsOutputTypeDef],
        "SecondaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsOutputTypeDef],
        "SecondaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsOutputTypeDef],
        "SingleAxisOptions": NotRequired[SingleAxisOptionsTypeDef],
        "DefaultSeriesSettings": NotRequired[LineChartDefaultSeriesSettingsTypeDef],
        "Series": NotRequired[list[SeriesItemTypeDef]],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsOutputTypeDef],
        "ReferenceLines": NotRequired[list[ReferenceLineTypeDef]],
        "Tooltip": NotRequired[TooltipOptionsOutputTypeDef],
        "ContributionAnalysisDefaults": NotRequired[list[ContributionAnalysisDefaultOutputTypeDef]],
        "VisualPalette": NotRequired[VisualPaletteOutputTypeDef],
        "Interactions": NotRequired[VisualInteractionOptionsTypeDef],
    },
)
LineChartConfigurationTypeDef = TypedDict(
    "LineChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[LineChartFieldWellsTypeDef],
        "SortConfiguration": NotRequired[LineChartSortConfigurationTypeDef],
        "ForecastConfigurations": NotRequired[Sequence[ForecastConfigurationTypeDef]],
        "Type": NotRequired[LineChartTypeType],
        "SmallMultiplesOptions": NotRequired[SmallMultiplesOptionsTypeDef],
        "XAxisDisplayOptions": NotRequired[AxisDisplayOptionsTypeDef],
        "XAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "SecondaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsTypeDef],
        "SecondaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsTypeDef],
        "SingleAxisOptions": NotRequired[SingleAxisOptionsTypeDef],
        "DefaultSeriesSettings": NotRequired[LineChartDefaultSeriesSettingsTypeDef],
        "Series": NotRequired[Sequence[SeriesItemTypeDef]],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsTypeDef],
        "ReferenceLines": NotRequired[Sequence[ReferenceLineTypeDef]],
        "Tooltip": NotRequired[TooltipOptionsTypeDef],
        "ContributionAnalysisDefaults": NotRequired[Sequence[ContributionAnalysisDefaultTypeDef]],
        "VisualPalette": NotRequired[VisualPaletteTypeDef],
        "Interactions": NotRequired[VisualInteractionOptionsTypeDef],
    },
)


class PieChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[PieChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[PieChartSortConfigurationOutputTypeDef]
    DonutOptions: NotRequired[DonutOptionsTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    ContributionAnalysisDefaults: NotRequired[list[ContributionAnalysisDefaultOutputTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PieChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[PieChartFieldWellsTypeDef]
    SortConfiguration: NotRequired[PieChartSortConfigurationTypeDef]
    DonutOptions: NotRequired[DonutOptionsTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    ContributionAnalysisDefaults: NotRequired[Sequence[ContributionAnalysisDefaultTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PivotTableConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[PivotTableFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[PivotTableSortConfigurationOutputTypeDef]
    TableOptions: NotRequired[PivotTableOptionsOutputTypeDef]
    TotalOptions: NotRequired[PivotTableTotalOptionsOutputTypeDef]
    FieldOptions: NotRequired[PivotTableFieldOptionsOutputTypeDef]
    PaginatedReportOptions: NotRequired[PivotTablePaginatedReportOptionsTypeDef]
    DashboardCustomizationVisualOptions: NotRequired[
        DashboardCustomizationVisualOptionsOutputTypeDef
    ]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PivotTableConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[PivotTableFieldWellsTypeDef]
    SortConfiguration: NotRequired[PivotTableSortConfigurationTypeDef]
    TableOptions: NotRequired[PivotTableOptionsTypeDef]
    TotalOptions: NotRequired[PivotTableTotalOptionsTypeDef]
    FieldOptions: NotRequired[PivotTableFieldOptionsTypeDef]
    PaginatedReportOptions: NotRequired[PivotTablePaginatedReportOptionsTypeDef]
    DashboardCustomizationVisualOptions: NotRequired[DashboardCustomizationVisualOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class RadarChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[RadarChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[RadarChartSortConfigurationOutputTypeDef]
    Shape: NotRequired[RadarChartShapeType]
    BaseSeriesSettings: NotRequired[RadarChartSeriesSettingsTypeDef]
    StartAngle: NotRequired[float]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    AlternateBandColorsVisibility: NotRequired[VisibilityType]
    AlternateBandEvenColor: NotRequired[str]
    AlternateBandOddColor: NotRequired[str]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    AxesRangeScale: NotRequired[RadarChartAxesRangeScaleType]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class RadarChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[RadarChartFieldWellsTypeDef]
    SortConfiguration: NotRequired[RadarChartSortConfigurationTypeDef]
    Shape: NotRequired[RadarChartShapeType]
    BaseSeriesSettings: NotRequired[RadarChartSeriesSettingsTypeDef]
    StartAngle: NotRequired[float]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    AlternateBandColorsVisibility: NotRequired[VisibilityType]
    AlternateBandEvenColor: NotRequired[str]
    AlternateBandOddColor: NotRequired[str]
    CategoryAxis: NotRequired[AxisDisplayOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ColorAxis: NotRequired[AxisDisplayOptionsTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    AxesRangeScale: NotRequired[RadarChartAxesRangeScaleType]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class SankeyDiagramChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[SankeyDiagramFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[SankeyDiagramSortConfigurationOutputTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class SankeyDiagramChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[SankeyDiagramFieldWellsTypeDef]
    SortConfiguration: NotRequired[SankeyDiagramSortConfigurationTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ScatterPlotConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[ScatterPlotFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[ScatterPlotSortConfigurationTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    YAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ScatterPlotConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[ScatterPlotFieldWellsTypeDef]
    SortConfiguration: NotRequired[ScatterPlotSortConfigurationTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    YAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class InsightConfigurationOutputTypeDef(TypedDict):
    Computations: NotRequired[list[ComputationTypeDef]]
    CustomNarrative: NotRequired[CustomNarrativeOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class InsightConfigurationTypeDef(TypedDict):
    Computations: NotRequired[Sequence[ComputationTypeDef]]
    CustomNarrative: NotRequired[CustomNarrativeOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TreeMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[TreeMapFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[TreeMapSortConfigurationOutputTypeDef]
    GroupLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    SizeLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorScale: NotRequired[ColorScaleOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TreeMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[TreeMapFieldWellsTypeDef]
    SortConfiguration: NotRequired[TreeMapSortConfigurationTypeDef]
    GroupLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    SizeLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    ColorScale: NotRequired[ColorScaleTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WaterfallChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[WaterfallChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[WaterfallChartSortConfigurationOutputTypeDef]
    WaterfallChartOptions: NotRequired[WaterfallChartOptionsTypeDef]
    CategoryAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    CategoryAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    ColorConfiguration: NotRequired[WaterfallChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WaterfallChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[WaterfallChartFieldWellsTypeDef]
    SortConfiguration: NotRequired[WaterfallChartSortConfigurationTypeDef]
    WaterfallChartOptions: NotRequired[WaterfallChartOptionsTypeDef]
    CategoryAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    CategoryAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteTypeDef]
    ColorConfiguration: NotRequired[WaterfallChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WordCloudChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[WordCloudFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[WordCloudSortConfigurationOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    WordCloudOptions: NotRequired[WordCloudOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WordCloudChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[WordCloudFieldWellsTypeDef]
    SortConfiguration: NotRequired[WordCloudSortConfigurationTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsTypeDef]
    WordCloudOptions: NotRequired[WordCloudOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PluginVisualOutputTypeDef(TypedDict):
    VisualId: str
    PluginArn: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PluginVisualConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class PluginVisualTypeDef(TypedDict):
    VisualId: str
    PluginArn: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PluginVisualConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class TableConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[TableFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[TableSortConfigurationOutputTypeDef]
    TableOptions: NotRequired[TableOptionsOutputTypeDef]
    TotalOptions: NotRequired[TotalOptionsOutputTypeDef]
    FieldOptions: NotRequired[TableFieldOptionsOutputTypeDef]
    PaginatedReportOptions: NotRequired[TablePaginatedReportOptionsTypeDef]
    TableInlineVisualizations: NotRequired[list[TableInlineVisualizationTypeDef]]
    DashboardCustomizationVisualOptions: NotRequired[
        DashboardCustomizationVisualOptionsOutputTypeDef
    ]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TableConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[TableFieldWellsTypeDef]
    SortConfiguration: NotRequired[TableSortConfigurationTypeDef]
    TableOptions: NotRequired[TableOptionsTypeDef]
    TotalOptions: NotRequired[TotalOptionsTypeDef]
    FieldOptions: NotRequired[TableFieldOptionsTypeDef]
    PaginatedReportOptions: NotRequired[TablePaginatedReportOptionsTypeDef]
    TableInlineVisualizations: NotRequired[Sequence[TableInlineVisualizationTypeDef]]
    DashboardCustomizationVisualOptions: NotRequired[DashboardCustomizationVisualOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class LayoutConfigurationOutputTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationOutputTypeDef]
    FreeFormLayout: NotRequired[FreeFormLayoutConfigurationOutputTypeDef]
    SectionBasedLayout: NotRequired[SectionBasedLayoutConfigurationOutputTypeDef]


class LayoutConfigurationTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationTypeDef]
    FreeFormLayout: NotRequired[FreeFormLayoutConfigurationTypeDef]
    SectionBasedLayout: NotRequired[SectionBasedLayoutConfigurationTypeDef]


TransformOperationUnionTypeDef = Union[TransformOperationTypeDef, TransformOperationOutputTypeDef]


class DataPrepConfigurationTypeDef(TypedDict):
    SourceTableMap: Mapping[str, SourceTableTypeDef]
    TransformStepMap: Mapping[str, TransformStepTypeDef]
    DestinationTableMap: Mapping[str, DestinationTableTypeDef]


TopicIRUnionTypeDef = Union[TopicIRTypeDef, TopicIROutputTypeDef]


class DescribeAnalysisResponseTypeDef(TypedDict):
    Analysis: AnalysisTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DashboardTypeDef(TypedDict):
    DashboardId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[DashboardVersionTypeDef]
    CreatedTime: NotRequired[datetime]
    LastPublishedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    LinkEntities: NotRequired[list[str]]


class TemplateTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[TemplateVersionTypeDef]
    TemplateId: NotRequired[str]
    LastUpdatedTime: NotRequired[datetime]
    CreatedTime: NotRequired[datetime]


class FilterOutputTypeDef(TypedDict):
    CategoryFilter: NotRequired[CategoryFilterOutputTypeDef]
    NumericRangeFilter: NotRequired[NumericRangeFilterOutputTypeDef]
    NumericEqualityFilter: NotRequired[NumericEqualityFilterOutputTypeDef]
    TimeEqualityFilter: NotRequired[TimeEqualityFilterOutputTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeFilterOutputTypeDef]
    RelativeDatesFilter: NotRequired[RelativeDatesFilterOutputTypeDef]
    TopBottomFilter: NotRequired[TopBottomFilterOutputTypeDef]
    NestedFilter: NotRequired[NestedFilterOutputTypeDef]


class FilterTypeDef(TypedDict):
    CategoryFilter: NotRequired[CategoryFilterTypeDef]
    NumericRangeFilter: NotRequired[NumericRangeFilterTypeDef]
    NumericEqualityFilter: NotRequired[NumericEqualityFilterTypeDef]
    TimeEqualityFilter: NotRequired[TimeEqualityFilterTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeFilterTypeDef]
    RelativeDatesFilter: NotRequired[RelativeDatesFilterTypeDef]
    TopBottomFilter: NotRequired[TopBottomFilterTypeDef]
    NestedFilter: NotRequired[NestedFilterTypeDef]


class BarChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BarChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class BarChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BarChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class BoxPlotVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BoxPlotChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class BoxPlotVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BoxPlotChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class ComboChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ComboChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class ComboChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ComboChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class FilledMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FilledMapConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[FilledMapConditionalFormattingOutputTypeDef]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]
    GeocodingPreferences: NotRequired[list[GeocodePreferenceTypeDef]]


class FilledMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FilledMapConfigurationTypeDef]
    ConditionalFormatting: NotRequired[FilledMapConditionalFormattingTypeDef]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]
    GeocodingPreferences: NotRequired[Sequence[GeocodePreferenceTypeDef]]


class FunnelChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FunnelChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class FunnelChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FunnelChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class GeospatialLayerMapConfigurationOutputTypeDef(TypedDict):
    Legend: NotRequired[LegendOptionsTypeDef]
    MapLayers: NotRequired[list[GeospatialLayerItemOutputTypeDef]]
    MapState: NotRequired[GeospatialMapStateTypeDef]
    MapStyle: NotRequired[GeospatialMapStyleTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class GeospatialLayerMapConfigurationTypeDef(TypedDict):
    Legend: NotRequired[LegendOptionsTypeDef]
    MapLayers: NotRequired[Sequence[GeospatialLayerItemTypeDef]]
    MapState: NotRequired[GeospatialMapStateTypeDef]
    MapStyle: NotRequired[GeospatialMapStyleTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class GeospatialMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialMapConfigurationOutputTypeDef]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]
    GeocodingPreferences: NotRequired[list[GeocodePreferenceTypeDef]]


class GeospatialMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialMapConfigurationTypeDef]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]
    GeocodingPreferences: NotRequired[Sequence[GeocodePreferenceTypeDef]]


class HeatMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HeatMapConfigurationOutputTypeDef]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class HeatMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HeatMapConfigurationTypeDef]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class HistogramVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HistogramConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class HistogramVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HistogramConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class LineChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[LineChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class LineChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[LineChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class PieChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PieChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class PieChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PieChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class PivotTableVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PivotTableConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[PivotTableConditionalFormattingOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class PivotTableVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PivotTableConfigurationTypeDef]
    ConditionalFormatting: NotRequired[PivotTableConditionalFormattingTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class RadarChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[RadarChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class RadarChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[RadarChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class SankeyDiagramVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[SankeyDiagramChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class SankeyDiagramVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[SankeyDiagramChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class ScatterPlotVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ScatterPlotConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class ScatterPlotVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ScatterPlotConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class InsightVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    InsightConfiguration: NotRequired[InsightConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class InsightVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    InsightConfiguration: NotRequired[InsightConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class TreeMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TreeMapConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class TreeMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TreeMapConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class WaterfallVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WaterfallChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class WaterfallVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WaterfallChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class WordCloudVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WordCloudChartConfigurationOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[list[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class WordCloudVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WordCloudChartConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class TableVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TableConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[TableConditionalFormattingOutputTypeDef]
    Actions: NotRequired[list[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class TableVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TableConfigurationTypeDef]
    ConditionalFormatting: NotRequired[TableConditionalFormattingTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class LayoutOutputTypeDef(TypedDict):
    Configuration: LayoutConfigurationOutputTypeDef


class LayoutTypeDef(TypedDict):
    Configuration: LayoutConfigurationTypeDef


class LogicalTableTypeDef(TypedDict):
    Alias: str
    Source: LogicalTableSourceTypeDef
    DataTransforms: NotRequired[Sequence[TransformOperationUnionTypeDef]]


DataPrepConfigurationUnionTypeDef = Union[
    DataPrepConfigurationTypeDef, DataPrepConfigurationOutputTypeDef
]


class TopicVisualTypeDef(TypedDict):
    VisualId: NotRequired[str]
    Role: NotRequired[VisualRoleType]
    Ir: NotRequired[TopicIRUnionTypeDef]
    SupportingVisuals: NotRequired[Sequence[Mapping[str, Any]]]


class DescribeDashboardResponseTypeDef(TypedDict):
    Dashboard: DashboardTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTemplateResponseTypeDef(TypedDict):
    Template: TemplateTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class FilterGroupOutputTypeDef(TypedDict):
    FilterGroupId: str
    Filters: list[FilterOutputTypeDef]
    ScopeConfiguration: FilterScopeConfigurationOutputTypeDef
    CrossDataset: CrossDatasetTypesType
    Status: NotRequired[WidgetStatusType]


class FilterGroupTypeDef(TypedDict):
    FilterGroupId: str
    Filters: Sequence[FilterTypeDef]
    ScopeConfiguration: FilterScopeConfigurationTypeDef
    CrossDataset: CrossDatasetTypesType
    Status: NotRequired[WidgetStatusType]


class LayerMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialLayerMapConfigurationOutputTypeDef]
    VisualContentAltText: NotRequired[str]


class LayerMapVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialLayerMapConfigurationTypeDef]
    VisualContentAltText: NotRequired[str]


LogicalTableUnionTypeDef = Union[LogicalTableTypeDef, LogicalTableOutputTypeDef]
TopicVisualUnionTypeDef = Union[TopicVisualTypeDef, TopicVisualOutputTypeDef]


class VisualOutputTypeDef(TypedDict):
    TableVisual: NotRequired[TableVisualOutputTypeDef]
    PivotTableVisual: NotRequired[PivotTableVisualOutputTypeDef]
    BarChartVisual: NotRequired[BarChartVisualOutputTypeDef]
    KPIVisual: NotRequired[KPIVisualOutputTypeDef]
    PieChartVisual: NotRequired[PieChartVisualOutputTypeDef]
    GaugeChartVisual: NotRequired[GaugeChartVisualOutputTypeDef]
    LineChartVisual: NotRequired[LineChartVisualOutputTypeDef]
    HeatMapVisual: NotRequired[HeatMapVisualOutputTypeDef]
    TreeMapVisual: NotRequired[TreeMapVisualOutputTypeDef]
    GeospatialMapVisual: NotRequired[GeospatialMapVisualOutputTypeDef]
    FilledMapVisual: NotRequired[FilledMapVisualOutputTypeDef]
    LayerMapVisual: NotRequired[LayerMapVisualOutputTypeDef]
    FunnelChartVisual: NotRequired[FunnelChartVisualOutputTypeDef]
    ScatterPlotVisual: NotRequired[ScatterPlotVisualOutputTypeDef]
    ComboChartVisual: NotRequired[ComboChartVisualOutputTypeDef]
    BoxPlotVisual: NotRequired[BoxPlotVisualOutputTypeDef]
    WaterfallVisual: NotRequired[WaterfallVisualOutputTypeDef]
    HistogramVisual: NotRequired[HistogramVisualOutputTypeDef]
    WordCloudVisual: NotRequired[WordCloudVisualOutputTypeDef]
    InsightVisual: NotRequired[InsightVisualOutputTypeDef]
    SankeyDiagramVisual: NotRequired[SankeyDiagramVisualOutputTypeDef]
    CustomContentVisual: NotRequired[CustomContentVisualOutputTypeDef]
    EmptyVisual: NotRequired[EmptyVisualOutputTypeDef]
    RadarChartVisual: NotRequired[RadarChartVisualOutputTypeDef]
    PluginVisual: NotRequired[PluginVisualOutputTypeDef]


class VisualTypeDef(TypedDict):
    TableVisual: NotRequired[TableVisualTypeDef]
    PivotTableVisual: NotRequired[PivotTableVisualTypeDef]
    BarChartVisual: NotRequired[BarChartVisualTypeDef]
    KPIVisual: NotRequired[KPIVisualTypeDef]
    PieChartVisual: NotRequired[PieChartVisualTypeDef]
    GaugeChartVisual: NotRequired[GaugeChartVisualTypeDef]
    LineChartVisual: NotRequired[LineChartVisualTypeDef]
    HeatMapVisual: NotRequired[HeatMapVisualTypeDef]
    TreeMapVisual: NotRequired[TreeMapVisualTypeDef]
    GeospatialMapVisual: NotRequired[GeospatialMapVisualTypeDef]
    FilledMapVisual: NotRequired[FilledMapVisualTypeDef]
    LayerMapVisual: NotRequired[LayerMapVisualTypeDef]
    FunnelChartVisual: NotRequired[FunnelChartVisualTypeDef]
    ScatterPlotVisual: NotRequired[ScatterPlotVisualTypeDef]
    ComboChartVisual: NotRequired[ComboChartVisualTypeDef]
    BoxPlotVisual: NotRequired[BoxPlotVisualTypeDef]
    WaterfallVisual: NotRequired[WaterfallVisualTypeDef]
    HistogramVisual: NotRequired[HistogramVisualTypeDef]
    WordCloudVisual: NotRequired[WordCloudVisualTypeDef]
    InsightVisual: NotRequired[InsightVisualTypeDef]
    SankeyDiagramVisual: NotRequired[SankeyDiagramVisualTypeDef]
    CustomContentVisual: NotRequired[CustomContentVisualTypeDef]
    EmptyVisual: NotRequired[EmptyVisualTypeDef]
    RadarChartVisual: NotRequired[RadarChartVisualTypeDef]
    PluginVisual: NotRequired[PluginVisualTypeDef]


class CreateDataSetRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    Name: str
    PhysicalTableMap: Mapping[str, PhysicalTableUnionTypeDef]
    ImportMode: DataSetImportModeType
    LogicalTableMap: NotRequired[Mapping[str, LogicalTableUnionTypeDef]]
    ColumnGroups: NotRequired[Sequence[ColumnGroupUnionTypeDef]]
    FieldFolders: NotRequired[Mapping[str, FieldFolderUnionTypeDef]]
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionTagConfiguration: NotRequired[RowLevelPermissionTagConfigurationUnionTypeDef]
    ColumnLevelPermissionRules: NotRequired[Sequence[ColumnLevelPermissionRuleUnionTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataSetUsageConfiguration: NotRequired[DataSetUsageConfigurationTypeDef]
    DatasetParameters: NotRequired[Sequence[DatasetParameterUnionTypeDef]]
    FolderArns: NotRequired[Sequence[str]]
    PerformanceConfiguration: NotRequired[PerformanceConfigurationUnionTypeDef]
    UseAs: NotRequired[Literal["RLS_RULES"]]
    DataPrepConfiguration: NotRequired[DataPrepConfigurationUnionTypeDef]
    SemanticModelConfiguration: NotRequired[SemanticModelConfigurationUnionTypeDef]


class UpdateDataSetRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    Name: str
    PhysicalTableMap: Mapping[str, PhysicalTableUnionTypeDef]
    ImportMode: DataSetImportModeType
    LogicalTableMap: NotRequired[Mapping[str, LogicalTableUnionTypeDef]]
    ColumnGroups: NotRequired[Sequence[ColumnGroupUnionTypeDef]]
    FieldFolders: NotRequired[Mapping[str, FieldFolderUnionTypeDef]]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionTagConfiguration: NotRequired[RowLevelPermissionTagConfigurationUnionTypeDef]
    ColumnLevelPermissionRules: NotRequired[Sequence[ColumnLevelPermissionRuleUnionTypeDef]]
    DataSetUsageConfiguration: NotRequired[DataSetUsageConfigurationTypeDef]
    DatasetParameters: NotRequired[Sequence[DatasetParameterUnionTypeDef]]
    PerformanceConfiguration: NotRequired[PerformanceConfigurationUnionTypeDef]
    DataPrepConfiguration: NotRequired[DataPrepConfigurationUnionTypeDef]
    SemanticModelConfiguration: NotRequired[SemanticModelConfigurationUnionTypeDef]


class CreateTopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: str
    DatasetArn: str
    Question: str
    Mir: NotRequired[TopicIRUnionTypeDef]
    PrimaryVisual: NotRequired[TopicVisualUnionTypeDef]
    Template: NotRequired[TopicTemplateUnionTypeDef]


class SheetDefinitionOutputTypeDef(TypedDict):
    SheetId: str
    Title: NotRequired[str]
    Description: NotRequired[str]
    Name: NotRequired[str]
    ParameterControls: NotRequired[list[ParameterControlOutputTypeDef]]
    FilterControls: NotRequired[list[FilterControlOutputTypeDef]]
    Visuals: NotRequired[list[VisualOutputTypeDef]]
    TextBoxes: NotRequired[list[SheetTextBoxTypeDef]]
    Images: NotRequired[list[SheetImageOutputTypeDef]]
    Layouts: NotRequired[list[LayoutOutputTypeDef]]
    SheetControlLayouts: NotRequired[list[SheetControlLayoutOutputTypeDef]]
    ContentType: NotRequired[SheetContentTypeType]
    CustomActionDefaults: NotRequired[VisualCustomActionDefaultsTypeDef]


class SheetDefinitionTypeDef(TypedDict):
    SheetId: str
    Title: NotRequired[str]
    Description: NotRequired[str]
    Name: NotRequired[str]
    ParameterControls: NotRequired[Sequence[ParameterControlTypeDef]]
    FilterControls: NotRequired[Sequence[FilterControlTypeDef]]
    Visuals: NotRequired[Sequence[VisualTypeDef]]
    TextBoxes: NotRequired[Sequence[SheetTextBoxTypeDef]]
    Images: NotRequired[Sequence[SheetImageTypeDef]]
    Layouts: NotRequired[Sequence[LayoutTypeDef]]
    SheetControlLayouts: NotRequired[Sequence[SheetControlLayoutTypeDef]]
    ContentType: NotRequired[SheetContentTypeType]
    CustomActionDefaults: NotRequired[VisualCustomActionDefaultsTypeDef]


class BatchCreateTopicReviewedAnswerRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    Answers: Sequence[CreateTopicReviewedAnswerTypeDef]


class AnalysisDefinitionOutputTypeDef(TypedDict):
    DataSetIdentifierDeclarations: list[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[list[SheetDefinitionOutputTypeDef]]
    CalculatedFields: NotRequired[list[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[list[ParameterDeclarationOutputTypeDef]]
    FilterGroups: NotRequired[list[FilterGroupOutputTypeDef]]
    ColumnConfigurations: NotRequired[list[ColumnConfigurationOutputTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsOutputTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[list[StaticFileTypeDef]]


class DashboardVersionDefinitionOutputTypeDef(TypedDict):
    DataSetIdentifierDeclarations: list[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[list[SheetDefinitionOutputTypeDef]]
    CalculatedFields: NotRequired[list[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[list[ParameterDeclarationOutputTypeDef]]
    FilterGroups: NotRequired[list[FilterGroupOutputTypeDef]]
    ColumnConfigurations: NotRequired[list[ColumnConfigurationOutputTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsOutputTypeDef]
    StaticFiles: NotRequired[list[StaticFileTypeDef]]


class TemplateVersionDefinitionOutputTypeDef(TypedDict):
    DataSetConfigurations: list[DataSetConfigurationOutputTypeDef]
    Sheets: NotRequired[list[SheetDefinitionOutputTypeDef]]
    CalculatedFields: NotRequired[list[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[list[ParameterDeclarationOutputTypeDef]]
    FilterGroups: NotRequired[list[FilterGroupOutputTypeDef]]
    ColumnConfigurations: NotRequired[list[ColumnConfigurationOutputTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsOutputTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[list[StaticFileTypeDef]]


class AnalysisDefinitionTypeDef(TypedDict):
    DataSetIdentifierDeclarations: Sequence[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[Sequence[SheetDefinitionTypeDef]]
    CalculatedFields: NotRequired[Sequence[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[Sequence[ParameterDeclarationTypeDef]]
    FilterGroups: NotRequired[Sequence[FilterGroupTypeDef]]
    ColumnConfigurations: NotRequired[Sequence[ColumnConfigurationTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[Sequence[StaticFileTypeDef]]


class DashboardVersionDefinitionTypeDef(TypedDict):
    DataSetIdentifierDeclarations: Sequence[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[Sequence[SheetDefinitionTypeDef]]
    CalculatedFields: NotRequired[Sequence[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[Sequence[ParameterDeclarationTypeDef]]
    FilterGroups: NotRequired[Sequence[FilterGroupTypeDef]]
    ColumnConfigurations: NotRequired[Sequence[ColumnConfigurationTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    StaticFiles: NotRequired[Sequence[StaticFileTypeDef]]


class TemplateVersionDefinitionTypeDef(TypedDict):
    DataSetConfigurations: Sequence[DataSetConfigurationTypeDef]
    Sheets: NotRequired[Sequence[SheetDefinitionTypeDef]]
    CalculatedFields: NotRequired[Sequence[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[Sequence[ParameterDeclarationTypeDef]]
    FilterGroups: NotRequired[Sequence[FilterGroupTypeDef]]
    ColumnConfigurations: NotRequired[Sequence[ColumnConfigurationTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[Sequence[StaticFileTypeDef]]


class DescribeAnalysisDefinitionResponseTypeDef(TypedDict):
    AnalysisId: str
    Name: str
    Errors: list[AnalysisErrorTypeDef]
    ResourceStatus: ResourceStatusType
    ThemeArn: str
    Definition: AnalysisDefinitionOutputTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDashboardDefinitionResponseTypeDef(TypedDict):
    DashboardId: str
    Errors: list[DashboardErrorTypeDef]
    Name: str
    ResourceStatus: ResourceStatusType
    ThemeArn: str
    Definition: DashboardVersionDefinitionOutputTypeDef
    Status: int
    RequestId: str
    DashboardPublishOptions: DashboardPublishOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTemplateDefinitionResponseTypeDef(TypedDict):
    Name: str
    TemplateId: str
    Errors: list[TemplateErrorTypeDef]
    ResourceStatus: ResourceStatusType
    ThemeArn: str
    Definition: TemplateVersionDefinitionOutputTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


AnalysisDefinitionUnionTypeDef = Union[AnalysisDefinitionTypeDef, AnalysisDefinitionOutputTypeDef]
DashboardVersionDefinitionUnionTypeDef = Union[
    DashboardVersionDefinitionTypeDef, DashboardVersionDefinitionOutputTypeDef
]
TemplateVersionDefinitionUnionTypeDef = Union[
    TemplateVersionDefinitionTypeDef, TemplateVersionDefinitionOutputTypeDef
]


class CreateAnalysisRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    Name: str
    Parameters: NotRequired[ParametersUnionTypeDef]
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    SourceEntity: NotRequired[AnalysisSourceEntityTypeDef]
    ThemeArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Definition: NotRequired[AnalysisDefinitionUnionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]
    FolderArns: NotRequired[Sequence[str]]


class UpdateAnalysisRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    Name: str
    Parameters: NotRequired[ParametersUnionTypeDef]
    SourceEntity: NotRequired[AnalysisSourceEntityTypeDef]
    ThemeArn: NotRequired[str]
    Definition: NotRequired[AnalysisDefinitionUnionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]


class CreateDashboardRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    Name: str
    Parameters: NotRequired[ParametersUnionTypeDef]
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    SourceEntity: NotRequired[DashboardSourceEntityTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VersionDescription: NotRequired[str]
    DashboardPublishOptions: NotRequired[DashboardPublishOptionsTypeDef]
    ThemeArn: NotRequired[str]
    Definition: NotRequired[DashboardVersionDefinitionUnionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]
    FolderArns: NotRequired[Sequence[str]]
    LinkSharingConfiguration: NotRequired[LinkSharingConfigurationUnionTypeDef]
    LinkEntities: NotRequired[Sequence[str]]


class UpdateDashboardRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    Name: str
    SourceEntity: NotRequired[DashboardSourceEntityTypeDef]
    Parameters: NotRequired[ParametersUnionTypeDef]
    VersionDescription: NotRequired[str]
    DashboardPublishOptions: NotRequired[DashboardPublishOptionsTypeDef]
    ThemeArn: NotRequired[str]
    Definition: NotRequired[DashboardVersionDefinitionUnionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]


class CreateTemplateRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    Name: NotRequired[str]
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    SourceEntity: NotRequired[TemplateSourceEntityTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VersionDescription: NotRequired[str]
    Definition: NotRequired[TemplateVersionDefinitionUnionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]


class UpdateTemplateRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    SourceEntity: NotRequired[TemplateSourceEntityTypeDef]
    VersionDescription: NotRequired[str]
    Name: NotRequired[str]
    Definition: NotRequired[TemplateVersionDefinitionUnionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]
