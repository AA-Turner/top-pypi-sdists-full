"""Tests for insert."""

from tests.helpers import assert_table_lineage_equal


def test_insert_rds_staging_perspectium_instance_log_errors_q8():
    """insert - Query 8"""
    sql = """ merge into RDS.STAGING.PERSPECTIUM_INSTANCE_LOG_ERRORS as target
                            using (select column1 INSTANCE_NAME,column2 NAME, column3 VALUE,column4 TYPE,column5 SYS_CREATED_ON, column6 ETL_EXTRACT_DATE
                            from (values ('placeholder_1', 'placeholder_2', 'placeholder_3', 'placeholder_4', 'placeholder_5', 'placeholder_6')))
                            as src
                            on target.INSTANCE_NAME = src.INSTANCE_NAME and target.NAME = src.NAME and target.TYPE = src.TYPE and target.SYS_CREATED_ON = src.SYS_CREATED_ON
                            when matched then update set target.VALUE = src.VALUE,target.ETL_EXTRACT_DATE = src.ETL_EXTRACT_DATE
                            when not matched then insert (INSTANCE_NAME,NAME,VALUE,TYPE,SYS_CREATED_ON, ETL_EXTRACT_DATE) values (src.INSTANCE_NAME, src.NAME, src.VALUE,src.TYPE, src.SYS_CREATED_ON, src.ETL_EXTRACT_DATE);"""
    # SqlParse: IndexError - list index out of range (analyzer.py:200)
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"rds.staging.perspectium_instance_log_errors"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
    )


