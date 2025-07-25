__all__ = [
    'json_schema',

    'Encoder',
    'TypeEncoder',

    'ModifierEncoder',
    'AnyEncoder',
    'StringEncoder',
    'NumberEncoder',
    'BooleanEncoder',
    'DateTimeEncoder',
    'DateEncoder',
    'TimeEncoder',
    'ListEncoder',
    'TupleEncoder',
    'ObjectEncoder',
    'DictEncoder',
    'OneOfEncoder',
    'ConstantEncoder',
]

import lollipop.type_registry as lr
import lollipop.types as lt
import lollipop.validators as lv
from lollipop.utils import identity, is_mapping

from collections import OrderedDict
from .compat import itervalues, iteritems
import re


def find_validators(schema, validator_type):
    return [validator
            for validator in schema.validators
            if isinstance(validator, validator_type)]


class Definition(object):
    def __init__(self, name):
        self.name = name
        self.jsonschema = None


def _sanitize_name(name):
    valid_chars_name = re.sub('[^a-zA-Z0-9-_]+', ' ', name).strip()
    camel_cased_name = re.sub('[_ ]+([a-z])', lambda m: m.group(1).upper(),
                              valid_chars_name)
    return camel_cased_name


def has_modifier(schema, modifier):
    while isinstance(schema, (lt.Modifier, lr.TypeRef)):
        if isinstance(schema, modifier):
            return True
        schema = schema.inner_type
    return False


def is_optional(schema):
    return has_modifier(schema, lt.Optional)


class TypeEncoder(object):
    schema_type = object

    def match(self, schema):
        return isinstance(schema, self.schema_type)

    def json_schema(self, encoder, schema):
        js = OrderedDict()
        if schema.name:
            js['title'] = schema.name
        if schema.description:
            js['description'] = schema.description

        any_of_validators = find_validators(schema, lv.AnyOf)
        if any_of_validators:
            choices = set(any_of_validators[0].choices)
            for validator in any_of_validators[1:]:
                choices = choices.intersection(set(validator.choices))

            if not choices:
                raise ValueError('AnyOf constraints choices does not allow any values')

            js['enum'] = list(schema.dump(choice) for choice in sorted(choices))

        none_of_validators = find_validators(schema, lv.NoneOf)
        if none_of_validators:
            choices = set(none_of_validators[0].values)
            for validator in none_of_validators[1:]:
                choices = choices.union(set(validator.values))

            if choices:
                js['not'] = {'enum': list(
                    schema.dump(choice) for choice in sorted(choices))}

        return js


def is_dump_schema(schema):
    return not has_modifier(schema, lt.LoadOnly)


def is_load_schema(schema):
    return not has_modifier(schema, lt.DumpOnly)


class ModifierEncoder(TypeEncoder):
    schema_type = lt.Modifier

    def json_schema(self, encoder, schema):
        inner_schema = encoder.json_schema(schema.inner_type)

        if inner_schema is None:
            return None

        if isinstance(schema, lt.Optional):
            default = schema.load_default()

            if default not in [None, lt.MISSING]:
                default = schema.inner_type.dump(default)

            js = {
                'anyOf': [
                    inner_schema,
                    {
                        'type': 'null',
                    }
                ],
            }

            if default is not lt.MISSING:
                js['default'] = default

        elif encoder.mode and (
                (encoder.mode == 'dump' and not is_dump_schema(schema)) or
                (encoder.mode == 'load' and not is_load_schema(schema))
        ):
            return None
        else:
            js = inner_schema

        return js


class AnyEncoder(TypeEncoder):
    schema_type = lt.Any


class StringEncoder(TypeEncoder):
    schema_type = lt.String

    def json_schema(self, encoder, schema):
        js = super(StringEncoder, self).json_schema(encoder, schema)

        js['type'] = 'string'

        length_validators = find_validators(schema, lv.Length)
        if length_validators:
            exact_values = [
                v.exact for v in length_validators if v.exact is not None
            ]

            min_values = (
                [v.min for v in length_validators if v.min is not None]
                + exact_values
            )
            if min_values:
                js['minLength'] = max(min_values)

            max_values = (
                [v.max for v in length_validators if v.max is not None]
                + exact_values
            )
            if max_values:
                js['maxLength'] = min(max_values)

        regexp_validators = find_validators(schema, lv.Regexp)
        if regexp_validators:
            js['pattern'] = regexp_validators[0].regexp.pattern

        return js


class NumberEncoder(TypeEncoder):
    schema_type = lt.Number

    def json_schema(self, encoder, schema):
        js = super(NumberEncoder, self).json_schema(encoder, schema)

        if isinstance(schema, lt.Integer):
            js['type'] = 'integer'
        else:
            js['type'] = 'number'

        range_validators = find_validators(schema, lv.Range)
        if range_validators:
            min_values = [v.min for v in range_validators if v.min is not None]
            if min_values:
                js['minimum'] = max(min_values)

            max_values = [v.max for v in range_validators if v.max is not None]
            if max_values:
                js['maximum'] = min(max_values)

        return js


