# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.policy.registry import register_trigger_rule


DISALLOWED_TAGS = [
    "CUSTOM_ENCODED_SQL_INJECTION",
    "CUSTOM_ENCODED",
    "CUSTOM_VALIDATED_SQL_INJECTION",
    "CUSTOM_VALIDATED",
    "LIMITED_CHARS",
    "SQL_ENCODED",
]

# NOTE: The nodes for the methods in dbapi2 modules do not correspond exactly to real
# patch locations. Instead, we pretend that every dbapi2 cursor object is
# called Cursor. This is done for convenience and for storytelling purposes.
# Our patches (which in these cases are not controlled by policy) account for
# this and perform the policy lookup correctly
sql_injection_triggers = [
    {
        "module": ["sqlite3.dbapi2", "sqlite3"],
        "class_name": "Cursor",
        "method_name": ["execute", "executemany", "executescript"],
        # ARG_1 is safe, because the SQL statement is prepared
        # takes no keyword arguments
        "source": "ARG_0",
        "policy_patch": False,
    },
    {
        "module": "mysql.connector",
        "class_name": "Cursor",
        "method_name": ["execute", "executemany"],
        # ARG_1 is safe, because the SQL statement is prepared
        "source": "ARG_0,KWARG:operation",
        "policy_patch": False,
    },
    {
        "module": "mysql.connector.cursor_cext",
        "class_name": "CMySQLCursor",
        "method_name": ["execute", "executemany"],
        # ARG_1 is safe, because the SQL statement is prepared
        "source": "ARG_0,KWARG:operation",
        "policy_patch": False,
    },
    {
        "module": "pymysql",
        "class_name": "Cursor",
        "method_name": ["execute", "executemany"],
        # ARG_1 is safe, because the SQL statement is prepared
        "source": "ARG_0,KWARG:query",
        "policy_patch": False,
    },
    {
        "module": "psycopg2",
        "class_name": "Cursor",
        "method_name": ["execute", "executemany"],
        # ARG_1 is safe, because the SQL statement is prepared
        "source": "ARG_0,KWARG:query",
        "policy_patch": False,
    },
    {
        # Used to handle any SQLAlchemy dialect
        "module": "sqlalchemy",
        "class_name": "Cursor",
        "method_name": ["execute", "executemany"],
        "source": "ARG_0",
        "policy_patch": False,
    },
]


register_trigger_rule(
    DataflowRule.from_nodes(
        "sql-injection",
        sql_injection_triggers,
        disallowed_tags=DISALLOWED_TAGS,
    )
)
