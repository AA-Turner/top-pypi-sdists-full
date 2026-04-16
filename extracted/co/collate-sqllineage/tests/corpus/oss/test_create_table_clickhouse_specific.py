"""Tests for ClickHouse specific create table queries."""

import pytest

from tests.helpers import (
    TestColumnQualifierTuple,
    assert_column_lineage_equal,
    assert_table_lineage_equal,
)


@pytest.mark.parametrize("dialect", ["clickhouse"])
def test_create_table_query_union_all_clickhouse_dbt_21953(dialect: str):
    """
    Test lineage for a create table with union all query with multiple sources and subqueries,
    based on a real-world example from dbt ClickHouse adapter issue #21953.

    Reference: https://github.com/open-metadata/OpenMetadata/issues/21953
    """

    sql = """
create table "default"."dws"."dim_vendor" as













with final_data as (

  select
    date_id as date_id,
    vendor_id as vendor_id,
    vendor_code as vendor_code,
    vendor_name as vendor_name,
    vendor_name_cn as vendor_name_cn,
    vendor_short_name as vendor_short_name,
    active_flag as active_flag,
    avl_status as avl_status,
    approval_status as approval_status,
    vendor_created_time as vendor_created_time,
    date_last_modified as date_last_modified,
    default_ship_terms as default_ship_terms,
    vendor_lead_time as vendor_lead_time,
    production_lead_time as production_lead_time,
    delivery_lead_time as delivery_lead_time,
    vendor_type as vendor_type,
    vendor_commodity as vendor_commodity,
    legacy_entity as legacy_entity,
    incoterms as incoterms,
    best_terms as best_terms,
    vendor_contact_1 as vendor_contact_1,
    vendor_contact_2 as vendor_contact_2,
    vendor_tel_1 as vendor_tel_1,
    vendor_tel_2 as vendor_tel_2,
    vendor_email as vendor_email,
    sourcing_office as sourcing_office,
    city as city,
    state as state,
    state_code as state_code,
    country as country,
    country_code as country_code,
    vendor_address as vendor_address,
    vendor_address_cn as vendor_address_cn,
    manufacture_address as manufacture_address,
    delivery_address as delivery_address,
    sourcing_buyer as sourcing_buyer,
    purchasing_buyer as purchasing_buyer,
    currency as currency,
    deposite_rate as deposite_rate,
    compliance as compliance,
    bank_account_cny as bank_account_cny,
    bank_account_name_cny as bank_account_name_cny,
    bank_name_cny as bank_name_cny,
    bank_country as bank_country,
    bank_routing_no as bank_routing_no,
    bank_address_cny as bank_address_cny,
    bank_account_usd as bank_account_usd,
    bank_account_name_usd as bank_account_name_usd,
    bank_name_usd as bank_name_usd,
    bank_address_usd as bank_address_usd,
    swift_code as swift_code,
    ap_account_code as ap_account_code,
    settlement_method_no as settlement_method_no,
    invoice_type as invoice_type,
    tax_rate as tax_rate,
    tax_type as tax_type,
    qc_address as qc_address,
    qc_type as qc_type,
    qc_area as qc_area,
    soc_letter_of_chemicals as soc_letter_of_chemicals,
    ab1200_certification as ab1200_certification,
    chcc_certification as chcc_certification,
    pa_no as pa_no,
    carb_certification_no as carb_certification_no,
    carb_certification_expiration as carb_certification_expiration,
    fda_supplier_registration_required as fda_supplier_registration_required,
    fda_registration_type as fda_registration_type,
    fda_supplier_reg_number as fda_supplier_reg_number,
    fda_supplier_reg_expiration_date as fda_supplier_reg_expiration_date,
    food_signed_supplier_approval_form as food_signed_supplier_approval_form,
    food_claim_verification_documents as food_claim_verification_documents,
    food_bioengineered_status_document as food_bioengineered_status_document,
    food_food_safety_plan_haccp as food_food_safety_plan_haccp,
    food_food_safety_certification as food_food_safety_certification,
    food_allergen_matrix as food_allergen_matrix,
    food_signed_prop_65_certification as food_signed_prop_65_certification,
    food_prop_65_statement as food_prop_65_statement,
    food_fsma_compliance_statement as food_fsma_compliance_statement,
    food_vendor_setup_form as food_vendor_setup_form,
    food_supplier_expectation_manual as food_supplier_expectation_manual,
    food_insurance_letter as food_insurance_letter,
    food_letter_of_continuing_guarantee as food_letter_of_continuing_guarantee,
    food_current_3rd_party_audit as food_current_3rd_party_audit,
    vendor_folder_link as vendor_folder_link,
    last_po_date as last_po_date,
    vendor_classification as vendor_classification,
    partial_delivery as partial_delivery,
    remark as remark,
    data_source as data_source,
    data_source_key as data_source_key,
    today() as uds_load_date,
    now() as uds_load_time,
    1 as uds_ch_sign
  from `dbt`.`int_dim_vendor__fb_vendor`
  union all

  select
    date_id as date_id,
    vendor_id as vendor_id,
    null as vendor_code,
    vendor_name as vendor_name,
    vendor_name_cn as vendor_name_cn,
    null as vendor_short_name,
    active_flag as active_flag,
    null as avl_status,
    null as approval_status,
    vendor_created_time as vendor_created_time,
    date_last_modified as date_last_modified,
    default_ship_terms as default_ship_terms,
    vendor_lead_time as vendor_lead_time,
    null as production_lead_time,
    null as delivery_lead_time,
    vendor_type as vendor_type,
    null as vendor_commodity,
    null as legacy_entity,
    incoterms as incoterms,
    best_terms as best_terms,
    null as vendor_contact_1,
    null as vendor_contact_2,
    null as vendor_tel_1,
    null as vendor_tel_2,
    null as vendor_email,
    sourcing_office as sourcing_office,
    city as city,
    state as state,
    state_code as state_code,
    country as country,
    country_code as country_code,
    vendor_address as vendor_address,
    vendor_address_cn as vendor_address_cn,
    null as manufacture_address,
    null as delivery_address,
    null as sourcing_buyer,
    null as purchasing_buyer,
    null as currency,
    null as deposite_rate,
    null as compliance,
    null as bank_account_cny,
    null as bank_account_name_cny,
    null as bank_name_cny,
    null as bank_country,
    null as bank_routing_no,
    null as bank_address_cny,
    null as bank_account_usd,
    null as bank_account_name_usd,
    null as bank_name_usd,
    null as bank_address_usd,
    null as swift_code,
    null as ap_account_code,
    null as settlement_method_no,
    null as invoice_type,
    null as tax_rate,
    null as tax_type,
    null as qc_address,
    null as qc_type,
    null as qc_area,
    null as soc_letter_of_chemicals,
    null as ab1200_certification,
    null as chcc_certification,
    null as pa_no,
    null as carb_certification_no,
    null as carb_certification_expiration,
    null as fda_supplier_registration_required,
    null as fda_registration_type,
    null as fda_supplier_reg_number,
    null as fda_supplier_reg_expiration_date,
    null as food_signed_supplier_approval_form,
    null as food_claim_verification_documents,
    null as food_bioengineered_status_document,
    null as food_food_safety_plan_haccp,
    null as food_food_safety_certification,
    null as food_allergen_matrix,
    null as food_signed_prop_65_certification,
    null as food_prop_65_statement,
    null as food_fsma_compliance_statement,
    null as food_vendor_setup_form,
    null as food_supplier_expectation_manual,
    null as food_insurance_letter,
    null as food_letter_of_continuing_guarantee,
    null as food_current_3rd_party_audit,
    null as vendor_folder_link,
    null as last_po_date,
    null as vendor_classification,
    null as partial_delivery,
    null as remark,
    data_source as data_source,
    data_source_key as data_source_key,
    today() as uds_load_date,
    now() as uds_load_time,
    1 as uds_ch_sign
  from `dbt`.`int_dim_vendor__oms_vendor`
  where vendor_name not in
  (
    select distinct vendor_name from `dbt`.`int_dim_vendor__fb_vendor`
  )
  union all

  select
    date_id as date_id,
    vendor_id as vendor_id,
    null as vendor_code,
    vendor_name as vendor_name,
    null as vendor_name_cn,
    null as vendor_short_name,
    active_flag as active_flag,
    null as avl_status,
    null as approval_status,
    null as vendor_created_time,
    null as date_last_modified,
    null as default_ship_terms,
    null as vendor_lead_time,
    null as production_lead_time,
    null as delivery_lead_time,
    null as vendor_type,
    null as vendor_commodity,
    null as legacy_entity,
    null as incoterms,
    null as best_terms,
    null as vendor_contact_1,
    null as vendor_contact_2,
    null as vendor_tel_1,
    null as vendor_tel_2,
    null as vendor_email,
    null as sourcing_office,
    null as city,
    null as state,
    null as state_code,
    null as country,
    null as country_code,
    null as vendor_address,
    null as vendor_address_cn,
    null as manufacture_address,
    null as delivery_address,
    null as sourcing_buyer,
    null as purchasing_buyer,
    null as currency,
    null as deposite_rate,
    null as compliance,
    null as bank_account_cny,
    null as bank_account_name_cny,
    null as bank_name_cny,
    null as bank_country,
    null as bank_routing_no,
    null as bank_address_cny,
    null as bank_account_usd,
    null as bank_account_name_usd,
    null as bank_name_usd,
    null as bank_address_usd,
    null as swift_code,
    null as ap_account_code,
    null as settlement_method_no,
    null as invoice_type,
    null as tax_rate,
    null as tax_type,
    null as qc_address,
    null as qc_type,
    null as qc_area,
    null as soc_letter_of_chemicals,
    null as ab1200_certification,
    null as chcc_certification,
    null as pa_no,
    null as carb_certification_no,
    null as carb_certification_expiration,
    null as fda_supplier_registration_required,
    null as fda_registration_type,
    null as fda_supplier_reg_number,
    null as fda_supplier_reg_expiration_date,
    null as food_signed_supplier_approval_form,
    null as food_claim_verification_documents,
    null as food_bioengineered_status_document,
    null as food_food_safety_plan_haccp,
    null as food_food_safety_certification,
    null as food_allergen_matrix,
    null as food_signed_prop_65_certification,
    null as food_prop_65_statement,
    null as food_fsma_compliance_statement,
    null as food_vendor_setup_form,
    null as food_supplier_expectation_manual,
    null as food_insurance_letter,
    null as food_letter_of_continuing_guarantee,
    null as food_current_3rd_party_audit,
    null as vendor_folder_link,
    null as last_po_date,
    null as vendor_classification,
    null as partial_delivery,
    null as remark,
    data_source as data_source,
    data_source_key as data_source_key,
    today() as uds_load_date,
    now() as uds_load_time,
    1 as uds_ch_sign
  from `dbt`.`int_dim_vendor__qb_vendor`
  where vendor_name not in
  (
    select distinct vendor_name from `dbt`.`int_dim_vendor__fb_vendor`
    union all
    select distinct vendor_name from `dbt`.`int_dim_vendor__oms_vendor`
  )
  union all

  select
    date_id as date_id,
    vendor_id as vendor_id,
    null as vendor_code,
    vendor_name as vendor_name,
    null as vendor_name_cn,
    null as vendor_short_name,
    active_flag as active_flag,
    null as avl_status,
    null as approval_status,
    vendor_created_time as vendor_created_time,
    date_last_modified as date_last_modified,
    null as default_ship_terms,
    vendor_lead_time as vendor_lead_time,
    null as production_lead_time,
    null as delivery_lead_time,
    vendor_type as vendor_type,
    null as vendor_commodity,
    null as legacy_entity,
    null as incoterms,
    best_terms as best_terms,
    null as vendor_contact_1,
    null as vendor_contact_2,
    null as vendor_tel_1,
    null as vendor_tel_2,
    null as vendor_email,
    null as sourcing_office,
    null as city,
    null as state,
    null as state_code,
    null as country,
    null as country_code,
    vendor_address as vendor_address,
    null as vendor_address_cn,
    null as manufacture_address,
    null as delivery_address,
    null as sourcing_buyer,
    null as purchasing_buyer,
    null as currency,
    null as deposite_rate,
    null as compliance,
    null as bank_account_cny,
    null as bank_account_name_cny,
    null as bank_name_cny,
    null as bank_country,
    null as bank_routing_no,
    null as bank_address_cny,
    null as bank_account_usd,
    null as bank_account_name_usd,
    null as bank_name_usd,
    null as bank_address_usd,
    null as swift_code,
    null as ap_account_code,
    null as settlement_method_no,
    null as invoice_type,
    null as tax_rate,
    null as tax_type,
    null as qc_address,
    null as qc_type,
    null as qc_area,
    null as soc_letter_of_chemicals,
    null as ab1200_certification,
    null as chcc_certification,
    null as pa_no,
    null as carb_certification_no,
    null as carb_certification_expiration,
    null as fda_supplier_registration_required,
    null as fda_registration_type,
    null as fda_supplier_reg_number,
    null as fda_supplier_reg_expiration_date,
    null as food_signed_supplier_approval_form,
    null as food_claim_verification_documents,
    null as food_bioengineered_status_document,
    null as food_food_safety_plan_haccp,
    null as food_food_safety_certification,
    null as food_allergen_matrix,
    null as food_signed_prop_65_certification,
    null as food_prop_65_statement,
    null as food_fsma_compliance_statement,
    null as food_vendor_setup_form,
    null as food_supplier_expectation_manual,
    null as food_insurance_letter,
    null as food_letter_of_continuing_guarantee,
    null as food_current_3rd_party_audit,
    null as vendor_folder_link,
    null as last_po_date,
    null as vendor_classification,
    null as partial_delivery,
    null as remark,
    data_source as data_source,
    data_source_key as data_source_key,
    today() as uds_load_date,
    now() as uds_load_time,
    1 as uds_ch_sign
  from `dbt`.`int_dim_vendor__ns_vendor`
  where vendor_name not in
  (
    select distinct vendor_name from `dbt`.`int_dim_vendor__fb_vendor`
    union all
    select distinct vendor_name from `dbt`.`int_dim_vendor__oms_vendor`
    union all
    select distinct vendor_name from `dbt`.`int_dim_vendor__qb_vendor`
  )
  union all

  select
    date_id as date_id,
    vendor_id as vendor_id,
    null as vendor_code,
    vendor_name as vendor_name,
    null as vendor_name_cn,
    null as vendor_short_name,
    active_flag as active_flag,
    null as avl_status,
    null as approval_status,
    vendor_created_time as vendor_created_time,
    date_last_modified as date_last_modified,
    null as default_ship_terms,
    vendor_lead_time as vendor_lead_time,
    null as production_lead_time,
    null as delivery_lead_time,
    vendor_type as vendor_type,
    null as vendor_commodity,
    null as legacy_entity,
    null as incoterms,
    best_terms as best_terms,
    null as vendor_contact_1,
    null as vendor_contact_2,
    null as vendor_tel_1,
    null as vendor_tel_2,
    null as vendor_email,
    null as sourcing_office,
    null as city,
    null as state,
    null as state_code,
    null as country,
    country_code as country_code,
    vendor_address as vendor_address,
    null as vendor_address_cn,
    null as manufacture_address,
    null as delivery_address,
    null as sourcing_buyer,
    null as purchasing_buyer,
    null as currency,
    null as deposite_rate,
    null as compliance,
    null as bank_account_cny,
    null as bank_account_name_cny,
    null as bank_name_cny,
    null as bank_country,
    null as bank_routing_no,
    null as bank_address_cny,
    null as bank_account_usd,
    null as bank_account_name_usd,
    null as bank_name_usd,
    null as bank_address_usd,
    null as swift_code,
    null as ap_account_code,
    null as settlement_method_no,
    null as invoice_type,
    null as tax_rate,
    null as tax_type,
    null as qc_address,
    null as qc_type,
    null as qc_area,
    null as soc_letter_of_chemicals,
    null as ab1200_certification,
    null as chcc_certification,
    null as pa_no,
    null as carb_certification_no,
    null as carb_certification_expiration,
    null as fda_supplier_registration_required,
    null as fda_registration_type,
    null as fda_supplier_reg_number,
    null as fda_supplier_reg_expiration_date,
    null as food_signed_supplier_approval_form,
    null as food_claim_verification_documents,
    null as food_bioengineered_status_document,
    null as food_food_safety_plan_haccp,
    null as food_food_safety_certification,
    null as food_allergen_matrix,
    null as food_signed_prop_65_certification,
    null as food_prop_65_statement,
    null as food_fsma_compliance_statement,
    null as food_vendor_setup_form,
    null as food_supplier_expectation_manual,
    null as food_insurance_letter,
    null as food_letter_of_continuing_guarantee,
    null as food_current_3rd_party_audit,
    null as vendor_folder_link,
    null as last_po_date,
    null as vendor_classification,
    null as partial_delivery,
    null as remark,
    data_source as data_source,
    data_source_key as data_source_key,
    today() as uds_load_date,
    now() as uds_load_time,
    1 as uds_ch_sign
  from `dbt`.`int_dim_vendor__df_vendor`
  where vendor_name not in
  (
    select distinct vendor_name from `dbt`.`int_dim_vendor__fb_vendor`
    union all
    select distinct vendor_name from `dbt`.`int_dim_vendor__oms_vendor`
    union all
    select distinct vendor_name from `dbt`.`int_dim_vendor__qb_vendor`
    union all
    select distinct vendor_name from `dbt`.`int_dim_vendor__ns_vendor`
  )
)
select * from final_data
where vendor_id is not null
    """

    assert_table_lineage_equal(
        sql,
        {
            "dbt.int_dim_vendor__fb_vendor",
            "dbt.int_dim_vendor__oms_vendor",
            "dbt.int_dim_vendor__qb_vendor",
            "dbt.int_dim_vendor__ns_vendor",
            "dbt.int_dim_vendor__df_vendor",
        },  # source_tables
        {"default.dws.dim_vendor"},  # target_tables
        dialect=dialect,
        # SqlFluff doesn't track NOT IN subqueries as intermediate graph nodes; skip graph check.
        skip_graph_check=True,
    )

    # skip_graph_check=True: SqlFluff omits NOT IN subquery nodes from graph; SqlParse includes them.
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple(
                    "active_flag", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("active_flag", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("best_terms", "dbt.int_dim_vendor__df_vendor"),
                TestColumnQualifierTuple("best_terms", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "country_code", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("country_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("data_source", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source_key", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("data_source_key", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("date_id", "dbt.int_dim_vendor__df_vendor"),
                TestColumnQualifierTuple("date_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "date_last_modified", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple(
                    "date_last_modified", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_address", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("vendor_address", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_created_time", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple(
                    "vendor_created_time", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("vendor_id", "dbt.int_dim_vendor__df_vendor"),
                TestColumnQualifierTuple("vendor_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_lead_time", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("vendor_lead_time", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_name", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("vendor_name", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_type", "dbt.int_dim_vendor__df_vendor"
                ),
                TestColumnQualifierTuple("vendor_type", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "ab1200_certification", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "ab1200_certification", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "active_flag", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("active_flag", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "ap_account_code", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("ap_account_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "approval_status", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("approval_status", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("avl_status", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("avl_status", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_account_cny", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_account_cny", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_account_name_cny", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "bank_account_name_cny", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_account_name_usd", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "bank_account_name_usd", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_account_usd", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_account_usd", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_address_cny", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_address_cny", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_address_usd", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_address_usd", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_country", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_country", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_name_cny", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_name_cny", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_name_usd", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_name_usd", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "bank_routing_no", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("bank_routing_no", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("best_terms", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("best_terms", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "carb_certification_expiration", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "carb_certification_expiration", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "carb_certification_no", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "carb_certification_no", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "chcc_certification", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "chcc_certification", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("city", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("city", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("compliance", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("compliance", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("country", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("country", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "country_code", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("country_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("currency", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("currency", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("data_source", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source_key", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("data_source_key", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("date_id", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("date_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "date_last_modified", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "date_last_modified", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "default_ship_terms", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "default_ship_terms", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "delivery_address", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("delivery_address", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "delivery_lead_time", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "delivery_lead_time", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "deposite_rate", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("deposite_rate", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "fda_registration_type", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "fda_registration_type", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "fda_supplier_reg_expiration_date", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "fda_supplier_reg_expiration_date", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "fda_supplier_reg_number", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "fda_supplier_reg_number", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "fda_supplier_registration_required",
                    "dbt.int_dim_vendor__fb_vendor",
                ),
                TestColumnQualifierTuple(
                    "fda_supplier_registration_required", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_allergen_matrix", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_allergen_matrix", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_bioengineered_status_document",
                    "dbt.int_dim_vendor__fb_vendor",
                ),
                TestColumnQualifierTuple(
                    "food_bioengineered_status_document", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_claim_verification_documents", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_claim_verification_documents", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_current_3rd_party_audit", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_current_3rd_party_audit", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_food_safety_certification", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_food_safety_certification", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_food_safety_plan_haccp", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_food_safety_plan_haccp", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_fsma_compliance_statement", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_fsma_compliance_statement", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_insurance_letter", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_insurance_letter", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_letter_of_continuing_guarantee",
                    "dbt.int_dim_vendor__fb_vendor",
                ),
                TestColumnQualifierTuple(
                    "food_letter_of_continuing_guarantee", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_prop_65_statement", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_prop_65_statement", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_signed_prop_65_certification", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_signed_prop_65_certification", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_signed_supplier_approval_form",
                    "dbt.int_dim_vendor__fb_vendor",
                ),
                TestColumnQualifierTuple(
                    "food_signed_supplier_approval_form", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_supplier_expectation_manual", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_supplier_expectation_manual", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "food_vendor_setup_form", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "food_vendor_setup_form", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("incoterms", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("incoterms", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "invoice_type", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("invoice_type", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "last_po_date", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("last_po_date", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "legacy_entity", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("legacy_entity", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "manufacture_address", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "manufacture_address", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("pa_no", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("pa_no", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "partial_delivery", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("partial_delivery", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "production_lead_time", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "production_lead_time", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "purchasing_buyer", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("purchasing_buyer", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("qc_address", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("qc_address", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("qc_area", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("qc_area", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("qc_type", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("qc_type", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("remark", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("remark", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "settlement_method_no", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "settlement_method_no", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "soc_letter_of_chemicals", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "soc_letter_of_chemicals", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "sourcing_buyer", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("sourcing_buyer", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "sourcing_office", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("sourcing_office", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("state", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("state", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("state_code", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("state_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("swift_code", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("swift_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("tax_rate", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("tax_rate", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("tax_type", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("tax_type", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_address", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_address", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_address_cn", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_address_cn", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_classification", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "vendor_classification", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_code", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_commodity", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_commodity", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_contact_1", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_contact_1", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_contact_2", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_contact_2", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_created_time", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "vendor_created_time", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_email", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_email", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_folder_link", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple(
                    "vendor_folder_link", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("vendor_id", "dbt.int_dim_vendor__fb_vendor"),
                TestColumnQualifierTuple("vendor_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_lead_time", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_lead_time", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_name", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_name", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_name_cn", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_name_cn", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_short_name", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_short_name", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_tel_1", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_tel_1", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_tel_2", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_tel_2", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_type", "dbt.int_dim_vendor__fb_vendor"
                ),
                TestColumnQualifierTuple("vendor_type", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "active_flag", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple("active_flag", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("best_terms", "dbt.int_dim_vendor__ns_vendor"),
                TestColumnQualifierTuple("best_terms", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple("data_source", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source_key", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple("data_source_key", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("date_id", "dbt.int_dim_vendor__ns_vendor"),
                TestColumnQualifierTuple("date_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "date_last_modified", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple(
                    "date_last_modified", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_address", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple("vendor_address", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_created_time", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple(
                    "vendor_created_time", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("vendor_id", "dbt.int_dim_vendor__ns_vendor"),
                TestColumnQualifierTuple("vendor_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_lead_time", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple("vendor_lead_time", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_name", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple("vendor_name", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_type", "dbt.int_dim_vendor__ns_vendor"
                ),
                TestColumnQualifierTuple("vendor_type", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "active_flag", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("active_flag", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "best_terms", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("best_terms", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("city", "dbt.int_dim_vendor__oms_vendor"),
                TestColumnQualifierTuple("city", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("country", "dbt.int_dim_vendor__oms_vendor"),
                TestColumnQualifierTuple("country", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "country_code", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("country_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("data_source", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source_key", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("data_source_key", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("date_id", "dbt.int_dim_vendor__oms_vendor"),
                TestColumnQualifierTuple("date_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "date_last_modified", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple(
                    "date_last_modified", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple(
                    "default_ship_terms", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple(
                    "default_ship_terms", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("incoterms", "dbt.int_dim_vendor__oms_vendor"),
                TestColumnQualifierTuple("incoterms", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "sourcing_office", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("sourcing_office", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("state", "dbt.int_dim_vendor__oms_vendor"),
                TestColumnQualifierTuple("state", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "state_code", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("state_code", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_address", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("vendor_address", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_address_cn", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("vendor_address_cn", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_created_time", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple(
                    "vendor_created_time", "default.dws.dim_vendor"
                ),
            ),
            (
                TestColumnQualifierTuple("vendor_id", "dbt.int_dim_vendor__oms_vendor"),
                TestColumnQualifierTuple("vendor_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_lead_time", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("vendor_lead_time", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_name", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("vendor_name", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_name_cn", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("vendor_name_cn", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_type", "dbt.int_dim_vendor__oms_vendor"
                ),
                TestColumnQualifierTuple("vendor_type", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "active_flag", "dbt.int_dim_vendor__qb_vendor"
                ),
                TestColumnQualifierTuple("active_flag", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source", "dbt.int_dim_vendor__qb_vendor"
                ),
                TestColumnQualifierTuple("data_source", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "data_source_key", "dbt.int_dim_vendor__qb_vendor"
                ),
                TestColumnQualifierTuple("data_source_key", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("date_id", "dbt.int_dim_vendor__qb_vendor"),
                TestColumnQualifierTuple("date_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("vendor_id", "dbt.int_dim_vendor__qb_vendor"),
                TestColumnQualifierTuple("vendor_id", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple(
                    "vendor_name", "dbt.int_dim_vendor__qb_vendor"
                ),
                TestColumnQualifierTuple("vendor_name", "default.dws.dim_vendor"),
            ),
            (
                TestColumnQualifierTuple("*", "final_data", is_subquery=True),
                TestColumnQualifierTuple("*", "default.dws.dim_vendor"),
            ),
        ],
        dialect=dialect,
        skip_graph_check=True,
    )


@pytest.mark.parametrize("dialect", ["clickhouse"])
def test_create_table_cte_union_all_positional_column_alignment(dialect: str):
    """
    Test column lineage through CTEs combined via UNION ALL with SELECT *.
    Validates that positional column alignment maps source2.c to target.b.
    """
    sql = """
CREATE TABLE target
ENGINE = MergeTree()
ORDER BY id
AS
WITH
cte1 AS (
    SELECT a, b FROM source1
    WHERE id NOT IN (SELECT id FROM source2)
),
cte2 AS (
    SELECT a, c FROM source2
),
final AS (
    SELECT * FROM cte1
    UNION ALL
    SELECT * FROM cte2
)
SELECT * FROM final
    """

    assert_table_lineage_equal(
        sql,
        {"source1", "source2"},
        {"target"},
        dialect=dialect,
        skip_graph_check=True,
    )

    # Positional alignment: source2.c (position 2) should map to target.b (position 2 from cte1).
    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple("a", "source1"),
                TestColumnQualifierTuple("a", "target"),
            ),
            (
                TestColumnQualifierTuple("b", "source1"),
                TestColumnQualifierTuple("b", "target"),
            ),
            (
                TestColumnQualifierTuple("a", "source2"),
                TestColumnQualifierTuple("a", "target"),
            ),
            (
                TestColumnQualifierTuple("c", "source2"),
                TestColumnQualifierTuple("b", "target"),
            ),
        ],
        dialect=dialect,
        # SqlGlot: resolves per-column lineage but maps source2.c -> target.c (by name, not position)
        test_sqlglot=False,
        # SqlFluff: only produces wildcard edges (cte.* -> target.*), no column expansion
        test_sqlfluff=False,
        # SqlParse: returns empty column lineage
        test_sqlparse=False,
    )
