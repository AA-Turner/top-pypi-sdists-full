"""
This module implements a mapping algorithm to transform an Identity resource
from Globus Auth to a username which is meaningful in the context of the
Connector that is associated with the Storage Gateway where mapping is being
performed.

The input mapping_data consists of a list of mappings, which are passed in
as a dicts containing the following fields:

*   source: A source expression that contains a string which may include
    interpolations from properties of the Identity resource being
    evaluated.
*   match: A match expression to compare against the source. This
    expression supports a limited regular expression syntax which is
    applied to the source string.
*   output: An output expression which can contain references to properties
    of the input Identity resource or references to parenthesized
    subexpressions from applying the match expression to the source.
*   ignore_case: A boolean flag controlling whether to perform a case
    insensitive match. The default is False.
*   literal: A boolean flag whether to interpet the match expression
    literally, or to use the regular expression language defined below when
    determining whether a match succeeds. If this is set to True,
    references to match subexpressions may not be used in the output field.

Match Expression Language
-------------------------

When the literal flag is not present, the match value is interpreted using
a reduced version of the POSIX extended regular expression, including
special processing for the following tokens:

* :code:`.` any single character match
* :code:`?` for zero or one of the preceding match
* :code:`*` for zero or more of the preceding match
* :code:`|` for alternative match branches
* :code:`()` to group a match and created a numbered submatch for output
  interpolation
* `\\` to escape any of the above, `\\`, or :code:`"` from special
  processing

Any other string in the match expression is matched literally

Identity Data Interpolation
---------------------------

The source and output strings may include values that are interpolated from
a Globus auth identity resource, as described in the
`Globus Auth documentation
<https://docs.globus.org/api/auth/reference/#_identity_resource>`_.

Interpolations are indicated by surrounding the resource property with curly
braces. For example, to interpolate the username property of the identity
resource in the source string, one uses the value :code:`{username}`; likewise,
to interpolate the id property, one uses the string :code:`{id}`. Multiple
values may be interpolated into either the source or output strings.

Subexpression Interpolation
---------------------------

The output string may also contain references to subexpression matches which
are also interpolated into the output. The matching is down by using a similar
syntax the Identity Data Interpolation above, but using integer values to
reference matched subexpression, with indices starting at 0. For example, using
a match expression :code:`(.*)@example\\.org`, one can interpolate the part
before the :code:`@` symbol my using the string :code:`{0}` in the output
expression.

Examples
--------

To match username against a given domain, and return the username as the
output expression:

.. code-block:: json

    {
        "source": "{username}",
        "match": "(.*)@example\\.org",
        "output": "{0}"
    }

To match an identity ID and map to a particular user account

.. code-block:: json

    {
        "source": "{id}",
        "match": "b34bb069-3b68-4d38-b4e6-bc1e4fc95332",
        "output": "application_account"
    }

To rewrite an identity from one domain to another:

.. code-block: json

    {
        "source": "{username}",
        "match": "(.*)@example\\.edu"
        "output": "{0}@data.example.edu"
    }

To map a set of identities to a common account:

.. code-block: json

    {
        "source": "{username}",
        "match": "(alice|bob)@example\\.org",
        "output": "globus"
    }
"""

from __future__ import annotations

import re
import typing as t

from typing_extensions import Self

from ..errors import IdentityMappingError, InvalidMappingError
from ..schema import IdentityMappingConfiguration
from .abstract import IdentityMapping


class ExpressionIdentityMappingDict(t.TypedDict, total=False):
    source: str
    match: str
    output: str
    literal: bool
    ignore_case: bool


class CompiledExpressionIdentityMappingDict(t.TypedDict, total=False):
    source: str
    match: str
    output: str
    literal: bool
    ignore_case: bool
    compiled_match: t.Pattern


class ExpressionMappingDocument(IdentityMappingConfiguration):
    mappings: list[ExpressionIdentityMappingDict]


