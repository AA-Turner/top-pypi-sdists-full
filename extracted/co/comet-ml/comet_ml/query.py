# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

import logging
import numbers
from datetime import datetime

from .exceptions import QueryException

__all__ = ["Environment", "Metadata", "Metric", "Other", "Parameter", "Tag"]


LOGGER = logging.getLogger(__name__)


class QueryExpression(object):
    def __init__(self, lhs, op, rhs=None, negated=False):
        self.lhs = lhs
        self.op = op
        self.negated = negated
        if isinstance(rhs, datetime):
            self.rhs = rhs.isoformat(" ")
        elif hasattr(rhs, "decode"):
            ok = True
            try:
                self.rhs = rhs.decode("utf-8")
            except Exception:
                LOGGER.debug("Error decoding value", exc_info=True)
                ok = False

            if not ok:
                raise ValueError("invalid expression %r: can't decode to unicode", rhs)
        else:
            self.rhs = rhs

    def __bool__(self):
        # For Python 3:
        raise TypeError(
            "can't use logical operators; use '&' for AND, '|' for OR, and '~' to invert your query"
        )

    def __nonzero__(self):
        # For Python 2:
        raise TypeError(
            "can't use logical operators; use '&' for AND, '|' for OR, and '~' to invert your query"
        )

    def __and__(self, rhs):
        return QueryExpression(self, "&", rhs)

    def __or__(self, rhs):
        return QueryExpression(self, "|", rhs)

    def __eq__(self, rhs):
        raise ValueError(
            "illegal operator on a query expression; use parentheses around expressions"
        )

    def __ne__(self, rhs):
        raise ValueError(
            "illegal operator on a query expression; use parentheses around expressions"
        )

    def __lt__(self, rhs):
        raise ValueError(
            "illegal operator on a query expression; use parentheses around expressions"
        )

    def __le__(self, rhs):
        raise ValueError(
            "illegal operator on a query expression; use parentheses around expressions"
        )

    def __gt__(self, rhs):
        raise ValueError(
            "illegal operator on a query expression; use parentheses around expressions"
        )

    def __ge__(self, rhs):
        raise ValueError(
            "illegal operator on a query expression; use parentheses around expressions"
        )

    def __invert__(self):
        if isinstance(self.lhs, _Tag):
            raise ValueError("can't negate a Tag expression")
        # Handle logical operators
        if self.op == "&":
            # De Morgan's law: ~(A & B) = ~A | ~B
            return QueryExpression(
                self.lhs.__invert__(), "|", self.rhs.__invert__(), negated=True
            )
        elif self.op == "|":
            # De Morgan's law: ~(A | B) = ~A & ~B
            return QueryExpression(
                self.lhs.__invert__(), "&", self.rhs.__invert__(), negated=True
            )
        # mathematical (6, including negatives):
        elif self.op == "equal":
            return QueryExpression(self.lhs, "not_equal", self.rhs, negated=True)
        elif self.op == "not_equal":
            return QueryExpression(self.lhs, "equal", self.rhs, negated=True)
        elif self.op == "less":
            return QueryExpression(self.lhs, "greater_or_equal", self.rhs, negated=True)
        elif self.op == "greater_or_equal":
            return QueryExpression(self.lhs, "less", self.rhs, negated=True)
        elif self.op == "greater":
            return QueryExpression(self.lhs, "less_or_equal", self.rhs, negated=True)
        elif self.op == "less_or_equal":
            return QueryExpression(self.lhs, "greater", self.rhs, negated=True)
        # special (6 positive, 6 negatives == 12):
        elif self.op == "between":
            return QueryExpression(self.lhs, "not_between", self.rhs, negated=True)
        elif self.op == "not_between":
            return QueryExpression(self.lhs, "between", self.rhs, negated=True)
        elif self.op == "contains":
            return QueryExpression(self.lhs, "not_contains", self.rhs, negated=True)
        elif self.op == "not_contains":
            return QueryExpression(self.lhs, "contains", self.rhs, negated=True)
        elif self.op == "begins_with":
            return QueryExpression(self.lhs, "not_begins_with", self.rhs, negated=True)
        elif self.op == "not_begins_with":
            return QueryExpression(self.lhs, "begins_with", self.rhs, negated=True)
        elif self.op == "ends_with":
            return QueryExpression(self.lhs, "not_ends_with", self.rhs, negated=True)
        elif self.op == "not_ends_with":
            return QueryExpression(self.lhs, "ends_with", self.rhs, negated=True)
        elif self.op == "is_null":
            return QueryExpression(self.lhs, "is_not_null", self.rhs, negated=True)
        elif self.op == "is_not_null":
            return QueryExpression(self.lhs, "is_null", self.rhs, negated=True)
        elif self.op == "is_empty":
            return QueryExpression(self.lhs, "is_not_empty", self.rhs, negated=True)
        elif self.op == "is_not_empty":
            return QueryExpression(self.lhs, "is_empty", self.rhs, negated=True)
        elif self.op is None:
            raise ValueError("can't negate this expression: %s" % repr(self))
        else:
            raise ValueError("unknown operator: %s" % self.op)

    def __repr__(self):
        if self.op:
            pp = {
                "equal": "==",
                "not_equal": "!=",
                "less": "<",
                "less_or_equal": "<=",
                "greater": ">",
                "greater_or_equal": ">=",
                "is_empty": "==",
                "is_not_empty": "!=",
                "is_null": "==",
                "is_not_null": "!=",
            }
            return "(%r %s %r)" % (self.lhs, pp.get(self.op, self.op), self.rhs)
        else:
            return repr(self.lhs)

    def _get_qtype(self, columns):
        # return string, boolean, double, datetime, timenumber
        for column_data in columns["columns"]:
            if (
                column_data["name"] == self.lhs.name
                and column_data["source"] == self.lhs.source
            ):
                return column_data["type"]
        raise QueryException("no such %s: %r" % (self.lhs.source, self.lhs.name))

    def _verify_qtype(self, qtype):
        if self.op in ["begins_with", "not_begins_with"]:
            if qtype != "string":
                raise ValueError(
                    "QueryVariable.startswith() requires that QueryVariable be a string type not %r"
                    % qtype
                )
        elif self.op in ["ends_with", "not_ends_with"]:
            if qtype != "string":
                raise ValueError(
                    "QueryVariable.endswith() requires that QueryVariable be a string type not %r"
                    % qtype
                )
        elif self.op in ["contains", "not_contains"]:
            if qtype != "string":
                raise ValueError(
                    "QueryVariable.contains() requires that QueryVariable be a string type not %r"
                    % qtype
                )
        elif self.op in ["between", "not_between"]:
            if qtype == "string":
                raise ValueError(
                    "QueryVariable.between() requires that QueryVariable be a numeric type not %r"
                    % qtype
                )
        # else, query is pretty leniant on type matching

    def _get_rules(self, columns):
        if self.lhs.qtype is None:
            self.lhs.qtype = self._get_qtype(columns)
        self._verify_qtype(self.lhs.qtype)
        rule = {
            "id": self.lhs.name,
            "field": self.lhs.name,
            "type": self.lhs.qtype,
            "operator": self.op,
            "value": self.rhs,
        }
        return [rule]

    def get_predicates(self, columns):
        if self.op == "&":
            if isinstance(self.lhs, QueryVariable):
                raise ValueError(
                    "invalid query expression on left: %r; you need to compare this value"
                    % (self.lhs,)
                )
            elif not isinstance(self.lhs, QueryExpression):
                raise ValueError(
                    "invalid query expression on left: %r; do not use 'and', 'or', 'not', 'is', or 'in'"
                    % (self.lhs,)
                )
            if isinstance(self.rhs, QueryVariable):
                raise ValueError(
                    "invalid query expression on right: %r; you need to compare this value"
                    % (self.rhs,)
                )
            elif not isinstance(self.rhs, QueryExpression):
                raise ValueError(
                    "invalid query expression on right: %r; do not use 'and', 'or', 'not', 'is', or 'in'"
                    % (self.rhs,)
                )
            lhs_predicates = self.lhs.get_predicates(columns)
            rhs_predicates = self.rhs.get_predicates(columns)
            # Combine:
            for predicate in rhs_predicates:
                lhs_sources = [pred["source"] for pred in lhs_predicates]
                if predicate["source"] in lhs_sources:
                    index = lhs_sources.index(predicate["source"])
                    lhs_predicate = lhs_predicates[index]

                    # Check if we need to preserve nested structure for AND operations
                    # If either LHS or RHS has an OR condition, we need to create an AND condition
                    # with the LHS and RHS as separate rules
                    lhs_has_or = (
                        lhs_predicate["query"]["condition"] == "OR"
                        and len(lhs_predicate["query"]["rules"]) > 1
                    )
                    rhs_has_or = (
                        predicate["query"]["condition"] == "OR"
                        and len(predicate["query"]["rules"]) > 1
                    )

                    if lhs_has_or or rhs_has_or:
                        # Create an AND condition with LHS and RHS as separate rules
                        # But if LHS is a simple condition (single rule), extract it directly
                        lhs_rule = lhs_predicate["query"]
                        if (
                            lhs_predicate["query"]["condition"] == "AND"
                            and len(lhs_predicate["query"]["rules"]) == 1
                        ):
                            lhs_rule = lhs_predicate["query"]["rules"][0]

                        new_predicate = {
                            "source": predicate["source"],
                            "query": {
                                "condition": "AND",
                                "rules": [lhs_rule, predicate["query"]],
                                "valid": True,
                            },
                        }
                        lhs_predicates[index] = new_predicate
                    else:
                        # Both are simple conditions, combine rules:
                        lhs_predicates[index]["query"]["rules"].extend(
                            predicate["query"]["rules"]
                        )
                else:  # add to predicates:
                    lhs_predicates.append(predicate)

            # Handle negation for old API - add negated flag to the result
            if hasattr(self, "negated") and self.negated:
                for predicate in lhs_predicates:
                    predicate["negated"] = True

            return lhs_predicates
        elif self.op == "|":
            # For the old API, we need to handle OR expressions differently
            # If this is a negated AND expression that became OR, we should avoid creating OR
            if hasattr(self, "negated") and self.negated:
                # This is a negated AND that became OR - we need to handle it specially
                # Instead of creating OR, we'll create separate predicates with negation
                lhs_predicates = self.lhs.get_predicates(columns)
                rhs_predicates = self.rhs.get_predicates(columns)

                # Mark all predicates as negated
                for predicate in lhs_predicates:
                    predicate["negated"] = True
                for predicate in rhs_predicates:
                    predicate["negated"] = True

                # Return all predicates separately (not as OR)
                return lhs_predicates + rhs_predicates

            # Regular OR handling (should not happen in old API, but keep for safety)
            if isinstance(self.lhs, QueryVariable):
                raise ValueError(
                    "invalid query expression on left: %r; you need to compare this value"
                    % (self.lhs,)
                )
            elif not isinstance(self.lhs, QueryExpression):
                raise ValueError(
                    "invalid query expression on left: %r; do not use 'and', 'or', 'not', 'is', or 'in'"
                    % (self.lhs,)
                )
            if isinstance(self.rhs, QueryVariable):
                raise ValueError(
                    "invalid query expression on right: %r; you need to compare this value"
                    % (self.rhs,)
                )
            elif not isinstance(self.rhs, QueryExpression):
                raise ValueError(
                    "invalid query expression on right: %r; do not use 'and', 'or', 'not', 'is', or 'in'"
                    % (self.rhs,)
                )
            lhs_predicates = self.lhs.get_predicates(columns)
            rhs_predicates = self.rhs.get_predicates(columns)

            # Check if we can flatten the OR operation into a single source
            all_sources = set()
            all_rules = []

            for pred in lhs_predicates:
                all_sources.add(pred["source"])
                # If the predicate has a single rule, extract it directly
                if len(pred["query"]["rules"]) == 1:
                    rule = pred["query"]["rules"][0].copy()
                    rule["source"] = pred["source"]
                    all_rules.append(rule)
                else:
                    # Multiple rules, keep the nested structure
                    all_rules.append(pred["query"])

            for pred in rhs_predicates:
                all_sources.add(pred["source"])
                # If the predicate has a single rule, extract it directly
                if len(pred["query"]["rules"]) == 1:
                    rule = pred["query"]["rules"][0].copy()
                    rule["source"] = pred["source"]
                    all_rules.append(rule)
                else:
                    # Multiple rules, keep the nested structure
                    all_rules.append(pred["query"])

            # If all predicates are from the same source, we can flatten
            if len(all_sources) == 1:
                source = list(all_sources)[0]
                return [
                    {
                        "source": source,
                        "query": {
                            "condition": "OR",
                            "rules": all_rules,
                            "valid": True,
                        },
                    }
                ]
            else:
                # Multiple sources, need nested structure
                return [
                    {
                        "source": "nested",
                        "query": {
                            "condition": "OR",
                            "rules": all_rules,
                            "valid": True,
                        },
                    }
                ]
        else:
            predicate = {
                "source": self.lhs.source,
                "query": {
                    "condition": "AND",
                    "rules": self._get_rules(columns),
                    "valid": True,
                },
            }

            # Handle negation for simple comparisons
            if hasattr(self, "negated") and self.negated:
                predicate["negated"] = True

            return [predicate]

    def _apply_demorgan_laws(self):
        """
        Apply De Morgan's laws to remove all NOT operations from the query expression.

        De Morgan's laws:
        ~(A & B) = ~A | ~B
        ~(A | B) = ~A & ~B
        ~(~A) = A (double negation)

        Returns:
            A new QueryExpression with all NOT operations removed
        """
        # First, recursively apply De Morgan's laws to children
        if isinstance(self.lhs, QueryExpression):
            transformed_lhs = self.lhs._apply_demorgan_laws()
        else:
            transformed_lhs = self.lhs

        if isinstance(self.rhs, QueryExpression):
            transformed_rhs = self.rhs._apply_demorgan_laws()
        else:
            transformed_rhs = self.rhs

        # Now handle negation at this level
        if not hasattr(self, "negated") or not self.negated:
            # No negation, return with transformed children
            return QueryExpression(
                transformed_lhs, self.op, transformed_rhs, negated=False
            )

        # Handle negation
        if isinstance(transformed_lhs, QueryVariable):
            # The __invert__ method has already converted the operator to its opposite
            # So we just need to remove the negated flag
            return QueryExpression(
                transformed_lhs, self.op, transformed_rhs, negated=False
            )

        elif isinstance(transformed_lhs, QueryExpression):
            # The __invert__ method has already applied De Morgan's laws correctly
            # We just need to remove the negated flag and recursively process children
            return QueryExpression(
                transformed_lhs._apply_demorgan_laws(),
                self.op,
                transformed_rhs._apply_demorgan_laws(),
                negated=False,
            )

        return QueryExpression(transformed_lhs, self.op, transformed_rhs, negated=False)

    def get_predicates_for_search(self, columns):
        """
        Get predicates optimized for search API - applies De Morgan's laws and handles source information.

        This method first applies De Morgan's laws to remove all NOT operations,
        then processes the query to generate search format with proper source information.

        Args:
            columns: Column information from the backend

        Returns:
            Processed predicates ready for search API
        """
        # Apply De Morgan's laws to remove all NOT operations
        demorgan_query = self._apply_demorgan_laws()

        # Use a search-specific predicate generation method
        predicates = demorgan_query._get_predicates_for_search_internal(columns)

        # Convert to search format recursively
        return self._convert_to_search_format(predicates, demorgan_query)

    def _convert_to_search_format(self, predicates, demorgan_query):
        """
        Recursively convert predicates to search format.

        This method handles the conversion from the internal predicate format
        to the search API format, preserving the correct logical structure.
        """
        if len(predicates) == 1 and predicates[0]["source"] == "nested":
            # Handle nested OR/AND expressions
            return predicates[0]["query"]
        elif len(predicates) == 1:
            # Single predicate - use its condition
            return predicates[0]["query"]
        else:
            # Multiple predicates - determine if they should be AND or OR
            if hasattr(demorgan_query, "op") and demorgan_query.op == "|":
                condition = "OR"
            else:
                condition = "AND"

            new_predicates = {"condition": condition, "rules": []}
            for pred in predicates:
                expr = pred["query"]
                new_predicates["rules"].append(expr)
            return new_predicates

    def _normalize_rules_recursively(self, rules):
        """Recursively normalize rules to ensure consistent structure at all levels."""
        if not isinstance(rules, list):
            return rules

        normalized_rules = []
        for rule in rules:
            if isinstance(rule, dict):
                if "rules" in rule and isinstance(rule["rules"], list):
                    # This is a complex rule, normalize its nested rules first
                    normalized_nested = self._normalize_rules_recursively(rule["rules"])
                    rule = rule.copy()
                    rule["rules"] = normalized_nested
                normalized_rules.append(rule)
            else:
                normalized_rules.append(rule)

        # Check if we have mixed rule types at this level
        has_simple_rules = any("condition" not in rule for rule in normalized_rules)
        has_complex_rules = any("condition" in rule for rule in normalized_rules)

        if has_simple_rules and has_complex_rules:
            # Wrap all simple field rules in proper structure
            final_rules = []
            for rule in normalized_rules:
                if "condition" not in rule:
                    # This is a simple field rule, wrap it
                    final_rules.append(
                        {
                            "condition": "AND",
                            "rules": [rule],
                            "valid": True,
                        }
                    )
                else:
                    # This is already a complex rule
                    final_rules.append(rule)
            return final_rules

        return normalized_rules

    def _get_predicates_for_search_internal(self, columns):
        """
        Internal method to generate predicates for search API with proper source handling.

        This method is similar to get_predicates() but ensures that all rules
        have proper source information from the original QueryVariable.
        """
        if self.op == "&":
            # Handle AND operation
            lhs_predicates = self.lhs._get_predicates_for_search_internal(columns)
            rhs_predicates = self.rhs._get_predicates_for_search_internal(columns)

            # Combine predicates by source
            all_sources = set()
            all_rules = []

            for pred in lhs_predicates + rhs_predicates:
                all_sources.add(pred["source"])
                if len(pred["query"]["rules"]) == 1:
                    rule = pred["query"]["rules"][0].copy()
                    rule["source"] = pred["source"]
                    all_rules.append(rule)
                else:
                    # Multiple rules, keep the nested structure
                    all_rules.append(pred["query"])

            # Check if we have mixed rule types (simple field rules + complex nested rules)
            has_simple_rules = any("condition" not in rule for rule in all_rules)
            has_complex_rules = any("condition" in rule for rule in all_rules)

            if has_simple_rules and has_complex_rules:
                # Wrap all simple field rules in proper structure
                normalized_rules = []
                for rule in all_rules:
                    if "condition" not in rule:
                        # This is a simple field rule, wrap it
                        normalized_rules.append(
                            {
                                "condition": "AND",
                                "rules": [rule],
                                "valid": True,
                            }
                        )
                    else:
                        # This is already a complex rule
                        normalized_rules.append(rule)
                all_rules = normalized_rules

            # If all predicates are from the same source, we can flatten
            if len(all_sources) == 1:
                source = list(all_sources)[0]
                # Use the correct condition based on the operation
                condition = "OR" if self.op == "|" else "AND"
                # Final normalization: ensure all rules at the same level are consistent
                all_rules = self._normalize_rules_recursively(all_rules)

                return [
                    {
                        "source": source,
                        "query": {
                            "condition": condition,
                            "rules": all_rules,
                            "valid": True,
                        },
                    }
                ]
            else:
                # Multiple sources, need nested structure
                # Group rules by source and create nested structures
                source_groups = {}
                for pred in lhs_predicates + rhs_predicates:
                    source = pred["source"]
                    if source not in source_groups:
                        source_groups[source] = []
                    if len(pred["query"]["rules"]) == 1:
                        rule = pred["query"]["rules"][0].copy()
                        rule["source"] = pred["source"]
                        source_groups[source].append(rule)
                    else:
                        source_groups[source].append(pred["query"])

                # Create nested structure with one rule per source
                nested_rules = []
                for source, rules in source_groups.items():
                    if len(rules) == 1:
                        # Single rule for this source
                        nested_rules.append(rules[0])
                    else:
                        # Multiple rules for this source, wrap in AND condition
                        nested_rules.append(
                            {
                                "condition": "AND",
                                "rules": rules,
                                "valid": True,
                            }
                        )

                return [
                    {
                        "source": "nested",
                        "query": {
                            "condition": "AND",
                            "rules": nested_rules,
                            "valid": True,
                        },
                    }
                ]

        elif self.op == "|":
            # Handle OR operation
            try:
                lhs_predicates = self.lhs._get_predicates_for_search_internal(columns)
            except QueryException:
                # If left side fails (e.g., missing field), use empty predicates
                lhs_predicates = []

            try:
                rhs_predicates = self.rhs._get_predicates_for_search_internal(columns)
            except QueryException:
                # If right side fails (e.g., missing field), use empty predicates
                rhs_predicates = []

            # If both sides failed, re-raise the exception
            if not lhs_predicates and not rhs_predicates:
                raise QueryException("Both sides of OR query failed")

            # Combine predicates by source
            all_sources = set()
            all_rules = []

            for pred in lhs_predicates + rhs_predicates:
                all_sources.add(pred["source"])
                if len(pred["query"]["rules"]) == 1:
                    rule = pred["query"]["rules"][0].copy()
                    rule["source"] = pred["source"]
                    all_rules.append(rule)
                else:
                    # Multiple rules, keep the nested structure
                    all_rules.append(pred["query"])

            # Check if we have mixed rule types (simple field rules + complex nested rules)
            has_simple_rules = any("condition" not in rule for rule in all_rules)
            has_complex_rules = any("condition" in rule for rule in all_rules)

            if has_simple_rules and has_complex_rules:
                # Wrap all simple field rules in proper structure
                normalized_rules = []
                for rule in all_rules:
                    if "condition" not in rule:
                        # This is a simple field rule, wrap it
                        normalized_rules.append(
                            {
                                "condition": "AND",
                                "rules": [rule],
                                "valid": True,
                            }
                        )
                    else:
                        # This is already a complex rule
                        normalized_rules.append(rule)
                all_rules = normalized_rules

            # If all predicates are from the same source, we can flatten
            if len(all_sources) == 1:
                source = list(all_sources)[0]
                # Use the correct condition based on the operation
                condition = "OR" if self.op == "|" else "AND"
                # Final normalization: ensure all rules at the same level are consistent
                all_rules = self._normalize_rules_recursively(all_rules)

                return [
                    {
                        "source": source,
                        "query": {
                            "condition": condition,
                            "rules": all_rules,
                            "valid": True,
                        },
                    }
                ]
            else:
                # Multiple sources, need nested structure
                # Group rules by source and create nested structures
                source_groups = {}
                for pred in lhs_predicates + rhs_predicates:
                    source = pred["source"]
                    if source not in source_groups:
                        source_groups[source] = []
                    if len(pred["query"]["rules"]) == 1:
                        rule = pred["query"]["rules"][0].copy()
                        rule["source"] = pred["source"]
                        source_groups[source].append(rule)
                    else:
                        source_groups[source].append(pred["query"])

                # Create nested structure with one rule per source
                nested_rules = []
                for source, rules in source_groups.items():
                    if len(rules) == 1:
                        # Single rule for this source
                        nested_rules.append(rules[0])
                    else:
                        # Multiple rules for this source, wrap in OR condition
                        nested_rules.append(
                            {
                                "condition": "OR",
                                "rules": rules,
                                "valid": True,
                            }
                        )

                # Final normalization: ensure all rules at the same level are consistent
                nested_rules = self._normalize_rules_recursively(nested_rules)

                return [
                    {
                        "source": "nested",
                        "query": {
                            "condition": "OR",
                            "rules": nested_rules,
                            "valid": True,
                        },
                    }
                ]
        else:
            # Handle single expression (leaf node)
            qtype = self._get_qtype(columns)
            self._verify_qtype(qtype)

            predicate = {
                "source": self.lhs.source,  # Use the QueryVariable's source
                "query": {
                    "condition": "AND",
                    "rules": [
                        {
                            "id": self.lhs.name,
                            "field": self.lhs.name,
                            "type": qtype,
                            "operator": self.op,
                            "value": self.rhs,
                            "source": self.lhs.source,  # Add source to the rule
                        }
                    ],
                    "valid": True,
                },
            }

            return [predicate]


