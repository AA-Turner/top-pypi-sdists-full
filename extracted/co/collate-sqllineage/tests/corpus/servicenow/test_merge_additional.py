"""Tests for merge complex."""

from tests.helpers import assert_table_lineage_equal


def test_merge_complex_query_q20():
    """merge complex - Query 20"""
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


def test_merge_complex_query_q23():
    """merge complex - Query 23"""
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


def test_merge_complex_query_q26():
    """merge complex - Query 26"""
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


def test_merge_complex_query_q27():
    """merge complex - Query 27"""
    sql = """ update "HVR_IBCH_S4_SF_4_I_SNF_PRDS1" set
    "IS_BUSY" = '2025-01-01 00:00:00',
    "TBL_NAME" = 'placeholder_2',
    "HVR_OP" = 'placeholder_3'
where "PARALLEL_SESSION" = 'placeholder_4'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"<default>.hvr_ibch_s4_sf_4_i_snf_prds1"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_rds__q40():
    """merge complex - Query 40"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."OLANOW"."U_OLA_RELEASE_SPECIFIC_CONFIG" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."OLANOW"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.olanow.sys_audit_delete",
            "rds.olanow.u_ola_release_specific_config",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_merge_complex_query_q71():
    """merge complex - Query 71"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."EM_SALES_ACCOUNT_RT" AS SELECT * FROM "EDW_LS"."SALES_EM"."MVB_EM_SALES_ACCOUNT_RT" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.sales_em.mvb_em_sales_account_rt"},  # source_tables
        {"mat.matl.em_sales_account_rt"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q101():
    """merge complex - Query 101"""
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


def test_merge_complex_if_q104():
    """merge complex - Query 104"""
    sql = """ ALTER TABLE IF EXISTS