def test_insert_query_q12():
    """insert - Query 12"""
    sql = """ update "NOC"."LOGGING"."ETL_RDS_JOB_RUN_AUDIT"
set
job_status='2025-01-01 00:00:00',
JOB_END_TS=current_timestamp(),
-- job_run_duration='',
SOURCE_RECORD_COUNT=2,
PROCESSED_RECORD_COUNT=3,
ERROR_RECORD_COUNT = 4-'placeholder_5',
ETL_UPDATE_DATE= current_timestamp()
-- LAST_RUN_TIMESTAMP= current_timestamp()
where RDS_CONFIG_ID='2025-01-01 00:00:00'
and INTEG_JOB_ID = 7
and INTEG_TOOL_JOB_RUN_ID = 8 ;"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.logging.etl_rds_job_run_audit"},  # target_tables
        dialect="snowflake",
    )


def test_insert_query_q16():
    """insert - Query 16"""
    sql = """ """
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        set(),  # target_tables
        dialect="snowflake",
    )


def test_insert_rds__q24():
    """insert - Query 24"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."VALUESCAN"."SP_LOG" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."VALUESCAN"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.valuescan.sp_log", "rds.valuescan.sys_audit_delete"},  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_insert_u_pu_instance_application_module_q25():
    """insert - Query 25"""
    sql = """ Merge into u_pu_instance_application_module using u_pu_instance_application_module_1686951 on u_pu_instance_application_module."SYS_ID" = u_pu_instance_application_module_1686951."SYS_ID"  when matched then update set  u_pu_instance_application_module."U_INSTANCE_NAME" =  u_pu_instance_application_module_1686951."U_INSTANCE_NAME", u_pu_instance_application_module."PSP_PER_UPDATE_DT" =  '2025-01-01 00:00:00', u_pu_instance_application_module."SYS_TAGS" =  u_pu_instance_application_module_1686951."SYS_TAGS", u_pu_instance_application_module."SYS_ID" =  u_pu_instance_application_module_1686951."SYS_ID", u_pu_instance_application_module."U_APPLICATION" =  u_pu_instance_application_module_1686951."U_APPLICATION", u_pu_instance_application_module."PSP_PER_INSERT_DT" =  u_pu_instance_application_module."PSP_PER_INSERT_DT", u_pu_instance_application_module."SYS_CREATED_BY" =  u_pu_instance_application_module_1686951."SYS_CREATED_BY", u_pu_instance_application_module."SYS_UPDATED_ON" =  u_pu_instance_application_module_1686951."SYS_UPDATED_ON", u_pu_instance_application_module."U_REPORT_ID" =  u_pu_instance_application_module_1686951."U_REPORT_ID", u_pu_instance_application_module."U_TITLE" =  u_pu_instance_application_module_1686951."U_TITLE", u_pu_instance_application_module."SYS_MOD_COUNT" =  u_pu_instance_application_module_1686951."SYS_MOD_COUNT", u_pu_instance_application_module."U_TABLE" =  u_pu_instance_application_module_1686951."U_TABLE", u_pu_instance_application_module."PSP_PER_DELETE_DT" =  u_pu_instance_application_module_1686951."PSP_PER_DELETE_DT", u_pu_instance_application_module."U_ACTIVE" =  u_pu_instance_application_module_1686951."U_ACTIVE", u_pu_instance_application_module."SYS_UPDATED_BY" =  u_pu_instance_application_module_1686951."SYS_UPDATED_BY", u_pu_instance_application_module."U_UPDATED_ON" =  u_pu_instance_application_module_1686951."U_UPDATED_ON", u_pu_instance_application_module."SYS_CREATED_ON" =  u_pu_instance_application_module_1686951."SYS_CREATED_ON", u_pu_instance_application_module."U_SYS_ID" =  u_pu_instance_application_module_1686951."U_SYS_ID", u_pu_instance_application_module."U_APPLICATION_MENU_CREATED_BY" =  u_pu_instance_application_module_1686951."U_APPLICATION_MENU_CREATED_BY", u_pu_instance_application_module."U_APPLICATION_MODULE_CREATED_BY" =  u_pu_instance_application_module_1686951."U_APPLICATION_MODULE_CREATED_BY", u_pu_instance_application_module."U_APP_CREATED_ON" =  u_pu_instance_application_module_1686951."U_APP_CREATED_ON" when not matched then insert ( u_pu_instance_application_module."U_INSTANCE_NAME", u_pu_instance_application_module."PSP_PER_UPDATE_DT", u_pu_instance_application_module."SYS_TAGS", u_pu_instance_application_module."SYS_ID", u_pu_instance_application_module."U_APPLICATION", u_pu_instance_application_module."PSP_PER_INSERT_DT", u_pu_instance_application_module."SYS_CREATED_BY", u_pu_instance_application_module."SYS_UPDATED_ON", u_pu_instance_application_module."U_REPORT_ID", u_pu_instance_application_module."U_TITLE", u_pu_instance_application_module."SYS_MOD_COUNT", u_pu_instance_application_module."U_TABLE", u_pu_instance_application_module."PSP_PER_DELETE_DT", u_pu_instance_application_module."U_ACTIVE", u_pu_instance_application_module."SYS_UPDATED_BY", u_pu_instance_application_module."U_UPDATED_ON", u_pu_instance_application_module."SYS_CREATED_ON", u_pu_instance_application_module."U_SYS_ID", u_pu_instance_application_module."U_APPLICATION_MENU_CREATED_BY", u_pu_instance_application_module."U_APPLICATION_MODULE_CREATED_BY", u_pu_instance_application_module."U_APP_CREATED_ON") values ( u_pu_instance_application_module_1686951."U_INSTANCE_NAME", 'placeholder_2', u_pu_instance_application_module_1686951."SYS_TAGS", u_pu_instance_application_module_1686951."SYS_ID", u_pu_instance_application_module_1686951."U_APPLICATION", 'placeholder_3', u_pu_instance_application_module_1686951."SYS_CREATED_BY", u_pu_instance_application_module_1686951."SYS_UPDATED_ON", u_pu_instance_application_module_1686951."U_REPORT_ID", u_pu_instance_application_module_1686951."U_TITLE", u_pu_instance_application_module_1686951."SYS_MOD_COUNT", u_pu_instance_application_module_1686951."U_TABLE", u_pu_instance_application_module_1686951."PSP_PER_DELETE_DT", u_pu_instance_application_module_1686951."U_ACTIVE", u_pu_instance_application_module_1686951."SYS_UPDATED_BY", u_pu_instance_application_module_1686951."U_UPDATED_ON", u_pu_instance_application_module_1686951."SYS_CREATED_ON", u_pu_instance_application_module_1686951."U_SYS_ID", u_pu_instance_application_module_1686951."U_APPLICATION_MENU_CREATED_BY", u_pu_instance_application_module_1686951."U_APPLICATION_MODULE_CREATED_BY", u_pu_instance_application_module_1686951."U_APP_CREATED_ON")"""
    assert_table_lineage_equal(
        sql,
        {"<default>.u_pu_instance_application_module_1686951"},  # source_tables
        {"<default>.u_pu_instance_application_module"},  # target_tables
        dialect="snowflake",
    )


