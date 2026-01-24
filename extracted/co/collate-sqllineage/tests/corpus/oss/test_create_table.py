"""Tests for create table."""

import pytest

from tests.helpers import (
    TestColumnQualifierTuple,
    assert_column_lineage_equal,
    assert_table_lineage_equal,
)


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_create_table_query_nested_joins(dialect: str):
    sql = """CREATE OR REPLACE TABLE IDP_CASHFlow_dev.MRI.DISCOUNTED_CASHFLOWS_LICAT(
    "SLC_SEC_ID" STRING,
    "AS_OF_DATE" DATE NOT NULL,
    "PARENT_ENTITY_ID" STRING('zzz') NOT NULL,
    "CHILD_ENTITY_ID" STRING('zzz'),
    "SOURCE_SYSTEM_PORTFOLIO" STRING('zzz'),
    "CASHFLOW_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "LICAT_ASSET_TEXT" STRING('zzz'),
    "CREDIT_RISK_SOL_FAC_PERC" BIGINT,
    "MARKET_RISK_SOL_FAC_PERC" BIGINT,
    "DISCOUNT_FACTOR_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "DISC_CONTRACTUAL_CF_PV_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "DISC_RECOVERABLE_CF_PV_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "CREDIT_RISK_DISC_CF_PV_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "MARKET_RISK_RESIDUAL_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "MARKET_RISK_SOLVENCY_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "CREDIT_RISK_SOLVENCY_UNADJUSTED_AMOUNT_ORIGINAL" NUMBER('zzz', 'zzz'),
    "RUNDATE" TIMESTAMP_NTZ NOT NULL,
    "RUNID" BIGINT NOT NULL
) AS
SELECT
    *
FROM
    (
        SELECT
            'zzz' AS "SLC_SEC_ID",
            "AS_OF_DATE",
            "PARENT_ENTITY_ID",
            "CHILD_ENTITY_ID",
            "SOURCE_SYSTEM_PORTFOLIO",
            "CASHFLOW_AMOUNT_ORIGINAL",
            "LICAT_ASSET_TEXT",
            "CREDIT_RISK_SOL_FAC_PERC",
            "MARKET_RISK_SOL_FAC_PERC",
            "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
            "DISC_CONTRACTUAL_CF_PV_AMOUNT_ORIGINAL",
            "DISC_RECOVERABLE_CF_PV_AMOUNT_ORIGINAL",
            "CREDIT_RISK_DISC_CF_PV_AMOUNT_ORIGINAL",
            "MARKET_RISK_RESIDUAL_AMOUNT_ORIGINAL",
            CASE
                WHEN (
                    ("LICAT_ASSET_TEXT" = 'zzz')
                    OR ("LICAT_ASSET_TEXT" = 'zzz')
                ) THEN 'zzz'
                WHEN ("LICAT_ASSET_TEXT" = 'zzz') THEN (
                    (
                        "MARKET_RISK_RESIDUAL_AMOUNT_ORIGINAL" * "MARKET_RISK_SOL_FAC_PERC"
                    ) / 'zzz'
                )
                ELSE 'zzz' :: INT
            END AS "MARKET_RISK_SOLVENCY_AMOUNT_ORIGINAL",
            CASE
                WHEN (
                    ("LICAT_ASSET_TEXT" = 'zzz')
                    OR ("LICAT_ASSET_TEXT" = 'zzz')
                ) THEN 'zzz'
                WHEN ("LICAT_ASSET_TEXT" = 'zzz') THEN (
                    (
                        "MARKET_RISK_RESIDUAL_AMOUNT_ORIGINAL" * "CREDIT_RISK_SOL_FAC_PERC"
                    ) / 'zzz'
                )
                ELSE 'zzz' :: INT
            END AS "CREDIT_RISK_SOLVENCY_UNADJUSTED_AMOUNT_ORIGINAL",
            "RUNDATE",
            "RUNID"
        FROM
            (
                SELECT
                    "PROPERTY_ID",
                    "SCENARIO",
                    "LICAT_ASSET_TEXT",
                    "IFRS_STATEMENT_VALUE_AMT_ORIG",
                    "MARKET_RISK_SOL_FAC_PERC",
                    "CREDIT_RISK_SOL_FAC_PERC",
                    "CASHFLOW_AMOUNT_ORIGINAL",
                    "RUNID",
                    "PARENT_ENTITY_ID",
                    "CHILD_ENTITY_ID",
                    "RUNDATE",
                    "AS_OF_DATE",
                    "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
                    "SOURCE_SYSTEM_PORTFOLIO",
                    "DISC_CONTRACTUAL_CF_PV_AMOUNT_ORIGINAL",
                    "DISC_RECOVERABLE_CF_PV_AMOUNT_ORIGINAL",
                    "CREDIT_RISK_DISC_CF_PV_AMOUNT_ORIGINAL",
                    CASE
                        WHEN (
                            ("LICAT_ASSET_TEXT" = 'zzz')
                            OR ("LICAT_ASSET_TEXT" = 'zzz')
                        ) THEN 'zzz'
                        WHEN ("LICAT_ASSET_TEXT" = 'zzz') THEN (
                            "IFRS_STATEMENT_VALUE_AMT_ORIG" - "CREDIT_RISK_DISC_CF_PV_AMOUNT_ORIGINAL"
                        )
                        ELSE 'zzz' :: INT
                    END AS "MARKET_RISK_RESIDUAL_AMOUNT_ORIGINAL"
                FROM
                    (
                        SELECT
                            "PROPERTY_ID",
                            "SCENARIO",
                            "LICAT_ASSET_TEXT",
                            "IFRS_STATEMENT_VALUE_AMT_ORIG",
                            "MARKET_RISK_SOL_FAC_PERC",
                            "CREDIT_RISK_SOL_FAC_PERC",
                            "CASHFLOW_AMOUNT_ORIGINAL",
                            "RUNID",
                            "PARENT_ENTITY_ID",
                            "CHILD_ENTITY_ID",
                            "RUNDATE",
                            "AS_OF_DATE",
                            "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
                            "SOURCE_SYSTEM_PORTFOLIO",
                            "DISC_CONTRACTUAL_CF_PV_AMOUNT_ORIGINAL",
                            "DISC_RECOVERABLE_CF_PV_AMOUNT_ORIGINAL",
                            CASE
                                WHEN (
                                    "DISC_CONTRACTUAL_CF_PV_AMOUNT_ORIGINAL" IS NOT True
                                    OR "DISC_RECOVERABLE_CF_PV_AMOUNT_ORIGINAL" IS NOT True
                                ) THEN (
                                    "DISC_CONTRACTUAL_CF_PV_AMOUNT_ORIGINAL" + "DISC_RECOVERABLE_CF_PV_AMOUNT_ORIGINAL"
                                )
                                ELSE 'zzz' :: INT
                            END AS "CREDIT_RISK_DISC_CF_PV_AMOUNT_ORIGINAL"
                        FROM
                            (
                                SELECT
                                    "PROPERTY_ID",
                                    "SCENARIO",
                                    "LICAT_ASSET_TEXT",
                                    "IFRS_STATEMENT_VALUE_AMT_ORIG",
                                    "MARKET_RISK_SOL_FAC_PERC",
                                    "CREDIT_RISK_SOL_FAC_PERC",
                                    "CASHFLOW_AMOUNT_ORIGINAL",
                                    "RUNID",
                                    "PARENT_ENTITY_ID",
                                    "CHILD_ENTITY_ID",
                                    "RUNDATE",
                                    "AS_OF_DATE",
                                    "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
                                    "SOURCE_SYSTEM_PORTFOLIO",
                                    sum(
                                        CASE
                                            WHEN ("CASH_FLOW_TYPE" = 'zzz') THEN "DISCOUNT_FACTOR_AMOUNT_ORIGINAL"
                                            ELSE 'zzz' :: INT
                                        END
                                    ) AS "DISC_CONTRACTUAL_CF_PV_AMOUNT_ORIGINAL",
                                    sum(
                                        CASE
                                            WHEN ("CASH_FLOW_TYPE" = 'zzz') THEN "DISCOUNT_FACTOR_AMOUNT_ORIGINAL"
                                            ELSE 'zzz' :: INT
                                        END
                                    ) AS "DISC_RECOVERABLE_CF_PV_AMOUNT_ORIGINAL"
                                FROM
                                    (
                                        SELECT
                                            * RENAME (
                                                "LICAT_CREDIT_RISK_SOL_FAC_PERC" AS CREDIT_RISK_SOL_FAC_PERC
                                            )
                                        FROM
                                            (
                                                SELECT
                                                    * RENAME (
                                                        "LICAT_MARKET_RISK_SOL_FAC_PERC" AS MARKET_RISK_SOL_FAC_PERC
                                                    )
                                                FROM
                                                    (
                                                        SELECT
                                                            *
                                                        FROM
                                                            (
                                                                (
                                                                    SELECT
                                                                        "AS_OF_DATE" AS "AS_OF_DATE",
                                                                        "SEGMENT_ID" AS "SEGMENT_ID",
                                                                        "PROPERTY_ID" AS "PROPERTY_ID",
                                                                        "SOURCE_SYSTEM_PORTFOLIO" AS "SOURCE_SYSTEM_PORTFOLIO",
                                                                        "CASH_FLOW_SEQUENTIAL_YEAR" AS "CASH_FLOW_SEQUENTIAL_YEAR",
                                                                        "CASH_FLOW_TYPE" AS "CASH_FLOW_TYPE",
                                                                        "SCENARIO" AS "SCENARIO",
                                                                        "CASHFLOW_AMOUNT_ORIGINAL" AS "CASHFLOW_AMOUNT_ORIGINAL",
                                                                        "CASHFLOW_AMOUNT_FUNCTIONAL" AS "CASHFLOW_AMOUNT_FUNCTIONAL",
                                                                        "DISCOUNT_FACTOR_AMOUNT_ORIGINAL" AS "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
                                                                        "DISCOUNT_FACTOR_PCT" AS "DISCOUNT_FACTOR_PCT",
                                                                        "DISCOUNTED_AMOUNT_FUNCTIONAL" AS "DISCOUNTED_AMOUNT_FUNCTIONAL",
                                                                        "RUNDATE" AS "RUNDATE",
                                                                        "RUNID" AS "RUNID",
                                                                        "MAJOR_PRODUCT_CODE" AS "MAJOR_PRODUCT_CODE",
                                                                        "LICAT_ASSET_TEXT" AS "LICAT_ASSET_TEXT",
                                                                        "LICAT_CREDIT_RISK_SOL_FAC_PERC" AS "LICAT_CREDIT_RISK_SOL_FAC_PERC",
                                                                        "LICAT_MARKET_RISK_SOL_FAC_PERC" AS "LICAT_MARKET_RISK_SOL_FAC_PERC",
                                                                        "RECORD_TYPE" AS "RECORD_TYPE",
                                                                        "PARENT_ENTITY_ID" AS "PARENT_ENTITY_ID",
                                                                        "CHILD_ENTITY_ID" AS "CHILD_ENTITY_ID",
                                                                        "MAJOR_PRODUCT_CODECF" AS "MAJOR_PRODUCT_CODECF",
                                                                        "PORTFOLIO_NAME" AS "PORTFOLIO_NAME",
                                                                        "ALLOCATION_PERCENT" AS "ALLOCATION_PERCENT",
                                                                        "FILENAME" AS "FILENAME",
                                                                        "RUNDATECF" AS "RUNDATECF",
                                                                        "RUNIDCF" AS "RUNIDCF",
                                                                        "ASOFDATE" AS "ASOFDATE",
                                                                        "PROPERTY_IDPR" AS "PROPERTY_IDPR",
                                                                        "DEAL_SYSTEM_ID" AS "l_0000_DEAL_SYSTEM_ID",
                                                                        "DEAL_NAME_TEXT" AS "DEAL_NAME_TEXT",
                                                                        "COMPONENT_NAME_TEXT" AS "COMPONENT_NAME_TEXT",
                                                                        "ASSET_MANAGER_CODE" AS "ASSET_MANAGER_CODE",
                                                                        "ASSET_MANAGER_NAME" AS "ASSET_MANAGER_NAME",
                                                                        "PROJECT_ID" AS "PROJECT_ID",
                                                                        "PROJECT_NAME" AS "PROJECT_NAME",
                                                                        "PROPERTY_ADDRESS_LINE_1_TEXT" AS "PROPERTY_ADDRESS_LINE_1_TEXT",
                                                                        "PROPERTY_ADDRESS_LINE_2_TEXT" AS "PROPERTY_ADDRESS_LINE_2_TEXT",
                                                                        "PROPERTY_ADDRESS_LINE_3_TEXT" AS "PROPERTY_ADDRESS_LINE_3_TEXT",
                                                                        "PROPERTY_CITY_NAME" AS "PROPERTY_CITY_NAME",
                                                                        "PROPERTY_STATE" AS "PROPERTY_STATE",
                                                                        "PROPERTY_POSTAL_CODE" AS "PROPERTY_POSTAL_CODE",
                                                                        "PROPERTY_COUNTRY_CODE" AS "PROPERTY_COUNTRY_CODE",
                                                                        "PROPERTY_CURRENCY" AS "PROPERTY_CURRENCY",
                                                                        "PROPERTY_USAGE_CODE" AS "PROPERTY_USAGE_CODE",
                                                                        "PROPERTY_TYPE_CODE" AS "PROPERTY_TYPE_CODE",
                                                                        "COMPONENT_STATUS_TEXT" AS "COMPONENT_STATUS_TEXT",
                                                                        "CANADIAN_FEDERAL_TAX_CODE" AS "CANADIAN_FEDERAL_TAX_CODE",
                                                                        "ORIGINAL_ISSUE_DATE" AS "ORIGINAL_ISSUE_DATE",
                                                                        "SALE_DATE" AS "SALE_DATE",
                                                                        "PURCHASE_COMMITMENT_EXPIRY_DATE" AS "PURCHASE_COMMITMENT_EXPIRY_DATE",
                                                                        "PURCHASE_COMMITMENT_YIELD_PERCENT" AS "PURCHASE_COMMITMENT_YIELD_PERCENT",
                                                                        "SALE_COMMITMENT_EXPIRY_DATE" AS "SALE_COMMITMENT_EXPIRY_DATE",
                                                                        "SALE_COMMITMENT_YIELD_PERCENT" AS "SALE_COMMITMENT_YIELD_PERCENT",
                                                                        "PHYSICAL_COMPLETION_DATE" AS "PHYSICAL_COMPLETION_DATE",
                                                                        "SLF_OCCUPANCY_PERCENT" AS "SLF_OCCUPANCY_PERCENT",
                                                                        "INCOME_PRODUCING_DATE" AS "INCOME_PRODUCING_DATE",
                                                                        "JOINT_VENTURE_PARTNER_NAME" AS "JOINT_VENTURE_PARTNER_NAME",
                                                                        "SLF_OWNERSHIP_PERCENT" AS "SLF_OWNERSHIP_PERCENT",
                                                                        "ASSUMED_MORTGAGE_NUMBER" AS "ASSUMED_MORTGAGE_NUMBER",
                                                                        "ASSUMED_MORTGAGE_NAME" AS "ASSUMED_MORTGAGE_NAME",
                                                                        "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE_CODE" AS "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE_CODE",
                                                                        "ASSUMED_MORTGAGE_INTEREST_RATE_PERCENT" AS "ASSUMED_MORTGAGE_INTEREST_RATE_PERCENT",
                                                                        "ASSUMED_MORTGAGE_MATURITY_DATE" AS "ASSUMED_MORTGAGE_MATURITY_DATE",
                                                                        "PROPERTY_MANAGER_ID" AS "PROPERTY_MANAGER_ID",
                                                                        "PROPERTY_MANAGER_NAME" AS "PROPERTY_MANAGER_NAME",
                                                                        "INVESTMENT_MANAGER_FULL_NAME" AS "INVESTMENT_MANAGER_FULL_NAME",
                                                                        "ECONOMIC_EXPIRY_DATE" AS "ECONOMIC_EXPIRY_DATE",
                                                                        "PROPERTY_APPRAISAL_DATE" AS "PROPERTY_APPRAISAL_DATE",
                                                                        "REPORTING_REGION" AS "REPORTING_REGION",
                                                                        "INTERNAL_EXTERNAL_APPRAISAL_METHOD" AS "INTERNAL_EXTERNAL_APPRAISAL_METHOD",
                                                                        "IPD_FUND_TYPE_CD" AS "IPD_FUND_TYPE_CD",
                                                                        "CMA_CD" AS "CMA_CD",
                                                                        "IPD_PROVINCE_CD" AS "IPD_PROVINCE_CD",
                                                                        "IPD_INVESTMENT_TYPE_CD" AS "IPD_INVESTMENT_TYPE_CD",
                                                                        "IPD_BUILDINGS_CNT" AS "IPD_BUILDINGS_CNT",
                                                                        "OWNER_OCCUPIED_IND" AS "OWNER_OCCUPIED_IND",
                                                                        "PREDOMINANT_CURRENT_USE_CD" AS "PREDOMINANT_CURRENT_USE_CD",
                                                                        "PROPERTY_TYPE_RETAIL_CD" AS "PROPERTY_TYPE_RETAIL_CD",
                                                                        "PROPERTY_TYPE_MIXED_CD" AS "PROPERTY_TYPE_MIXED_CD",
                                                                        "RETAIL_ENCLOSED" AS "RETAIL_ENCLOSED",
                                                                        "OFFICE_NODE" AS "OFFICE_NODE",
                                                                        "INDUSTRY_NODE" AS "INDUSTRY_NODE",
                                                                        "ACTUAL_APPRAISAL_CURR_QUARTER" AS "ACTUAL_APPRAISAL_CURR_QUARTER",
                                                                        "APPRAISAL_METHOD_CD" AS "APPRAISAL_METHOD_CD",
                                                                        "APPRAISAL_STABILIZED_INCOME_AMT" AS "APPRAISAL_STABILIZED_INCOME_AMT",
                                                                        "APPRAISAL_TOTAL_AREA" AS "APPRAISAL_TOTAL_AREA",
                                                                        "APPRAISAL_RENTABLE_AREA" AS "APPRAISAL_RENTABLE_AREA",
                                                                        "APPRAISAL_TOTAL_UNITS_CNT" AS "APPRAISAL_TOTAL_UNITS_CNT",
                                                                        "APPRAISAL_RENTABLE_UNITS_CNT" AS "APPRAISAL_RENTABLE_UNITS_CNT",
                                                                        "DISCOUNT_RATE_CASH_FLOW_AMT" AS "DISCOUNT_RATE_CASH_FLOW_AMT",
                                                                        "EXIT_YIELD_AMT" AS "EXIT_YIELD_AMT",
                                                                        "CAPITALIZATION_RATE_AMT" AS "CAPITALIZATION_RATE_AMT",
                                                                        "GROSS_PART_PURCHASE_EXP_PER_NATIVE_AMT" AS "GROSS_PART_PURCHASE_EXP_PER_NATIVE_AMT",
                                                                        "IPD_ACQUISITION_ROUTE_CD" AS "IPD_ACQUISITION_ROUTE_CD",
                                                                        "IPD_GROSS_PURCHASE_PRICE_AMT" AS "IPD_GROSS_PURCHASE_PRICE_AMT",
                                                                        "IPD_NET_SALE_PRICE_AMT" AS "IPD_NET_SALE_PRICE_AMT",
                                                                        "IPD_SALE_DT" AS "IPD_SALE_DT",
                                                                        "PORTFOLIO_ALLOCATION_CD" AS "PORTFOLIO_ALLOCATION_CD",
                                                                        "PROPERTY_TYPE_OFFICE_CD" AS "PROPERTY_TYPE_OFFICE_CD",
                                                                        "PROPERTY_TYPE_RESIDENTIAL_CD" AS "PROPERTY_TYPE_RESIDENTIAL_CD",
                                                                        "PROPERTY_TYPE_INDUSTRIAL_CD" AS "PROPERTY_TYPE_INDUSTRIAL_CD",
                                                                        "PROPERTY_TYPE_OTHER_CD" AS "PROPERTY_TYPE_OTHER_CD",
                                                                        "OFFICE_BUILDING_GRADE_CD" AS "OFFICE_BUILDING_GRADE_CD",
                                                                        "PROPERTY_USAGE" AS "PROPERTY_USAGE",
                                                                        "PROPERTY_SUB_TYPE" AS "PROPERTY_SUB_TYPE",
                                                                        "PROPERTY_TYPE" AS "PROPERTY_TYPE",
                                                                        "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE" AS "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE",
                                                                        "ASIA_REAL_ESTATE_ID" AS "ASIA_REAL_ESTATE_ID",
                                                                        "UK_PROPERTY_ID" AS "UK_PROPERTY_ID",
                                                                        "UK_SECONDARY_PROPERTY_ID" AS "UK_SECONDARY_PROPERTY_ID",
                                                                        "IFRS_LEDGER_ASSET_TYPE" AS "IFRS_LEDGER_ASSET_TYPE",
                                                                        "SLC_ASSET_TYPE" AS "SLC_ASSET_TYPE",
                                                                        "SLC_SECURITY_TYPE" AS "SLC_SECURITY_TYPE",
                                                                        "VALUE_ADDED_TAX_IND" AS "VALUE_ADDED_TAX_IND",
                                                                        "SLC_SEC_ID" AS "SLC_SEC_ID",
                                                                        "STATUS" AS "STATUS",
                                                                        "LAST_ACTIVE" AS "LAST_ACTIVE",
                                                                        "RUNIDPR" AS "RUNIDPR",
                                                                        "RUNDATEPR" AS "RUNDATEPR"
                                                                    FROM
                                                                        (
                                                                            SELECT
                                                                                *
                                                                            FROM
                                                                                (
                                                                                    (
                                                                                        SELECT
                                                                                            "AS_OF_DATE" AS "AS_OF_DATE",
                                                                                            "SEGMENT_ID" AS "SEGMENT_ID",
                                                                                            "PROPERTY_ID" AS "PROPERTY_ID",
                                                                                            "SOURCE_SYSTEM_PORTFOLIO" AS "SOURCE_SYSTEM_PORTFOLIO",
                                                                                            "CASH_FLOW_SEQUENTIAL_YEAR" AS "CASH_FLOW_SEQUENTIAL_YEAR",
                                                                                            "CASH_FLOW_TYPE" AS "CASH_FLOW_TYPE",
                                                                                            "SCENARIO" AS "SCENARIO",
                                                                                            "CASHFLOW_AMOUNT_ORIGINAL" AS "CASHFLOW_AMOUNT_ORIGINAL",
                                                                                            "CASHFLOW_AMOUNT_FUNCTIONAL" AS "CASHFLOW_AMOUNT_FUNCTIONAL",
                                                                                            "DISCOUNT_FACTOR_AMOUNT_ORIGINAL" AS "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
                                                                                            "DISCOUNT_FACTOR_PCT" AS "DISCOUNT_FACTOR_PCT",
                                                                                            "DISCOUNTED_AMOUNT_FUNCTIONAL" AS "DISCOUNTED_AMOUNT_FUNCTIONAL",
                                                                                            "RUNDATE" AS "RUNDATE",
                                                                                            "RUNID" AS "RUNID",
                                                                                            "MAJOR_PRODUCT_CODE" AS "MAJOR_PRODUCT_CODE",
                                                                                            "LICAT_ASSET_TEXT" AS "LICAT_ASSET_TEXT",
                                                                                            "LICAT_CREDIT_RISK_SOL_FAC_PERC" AS "LICAT_CREDIT_RISK_SOL_FAC_PERC",
                                                                                            "LICAT_MARKET_RISK_SOL_FAC_PERC" AS "LICAT_MARKET_RISK_SOL_FAC_PERC",
                                                                                            "RECORD_TYPE" AS "RECORD_TYPE",
                                                                                            "PARENT_ENTITY_ID" AS "PARENT_ENTITY_ID",
                                                                                            "CHILD_ENTITY_ID" AS "CHILD_ENTITY_ID",
                                                                                            "MAJOR_PRODUCT_CODECF" AS "MAJOR_PRODUCT_CODECF",
                                                                                            "PORTFOLIO_NAME" AS "PORTFOLIO_NAME",
                                                                                            "ALLOCATION_PERCENT" AS "ALLOCATION_PERCENT",
                                                                                            "FILENAME" AS "FILENAME",
                                                                                            "RUNDATECF" AS "RUNDATECF",
                                                                                            "RUNIDCF" AS "RUNIDCF"
                                                                                        FROM
                                                                                            (
                                                                                                SELECT
                                                                                                    *
                                                                                                FROM
                                                                                                    (
                                                                                                        (
                                                                                                            SELECT
                                                                                                                "AS_OF_DATE" AS "AS_OF_DATE",
                                                                                                                "SEGMENT_ID" AS "SEGMENT_ID",
                                                                                                                "PROPERTY_ID" AS "PROPERTY_ID",
                                                                                                                "SOURCE_SYSTEM_PORTFOLIO" AS "SOURCE_SYSTEM_PORTFOLIO",
                                                                                                                "CASH_FLOW_SEQUENTIAL_YEAR" AS "CASH_FLOW_SEQUENTIAL_YEAR",
                                                                                                                "CASH_FLOW_TYPE" AS "CASH_FLOW_TYPE",
                                                                                                                "SCENARIO" AS "SCENARIO",
                                                                                                                "CASHFLOW_AMOUNT_ORIGINAL" AS "CASHFLOW_AMOUNT_ORIGINAL",
                                                                                                                "CASHFLOW_AMOUNT_FUNCTIONAL" AS "CASHFLOW_AMOUNT_FUNCTIONAL",
                                                                                                                "DISCOUNT_FACTOR_AMOUNT_ORIGINAL" AS "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
                                                                                                                "DISCOUNT_FACTOR_PCT" AS "DISCOUNT_FACTOR_PCT",
                                                                                                                "DISCOUNTED_AMOUNT_FUNCTIONAL" AS "DISCOUNTED_AMOUNT_FUNCTIONAL",
                                                                                                                "RUNDATE" AS "RUNDATE",
                                                                                                                "RUNID" AS "RUNID",
                                                                                                                "MAJOR_PRODUCT_CODE" AS "MAJOR_PRODUCT_CODE",
                                                                                                                "LICAT_ASSET_TEXT" AS "LICAT_ASSET_TEXT",
                                                                                                                "LICAT_CREDIT_RISK_SOL_FAC_PERC" AS "LICAT_CREDIT_RISK_SOL_FAC_PERC",
                                                                                                                "LICAT_MARKET_RISK_SOL_FAC_PERC" AS "LICAT_MARKET_RISK_SOL_FAC_PERC"
                                                                                                            FROM
                                                                                                                IDP_CASHFlow_dev.MRI.DISCOUNTED_CASHFLOWS
                                                                                                            WHERE
                                                                                                                ("RUNDATE" = 'zzz')
                                                                                                        ) AS SNOWPARK_LEFT
                                                                                                        INNER JOIN (
                                                                                                            SELECT
                                                                                                                "RECORD_TYPE" AS "RECORD_TYPE",
                                                                                                                "PARENT_ENTITY_ID" AS "PARENT_ENTITY_ID",
                                                                                                                "CHILD_ENTITY_ID" AS "CHILD_ENTITY_ID",
                                                                                                                "MAJOR_PRODUCT_CODE" AS "MAJOR_PRODUCT_CODECF",
                                                                                                                "PORTFOLIO_NAME" AS "PORTFOLIO_NAME",
                                                                                                                "ALLOCATION_PERCENT" AS "ALLOCATION_PERCENT",
                                                                                                                "FILENAME" AS "FILENAME",
                                                                                                                "RUNDATE" AS "RUNDATECF",
                                                                                                                "RUNID" AS "RUNIDCF"
                                                                                                            FROM
                                                                                                                SDP_MRI_dev.DBO.SEGMENT
                                                                                                            WHERE
                                                                                                                ("RUNDATE" = 'zzz')
                                                                                                        ) AS SNOWPARK_RIGHT ON ("SEGMENT_ID" = "CHILD_ENTITY_ID")
                                                                                                    )
                                                                                            )
                                                                                    ) AS SNOWPARK_LEFT
                                                                                    INNER JOIN (
                                                                                        SELECT
                                                                                            "ASOFDATE" AS "ASOFDATE",
                                                                                            "PROPERTY_ID" AS "PROPERTY_IDPR",
                                                                                            "DEAL_SYSTEM_ID" AS "DEAL_SYSTEM_ID",
                                                                                            "DEAL_NAME_TEXT" AS "DEAL_NAME_TEXT",
                                                                                            "COMPONENT_NAME_TEXT" AS "COMPONENT_NAME_TEXT",
                                                                                            "ASSET_MANAGER_CODE" AS "ASSET_MANAGER_CODE",
                                                                                            "ASSET_MANAGER_NAME" AS "ASSET_MANAGER_NAME",
                                                                                            "PROJECT_ID" AS "PROJECT_ID",
                                                                                            "PROJECT_NAME" AS "PROJECT_NAME",
                                                                                            "PROPERTY_ADDRESS_LINE_1_TEXT" AS "PROPERTY_ADDRESS_LINE_1_TEXT",
                                                                                            "PROPERTY_ADDRESS_LINE_2_TEXT" AS "PROPERTY_ADDRESS_LINE_2_TEXT",
                                                                                            "PROPERTY_ADDRESS_LINE_3_TEXT" AS "PROPERTY_ADDRESS_LINE_3_TEXT",
                                                                                            "PROPERTY_CITY_NAME" AS "PROPERTY_CITY_NAME",
                                                                                            "PROPERTY_STATE" AS "PROPERTY_STATE",
                                                                                            "PROPERTY_POSTAL_CODE" AS "PROPERTY_POSTAL_CODE",
                                                                                            "PROPERTY_COUNTRY_CODE" AS "PROPERTY_COUNTRY_CODE",
                                                                                            "PROPERTY_CURRENCY" AS "PROPERTY_CURRENCY",
                                                                                            "PROPERTY_USAGE_CODE" AS "PROPERTY_USAGE_CODE",
                                                                                            "PROPERTY_TYPE_CODE" AS "PROPERTY_TYPE_CODE",
                                                                                            "COMPONENT_STATUS_TEXT" AS "COMPONENT_STATUS_TEXT",
                                                                                            "CANADIAN_FEDERAL_TAX_CODE" AS "CANADIAN_FEDERAL_TAX_CODE",
                                                                                            "ORIGINAL_ISSUE_DATE" AS "ORIGINAL_ISSUE_DATE",
                                                                                            "SALE_DATE" AS "SALE_DATE",
                                                                                            "PURCHASE_COMMITMENT_EXPIRY_DATE" AS "PURCHASE_COMMITMENT_EXPIRY_DATE",
                                                                                            "PURCHASE_COMMITMENT_YIELD_PERCENT" AS "PURCHASE_COMMITMENT_YIELD_PERCENT",
                                                                                            "SALE_COMMITMENT_EXPIRY_DATE" AS "SALE_COMMITMENT_EXPIRY_DATE",
                                                                                            "SALE_COMMITMENT_YIELD_PERCENT" AS "SALE_COMMITMENT_YIELD_PERCENT",
                                                                                            "PHYSICAL_COMPLETION_DATE" AS "PHYSICAL_COMPLETION_DATE",
                                                                                            "SLF_OCCUPANCY_PERCENT" AS "SLF_OCCUPANCY_PERCENT",
                                                                                            "INCOME_PRODUCING_DATE" AS "INCOME_PRODUCING_DATE",
                                                                                            "JOINT_VENTURE_PARTNER_NAME" AS "JOINT_VENTURE_PARTNER_NAME",
                                                                                            "SLF_OWNERSHIP_PERCENT" AS "SLF_OWNERSHIP_PERCENT",
                                                                                            "ASSUMED_MORTGAGE_NUMBER" AS "ASSUMED_MORTGAGE_NUMBER",
                                                                                            "ASSUMED_MORTGAGE_NAME" AS "ASSUMED_MORTGAGE_NAME",
                                                                                            "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE_CODE" AS "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE_CODE",
                                                                                            "ASSUMED_MORTGAGE_INTEREST_RATE_PERCENT" AS "ASSUMED_MORTGAGE_INTEREST_RATE_PERCENT",
                                                                                            "ASSUMED_MORTGAGE_MATURITY_DATE" AS "ASSUMED_MORTGAGE_MATURITY_DATE",
                                                                                            "PROPERTY_MANAGER_ID" AS "PROPERTY_MANAGER_ID",
                                                                                            "PROPERTY_MANAGER_NAME" AS "PROPERTY_MANAGER_NAME",
                                                                                            "INVESTMENT_MANAGER_FULL_NAME" AS "INVESTMENT_MANAGER_FULL_NAME",
                                                                                            "ECONOMIC_EXPIRY_DATE" AS "ECONOMIC_EXPIRY_DATE",
                                                                                            "PROPERTY_APPRAISAL_DATE" AS "PROPERTY_APPRAISAL_DATE",
                                                                                            "REPORTING_REGION" AS "REPORTING_REGION",
                                                                                            "INTERNAL_EXTERNAL_APPRAISAL_METHOD" AS "INTERNAL_EXTERNAL_APPRAISAL_METHOD",
                                                                                            "IPD_FUND_TYPE_CD" AS "IPD_FUND_TYPE_CD",
                                                                                            "CMA_CD" AS "CMA_CD",
                                                                                            "IPD_PROVINCE_CD" AS "IPD_PROVINCE_CD",
                                                                                            "IPD_INVESTMENT_TYPE_CD" AS "IPD_INVESTMENT_TYPE_CD",
                                                                                            "IPD_BUILDINGS_CNT" AS "IPD_BUILDINGS_CNT",
                                                                                            "OWNER_OCCUPIED_IND" AS "OWNER_OCCUPIED_IND",
                                                                                            "PREDOMINANT_CURRENT_USE_CD" AS "PREDOMINANT_CURRENT_USE_CD",
                                                                                            "PROPERTY_TYPE_RETAIL_CD" AS "PROPERTY_TYPE_RETAIL_CD",
                                                                                            "PROPERTY_TYPE_MIXED_CD" AS "PROPERTY_TYPE_MIXED_CD",
                                                                                            "RETAIL_ENCLOSED" AS "RETAIL_ENCLOSED",
                                                                                            "OFFICE_NODE" AS "OFFICE_NODE",
                                                                                            "INDUSTRY_NODE" AS "INDUSTRY_NODE",
                                                                                            "ACTUAL_APPRAISAL_CURR_QUARTER" AS "ACTUAL_APPRAISAL_CURR_QUARTER",
                                                                                            "APPRAISAL_METHOD_CD" AS "APPRAISAL_METHOD_CD",
                                                                                            "APPRAISAL_STABILIZED_INCOME_AMT" AS "APPRAISAL_STABILIZED_INCOME_AMT",
                                                                                            "APPRAISAL_TOTAL_AREA" AS "APPRAISAL_TOTAL_AREA",
                                                                                            "APPRAISAL_RENTABLE_AREA" AS "APPRAISAL_RENTABLE_AREA",
                                                                                            "APPRAISAL_TOTAL_UNITS_CNT" AS "APPRAISAL_TOTAL_UNITS_CNT",
                                                                                            "APPRAISAL_RENTABLE_UNITS_CNT" AS "APPRAISAL_RENTABLE_UNITS_CNT",
                                                                                            "DISCOUNT_RATE_CASH_FLOW_AMT" AS "DISCOUNT_RATE_CASH_FLOW_AMT",
                                                                                            "EXIT_YIELD_AMT" AS "EXIT_YIELD_AMT",
                                                                                            "CAPITALIZATION_RATE_AMT" AS "CAPITALIZATION_RATE_AMT",
                                                                                            "GROSS_PART_PURCHASE_EXP_PER_NATIVE_AMT" AS "GROSS_PART_PURCHASE_EXP_PER_NATIVE_AMT",
                                                                                            "IPD_ACQUISITION_ROUTE_CD" AS "IPD_ACQUISITION_ROUTE_CD",
                                                                                            "IPD_GROSS_PURCHASE_PRICE_AMT" AS "IPD_GROSS_PURCHASE_PRICE_AMT",
                                                                                            "IPD_NET_SALE_PRICE_AMT" AS "IPD_NET_SALE_PRICE_AMT",
                                                                                            "IPD_SALE_DT" AS "IPD_SALE_DT",
                                                                                            "PORTFOLIO_ALLOCATION_CD" AS "PORTFOLIO_ALLOCATION_CD",
                                                                                            "PROPERTY_TYPE_OFFICE_CD" AS "PROPERTY_TYPE_OFFICE_CD",
                                                                                            "PROPERTY_TYPE_RESIDENTIAL_CD" AS "PROPERTY_TYPE_RESIDENTIAL_CD",
                                                                                            "PROPERTY_TYPE_INDUSTRIAL_CD" AS "PROPERTY_TYPE_INDUSTRIAL_CD",
                                                                                            "PROPERTY_TYPE_OTHER_CD" AS "PROPERTY_TYPE_OTHER_CD",
                                                                                            "OFFICE_BUILDING_GRADE_CD" AS "OFFICE_BUILDING_GRADE_CD",
                                                                                            "PROPERTY_USAGE" AS "PROPERTY_USAGE",
                                                                                            "PROPERTY_SUB_TYPE" AS "PROPERTY_SUB_TYPE",
                                                                                            "PROPERTY_TYPE" AS "PROPERTY_TYPE",
                                                                                            "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE" AS "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE",
                                                                                            "ASIA_REAL_ESTATE_ID" AS "ASIA_REAL_ESTATE_ID",
                                                                                            "UK_PROPERTY_ID" AS "UK_PROPERTY_ID",
                                                                                            "UK_SECONDARY_PROPERTY_ID" AS "UK_SECONDARY_PROPERTY_ID",
                                                                                            "IFRS_LEDGER_ASSET_TYPE" AS "IFRS_LEDGER_ASSET_TYPE",
                                                                                            "SLC_ASSET_TYPE" AS "SLC_ASSET_TYPE",
                                                                                            "SLC_SECURITY_TYPE" AS "SLC_SECURITY_TYPE",
                                                                                            "VALUE_ADDED_TAX_IND" AS "VALUE_ADDED_TAX_IND",
                                                                                            "SLC_SEC_ID" AS "SLC_SEC_ID",
                                                                                            "STATUS" AS "STATUS",
                                                                                            "LAST_ACTIVE" AS "LAST_ACTIVE",
                                                                                            "RUNID" AS "RUNIDPR",
                                                                                            "RUNDATE" AS "RUNDATEPR"
                                                                                        FROM
                                                                                            (
                                                                                                SELECT
                                                                                                    "ASOFDATE",
                                                                                                    "PROPERTY_ID",
                                                                                                    "DEAL_SYSTEM_ID",
                                                                                                    "DEAL_NAME_TEXT",
                                                                                                    "COMPONENT_NAME_TEXT",
                                                                                                    "ASSET_MANAGER_CODE",
                                                                                                    "ASSET_MANAGER_NAME",
                                                                                                    "PROJECT_ID",
                                                                                                    "PROJECT_NAME",
                                                                                                    "PROPERTY_ADDRESS_LINE_1_TEXT",
                                                                                                    "PROPERTY_ADDRESS_LINE_2_TEXT",
                                                                                                    "PROPERTY_ADDRESS_LINE_3_TEXT",
                                                                                                    "PROPERTY_CITY_NAME",
                                                                                                    "PROPERTY_STATE",
                                                                                                    "PROPERTY_POSTAL_CODE",
                                                                                                    "PROPERTY_COUNTRY_CODE",
                                                                                                    "PROPERTY_CURRENCY",
                                                                                                    "PROPERTY_USAGE_CODE",
                                                                                                    "PROPERTY_TYPE_CODE",
                                                                                                    "COMPONENT_STATUS_TEXT",
                                                                                                    "CANADIAN_FEDERAL_TAX_CODE",
                                                                                                    "ORIGINAL_ISSUE_DATE",
                                                                                                    "SALE_DATE",
                                                                                                    "PURCHASE_COMMITMENT_EXPIRY_DATE",
                                                                                                    "PURCHASE_COMMITMENT_YIELD_PERCENT",
                                                                                                    "SALE_COMMITMENT_EXPIRY_DATE",
                                                                                                    "SALE_COMMITMENT_YIELD_PERCENT",
                                                                                                    "PHYSICAL_COMPLETION_DATE",
                                                                                                    "SLF_OCCUPANCY_PERCENT",
                                                                                                    "INCOME_PRODUCING_DATE",
                                                                                                    "JOINT_VENTURE_PARTNER_NAME",
                                                                                                    "SLF_OWNERSHIP_PERCENT",
                                                                                                    "ASSUMED_MORTGAGE_NUMBER",
                                                                                                    "ASSUMED_MORTGAGE_NAME",
                                                                                                    "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE_CODE",
                                                                                                    "ASSUMED_MORTGAGE_INTEREST_RATE_PERCENT",
                                                                                                    "ASSUMED_MORTGAGE_MATURITY_DATE",
                                                                                                    "PROPERTY_MANAGER_ID",
                                                                                                    "PROPERTY_MANAGER_NAME",
                                                                                                    "INVESTMENT_MANAGER_FULL_NAME",
                                                                                                    "ECONOMIC_EXPIRY_DATE",
                                                                                                    "PROPERTY_APPRAISAL_DATE",
                                                                                                    "REPORTING_REGION",
                                                                                                    "INTERNAL_EXTERNAL_APPRAISAL_METHOD",
                                                                                                    "IPD_FUND_TYPE_CD",
                                                                                                    "CMA_CD",
                                                                                                    "IPD_PROVINCE_CD",
                                                                                                    "IPD_INVESTMENT_TYPE_CD",
                                                                                                    "IPD_BUILDINGS_CNT",
                                                                                                    "OWNER_OCCUPIED_IND",
                                                                                                    "PREDOMINANT_CURRENT_USE_CD",
                                                                                                    "PROPERTY_TYPE_RETAIL_CD",
                                                                                                    "PROPERTY_TYPE_MIXED_CD",
                                                                                                    "RETAIL_ENCLOSED",
                                                                                                    "OFFICE_NODE",
                                                                                                    "INDUSTRY_NODE",
                                                                                                    "ACTUAL_APPRAISAL_CURR_QUARTER",
                                                                                                    "APPRAISAL_METHOD_CD",
                                                                                                    "APPRAISAL_STABILIZED_INCOME_AMT",
                                                                                                    "APPRAISAL_TOTAL_AREA",
                                                                                                    "APPRAISAL_RENTABLE_AREA",
                                                                                                    "APPRAISAL_TOTAL_UNITS_CNT",
                                                                                                    "APPRAISAL_RENTABLE_UNITS_CNT",
                                                                                                    "DISCOUNT_RATE_CASH_FLOW_AMT",
                                                                                                    "EXIT_YIELD_AMT",
                                                                                                    "CAPITALIZATION_RATE_AMT",
                                                                                                    "GROSS_PART_PURCHASE_EXP_PER_NATIVE_AMT",
                                                                                                    "IPD_ACQUISITION_ROUTE_CD",
                                                                                                    "IPD_GROSS_PURCHASE_PRICE_AMT",
                                                                                                    "IPD_NET_SALE_PRICE_AMT",
                                                                                                    "IPD_SALE_DT",
                                                                                                    "PORTFOLIO_ALLOCATION_CD",
                                                                                                    "PROPERTY_TYPE_OFFICE_CD",
                                                                                                    "PROPERTY_TYPE_RESIDENTIAL_CD",
                                                                                                    "PROPERTY_TYPE_INDUSTRIAL_CD",
                                                                                                    "PROPERTY_TYPE_OTHER_CD",
                                                                                                    "OFFICE_BUILDING_GRADE_CD",
                                                                                                    "PROPERTY_USAGE",
                                                                                                    "PROPERTY_SUB_TYPE",
                                                                                                    "PROPERTY_TYPE",
                                                                                                    "ASSUMED_MORTGAGE_INTEREST_RATE_TYPE",
                                                                                                    "ASIA_REAL_ESTATE_ID",
                                                                                                    "UK_PROPERTY_ID",
                                                                                                    "UK_SECONDARY_PROPERTY_ID",
                                                                                                    "IFRS_LEDGER_ASSET_TYPE",
                                                                                                    "SLC_ASSET_TYPE",
                                                                                                    "SLC_SECURITY_TYPE",
                                                                                                    "VALUE_ADDED_TAX_IND",
                                                                                                    "SLC_SEC_ID",
                                                                                                    "STATUS",
                                                                                                    "LAST_ACTIVE",
                                                                                                    "RUNID",
                                                                                                    CAST ("RUNDATE" AS DATE) AS "RUNDATE"
                                                                                                FROM
                                                                                                    IDP_SMF_dev.MRI.PROPERTY
                                                                                            )
                                                                                        WHERE
                                                                                            ("RUNDATE" = 'zzz')
                                                                                    ) AS SNOWPARK_RIGHT ON ("PROPERTY_IDPR" = "PARENT_ENTITY_ID")
                                                                                )
                                                                        )
                                                                ) AS SNOWPARK_LEFT
                                                                LEFT OUTER JOIN (
                                                                    SELECT
                                                                        "INV_DEAL_COMPONENT_ID" AS "INV_DEAL_COMPONENT_ID",
                                                                        "DEAL_SYSTEM_ID" AS "r_0001_DEAL_SYSTEM_ID",
                                                                        "IFRS_STATEMENT_VALUE_AMT_ORIG" AS "IFRS_STATEMENT_VALUE_AMT_ORIG"
                                                                    FROM
                                                                        (
                                                                            SELECT
                                                                                "INV_DEAL_COMPONENT_ID",
                                                                                "DEAL_SYSTEM_ID",
                                                                                sum(
                                                                                    CASE
                                                                                        WHEN (
                                                                                            (
                                                                                                "BASIS" IN ('zzz', 'zzz', 'zzz')
                                                                                                AND (
                                                                                                    (
                                                                                                        (
                                                                                                            (
                                                                                                                (
                                                                                                                    (
                                                                                                                        (
                                                                                                                            ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                            AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                        )
                                                                                                                        OR (
                                                                                                                            ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                            AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                        )
                                                                                                                    )
                                                                                                                    OR (
                                                                                                                        ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                        AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                    )
                                                                                                                )
                                                                                                                OR (
                                                                                                                    ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                    AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                )
                                                                                                            )
                                                                                                            OR (
                                                                                                                ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                            )
                                                                                                        )
                                                                                                        OR (
                                                                                                            ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                            AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                        )
                                                                                                    )
                                                                                                    OR (
                                                                                                        ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                        AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                    )
                                                                                                )
                                                                                            )
                                                                                            OR (
                                                                                                "BASIS" IN ('zzz', 'zzz')
                                                                                                AND (
                                                                                                    (
                                                                                                        (
                                                                                                            (
                                                                                                                (
                                                                                                                    (
                                                                                                                        (
                                                                                                                            ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                            AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                        )
                                                                                                                        OR (
                                                                                                                            ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                            AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                        )
                                                                                                                    )
                                                                                                                    OR (
                                                                                                                        ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                        AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                    )
                                                                                                                )
                                                                                                                OR (
                                                                                                                    ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                    AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                                )
                                                                                                            )
                                                                                                            OR (
                                                                                                                ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                                AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                            )
                                                                                                        )
                                                                                                        OR (
                                                                                                            ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                            AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                        )
                                                                                                    )
                                                                                                    OR (
                                                                                                        ("ADMIN_GL_ACCOUNT_CODE" >= 'zzz')
                                                                                                        AND ("ADMIN_GL_ACCOUNT_CODE" <= 'zzz')
                                                                                                    )
                                                                                                )
                                                                                            )
                                                                                        ) THEN "PERIOD_ENDING_BALANCE"
                                                                                        ELSE 'zzz' :: INT
                                                                                    END
                                                                                ) AS "IFRS_STATEMENT_VALUE_AMT_ORIG"
                                                                            FROM
                                                                                (
                                                                                    SELECT
                                                                                        *
                                                                                    FROM
                                                                                        SDP_MRI_dev.DBO.ACCOUNT_BALANCE
                                                                                )
                                                                            GROUP BY
                                                                                "INV_DEAL_COMPONENT_ID",
                                                                                "DEAL_SYSTEM_ID"
                                                                        )
                                                                ) AS SNOWPARK_RIGHT ON (
                                                                    ("CHILD_ENTITY_ID" = "INV_DEAL_COMPONENT_ID")
                                                                    AND (
                                                                        "l_0000_DEAL_SYSTEM_ID" = "r_0001_DEAL_SYSTEM_ID"
                                                                    )
                                                                )
                                                            )
                                                    )
                                            )
                                    )
                                GROUP BY
                                    "PROPERTY_ID",
                                    "SCENARIO",
                                    "LICAT_ASSET_TEXT",
                                    "IFRS_STATEMENT_VALUE_AMT_ORIG",
                                    "MARKET_RISK_SOL_FAC_PERC",
                                    "CREDIT_RISK_SOL_FAC_PERC",
                                    "CASHFLOW_AMOUNT_ORIGINAL",
                                    "RUNID",
                                    "PARENT_ENTITY_ID",
                                    "CHILD_ENTITY_ID",
                                    "RUNDATE",
                                    "AS_OF_DATE",
                                    "DISCOUNT_FACTOR_AMOUNT_ORIGINAL",
                                    "SOURCE_SYSTEM_PORTFOLIO"
                            )
                    )
            )
    )"""
    assert_table_lineage_equal(
        sql,
        {
            "sdp_mri_dev.dbo.segment",
            "sdp_mri_dev.dbo.account_balance",
            "idp_smf_dev.mri.property",
            "idp_cashflow_dev.mri.discounted_cashflows",
        },  # source_tables
        {"idp_cashflow_dev.mri.discounted_cashflows_licat"},  # target_tables
        dialect=dialect,
        test_sqlparse=False,
    )

    common_expected_column_lineage = [
        (
            TestColumnQualifierTuple(
                "licat_asset_text", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "market_risk_residual_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "cash_flow_type", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "market_risk_solvency_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple("basis", "sdp_mri_dev.dbo.account_balance"),
            TestColumnQualifierTuple(
                "market_risk_solvency_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "period_ending_balance", "sdp_mri_dev.dbo.account_balance"
            ),
            TestColumnQualifierTuple(
                "market_risk_residual_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "as_of_date", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "as_of_date", "idp_cashflow_dev.mri.discounted_cashflows_licat"
            ),
        ),
        (
            TestColumnQualifierTuple(
                "*", "subquery_1614383322482569396", is_subquery=True
            ),
            TestColumnQualifierTuple(
                "credit_risk_solvency_unadjusted_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple("child_entity_id", "sdp_mri_dev.dbo.segment"),
            TestColumnQualifierTuple(
                "child_entity_id", "idp_cashflow_dev.mri.discounted_cashflows_licat"
            ),
        ),
        (
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "credit_risk_disc_cf_pv_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "admin_gl_account_code", "sdp_mri_dev.dbo.account_balance"
            ),
            TestColumnQualifierTuple(
                "credit_risk_solvency_unadjusted_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "cash_flow_type", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "disc_contractual_cf_pv_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "source_system_portfolio",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "source_system_portfolio",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "licat_asset_text", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "market_risk_solvency_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "cashflow_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "cashflow_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "credit_risk_solvency_unadjusted_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "admin_gl_account_code", "sdp_mri_dev.dbo.account_balance"
            ),
            TestColumnQualifierTuple(
                "market_risk_residual_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "*", "subquery_-8098524472634041444", is_subquery=True
            ),
            TestColumnQualifierTuple(
                "*", "idp_cashflow_dev.mri.discounted_cashflows_licat"
            ),
        ),
        (
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "disc_recoverable_cf_pv_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple("parent_entity_id", "sdp_mri_dev.dbo.segment"),
            TestColumnQualifierTuple(
                "parent_entity_id",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "period_ending_balance", "sdp_mri_dev.dbo.account_balance"
            ),
            TestColumnQualifierTuple(
                "market_risk_solvency_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "market_risk_residual_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "cash_flow_type", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "credit_risk_disc_cf_pv_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "runid", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "runid", "idp_cashflow_dev.mri.discounted_cashflows_licat"
            ),
        ),
        (
            TestColumnQualifierTuple(
                "cash_flow_type", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "credit_risk_solvency_unadjusted_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "licat_asset_text", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "licat_asset_text",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "*", "subquery_1614383322482569396", is_subquery=True
            ),
            TestColumnQualifierTuple(
                "market_risk_solvency_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "admin_gl_account_code", "sdp_mri_dev.dbo.account_balance"
            ),
            TestColumnQualifierTuple(
                "market_risk_solvency_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "cash_flow_type", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "disc_recoverable_cf_pv_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple("basis", "sdp_mri_dev.dbo.account_balance"),
            TestColumnQualifierTuple(
                "credit_risk_solvency_unadjusted_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "cash_flow_type", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "market_risk_residual_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "market_risk_solvency_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "rundate", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "rundate", "idp_cashflow_dev.mri.discounted_cashflows_licat"
            ),
        ),
        (
            TestColumnQualifierTuple("basis", "sdp_mri_dev.dbo.account_balance"),
            TestColumnQualifierTuple(
                "market_risk_residual_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "licat_asset_text", "idp_cashflow_dev.mri.discounted_cashflows"
            ),
            TestColumnQualifierTuple(
                "credit_risk_solvency_unadjusted_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "period_ending_balance", "sdp_mri_dev.dbo.account_balance"
            ),
            TestColumnQualifierTuple(
                "credit_risk_solvency_unadjusted_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
        (
            TestColumnQualifierTuple(
                "discount_factor_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows",
            ),
            TestColumnQualifierTuple(
                "disc_contractual_cf_pv_amount_original",
                "idp_cashflow_dev.mri.discounted_cashflows_licat",
            ),
        ),
    ]

    # skip column lineage for this query since subquery aliases are non-deterministic
    # across diff parsers
    assert_column_lineage_equal(
        sql,
        [
            *common_expected_column_lineage,
            (
                TestColumnQualifierTuple(
                    "*", "subquery_1614383322482569396", is_subquery=True
                ),
                TestColumnQualifierTuple(
                    "credit_risk_solvency_unadjusted_amount_original",
                    "idp_cashflow_dev.mri.discounted_cashflows_licat",
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "*", "subquery_-8098524472634041444", is_subquery=True
                ),
                TestColumnQualifierTuple(
                    "*", "idp_cashflow_dev.mri.discounted_cashflows_licat"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "*", "subquery_1614383322482569396", is_subquery=True
                ),
                TestColumnQualifierTuple(
                    "market_risk_solvency_amount_original",
                    "idp_cashflow_dev.mri.discounted_cashflows_licat",
                ),
            ),
        ],
        dialect=dialect,
        # SqlGlot throws error in wildcard expansion for subqueries
        # TODO: Fix SqlGlot to handle wildcard expansion in subqueries correctly
        test_sqlglot=False,
        # skipping sqlfluff at this moment due to non-deterministic hashing in subquery alias
        test_sqlfluff=False,
        test_sqlparse=False,
    )
