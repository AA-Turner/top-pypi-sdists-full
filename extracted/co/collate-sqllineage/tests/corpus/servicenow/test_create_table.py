"""Tests for create table."""

from tests.helpers import assert_table_lineage_equal


def test_create_table_query_q605():
    """create table - Query 605"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_TARGET_COUNT = 2 WHERE TARGET_SCHEMA = 'placeholder_3' AND                                     TARGET_TABLE_NAME = 'placeholder_4'"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
    )


def test_create_table_rds__q1460():
    """create table - Query 1460"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."LEARNING_HUB"."U_EMPLOYEE" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."LEARNING_HUB"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.learning_hub.sys_audit_delete",
            "rds.learning_hub.u_employee",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_rds__q3610():
    """create table - Query 3610"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."U_DNB" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.surf.sys_audit_delete", "rds.surf.u_dnb"},  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_query_q3954():
    """create table - Query 3954"""
    sql = """ insert into "EDW"."ENTERPRISE"."ETL_DUPLICATE_DATA_LOG" ("TARGET_OBJECT", "SOURCE_VIEW", "MERGE_KEY", "DUPLICATES_IDENTIFIED_TS") select "TARGET_OBJECT", "SOURCE_VIEW", "MERGE_KEY", "DUPLICATES_IDENTIFIED_TS" from (select
    "TARGET_OBJECT" as "TARGET_OBJECT",
    "SOURCE_VIEW" as "SOURCE_VIEW",
    "MERGE_KEY" as "MERGE_KEY",
    "DUPLICATES_IDENTIFIED_TS" as "DUPLICATES_IDENTIFIED_TS"
from (SELECT DISTINCT
  "TARGET_OBJECT",
  "SOURCE_VIEW",
  "MERGE_KEY",
  "DUPLICATES_IDENTIFIED_TS"
FROM ((SELECT
  CONCAT('placeholder_1','placeholder_2','placeholder_3','placeholder_4','placeholder_5')
AS "TARGET_OBJECT",
  'placeholder_6'
AS "SOURCE_VIEW",
  'placeholder_7'
AS "MERGE_KEY",
  current_timestamp()
AS "DUPLICATES_IDENTIFIED_TS"
FROM ((SELECT
  *
FROM ((SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY "COMMIT_ID"
                     ORDER BY "COMMIT_ID" ASC) AS "RNO"
FROM ((select * from (SELECT
  "COMMIT_QUARTER_ID",
  "COMMIT_QUARTER_DT",
  "COMMIT_QUARTER_YYQQ",
  "WEEK_ID",
  "WEEK_DT",
  "WEEK_NUMBER",
  "WEEK_RANK",
  "MAX_WEEK_NUMBER",
  "TERRITORY_ID",
  "GEO_ID",
  "OWNER_ID",
  "OWNER_NAME",
  "BU_ID",
  "COMMIT_ID",
  "COMMIT_TYPE",
  "COMMIT_USD",
  "COMMIT_CLOSETODATE_USD",
  "COMMIT_EXPECTEDTOCLOSETHISWEEK_USD",
  "COMMIT_EXPECT_USD",
  "COMMIT_EXPECTED_NEWLOGOS",
  "COMMIT_EXPECT_MONTH_USD",
  "COMMIT_UPSIDE_MONTH_USD",
  "COMMIT_MONTH_USD",
  "COMMIT_EXPECT_PSREVENUE_MONTH_USD",
  "COMMIT_EXPECT_PSREVENUE_USD",
  "COMMIT_UPSIDE_USD",
  "COMMIT_CLOSEDTOQUOTA_USD",
  "COMMIT_UPDATE_TS",
  "TERRITORY_SYSID",
  "OWNER_SYSID",
  "COMMIT_DSR_EXPECTEDTOCLOSETHISWEEK_USD",
  "COMMIT_DSR_EXPECTED_NEWLOGOS",
  "COMMIT_DSR_EXPECT_MONTH_USD",
  "COMMIT_DSR_EXPECT_USD",
  "COMMIT_DSR_MONTH_USD",
  "COMMIT_DSR_UPSIDE_MONTH_USD",
  "COMMIT_DSR_UPSIDE_USD",
  "COMMIT_DSR_USD",
  "COMMIT_NOTES",
  "DSR_MARKET_SEGMENTATION",
  "EXPECT_NOTES",
  "UPSIDE_NOTES"
FROM "EDW"."SALES"."STG_FACT_COMMIT_W") where LEFT(COMMIT_QUARTER_YYQQ,'placeholder_8') = SUBSTR(convert_timezone('placeholder_9',current_timestamp),'placeholder_10','placeholder_11')
))))
WHERE ("RNO" = '2025-01-01 00:00:00')))))))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"edw.sales.stg_fact_commit_w"},  # source_tables
        {"edw.enterprise.etl_duplicate_data_log"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_edw_ls__q4082():
    """create table - Query 4082"""
    sql = """ INSERT INTO EDW_LS."PRODUCT_EM"."U_CUSTOMER_PRODUCT_PROFILE_STAGE_MASTER"
SELECT DISTINCT account_number,
                account_name,
                customer_product_profile_sys_id,
                customer_profile_sys_id,
                application_sys_id,
                app_name,
                esm_name,
                license_active_flag,
                licensed_first_date,
                current_contract,
                current_contract_sys_id,
                license_inactive_flag,
                opportunity_pipeline_flag,
                opportunity_count,
                deployment_scheduled_flag,
                deployment_scheduled_next,
                deployment_scheduled_next_sys_id,
                deployment_scheduled_count,
                deployment_completed_flag,
                deployment_completed_oldest,
                deployment_completed_oldest_sys_id,
                deployment_completed_count,
                deployment_active_flag,
                deployment_active_oldest,
                deployment_active_oldest_sys_id,
                deployment_active_count,
                usage_status,
                license_status,
                u_ps_implementation_status,
                u_ua_adoption_status,
                metric,
                metric_2,
                usage_date,
                legacy_usage_indicator,
                dv_legacy_usage_indicator,
                status_summary,
                u_ps_services_vendor_type,
                u_ps_services_vendor,
                u_ps_services_first_sold_date,
                u_ps_deployment_start_date,
                u_ps_go_live_date,
                u_bu_deal_size_band,
                u_bu_license_size_band,
                u_renewal_risk_score,
                u_renewal_risk_reason_code,
                u_renewal_risk_band,
                date_generated,
                checksum
FROM EDW_LS."PRODUCT_EM"."U_CUSTOMER_PRODUCT_PROFILE_STAGE_IN"
WHERE CUSTOMER_PRODUCT_PROFILE_SYS_ID || CUSTOMER_PROFILE_SYS_ID || APPLICATION_SYS_ID NOT IN
    (SELECT CUSTOMER_PRODUCT_PROFILE_SYS_ID || CUSTOMER_PROFILE_SYS_ID || APPLICATION_SYS_ID
     FROM EDW_LS."PRODUCT_EM"."U_CUSTOMER_PRODUCT_PROFILE_STAGE_MASTER");"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # SqlFluff: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"edw_ls.product_em.u_customer_product_profile_stage_in"},  # source_tables
        {"edw_ls.product_em.u_customer_product_profile_stage_master"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        test_sqlfluff=False,
        skip_graph_check=True,
    )


def test_create_table_rds_powerbi__q4736():
    """create table - Query 4736"""
    sql = """ insert into RDS.POWERBI.STG_FABRIC_CAPACITY_METRICS
(select 'placeholder_1','placeholder_2',"Data Value",'placeholder_3'
from RDS.POWERBI."TEMP_FABRIC_CAPACITY_METRICS_7B4ECCAF-EF86-475A-B8AB-EA595D5066E3")"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.powerbi.temp_fabric_capacity_metrics_7b4eccaf-ef86-475a-b8ab-ea595d5066e3"
        },  # source_tables
        {"rds.powerbi.stg_fabric_capacity_metrics"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_create_table_rds_dynamics365_equipments_q4909():
    """create table - Query 4909"""
    sql = """ insert into RDS.DYNAMICS365.TABLES_DELETED_RECORDS_ID ( SCHEMA ,  STORED_PROCEDURE ,  SOURCE_TABLE_NAME ,  OBJECT_ID ,  TIME_STAMP )
    select 'placeholder_1' , 'placeholder_2' , 'placeholder_3' , "EQUIPMENTID" ,  CURRENT_TIMESTAMP
    FROM RDS.DYNAMICS365.EQUIPMENTS
    where "EQUIPMENTID" IN (select distinct OBJECTID FROM "RDS"."DYNAMICS365"."AUDITS" WHERE "ACTION"='placeholder_4' and "OPERATION" = 'placeholder_5' AND LOWER( "OBJECTTYPECODE" ) = 'placeholder_6' AND CAST( "CREATEDON" AS DATE ) >=DATEADD(DAY, 'placeholder_7', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.dynamics365.audits", "rds.dynamics365.equipments"},  # source_tables
        {"rds.dynamics365.tables_deleted_records_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_rds_dynamics365_sn_opportunitysummaries_q5027():
    """create table - Query 5027"""
    sql = """ insert into RDS.DYNAMICS365.TABLES_DELETED_RECORDS_ID ( SCHEMA ,  STORED_PROCEDURE ,  SOURCE_TABLE_NAME ,  OBJECT_ID ,  TIME_STAMP )
    select 'placeholder_1' , 'placeholder_2' , 'placeholder_3' , "SN_OPPORTUNITYSUMMARYID" ,  CURRENT_TIMESTAMP
    FROM RDS.DYNAMICS365.SN_OPPORTUNITYSUMMARIES
    where "SN_OPPORTUNITYSUMMARYID" IN (select distinct OBJECTID FROM "RDS"."DYNAMICS365"."AUDITS" WHERE "ACTION"='placeholder_4' and "OPERATION" = 'placeholder_5' AND LOWER( "OBJECTTYPECODE" ) = 'placeholder_6' AND CAST( "CREATEDON" AS DATE ) >=DATEADD(DAY, 'placeholder_7', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.dynamics365.audits",
            "rds.dynamics365.sn_opportunitysummaries",
        },  # source_tables
        {"rds.dynamics365.tables_deleted_records_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_rds__q5103():
    """create table - Query 5103"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."X_SNC_PO_ACCR_AUTO_OPEN_PO_LINES" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.surf.sys_audit_delete",
            "rds.surf.x_snc_po_accr_auto_open_po_lines",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_rds__q5254():
    """create table - Query 5254"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."X_SNC_GTM_SALES_ACCOUNT" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.surf.sys_audit_delete",
            "rds.surf.x_snc_gtm_sales_account",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_rds__q5508():
    """create table - Query 5508"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."X_SNC_GTM_SALES_SALES_ALERT" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.surf.sys_audit_delete",
            "rds.surf.x_snc_gtm_sales_sales_alert",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_edw_sales_src_v_fact_pipeline_conversion_q5512():
    """create table - Query 5512"""
    sql = """ INSERT INTO EDW.SALES.STG_FACT_PIPELINE_CONVERSION (BU_GROUP_ID, GEO_ID, NNACV_PREDICTED_USD_CY_FX, NNACV_PREDICTED_USD_CY_FX_BOW, NNACV_PREDICTED_USD_CY_FX_STLW, NNACV_PREDICTED_USD_CY_FX_STLY, QUARTER_ID, QUARTER_YYQQ, TERRITORY_ID, TERRITORY_SYSID, ETL_CREATED_TS, ETL_UPDATED_TS)
(SELECT BU_GROUP_ID, GEO_ID, NNACV_PREDICTED_USD_CY_FX, NNACV_PREDICTED_USD_CY_FX_BOW, NNACV_PREDICTED_USD_CY_FX_STLW, NNACV_PREDICTED_USD_CY_FX_STLY, QUARTER_ID, QUARTER_YYQQ, TERRITORY_ID, TERRITORY_SYSID, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()
FROM EDW.SALES.SRC_V_FACT_PIPELINE_CONVERSION
)"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"edw.sales.src_v_fact_pipeline_conversion"},  # source_tables
        {"edw.sales.stg_fact_pipeline_conversion"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_create_table_rule_engine_table_q5542():
    """create table - Query 5542"""
    sql = """ MERGE  INTO RULE_ENGINE_TABLE USING ( SELECT "OpportunityParentNumber" AS "r_pygc_OpportunityParentNumber", "LineItemNumber_CRM" AS "r_pygc_LineItemNumber_CRM", "ALLOCATION_SEQ_NUM" AS "r_pygc_ALLOCATION_SEQ_NUM", "PROTECTION_LINE_AMT" AS "r_pygc_PROTECTION_LINE_AMT", "TOTAL_GO_FWD_AMT" AS "r_pygc_TOTAL_GO_FWD_AMT", "TOTAL_BU_RR_AMT" AS "r_pygc_TOTAL_BU_RR_AMT" FROM (SELECT RULE_ENGINE_TABLE."OpportunityParentNumber", RULE_ENGINE_TABLE."LineItemNumber_CRM", RULE_ENGINE_TABLE."ALLOCATION_SEQ_NUM", RULE_ENGINE_TABLE."PROTECTION_LINE_AMT", RULE_ENGINE_TABLE."TOTAL_GO_FWD_AMT", RULE_ENGINE_TABLE."TOTAL_BU_RR_AMT" FROM RULE_ENGINE_TABLE WHERE  "PRODUCT_CODE_RR_FLAG" = 'placeholder_1' AND  "LINE_PROTECTION_PCT" <> 'placeholder_2' AND  "LINE_PROTECTION_PCT" IS NOT TRUE AND  "LINE_ALLOCATION_TYPE" = 'placeholder_4' AND  "TOTAL_BU_RR_AMT" > 'placeholder_5')) ON ((("OpportunityParentNumber" = "r_pygc_OpportunityParentNumber") AND ("LineItemNumber_CRM" = "r_pygc_LineItemNumber_CRM")) AND ("ALLOCATION_SEQ_NUM" = "r_pygc_ALLOCATION_SEQ_NUM")) WHEN  MATCHED  THEN  UPDATE  SET "ORIG_TOTAL_BU_RR_AMT" = "r_pygc_TOTAL_BU_RR_AMT" """
    # SqlParse: Cannot extract source tables from subqueries/complex queries
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"<default>.rule_engine_table"},  # source_tables
        {"<default>.rule_engine_table"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_create_table_rule_engine_table_q5556():
    """create table - Query 5556"""
    sql = """ MERGE  INTO RULE_ENGINE_TABLE USING ( SELECT "OpportunityParentNumber" AS "r_a9z4_OpportunityParentNumber", "LineItemNumber_CRM" AS "r_a9z4_LineItemNumber_CRM", "ALLOCATION_SEQ_NUM" AS "r_a9z4_ALLOCATION_SEQ_NUM", "PROTECTION_LINE_AMT" AS "r_a9z4_PROTECTION_LINE_AMT", "LINE_PROTECTION_PCT" AS "r_a9z4_LINE_PROTECTION_PCT", "TOTAL_GO_FWD_AMT" AS "r_a9z4_TOTAL_GO_FWD_AMT", "TOTAL_BU_RR_AMT" AS "r_a9z4_TOTAL_BU_RR_AMT" FROM ( SELECT "OpportunityParentNumber", "LineItemNumber_CRM", "ALLOCATION_SEQ_NUM", "PROTECTION_LINE_AMT", "LINE_PROTECTION_PCT", "TOTAL_GO_FWD_AMT", (iff( CAST ("TOTAL_BU_RR_AMT" AS FLOAT) IS TRUE, 'placeholder_2',  CAST ("TOTAL_BU_RR_AMT" AS FLOAT)) * iff( CAST ("LINE_PROTECTION_PCT" AS FLOAT) IS TRUE, 'placeholder_4',  CAST ("LINE_PROTECTION_PCT" AS FLOAT))) AS "TOTAL_BU_RR_AMT" FROM (SELECT RULE_ENGINE_TABLE."OpportunityParentNumber", RULE_ENGINE_TABLE."LineItemNumber_CRM", RULE_ENGINE_TABLE."ALLOCATION_SEQ_NUM", RULE_ENGINE_TABLE."PROTECTION_LINE_AMT", RULE_ENGINE_TABLE."LINE_PROTECTION_PCT", RULE_ENGINE_TABLE."TOTAL_GO_FWD_AMT", RULE_ENGINE_TABLE."TOTAL_BU_RR_AMT" FROM RULE_ENGINE_TABLE WHERE  "PRODUCT_CODE_RR_FLAG" = 'placeholder_5' AND  "LINE_PROTECTION_PCT" <> 'placeholder_6' AND  "LINE_PROTECTION_PCT" IS NOT TRUE AND  "LINE_ALLOCATION_TYPE" = 'placeholder_8' AND  "TOTAL_BU_RR_AMT" > 'placeholder_9'))) ON ((("OpportunityParentNumber" = "r_a9z4_OpportunityParentNumber") AND ("LineItemNumber_CRM" = "r_a9z4_LineItemNumber_CRM")) AND ("ALLOCATION_SEQ_NUM" = "r_a9z4_ALLOCATION_SEQ_NUM")) WHEN  MATCHED  THEN  UPDATE  SET "TOTAL_BU_RR_AMT" = "r_a9z4_TOTAL_BU_RR_AMT" """
    # SqlParse: Cannot extract source tables from subqueries/complex queries
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"<default>.rule_engine_table"},  # source_tables
        {"<default>.rule_engine_table"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_create_table_rds__q5584():
    """create table - Query 5584"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."X_SNC_TREASURY_FOR_TREASURY_INPUT" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.surf.sys_audit_delete",
            "rds.surf.x_snc_treasury_for_treasury_input",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )
