"""Tests for swap remaining."""

from tests.helpers import assert_table_lineage_equal


def test_swap_remaining_rds_staging_perspectium_instance_log_errors_q540():
    """swap remaining - Query 540"""
    sql = """ merge into RDS.STAGING.PERSPECTIUM_INSTANCE_LOG_ERRORS as target
                            using (select column1 INSTANCE_NAME,column2 NAME, column3 VALUE,column4 TYPE,column5 SYS_CREATED_ON, column6 ETL_EXTRACT_DATE
                            from (values ('placeholder_1', 'placeholder_2', 'placeholder_3', 'placeholder_4', 'placeholder_5', 'placeholder_6')))
                            as src
                            on target.INSTANCE_NAME = src.INSTANCE_NAME and target.NAME = src.NAME and target.TYPE = src.TYPE and target.SYS_CREATED_ON = src.SYS_CREATED_ON
                            when matched then update set target.VALUE = src.VALUE,target.ETL_EXTRACT_DATE = src.ETL_EXTRACT_DATE
                            when not matched then insert (INSTANCE_NAME,NAME,VALUE,TYPE,SYS_CREATED_ON, ETL_EXTRACT_DATE) values (src.INSTANCE_NAME, src.NAME, src.VALUE,src.TYPE, src.SYS_CREATED_ON, src.ETL_EXTRACT_DATE);"""
    # SqlParse: Cannot extract source tables from complex MERGE statements
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"rds.staging.perspectium_instance_log_errors"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
    )


