import marshmallow as ma

from .data_type import Schema, data_type, data_type_schema


class MappingExpression(ma.Schema):
    """
    The MappingExpression document type contains information about a mapping
    expression, including the input, match, output, and flags used to process
    this expression.
    """

    source = ma.fields.String(
        metadata={
            "description": (
                "A string comprised of text plus identity set data field names"
                " surrounded by curly brackets `{}` which are interpolated into the"
                " text."
            )
        }
    )
    match = ma.fields.String(
        metadata={
            "description": (
                "An expression which is applied to the output performing"
                " interpolation on source for determining if this mapping applies."
                " This requires a full string match on the source."
            )
        }
    )
    ignore_case = ma.fields.Boolean(
        metadata={
            "description": (
                "Flag indicating the match should be executed as a case insensitive"
                " comparison. If not present, this defaults to false."
            )
        }
    )
    literal = ma.fields.Boolean(
        metadata={
            "description": (
                "Flag indicating the match expression should be done as a literal"
                " match, ignoring any special regular characters. If not present,"
                " this defaults to false."
            )
        }
    )
    output = ma.fields.String(
        metadata={
            "description": (
                "A string representing the result of the mapping if the match"
                " succeeded. References to the original identity_set data can be"
                " interpolated as in the *source* property.  References to match"
                " groups from the *match* property can be interpolated with numbers"
                " (indices starting with 0) surrounded by curly brackets `{}`."
            )
        }
    )


@data_type("expression_identity_mapping#1.0.0", schema_base_name="IdentityMapping")
class ExpressionIdentityMapping_1_0_0(Schema):
    __doc__ = """
    The ExpressionIdentityMapping defines a set of identity mapping expressions
    to map Globus Auth identity data to a connector-specific list of account
    names.
    """

    mappings = ma.fields.List(
        ma.fields.Nested(MappingExpression),
        metadata={"description": "Array of expression-based identity mapping values"},
    )


# We use IdentityMapping in the storage gateway schema like an ordinary
# DATA_TYPE schema, but this one is a bit different since it has disjoint
# data types, in this case, we provide more insight in the docstring and
# choose the desired DATA_TYPE from the object we're serializing
IdentityMapping = data_type_schema.IdentityMapping
IdentityMapping.__doc__ = """
    Globus Connect Server provides two ways for you to implement a custom
    Globus identity to account mapping: expression-based and external program

    With expression-based mapping you can write rules that extract data from
    fields in the Globus identity document to form storage gateway-specific
    usernames. If there is a regular relationship between most of your users'
    Identity information to their account names, this is probably the most
    direct way to accomplish the mapping.

    With external program mappings you can use any mechanism you like (static
    mapping, ldap, database, etc) to look up account information and return the
    mapped account user name. If you have an account system that has usernames
    without a simple relationship to your users' Globus identities, or that
    requires interfacing with an accounting system, this may be necessary.
"""


def __get_identity_mapping_object_type(obj):
    return ma.utils.get_value(obj, "DATA_TYPE")


IdentityMapping.get_obj_type = __get_identity_mapping_object_type