def test_insert_query_q31():
    """insert - Query 31"""
    sql = """ update "NOC"."LOGGING"."ETL_RDS_JOB_RUN_AUDIT"
set
job_status='2025-01-01 00:00:00',
JOB_END_TS=current_timestamp(),
-- job_run_duration='41320',
SOURCE_RECORD_COUNT=2,
PROCESSED_RECORD_COUNT=3,
ERROR_RECORD_COUNT = 4-'placeholder_5',
ETL_UPDATE_DATE= current_timestamp()
-- LAST_RUN_TIMESTAMP= current_timestamp()
where RDS_CONFIG_ID='2025-01-01 00:00:00'
and INTEG_JOB_ID = 7
and INTEG_TOOL_JOB_RUN_ID = 8 ;"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.logging.etl_rds_job_run_audit"},  # target_tables
        dialect="snowflake",
    )


def test_insert_rds__q35():
    """insert - Query 35"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."APPSTORE"."SN_APPSTOREAUDIT_INSTANCE_APP_INSTALL" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."APPSTORE"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.appstore.sn_appstoreaudit_instance_app_install",
            "rds.appstore.sys_audit_delete",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_insert_query_q36():
    """insert - Query 36"""
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


def test_insert_outreach_public_meetings_q38():
    """insert - Query 38"""
    sql = """ INSERT INTO RDS.OUTREACH.STG_MEETINGS
("SURROGATE_ID","CALENDAR_IDS","TITLE","RECURRING_EXTERNAL_EVENT_ID","USER_ID","IS_DELETED_IN_APP","CREATOR_TYPE","SYNC_ATTEMPTS","HAS_PROSPECTS","LOCATION","CREATOR_ID","ICAL_SEQUENCE","SYNC_STARTED_AT","EXTERNAL_UPDATED_AT","EXTERNAL_EVENT_ID","END_TIME","UPDATED_AT","SYNCED_AT","BOOKER_ID","ONLINE_MEETING_LINK","ICAL_ID","SOURCE","CANCELED","ID","ALL_DAY","CREATED_AT","DML_TYPE","START_TIME","BENTO","ORGANIZER","OPPORTUNITY_IDS","EVENT_LINK","RECURRING","NO_SHOW_AT","O_ID","SENSITIVE","DESCRIPTION","DML_AT","EXTERNAL_CREATED_AT")
select "SURROGATE_ID","CALENDAR_IDS","TITLE","RECURRING_EXTERNAL_EVENT_ID","USER_ID","IS_DELETED_IN_APP","CREATOR_TYPE","SYNC_ATTEMPTS","HAS_PROSPECTS","LOCATION","CREATOR_ID","ICAL_SEQUENCE","SYNC_STARTED_AT","EXTERNAL_UPDATED_AT","EXTERNAL_EVENT_ID","END_TIME","UPDATED_AT","SYNCED_AT","BOOKER_ID","ONLINE_MEETING_LINK","ICAL_ID","SOURCE","CANCELED","ID","ALL_DAY","CREATED_AT","DML_TYPE","START_TIME","BENTO","ORGANIZER","OPPORTUNITY_IDS","EVENT_LINK","RECURRING","NO_SHOW_AT","O_ID","SENSITIVE","DESCRIPTION","DML_AT","EXTERNAL_CREATED_AT" from OUTREACH.PUBLIC.MEETINGS"""
    assert_table_lineage_equal(
        sql,
        {"outreach.public.meetings"},  # source_tables
        {"rds.outreach.stg_meetings"},  # target_tables
        dialect="snowflake",
    )


def test_insert_rds__q41():
    """insert - Query 41"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."ASMT_METRIC_RESULT" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.surf.asmt_metric_result", "rds.surf.sys_audit_delete"},  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_insert_rds__q42():
    """insert - Query 42"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SUPPORTTOOLS"."CMN_LOCATION" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SUPPORTTOOLS"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.supporttools.cmn_location",
            "rds.supporttools.sys_audit_delete",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_insert_edw_ls__q43():
    """insert - Query 43"""
    sql = """ CREATE OR REPLACE TEMPORARY TABLE EDW_LS.MARKETING_EM.TEMP_deletedrecords   AS
SELECT "LineItemNumber"
FROM EDW_LS."MARKETING"."TBL_OPTYLINE_MOVEMENT" M
LEFT OUTER JOIN ODS_LS."SURF"."SALES_OPPORTUNITY_ITEM" OI ON OI."OptyItemLineItemNumber" = M."LineItemNumber"
WHERE OI."OptyItemLineItemNumber" IS TRUE
  AND M."Deleted"='placeholder_2';"""
    assert_table_lineage_equal(
        sql,
        {
            "edw_ls.marketing.tbl_optyline_movement",
            "ods_ls.surf.sales_opportunity_item",
        },  # source_tables
        {"edw_ls.marketing_em.temp_deletedrecords"},  # target_tables
        dialect="snowflake",
    )


