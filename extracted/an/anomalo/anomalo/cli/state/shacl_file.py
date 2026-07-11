from __future__ import annotations

import json
import os
from typing import Any

from pyshacl import validate
from rdflib import RDF, Graph, Literal, Namespace, URIRef

from .errors import InvalidFile
from .models import Check, State, Table


VERSION_ID = 2

# Namespace definitions
ANOMALO = Namespace("http://anomalo.com/ontology#")
SHAPES = Namespace("http://anomalo.com/shapes#")
SH = Namespace("http://www.w3.org/ns/shacl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


class ShaclFileDriver:
    def __init__(self, state: State | None = None, validate_shacl: bool = True):
        self.state = state or State()
        self.validate_shacl = validate_shacl

    def load_file(self, filename: str) -> None:
        try:
            graph = Graph()
            graph.parse(filename, format="turtle")
        except FileNotFoundError as e:
            raise InvalidFile(filename, "cannot be read") from e
        except Exception as e:
            raise InvalidFile(filename, f"invalid SHACL/Turtle format: {e}") from e

        # Perform SHACL validation if enabled
        if self.validate_shacl:
            self._validate_with_shacl(graph, filename)

        self.state = self._graph_to_state(graph)

    def write_file(self, filename: str) -> None:
        graph = self._state_to_graph(self.state)
        graph.serialize(destination=filename, format="turtle")

    def to_string(self) -> str:
        graph = self._state_to_graph(self.state)
        return graph.serialize(format="turtle")

    def _validate_with_shacl(self, graph: Graph, filename: str) -> None:
        """Validate the graph against SHACL shapes.

        Args:
            graph: The RDF graph to validate
            filename: The filename being validated (for error messages)

        Raises:
            InvalidFile: If SHACL validation fails
        """
        # Load the SHACL shapes file
        shapes_path = os.path.join(
            os.path.dirname(__file__), "anomalo_shacl_shapes.ttl"
        )

        try:
            shapes_graph = Graph()
            shapes_graph.parse(shapes_path, format="turtle")
        except Exception as e:
            # If we can't load the shapes file, log a warning but don't fail
            # This allows the system to work even if the shapes file is missing
            import logging

            logging.warning(
                f"Could not load SHACL shapes from {shapes_path}: {e}. "
                "Skipping SHACL validation."
            )
            return

        # Perform validation
        try:
            conforms, results_graph, results_text = validate(
                graph,
                shacl_graph=shapes_graph,
                inference="rdfs",
                abort_on_first=False,
                allow_warnings=True,
            )

            if not conforms:
                raise InvalidFile(
                    filename, f"SHACL validation failed:\n\n{results_text}"
                )
        except InvalidFile:
            raise
        except Exception as e:
            raise InvalidFile(filename, f"SHACL validation error: {e}") from e

    def _graph_to_state(self, graph: Graph) -> State:
        state = State()

        # Find all Tables (instances of anomalo:Table)
        for table_uri in graph.subjects(RDF.type, ANOMALO.Table):
            table_ref = self._get_property_value(graph, table_uri, ANOMALO.tableRef)
            if not table_ref:
                continue

            table = Table()

            # Extract table configuration
            config_uri = graph.value(table_uri, ANOMALO.hasConfiguration)
            if config_uri:
                table.config = self._extract_configuration(graph, config_uri)

            # Extract labels - check for explicit empty marker
            has_empty_labels_marker = graph.value(table_uri, ANOMALO.hasEmptyLabels)
            if has_empty_labels_marker:
                table.labels = []
            else:
                labels = list(graph.objects(table_uri, ANOMALO.hasLabel))
                if labels:
                    table.labels = [str(label) for label in labels]

            # Extract notification_channels - check for explicit empty marker
            has_empty_notif_marker = graph.value(
                table_uri, ANOMALO.hasEmptyNotificationChannels
            )
            if has_empty_notif_marker:
                table.notification_channels = []
            else:
                notif_channels = list(
                    graph.objects(table_uri, ANOMALO.hasNotificationChannel)
                )
                if notif_channels:
                    table.notification_channels = [str(nc) for nc in notif_channels]

            # Extract checks
            for check_uri in graph.objects(table_uri, ANOMALO.hasCheck):
                check_ref = self._get_property_value(graph, check_uri, ANOMALO.checkRef)
                if check_ref:
                    table.checks[check_ref] = self._extract_check(graph, check_uri)

            # Extract system checks
            for check_uri in graph.objects(table_uri, ANOMALO.hasSystemCheck):
                check_ref = self._get_property_value(graph, check_uri, ANOMALO.checkRef)
                if check_ref:
                    table.system_checks[check_ref] = self._extract_check(
                        graph, check_uri
                    )

            state.tables[table_ref] = table

        return state

    def _extract_configuration(
        self, graph: Graph, config_uri: URIRef
    ) -> dict[str, Any]:
        config = {}

        # Mapping from RDF property to config key
        property_map = {
            ANOMALO.enableDataQuality: ("enable_data_quality", bool),
            ANOMALO.enableObservability: ("enable_observability", bool),
            ANOMALO.checkCadenceType: ("check_cadence_type", str),
            ANOMALO.checkCadenceRunAtDuration: ("check_cadence_run_at_duration", str),
            ANOMALO.scopeOfDataToCheck: ("scope_of_data_to_check", str),
            ANOMALO.alwaysAlertOnErrors: ("always_alert_on_errors", bool),
            ANOMALO.useAutoSla: ("use_auto_sla", bool),
            ANOMALO.definition: ("definition", str),
            ANOMALO.anomaloViewSql: ("anomalo_view_sql", str),
            ANOMALO.freshAfter: ("fresh_after", str),
            ANOMALO.notifyAfter: ("notify_after", str),
            ANOMALO.intervalSkipExpr: ("interval_skip_expr", str),
            ANOMALO.customHolidays: ("custom_holidays", str),
            ANOMALO.timeColumnType: ("time_column_type", str),
        }

        for rdf_prop, (config_key, value_type) in property_map.items():
            value = graph.value(config_uri, rdf_prop)
            if value is not None:
                if value_type == bool:
                    config[config_key] = value.toPython()
                else:
                    str_value = str(value)
                    # Skip string "None"
                    if str_value == "None":
                        continue
                    config[config_key] = str_value
            else:
                # Check for explicit null marker
                null_prop_uri = URIRef(str(rdf_prop) + "_isNull")
                is_null = graph.value(config_uri, null_prop_uri)
                if is_null:
                    config[config_key] = None

        # Handle multi-value properties
        time_columns = list(graph.objects(config_uri, ANOMALO.timeColumn))
        if time_columns:
            config["time_columns"] = [str(tc) for tc in time_columns]
        else:
            # Check for null marker
            is_null = graph.value(config_uri, ANOMALO.timeColumnsIsNull)
            if is_null:
                config["time_columns"] = None

        disabled_checks = list(
            graph.objects(config_uri, ANOMALO.disabledQualityCheckId)
        )
        if disabled_checks:
            config["disabled_quality_check_ids"] = [int(dc) for dc in disabled_checks]

        return config

    def _extract_check(self, graph: Graph, check_uri: URIRef) -> Check:
        check_type = self._get_property_value(graph, check_uri, ANOMALO.checkType)
        check = Check(check_type=check_type or "unknown")

        # Extract parameters
        params = {}
        for param_uri in graph.objects(check_uri, ANOMALO.hasParameter):
            param_name = self._get_property_value(
                graph, param_uri, ANOMALO.parameterName
            )
            # Get the actual Literal object to access datatype
            param_literal = graph.value(param_uri, ANOMALO.parameterValue)
            if param_name:
                if param_literal is not None:
                    param_value = self._parse_typed_literal(param_literal)
                    # Skip string "None"
                    if param_value == "None":
                        continue
                    params[param_name] = param_value
                else:
                    # Check for explicit null marker
                    is_null = graph.value(param_uri, ANOMALO.isNull)
                    if is_null:
                        params[param_name] = None

        # Add other check properties to params
        priority_literal = graph.value(check_uri, ANOMALO.priorityLevel)
        if priority_literal is not None:
            params["priority_level"] = self._parse_typed_literal(priority_literal)

        time_based = graph.value(check_uri, ANOMALO.timeBased)
        if time_based is not None:
            params["time_based"] = time_based.toPython()

        alert_default = graph.value(check_uri, ANOMALO.alertDefaultNotifChannel)
        if alert_default is not None:
            params["alert_default_notif_channel"] = alert_default.toPython()

        check.params = params

        # Extract labels - check for explicit empty marker
        has_empty_labels_marker = graph.value(check_uri, ANOMALO.hasEmptyLabels)
        if has_empty_labels_marker:
            check.labels = []
        else:
            labels = list(graph.objects(check_uri, ANOMALO.hasLabel))
            if labels:
                check.labels = [str(label) for label in labels]

        # Extract notification_channels - check for explicit empty marker
        has_empty_notif_marker = graph.value(
            check_uri, ANOMALO.hasEmptyNotificationChannels
        )
        if has_empty_notif_marker:
            check.notification_channels = []
        else:
            notif_channels = list(
                graph.objects(check_uri, ANOMALO.hasNotificationChannel)
            )
            if notif_channels:
                check.notification_channels = [str(nc) for nc in notif_channels]

        return check

    def _get_property_value(
        self, graph: Graph, subject: URIRef, predicate: URIRef
    ) -> str | None:
        value = graph.value(subject, predicate)
        return str(value) if value is not None else None

    def _parse_typed_literal(self, literal) -> Any:
        """Parse an RDF Literal with datatype information."""
        # Get the datatype if present
        datatype = literal.datatype if hasattr(literal, "datatype") else None

        # Convert based on datatype - ONLY if explicit datatype is set
        if datatype == XSD.boolean:
            return literal.toPython()
        elif datatype == XSD.integer:
            return int(literal)
        elif datatype == XSD.double or datatype == XSD.float:
            return float(literal)
        else:
            # String value or no explicit datatype
            str_value = str(literal)

            # Try to parse as JSON for lists (JSON-encoded arrays)
            if str_value.startswith("[") and str_value.endswith("]"):
                try:
                    return json.loads(str_value)
                except (json.JSONDecodeError, ValueError):
                    pass

            # For untyped strings, return as-is (don't try to convert to int/float)
            # This preserves values like "1079" as strings
            return str_value

    def _state_to_graph(self, state: State) -> Graph:
        graph = Graph()
        graph.bind("anomalo", ANOMALO)
        graph.bind("shapes", SHAPES)
        graph.bind("sh", SH)
        graph.bind("xsd", XSD)

        # Add configuration metadata
        config_uri = URIRef("http://anomalo.com/configuration")
        graph.add((config_uri, RDF.type, ANOMALO.Configuration))
        graph.add(
            (config_uri, ANOMALO.versionID, Literal(VERSION_ID, datatype=XSD.integer))
        )

        # Add each table
        for table_ref, table in state.tables.items():
            table_uri = URIRef(f"http://anomalo.com/tables/{table_ref}")
            graph.add((table_uri, RDF.type, ANOMALO.Table))
            graph.add((table_uri, ANOMALO.tableRef, Literal(table_ref)))

            # Parse table_ref to extract warehouse, schema, and table name
            parts = table_ref.split(".")
            if len(parts) >= 3:
                graph.add((table_uri, ANOMALO.warehouse, Literal(parts[0])))
                graph.add((table_uri, ANOMALO.schema, Literal(parts[1])))
                graph.add((table_uri, ANOMALO.tableName, Literal(".".join(parts[2:]))))

            # Add labels - distinguish between None (omitted), [] (empty), and values
            if table.labels is not None:
                if len(table.labels) == 0:
                    # Explicitly mark as empty list
                    graph.add(
                        (
                            table_uri,
                            ANOMALO.hasEmptyLabels,
                            Literal(True, datatype=XSD.boolean),
                        )
                    )
                else:
                    for label in table.labels:
                        graph.add((table_uri, ANOMALO.hasLabel, Literal(label)))

            # Add notification_channels
            if table.notification_channels is not None:
                if len(table.notification_channels) == 0:
                    # Explicitly mark as empty list
                    graph.add(
                        (
                            table_uri,
                            ANOMALO.hasEmptyNotificationChannels,
                            Literal(True, datatype=XSD.boolean),
                        )
                    )
                else:
                    for nc in table.notification_channels:
                        graph.add(
                            (table_uri, ANOMALO.hasNotificationChannel, Literal(nc))
                        )

            # Add configuration
            if table.config:
                table_config_uri = URIRef(
                    f"http://anomalo.com/tables/{table_ref}/config"
                )
                graph.add((table_config_uri, RDF.type, ANOMALO.TableConfiguration))
                graph.add((table_uri, ANOMALO.hasConfiguration, table_config_uri))
                self._add_configuration(graph, table_config_uri, table.config)

            # Add checks
            for check_ref, check in table.checks.items():
                check_uri = URIRef(
                    f"http://anomalo.com/tables/{table_ref}/checks/{check_ref}"
                )
                graph.add((check_uri, RDF.type, ANOMALO.Check))
                graph.add((table_uri, ANOMALO.hasCheck, check_uri))
                self._add_check(graph, check_uri, check_ref, check)

            # Add system checks
            for check_ref, check in table.system_checks.items():
                check_uri = URIRef(
                    f"http://anomalo.com/tables/{table_ref}/system_checks/{check_ref}"
                )
                graph.add((check_uri, RDF.type, ANOMALO.SystemCheck))
                graph.add((table_uri, ANOMALO.hasSystemCheck, check_uri))
                self._add_check(graph, check_uri, check_ref, check)

        return graph

    def _add_configuration(
        self, graph: Graph, config_uri: URIRef, config: dict[str, Any]
    ) -> None:
        # Mapping from config key to RDF property
        property_map = {
            "enable_data_quality": (ANOMALO.enableDataQuality, XSD.boolean),
            "enable_observability": (ANOMALO.enableObservability, XSD.boolean),
            "check_cadence_type": (ANOMALO.checkCadenceType, XSD.string),
            "check_cadence_run_at_duration": (
                ANOMALO.checkCadenceRunAtDuration,
                XSD.string,
            ),
            "scope_of_data_to_check": (ANOMALO.scopeOfDataToCheck, XSD.string),
            "always_alert_on_errors": (ANOMALO.alwaysAlertOnErrors, XSD.boolean),
            "use_auto_sla": (ANOMALO.useAutoSla, XSD.boolean),
            "definition": (ANOMALO.definition, XSD.string),
            "anomalo_view_sql": (ANOMALO.anomaloViewSql, XSD.string),
            "fresh_after": (ANOMALO.freshAfter, XSD.string),
            "notify_after": (ANOMALO.notifyAfter, XSD.duration),
            "interval_skip_expr": (ANOMALO.intervalSkipExpr, XSD.string),
            "custom_holidays": (ANOMALO.customHolidays, XSD.string),
            "time_column_type": (ANOMALO.timeColumnType, XSD.string),
        }

        for config_key, value in config.items():
            if config_key in property_map:
                rdf_prop, datatype = property_map[config_key]

                # Handle None values with explicit markers
                if value is None:
                    null_prop_uri = URIRef(str(rdf_prop) + "_isNull")
                    graph.add(
                        (config_uri, null_prop_uri, Literal(True, datatype=XSD.boolean))
                    )
                    continue

                # Skip string "None"
                if isinstance(value, str) and value == "None":
                    continue

                graph.add((config_uri, rdf_prop, Literal(value, datatype=datatype)))
            elif config_key == "time_columns":
                if value is None:
                    # Explicit null marker
                    graph.add(
                        (
                            config_uri,
                            ANOMALO.timeColumnsIsNull,
                            Literal(True, datatype=XSD.boolean),
                        )
                    )
                elif isinstance(value, list):
                    for tc in value:
                        graph.add((config_uri, ANOMALO.timeColumn, Literal(tc)))
            elif config_key == "disabled_quality_check_ids" and isinstance(value, list):
                for dc in value:
                    graph.add(
                        (
                            config_uri,
                            ANOMALO.disabledQualityCheckId,
                            Literal(dc, datatype=XSD.integer),
                        )
                    )

    def _add_check(
        self, graph: Graph, check_uri: URIRef, check_ref: str, check: Check
    ) -> None:
        graph.add((check_uri, ANOMALO.checkRef, Literal(check_ref)))
        graph.add((check_uri, ANOMALO.checkType, Literal(check.check_type)))

        # Add parameters as separate Parameter objects
        for param_name, param_value in check.params.items():
            if param_name in (
                "priority_level",
                "time_based",
                "alert_default_notif_channel",
            ):
                # Skip None values - direct properties don't use isNull markers
                if param_value is None:
                    continue
                # These are direct properties, not parameters
                if param_name == "priority_level":
                    graph.add((check_uri, ANOMALO.priorityLevel, Literal(param_value)))
                elif param_name == "time_based":
                    graph.add(
                        (
                            check_uri,
                            ANOMALO.timeBased,
                            Literal(param_value, datatype=XSD.boolean),
                        )
                    )
                elif param_name == "alert_default_notif_channel":
                    graph.add(
                        (
                            check_uri,
                            ANOMALO.alertDefaultNotifChannel,
                            Literal(param_value, datatype=XSD.boolean),
                        )
                    )
            else:
                # Create a Parameter object
                param_uri = URIRef(f"{check_uri}/param/{param_name}")
                graph.add((param_uri, RDF.type, ANOMALO.Parameter))
                graph.add((check_uri, ANOMALO.hasParameter, param_uri))
                graph.add((param_uri, ANOMALO.parameterName, Literal(param_name)))

                # Handle null values explicitly
                if param_value is None:
                    # Mark as explicitly null
                    graph.add(
                        (param_uri, ANOMALO.isNull, Literal(True, datatype=XSD.boolean))
                    )
                    continue

                # Skip string "None"
                if isinstance(param_value, str) and param_value == "None":
                    continue

                # Store value with type information
                if isinstance(param_value, bool):
                    graph.add(
                        (
                            param_uri,
                            ANOMALO.parameterValue,
                            Literal(param_value, datatype=XSD.boolean),
                        )
                    )
                elif isinstance(param_value, int):
                    graph.add(
                        (
                            param_uri,
                            ANOMALO.parameterValue,
                            Literal(param_value, datatype=XSD.integer),
                        )
                    )
                elif isinstance(param_value, float):
                    graph.add(
                        (
                            param_uri,
                            ANOMALO.parameterValue,
                            Literal(param_value, datatype=XSD.double),
                        )
                    )
                elif isinstance(param_value, list):
                    # Store list as JSON string
                    graph.add(
                        (
                            param_uri,
                            ANOMALO.parameterValue,
                            Literal(json.dumps(param_value)),
                        )
                    )
                else:
                    # Store as string
                    graph.add(
                        (param_uri, ANOMALO.parameterValue, Literal(str(param_value)))
                    )

        # Add labels - distinguish between None (omitted), [] (empty), and values
        if check.labels is not None:
            if len(check.labels) == 0:
                # Explicitly mark as empty list
                graph.add(
                    (
                        check_uri,
                        ANOMALO.hasEmptyLabels,
                        Literal(True, datatype=XSD.boolean),
                    )
                )
            else:
                for label in check.labels:
                    graph.add((check_uri, ANOMALO.hasLabel, Literal(label)))

        # Add notification_channels
        if check.notification_channels is not None:
            if len(check.notification_channels) == 0:
                # Explicitly mark as empty list
                graph.add(
                    (
                        check_uri,
                        ANOMALO.hasEmptyNotificationChannels,
                        Literal(True, datatype=XSD.boolean),
                    )
                )
            else:
                for nc in check.notification_channels:
                    graph.add((check_uri, ANOMALO.hasNotificationChannel, Literal(nc)))