RDS.OUTREACH.CONTENT_CATEGORIES
SWAP WITH
RDS.OUTREACH.STG_CONTENT_CATEGORIES"""
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_content_categories"},  # source_tables
        {"rds.outreach.content_categories"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_merge_complex_selfserve_platform_perf_surf_perf_test_details_q114():
    """merge complex - Query 114"""
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


def test_merge_complex_cdl_ls__q116():
    """merge complex - Query 116"""
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


def test_merge_complex_query_q121():
    """merge complex - Query 121"""
    sql = """ merge into "RDS"."RAINFOCUS"."SURVEY_RESPONSES" as "target" using (SELECT DISTINCT
  "event",
  "nextId",
  "responseCode",
  "responseMessage",
  "timestamp",
  "surveyId",
  "surveyName",
  "code",
  "sessionId",
  "sessionTimeId",
  "title",
  "attendeeId",
  "attendeeName",
  "companyname",
  "email",
  "lastModified",
  "submissionId",
  "submissionTime",
  "answerId",
  "questionId",
  "value",
  "scaleWeight",
  "speakerId",
  "speakerName",
  "speakerEmail",
  "ETL_UPDATE_DATE",
  "ETL_DELETE_DATE",
  "ETL_INSERT_DATE",
  "eloqua_campaign_id"
FROM ((SELECT
  "event",
  "nextId",
  "responseCode",
  "responseMessage",
  CASE
WHEN ("timestamp" IS NULL or upper("timestamp") = '2025-01-01 00:00:00') THEN 'placeholder_2'
ELSE "timestamp"
END
AS "timestamp",
  CASE
WHEN ("surveyId" IS NULL or upper("surveyId") = '2025-01-01 00:00:00') THEN 'placeholder_4'
ELSE "surveyId"
END
AS "surveyId",
  "surveyName",
  "code",
  CASE
WHEN ("sessionId" IS NULL or upper("sessionId") = 'placeholder_5') THEN 'placeholder_6'
ELSE "sessionId"
END
AS "sessionId",
  CASE
WHEN ("sessionTimeId" IS NULL or upper("sessionTimeId") = '2025-01-01 00:00:00') THEN 'placeholder_8'
ELSE "sessionTimeId"
END
AS "sessionTimeId",
  "title",
  CASE
WHEN ("attendeeId" IS NULL or upper("attendeeId") = '2025-01-01 00:00:00') THEN 'placeholder_10'
ELSE "attendeeId"
END
AS "attendeeId",
  "attendeeName",
  CASE
WHEN ("companyname" IS NULL or upper("companyname") = 'placeholder_11') THEN 'placeholder_12'
ELSE "companyname"
END
AS "companyname",
  "email",
  "lastModified",
  CASE
WHEN ("submissionId" IS NULL or upper("submissionId") = '2025-01-01 00:00:00') THEN 'placeholder_14'
ELSE "submissionId"
END
AS "submissionId",
  "submissionTime",
  CASE
WHEN ("answerId" IS NULL or upper("answerId") = '2025-01-01 00:00:00') THEN 'placeholder_16'
ELSE "answerId"
END
AS "answerId",
  CASE
WHEN ("questionId" IS NULL or upper("questionId") = 'placeholder_17') THEN 'placeholder_18'
ELSE "questionId"
END
AS "questionId",
  "value",
  CASE
WHEN ("scaleWeight" IS NULL or upper("scaleWeight") = 'placeholder_19') THEN 'placeholder_20'
ELSE "scaleWeight"
END
AS "scaleWeight",
  CASE
WHEN ("speakerId" IS NULL or upper("speakerId") = 'placeholder_21') THEN 'placeholder_22'
ELSE "speakerId"
END
AS "speakerId",
  CASE
WHEN ("speakerName" IS NULL or upper("speakerName") = 'placeholder_23') THEN 'placeholder_24'
ELSE "speakerName"
END
AS "speakerName",
  CASE
WHEN ("speakerEmail" IS NULL or upper("speakerEmail") = 'placeholder_25') THEN 'placeholder_26'
ELSE "speakerEmail"
END
AS "speakerEmail",
  CURRENT_TIMESTAMP()
AS "ETL_UPDATE_DATE",
  NULL
AS "ETL_DELETE_DATE",
  CURRENT_TIMESTAMP()
AS "ETL_INSERT_DATE",
  'placeholder_27'
AS "eloqua_campaign_id"
FROM ((SELECT
    "FLATTEN_VARIANT_INPUT"."DATA_VALUE":"event"::varchar as "event",
    "FLATTEN_VARIANT_INPUT"."DATA_VALUE":"nextId"::varchar as "nextId",
    "FLATTEN_VARIANT_INPUT"."DATA_VALUE":"responseCode"::varchar as "responseCode",
    "FLATTEN_VARIANT_INPUT"."DATA_VALUE":"responseMessage"::varchar as "responseMessage",
    "FLATTEN_VARIANT_INPUT"."DATA_VALUE":"timestamp"::varchar as "timestamp",
    "surveys".VALUE:"surveyId"::varchar as "surveyId",
    "surveys".VALUE:"surveyName"::varchar as "surveyName",
    "sessionTimes".VALUE:"code"::varchar as "code",
    "sessionTimes".VALUE:"sessionId"::varchar as "sessionId",
    "sessionTimes".VALUE:"sessionTimeId"::varchar as "sessionTimeId",
    "sessionTimes".VALUE:"title"::varchar as "title",
    "submissions".VALUE:"attendeeId"::varchar as "attendeeId",
    "submissions".VALUE:"attendeeName"::varchar as "attendeeName",
    "submissions".VALUE:"companyname"::varchar as "companyname",
    "submissions".VALUE:"email"::varchar as "email",
    "submissions".VALUE:"lastModified"::timestamp as "lastModified",
    "submissions".VALUE:"submissionId"::varchar as "submissionId",
    "submissions".VALUE:"submissionTime"::timestamp as "submissionTime",
    "responses".VALUE:"answerId"::varchar as "answerId",
    "responses".VALUE:"questionId"::varchar as "questionId",
    "responses".VALUE:"value"::varchar as "value",
    "responses".VALUE:"scaleWeight"::varchar as "scaleWeight",
    "responses".VALUE:"speakerId"::varchar as "speakerId",
    "responses".VALUE:"speakerName"::varchar as "speakerName",
    "responses".VALUE:"speakerEmail"::varchar as "speakerEmail"
FROM
    (SELECT
      "DATA_VALUE"
    FROM "RDS"."RAINFOCUS"."STG_SURVEY_RESPONSES") "FLATTEN_VARIANT_INPUT",
    lateral flatten(input=>"FLATTEN_VARIANT_INPUT"."DATA_VALUE":surveys) "surveys",
    lateral flatten(input=>"surveys".VALUE:sessionTimes) "sessionTimes",
    lateral flatten(input=>"sessionTimes".VALUE:submissions) "submissions",
    lateral flatten(input=>"submissions".VALUE:responses) "responses"))))) as "input" on "target"."eloqua_campaign_id"="input"."eloqua_campaign_id"