def test_insert_query_q45():
    """insert - Query 45"""
    sql = """ update "NOC"."LOGGING"."ETL_RDS_JOB_RUN_AUDIT"
set
job_status='2025-01-01 00:00:00',
JOB_END_TS=current_timestamp(),
-- job_run_duration='6242',
SOURCE_RECORD_COUNT=2,
PROCESSED_RECORD_COUNT=3,
ERROR_RECORD_COUNT = 4-'placeholder_5',
ETL_UPDATE_DATE= current_timestamp()
-- LAST_RUN_TIMESTAMP= current_timestamp()
where RDS_CONFIG_ID='2025-01-01 00:00:00'
and INTEG_JOB_ID = 7
and INTEG_TOOL_JOB_RUN_ID = 8 ;"""
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.logging.etl_rds_job_run_audit"},  # target_tables
        dialect="snowflake",
    )


def test_insert_rds__q47():
    """insert - Query 47"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."PARTNER_PORTAL"."U_4C_METRIC" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."PARTNER_PORTAL"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.partner_portal.sys_audit_delete",
            "rds.partner_portal.u_4c_metric",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_insert_query_q48():
    """insert - Query 48"""
    sql = """ """
    assert_table_lineage_equal(
        sql, set(), set(), dialect="snowflake"  # source_tables  # target_tables
    )


def test_insert_rds__q52():
    """insert - Query 52"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."IMPACT"."X_SNC_CUSP_ACTIVITY_BASE" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."IMPACT"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.impact.sys_audit_delete",
            "rds.impact.x_snc_cusp_activity_base",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        skip_graph_check=True,
    )


