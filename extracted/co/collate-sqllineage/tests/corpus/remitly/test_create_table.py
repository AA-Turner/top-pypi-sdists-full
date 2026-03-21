"""Tests for Remitly Trino CREATE TABLE queries."""

import pytest

from tests.helpers import assert_table_lineage_equal


@pytest.mark.parametrize("dialect", ["trino"])
def test_with_compound_query(dialect: str):
    """Test CREATE OR REPLACE TABLE with complex CASE/WHEN and regex functions."""
    sql = """CREATE OR REPLACE TABLE marketing_intermediate.rockerbox_mta_preprocessed_step1

AS -- *****************************************************************************************************
-- ************ Add corridor and conversion_type, Create separate columns for names and ids ************
-- *****************************************************************************************************

select mta.date_key
     , SUBSTRING(mta.action, length(mta.action) - 6, 3) || '-' || SUBSTRING(mta.action, length(mta.action) - 2, 3) as corridor
     , case
           when lower(mta.action) like '%ftt_finish%' then 'NCA'
           when lower(mta.action) like '%complete_registration%' then 'Signup'
           else 'Other' end                                                                                  as conversion_type
     , cd.customer_key
     , mta.external_id                                                                                       as customer_public_id
     , mta.event_id
     , mta.conversion_key
     , mta.report_name
     , mta.precedence
     , trim(mta.tier_1)                                                                                      as channel_group
     , lower(trim(mta.tier_2))                                                                               as channel_source
     , case
           WHEN (REGEXP_LIKE(mta.tier_3, '^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$')
      AND tier_4 = 'snapchat_int') then null
           when cardinality(regexp_extract_all(mta.tier_3, '^[0-9]+$')) = 0 then mta.tier_3
           else null end                                                                                     as campaign_name
     , case
           when cardinality(regexp_extract_all(mta.tier_3, '^[0-9]+$')) = 1 or
           ((REGEXP_LIKE(mta.tier_3, '^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$')
      AND tier_4 = 'snapchat_int')) then mta.tier_3
           else null end                                                                                     as campaign_id
     , case
           when cardinality(regexp_extract_all(mta.tier_4, '^[0-9]+$')) = 0 then mta.tier_4
           else null end                                                                                     as adset_name
     , case when cardinality(regexp_extract_all(mta.tier_4, '^[0-9]+$')) = 1 then mta.tier_4 else null end   as adset_id
     , case
            WHEN (REGEXP_LIKE(mta.tier_3, '^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$')
      AND tier_4 = 'snapchat_int') then null
           when cardinality(regexp_extract_all(mta.tier_5, '^[0-9]+$')) = 0 then mta.tier_5 else null end   as ad_name
     , case when cardinality(regexp_extract_all(mta.tier_5, '^[0-9]+$')) = 1 or
           ( (REGEXP_LIKE(mta.tier_3, '^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$')
      AND tier_4 = 'snapchat_int')) then mta.tier_5 else null end                                      as ad_id
     , mta.original_url
     , mta.first_touch                                                                                       as first_touch
     , mta.even                                                                                              as even_touch
     , mta.last_touch                                                                                        as last_touch
     , mta.even                                                                                              as stat_model
     , mta.sequence_number
     , mta.timestamp_conv
     , mta.timestamp_events
     , mta.matches
from marketing_raw.rockerbox_mta mta
         join marketing.core_marketing_customer_dimension cd
              on mta.external_id = cd.customer_public_id"""
    assert_table_lineage_equal(
        sql,
        {"marketing_raw.rockerbox_mta", "marketing.core_marketing_customer_dimension"},
        {"marketing_intermediate.rockerbox_mta_preprocessed_step1"},
        dialect=dialect,
    )