class ExpressionIdentityMapping(IdentityMapping):
    """
    The ExpressionIdentityMapping class implements a mapping algorithm to
    transform an Identity resource from Globus Auth to a username which is
    meaningful in the context of the Connector that is associated with the
    Storage Gateway mapping is being performed on.
    """

    DATA_TYPE = "expression_identity_mapping#1.0.0"

    def __init__(
        self,
        mapping_data: t.Iterable[ExpressionIdentityMappingDict],
        storage_gateway: str | None = None,
        connector: str | None = None,
    ) -> None:
        """
        :param list[ExpressionIdentityMappingDict] mapping_data:
            Identity mapping definitions as described in the API documentation.
        :param str storage_gateway:
            The storage gateway that the mapping will be performed for. This is
            not used in this module
        :param str connector:
            The connector uuid that the mapping will be performed for. This is
            not used in this module
        """
        self.mappings: list[CompiledExpressionIdentityMappingDict] = []
        self.connector = connector
        self.storage_gateway = storage_gateway

        for m in mapping_data:
            mapping: CompiledExpressionIdentityMappingDict = {
                "source": m["source"],
                "compiled_match": self._compile_match(
                    m["match"],
                    m.get("ignore_case", False),
                    m.get("literal", False),
                ),
                "match": m["match"],
                "output": m["output"],
            }
            if "ignore_case" in m:
                mapping["ignore_case"] = m["ignore_case"]
            if "literal" in m:
                mapping["literal"] = m["literal"]
            self.mappings.append(mapping)
        self._init_mappings = mapping_data

    def __repr__(self) -> str:
        args = ", ".join(map(str, self._init_mappings))
        sg = f"'{self.storage_gateway}'" if self.storage_gateway else "None"
        conn = f"'{self.connector}'" if self.connector else "None"
        return f"{type(self).__name__}([{args}], {sg}, {conn})"

    @classmethod
    def _from_mapping_document(
        cls,
        mapping_document: ExpressionMappingDocument,
        connector: str | None = None,
        storage_gateway: str | None = None,
    ) -> Self:
        return cls(
            mapping_document["mappings"],
            connector=connector,
            storage_gateway=storage_gateway,
        )

    @staticmethod
    def _compile_match(
        match: str, ignore_case: bool = False, literal: bool = False
    ) -> t.Pattern:
        original_match = match
        if not literal:
            bad_escape = re.search(r"(\\[^.?*|()\\0-9])", match)
            if bad_escape:
                raise InvalidMappingError(
                    f"{match} - Invalid \\ expression: {bad_escape.group()}"
                )
            unsupported_re = re.search(r"([*?]\?)", match)
            if unsupported_re:
                raise InvalidMappingError(
                    f"{match} - Invalid ? expression: {unsupported_re.group()}"
                )
            leading_wildcard_re = re.search(r"^([*?])", match)
            if leading_wildcard_re:
                _g = leading_wildcard_re.group()
                raise InvalidMappingError(
                    f"{match} - Invalid leading wildcard expression: {_g}"
                )

            # Escape python regex specials that we don't support
            match = re.sub(r"(?<!\\)([\^\$\+\{\}\[\]])", r"\\\1", match)
        else:
            match = re.sub(r"(?<!\\)([\^\?\*\|\(\)\\\$\+\.\{\}\[\]])", r"\\\1", match)
            match = re.sub(r"(\\[0-9])", r"\\\1", match)

        try:
            return re.compile("^" + match + "$", re.I if ignore_case else 0)
        except Exception as e:
            raise InvalidMappingError("Invalid mapping {}: {}", original_match, str(e))

    @staticmethod
    def _interpolate(
        string: str, identity_data: t.Mapping[str, str], matches: list | None = None
    ) -> str:
        if not matches:
            matches = []
        interpolated = string

        for m in re.finditer(r"(?<!\\)(\\\\)*({([^}]*)})", string):
            subexp, subname = m.groups()[1:]
            try:
                matchref = int(subname)
                if matchref >= len(matches):
                    raise IdentityMappingError(f"Invalid reference to {matchref}")
                repl = matches[matchref]
            except ValueError:
                repl = identity_data.get(subname, None)
            if repl is None:
                raise IdentityMappingError(f"Missing identity property {subname}")
            interpolated = interpolated.replace(subexp, repl)
        return interpolated

    def map_identity(self, identity_data: t.Mapping[str, str]) -> str | None:
        """
        Applies the defined mapping (e.g., as defined via
        `.from_mapping_document()`) to `identity_data`, and, if successful,
        returns the interpolated output string of the first match.  If no
        mapping matches, returns `None`.
        """
        for m in self.mappings:
            source = self._interpolate(m["source"], identity_data)
            mr = m["compiled_match"].match(source)
            if mr:
                return self._interpolate(m["output"], identity_data, list(mr.groups()))
        return None

    def map_identities(
        self, identity_data: t.Iterable[t.Mapping[str, str]]
    ) -> list[dict[str, list[str]]]:
        """
        Applies each defined mapping -- in order -- to each identity resource
        in `identity_data`.  Matches are included in the result.  Each item in
        the returned list is a dictionary mapping the id of an identity to a
        list of successfully mapped values.

        In pseudocode:

            for mapping in mappings:
                for identity in identity_data:
                    if mapping matches identity:
                        add to output
        """
        results = []
        for m in self.mappings:
            m_re = m["compiled_match"]
            m_output = m["output"]
            mapping_results: dict[str, list[str]] = {}
            for rec in identity_data:
                if rec.get("status") not in ("used", "private"):
                    continue

                source = self._interpolate(m["source"], rec)
                mr = m_re.match(source)
                if mr:
                    identity_id = rec["id"]
                    if identity_id not in mapping_results:
                        mapping_results[identity_id] = []
                    mapping_results[identity_id].append(
                        self._interpolate(m_output, rec, list(mr.groups()))
                    )
            results.append(mapping_results)
        return results