def test_swap_remaining_rds__q595():
    """swap remaining - Query 595"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF"."CMDB_CI_BUSINESS_APP" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.surf.cmdb_ci_business_app", "rds.surf.sys_audit_delete"},  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_swap_remaining_edw_ls__q602():
    """swap remaining - Query 602"""
    sql = """ CREATE OR REPLACE TEMPORARY TABLE EDW_LS."FINANCE_AR_EM"."TEMP_EM_ACCOUNTING_DOCUMENT_ITEM"  AS
            SELECT "BSEG_ClearingDate" as "BSEG_ClearingDate",
            "BSEG_ClearingEntryDate" as "BSEG_ClearingEntryDate",
            "CC_InvoiceClearingDays" as "CC_InvoiceClearingDays",
            "BSEG_Current_and_Prior_Qtr_Flag" as "BSEG_Current_and_Prior_Qtr_Flag",
            "BSEG_Client" as "BSEG_Client",
            "BSEG_CompanyCode" as "BSEG_CompanyCode",
            "BSEG_AccountingDocument" as "BSEG_AccountingDocument",
            "Test" as "Test",
            ROW_NUMBER()  OVER(
            PARTITION BY "BSEG_CompanyCode",
            "BSEG_AccountingDocument"
            ORDER BY "BSEG_ClearingDate" DESC
            )"Rank_Column"
             FROM
            (SELECT "BSEG_AccountingDocument" as "BSEG_AccountingDocument",
            "BSEG_CompanyCode" as "BSEG_CompanyCode",
            "BSEG_Client" as "BSEG_Client",
            "BSEG_ClearingDate" as "BSEG_ClearingDate",
            "BSEG_ClearingEntryDate" as "BSEG_ClearingEntryDate",
            "CC_InvoiceClearingDays" as "CC_InvoiceClearingDays",
            "BSEG_Current_and_Prior_Qtr_Flag" as "BSEG_Current_and_Prior_Qtr_Flag",
            "Test" as "Test" FROM
            (SELECT "BSEG_Client" as "BSEG_Client",
            "BSEG_CompanyCode" as "BSEG_CompanyCode",
            "BSEG_AccountingDocument" as "BSEG_AccountingDocument",
            "BSEG_ClearingDate" as "BSEG_ClearingDate",
            "BSEG_ClearingEntryDate" as "BSEG_ClearingEntryDate",
            "BSEG_AccountType" as "BSEG_AccountType",
            "BSEG_FPA_Quarter_Flag" as "BSEG_FPA_Quarter_Flag",
            "BSEG_Clearing_Date_Qtr_End_Date" as "BSEG_Clearing_Date_Qtr_End_Date",
            to_date("BSEG_ClearingDate",'placeholder_1')  as "CC_ToDateClearingDate",
            to_date("BSEG_ClearingEntryDate",'placeholder_2')  as "CC_ToDateClearingEntryDate",
            DATEDIFF(day,"CC_ToDateClearingDate","CC_ToDateClearingEntryDate")  as "CC_InvoiceClearingDays",
            IFF("BSEG_FPA_Quarter_Flag" = '2025-01-01 00:00:00', "BSEG_Clearing_Date_Qtr_End_Date",CURRENT_TIMESTAMP )  as "BSEG_Cleared_Current_Qtr_End",
            IFF("BSEG_FPA_Quarter_Flag" LIKE 'placeholder_4' ,'placeholder_5', 'placeholder_6')  as "BSEG_Current_and_Prior_Qtr_Flag",
            "BSEG_CompanyCode"||"BSEG_AccountingDocument" as "Test" FROM EDW_LS."FINANCE_AR_EM"."EM_ACCOUNTING_DOCUMENT_ITEM"
            WHERE "BSEG_ClearingDate" != '2025-01-01 00:00:00' and "BSEG_AccountType" = 'placeholder_8')"Projection_7"
            GROUP BY
            "BSEG_AccountingDocument",
            "BSEG_CompanyCode",
            "BSEG_Client",
            "BSEG_ClearingDate",
            "BSEG_ClearingEntryDate",
            "CC_InvoiceClearingDays",
            "BSEG_Current_and_Prior_Qtr_Flag",
            "Test")"Aggregation_1"
            QUALIFY "Rank_Column" <= 'placeholder_9'"""
    # SqlParse: Cannot extract source tables from subqueries/complex queries
    assert_table_lineage_equal(
        sql,
        {"edw_ls.finance_ar_em.em_accounting_document_item"},  # source_tables
        {"edw_ls.finance_ar_em.temp_em_accounting_document_item"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
    )


def test_swap_remaining_rds__q655():
    """swap remaining - Query 655"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."SURF_ALT"."U_SALES_TERRITORY" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."SURF_ALT"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.surf_alt.sys_audit_delete",
            "rds.surf_alt.u_sales_territory",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_swap_remaining_rds_surf_alt_stg_sys_audit_delete_delta_q716():
    """swap remaining - Query 716"""
    sql = """ MERGE INTO RDS.SURF_ALT.SYS_AUDIT_DELETE AS TGT
            USING (
                select * from
                (
                        select *,row_number() over(partition by sys_id order by sys_updated_on desc) as rn
                        from (select * from RDS.SURF_ALT.STG_SYS_AUDIT_DELETE_DELTA )

                ) where rn='placeholder_1'
            ) AS STG
            ON TGT.SYS_ID=STG.SYS_ID
            WHEN NOT MATCHED THEN INSERT("SYS_ID", "TABLENAME", "SYS_MOD_COUNT", "SYS_CREATED_ON", "PAYLOAD", "SYS_UPDATED_ON", "SYS_UPDATED_BY", "DISPLAY_VALUE", "SYS_CREATED_BY", "DOCUMENTKEY", "PSP_PER_DELETE_DT",PSP_PER_INSERT_DT,PSP_PER_UPDATE_DT,PSP_DELTA_UPDATE_DT) VALUES(STG."SYS_ID",STG."TABLENAME",STG."SYS_MOD_COUNT",STG."SYS_CREATED_ON",STG."PAYLOAD",STG."SYS_UPDATED_ON",STG."SYS_UPDATED_BY",STG."DISPLAY_VALUE",STG."SYS_CREATED_BY",STG."DOCUMENTKEY",STG."PSP_PER_DELETE_DT",current_timestamp(),current_timestamp(),current_timestamp())
            WHEN MATCHED and stg.sys_updated_on>tgt.sys_updated_on THEN UPDATE SET TGT."SYS_ID" = STG."SYS_ID", TGT."TABLENAME" = STG."TABLENAME", TGT."SYS_MOD_COUNT" = STG."SYS_MOD_COUNT", TGT."SYS_CREATED_ON" = STG."SYS_CREATED_ON", TGT."PAYLOAD" = STG."PAYLOAD", TGT."SYS_UPDATED_ON" = STG."SYS_UPDATED_ON", TGT."SYS_UPDATED_BY" = STG."SYS_UPDATED_BY", TGT."DISPLAY_VALUE" = STG."DISPLAY_VALUE", TGT."SYS_CREATED_BY" = STG."SYS_CREATED_BY", TGT."DOCUMENTKEY" = STG."DOCUMENTKEY", TGT."PSP_PER_DELETE_DT" = STG."PSP_PER_DELETE_DT" ,PSP_PER_UPDATE_DT=current_timestamp(), PSP_DELTA_UPDATE_DT=current_timestamp()
            WHEN MATCHED THEN UPDATE SET TGT."SYS_ID" = STG."SYS_ID", TGT."TABLENAME" = STG."TABLENAME", TGT."SYS_MOD_COUNT" = STG."SYS_MOD_COUNT", TGT."SYS_CREATED_ON" = STG."SYS_CREATED_ON", TGT."PAYLOAD" = STG."PAYLOAD", TGT."SYS_UPDATED_ON" = STG."SYS_UPDATED_ON", TGT."SYS_UPDATED_BY" = STG."SYS_UPDATED_BY", TGT."DISPLAY_VALUE" = STG."DISPLAY_VALUE", TGT."SYS_CREATED_BY" = STG."SYS_CREATED_BY", TGT."DOCUMENTKEY" = STG."DOCUMENTKEY", TGT."PSP_PER_DELETE_DT" = STG."PSP_PER_DELETE_DT" ,PSP_PER_UPDATE_DT=current_timestamp()"""
    # SqlParse: Cannot extract source tables from complex MERGE statements
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.surf_alt.stg_sys_audit_delete_delta"},  # source_tables
        {"rds.surf_alt.sys_audit_delete"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_swap_remaining_query_q731():
    """swap remaining - Query 731"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_SOURCE_COUNT = 2 WHERE SOURCE_SCHEMA = 'placeholder_3' AND                                     SOURCE_TABLE_NAME = 'placeholder_4'"""
    # SqlParse: Cannot extract source tables from subqueries/complex queries
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
    )