class BooleanEncoder(TypeEncoder):
    schema_type = lt.Boolean

    def json_schema(self, encoder, schema):
        js = super(BooleanEncoder, self).json_schema(encoder, schema)
        js['type'] = 'boolean'
        return js


class DateTimeEncoder(TypeEncoder):
    schema_type = lt.DateTime

    def json_schema(self, encoder, schema):
        js = super(DateTimeEncoder, self).json_schema(encoder, schema)

        js['type'] = 'string'
        js['format'] = 'date-time'

        return js


class DateEncoder(TypeEncoder):
    schema_type = lt.Date

    def json_schema(self, encoder, schema):
        js = super(DateEncoder, self).json_schema(encoder, schema)

        js['type'] = 'string'
        js['format'] = 'date'

        return js


class TimeEncoder(TypeEncoder):
    schema_type = lt.Time

    def json_schema(self, encoder, schema):
        js = super(TimeEncoder, self).json_schema(encoder, schema)

        js['type'] = 'string'
        js['format'] = 'time'

        return js


class ListEncoder(TypeEncoder):
    schema_type = lt.List

    def json_schema(self, encoder, schema):
        js = super(ListEncoder, self).json_schema(encoder, schema)

        js['type'] = 'array'
        item_schema = encoder.json_schema(schema.item_type)
        if item_schema is None:
            js['maxItems'] = 0
        else:
            js['items'] = item_schema
            length_validators = find_validators(schema, lv.Length)
            if length_validators:
                exact_values = [
                    v.exact for v in length_validators if v.exact is not None
                ]

                min_values = (
                    [v.min for v in length_validators if v.min is not None]
                    + exact_values
                )
                if min_values:
                    js['minItems'] = max(min_values)

                max_values = (
                    [v.max for v in length_validators if v.max is not None]
                    + exact_values
                )
                if max_values:
                    js['maxItems'] = min(max_values)

            unique_validators = find_validators(schema, lv.Unique)
            if unique_validators and any(v.key is identity for v in unique_validators):
                js['uniqueItems'] = True

        return js


class TupleEncoder(TypeEncoder):
    schema_type = lt.Tuple

    def json_schema(self, encoder, schema):
        js = super(TupleEncoder, self).json_schema(encoder, schema)

        js['type'] = 'array'
        items_schema = [
            item_schema
            for item_type in schema.item_types
            for item_schema in [encoder.json_schema(item_type)]
            if item_schema is not None
        ]
        if not items_schema:
            js['maxItems'] = 0
        else:
            # modern JSON Schema standard prescribes to use "prefixItems" for
            # tuples, not "items", see
            # https://json-schema.org/understanding-json-schema/reference/array
            js['prefixItems'] = items_schema
            js['minItems'] = len(items_schema)
            js['maxItems'] = len(items_schema)
            js['items'] = False

        return js


def is_type(schema, schema_type):
    while isinstance(schema, (lt.Modifier, lr.TypeRef)):
        schema = schema.inner_type
    return isinstance(schema, schema_type)


class ObjectEncoder(TypeEncoder):
    schema_type = lt.Object

    def json_schema(self, encoder, schema):
        js = super(ObjectEncoder, self).json_schema(encoder, schema)

        js['type'] = 'object'
        properties = OrderedDict(
            (field_name, field_schema)
            for field_name, field in iteritems(schema.fields)
            for field_schema in [encoder.json_schema(field.field_type)]
            if field_schema is not None
        )
        if properties:
            js['properties'] = properties

            required = [
                field_name
                for field_name, field in sorted(iteritems(schema.fields))
                if not is_optional(field.field_type) and field_name in js['properties']
            ]
            if required:
                js['required'] = required

        if schema.allow_extra_fields in [True, False]:
            js['additionalProperties'] = schema.allow_extra_fields
        elif isinstance(schema.allow_extra_fields, lt.Field):
            field_type = schema.allow_extra_fields.field_type
            field_schema = encoder.json_schema(field_type)
            if field_schema is not None:
                if is_type(field_type, lt.Any):
                    js['additionalProperties'] = True
                else:
                    js['additionalProperties'] = field_schema

        if not js.get('properties') and not js.get('additionalProperties'):
            js['maxProperties'] = 0

        return js


class DictEncoder(TypeEncoder):
    schema_type = lt.Dict

    def json_schema(self, encoder, schema):
        js = super(DictEncoder, self).json_schema(encoder, schema)

        js['type'] = 'object'
        properties = OrderedDict(
            (k, value_schema)
            for k, v in iteritems(schema.value_types)
            for value_schema in [encoder.json_schema(v)]
            if value_schema is not None
        )
        if properties:
            js['properties'] = properties
        required = [
            k
            for k, v in sorted(iteritems(schema.value_types))
            if not is_optional(v) and k in properties
        ]
        if required:
            js['required'] = required
        if hasattr(schema.value_types, 'default'):
            additional_schema = encoder.json_schema(schema.value_types.default)
            if additional_schema is not None:
                js['additionalProperties'] = additional_schema

        if not js.get('properties') and not js.get('additionalProperties'):
            js['maxProperties'] = 0

        return js


