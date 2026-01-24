"""Tests for sqlglot limitations."""

from tests.helpers import assert_table_lineage_equal


def test_sqlglot_limitations_query_q20():
    """sqlglot limitations - Query 20"""
    sql = """ UPDATE NOC.CONFIG."ETL_RDS_CONFIG_RECON"
SET LAST_RDS_JOB_RUN_ID='2025-01-01 00:00:00',
    TOTAL_SOURCE_COUNT=2,
    TOTAL_TARGET_COUNT=3,
    ETL_UPDATE_DATE=current_timestamp()
    WHERE RDS_CONFIG_ID='2025-01-01 00:00:00'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q23():
    """sqlglot limitations - Query 23"""
    sql = """ insert into "EDW_LS"."BIECC"."ST_PR_FPA_APPROVER" ("PrNumber", "PrCreateDate", "PrState", "CostCenter", "FpnaApprover", "Timestamp", "SystemDate", "PrAmountUsd", "Counter") select "PrNumber", "PrCreateDate", "PrState", "CostCenter", "FpnaApprover", "Timestamp", "SystemDate", "PrAmountUsd", "Counter" from (select
    "PrNumber" as "PrNumber",
    "PrCreateDate" as "PrCreateDate",
    "PrState" as "PrState",
    "CostCenter" as "CostCenter",
    "FpnaApprover" as "FpnaApprover",
    "Timestamp" as "Timestamp",
    "SystemDate" as "SystemDate",
    "PrAmountUsd" as "PrAmountUsd",
    "Counter" as "Counter"
from (SELECT
  *
FROM ((SELECT
  "left_input"."PrNumber" AS "PrNumber",
  "left_input"."PrCreateDate" AS "PrCreateDate",
  "left_input"."PrState" AS "PrState",
  "left_input"."CostCenter" AS "CostCenter",
  "left_input"."FpnaApprover" AS "FpnaApprover",
  "left_input"."Timestamp" AS "Timestamp",
  "left_input"."SystemDate" AS "SystemDate",
  "left_input"."PrAmountUsd" AS "PrAmountUsd",
  "left_input"."Counter" AS "Counter",
  "input"."PrNumber" AS "PrNumber_check"
FROM ((SELECT
  *
FROM (SELECT
  "PrNumber",
  "PrCreateDate",
  "PrState",
  "CostCenter",
  "FpnaApprover",
  "PrAmountUsd",
  "Timestamp",
  "SystemDate",
  "Counter"
FROM "EDW_LS"."FINANCE_PTP_EM"."EM_PR_FPA_APPROVER")
WHERE ("Timestamp" > '2025-01-01 00:00:00'))) AS "left_input"
     LEFT OUTER JOIN
     (SELECT
  "PrNumber",
  "PrCreateDate",
  "PrState",
  "CostCenter",
  "FpnaApprover",
  "Timestamp",
  "SystemDate",
  "PrAmountUsd",
  "Counter"
FROM "EDW_LS"."BIECC"."ST_PR_FPA_APPROVER") AS "input"
     ON "left_input"."PrNumber"="input"."PrNumber"))
WHERE ("PrNumber_check" IS TRUE)))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "edw_ls.biecc.st_pr_fpa_approver",
            "edw_ls.finance_ptp_em.em_pr_fpa_approver",
        },  # source_tables
        {"edw_ls.biecc.st_pr_fpa_approver"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_sqlglot_limitations_query_q26():
    """sqlglot limitations - Query 26"""
    sql = """ merge into "RDS"."MARKETO"."INTERESTING_MOMENTS" as "target" using (SELECT
  "ID",
  "MARKETOGUID",
  "LEADID",
  TO_TIMESTAMP_NTZ("ACTIVITYDATE")
AS "ACTIVITYDATE",
  "ACTIVITYTYPEID",
  "PRIMARYATTRIBUTEVALUE",
  "CAMPAIGNID",
  "CAMPAIGN",
  "PRIMARYATTRIBUTEVALUEID",
  "SOURCE",
  TO_TIMESTAMP_NTZ("DATE")
AS "DATE",
  "DESCRIPTION",
  CURRENT_TIMESTAMP()
AS "ETL_INSERT_DATE",
  CURRENT_TIMESTAMP()
AS "ETL_UPDATE_DATE",
  NULL
AS "ETL_DELETE_DATE"
FROM ((SELECT
  "ID",
  "max_MARKETOGUID" AS "MARKETOGUID",
  "max_LEADID" AS "LEADID",
  "max_ACTIVITYDATE" AS "ACTIVITYDATE",
  "max_ACTIVITYTYPEID" AS "ACTIVITYTYPEID",
  "max_PRIMARYATTRIBUTEVALUE" AS "PRIMARYATTRIBUTEVALUE",
  "max_CAMPAIGNID" AS "CAMPAIGNID",
  "max_CAMPAIGN" AS "CAMPAIGN",
  "max_PRIMARYATTRIBUTEVALUEID" AS "PRIMARYATTRIBUTEVALUEID",
  "max_SOURCE" AS "SOURCE",
  "max_DATE" AS "DATE",
  "max_DESCRIPTION" AS "DESCRIPTION"
FROM ((SELECT
  "ID",
  MAX("MARKETOGUID") AS "max_MARKETOGUID",
  MAX("LEADID") AS "max_LEADID",
  MAX("ACTIVITYDATE") AS "max_ACTIVITYDATE",
  MAX("ACTIVITYTYPEID") AS "max_ACTIVITYTYPEID",
  MAX("PRIMARYATTRIBUTEVALUE") AS "max_PRIMARYATTRIBUTEVALUE",
  MAX("CAMPAIGNID") AS "max_CAMPAIGNID",
  MAX("CAMPAIGN") AS "max_CAMPAIGN",
  MAX("PRIMARYATTRIBUTEVALUEID") AS "max_PRIMARYATTRIBUTEVALUEID",
  MAX("SOURCE") AS "max_SOURCE",
  MAX("DATE") AS "max_DATE",
  MAX("DESCRIPTION") AS "max_DESCRIPTION"
FROM ((SELECT DISTINCT
  "ID",
  "MARKETOGUID",
  "LEADID",
  "ACTIVITYDATE",
  "ACTIVITYTYPEID",
  "PRIMARYATTRIBUTEVALUE",
  "PRIMARYATTRIBUTEVALUEID",
  "CAMPAIGNID",
  "CAMPAIGN",
  "SOURCE",
  "DATE",
  "DESCRIPTION"
FROM ((SELECT
 *
 FROM ((SELECT
  "ID",
  "MARKETOGUID",
  "LEADID",
  "ACTIVITYDATE",
  "ACTIVITYTYPEID",
  "PRIMARYATTRIBUTEVALUE",
  "PRIMARYATTRIBUTEVALUEID",
  "CAMPAIGNID",
  "NAME",
  "Value",
  replace("NAME",'placeholder_1','placeholder_2')
AS "UP_NAME"
FROM ((SELECT
    "res".VALUE:"id"::number as "ID",
    "res".VALUE:"marketoGUID"::number as "MARKETOGUID",
    "res".VALUE:"leadId"::number as "LEADID",
    "res".VALUE:"activityDate"::timestamp as "ACTIVITYDATE",
    "res".VALUE:"activityTypeId"::number as "ACTIVITYTYPEID",
    "res".VALUE:"primaryAttributeValue"::varchar as "PRIMARYATTRIBUTEVALUE",
    "res".VALUE:"primaryAttributeValueId"::number as "PRIMARYATTRIBUTEVALUEID",
    "res".VALUE:"campaignId"::number as "CAMPAIGNID",
    "att".VALUE:"name"::varchar as "NAME",
    "att".VALUE:"value"::varchar as "Value"
FROM
    (SELECT
      "Data Value"
    FROM "RDS"."MARKETO"."STG_INTERESTING_MOMENTS") "FLATTEN_VARIANT_INPUT",
    lateral flatten(input=>"FLATTEN_VARIANT_INPUT"."Data Value":result) "res",
    lateral flatten(input=>"res".VALUE:attributes, recursive => true) "att"))))
 PIVOT
 (
 MAX("Value")
 FOR "UP_NAME" IN ('placeholder_3', 'placeholder_4', 'placeholder_5', 'placeholder_6')
 ) AS P (ID, MARKETOGUID, LEADID, ACTIVITYDATE, ACTIVITYTYPEID, PRIMARYATTRIBUTEVALUE, PRIMARYATTRIBUTEVALUEID, CAMPAIGNID, NAME, Campaign, Source, Date, Description)))))
GROUP BY ( "ID" )))))) as "input" on "target"."ID"="input"."ID" when matched then update set "ID" = "input"."ID", "MARKETOGUID" = "input"."MARKETOGUID", "LEADID" = "input"."LEADID", "ACTIVITYDATE" = "input"."ACTIVITYDATE", "ACTIVITYTYPEID" = "input"."ACTIVITYTYPEID", "PRIMARYATTRIBUTEVALUEID" = "input"."PRIMARYATTRIBUTEVALUEID", "PRIMARYATTRIBUTEVALUE" = "input"."PRIMARYATTRIBUTEVALUE", "CAMPAIGN" = "input"."CAMPAIGN", "DATE" = "input"."DATE", "DESCRIPTION" = "input"."DESCRIPTION", "SOURCE" = "input"."SOURCE", "CAMPAIGNID" = "input"."CAMPAIGNID", "ETL_UPDATE_DATE" = "input"."ETL_UPDATE_DATE" when not matched then insert ("ID","MARKETOGUID","LEADID","ACTIVITYDATE","ACTIVITYTYPEID","PRIMARYATTRIBUTEVALUEID","PRIMARYATTRIBUTEVALUE","CAMPAIGN","DATE","DESCRIPTION","SOURCE","CAMPAIGNID","ETL_INSERT_DATE","ETL_UPDATE_DATE","ETL_DELETE_DATE") values ("input"."ID","input"."MARKETOGUID","input"."LEADID","input"."ACTIVITYDATE","input"."ACTIVITYTYPEID","input"."PRIMARYATTRIBUTEVALUEID","input"."PRIMARYATTRIBUTEVALUE","input"."CAMPAIGN","input"."DATE","input"."DESCRIPTION","input"."SOURCE","input"."CAMPAIGNID","input"."ETL_INSERT_DATE","input"."ETL_UPDATE_DATE","input"."ETL_DELETE_DATE")"""
    # SqlFluff: IndexError - tuple index out of range (utils.py:43)
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.marketo.stg_interesting_moments"},  # source_tables
        {"rds.marketo.interesting_moments"},  # target_tables
        dialect="snowflake",
        test_sqlfluff=False,
        skip_graph_check=True,
    )