class QueryVariable(object):
    def __init__(self, name, qtype=None):
        self.name = name
        self.qtype = qtype

    def __bool__(self):
        # For Python 3:
        raise TypeError("can't use logical operators on a QueryVariable")

    def __nonzero__(self):
        # For Python 2:
        raise TypeError("can't use logical operators on a QueryVariable")

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)

    def __contains__(self, rhs):
        raise ValueError("can't use 'in' operator in queries; use X.contains(Y)")

    def contains(self, rhs):
        if not isinstance(rhs, str):
            raise ValueError(
                "QueryVariable.contains(X) requires that X be a string type"
            )
        return QueryExpression(self, "contains", rhs)

    def between(self, low, high):
        if not isinstance(low, numbers.Number) or not isinstance(high, numbers.Number):
            raise ValueError(
                "QueryVariable.between(low, high) requires that low and high be numbers"
            )
        return QueryExpression(self, "between", [str(low), str(high)])

    def startswith(self, rhs):
        if not isinstance(rhs, str):
            raise ValueError(
                "QueryVariable.startswith(X) requires that X be a string type"
            )
        return QueryExpression(self, "begins_with", rhs)

    def endswith(self, rhs):
        if not isinstance(rhs, str):
            raise ValueError(
                "QueryVariable.endswith(X) requires that X be a string type"
            )
        return QueryExpression(self, "ends_with", rhs)

    def __eq__(self, rhs):
        if rhs is None:
            return QueryExpression(self, "is_null", None)
        elif rhs == "":
            return QueryExpression(self, "is_empty", None)
        elif rhs is True:
            return QueryExpression(self, "equal", 1)
        elif rhs is False:
            return QueryExpression(self, "equal", 0)
        else:
            return QueryExpression(self, "equal", rhs)

    def __ne__(self, rhs):
        if rhs is None:
            return QueryExpression(self, "is_not_null", None)
        elif rhs == "":
            return QueryExpression(self, "is_not_empty", None)
        elif rhs is True:
            return QueryExpression(self, "not_equal", 1)
        elif rhs is False:
            return QueryExpression(self, "not_equal", 0)
        else:
            return QueryExpression(self, "not_equal", rhs)

    def __lt__(self, rhs):
        return QueryExpression(self, "less", rhs)

    def __le__(self, rhs):
        return QueryExpression(self, "less_or_equal", rhs)

    def __gt__(self, rhs):
        return QueryExpression(self, "greater", rhs)

    def __ge__(self, rhs):
        return QueryExpression(self, "greater_or_equal", rhs)