class OneOfEncoder(TypeEncoder):
    schema_type = lt.OneOf

    def json_schema(self, encoder, schema):
        js = super(OneOfEncoder, self).json_schema(encoder, schema)

        types = itervalues(schema.types) \
            if is_mapping(schema.types) else schema.types
        js['anyOf'] = [
            variant_schema
            for variant in types
            for variant_schema in [encoder.json_schema(variant)]
            if variant_schema is not None
        ]
        if not js['anyOf']:
            return None

        return js


class ConstantEncoder(TypeEncoder):
    schema_type = lt.Constant

    def json_schema(self, encoder, schema):
        js = super(ConstantEncoder, self).json_schema(encoder, schema)
        js['const'] = schema.value
        return js


class SchemaUsageCounter(object):
    def __init__(self, type_encoders, mode=None):
        self._type_encoders = type_encoders
        self.mode = mode
        self.counts = {}

    def json_schema(self, schema, force_render=False):
        if isinstance(schema, lr.TypeRef):
            schema = schema.inner_type

        schema_key = (schema, self.mode)

        if schema_key in self.counts:
            self.counts[schema_key] += 1
            return

        self.counts[schema_key] = 1

        for type_encoder in self._type_encoders:
            if type_encoder.match(schema):
                type_encoder.json_schema(self, schema)
                break


class JsonSchemaGenerator(object):
    def __init__(self, type_encoders, definitions=None, mode=None):
        self.type_encoders = type_encoders
        self.definitions = definitions
        self.mode = mode

    def json_schema(self, schema, force_render=False):
        if isinstance(schema, lr.TypeRef):
            schema = schema.inner_type

        schema_key = (schema, self.mode)
        if schema_key in self.definitions and not force_render:
            return {'$ref': '#/components/schemas/' + self.definitions[schema_key].name}

        js = None
        for type_encoder in self.type_encoders:
            if type_encoder.match(schema):
                js = type_encoder.json_schema(self, schema)
                break

        return js


class Encoder(object):
    def __init__(self):
        self._encoders = []

        self.add_encoder(ModifierEncoder())
        self.add_encoder(AnyEncoder())
        self.add_encoder(StringEncoder())
        self.add_encoder(NumberEncoder())
        self.add_encoder(BooleanEncoder())
        self.add_encoder(DateTimeEncoder())
        self.add_encoder(DateEncoder())
        self.add_encoder(TimeEncoder())
        self.add_encoder(ListEncoder())
        self.add_encoder(TupleEncoder())
        self.add_encoder(ObjectEncoder())
        self.add_encoder(DictEncoder())
        self.add_encoder(OneOfEncoder())
        self.add_encoder(ConstantEncoder())

    def add_encoder(self, encoder):
        self._encoders.insert(0, encoder)

    def json_schema(self, schema, definitions=None, mode=None):
        """Convert Lollipop schema to JSON schema."""
        is_top_level_schema = definitions is None
        if definitions is None:
            definitions = {}

        definition_names = {definition.name
                            for definition in itervalues(definitions)}

        counter = SchemaUsageCounter(self._encoders, mode=mode)
        counter.json_schema(schema)
        counts = counter.counts

        mode_suffix = '_' + mode if mode else ''

        for schema_key, count in iteritems(counts):
            if count == 1:
                continue

            schema1, mode = schema_key
            if schema_key not in definitions:
                def_name = schema1.name or 'Type'
                def_name += mode_suffix
                def_name = _sanitize_name(def_name)

                if def_name in definition_names:
                    i = 1
                    while def_name + str(i) in definition_names:
                        i += 1
                    def_name += str(i)

                definitions[schema_key] = Definition(def_name)
                definition_names.add(def_name)

        generator = JsonSchemaGenerator(self._encoders, definitions=definitions, mode=mode)

        for schema_key, definition in iteritems(definitions):
            if definition.jsonschema is not None:
                continue

            schema1, mode = schema_key

            definitions[schema_key].jsonschema = generator.json_schema(
                schema1, force_render=True,
            )

        js = generator.json_schema(schema)
        if is_top_level_schema and definitions:
            components_obj = js.setdefault('components', {})
            schemas_obj = components_obj.setdefault('schemas', {})
            schemas_obj.update({
                definition.name: definition.jsonschema
                for definition in itervalues(definitions)
            })

        return js


_DEFAULT_ENCODER = Encoder()
json_schema = _DEFAULT_ENCODER.json_schema