def test_insert_rds_hi_change_request_q53():
    """insert - Query 53"""
    sql = """ CREATE OR REPLACE TABLE SELFSERVE.SRE.SRE_ASSIGNED_TASKS_PROC AS
            WITH SYS_USER AS
            (SELECT
                DISTINCT
                SYS_ID,
                NAME,
                DV_DEPARTMENT,
                DV_LOCATION,
                U_COUNTRY,
                DV_MANAGER,
                EMAIL,
                DV_COMPANY
             FROM
                 "RDS"."HI"."SYS_USER"
            ),
            ALL_TASK AS
            (SELECT
                DISTINCT
                MAIN.SYS_ID,
                MAIN.NUMBER,
                MAIN.DV_SYS_CLASS_NAME AS TASK_TYPE,
                MAIN.DV_URGENCY AS PRIORITY,
                MAIN.DV_PRIORITY AS DV_PRIORITY,
                MAIN.SHORT_DESCRIPTION,
                MAIN.DV_ASSIGNMENT_GROUP,
                CONVERT_TIMEZONE('placeholder_1','placeholder_2',MAIN.SYS_CREATED_ON) AS CREATED_ON,
                TO_DATE(CONVERT_TIMEZONE('placeholder_3','placeholder_4',MAIN.SYS_CREATED_ON)) AS CREATED,
                CONVERT_TIMEZONE('placeholder_5','placeholder_6',MAIN.OPENED_AT) AS OPENED_AT,
                CONVERT_TIMEZONE('placeholder_7','placeholder_8',MAIN.CLOSED_AT) AS CLOSED_AT,
                CONVERT_TIMEZONE('placeholder_9','placeholder_10',MAIN.SYS_UPDATED_ON) AS SYS_UPDATED_ON,
                MAIN.SYS_CREATED_BY,
                MAIN.DV_OPENED_BY AS OPENED_BY,
                OPENED_BY.DV_DEPARTMENT AS OPENED_BY_DEPARTMENT,
                OPENED_BY.DV_LOCATION AS OPENED_BY_LOCATION,
                OPENED_BY.U_COUNTRY AS OPENED_BY_COUNTRY,
                OPENED_BY.DV_MANAGER AS OPENED_BY_MANAGER,
                OPENED_BY.EMAIL AS OPENED_BY_EMAIL,
                OPENED_BY.DV_COMPANY AS OPENED_BY_COMPANY,
                MAIN.DV_CLOSED_BY AS CLOSED_BY,
                CLOSED_BY.DV_DEPARTMENT AS CLOSED_BY_DEPARTMENT,
                CLOSED_BY.DV_LOCATION AS CLOSED_BY_LOCATION,
                CLOSED_BY.U_COUNTRY AS CLOSED_BY_COUNTRY,
                CLOSED_BY.DV_MANAGER AS CLOSED_BY_MANAGER,
                CLOSED_BY.EMAIL AS CLOSED_BY_EMAIL,
                CLOSED_BY.DV_COMPANY AS CLOSED_BY_COMPANY,
                MAIN.ACTIVE,
                MAIN.DV_STATE AS STATE,
                MAIN.U_TAGS,
                MAIN.DV_PARENT,
                MAIN.SYS_TAGS,
                MAIN.DV_COMPANY,
                MAIN.DV_ASSIGNED_TO,
                MAIN.SYS_UPDATED_BY,
                ASSIGNED_TO,
                ASSIGNED_TO.DV_DEPARTMENT AS ASSIGNED_TO_DEPARTMENT,
                ASSIGNED_TO.DV_LOCATION AS ASSIGNED_TO_LOCATION,
                ASSIGNED_TO.U_COUNTRY AS ASSIGNED_TO_COUNTRY,
                ASSIGNED_TO.DV_MANAGER AS ASSIGNED_TO_MANAGER,
                ASSIGNED_TO.EMAIL AS ASSIGNED_TO_EMAIL,
                CUST.DV_U_EU_DATA_CONSENT,
                CONCAT('placeholder_11',MAIN.NUMBER) AS WORK_RECORD_URL
             FROM
                "RDS"."HI"."TASK" MAIN
             LEFT JOIN
                 SYS_USER OPENED_BY
             ON
                 MAIN.OPENED_BY = OPENED_BY.SYS_ID
             LEFT JOIN
                 SYS_USER CLOSED_BY
             ON
                 MAIN.CLOSED_BY = CLOSED_BY.SYS_ID
             LEFT JOIN
                 SYS_USER ASSIGNED_TO
             ON
                 MAIN.ASSIGNED_TO = ASSIGNED_TO.SYS_ID
             LEFT JOIN
                 "RDS"."HI"."CUSTOMER_ACCOUNT" CUST
             ON
                 MAIN.COMPANY = CUST.SYS_ID
            ),
            CHANGE_REQUEST AS
            (SELECT
                 DISTINCT
                 SYS_ID,
                 NUMBER,
                 DV_TYPE AS CHANGE_REQUEST_TYPE,
                 DV_CATEGORY AS CHANGE_REQUEST_CATEGORY,
                 DV_U_SUB_CATEGORY AS CHANGE_SUB_CATEGORY,
                 DV_IMPACT AS CHANGE_DV_IMPACT,
                 DV_RISK AS CHANGE_DV_RISK
             FROM
                 RDS.HI.CHANGE_REQUEST
            ),
            INCIDENT_CATEGORY AS
            (SELECT
                DISTINCT
                A.U_NAME AS INCIDENT_CATEGORY,
                REPLACE(A.DV_U_PARENT,'placeholder_12','placeholder_13') AS INCIDENT_CATEGORY_PARENT,
                REPLACE(B.DV_U_PARENT,'placeholder_14','placeholder_15') AS INCIDENT_CATEGORY_PARENT_PARENT,
                REPLACE(C.DV_U_PARENT,'placeholder_16','placeholder_17') AS INCIDENT_CATEGORY_PARENT_PARENT_PARENT,
                REPLACE(D.DV_U_PARENT,'placeholder_18','placeholder_19') AS INCIDENT_CATEGORY_PARENT_PARENT_PARENT_PARENT
             FROM
                 "RDS"."HI"."U_PRODUCT_CATEGORY" A
             LEFT JOIN
                 "RDS"."HI"."U_PRODUCT_CATEGORY" B
             ON
                 A.DV_U_PARENT = B.U_NAME
             LEFT JOIN
                 "RDS"."HI"."U_PRODUCT_CATEGORY" C
             ON
                 B.DV_U_PARENT = C.U_NAME
             LEFT JOIN
                 "RDS"."HI"."U_PRODUCT_CATEGORY" D
             ON
                 C.DV_U_PARENT = D.U_NAME
            ),
            CASES AS
            (SELECT
                DISTINCT
                SYS_ID,
                NUMBER,
                DV_U_CASE_CATEGORY AS CASE_CATEGORY,
                DV_U_CASE_TYPE AS CASE_TYPE
             FROM
                 RDS.HI.SN_CUSTOMERSERVICE_CASE
            ),
            PROBLEMS AS
            (SELECT
                DISTINCT
                SYS_ID,
                NUMBER,
                DV_U_PROBLEM_CATEGORY AS PROBLEM_CATEGORY,
                DV_U_PRODUCT_SERVICE_AFFECTED AS PROBLEM_PRODUCT_SERVICE_AFFECTED,
                DV_U_PROBLEM_TYPE AS PROBLEM_TYPE,
                DV_U_SEVERITY AS PROBLEM_SEVERITY,
                DV_U_PRODUCT_INITIAL_TAXONOMY AS PROBLEM_PRODUCT_INITIAL_TAXONOMY,
                DV_U_SUBCATEGORY,
                DV_U_SOURCE AS PROBLEM_SOURCE,
                SHORT_DESCRIPTION
             FROM
                 RDS.HI.PROBLEM
            ),
            INCIDENT AS
            (SELECT
                DISTINCT
                MAIN.SYS_ID,
                MAIN.NUMBER,
                MAIN.DV_CAUSED_BY AS INC_DV_CAUSED_BY,
                MAIN.DV_U_INCIDENT_CATEGORY AS INCIDENT_CATEGORY,
                MAIN.DV_U_INCIDENT_TYPE AS U_INCIDENT_TYPE,
                MAIN.DV_PROBLEM_ID,
                PRB.SHORT_DESCRIPTION AS PROBLEM_SHORT_DESCRIPTION,
                PRB.PROBLEM_CATEGORY AS DV_U_PROBLEM_CATEGORY,
                PRB.DV_U_SUBCATEGORY,
                IC.INCIDENT_CATEGORY_PARENT,
                IC.INCIDENT_CATEGORY_PARENT_PARENT,
                IC.INCIDENT_CATEGORY_PARENT_PARENT_PARENT,
                IC.INCIDENT_CATEGORY_PARENT_PARENT_PARENT_PARENT
             FROM
                 RDS.HI.INCIDENT MAIN
             LEFT JOIN
                PROBLEMS PRB
            ON
                MAIN.DV_PROBLEM_ID = PRB.NUMBER
             LEFT JOIN
                INCIDENT_CATEGORY IC
            ON
                MAIN.DV_U_INCIDENT_CATEGORY = IC.INCIDENT_CATEGORY
            )
            SELECT
                MAIN.SYS_ID,
                MAIN.NUMBER,
                MAIN.TASK_TYPE,
                MAIN.DV_PRIORITY,
                MAIN.SHORT_DESCRIPTION,
                MAIN.DV_ASSIGNMENT_GROUP,
                MAIN.CREATED_ON,
                MAIN.CREATED,
                MAIN.OPENED_AT,
                MAIN.CLOSED_AT,
                MAIN.SYS_UPDATED_ON,
                MAIN.SYS_CREATED_BY,
                MAIN.OPENED_BY,
                MAIN.OPENED_BY_DEPARTMENT,
                MAIN.OPENED_BY_LOCATION,
                MAIN.OPENED_BY_COUNTRY,
                MAIN.OPENED_BY_MANAGER,
                MAIN.OPENED_BY_EMAIL,
                MAIN.OPENED_BY_COMPANY,
                MAIN.CLOSED_BY,
                MAIN.CLOSED_BY_DEPARTMENT,
                MAIN.CLOSED_BY_LOCATION,
                MAIN.CLOSED_BY_COUNTRY,
                MAIN.CLOSED_BY_MANAGER,
                MAIN.CLOSED_BY_EMAIL,
                MAIN.CLOSED_BY_COMPANY,
                MAIN.ACTIVE,
                MAIN.STATE,
                MAIN.U_TAGS,
                MAIN.DV_PARENT,
                MAIN.SYS_TAGS,
                MAIN.DV_COMPANY,
                MAIN.DV_ASSIGNED_TO,
                MAIN.ASSIGNED_TO_DEPARTMENT,
                MAIN.ASSIGNED_TO_LOCATION,
                MAIN.ASSIGNED_TO_COUNTRY,
                MAIN.ASSIGNED_TO_MANAGER,
                MAIN.ASSIGNED_TO_EMAIL,
                MAIN.DV_U_EU_DATA_CONSENT,
                MAIN.WORK_RECORD_URL,
                MAIN.SYS_UPDATED_BY,
                PARENT.SYS_ID AS PARENT_SYS_ID,
                PARENT.NUMBER AS PARENT_NUMBER,
                PARENT.TASK_TYPE AS PARENT_TASK_TYPE,
                PARENT.DV_PRIORITY AS PARENT_DV_PRIORITY,
                PARENT.SHORT_DESCRIPTION AS PARENT_SHORT_DESCRIPTION,
                PARENT.DV_ASSIGNMENT_GROUP AS PARENT_DV_ASSIGNMENT_GROUP,
                PARENT.CREATED_ON AS PARENT_CREATED_ON,
                PARENT.CREATED AS PARENT_CREATED,
                PARENT.OPENED_AT AS PARENT_OPENED_AT,
                PARENT.CLOSED_AT AS PARENT_CLOSED_AT,
                PARENT.SYS_UPDATED_ON AS PARENT_SYS_UPDATED_ON,
                PARENT.SYS_CREATED_BY AS PARENT_SYS_CREATED_BY,
                PARENT.OPENED_BY AS PARENT_OPENED_BY,
                PARENT.OPENED_BY_DEPARTMENT AS PARENT_OPENED_BY_DEPARTMENT,
                PARENT.OPENED_BY_LOCATION AS PARENT_OPENED_BY_LOCATION,
                PARENT.OPENED_BY_COUNTRY AS PARENT_OPENED_BY_COUNTRY,
                PARENT.OPENED_BY_MANAGER AS PARENT_OPENED_BY_MANAGER,
                PARENT.OPENED_BY_EMAIL AS PARENT_OPENED_BY_EMAIL,
                PARENT.OPENED_BY_COMPANY AS PARENT_OPENED_BY_COMPANY,
                PARENT.CLOSED_BY AS PARENT_CLOSED_BY,
                PARENT.CLOSED_BY_DEPARTMENT AS PARENT_CLOSED_BY_DEPARTMENT,
                PARENT.CLOSED_BY_LOCATION AS PARENT_CLOSED_BY_LOCATION,
                PARENT.CLOSED_BY_COUNTRY AS PARENT_CLOSED_BY_COUNTRY,
                PARENT.CLOSED_BY_MANAGER AS PARENT_CLOSED_BY_MANAGER,
                PARENT.CLOSED_BY_EMAIL AS PARENT_CLOSED_BY_EMAIL,
                PARENT.CLOSED_BY_COMPANY AS PARENT_CLOSED_BY_COMPANY,
                PARENT.ACTIVE AS PARENT_ACTIVE,
                PARENT.STATE AS PARENT_STATE,
                PARENT.U_TAGS AS PARENT_U_TAGS,
                PARENT.DV_PARENT AS PARENT_DV_PARENT,
                PARENT.SYS_TAGS AS PARENT_SYS_TAGS,
                PARENT.DV_COMPANY AS PARENT_DV_COMPANY,
                PARENT.DV_ASSIGNED_TO AS PARENT_DV_ASSIGNED_TO,
                PARENT.ASSIGNED_TO_DEPARTMENT AS PARENT_ASSIGNED_TO_DEPARTMENT,
                PARENT.ASSIGNED_TO_LOCATION AS PARENT_ASSIGNED_TO_LOCATION,
                PARENT.ASSIGNED_TO_COUNTRY AS PARENT_ASSIGNED_TO_COUNTRY,
                PARENT.ASSIGNED_TO_MANAGER AS PARENT_ASSIGNED_TO_MANAGER,
                PARENT.ASSIGNED_TO_EMAIL AS PARENT_ASSIGNED_TO_EMAIL,
                PARENT.DV_U_EU_DATA_CONSENT AS PARENT_DV_U_EU_DATA_CONSENT,
                PARENT.WORK_RECORD_URL AS PARENT_WORK_RECORD_URL,
                CR.CHANGE_REQUEST_TYPE,
                CR.CHANGE_REQUEST_CATEGORY,
                CR.CHANGE_SUB_CATEGORY,
                CR.CHANGE_DV_IMPACT,
                CR.CHANGE_DV_RISK,
                CR_PARENT.CHANGE_REQUEST_TYPE AS PARENT_CHANGE_REQUEST_TYPE,
                CR_PARENT.CHANGE_REQUEST_CATEGORY AS PARENT_CHANGE_REQUEST_CATEGORY,
                CR_PARENT.CHANGE_SUB_CATEGORY AS PARENT_CHANGE_SUB_CATEGORY,
                CR_PARENT.CHANGE_DV_IMPACT AS PARENT_CHANGE_DV_IMPACT,
                CR_PARENT.CHANGE_DV_RISK AS PARENT_CHANGE_DV_RISK,
                CS.CASE_CATEGORY,
                CS.CASE_TYPE,
                CS_PARENT.CASE_CATEGORY AS PARENT_CASE_CATEGORY,
                CS_PARENT.CASE_TYPE AS PARENT_CASE_TYPE,
                INC.INC_DV_CAUSED_BY,
                INC.INCIDENT_CATEGORY,
                INC.U_INCIDENT_TYPE,
                INC.DV_PROBLEM_ID AS INC_PROBLEM_ID,
                INC.PROBLEM_SHORT_DESCRIPTION,
                INC.DV_U_PROBLEM_CATEGORY,
                INC.DV_U_SUBCATEGORY,
                INC.INCIDENT_CATEGORY_PARENT,
                INC.INCIDENT_CATEGORY_PARENT_PARENT,
                INC.INCIDENT_CATEGORY_PARENT_PARENT_PARENT,
                INC.INCIDENT_CATEGORY_PARENT_PARENT_PARENT_PARENT,
                PARENT_INC.INC_DV_CAUSED_BY AS PARENT_INC_DV_CAUSED_BY,
                PARENT_INC.INCIDENT_CATEGORY AS PARENT_INCIDENT_CATEGORY,
                PARENT_INC.U_INCIDENT_TYPE AS PARENT_U_INCIDENT_TYPE,
                PRB.PROBLEM_CATEGORY,
                PRB.PROBLEM_PRODUCT_SERVICE_AFFECTED,
                PRB.PROBLEM_TYPE,
                PRB.PROBLEM_SOURCE,
                PRB.PROBLEM_SEVERITY,
                PRB.PROBLEM_PRODUCT_INITIAL_TAXONOMY
            FROM
                ALL_TASK MAIN
            LEFT JOIN
                ALL_TASK PARENT
            ON
                MAIN.DV_PARENT = PARENT.NUMBER
            LEFT JOIN
                CHANGE_REQUEST CR
            ON
                MAIN.NUMBER = CR.NUMBER
            LEFT JOIN
                CHANGE_REQUEST CR_PARENT
            ON
                MAIN.DV_PARENT = CR_PARENT.NUMBER
            LEFT JOIN
                CASES CS
            ON
                MAIN.NUMBER = CS.NUMBER
            LEFT JOIN
                CASES CS_PARENT
            ON
                MAIN.DV_PARENT = CS_PARENT.NUMBER
            LEFT JOIN
                INCIDENT INC
            ON
                MAIN.SYS_ID = INC.SYS_ID
            LEFT JOIN
                INCIDENT PARENT_INC
            ON
                MAIN.DV_PARENT = PARENT_INC.NUMBER
            LEFT JOIN
                PROBLEMS PRB
            ON
                MAIN.SYS_ID = PRB.SYS_ID
            WHERE
                MAIN.CREATED >=
                    DATE_TRUNC('placeholder_20',DATEADD(QUARTERS,'placeholder_21',CONVERT_TIMEZONE('placeholder_22','placeholder_23',CURRENT_DATE())))
                AND (MAIN.DV_ASSIGNMENT_GROUP IN ('placeholder_24','placeholder_25')
                             OR MAIN.ASSIGNED_TO IN (SELECT SYS_ID FROM SELFSERVE.SRE.SRE_ASSIGNEE_USER_LIST))
            ;"""
    # SqlParse: Cannot extract source tables from subqueries/complex queries
    # SqlFluff: Cannot extract correct source tables from complex queries
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.hi.change_request",
            "rds.hi.customer_account",
            "rds.hi.incident",
            "rds.hi.problem",
            "rds.hi.sn_customerservice_case",
            "rds.hi.sys_user",
            "rds.hi.task",
            "rds.hi.u_product_category",
            "selfserve.sre.sre_assignee_user_list",
        },  # source_tables
        {"selfserve.sre.sre_assigned_tasks_proc"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        test_sqlfluff=False,
        skip_graph_check=True,
    )