class Metric(QueryVariable):
    """
    Create a QueryVariable for querying metrics.

    Args:
        name: String, name of the log_metric() item

    Returns: a `QueryVariable` to be used with `API.query()`
        to match the experiments

    Examples:

    ```python
    >>> from comet_ml.api import API, Metric
    >>> api = API()
    >>> api.query("workspace", "project", Metric("accuracy") > 0.9)
    ```

    Note: you must always use a query operator with a `QueryVariable`,
        such as `==`, `<`, or `QueryVariable.contains("substring")`
    """

    source = "metrics"


class Parameter(QueryVariable):
    """
    Create a QueryVariable for querying parameters.

    Args:
        name: String, name of the log_parameter() item

    Returns: a `QueryVariable` to be used with `API.query()`
        to match the experiments

    Examples:

    ```python
    >>> from comet_ml.api import API, Parameter
    >>> api = API()
    >>> api.query("workspace", "project", Parameter("learning rate") >= 1.2)
    ```

    Note: you must always use a query operator with a `QueryVariable`,
        such as `==`, `<`, or `QueryVariable.contains("substring")`
    """

    source = "params"


class Metadata(QueryVariable):
    """
    Create a QueryVariable for querying metadata.

    Args:
        name: String, name of the metadata item

    Returns: a `QueryVariable` to be used with `API.query()`
        to match the experiments

    Examples:

    ```python
    >>> from comet_ml.api import API, Metadata
    >>> api = API()
    >>> api.query("workspace", "project", Metadata("name") == "value")
    ```

    Note: you must always use a query operator with a `QueryVariable`,
        such as `==`, `<`, or `QueryVariable.contains("substring")`
    """

    source = "metadata"


