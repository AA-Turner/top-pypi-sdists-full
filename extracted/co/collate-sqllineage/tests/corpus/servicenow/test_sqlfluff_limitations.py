"""Tests for sqlfluff limitations."""

from tests.helpers import assert_table_lineage_equal


def test_sqlfluff_limitations_if_q67():
    """sqlfluff limitations - Query 67"""
    sql = """ ALTER TABLE IF EXISTS
RDS.OUTREACH.TEAMS
SWAP WITH
RDS.OUTREACH.STG_TEAMS"""
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    # SqlFluff: Cannot correctly parse SWAP statements
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_teams"},  # source_tables
        {"rds.outreach.teams"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_rds__q69():
    """sqlfluff limitations - Query 69"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."LEARNING_HUB"."SN_LXP_CONTENT_ITEM" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."LEARNING_HUB"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {
            "rds.learning_hub.sn_lxp_content_item",
            "rds.learning_hub.sys_audit_delete",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_rds_dynamics365_activitypointers_q90():
    """sqlfluff limitations - Query 90"""
    sql = """ insert into RDS.DYNAMICS365.TABLES_DELETED_RECORDS_ID ( SCHEMA ,  STORED_PROCEDURE ,  SOURCE_TABLE_NAME ,  OBJECT_ID ,  TIME_STAMP )
    select 'placeholder_1' , 'placeholder_2' , 'placeholder_3' , "ACTIVITYID" ,  CURRENT_TIMESTAMP
    FROM RDS.DYNAMICS365.ACTIVITYPOINTERS
    where "ACTIVITYID" IN (select distinct OBJECTID FROM "RDS"."DYNAMICS365"."AUDITS" WHERE "ACTION"='placeholder_4' and "OPERATION" = 'placeholder_5' AND LOWER( "OBJECTTYPECODE" ) = 'placeholder_6' AND CAST( "CREATEDON" AS DATE ) >=DATEADD(DAY, 'placeholder_7', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {"rds.dynamics365.activitypointers", "rds.dynamics365.audits"},  # source_tables
        {"rds.dynamics365.tables_deleted_records_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_rds__q315():
    """sqlfluff limitations - Query 315"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."DATACENTER"."U_AUDIT_REQUEST" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."DATACENTER"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {
            "rds.datacenter.sys_audit_delete",
            "rds.datacenter.u_audit_request",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_query_q419():
    """sqlfluff limitations - Query 419"""
    sql = """ update "NOC"."LOGGING"."ETL_RDS_JOB_RUN_AUDIT"
set
job_status='2025-01-01 00:00:00',
JOB_END_TS=current_timestamp(),
-- job_run_duration='53970',
SOURCE_RECORD_COUNT=2,
PROCESSED_RECORD_COUNT=3,
ERROR_RECORD_COUNT = 4-'placeholder_5',
ETL_UPDATE_DATE= current_timestamp()
-- LAST_RUN_TIMESTAMP= current_timestamp()
where RDS_CONFIG_ID='2025-01-01 00:00:00'
and INTEG_JOB_ID = 7
and INTEG_TOOL_JOB_RUN_ID = 8 ;"""
    # SqlFluff: Cannot extract correct source tables from complex queries
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.logging.etl_rds_job_run_audit"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_rds__q475():
    """sqlfluff limitations - Query 475"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."LXP"."CMDB_CI_SERVICE_BUSINESS" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."LXP"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {
            "rds.lxp.cmdb_ci_service_business",
            "rds.lxp.sys_audit_delete",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_query_q496():
    """sqlfluff limitations - Query 496"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_TARGET_COUNT = 2 WHERE TARGET_SCHEMA = 'placeholder_3' AND                                     TARGET_TABLE_NAME = 'placeholder_4'"""
    # SqlFluff: Cannot extract correct source tables from complex queries
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_edw_ls__q703():
    """sqlfluff limitations - Query 703"""
    sql = """ CREATE OR REPLACE TEMPORARY TABLE EDW_LS."FINANCE_AR_EM"."TEMP_EM_BILLINGS_WITH_CONTRACT_INFO" AS
            SELECT "VBRP_Client" as "VBRP_Client",
            "VBRP_BillingDocument" as "VBRP_BillingDocument",
            "VBRP_BillingItem" as "VBRP_BillingItem",
            "AssociatedContractNumber" as "AssociatedContractNumber",
            "AssociatedContractLineNumber" as "AssociatedContractLineNumber",
            "VBRP_SalesDocument" as "VBRP_SalesDocument",
            "VBRP_SalesDocumentItem" as "VBRP_SalesDocumentItem",
            "VBRP_DocumentNumberoftheReferenceDocument" as "VBRP_DocumentNumberoftheReferenceDocument",
            "VBRP_ItemNumberoftheReferenceItem" as "VBRP_ItemNumberoftheReferenceItem",
            "VBRP_DateonWhichServicesRendered" as "VBRP_DateonWhichServicesRendered",
            "VBRP_DocumentCategoryofPrecedingSDDocument" as "VBRP_DocumentCategoryofPrecedingSDDocument",
            "VBRP_MaterialNumber" as "VBRP_MaterialNumber",
            "VBRP_MaterialGroup" as "VBRP_MaterialGroup",
            "VBRP_SalesDocumentItemCategory" as "VBRP_SalesDocumentItemCategory",
            "VBRP_SalesGroup" as "VBRP_SalesGroup",
            "VBRP_ContractType" as "VBRP_ContractType",
            "VBRP_BillingPlanNumber" as "VBRP_BillingPlanNumber",
            "VBRP_BillingPlanItem" as "VBRP_BillingPlanItem",
            "VBRP_TaxClassificationMaterial" as "VBRP_TaxClassificationMaterial",
            "VBRK_BillingType" as "VBRK_BillingType",
            "VBRK_SDDocumentCategory" as "VBRK_SDDocumentCategory",
            "VBRK_SDDocumentCurrency" as "VBRK_SDDocumentCurrency",
            "VBRK_SalesOrganization" as "VBRK_SalesOrganization",
            "VBRK_NumberofTheDocumentCondition" as "VBRK_NumberofTheDocumentCondition",
            "VBRK_BillingDateforBillingIndexandPrintout" as "VBRK_BillingDateforBillingIndexandPrintout",
            "VBRK_StatusforTransfertoAccounting" as "VBRK_StatusforTransfertoAccounting",
            "VBRK_DateonWhichRecordWasCreated" as "VBRK_DateonWhichRecordWasCreated",
            "VBRK_TermsofPaymentKey" as "VBRK_TermsofPaymentKey",
            "VBRK_CancelledBillingDocumentNumber" as "VBRK_CancelledBillingDocumentNumber",
            "VBRK_DummyInvoiceFlag" as "VBRK_DummyInvoiceFlag",
            "VBFA_PreceedingSDDocument" as "VBFA_PreceedingSDDocument",
            "VBFA_PreceedingSDDocumentItem" as "VBFA_PreceedingSDDocumentItem",
            "VBRP_ActualInvoicedQuantity" as "VBRP_ActualInvoicedQuantity",
            "VBRP_ExchangeRateforPriceDetermination" as "VBRP_ExchangeRateforPriceDetermination",
            "VBRP_NetValueoftheBillingIteminDocumentCurrency" as "VBRP_NetValueoftheBillingIteminDocumentCurrency",
            "VBRP_TaxAmountinDocumentCurrency" as "VBRP_TaxAmountinDocumentCurrency",
            "VBRK_ExchangeRateforFIPostings" as "VBRK_ExchangeRateforFIPostings",
            "VBRP_ItemCategoryDescription" as "VBRP_ItemCategoryDescription",
            "CC_DocumentType" as "CC_DocumentType",
            "T001_CompanyCodeCurrencyKey" as "T001_CompanyCodeCurrencyKey",
            "CC_BillingAmountLC.CURRENCY" as "CC_BillingAmountLC.CURRENCY",
            "CC_BillingAmountLC" as "CC_BillingAmountLC",
            "CC_FXDate" as "CC_FXDate",
            "GrossDownFlatFileQuarterKey" as "GrossDownFlatFileQuarterKey",
            "GrossDownFlatFileYearKey" as "GrossDownFlatFileYearKey",
            "CC_BillingAmountDC" as "CC_BillingAmountDC",
            "CC_TaxAmountLC" as "CC_TaxAmountLC",
            "CC_TaxAmountLC.CURRENCY" as "CC_TaxAmountLC.CURRENCY",
            "CC_BundleLevelItem" as "CC_BundleLevelItem",
            "CC_CancelledorCancellingBillingDocFlag" as "CC_CancelledorCancellingBillingDocFlag",
            "T023T_MatGroupLongText" as "T023T_MatGroupLongText",
            "C_ProductCategory" as "C_ProductCategory",
            "CC_CancellationFlag" as "CC_CancellationFlag",
            "MaterialDescription" as "MaterialDescription",
            "CC_TaxAmountDC" as "CC_TaxAmountDC",
            "VBRK_CancelledBillingDocumentDate" as "VBRK_CancelledBillingDocumentDate",
            "VBRK_Date_On_Which_Document_is_Canceled" as "VBRK_Date_On_Which_Document_is_Canceled",
            "Cancelled_Date_PCF" as "Cancelled_Date_PCF",
            "CC_CancelledBillingdocYN" as "CC_CancelledBillingdocYN",
            "CC_CancellationBillingDocFlag" as "CC_CancellationBillingDocFlag",
            "AccountingDocTypeOfBillingDoc" as "AccountingDocTypeOfBillingDoc",
            IFF("VBRK_StatusforTransfertoAccounting" = 'placeholder_1', 'placeholder_2', 'placeholder_3')  as "CC_BillingAccountingDocument",
            to_date("VBRK_Date_On_Which_Document_is_Canceled",'placeholder_4')  as "CC_CancelledBillingDocumentDate"
            FROM EDW_LS."FINANCE_AR_EM"."EM_BILLINGS_WITH_CONTRACT_INFO"
            WHERE "VBRP_MaterialNumber" <> 'placeholder_5' AND
            ("VBRK_DummyInvoiceFlag" IS TRUE or "VBRK_DummyInvoiceFlag" ='placeholder_7') AND
            "VBRP_ItemCategoryDescription" not IN('placeholder_8','placeholder_9')  AND
            "CC_BundleLevelItem" IS TRUE"""
    # SqlFluff: Cannot extract correct source tables from complex queries
    assert_table_lineage_equal(
        sql,
        {"edw_ls.finance_ar_em.em_billings_with_contract_info"},  # source_tables
        {"edw_ls.finance_ar_em.temp_em_billings_with_contract_info"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_edw_ls_sales_em_v_sales_leader_forecast_summary_q706():
    """sqlfluff limitations - Query 706"""
    sql = """ create or replace temp table EDW_LS.SALES_EM.TEMP_SLD_SUMMARY AS
SELECT * FROM EDW_LS.SALES_EM.V_SALES_LEADER_FORECAST_SUMMARY"""
    # SqlFluff: Cannot extract correct source tables from complex queries
    assert_table_lineage_equal(
        sql,
        {"edw_ls.sales_em.v_sales_leader_forecast_summary"},  # source_tables
        {"edw_ls.sales_em.temp_sld_summary"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_cdl_ls__q737():
    """sqlfluff limitations - Query 737"""
    sql = """ CREATE OR REPLACE  TABLE EDW_LS.BIECC.BOOKINGS_METRICS ("Close_Quarter", "Close_Quarter_Flag", "VALUE", "FIN_PCT", "NewCustomerFinNNACV_PCT", "CustomerUpsellFinNNACV_PCT", "RenewalACVAC_PCT", "TotalACVBookings_Corp_PCT", "PSBookingsExclCustomerSuccess_PCT", "TrainingBookingsExcl_CustomerSuccess_PCT", "CSNNACVExcl_SAMAllocation_PCT", "CSRenewalACVExclSAMAllocation_PCT", "TotalServicesBookingsInc_PCT", "TotalBookings_PCT", "CSBookings_PCT", "OptyItemCSRenewalACV_PCT", "AcctName", "AcctOverrideSegment", "BaselineDealQuarter", "BaselineQtrAcctBU", "BUWon_CC", "HQ_Business_Segment_QE_Fixed", "HQ_Industry_Category_QE_Fixed", "HQFinanceReportingType_CC", "LegacyBaselineQuarter", "OptyOpportunityLinkReason", "OptyRenewalStatus_CC", "PRE_BUY_FLAG", "ProductBusinessUnitValue", "ProductFamily3Value", "ProductFlag_CC", "ReportingTerritoryGeo_CC", "Workflow", "CB_LostACV", "AccountTotalRenewalOpportunity_CC", "BaselineNNACV_CC", "CB_CSNNACVExcl_SAMAllocation_CC", "CB_CSRenewalACVExclSAMAllocation", "CB_CustomerUpsellFinNNACV_CC", "CB_NewCustomerFinNNACV_CC", "CB_PSBookingsExcl_CustomerSuccess_CC", "CB_TotalBookings_Corp_CC", "CB_TotalCustomerSuccessACV_CC", "CB_TotalServicesBookingsExcl_CustomerSuccess_CC", "CB_TotalServicesBookingsInc_CSExcl_SAMAllocation_CC", "CB_TrainingBookingsExcl_CustomerSuccess_CC", "CB_TotalACVBookings_Corp_CC", "CSBookings_CC", "CumulativeNetNewACV", "OptyItemTerm", "OptyItemCSRenewalACV_USD_CC", "RenewalACVAC_CC", "TermNNACVFactor_CC", "TermRenewalACVFactor_CC", "AcctBUNNACVBridgeFlag", "AcctWWNNACVBridgeFlag", "TotalRenewalOpportunity_CC", "CumulativeNetNewACV_Adhoc", "FINNNACV_CC_Adhoc", "RenewalACVAC_CC_Adhoc", "OptyStage", "DNBBusinessName", "LostACV_PCT", "OptyItemLineItemNumber", "OptyItemCurrencyCode", "OptyCloseMonth_CC", "FinNNACVDC_CC", "RenewalRate_BP", "BUForecastNetNewACV", "1M_PCT", "1M_5M_PCT", "5M_10M_PCT", "10M_20M_PCT", "20M_PCT", "RecordKey", "Count", "AcctCustomerHQ", "Customer_1m_FLAG", "Customer_5M_FLAG", "Customer_10M_FLAG", "Customer_20M_FLAG", "Cum_NNACV", "PCT", "BUGroup", "CurrentMajorArea_CC", "OptyTerrGeo_SalesGeo", "Workflow_IR", "AcctCountry", "AcctBUSalesNNACVBridgeFlag", "AcctCountryTier", "CurrentGeo_CC", "FinNNACV_CC", "FinNNACV_Round", "Quota", "FinNNACVDCConstFX_CC", "NewFinNNACV_CALC", "AcctCustCounter", "CB_CommRenewalACV_CC", "CommNNACVUSD_CC", "CommRenewalOpp_CC", "AvgTerm_TermFactorUpsell_CC", "AvgTerm_UpsellACV_CC")
AS
SELECT "Close_Quarter",
       "Close_Quarter_Flag",
       "VALUE",
       "FIN_PCT",
       "NewCustomerFinNNACV_PCT",
       "CustomerUpsellFinNNACV_PCT",
       "RenewalACVAC_PCT",
       "TotalACVBookings_Corp_PCT",
       "PSBookingsExclCustomerSuccess_PCT",
       "TrainingBookingsExcl_CustomerSuccess_PCT",
       "CSNNACVExcl_SAMAllocation_PCT",
       "CSRenewalACVExclSAMAllocation_PCT",
       "TotalServicesBookingsInc_PCT",
       "TotalBookings_PCT",
       "CSBookings_PCT",
       "OptyItemCSRenewalACV_PCT",
       "AcctName",
       "AcctOverrideSegment",
       "BaselineDealQuarter",
       "BaselineQtrAcctBU",
       "BUWon_CC",
       "HQ_Business_Segment_QE_Fixed",
       "HQ_Industry_Category_QE_Fixed",
       "HQFinanceReportingType_CC",
       "LegacyBaselineQuarter",
       "OptyOpportunityLinkReason",
       "OptyRenewalStatus_CC",
       "PRE_BUY_FLAG",
       "ProductBusinessUnitValue",
       "ProductFamily3Value",
       "ProductFlag_CC",
       "ReportingTerritoryGeo_CC",
       "Workflow",
       "CB_LostACV",
       "AccountTotalRenewalOpportunity_CC",
       "BaselineNNACV_CC",
       "CB_CSNNACVExcl_SAMAllocation_CC",
       "CB_CSRenewalACVExclSAMAllocation",
       "CB_CustomerUpsellFinNNACV_CC",
       "CB_NewCustomerFinNNACV_CC",
       "CB_PSBookingsExcl_CustomerSuccess_CC",
       "CB_TotalBookings_Corp_CC",
       "CB_TotalCustomerSuccessACV_CC",
       "CB_TotalServicesBookingsExcl_CustomerSuccess_CC",
       "CB_TotalServicesBookingsInc_CSExcl_SAMAllocation_CC",
       "CB_TrainingBookingsExcl_CustomerSuccess_CC",
       "CB_TotalACVBookings_Corp_CC",
       "CSBookings_CC",
       "CumulativeNetNewACV",
       "OptyItemTerm",
       "OptyItemCSRenewalACV_USD_CC",
       "RenewalACVAC_CC",
       "TermNNACVFactor_CC",
       "TermRenewalACVFactor_CC",
       "AcctBUNNACVBridgeFlag",
       "AcctWWNNACVBridgeFlag",
       "TotalRenewalOpportunity_CC",
       "CumulativeNetNewACV_Adhoc",
       "FINNNACV_CC_Adhoc",
       "RenewalACVAC_CC_Adhoc",
       "OptyStage",
       "DNBBusinessName",
       "LostACV_PCT",
       "OptyItemLineItemNumber",
       "OptyItemCurrencyCode",
       "OptyCloseMonth_CC",
       "FinNNACVDC_CC",
       "RenewalRate_BP",
       "BUForecastNetNewACV",
       "1M_PCT",
       "1M_5M_PCT",
       "5M_10M_PCT",
       "10M_20M_PCT",
       "20M_PCT",
       "RecordKey",
       "Count",
       "AcctCustomerHQ",
       "Customer_1m_FLAG",
       "Customer_5M_FLAG",
       "Customer_10M_FLAG",
       "Customer_20M_FLAG",
       "Cum_NNACV",
       "PCT",
       "BUGroup",
       "CurrentMajorArea_CC",
       "OptyTerrGeo_SalesGeo",
       "Workflow_IR",
       "AcctCountry",
       "AcctBUSalesNNACVBridgeFlag",
       "AcctCountryTier",
       "CurrentGeo_CC",
       SUM ("FinNNACV_CC") AS "FinNNACV_CC",
           SUM ("FinNNACV_Round") AS "FinNNACV_Round",
               SUM ("Quota") AS "Quota",
                   SUM ("FinNNACVDCConstFX_CC") AS "FinNNACVDCConstFX_CC",
                       SUM ("NewFinNNACV_CALC") AS "NewFinNNACV_CALC",
                           SUM ("AcctCustCounter") AS "AcctCustCounter",
                               SUM ("CB_CommRenewalACV_CC") AS "CB_CommRenewalACV_CC",
                                   SUM ("CommNNACVUSD_CC") AS "CommNNACVUSD_CC",
                                       SUM ("CommRenewalOpp_CC") AS "CommRenewalOpp_CC",
                                           SUM ("AvgTerm_TermFactorUpsell_CC") AS "AvgTerm_TermFactorUpsell_CC",
                                               SUM ("AvgTerm_UpsellACV_CC") AS "AvgTerm_UpsellACV_CC"
            FROM CDL_LS."FINANCE_FPA_RPT"."BOOKINGS_METRICS"
/*"_SYS_BIC"."BOOKINGS_REAL_TIME.REPORTINGVIEWS/BOOKINGS_METRICS"*/

GROUP BY "Close_Quarter",
         "Close_Quarter_Flag",
         "VALUE",
         "FIN_PCT",
         "NewCustomerFinNNACV_PCT",
         "CustomerUpsellFinNNACV_PCT",
         "RenewalACVAC_PCT",
         "TotalACVBookings_Corp_PCT",
         "PSBookingsExclCustomerSuccess_PCT",
         "TrainingBookingsExcl_CustomerSuccess_PCT",
         "CSNNACVExcl_SAMAllocation_PCT",
         "CSRenewalACVExclSAMAllocation_PCT",
         "TotalServicesBookingsInc_PCT",
         "TotalBookings_PCT",
         "CSBookings_PCT",
         "OptyItemCSRenewalACV_PCT",
         "AcctName",
         "AcctOverrideSegment",
         "BaselineDealQuarter",
         "BaselineQtrAcctBU",
         "BUWon_CC",
         "HQ_Business_Segment_QE_Fixed",
         "HQ_Industry_Category_QE_Fixed",
         "HQFinanceReportingType_CC",
         "LegacyBaselineQuarter",
         "OptyOpportunityLinkReason",
         "OptyRenewalStatus_CC",
         "PRE_BUY_FLAG",
         "ProductBusinessUnitValue",
         "ProductFamily3Value",
         "ProductFlag_CC",
         "ReportingTerritoryGeo_CC",
         "Workflow",
         "CB_LostACV",
         "AccountTotalRenewalOpportunity_CC",
         "BaselineNNACV_CC",
         "CB_CSNNACVExcl_SAMAllocation_CC",
         "CB_CSRenewalACVExclSAMAllocation",
         "CB_CustomerUpsellFinNNACV_CC",
         "CB_NewCustomerFinNNACV_CC",
         "CB_PSBookingsExcl_CustomerSuccess_CC",
         "CB_TotalBookings_Corp_CC",
         "CB_TotalCustomerSuccessACV_CC",
         "CB_TotalServicesBookingsExcl_CustomerSuccess_CC",
         "CB_TotalServicesBookingsInc_CSExcl_SAMAllocation_CC",
         "CB_TrainingBookingsExcl_CustomerSuccess_CC",
         "CB_TotalACVBookings_Corp_CC",
         "CSBookings_CC",
         "CumulativeNetNewACV",
         "OptyItemTerm",
         "OptyItemCSRenewalACV_USD_CC",
         "RenewalACVAC_CC",
         "TermNNACVFactor_CC",
         "TermRenewalACVFactor_CC",
         "AcctBUNNACVBridgeFlag",
         "AcctWWNNACVBridgeFlag",
         "TotalRenewalOpportunity_CC",
         "CumulativeNetNewACV_Adhoc",
         "FINNNACV_CC_Adhoc",
         "RenewalACVAC_CC_Adhoc",
         "OptyStage",
         "DNBBusinessName",
         "LostACV_PCT",
         "OptyItemLineItemNumber",
         "OptyItemCurrencyCode",
         "OptyCloseMonth_CC",
         "FinNNACVDC_CC",
         "RenewalRate_BP",
         "BUForecastNetNewACV",
         "1M_PCT",
         "1M_5M_PCT",
         "5M_10M_PCT",
         "10M_20M_PCT",
         "20M_PCT",
         "RecordKey",
         "Count",
         "AcctCustomerHQ",
         "Customer_1m_FLAG",
         "Customer_5M_FLAG",
         "Customer_10M_FLAG",
         "Customer_20M_FLAG",
         "Cum_NNACV",
         "PCT",
         "BUGroup",
         "CurrentMajorArea_CC",
         "OptyTerrGeo_SalesGeo",
         "Workflow_IR",
         "AcctCountry",
         "AcctBUSalesNNACVBridgeFlag",
         "AcctCountryTier",
         "CurrentGeo_CC";"""
    # SqlFluff: Cannot extract correct source tables from complex queries
    assert_table_lineage_equal(
        sql,
        {"cdl_ls.finance_fpa_rpt.bookings_metrics"},  # source_tables
        {"edw_ls.biecc.bookings_metrics"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_rds__q768():
    """sqlfluff limitations - Query 768"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."HEALTHSCAN"."X_SNC_PIE_STATISTIC" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."HEALTHSCAN"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {
            "rds.healthscan.sys_audit_delete",
            "rds.healthscan.x_snc_pie_statistic",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_outreach_public_team_memberships_q1093():
    """sqlfluff limitations - Query 1093"""
    sql = """ INSERT INTO RDS.OUTREACH.STG_TEAM_MEMBERSHIPS
("TEAM_ID","BENTO","O_ID","UPDATER_ID","CREATED_AT","IS_DELETED_IN_APP","UPDATED_AT","DML_TYPE","ID","USER_ID","CREATOR_ID","SURROGATE_ID","DML_AT")
select "TEAM_ID","BENTO","O_ID","UPDATER_ID","CREATED_AT","IS_DELETED_IN_APP","UPDATED_AT","DML_TYPE","ID","USER_ID","CREATOR_ID","SURROGATE_ID","DML_AT" from OUTREACH.PUBLIC.TEAM_MEMBERSHIPS"""
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {"outreach.public.team_memberships"},  # source_tables
        {"rds.outreach.stg_team_memberships"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_rds_sap_ems_stg_customers_q1099():
    """sqlfluff limitations - Query 1099"""
    sql = """ insert into RDS.SAP_EMS.STG_CUSTOMERS
(
CUSTOMER_ID ,
CUSTOMER_NAME ,
CUSTOMER_SYSTEM ,
CUSTOMER_GROUP ,
VALID_TO ,
DELETED ,
ETL_INSERT_DATE
)
select
value:CustomerID::varchar as "CUSTOMER_ID",
value:CustomerName::varchar as "CUSTOMER_NAME",
value:CustomerSystem::varchar as    "CUSTOMER_SYSTEM",
value:CustomerGroup::varchar as    "CUSTOMER_GROUP",
to_date(value:ValidTo::varchar, 'placeholder_1') as "VALID_TO",
value:Deleted::varchar as    "DELETED",
current_timestamp()
from
 "RDS"."SAP_EMS".STG_CUSTOMERS_JSON_26
, lateral flatten(input => "Data Value":"data"."customers");"""
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {"rds.sap_ems.stg_customers_json_26"},  # source_tables
        {"rds.sap_ems.stg_customers"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_query_q1179():
    """sqlfluff limitations - Query 1179"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_SOURCE_COUNT = 2 WHERE SOURCE_SCHEMA = 'placeholder_3' AND                                     SOURCE_TABLE_NAME = 'placeholder_4'"""
    # SqlFluff: Cannot extract correct source tables from complex queries
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_rds__q1220():
    """sqlfluff limitations - Query 1220"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."USAGEANALYTICS"."U_ERROR_INSTANCES" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."USAGEANALYTICS"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {
            "rds.usageanalytics.sys_audit_delete",
            "rds.usageanalytics.u_error_instances",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_cdl_ls_finance_gl_rpt_temp_grir_aging_analysis_q1422():
    """sqlfluff limitations - Query 1422"""
    sql = """ CREATE OR REPLACE TEMPORARY TABLE CDL_LS.FINANCE_GL_RPT.TEMP_T_TABLE_IR   AS
SELECT "PurchasingDocument", "PurchasingDocumentItem","PostingDate","PostingDate_E", :1 AS "RunDate",SUM("AmountInUSD") AS "AmountInUSDIR"
FROM CDL_LS.FINANCE_GL_RPT.TEMP_GRIR_AGING_ANALYSIS
WHERE ("AccountingDocumentType_Calc" IN ('placeholder_1','placeholder_2'))
GROUP BY "PurchasingDocument", "PurchasingDocumentItem","PostingDate","PostingDate_E";"""
    # SqlFluff: Cannot extract correct source tables from complex queries
    assert_table_lineage_equal(
        sql,
        {"cdl_ls.finance_gl_rpt.temp_grir_aging_analysis"},  # source_tables
        {"cdl_ls.finance_gl_rpt.temp_t_table_ir"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_sys_audit_delete_q1735():
    """sqlfluff limitations - Query 1735"""
    sql = """ Merge into sys_audit_delete using sys_audit_delete_3484154 on sys_audit_delete."SYS_ID" = sys_audit_delete_3484154."SYS_ID"  when matched then update set  sys_audit_delete."DISPLAY_VALUE" =  sys_audit_delete_3484154."DISPLAY_VALUE", sys_audit_delete."SYS_MOD_COUNT" =  sys_audit_delete_3484154."SYS_MOD_COUNT", sys_audit_delete."SYS_UPDATED_ON" =  sys_audit_delete_3484154."SYS_UPDATED_ON", sys_audit_delete."SYS_ID" =  sys_audit_delete_3484154."SYS_ID", sys_audit_delete."SYS_UPDATED_BY" =  sys_audit_delete_3484154."SYS_UPDATED_BY", sys_audit_delete."PAYLOAD" =  sys_audit_delete_3484154."PAYLOAD", sys_audit_delete."SYS_CREATED_ON" =  sys_audit_delete_3484154."SYS_CREATED_ON", sys_audit_delete."DOCUMENTKEY" =  sys_audit_delete_3484154."DOCUMENTKEY", sys_audit_delete."DELETE_RECOVERY" =  sys_audit_delete_3484154."DELETE_RECOVERY", sys_audit_delete."DV_DELETE_RECOVERY" =  sys_audit_delete_3484154."DV_DELETE_RECOVERY", sys_audit_delete."TABLENAME" =  sys_audit_delete_3484154."TABLENAME", sys_audit_delete."SYS_CREATED_BY" =  sys_audit_delete_3484154."SYS_CREATED_BY", sys_audit_delete."TRANSACTION" =  sys_audit_delete_3484154."TRANSACTION", sys_audit_delete."DV_TRANSACTION" =  sys_audit_delete_3484154."DV_TRANSACTION", sys_audit_delete."PSP_PER_INSERT_DT" =  sys_audit_delete."PSP_PER_INSERT_DT", sys_audit_delete."PSP_PER_DELETE_DT" =  sys_audit_delete_3484154."PSP_PER_DELETE_DT", sys_audit_delete."PSP_PER_UPDATE_DT" =  '2025-01-01 00:00:00' when not matched then insert ( sys_audit_delete."DISPLAY_VALUE", sys_audit_delete."SYS_MOD_COUNT", sys_audit_delete."SYS_UPDATED_ON", sys_audit_delete."SYS_ID", sys_audit_delete."SYS_UPDATED_BY", sys_audit_delete."PAYLOAD", sys_audit_delete."SYS_CREATED_ON", sys_audit_delete."DOCUMENTKEY", sys_audit_delete."DELETE_RECOVERY", sys_audit_delete."DV_DELETE_RECOVERY", sys_audit_delete."TABLENAME", sys_audit_delete."SYS_CREATED_BY", sys_audit_delete."TRANSACTION", sys_audit_delete."DV_TRANSACTION", sys_audit_delete."PSP_PER_INSERT_DT", sys_audit_delete."PSP_PER_DELETE_DT", sys_audit_delete."PSP_PER_UPDATE_DT") values ( sys_audit_delete_3484154."DISPLAY_VALUE", sys_audit_delete_3484154."SYS_MOD_COUNT", sys_audit_delete_3484154."SYS_UPDATED_ON", sys_audit_delete_3484154."SYS_ID", sys_audit_delete_3484154."SYS_UPDATED_BY", sys_audit_delete_3484154."PAYLOAD", sys_audit_delete_3484154."SYS_CREATED_ON", sys_audit_delete_3484154."DOCUMENTKEY", sys_audit_delete_3484154."DELETE_RECOVERY", sys_audit_delete_3484154."DV_DELETE_RECOVERY", sys_audit_delete_3484154."TABLENAME", sys_audit_delete_3484154."SYS_CREATED_BY", sys_audit_delete_3484154."TRANSACTION", sys_audit_delete_3484154."DV_TRANSACTION", 'placeholder_2', sys_audit_delete_3484154."PSP_PER_DELETE_DT", 'placeholder_3')"""
    # SqlFluff: Missing or incorrect source table extraction in MERGE
    assert_table_lineage_equal(
        sql,
        {"<default>.sys_audit_delete_3484154"},  # source_tables
        {"<default>.sys_audit_delete"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_edw_sales_fact_fixeddata_pipeline_q1888():
    """sqlfluff limitations - Query 1888"""
    sql = """ MERGE INTO EDW.SALES.FACT_FIXEDDATA_PIPELINE TGT
     USING (
     SELECT

        T.PIPELINE_ID

     FROM
        EDW.SALES.FACT_FIXEDDATA_PIPELINE T
        LEFT JOIN  EDW.SALES.FACT_FIXEDDATA_PIPELINE_TEMP S ON T.PIPELINE_ID = S.PIPELINE_ID
     WHERE ((T.QUARTER_YYQQ >= :from_qtr AND :IP_LOAD_TYPE='placeholder_1') OR (:IP_LOAD_TYPE='placeholder_2'))
     AND S.PIPELINE_ID IS NULL
     ) SRC
     ON SRC.PIPELINE_ID = TGT.PIPELINE_ID
     WHEN MATCHED THEN DELETE"""
    # SqlFluff: Missing or incorrect source table extraction in MERGE
    assert_table_lineage_equal(
        sql,
        {
            "edw.sales.fact_fixeddata_pipeline",
            "edw.sales.fact_fixeddata_pipeline_temp",
        },  # source_tables
        {"edw.sales.fact_fixeddata_pipeline"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
    )


def test_sqlfluff_limitations_rds__q1895():
    """sqlfluff limitations - Query 1895"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."HI"."METRIC_INSTANCE" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."HI"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {"rds.hi.metric_instance", "rds.hi.sys_audit_delete"},  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )


def test_sqlfluff_limitations_rds_dynamics365_sn_approvals_q2016():
    """sqlfluff limitations - Query 2016"""
    sql = """ insert into RDS.DYNAMICS365.TABLES_DELETED_RECORDS_ID ( SCHEMA ,  STORED_PROCEDURE ,  SOURCE_TABLE_NAME ,  OBJECT_ID ,  TIME_STAMP )
    select 'placeholder_1' , 'placeholder_2' , 'placeholder_3' , "ACTIVITYID" ,  CURRENT_TIMESTAMP
    FROM RDS.DYNAMICS365.SN_APPROVALS
    where "ACTIVITYID" IN (select distinct OBJECTID FROM "RDS"."DYNAMICS365"."AUDITS" WHERE "ACTION"='placeholder_4' and "OPERATION" = 'placeholder_5' AND LOWER( "OBJECTTYPECODE" ) = 'placeholder_6' AND CAST( "CREATEDON" AS DATE ) >=DATEADD(DAY, 'placeholder_7', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    assert_table_lineage_equal(
        sql,
        {"rds.dynamics365.audits", "rds.dynamics365.sn_approvals"},  # source_tables
        {"rds.dynamics365.tables_deleted_records_id"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        test_sqlparse=False,
    )