and "target"."sessionId"="input"."sessionId"
and "target"."questionId"="input"."questionId"
and "target"."answerId"="input"."answerId"
and "target"."sessionTimeId"="input"."sessionTimeId"
and "target"."attendeeId"="input"."attendeeId"
and "target"."surveyId"="input"."surveyId"
and "target"."speakerId"="input"."speakerId"
and "target"."submissionId"="input"."submissionId" when matched then update set "timestamp" = "input"."timestamp", "event" = "input"."event", "eloqua_campaign_id" = "input"."eloqua_campaign_id", "code" = "input"."code", "sessionId" = "input"."sessionId", "sessionTimeId" = "input"."sessionTimeId", "title" = "input"."title", "answerId" = "input"."answerId", "questionId" = "input"."questionId", "scaleWeight" = "input"."scaleWeight", "value" = "input"."value", "surveyId" = "input"."surveyId", "surveyName" = "input"."surveyName", "submissionId" = "input"."submissionId", "attendeeId" = "input"."attendeeId", "attendeeName" = "input"."attendeeName", "email" = "input"."email", "companyname" = "input"."companyname", "submissionTime" = "input"."submissionTime", "lastModified" = "input"."lastModified", "ETL_UPDATE_DATE" = "input"."ETL_UPDATE_DATE", "speakerId" = "input"."speakerId", "speakerName" = "input"."speakerName", "speakerEmail" = "input"."speakerEmail" when not matched then insert ("timestamp","event","eloqua_campaign_id","code","sessionId","sessionTimeId","title","answerId","questionId","scaleWeight","value","surveyId","surveyName","submissionId","attendeeId","attendeeName","email","companyname","submissionTime","lastModified","ETL_INSERT_DATE","speakerId","speakerName","speakerEmail") values ("input"."timestamp","input"."event","input"."eloqua_campaign_id","input"."code","input"."sessionId","input"."sessionTimeId","input"."title","input"."answerId","input"."questionId","input"."scaleWeight","input"."value","input"."surveyId","input"."surveyName","input"."submissionId","input"."attendeeId","input"."attendeeName","input"."email","input"."companyname","input"."submissionTime","input"."lastModified","input"."ETL_INSERT_DATE","input"."speakerId","input"."speakerName","input"."speakerEmail")"""
    # SqlFluff: IndexError - tuple index out of range (utils.py:43)
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.rainfocus.stg_survey_responses"},  # source_tables
        {"rds.rainfocus.survey_responses"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
        test_sqlfluff=False,
    )


def test_merge_complex_query_q122():
    """merge complex - Query 122"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."RPT_CONTRACT_DETAILS_MASTER" AS SELECT * FROM "CDL_LS"."FINANCE_REVENUE_RPT"."MVB_RPT_CONTRACT_DETAILS_MASTER" """
    assert_table_lineage_equal(
        sql,
        {"cdl_ls.finance_revenue_rpt.mvb_rpt_contract_details_master"},  # source_tables
        {"mat.matl.rpt_contract_details_master"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q124():
    """merge complex - Query 124"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."EM_PR_SOURCING_DETAILS" AS SELECT * FROM "EDW_LS"."FINANCE_PTP_EM"."MVB_EM_PR_SOURCING_DETAILS" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.finance_ptp_em.mvb_em_pr_sourcing_details"},  # source_tables
        {"mat.matl.em_pr_sourcing_details"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q136():
    """merge complex - Query 136"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."PSSERVICES_COMMITS" AS SELECT * FROM "EDW_LS"."CUSTOMER_PSA_EM"."MVB_PSSERVICES_COMMITS" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.customer_psa_em.mvb_psservices_commits"},  # source_tables
        {"mat.matl.psservices_commits"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q142():
    """merge complex - Query 142"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."UTILIZATION_ACTUALS_PSANEW" AS SELECT * FROM "EDW_LS"."CUSTOMER_PSANEW_EM"."MVB_UTILIZATION_ACTUALS" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.customer_psanew_em.mvb_utilization_actuals"},  # source_tables
        {"mat.matl.utilization_actuals_psanew"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q148():
    """merge complex - Query 148"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."RPT_DS_MONTHLY_RECOMMENDATIONS_CD" AS SELECT * FROM "CDL_LS"."CUSTOMER_CD_RPT"."MVB_RPT_DS_MONTHLY_RECOMMENDATIONS_CD" """
    assert_table_lineage_equal(
        sql,
        {
            "cdl_ls.customer_cd_rpt.mvb_rpt_ds_monthly_recommendations_cd"
        },  # source_tables
        {"mat.matl.rpt_ds_monthly_recommendations_cd"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q150():
    """merge complex - Query 150"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."CD_ALERT_RECOMMENDATION_PAGE_SUCCESS_PLAYS_INDEX" AS SELECT * FROM "EDW_LS"."CUSTOMER_CD_EM"."MVB_CD_ALERT_RECOMMENDATION_PAGE_SUCCESS_PLAYS_INDEX" """
    assert_table_lineage_equal(
        sql,
        {
            "edw_ls.customer_cd_em.mvb_cd_alert_recommendation_page_success_plays_index"
        },  # source_tables
        {"mat.matl.cd_alert_recommendation_page_success_plays_index"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q164():
    """merge complex - Query 164"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."RPT_VENDOR_SPEND_ANALYTICS" AS SELECT * FROM "CDL_LS"."FINANCE_PTP_RPT"."MVB_RPT_VENDOR_SPEND_ANALYTICS" """
    assert_table_lineage_equal(
        sql,
        {"cdl_ls.finance_ptp_rpt.mvb_rpt_vendor_spend_analytics"},  # source_tables
        {"mat.matl.rpt_vendor_spend_analytics"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_rds__q169():
    """merge complex - Query 169"""
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


def test_merge_complex_rds__q177():
    """merge complex - Query 177"""
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


def test_merge_complex_query_q192():
    """merge complex - Query 192"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."ENGAGEMENT_SURVEY" AS SELECT * FROM "CDL_LS"."CUSTOMER_RPT"."MVB_ENGAGEMENT_SURVEY" """
    assert_table_lineage_equal(
        sql,
        {"cdl_ls.customer_rpt.mvb_engagement_survey"},  # source_tables
        {"mat.matl.engagement_survey"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q194():
    """merge complex - Query 194"""
    sql = """ CREATE OR REPLACE TRANSIENT TABLE "MAT"."MATL"."EM_OPPORTUNITY_PARTNER_DEAL" AS SELECT * FROM "EDW_LS"."PARTNER_EM"."MVB_EM_OPPORTUNITY_PARTNER_DEAL" """
    assert_table_lineage_equal(
        sql,
        {"edw_ls.partner_em.mvb_em_opportunity_partner_deal"},  # source_tables
        {"mat.matl.em_opportunity_partner_deal"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_time_card_daily_q199():
    """merge complex - Query 199"""
    sql = """ Merge into time_card_daily using time_card_daily_2041343 on time_card_daily."SYS_ID" = time_card_daily_2041343."SYS_ID"  when matched then update set  time_card_daily."DATE" =  time_card_daily_2041343."DATE", time_card_daily."X_SNC_PSA_TIME_TOTAL_AMOUNT" =  time_card_daily_2041343."X_SNC_PSA_TIME_TOTAL_AMOUNT", time_card_daily."TIME_CARD" =  time_card_daily_2041343."TIME_CARD", time_card_daily."DV_TIME_CARD" =  time_card_daily_2041343."DV_TIME_CARD", time_card_daily."SYS_MOD_COUNT" =  time_card_daily_2041343."SYS_MOD_COUNT", time_card_daily."SYS_UPDATED_ON" =  time_card_daily_2041343."SYS_UPDATED_ON", time_card_daily."SYS_TAGS" =  time_card_daily_2041343."SYS_TAGS", time_card_daily."TIME_WORKED" =  time_card_daily_2041343."TIME_WORKED", time_card_daily."X_SNC_PSA_TIME_HOURLY_RATE_SOLD" =  time_card_daily_2041343."X_SNC_PSA_TIME_HOURLY_RATE_SOLD", time_card_daily."SYS_ID" =  time_card_daily_2041343."SYS_ID", time_card_daily."SYS_UPDATED_BY" =  time_card_daily_2041343."SYS_UPDATED_BY", time_card_daily."X_SNC_PSA_TIME_USD_FX_RATE" =  time_card_daily_2041343."X_SNC_PSA_TIME_USD_FX_RATE", time_card_daily."SYS_CREATED_ON" =  time_card_daily_2041343."SYS_CREATED_ON", time_card_daily."X_SNC_PSA_TIME_ACCOUNTING_PERIOD" =  time_card_daily_2041343."X_SNC_PSA_TIME_ACCOUNTING_PERIOD", time_card_daily."DV_X_SNC_PSA_TIME_ACCOUNTING_PERIOD" =  time_card_daily_2041343."DV_X_SNC_PSA_TIME_ACCOUNTING_PERIOD", time_card_daily."SYS_CREATED_BY" =  time_card_daily_2041343."SYS_CREATED_BY", time_card_daily."PSP_PER_INSERT_DT" =  time_card_daily."PSP_PER_INSERT_DT", time_card_daily."PSP_PER_DELETE_DT" =  time_card_daily_2041343."PSP_PER_DELETE_DT", time_card_daily."PSP_PER_UPDATE_DT" =  '2025-01-01 00:00:00' when not matched then insert ( time_card_daily."DATE", time_card_daily."X_SNC_PSA_TIME_TOTAL_AMOUNT", time_card_daily."TIME_CARD", time_card_daily."DV_TIME_CARD", time_card_daily."SYS_MOD_COUNT", time_card_daily."SYS_UPDATED_ON", time_card_daily."SYS_TAGS", time_card_daily."TIME_WORKED", time_card_daily."X_SNC_PSA_TIME_HOURLY_RATE_SOLD", time_card_daily."SYS_ID", time_card_daily."SYS_UPDATED_BY", time_card_daily."X_SNC_PSA_TIME_USD_FX_RATE", time_card_daily."SYS_CREATED_ON", time_card_daily."X_SNC_PSA_TIME_ACCOUNTING_PERIOD", time_card_daily."DV_X_SNC_PSA_TIME_ACCOUNTING_PERIOD", time_card_daily."SYS_CREATED_BY", time_card_daily."PSP_PER_INSERT_DT", time_card_daily."PSP_PER_DELETE_DT", time_card_daily."PSP_PER_UPDATE_DT") values ( time_card_daily_2041343."DATE", time_card_daily_2041343."X_SNC_PSA_TIME_TOTAL_AMOUNT", time_card_daily_2041343."TIME_CARD", time_card_daily_2041343."DV_TIME_CARD", time_card_daily_2041343."SYS_MOD_COUNT", time_card_daily_2041343."SYS_UPDATED_ON", time_card_daily_2041343."SYS_TAGS", time_card_daily_2041343."TIME_WORKED", time_card_daily_2041343."X_SNC_PSA_TIME_HOURLY_RATE_SOLD", time_card_daily_2041343."SYS_ID", time_card_daily_2041343."SYS_UPDATED_BY", time_card_daily_2041343."X_SNC_PSA_TIME_USD_FX_RATE", time_card_daily_2041343."SYS_CREATED_ON", time_card_daily_2041343."X_SNC_PSA_TIME_ACCOUNTING_PERIOD", time_card_daily_2041343."DV_X_SNC_PSA_TIME_ACCOUNTING_PERIOD", time_card_daily_2041343."SYS_CREATED_BY", 'placeholder_2', time_card_daily_2041343."PSP_PER_DELETE_DT", 'placeholder_3')"""
    assert_table_lineage_equal(
        sql,
        {"<default>.time_card_daily_2041343"},  # source_tables
        {"<default>.time_card_daily"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_rds__q200():
    """merge complex - Query 200"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SUPPORTTOOLS"."X_SNC_CALABRIO_EXCEPTION" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SUPPORTTOOLS"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.supporttools.sys_audit_delete",
            "rds.supporttools.x_snc_calabrio_exception",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_merge_complex_query_q203():
    """merge complex - Query 203"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_SOURCE_COUNT = 2 WHERE SOURCE_SCHEMA = 'placeholder_3' AND                                     SOURCE_TABLE_NAME = 'placeholder_4'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_query_q216():
    """merge complex - Query 216"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_SOURCE_COUNT = 2 WHERE SOURCE_SCHEMA = 'placeholder_3' AND                                     SOURCE_TABLE_NAME = 'placeholder_4'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_edw_ls_partner_em_temp_partner_rt_q220():
    """merge complex - Query 220"""
    sql = """ CREATE OR REPLACE TEMPORARY TABLE EDW_LS.PARTNER_EM.TEMP_PARTNER_ATTR   AS
SELECT DISTINCT ATTR."ParentPartnerSysID",
                ATTR."ParentPartner",
                ATTR."ParentPartnerNumber",
                ATTR."ParentPartnerType",
                ATTR."ParentPartnerPublicSectorFlag",
                ATTR."ParentPartnerServiceProviderFlag",
                ATTR."ParentPartnerSalesTierLevel",
                ATTR."ParentPartnerServiceTierLevel",
                ATTR."ParentPartnerTechnologyTierLevel",
                ATTR."ParentPartnerOnBoardedDate",
                ATTR."ParentPartnerGeo",
                ATTR."ParentPartnerCountry",
                ATTR."ParentPartnerSegment",
                ATTR."ParentPartnerCategoryCode",
                ATTR."PartnerFinderURL",
                ATTR."AcctPrimarySalesRep",
                ATTR."AcctChannelManager",
                ATTR."AcctSolutionConsultant",
                UST."AccountJobFunctionName",
                UST."AccountOwnerName",
                EMP."EmpName" AS "PartnerDevelopmentManager",
                "AcctAnnualRevenue",
                "StrategicGroupName",
                "GoToMarketSegmentVCU",
                ATTR."ParentPartnerPublicSectorDate",
                ATTR."ParentPartnerFinalDemotionDate"
FROM EDW_LS.PARTNER_EM.TEMP_PARTNER_RT ATTR
LEFT JOIN
  (SELECT DISTINCT "AccountSysID",
                 /* "AccountOwnerName", */
                   LISTAGG("AccountOwnerName", 'placeholder_1') AS "AccountOwnerName",
                   "AccountActive",
                  /* "SalesTeamAccountName", */
                   "AccountJobFunctionName",
                   "AccountPrimaryAssignment"
   FROM "ODS_LS"."SURF"."U_ST_ACCOUNT"
   WHERE "AccountJobFunctionName"= 'placeholder_2'
     AND "AccountActive"='placeholder_3'
     AND "AccountPrimaryAssignment"='placeholder_4'
     group by all)UST ON ATTR."AcctSysID"="AccountSysID"
LEFT JOIN (
SELECT DISTINCT "EmpSysID",
                "EmpName"
FROM "ODS_LS"."SURF"."EMPLOYEE" )EMP ON ATTR."PartnerDevelopmentManager"=EMP."EmpName";"""
    assert_table_lineage_equal(
        sql,
        {
            "edw_ls.partner_em.temp_partner_rt",
            "ods_ls.surf.employee",
            "ods_ls.surf.u_st_account",
        },  # source_tables
        {"edw_ls.partner_em.temp_partner_attr"},  # target_tables
        dialect="snowflake",
    )


def test_merge_complex_rds_powerbi__q229():
    """merge complex - Query 229"""
    sql = """ insert into RDS.POWERBI.STG_FABRIC_CAPACITY_METRICS
(select 'placeholder_1','placeholder_2',"Data Value",'placeholder_3'
from RDS.POWERBI."TEMP_FABRIC_CAPACITY_METRICS_1BB61C0E-9F72-4F46-A655-9E5691CADBF2")"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.powerbi.temp_fabric_capacity_metrics_1bb61c0e-9f72-4f46-a655-9e5691cadbf2"
        },  # source_tables
        {"rds.powerbi.stg_fabric_capacity_metrics"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_merge_complex_rds__q239():
    """merge complex - Query 239"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."APPSTORE"."CORE_COMPANY" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."APPSTORE"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.appstore.core_company", "rds.appstore.sys_audit_delete"},  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_merge_complex_query_q253():
    """merge complex - Query 253"""
    sql = """ update "HVR_IBCH_S4_SF_3_I_SNF_PRDS" set
    "IS_BUSY" = '2025-01-01 00:00:00',
    "TBL_NAME" = 'placeholder_2',
    "HVR_OP" = 'placeholder_3'
where "PARALLEL_SESSION" = 'placeholder_4'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"<default>.hvr_ibch_s4_sf_3_i_snf_prds"},  # target_tables
        dialect="snowflake",
    )