def test_swap_remaining_query_q787():
    """swap remaining - Query 787"""
    sql = """ UPDATE NOC.CONFIG.ETL_RDS_CONFIG_RECON                                     SET ETL_UPDATE_DATE = CURRENT_TIMESTAMP, LAST_RDS_JOB_RUN_ID = '2025-01-01 00:00:00',                                     TOTAL_SOURCE_COUNT = 2 WHERE SOURCE_SCHEMA = 'placeholder_3' AND                                     SOURCE_TABLE_NAME = 'placeholder_4'"""
    # SqlParse: Cannot extract source tables from subqueries/complex queries
    assert_table_lineage_equal(
        sql,
        set(),  # source_tables
        {"noc.config.etl_rds_config_recon"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
    )


def test_swap_remaining_rds__q866():
    """swap remaining - Query 866"""
    sql = """ insert into RDS."STAGING"."INSTANCE_TABLES_DELETED_SYS_ID" ("SCHEMA" ,  "STORED_PROCEDURE" ,  "SOURCE_TABLE_NAME" ,  "SYS_ID" ,  "TIME_STAMP")
    SELECT 'placeholder_1', 'placeholder_2', 'placeholder_3', SYS_ID,  CURRENT_TIMESTAMP
    FROM RDS."APPSTORE"."SN_APPSTORE_APPLICATION" where sys_id IN (SELECT DISTINCT D.DOCUMENTKEY
    FROM "RDS"."APPSTORE"."SYS_AUDIT_DELETE" D
    WHERE D.TABLENAME LIKE LOWER('placeholder_4')  AND CAST( D.SYS_UPDATED_ON AS DATE )  >= DATEADD(DAY, 'placeholder_5', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {
            "rds.appstore.sn_appstore_application",
            "rds.appstore.sys_audit_delete",
        },  # source_tables
        {"rds.staging.instance_tables_deleted_sys_id"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )


def test_swap_remaining_dynamics365_stg_sn_opportunitysubproductses_q899():
    """swap remaining - Query 899"""
    sql = """ MERGE INTO DYNAMICS365.sn_opportunitysubproductses TARGET USING ( SELECT * FROM DYNAMICS365.stg_sn_opportunitysubproductses WHERE ETL_REFRESH_SCHEDULE = 'placeholder_1') INPUT ON "TARGET"."SN_OPPORTUNITYSUBPRODUCTSID"="INPUT"."SN_OPPORTUNITYSUBPRODUCTSID" WHEN MATCHED THEN UPDATE SET "TARGET"."CREATEDONBEHALFBY"="INPUT"."CREATEDONBEHALFBY","TARGET"."OWNINGTEAM"="INPUT"."OWNINGTEAM","TARGET"."TRANSACTIONCURRENCYIDNAME"="INPUT"."TRANSACTIONCURRENCYIDNAME","TARGET"."STATUSCODE"="INPUT"."STATUSCODE","TARGET"."IMPORTSEQUENCENUMBER"="INPUT"."IMPORTSEQUENCENUMBER","TARGET"."OWNINGBUSINESSUNITNAME"="INPUT"."OWNINGBUSINESSUNITNAME","TARGET"."VERSIONNUMBER"="INPUT"."VERSIONNUMBER","TARGET"."SN_OPPORTUNITYSUBPRODUCTSID"="INPUT"."SN_OPPORTUNITYSUBPRODUCTSID","TARGET"."MODIFIEDONBEHALFBY"="INPUT"."MODIFIEDONBEHALFBY","TARGET"."CREATEDBYYOMINAME"="INPUT"."CREATEDBYYOMINAME","TARGET"."OWNINGBUSINESSUNIT"="INPUT"."OWNINGBUSINESSUNIT","TARGET"."STATUSCODENAME"="INPUT"."STATUSCODENAME","TARGET"."SN_NAME"="INPUT"."SN_NAME","TARGET"."STATECODE"="INPUT"."STATECODE","TARGET"."SN_AUTOCREATED"="INPUT"."SN_AUTOCREATED","TARGET"."OWNERIDYOMINAME"="INPUT"."OWNERIDYOMINAME","TARGET"."SN_PERCENTAGE"="INPUT"."SN_PERCENTAGE","TARGET"."OWNERID"="INPUT"."OWNERID","TARGET"."CREATEDBY"="INPUT"."CREATEDBY","TARGET"."MODIFIEDONBEHALFBYYOMINAME"="INPUT"."MODIFIEDONBEHALFBYYOMINAME","TARGET"."SN_SUBPRODUCTNAME"="INPUT"."SN_SUBPRODUCTNAME","TARGET"."SN_OPPORTUNITYPRODUCT"="INPUT"."SN_OPPORTUNITYPRODUCT","TARGET"."UTCCONVERSIONTIMEZONECODE"="INPUT"."UTCCONVERSIONTIMEZONECODE","TARGET"."SN_ANNUALRATEAMOUNT_BASE"="INPUT"."SN_ANNUALRATEAMOUNT_BASE","TARGET"."CREATEDONBEHALFBYYOMINAME"="INPUT"."CREATEDONBEHALFBYYOMINAME","TARGET"."SN_AMOUNT"="INPUT"."SN_AMOUNT","TARGET"."CREATEDONBEHALFBYNAME"="INPUT"."CREATEDONBEHALFBYNAME","TARGET"."MODIFIEDON"="INPUT"."MODIFIEDON","TARGET"."STATECODENAME"="INPUT"."STATECODENAME","TARGET"."MODIFIEDBYYOMINAME"="INPUT"."MODIFIEDBYYOMINAME","TARGET"."MODIFIEDBY"="INPUT"."MODIFIEDBY","TARGET"."SN_OPPORTUNITYPRODUCTNAME"="INPUT"."SN_OPPORTUNITYPRODUCTNAME","TARGET"."CREATEDBYNAME"="INPUT"."CREATEDBYNAME","TARGET"."OWNERIDNAME"="INPUT"."OWNERIDNAME","TARGET"."OWNINGUSER"="INPUT"."OWNINGUSER","TARGET"."MODIFIEDONBEHALFBYNAME"="INPUT"."MODIFIEDONBEHALFBYNAME","TARGET"."SN_CURRENCYCODE"="INPUT"."SN_CURRENCYCODE","TARGET"."SN_AMOUNT_BASE"="INPUT"."SN_AMOUNT_BASE","TARGET"."EXCHANGERATE"="INPUT"."EXCHANGERATE","TARGET"."SN_SUBPRODUCT"="INPUT"."SN_SUBPRODUCT","TARGET"."MODIFIEDBYNAME"="INPUT"."MODIFIEDBYNAME","TARGET"."OWNERIDTYPE"="INPUT"."OWNERIDTYPE","TARGET"."CREATEDON"="INPUT"."CREATEDON","TARGET"."TIMEZONERULEVERSIONNUMBER"="INPUT"."TIMEZONERULEVERSIONNUMBER","TARGET"."SN_ANNUALEXCHANGERATE"="INPUT"."SN_ANNUALEXCHANGERATE","TARGET"."OVERRIDDENCREATEDON"="INPUT"."OVERRIDDENCREATEDON","TARGET"."SN_ANNUALRATEAMOUNT"="INPUT"."SN_ANNUALRATEAMOUNT","TARGET"."SN_AUTOCREATEDNAME"="INPUT"."SN_AUTOCREATEDNAME","TARGET"."TRANSACTIONCURRENCYID"="INPUT"."TRANSACTIONCURRENCYID","TARGET"."SN_CUSTOMEXCHANGERATE"="INPUT"."SN_CUSTOMEXCHANGERATE","TARGET"."ETL_UPDATE_DATE"=CURRENT_TIMESTAMP WHEN NOT MATCHED THEN INSERT ("CREATEDONBEHALFBY","OWNINGTEAM","TRANSACTIONCURRENCYIDNAME","STATUSCODE","IMPORTSEQUENCENUMBER","OWNINGBUSINESSUNITNAME","VERSIONNUMBER","SN_OPPORTUNITYSUBPRODUCTSID","MODIFIEDONBEHALFBY","CREATEDBYYOMINAME","OWNINGBUSINESSUNIT","STATUSCODENAME","SN_NAME","STATECODE","SN_AUTOCREATED","OWNERIDYOMINAME","SN_PERCENTAGE","OWNERID","CREATEDBY","MODIFIEDONBEHALFBYYOMINAME","SN_SUBPRODUCTNAME","SN_OPPORTUNITYPRODUCT","UTCCONVERSIONTIMEZONECODE","SN_ANNUALRATEAMOUNT_BASE","CREATEDONBEHALFBYYOMINAME","SN_AMOUNT","CREATEDONBEHALFBYNAME","MODIFIEDON","STATECODENAME","MODIFIEDBYYOMINAME","MODIFIEDBY","SN_OPPORTUNITYPRODUCTNAME","CREATEDBYNAME","OWNERIDNAME","OWNINGUSER","MODIFIEDONBEHALFBYNAME","SN_CURRENCYCODE","SN_AMOUNT_BASE","EXCHANGERATE","SN_SUBPRODUCT","MODIFIEDBYNAME","OWNERIDTYPE","CREATEDON","TIMEZONERULEVERSIONNUMBER","SN_ANNUALEXCHANGERATE","OVERRIDDENCREATEDON","SN_ANNUALRATEAMOUNT","SN_AUTOCREATEDNAME","TRANSACTIONCURRENCYID","SN_CUSTOMEXCHANGERATE","ETL_UPDATE_DATE") VALUES ("INPUT"."CREATEDONBEHALFBY","INPUT"."OWNINGTEAM","INPUT"."TRANSACTIONCURRENCYIDNAME","INPUT"."STATUSCODE","INPUT"."IMPORTSEQUENCENUMBER","INPUT"."OWNINGBUSINESSUNITNAME","INPUT"."VERSIONNUMBER","INPUT"."SN_OPPORTUNITYSUBPRODUCTSID","INPUT"."MODIFIEDONBEHALFBY","INPUT"."CREATEDBYYOMINAME","INPUT"."OWNINGBUSINESSUNIT","INPUT"."STATUSCODENAME","INPUT"."SN_NAME","INPUT"."STATECODE","INPUT"."SN_AUTOCREATED","INPUT"."OWNERIDYOMINAME","INPUT"."SN_PERCENTAGE","INPUT"."OWNERID","INPUT"."CREATEDBY","INPUT"."MODIFIEDONBEHALFBYYOMINAME","INPUT"."SN_SUBPRODUCTNAME","INPUT"."SN_OPPORTUNITYPRODUCT","INPUT"."UTCCONVERSIONTIMEZONECODE","INPUT"."SN_ANNUALRATEAMOUNT_BASE","INPUT"."CREATEDONBEHALFBYYOMINAME","INPUT"."SN_AMOUNT","INPUT"."CREATEDONBEHALFBYNAME","INPUT"."MODIFIEDON","INPUT"."STATECODENAME","INPUT"."MODIFIEDBYYOMINAME","INPUT"."MODIFIEDBY","INPUT"."SN_OPPORTUNITYPRODUCTNAME","INPUT"."CREATEDBYNAME","INPUT"."OWNERIDNAME","INPUT"."OWNINGUSER","INPUT"."MODIFIEDONBEHALFBYNAME","INPUT"."SN_CURRENCYCODE","INPUT"."SN_AMOUNT_BASE","INPUT"."EXCHANGERATE","INPUT"."SN_SUBPRODUCT","INPUT"."MODIFIEDBYNAME","INPUT"."OWNERIDTYPE","INPUT"."CREATEDON","INPUT"."TIMEZONERULEVERSIONNUMBER","INPUT"."SN_ANNUALEXCHANGERATE","INPUT"."OVERRIDDENCREATEDON","INPUT"."SN_ANNUALRATEAMOUNT","INPUT"."SN_AUTOCREATEDNAME","INPUT"."TRANSACTIONCURRENCYID","INPUT"."SN_CUSTOMEXCHANGERATE",CURRENT_TIMESTAMP)"""
    # SqlParse: Cannot extract source tables from complex MERGE statements
    assert_table_lineage_equal(
        sql,
        {"dynamics365.stg_sn_opportunitysubproductses"},  # source_tables
        {"dynamics365.sn_opportunitysubproductses"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
    )


def test_swap_remaining_rds_dynamics365_businessunits_q17475():
    """swap remaining - Query 17475"""
    sql = """ insert into RDS.DYNAMICS365.TABLES_DELETED_RECORDS_ID ( SCHEMA ,  STORED_PROCEDURE ,  SOURCE_TABLE_NAME ,  OBJECT_ID ,  TIME_STAMP )
    select 'placeholder_1' , 'placeholder_2' , 'placeholder_3' , "BUSINESSUNITID" ,  CURRENT_TIMESTAMP
    FROM RDS.DYNAMICS365.BUSINESSUNITS
    where "BUSINESSUNITID" IN (select distinct OBJECTID FROM "RDS"."DYNAMICS365"."AUDITS" WHERE "ACTION"='placeholder_4' and "OPERATION" = 'placeholder_5' AND LOWER( "OBJECTTYPECODE" ) = 'placeholder_6' AND CAST( "CREATEDON" AS DATE ) >=DATEADD(DAY, 'placeholder_7', CURRENT_DATE ))"""
    # SqlParse: Includes target table as source in INSERT INTO...SELECT
    # Graph: Parsers create different graph structures (table lineage is correct)
    assert_table_lineage_equal(
        sql,
        {"rds.dynamics365.audits", "rds.dynamics365.businessunits"},  # source_tables
        {"rds.dynamics365.tables_deleted_records_id"},  # target_tables
        dialect="snowflake",
        test_sqlparse=False,
        skip_graph_check=True,
    )