def test_sqlglot_limitations_rds_dynamics365_appointments_q54():
    """sqlglot limitations - Query 54"""
    sql = """ insert into RDS.DYNAMICS365.TABLES_DELETED_RECORDS_ID ( SCHEMA ,  STORED_PROCEDURE ,  SOURCE_TABLE_NAME ,  OBJECT_ID ,  TIME_STAMP )
    select 'placeholder_1' , 'placeholder_2' , 'placeholder_3' , "ACTIVITYID" ,  CURRENT_TIMESTAMP
    FROM RDS.DYNAMICS365.APPOINTMENTS
    where "ACTIVITYID" IN (select distinct OBJECTID FROM "RDS"."DYNAMICS365"."AUDITS" WHERE "ACTION"='placeholder_4' and "OPERATION" = 'placeholder_5' AND LOWER( "OBJECTTYPECODE" ) = 'placeholder_6' AND CAST( "CREATEDON" AS DATE ) >=DATEADD(DAY, 'placeholder_7', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.dynamics365.appointments", "rds.dynamics365.audits"},  # source_tables
        {"rds.dynamics365.tables_deleted_records_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_sqlglot_limitations_query_q63():
    """sqlglot limitations - Query 63"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_TARGET_COUNT = 2 WHERE TARGET_SCHEMA = 'placeholder_3' AND                                     TARGET_TABLE_NAME = 'placeholder_4'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q71():
    """sqlglot limitations - Query 71"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."EM_SALES_ACCOUNT_RT" AS SELECT * FROM "EDW_LS"."SALES_EM"."MVB_EM_SALES_ACCOUNT_RT" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.sales_em.mvb_em_sales_account_rt"},  # source_tables
        {"mat.matl.em_sales_account_rt"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_rds__q81():
    """sqlglot limitations - Query 81"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."PARTNER_PORTAL"."U_4C_METRIC_DEFINITION" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."PARTNER_PORTAL"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.partner_portal.sys_audit_delete",
            "rds.partner_portal.u_4c_metric_definition",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_sqlglot_limitations_rds__q94():
    """sqlglot limitations - Query 94"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."DATACENTER"."CMDB_CI_DB_MYSQL_INSTANCE" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."DATACENTER"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.datacenter.cmdb_ci_db_mysql_instance",
            "rds.datacenter.sys_audit_delete",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_sqlglot_limitations_query_q101():
    """sqlglot limitations - Query 101"""
    sql = """ UPDATE NOC.CONFIG."ETL_RDS_CONFIG_RECON"