class Environment(QueryVariable):
    """
    Create a QueryVariable for querying environment details.

    Args:
        name: String, name of the environment item

    Returns: a `QueryVariable` to be used with `API.query()`
        to match the experiments

    Examples:

    ```python
    >>> from comet_ml.api import API, Environment
    >>> api = API()
    >>> api.query("workspace", "project", Environment("os") == "darwin")
    ```

    Note: you must always use a query operator with a `QueryVariable`,
        such as `==`, `<`, or `QueryVariable.contains("substring")`
    """

    source = "env_details"


class Other(QueryVariable):
    """
    Create a QueryVariable for querying logged-others.

    Args:
        name: String, name of the log_other() item

    Returns: a `QueryVariable` to be used with `API.query()`
        to match the experiments

    Examples:

    ```python
    >>> from comet_ml.api import API, Other
    >>> api = API()
    >>> api.query("workspace", "project", Other("other name") == "value")
    ```

    Note: you must always use a query operator with a `QueryVariable`,
        such as `==`, `<`, or `QueryVariable.contains("substring")`
    """

    source = "log_other"


class _Tag(QueryVariable):
    source = "tag"

    def __repr__(self):
        return "Tag(%r)" % (self.name,)


class Tag(QueryExpression):
    """
    Create a QueryExpression for querying tags.

    Args:
        name: String, name of tag

    Returns: a `QueryExpression` to be used with `API.query()`
        to match the experiments with this tag

    Examples:

    ```python
    >>> from comet_ml.api import API, Tag
    >>> api = API()
    >>> api.query("workspace", "project", Tag("tag name"))
    ```

    Note: if used on a project that does not contain any items
        with this tag, then a warning will appear and no items
        will match.
    """

    def __init__(self, name):
        self.lhs = _Tag(name, qtype="string")
        self.op = "equal"
        self.rhs = name

    def __repr__(self):
        return "Tag(%r)" % (self.rhs,)
