import lollipop.type_registry as lr
import lollipop.types as lt
import lollipop.validators as lv
from lollipop.utils import is_mapping, DictWithDefault
from lollipop_jsonschema import json_schema, TypeEncoder, Encoder
import pytest
from collections import namedtuple


def sorted_dicts(items):
    def normalize(v):
        return [(k, normalize(v)) for k, v in v.items()] if is_mapping(v) else v
    return sorted(items, key=normalize)


NULL_TYPE = {
    'type': 'null',
}


class TestJsonSchema:
    def test_string_schema(self):
        assert json_schema(lt.String()) == {'type': 'string'}

    def test_string_minLength(self):
        assert json_schema(lt.String(validate=lv.Length(min=1))) == \
            {'type': 'string', 'minLength': 1}
        assert json_schema(lt.String(validate=lv.Length(min=0))) == \
            {'type': 'string', 'minLength': 0}

    def test_string_multiple_minLength(self):
        assert json_schema(lt.String(validate=[lv.Length(min=1),
                                               lv.Length(min=3)])) == \
            {'type': 'string', 'minLength': 3}

    def test_string_maxLength(self):
        assert json_schema(lt.String(validate=lv.Length(max=10))) == \
            {'type': 'string', 'maxLength': 10}
        assert json_schema(lt.String(validate=lv.Length(max=0))) == \
            {'type': 'string', 'maxLength': 0}

    def test_string_multiple_maxLength(self):
        assert json_schema(lt.String(validate=[lv.Length(max=10),
                                               lv.Length(max=5)])) == \
            {'type': 'string', 'maxLength': 5}

    def test_string_min_and_maxLength(self):
        assert json_schema(lt.String(validate=lv.Length(min=1, max=10))) == \
            {'type': 'string', 'minLength': 1, 'maxLength': 10}
        assert json_schema(lt.String(validate=lv.Length(min=0, max=10))) == \
            {'type': 'string', 'minLength': 0, 'maxLength': 10}
        assert json_schema(lt.String(validate=lv.Length(min=-10, max=0))) == \
            {'type': 'string', 'minLength': -10, 'maxLength': 0}

    def test_string_multiple_min_and_maxLength(self):
        assert json_schema(lt.String(validate=[lv.Length(min=1, max=10),
                                               lv.Length(min=5, max=15)])) == \
            {'type': 'string', 'minLength': 5, 'maxLength': 10}

    def test_string_exact_length(self):
        assert json_schema(lt.String(validate=lv.Length(exact=5))) == \
            {'type': 'string', 'minLength': 5, 'maxLength': 5}
        assert json_schema(lt.String(validate=lv.Length(exact=0))) == \
            {'type': 'string', 'minLength': 0, 'maxLength': 0}

    def test_string_min_max_and_exact_length(self):
        assert json_schema(lt.String(validate=[lv.Length(exact=5),
                                               lv.Length(min=1),
                                               lv.Length(max=10)])) == \
            {'type': 'string', 'minLength': 5, 'maxLength': 5}

    def test_string_pattern(self):
        assert json_schema(lt.String(validate=lv.Regexp('[a-z0-9]+'))) == \
            {'type': 'string', 'pattern': '[a-z0-9]+'}

    def test_number_schema(self):
        assert json_schema(lt.Float()) == {'type': 'number'}

    def test_number_minimum(self):
        assert json_schema(lt.Float(validate=lv.Range(min=2))) == \
            {'type': 'number', 'minimum': 2}
        assert json_schema(lt.Float(validate=lv.Range(min=0))) == \
            {'type': 'number', 'minimum': 0}

    def test_number_multiple_minimum(self):
        assert json_schema(lt.Float(validate=[lv.Range(min=2),
                                              lv.Range(min=5)])) == \
            {'type': 'number', 'minimum': 5}

    def test_number_maximum(self):
        assert json_schema(lt.Float(validate=lv.Range(max=10))) == \
            {'type': 'number', 'maximum': 10}
        assert json_schema(lt.Float(validate=lv.Range(max=0))) == \
            {'type': 'number', 'maximum': 0}

    def test_number_multiple_maximum(self):
        assert json_schema(lt.Float(validate=[lv.Range(max=10),
                                              lv.Range(max=20)])) == \
            {'type': 'number', 'maximum': 10}

    def test_number_minimum_and_maximum(self):
        assert json_schema(lt.Float(validate=lv.Range(min=1, max=10))) == \
            {'type': 'number', 'minimum': 1, 'maximum': 10}
        assert json_schema(lt.Float(validate=lv.Range(min=0, max=10))) == \
            {'type': 'number', 'minimum': 0, 'maximum': 10}
        assert json_schema(lt.Float(validate=lv.Range(min=-10, max=0))) == \
            {'type': 'number', 'minimum': -10, 'maximum': 0}

    def test_number_multiple_minimum_and_maximum(self):
        assert json_schema(lt.Float(validate=[lv.Range(min=1, max=10),
                                              lv.Range(min=5, max=15)])) == \
            {'type': 'number', 'minimum': 5, 'maximum': 10}

    def test_integer_schema(self):
        assert json_schema(lt.Integer()) == {'type': 'integer'}

    def test_integer_minimum(self):
        assert json_schema(lt.Integer(validate=lv.Range(min=2))) == \
            {'type': 'integer', 'minimum': 2}
        assert json_schema(lt.Integer(validate=lv.Range(min=0))) == \
            {'type': 'integer', 'minimum': 0}

    def test_integer_multiple_minimum(self):
        assert json_schema(lt.Integer(validate=[lv.Range(min=2),
                                                lv.Range(min=5)])) == \
            {'type': 'integer', 'minimum': 5}

    def test_integer_maximum(self):
        assert json_schema(lt.Integer(validate=lv.Range(max=10))) == \
            {'type': 'integer', 'maximum': 10}
        assert json_schema(lt.Integer(validate=lv.Range(max=0))) == \
            {'type': 'integer', 'maximum': 0}

    def test_integer_multiple_maximum(self):
        assert json_schema(lt.Integer(validate=[lv.Range(max=10),
                                                lv.Range(max=20)])) == \
            {'type': 'integer', 'maximum': 10}

    def test_integer_minimum_and_maximum(self):
        assert json_schema(lt.Integer(validate=lv.Range(min=1, max=10))) == \
            {'type': 'integer', 'minimum': 1, 'maximum': 10}
        assert json_schema(lt.Integer(validate=lv.Range(min=0, max=10))) == \
            {'type': 'integer', 'minimum': 0, 'maximum': 10}
        assert json_schema(lt.Integer(validate=lv.Range(min=-10, max=0))) == \
            {'type': 'integer', 'minimum': -10, 'maximum': 0}

    def test_integer_multiple_minimum_and_maximum(self):
        assert json_schema(lt.Integer(validate=[lv.Range(min=1, max=10),
                                                lv.Range(min=5, max=15)])) == \
            {'type': 'integer', 'minimum': 5, 'maximum': 10}

    def test_boolean_schema(self):
        assert json_schema(lt.Boolean()) == {'type': 'boolean'}

    def test_list_schema(self):
        assert json_schema(lt.List(lt.String())) == \
            {'type': 'array', 'items': {'type': 'string'}}

    def test_list_minItems(self):
        assert json_schema(lt.List(lt.String(), validate=lv.Length(min=1))) == \
            {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1}
        assert json_schema(lt.List(lt.String(), validate=lv.Length(min=0))) == \
            {'type': 'array', 'items': {'type': 'string'}, 'minItems': 0}

    def test_list_multiple_minItems(self):
        assert json_schema(lt.List(lt.String(), validate=[lv.Length(min=1),
                                                          lv.Length(min=5)])) == \
            {'type': 'array', 'items': {'type': 'string'}, 'minItems': 5}

    def test_list_maxItems(self):
        assert json_schema(lt.List(lt.String(), validate=lv.Length(max=10))) == \
            {'type': 'array', 'items': {'type': 'string'}, 'maxItems': 10}
        assert json_schema(lt.List(lt.String(), validate=lv.Length(max=0))) == \
            {'type': 'array', 'items': {'type': 'string'}, 'maxItems': 0}

    def test_list_multiple_maxItems(self):
        assert json_schema(lt.List(lt.String(), validate=[lv.Length(max=10),
                                                          lv.Length(max=20)])) == \
            {'type': 'array', 'items': {'type': 'string'}, 'maxItems': 10}

    def test_list_min_and_maxItems(self):
        assert json_schema(lt.List(lt.String(),
                                   validate=lv.Length(min=1, max=10))) == \
            {'type': 'array', 'items': {'type': 'string'},
             'minItems': 1, 'maxItems': 10}
        assert json_schema(lt.List(lt.String(),
                                   validate=lv.Length(min=0, max=10))) == \
            {'type': 'array', 'items': {'type': 'string'},
             'minItems': 0, 'maxItems': 10}
        assert json_schema(lt.List(lt.String(),
                                   validate=lv.Length(min=-10, max=0))) == \
            {'type': 'array', 'items': {'type': 'string'},
             'minItems': -10, 'maxItems': 0}

    def test_list_multiple_min_and_maxItems(self):
        assert json_schema(lt.List(lt.String(),
                                   validate=[lv.Length(min=1, max=10),
                                             lv.Length(min=5, max=15)])) == \
            {'type': 'array', 'items': {'type': 'string'},
             'minItems': 5, 'maxItems': 10}

    def test_list_exact_items(self):
        assert json_schema(lt.List(lt.String(), validate=lv.Length(exact=5))) == \
            {'type': 'array', 'items': {'type': 'string'},
             'minItems': 5, 'maxItems': 5}
        assert json_schema(lt.List(lt.String(), validate=lv.Length(exact=0))) == \
            {'type': 'array', 'items': {'type': 'string'},
             'minItems': 0, 'maxItems': 0}

    def test_list_uniqueItems(self):
        assert json_schema(lt.List(lt.String(), validate=lv.Unique())) == \
            {'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True}

    def test_tuple_schema(self):
        assert json_schema(lt.Tuple([lt.String(), lt.Integer(), lt.Boolean()])) == \
            {
                'type': 'array',
                 'prefixItems': [
                    {'type': 'string'},
                    {'type': 'integer'},
                    {'type': 'boolean'},
                ],
                'items': False,
                'minItems': 3,
                'maxItems': 3,
            }

    def test_object_schema(self):
        result = json_schema(lt.Object({'foo': lt.String(), 'bar': lt.Integer()}))

        assert len(result) == 3
        assert result['type'] == 'object'
        assert result['properties'] == {
            'foo': {'type': 'string'},
            'bar': {'type': 'integer'},
        }
        assert result['required'] == sorted(['foo', 'bar'])

    def test_object_optional_fields(self):
        result = json_schema(lt.Object({'foo': lt.String(),
                                        'bar': lt.Optional(lt.Integer())}))
        assert 'bar' not in result['required']

    def test_object_optional_fields_wrapped_in_other_modifiers(self):
        result = json_schema(lt.Object({
            'foo': lt.String(),
            'bar': lt.DumpOnly(lt.Optional(lt.Integer())),
        }))
        assert 'bar' not in result['required']

    def test_object_all_optional_fields(self):
        result = json_schema(lt.Object({'foo': lt.Optional(lt.String()),
                                        'bar': lt.Optional(lt.Integer())}))
        assert 'required' not in result

    def test_object_no_allow_extra_fields(self):
        result = json_schema(lt.Object({
            'foo': lt.String(), 'bar': lt.Integer(),
        }))

        assert 'additionalProperties' not in result

    def test_object_allow_extra_fields_true(self):
        result = json_schema(lt.Object({
            'foo': lt.String(), 'bar': lt.Integer(),
        }, allow_extra_fields=True))

        assert result['additionalProperties'] is True

    def test_object_allow_extra_fields_any(self):
        result = json_schema(lt.Object({
            'foo': lt.String(), 'bar': lt.Integer(),
        }, allow_extra_fields=lt.Any()))

        assert result['additionalProperties'] is True

    def test_object_allow_extra_fields_any_with_modifiers(self):
        result = json_schema(lt.Object({
            'foo': lt.String(), 'bar': lt.Integer(),
        }, allow_extra_fields=lt.Transform(lt.Any())))

        assert result['additionalProperties'] is True

    def test_object_allow_extra_fields_false(self):
        result = json_schema(lt.Object({
            'foo': lt.String(), 'bar': lt.Integer(),
        }, allow_extra_fields=False))

        assert result['additionalProperties'] is False

    def test_object_allow_extra_fields_type(self):
        result = json_schema(lt.Object({
            'foo': lt.String(), 'bar': lt.Integer(),
        }, allow_extra_fields=lt.Object({
            'bar': lt.String(), 'foo': lt.Integer(),
        })))

        additional = result['additionalProperties']
        assert additional['type'] == 'object'
        assert additional['properties'] == {
            'foo': {'type': 'integer'},
            'bar': {'type': 'string'},
        }

    def test_fixed_fields_dict_schema(self):
        result = json_schema(lt.Dict({'foo': lt.String(), 'bar': lt.Integer()}))

        assert len(result) == 3
        assert result['type'] == 'object'
        assert result['properties'] == {
            'foo': {'type': 'string'},
            'bar': {'type': 'integer'},
        }
        assert result['required'] == sorted(['foo', 'bar'])

    def test_variadic_fields_dict_schema(self):
        result = json_schema(lt.Dict(lt.Integer()))

        assert len(result) == 2
        assert result['type'] == 'object'
        assert result['additionalProperties'] == {'type': 'integer'}

    def test_fixed_fields_dict_optional_fields(self):
        result = json_schema(lt.Dict({'foo': lt.String(),
                                      'bar': lt.Optional(lt.Integer())}))
        assert 'bar' not in result['required']

    def test_fixed_fields_dict_all_optional_fields(self):
        result = json_schema(lt.Dict({'foo': lt.Optional(lt.String()),
                                      'bar': lt.Optional(lt.Integer())}))
        assert 'required' not in result

    def test_schema_title(self):
        assert json_schema(lt.String(name='My string'))['title'] == 'My string'
        assert json_schema(lt.Integer(name='My integer'))['title'] == 'My integer'
        assert json_schema(lt.Float(name='My float'))['title'] == 'My float'
        assert json_schema(lt.Boolean(name='My boolean'))['title'] == 'My boolean'

    def test_schema_description(self):
        assert json_schema(lt.String(description='My description'))['description'] \
            == 'My description'
        assert json_schema(lt.Integer(description='My description'))['description'] \
            == 'My description'
        assert json_schema(lt.Float(description='My description'))['description'] \
            == 'My description'
        assert json_schema(lt.Boolean(description='My description'))['description'] \
            == 'My description'

    def test_type_with_any_of_validator_is_dumped_as_enum(self):
        jschema = json_schema(lt.String(validate=lv.AnyOf(['foo', 'bar', 'baz'])))
        assert len(jschema) == 2
        assert jschema['type'] == 'string'
        assert jschema['enum'] == sorted(['foo', 'bar', 'baz'])

        jschema = json_schema(lt.Integer(validate=lv.AnyOf([1, 2, 3])))
        assert len(jschema) == 2
        assert jschema['type'] == 'integer'
        assert jschema['enum'] == sorted([1, 2, 3])

    def test_type_with_any_of_validator_values_are_serialized(self):
        MyType = namedtuple('MyType', ['foo', 'bar'])

        MY_TYPE = lt.Object(
            {'foo': lt.String(), 'bar': lt.Integer()},
            validate=lv.AnyOf([MyType('hello', 1), MyType('goodbye', 2)]),
        )
        jschema = json_schema(MY_TYPE)

        assert jschema['enum'] == \
            [{'foo': 'goodbye', 'bar': 2}, {'foo': 'hello', 'bar': 1}]

    def test_type_with_multiple_any_of_validators(self):
        jschema = json_schema(
            lt.String(validate=[
                lv.AnyOf(['foo', 'bar', 'baz']),
                lv.AnyOf(['bar', 'baz', 'bam']),
            ])
        )

        assert len(jschema) == 2
        assert jschema['type'] == 'string'
        assert jschema['enum'] == sorted(['bar', 'baz'])

    def test_type_with_none_of_validator_is_dumped_as_not_enum(self):
        jschema = json_schema(lt.String(validate=lv.NoneOf(['foo', 'bar', 'baz'])))
        assert 'not' in jschema
        assert len(jschema['not']) == 1
        assert jschema['not']['enum'] == sorted(['foo', 'bar', 'baz'])

        jschema = json_schema(lt.Integer(validate=lv.NoneOf([1, 2, 3])))
        assert 'not' in jschema
        assert len(jschema['not']) == 1
        assert jschema['not']['enum'] == sorted([1, 2, 3])

    def test_type_with_none_of_validator_values_are_serialized(self):
        MyType = namedtuple('MyType', ['foo', 'bar'])

        MY_TYPE = lt.Object(
            {'foo': lt.String(), 'bar': lt.Integer()},
            validate=lv.NoneOf([MyType('hello', 1), MyType('goodbye', 2)]),
        )
        jschema = json_schema(MY_TYPE)

        assert jschema['not']['enum'] == \
            [{'foo': 'goodbye', 'bar': 2}, {'foo': 'hello', 'bar': 1}]

    def test_type_with_multiple_none_of_validators(self):
        jschema = json_schema(
            lt.String(validate=[
                lv.NoneOf(['foo', 'bar', 'baz']),
                lv.NoneOf(['bar', 'baz', 'bam']),
            ])
        )

        assert jschema['not']['enum'] == sorted(['foo', 'bar', 'baz', 'bam'])

    def test_constant(self):
        assert json_schema(lt.Constant('foo')) == {'const': 'foo'}
        assert json_schema(lt.Constant(123)) == {'const': 123}

    def test_optional_schema_is_its_inner_type_schema_with_default_annotation(self):
        assert json_schema(lt.Optional(lt.String())) == {
            'anyOf': [
                json_schema(lt.String()),
                NULL_TYPE,
            ],
            'default': None,
        }
        assert json_schema(lt.Optional(lt.Integer())) == {
            'anyOf': [
                json_schema(lt.Integer()),
                NULL_TYPE,
            ],
            'default': None
        }

    def test_optional_load_default_is_used_as_default(self):
        assert json_schema(lt.Optional(lt.String(), load_default='foo')) == {
            'anyOf': [
                json_schema(lt.String()),
                NULL_TYPE,
            ],
            'default': 'foo',
        }

    def test_optional_load_default_value_is_serialized(self):
        MyType = namedtuple('MyType', ['foo', 'bar'])

        result = json_schema(lt.Optional(lt.Object({
            'foo': lt.String(), 'bar': lt.Integer(),
        }), load_default=MyType('hello', 123)))

        assert result['default'] == {'foo': 'hello', 'bar': 123}

    def test_optional_load_default_is_skipped_if_MISSING(self):
        assert json_schema(lt.Optional(lt.String(), load_default=lt.MISSING)) == {
            'anyOf': [
                {
                    'type': 'string',
                },
                NULL_TYPE,
            ]
       }

    def test_one_of_schema_with_sequence(self):
        t1 = lt.String()
        t2 = lt.Integer()
        t3 = lt.Boolean()
        result = json_schema(lt.OneOf([t1, t2, t3]))

        assert sorted(['anyOf']) == sorted(result.keys())
        assert sorted_dicts([json_schema(t) for t in [t1, t2, t3]]) == \
            sorted_dicts(result['anyOf'])

    def test_one_of_schema_with_mapping(self):
        FOO_SCHEMA = lt.Object({'type': 'Foo', 'foo': lt.String()})
        BAR_SCHEMA = lt.Object({'type': 'Bar', 'bar': lt.Integer()})

        result = json_schema(lt.OneOf({'Foo': FOO_SCHEMA, 'Bar': BAR_SCHEMA},
                                      load_hint=lt.dict_value_hint('type'),
                                      dump_hint=lt.type_name_hint))

        assert sorted(['anyOf']) == sorted(result.keys())
        assert sorted_dicts([json_schema(FOO_SCHEMA), json_schema(BAR_SCHEMA)]) == \
            sorted_dicts(result['anyOf'])

    def test_no_definitions_if_no_duplicate_types(self):
        result = json_schema(lt.Object({'foo': lt.String(), 'bar': lt.String()}))

        assert 'definitions' not in result

    def test_duplicate_types_in_objects_are_extracted_to_definitions(self):
        type1 = lt.String(name='MyString')
        result = json_schema(lt.Object({'foo': type1, 'bar': type1}))

        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar'] == {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_types_in_objects_extra_fields_are_extracted_to_definitions(self):
        type1 = lt.String(name='MyString')
        result = json_schema(lt.Object({'foo': type1}, allow_extra_fields=type1))

        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['additionalProperties'] == {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_types_in_lists_are_extracted_to_definitions(self):
        type1 = lt.String(name='MyString')
        result = json_schema(lt.Object({'foo': type1,
                                        'bar': lt.List(type1)}))

        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar']['items'] == \
            {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_types_in_dicts_are_extracted_to_definitions(self):
        type1 = lt.String(name='MyString')
        result = json_schema(lt.Object({'foo': type1,
                                        'bar': lt.Dict({'baz': type1})}))

        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar']['properties']['baz'] == \
            {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_types_in_dicts_default_are_extracted_to_definitions(self):
        type1 = lt.String(name='MyString')
        result = json_schema(lt.Object({'foo': type1,
                                        'bar': lt.Dict(type1)}))

        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar']['additionalProperties'] == \
            {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_types_in_one_of_are_extracted_to_definitions(self):
        type1 = lt.String(name='MyString')
        result = json_schema(lt.Object({'foo': type1,
                                        'bar': lt.OneOf([type1, lt.Integer()])}))

        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar']['anyOf'][0] == \
            {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_types_in_optional_are_extracted_to_definitions(self):
        type1 = lt.String(name='MyString')
        result = json_schema(lt.Object({'foo': type1,
                                        'bar': lt.Optional(type1)}))

        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar'] == {
            'anyOf': [
                {
                    '$ref': '#/components/schemas/MyString',
                },
                NULL_TYPE,
            ],
            'default': None,
        }
        assert 'bar' not in result['required']

    def test_type_references(self):
        registry = lr.TypeRegistry()

        type1 = lt.String(name='MyString')
        type1_ref = registry.add('AString', type1)

        assert json_schema(type1_ref) == json_schema(type1)

    def test_duplicate_type_references_are_extracted_to_definitions(self):
        registry = lr.TypeRegistry()

        type1 = lt.String(name='MyString')
        type1_ref = registry.add('AString', type1)

        result = json_schema(lt.Object({'foo': type1_ref, 'bar': type1_ref}))
        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar'] == {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_type_and_type_references_are_extracted_to_definitions(self):
        registry = lr.TypeRegistry()

        type1 = lt.String(name='MyString')
        type1_ref = registry.add('AString', type1)

        result = json_schema(lt.Object({'foo': type1, 'bar': type1_ref}))
        assert 'components' in result
        assert 'schemas' in result['components']
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/MyString'}
        assert result['properties']['bar'] == {'$ref': '#/components/schemas/MyString'}

    def test_duplicate_types_multiple_calls_do_not_omit_load_only(self):
        base_type = lt.Object({
            'load_field': lt.LoadOnly(lt.String()),
            'dump_field': lt.DumpOnly(lt.Integer())
        }, name='my_object')

        type1 = lt.Object({'foo': base_type, 'bar': base_type})

        definitions = lt.OrderedDict()

        result = json_schema(type1, definitions=definitions, mode='dump')
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/myObjectDump'}
        assert result['properties']['bar'] == {'$ref': '#/components/schemas/myObjectDump'}

        assert (base_type, 'dump') in definitions
        assert (base_type, 'load') not in definitions

        assert definitions[(base_type, 'dump')].name == 'myObjectDump'
        assert ('dump_field' in
                definitions[(base_type, 'dump')].jsonschema['properties'])
        assert ('load_field' not in
                definitions[(base_type, 'dump')].jsonschema['properties'])

        # Check that after load mode, the load_only field is present.
        result = json_schema(type1, definitions=definitions, mode='load')
        assert result['properties']['foo'] == {'$ref': '#/components/schemas/myObjectLoad'}
        assert result['properties']['bar'] == {'$ref': '#/components/schemas/myObjectLoad'}

        assert (base_type, 'dump') in definitions
        assert (base_type, 'load') in definitions

        assert definitions[(base_type, 'dump')].name == 'myObjectDump'
        assert definitions[(base_type, 'load')].name == 'myObjectLoad'

        assert ('dump_field' in
                definitions[(base_type, 'dump')].jsonschema['properties'])
        assert ('load_field' not in
                definitions[(base_type, 'dump')].jsonschema['properties'])

        assert ('dump_field' not in
                definitions[(base_type, 'load')].jsonschema['properties'])
        # Without deduplicating by load/dump mode, we would not see the load_only
        # field.
        assert ('load_field' in
                definitions[(base_type, 'load')].jsonschema['properties'])

    def test_self_referencing_types(self):
        registry = lr.TypeRegistry()
        errors_type = registry.add('Errors', lt.Dict(
            lt.OneOf([lt.String(), lt.List(lt.String()), registry['Errors']]),
            name='Errors',
        ))

        result = json_schema(errors_type)

        assert sorted(result.keys()) == sorted(['components', '$ref'])

        assert 'Errors' in result['components']['schemas']
        errorsDef = result['components']['schemas']['Errors']
        assert errorsDef['title'] == 'Errors'
        assert errorsDef['type'] == 'object'
        assert errorsDef['additionalProperties'] == {
            'anyOf': [
                json_schema(lt.String()),
                json_schema(lt.List(lt.String())),
                {'$ref': '#/components/schemas/Errors'},
            ]
        }

        assert result['$ref'] == '#/components/schemas/Errors'

    def test_definition_name_sanitization(self):
        type1 = lt.String(name='My string!')

        result = json_schema(lt.Object({'foo': type1, 'bar': type1}))
        assert result['components']['schemas'] == {'MyString': json_schema(type1)}

    @pytest.mark.parametrize('mode', [None, 'load', 'dump'])
    def test_definition_name_conflict_resolving(self, mode):
        type1 = lt.String(name='MyType')
        type2 = lt.Integer(name='MyType')
        type3 = lt.Boolean(name='MyType')

        result = json_schema(lt.Object({
            'field1': type1, 'field2': type2, 'field3': type3,
            'field4': type1, 'field5': type2, 'field6': type3,
        }), mode=mode)

        refs = [
            '#/components/schemas/MyType'
            + (mode.capitalize() if mode else '')
            + (str(i) if i else '')
            for i in range(3)
        ]
        assert result['properties']['field1']['$ref'] in refs
        assert result['properties']['field2']['$ref'] in refs
        assert result['properties']['field3']['$ref'] in refs
        assert len(set(result['properties'][field]['$ref']
                       for field in ['field1', 'field2', 'field3'])) == 3

    @pytest.mark.parametrize('mode', [None, 'load', 'dump'])
    def test_unnamed_types_definition_name_conflict_resolving(self, mode):
        type1 = lt.String()
        type2 = lt.Integer()
        type3 = lt.Integer()

        result = json_schema(lt.Object({
            'field1': type1, 'field2': type2, 'field3': type3,
            'field4': type1, 'field5': type2, 'field6': type3,
        }), mode=mode)
        refs = [
            '#/components/schemas/Type'
            + (mode.capitalize() if mode else '')
            + (str(i) if i else '')
            for i in range(3)
        ]
        assert result['properties']['field1']['$ref'] in refs
        assert result['properties']['field2']['$ref'] in refs
        assert result['properties']['field3']['$ref'] in refs
        assert len(set(result['properties'][field]['$ref']
                       for field in ['field1', 'field2', 'field3'])) == 3

    def test_dump_only_type_in_normal_mode(self):
        type1 = lt.String()
        assert json_schema(lt.DumpOnly(type1)) == json_schema(type1)

    def test_dump_only_type_in_dump_mode(self):
        type1 = lt.String()
        assert json_schema(lt.DumpOnly(type1), mode='dump') == json_schema(type1)

    def test_dump_only_type_in_load_mode(self):
        assert json_schema(lt.DumpOnly(lt.String()), mode='load') is None

    def test_load_only_type_in_normal_mode(self):
        type1 = lt.String()
        assert json_schema(lt.LoadOnly(type1)) == json_schema(type1)

    def test_load_only_type_in_load_mode(self):
        type1 = lt.String()
        assert json_schema(lt.LoadOnly(type1), mode='load') == json_schema(type1)

    def test_load_only_type_in_dump_mode(self):
        assert json_schema(lt.LoadOnly(lt.String()), mode='dump') is None

    def test_list_with_item_type_in_incorrect_mode(self):
        assert json_schema(lt.List(lt.DumpOnly(lt.String())), mode='load') == \
            {'type': 'array', 'maxItems': 0}

    def test_tuple_with_item_type_in_incorrect_mode(self):
        assert json_schema(
            lt.Tuple([lt.String(), lt.DumpOnly(lt.Integer()), lt.Boolean()]),
            mode='load',
        ) == json_schema(lt.Tuple([lt.String(), lt.Boolean()]))

    def test_tuple_with_all_item_types_in_incorrect_mode(self):
        assert json_schema(
            lt.Tuple([lt.DumpOnly(lt.String()), lt.DumpOnly(lt.Integer())]),
            mode='load',
        ) == {'type': 'array', 'maxItems': 0}

    def test_dict_with_fixed_properties_in_incorrect_mode(self):
        assert json_schema(
            lt.Dict({'foo': lt.String(), 'bar': lt.DumpOnly(lt.Integer())}),
            mode='load',
        ) == json_schema(lt.Dict({'foo': lt.String()}))

        assert json_schema(
            lt.Dict({'foo': lt.DumpOnly(lt.String()),
                     'bar': lt.DumpOnly(lt.Integer())}),
            mode='load',
        ) == {'type': 'object', 'maxProperties': 0}

    def test_dict_with_default_in_incorrect_mode(self):
        assert json_schema(
            lt.Dict(
                DictWithDefault({
                    'foo': lt.String(),
                    'bar': lt.Integer(),
                }, lt.DumpOnly(lt.Boolean())),
            ),
            mode='load',
        ) == json_schema(lt.Dict({'foo': lt.String(), 'bar': lt.Integer()}))

        assert json_schema(lt.Dict(lt.DumpOnly(lt.String())), mode='load') == \
            {'type': 'object', 'maxProperties': 0}

    def test_dict_with_all_fixed_properties_and_default_in_incorrect_mode(self):
        assert json_schema(
            lt.Dict(
                DictWithDefault({
                    'foo': lt.DumpOnly(lt.String()),
                    'bar': lt.DumpOnly(lt.Integer()),
                }, lt.DumpOnly(lt.Boolean())),
            ),
            mode='load',
        ) == {'type': 'object', 'maxProperties': 0}

    def test_object_with_fields_in_incorrect_mode(self):
        assert json_schema(
            lt.Object({
                'foo': lt.String(),
                'bar': lt.DumpOnly(lt.Integer()),
            }),
            mode='load',
        ) == json_schema(lt.Object({'foo': lt.String()}))

    def test_object_with_allowed_extra_fields_in_incorrect_mode(self):
        assert json_schema(
            lt.Object({
                'foo': lt.String(),
                'bar': lt.Integer(),
            }, allow_extra_fields=lt.DumpOnly(lt.String())),
            mode='load',
        ) == json_schema(lt.Object({'foo': lt.String(), 'bar': lt.Integer()}))

    def test_object_with_all_fields_in_incorrect_mode(self):
        assert json_schema(
            lt.Object({
                'foo': lt.DumpOnly(lt.String()),
                'bar': lt.DumpOnly(lt.Integer()),
            }, allow_extra_fields=lt.String()),
            mode='load',
        ) == json_schema(lt.Object({}, allow_extra_fields=lt.String()))

        assert json_schema(
            lt.Object({
                'foo': lt.DumpOnly(lt.String()),
                'bar': lt.DumpOnly(lt.Integer()),
            }),
            mode='load',
        ) == {'type': 'object', 'maxProperties': 0}

    def test_object_with_all_fields_and_extra_fields_in_incorrect_mode(self):
        assert json_schema(
            lt.Object({
                'foo': lt.DumpOnly(lt.String()),
                'bar': lt.DumpOnly(lt.Integer()),
            }, allow_extra_fields=lt.DumpOnly(lt.String())),
            mode='load',
        ) == {'type': 'object', 'maxProperties': 0}

    def test_one_of_with_item_types_in_sequence_in_incorrect_mode(self):
        assert json_schema(
            lt.OneOf([lt.DumpOnly(lt.String()), lt.Integer(), lt.Boolean()]),
            mode='load',
        ) == json_schema(lt.OneOf([lt.Integer(), lt.Boolean()]))

    def test_one_of_with_all_item_types_in_sequence_in_incorrect_mode(self):
        assert json_schema(
            lt.OneOf([lt.DumpOnly(lt.String()), lt.DumpOnly(lt.Integer())]),
            mode='load',
        ) is None

    def test_one_of_with_item_types_in_mapping_in_incorrect_mode(self):
        assert json_schema(
            lt.OneOf({
                'foo': lt.String(),
                'bar': lt.DumpOnly(lt.Integer()),
            }),
            mode='load',
        ) == json_schema(lt.OneOf({'foo': lt.String()}))

    def test_type_ref_with_inner_type_in_incorrect_mode(self):
        registry = lr.TypeRegistry()
        type_ref = registry.add('Foo', lt.DumpOnly(lt.String()))

        assert json_schema(type_ref, mode='load') is None

    def test_custom_type_schema(self):
        class MyType(lt.Type):
            pass

        class MyTypeEncoder(TypeEncoder):
            schema_type = MyType

            def json_schema(self, encoder, schema):
                js = super(MyTypeEncoder, self).json_schema(encoder, schema)
                js['type'] = 'foo'
                return js

        encoder = Encoder()
        encoder.add_encoder(MyTypeEncoder())

        assert encoder.json_schema(MyType()) == {'type': 'foo'}