SET LAST_RDS_JOB_RUN_ID='2025-01-01 00:00:00',
    TOTAL_SOURCE_COUNT=2,
    TOTAL_TARGET_COUNT=3,
    ETL_UPDATE_DATE=current_timestamp()
    WHERE RDS_CONFIG_ID='2025-01-01 00:00:00'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_selfserve_platform_perf_surf_perf_test_details_q114():
    """sqlglot limitations - Query 114"""
    sql = """ UPDATE SELFSERVE.PLATFORM_PERF.SYS_LOG_TRANSACTION_SSOQA2_SSOUAT_STREAM_TEMP TEMP
SET TEMP.TRACK=STR.TRACK,
         TEMP.SUB_TRACK=STR.SUB_TRACK,
              TEMP.APPLICATION_NAME=STR.APPLICATION_NAME,
                   TEMP.RELEASE_NAME=STR.RELEASE_NAME,
                        TEMP.TEST_ID=STR.TEST_ID,
                             TEMP.VALID=STR.VALID,
                                  TEMP.EXECUTION_TAG=STR.EXECUTION_TAG,
                                        TEMP.INSTANCE=STR.INSTANCE
FROM SELFSERVE.PLATFORM_PERF.SURF_PERF_TEST_DETAILS STR
WHERE TEMP.CREATED_DATE_TIME BETWEEN DATEADD(minute, 'placeholder_1', STR.TEST_STARTTIME) AND DATEADD(minute, 'placeholder_2', STR.TEST_ENDEDTIME) AND STR.INSTANCE IN ('placeholder_3','placeholder_4')"""
    assert_table_lineage_equal(
        sql,
        {"selfserve.platform_perf.surf_perf_test_details"},  # source_tables
        {
            "selfserve.platform_perf.sys_log_transaction_ssoqa2_ssouat_stream_temp"
        },  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_cdl_ls__q116():
    """sqlglot limitations - Query 116"""
    sql = """ CREATE OR REPLACE TEMPORARY TABLE CDL_LS."FINANCE_REVENUE_RPT"."TEMP_RPT_CONTRACT_DETAILS_MASTER_NULLITEM" AS
            SELECT "Projection_8"."FPLTC_AuthorizationNumber" as "FPLTC_AuthorizationNumber",
            "Join_13"."Contract_WBSElement" as "Contract_WBSElement",
            "Join_13"."CC_BundleLevelMaterial" as "CC_BundleLevelMaterial",
            "Join_13"."CC_BundleLevelItem" as "CC_BundleLevelItem",
            "Join_13"."RPLNR" as "RPLNR",
            "Join_13"."Contract_OpportunityID" as "Contract_OpportunityID",
            "Join_13"."Contract_ContractEndDateNullItem" as "Contract_ContractEndDateNullItem",
            "Join_13"."Contract_ContractStartDateNullItem" as "Contract_ContractStartDateNullItem",
            "Join_13"."Contract_ContractSignedDateNullItem" as "Contract_ContractSignedDateNullItem",
            "Join_13"."Contract_ProductTypeDescriptionNullItem" as "Contract_ProductTypeDescriptionNullItem",
            "Join_13"."Contract_ProductTypeNullItem" as "Contract_ProductTypeNullItem",
            "Join_13"."Contract_ContractTypeDescriptionNullItem" as "Contract_ContractTypeDescriptionNullItem",
            "Join_13"."Contract_ProductNullItem" as "Contract_ProductNullItem",
            "Join_13"."Contract_OrderFormNullItem" as "Contract_OrderFormNullItem",
            "Join_13"."Sales_Document" as "Sales_Document",
            "Join_13"."Contract_DocumentTypeNullItem" as "Contract_DocumentTypeNullItem",
            "Join_13"."Contract_CustomerPOIDNotItem" as "Contract_CustomerPOIDNotItem",
            "Join_13"."Contract_OnPremiseDescriptionNullItem" as "Contract_OnPremiseDescriptionNullItem",
            "Join_13"."Contract_PaymentTermsNullItem" as "Contract_PaymentTermsNullItem",
            "Join_13"."Contract_InvoiceTermsNullItem" as "Contract_InvoiceTermsNullItem",
            "Join_13"."Contract_OriginalContractTermsNullItem" as "Contract_OriginalContractTermsNullItem",
            "Join_13"."Contract_WorkItemIDNullItem" as "Contract_WorkItemIDNullItem",
            "Join_13"."Contract_HeaderBillBlockNullItem" as "Contract_HeaderBillBlockNullItem",
            "Join_13"."Contract_TravelExpensePOIDNullItem" as "Contract_TravelExpensePOIDNullItem",
            "Join_13"."Contract_MultiElementFlagNullItem" as "Contract_MultiElementFlagNullItem",
            "Join_13"."Contract_ContingencyRevFlagNullItem" as "Contract_ContingencyRevFlagNullItem",
            "Join_13"."Contract_DeploymentNumberNullItem" as "Contract_DeploymentNumberNullItem",
            "Join_13"."OptyLineItemNumber" as "OptyLineItemNumber" FROM
            (SELECT "Aggregation_3"."Sales_Document" as "Sales_Document",
            "ContractNullItem"."Contract_OrderFormNullItem" as "Contract_OrderFormNullItem",
            "ContractNullItem"."Contract_ProductNullItem" as "Contract_ProductNullItem",
            "ContractNullItem"."Contract_ContractTypeDescriptionNullItem" as "Contract_ContractTypeDescriptionNullItem",
            "ContractNullItem"."Contract_ProductTypeNullItem" as "Contract_ProductTypeNullItem",
            "ContractNullItem"."Contract_ProductTypeDescriptionNullItem" as "Contract_ProductTypeDescriptionNullItem",
            "ContractNullItem"."Contract_ContractSignedDateNullItem" as "Contract_ContractSignedDateNullItem",
            "ContractNullItem"."Contract_ContractStartDateNullItem" as "Contract_ContractStartDateNullItem",
            "ContractNullItem"."Contract_ContractEndDateNullItem" as "Contract_ContractEndDateNullItem",
            "ContractNullItem"."Contract_OpportunityID" as "Contract_OpportunityID",
            "ContractNullItem"."RPLNR" as "RPLNR",
            "ContractNullItem"."CC_BundleLevelItem" as "CC_BundleLevelItem",
            "ContractNullItem"."CC_BundleLevelMaterial" as "CC_BundleLevelMaterial",
            "ContractNullItem"."Contract_WBSElement" as "Contract_WBSElement",
            "ContractNullItem"."Sales_Document" as "Sales_Document_1",
            "Aggregation_3"."CC_ItemToString" as "Item",
            "ContractNullItem"."Item" as "Item_1",
            "ContractNullItem"."Contract_DocumentTypeNullItem" as "Contract_DocumentTypeNullItem",
            "ContractNullItem"."Contract_CustomerPOIDNotItem" as "Contract_CustomerPOIDNotItem",
            "ContractNullItem"."Contract_OnPremiseDescriptionNullItem" as "Contract_OnPremiseDescriptionNullItem",
            "ContractNullItem"."Contract_PaymentTermsNullItem" as "Contract_PaymentTermsNullItem",
            "ContractNullItem"."CC_ContractInvoiceTermsNullItem" as "Contract_InvoiceTermsNullItem",
            "ContractNullItem"."Contract_OriginalContractTermsNullItem" as "Contract_OriginalContractTermsNullItem",
            "ContractNullItem"."CC_ContractWorkItemIDNullItem" as "Contract_WorkItemIDNullItem",
            "ContractNullItem"."Contract_HeaderBillBlockNullItem" as "Contract_HeaderBillBlockNullItem",
            "ContractNullItem"."Contract_TravelExpensePOIDNullItem" as "Contract_TravelExpensePOIDNullItem",
            "ContractNullItem"."Contract_MultiElementFlagNullItem" as "Contract_MultiElementFlagNullItem",
            "ContractNullItem"."Contract_ContingencyRevFlagNullItem" as "Contract_ContingencyRevFlagNullItem",
            "ContractNullItem"."Contract_DeploymentNumberNullItem" as "Contract_DeploymentNumberNullItem",
            "ContractNullItem"."OptyLineItemNumber" as "OptyLineItemNumber" FROM
            (SELECT "SalesDocument" as "Sales_Document",
            "SalesDocumentItem" as "Item",
            "OrderForm" as "Contract_OrderFormNullItem",
            "Material" as "Contract_ProductNullItem",
            "ContractTypeDesc" as "Contract_ContractTypeDescriptionNullItem",
            "MaterialGroup" as "Contract_ProductTypeNullItem",
            "MaterialGroupDescription" as "Contract_ProductTypeDescriptionNullItem",
            "ContractSignedDate" as "Contract_ContractSignedDateNullItem",
            "ContractStartDate" as "Contract_ContractStartDateNullItem",
            "ContractEndDate" as "Contract_ContractEndDateNullItem",
            "OpportunityID" as "Contract_OpportunityID",
            "PaymentCardPlanTypeNo" as "RPLNR",
            "PricingRefMaterial" as "UPMAT",
            "BundleLevelItem" as "UEPOS",
            "DeploymentNumber" as "Contract_DeploymentNumberNullItem",
            "WBSElement" as "Contract_WBSElement",
            "DocumentType" as "Contract_DocumentTypeNullItem",
            "CustomerPONumber" as "Contract_CustomerPOIDNotItem",
            "OnPremiseDesc" as "Contract_OnPremiseDescriptionNullItem",
            "TermsOfPayment" as "Contract_PaymentTermsNullItem",
            "OriginalContractTerms" as "Contract_OriginalContractTermsNullItem",
            "HeaderBillingBlock" as "Contract_HeaderBillBlockNullItem",
            "TravelExpensePO" as "Contract_TravelExpensePOIDNullItem",
            "MultiElement" as "Contract_MultiElementFlagNullItem",
            "ContingencyRev" as "Contract_ContingencyRevFlagNullItem",
            "SurfItemNumber" as "OptyLineItemNumber",
            "ContingencyFlagHdr" as "ContingencyFlagHdr",
            IFF(("UEPOS") IS NOT TRUE   or "UEPOS" != 'placeholder_2', "UEPOS", 'placeholder_3')  as "CC_BundleLevelItem",
            IFF(("UEPOS") IS NOT TRUE   or "UEPOS" != 'placeholder_5', "UPMAT", 'placeholder_6')  as "CC_BundleLevelMaterial",
            "ContingencyFlagHdr" as "CC_ContractInvoiceTermsNullItem",
            'placeholder_7' as "CC_ContractWorkItemIDNullItem" FROM CDL_LS."FINANCE_REVENUE_RPT"."RPT_CONTRACT_DETAILS_MASTER")"ContractNullItem"
            RIGHT JOIN
            (SELECT "Sales_Document" as "Sales_Document",
            MIN("CC_ItemToNumber_INT")  as "CC_ItemToNumber",
            (IFF(LENGTH(("CC_ItemToNumber") :: VARCHAR('placeholder_8'))  = 'placeholder_9', 'placeholder_10' || ("CC_ItemToNumber":: VARCHAR('placeholder_11')) , (IFF(LENGTH(("CC_ItemToNumber") :: VARCHAR('placeholder_12')  )  = 'placeholder_13', 'placeholder_14' || ("CC_ItemToNumber":: VARCHAR('placeholder_15')) , (IFF(LENGTH(("CC_ItemToNumber") :: VARCHAR('placeholder_16')  )  = 'placeholder_17', 'placeholder_18' || ("CC_ItemToNumber":: VARCHAR('placeholder_19')) , (IFF(LENGTH(("CC_ItemToNumber") :: VARCHAR('placeholder_20')  )  = 'placeholder_21', 'placeholder_22' || ("CC_ItemToNumber":: VARCHAR('placeholder_23')) , (IFF(LENGTH(("CC_ItemToNumber") :: VARCHAR('placeholder_24')  )  = 'placeholder_25', 'placeholder_26' || ("CC_ItemToNumber":: VARCHAR('placeholder_27')) , ("CC_ItemToNumber":: VARCHAR('placeholder_28')) ) ) ) ) ) ) ) ) ) :: VARCHAR('placeholder_29'))  as "CC_ItemToString" FROM
            (SELECT "SalesDocument" as "Sales_Document",
            "SalesDocumentItem" as "Item",
            ("Item") :: INT   as "CC_ItemToNumber_INT" FROM CDL_LS."FINANCE_REVENUE_RPT"."RPT_CONTRACT_DETAILS_MASTER")"Projection_10"
            GROUP BY
            "Sales_Document"
            --"CC_ItemToString"
            )"Aggregation_3"
            ON "ContractNullItem"."Sales_Document" = "Aggregation_3"."Sales_Document" AND "ContractNullItem"."Item" = "Aggregation_3"."CC_ItemToString")"Join_13"
            LEFT JOIN
            (SELECT "FPLTC_Client" as "FPLTC_Client",
            "FPLTC_BillingPlanNumber" as "FPLTC_BillingPlanNumber",
            "FPLTC_BillingPlanItem" as "FPLTC_BillingPlanItem",
            "FPLTC_AuthorizationNumber" as "FPLTC_AuthorizationNumber" FROM EDW_LS."FINANCE_AR_EM"."EM_PAYMENT_CARDS_TRANSACTION_DATA_SD"
            WHERE "FPLTC_BillingPlanItem" = 'placeholder_30' )"Projection_8"
            ON "Join_13"."RPLNR" = "Projection_8"."FPLTC_BillingPlanNumber"
             --ADDED TO FETCH UNIQUE RECORDS
            Qualify row_number () over(partition by "Sales_Document" order by "Contract_ContractStartDateNullItem" desc, "OptyLineItemNumber" asc)='2025-01-01 00:00:00'"""
    assert_table_lineage_equal(
        sql,
        {
            "cdl_ls.finance_revenue_rpt.rpt_contract_details_master",
            "edw_ls.finance_ar_em.em_payment_cards_transaction_data_sd",
        },  # source_tables
        {
            "cdl_ls.finance_revenue_rpt.temp_rpt_contract_details_master_nullitem"
        },  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_edw_ls_product_compliance_em_job_bd_files_q117():
    """sqlglot limitations - Query 117"""
    sql = """ UPDATE EDW_LS.PRODUCT_COMPLIANCE_EM.TBL_BD_FILES_ARRIVAL_CHECK AR
        SET AR.FILE_NAME = BD.NAME,
            AR.SIZE = BD.SIZE,
            AR.LAST_MODIFIED = BD.LAST_MODIFIED,
            AR.FILE_DATE = BD.FILE_DATE,
            AR.CREATED_TS = BD.CREATED_TS,
            AR.FILE_ARRIVED_FLAG = '2025-01-01 00:00:00'
        FROM EDW_LS.PRODUCT_COMPLIANCE_EM.JOB_BD_FILES BD
        WHERE AR.SEQNO = BD.SEQNO
        AND AR.TABLE_NAME = BD.TABLENAME
        AND TO_DATE(BD.CREATED_TS) = CURRENT_DATE
        AND BD.NAME IS NOT TRUE
        AND AR.FILE_NAME IS TRUE"""
    assert_table_lineage_equal(
        sql,
        {"edw_ls.product_compliance_em.job_bd_files"},  # source_tables
        {"edw_ls.product_compliance_em.tbl_bd_files_arrival_check"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q124():
    """sqlglot limitations - Query 124"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."EM_PR_SOURCING_DETAILS" AS SELECT * FROM "EDW_LS"."FINANCE_PTP_EM"."MVB_EM_PR_SOURCING_DETAILS" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.finance_ptp_em.mvb_em_pr_sourcing_details"},  # source_tables
        {"mat.matl.em_pr_sourcing_details"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q136():
    """sqlglot limitations - Query 136"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."PSSERVICES_COMMITS" AS SELECT * FROM "EDW_LS"."CUSTOMER_PSA_EM"."MVB_PSSERVICES_COMMITS" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.customer_psa_em.mvb_psservices_commits"},  # source_tables
        {"mat.matl.psservices_commits"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q142():
    """sqlglot limitations - Query 142"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."UTILIZATION_ACTUALS_PSANEW" AS SELECT * FROM "EDW_LS"."CUSTOMER_PSANEW_EM"."MVB_UTILIZATION_ACTUALS" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.customer_psanew_em.mvb_utilization_actuals"},  # source_tables
        {"mat.matl.utilization_actuals_psanew"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q148():
    """sqlglot limitations - Query 148"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."RPT_DS_MONTHLY_RECOMMENDATIONS_CD" AS SELECT * FROM "CDL_LS"."CUSTOMER_CD_RPT"."MVB_RPT_DS_MONTHLY_RECOMMENDATIONS_CD" """
    assert_table_lineage_equal(
        sql,
        {
            "cdl_ls.customer_cd_rpt.mvb_rpt_ds_monthly_recommendations_cd"
        },  # source_tables
        {"mat.matl.rpt_ds_monthly_recommendations_cd"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q150():
    """sqlglot limitations - Query 150"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."CD_ALERT_RECOMMENDATION_PAGE_SUCCESS_PLAYS_INDEX" AS SELECT * FROM "EDW_LS"."CUSTOMER_CD_EM"."MVB_CD_ALERT_RECOMMENDATION_PAGE_SUCCESS_PLAYS_INDEX" """
    assert_table_lineage_equal(
        sql,
        {
            "edw_ls.customer_cd_em.mvb_cd_alert_recommendation_page_success_plays_index"
        },  # source_tables
        {"mat.matl.cd_alert_recommendation_page_success_plays_index"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_query_q164():
    """sqlglot limitations - Query 164"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."RPT_VENDOR_SPEND_ANALYTICS" AS SELECT * FROM "CDL_LS"."FINANCE_PTP_RPT"."MVB_RPT_VENDOR_SPEND_ANALYTICS" """
    assert_table_lineage_equal(
        sql,
        {"cdl_ls.finance_ptp_rpt.mvb_rpt_vendor_spend_analytics"},  # source_tables
        {"mat.matl.rpt_vendor_spend_analytics"},  # target_tables
        dialect="snowflake",
    )


def test_sqlglot_limitations_rds__q169():
    """sqlglot limitations - Query 169"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."CMDB_CI_RPA_PROCESS" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.surf.cmdb_ci_rpa_process", "rds.surf.sys_audit_delete"},  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_sqlglot_limitations_rds__q177():
    """sqlglot limitations - Query 177"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."LEARNING_HUB"."SN_LXP_CONTENT_BASE" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."LEARNING_HUB"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.learning_hub.sn_lxp_content_base",
            "rds.learning_hub.sys_audit_delete",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )
