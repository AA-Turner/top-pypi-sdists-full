"""Tests for Snowflake ALTER TABLE ... SWAP WITH statements."""

from tests.helpers import assert_table_lineage_equal


def test_swap_rds_outreach_templates():
    """
    ServiceNow Query ID 4 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.TEMPLATES
SWAP WITH
RDS.OUTREACH.STG_TEMPLATES
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_templates"},
        {"rds.outreach.templates"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_users():
    """
    ServiceNow Query ID 51 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.USERS
SWAP WITH
RDS.OUTREACH.STG_USERS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_users"},
        {"rds.outreach.users"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_teams():
    """
    ServiceNow Query ID 68 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.TEAMS
SWAP WITH
RDS.OUTREACH.STG_TEAMS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_teams"},
        {"rds.outreach.teams"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_content_category_memberships():
    """
    ServiceNow Query ID 83 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.CONTENT_CATEGORY_MEMBERSHIPS
SWAP WITH
RDS.OUTREACH.STG_CONTENT_CATEGORY_MEMBERSHIPS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_content_category_memberships"},
        {"rds.outreach.content_category_memberships"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_content_categories():
    """
    ServiceNow Query ID 105 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.CONTENT_CATEGORIES
SWAP WITH
RDS.OUTREACH.STG_CONTENT_CATEGORIES
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_content_categories"},
        {"rds.outreach.content_categories"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_opportunities():
    """
    ServiceNow Query ID 160 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.SEQUENCE_STATES
SWAP WITH
RDS.OUTREACH.STG_SEQUENCE_STATES
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_sequence_states"},
        {"rds.outreach.sequence_states"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_mailings():
    """
    ServiceNow Query ID 173 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.CALLS
SWAP WITH
RDS.OUTREACH.STG_CALLS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_calls"},
        {"rds.outreach.calls"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_calls():
    """
    ServiceNow Query ID 179 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.MAILINGS
SWAP WITH
RDS.OUTREACH.STG_MAILINGS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_mailings"},
        {"rds.outreach.mailings"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_personas():
    """
    ServiceNow Query ID 189 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.ACCOUNTS
SWAP WITH
RDS.OUTREACH.STG_ACCOUNTS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_accounts"},
        {"rds.outreach.accounts"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_content_category_ownerships():
    """
    ServiceNow Query ID 241 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.TEAM_MEMBERSHIPS
SWAP WITH
RDS.OUTREACH.STG_TEAM_MEMBERSHIPS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_team_memberships"},
        {"rds.outreach.team_memberships"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_templates05():
    """
    ServiceNow Query ID 405 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.TEAM_MEMBERSHIPS_HISTORY
SWAP WITH
RDS.OUTREACH.STG_TEAM_MEMBERSHIPS_HISTORY
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_team_memberships_history"},
        {"rds.outreach.team_memberships_history"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_templates53():
    """
    ServiceNow Query ID 453 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.SEQUENCES
SWAP WITH
RDS.OUTREACH.STG_SEQUENCES
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_sequences"},
        {"rds.outreach.sequences"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_templates61():
    """
    ServiceNow Query ID 461 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.PROSPECT_EMAIL_ADDRESSES
SWAP WITH
RDS.OUTREACH.STG_PROSPECT_EMAIL_ADDRESSES
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_prospect_email_addresses"},
        {"rds.outreach.prospect_email_addresses"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_users8():
    """
    ServiceNow Query ID 518 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.CALENDARS
SWAP WITH
RDS.OUTREACH.STG_CALENDARS
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_calendars"},
        {"rds.outreach.calendars"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )


def test_swap_rds_outreach_prospects():
    """
    ServiceNow Query ID 522 - Swap Statements

    Reference parser: sqlglot
    Suspected incorrect: sqlparse
    """
    sql = """\
ALTER TABLE IF EXISTS
RDS.OUTREACH.MAILBOXES
SWAP WITH
RDS.OUTREACH.STG_MAILBOXES
"""

    # Table lineage
    # SqlParse: Cannot correctly parse SWAP statements - extracts wrong tables
    assert_table_lineage_equal(
        sql,
        {"rds.outreach.stg_mailboxes"},
        {"rds.outreach.mailboxes"},
        dialect="snowflake",
        test_sqlparse=False,  # SqlParse fails on this query
    )
