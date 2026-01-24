#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Utility functions for transforming Neo4j Spark Connector options to JDBC options.

This approach reuses the existing JDBC infrastructure for Neo4j integration.

Pros:
    - Reuses existing JDBC infrastructure, minimal code, easy maintenance
    - Single JDBC code path to maintain; improvements benefit Neo4j automatically
    - Users can use familiar Neo4j Spark Connector syntax

Cons:
    - Limited feature parity (no partitioning, no property projection)
    - JDBC single-connection bottleneck
    - Many Neo4j Spark Connector options aren't supported (e.g., node.keys,
      relationship.source.labels, schema.flatten.limit, partitioning options)
"""

import logging
import re
from typing import Literal

from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

logger = logging.getLogger("snowflake_connect_server")

# Valid Neo4j identifier pattern: starts with letter or underscore, followed by
# alphanumeric characters, underscores, or dollar signs
# Neo4j also allows backtick-quoted identifiers, but we don't support those here
_VALID_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_$]*$")


def validate_cypher_identifier(identifier: str, identifier_type: str) -> None:
    """
    Validate that a string is a safe Neo4j identifier (label, relationship type, or property).

    This prevents Cypher injection attacks by ensuring identifiers contain only
    safe characters.

    Args:
        identifier: The identifier to validate
        identifier_type: Description for error messages (e.g., "label", "relationship type")

    Raises:
        ValueError: If the identifier contains invalid characters
    """
    if not identifier:
        exception = ValueError(f"Neo4j {identifier_type} cannot be empty")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    if not _VALID_IDENTIFIER_PATTERN.match(identifier):
        exception = ValueError(
            f"Invalid Neo4j {identifier_type} '{identifier}'. "
            f"Identifiers must start with a letter or underscore and contain only "
            f"alphanumeric characters, underscores, or dollar signs."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def transform_neo4j_to_jdbc_options(
    options: dict[str, str],
    operation: Literal["read", "write"],
) -> dict[str, str]:
    """
    Transform Neo4j Spark Connector options to JDBC options.

    Args:
        options: Neo4j Spark Connector options dictionary
        operation: Either "read" or "write" to determine the transformation behavior

    Neo4j Spark Connector options:
        - url: bolt://host:port or neo4j://host:port
        - authentication.basic.username
        - authentication.basic.password
        - labels: Node label(s) to query/write
        - relationship: Relationship type to query (read only)
        - query: Custom Cypher query (read only)

    JDBC options (returned):
        - url: jdbc:neo4j:bolt://host:port
        - driver: org.neo4j.jdbc.Neo4jDriver
        - user: username
        - password: password
        - query: Cypher query (for read)
        - dbtable: Node label (for write)

    Returns:
        dict with JDBC-compatible options
    """
    jdbc_options = {}

    # Validate and transform URL to JDBC format
    # Neo4j JDBC 6.x expects: jdbc:neo4j://host:port (without transport protocol in URL)
    # Input can be: bolt://host:port, neo4j://host:port, or already jdbc:neo4j://...
    url = options.get("url", "")
    if not url:
        exception = ValueError(
            "Neo4j data source requires 'url' option (e.g., 'bolt://host:port' or 'neo4j://host:port')"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if url.startswith("jdbc:"):
        jdbc_options["url"] = url
    elif url.startswith("bolt://"):
        # bolt://host:port -> jdbc:neo4j://host:port (strip bolt://, add jdbc:neo4j://)
        jdbc_options["url"] = f"jdbc:neo4j://{url[7:]}"
    elif url.startswith("bolt+s://"):
        # bolt+s://host:port -> jdbc:neo4j+s://host:port
        jdbc_options["url"] = f"jdbc:neo4j+s://{url[9:]}"
    elif url.startswith("neo4j://"):
        # neo4j://host:port -> jdbc:neo4j://host:port
        jdbc_options["url"] = f"jdbc:neo4j://{url[8:]}"
    elif url.startswith("neo4j+s://"):
        # neo4j+s://host:port -> jdbc:neo4j+s://host:port
        jdbc_options["url"] = f"jdbc:neo4j+s://{url[10:]}"
    else:
        # Assume it's just host:port
        jdbc_options["url"] = f"jdbc:neo4j://{url}"

    # Set the JDBC driver (neo4j-jdbc 6.x uses org.neo4j.jdbc.Neo4jDriver)
    jdbc_options["driver"] = "org.neo4j.jdbc.Neo4jDriver"

    # Transform authentication options
    if "authentication.basic.username" in options:
        jdbc_options["user"] = options["authentication.basic.username"]
    if "authentication.basic.password" in options:
        jdbc_options["password"] = options["authentication.basic.password"]

    # Operation-specific transformations
    if operation == "read":
        # Build Cypher query from labels, relationship, or query options
        if "query" in options:
            jdbc_options["query"] = options["query"]
        elif "labels" in options:
            label = options["labels"]
            validate_cypher_identifier(label, "label")
            # Pass through - query will be resolved in jdbc_read_dbapi using existing connection
            jdbc_options["labels"] = label
        elif "relationship" in options:
            rel_type = options["relationship"]
            validate_cypher_identifier(rel_type, "relationship type")
            # Pass through - query will be resolved in jdbc_read_dbapi using existing connection
            jdbc_options["relationship"] = rel_type
        else:
            exception = ValueError(
                "Neo4j data source requires one of 'query', 'labels', or 'relationship' option"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
    elif operation == "write":
        # For write, labels becomes dbtable (the node label to create)
        if "labels" in options:
            label = options["labels"]
            validate_cypher_identifier(label, "label")
            jdbc_options["dbtable"] = label
        elif "node.keys" in options:
            # Some Neo4j connector variants use node.keys
            label = options.get("labels", "Node")
            validate_cypher_identifier(label, "label")
            jdbc_options["dbtable"] = label
        else:
            exception = ValueError(
                "Neo4j write requires 'labels' option to specify the node label"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception

    return jdbc_options