def test_insert_rds__q55():
    """insert - Query 55"""
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


def test_insert_rds_staging_perspectium_instance_log_errors_q56():
    """insert - Query 56"""
    sql = """ merge into RDS.STAGING.PERSPECTIUM_INSTANCE_LOG_ERRORS as target
                            using (select column1 INSTANCE_NAME,column2 NAME, column3 VALUE,column4 TYPE,column5 SYS_CREATED_ON, column6 ETL_EXTRACT_DATE
                            from (values ('placeholder_1', 'placeholder_2', 'placeholder_3', 'placeholder_4', 'placeholder_5', 'placeholder_6')))
                            as src
                            on target.INSTANCE_NAME = src.INSTANCE_NAME and target.NAME = src.NAME and target.TYPE = src.TYPE and target.SYS_CREATED_ON = src.SYS_CREATED_ON
                            when matched then update set target.VALUE = src.VALUE,target.ETL_EXTRACT_DATE = src.ETL_EXTRACT_DATE
                            when not matched then insert (INSTANCE_NAME,NAME,VALUE,TYPE,SYS_CREATED_ON, ETL_EXTRACT_DATE) values (src.INSTANCE_NAME, src.NAME, src.VALUE,src.TYPE, src.SYS_CREATED_ON, src.ETL_EXTRACT_DATE);"""
    # SqlParse: IndexError - list index out of range (analyzer.py:200)
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"rds.staging.perspectium_instance_log_errors"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
    )


def test_insert_rds_powerbi__q59():
    """insert - Query 59"""
    sql = """ insert into RDS.POWERBI.STG_FABRIC_CAPACITY_METRICS
(select 'placeholder_1','placeholder_2',"Data Value",'placeholder_3'
from RDS.POWERBI."TEMP_FABRIC_CAPACITY_METRICS_19E57AC7-D5ED-4C2D-A86F-39D130A439F8")"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.powerbi.temp_fabric_capacity_metrics_19e57ac7-d5ed-4c2d-a86f-39d130a439f8"
        },  # source_tables
        {"rds.powerbi.stg_fabric_capacity_metrics"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )
