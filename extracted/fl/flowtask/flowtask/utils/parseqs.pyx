import cython
import orjson
from typing import Type

prefixes = frozenset(('(', '[', '{'))


def is_parseable(str value):
    cdef str c = value[0]
    if c in prefixes:
        if c == '[':
            return ParseList
        elif c == '(':
            return ParseTuple
        elif c == '{':
            return ParseDict
    else:
        return False


def _parseString(value):
    if isinstance(value, str):
        if str(value).startswith("'"):
            return value[value.startswith('"') and len('"'):-1]
    return value


def parse_arguments(arguments):
    attributes = {}
    stepattrs = {}
    for i, arg in enumerate(arguments):
        if arg.startswith(("-", "--")):
            name = arg[2:]
            if ':' in name:
                try:
                    component, val = name.split(':')
                    try:
                        prev = stepattrs[component]
                    except KeyError:
                        prev = {}
                    attribute, value = val.split('=')
                    if '.' in attribute:
                        attrib, subattr = attribute.split('.')
                        new_val = {
                            attrib: {
                                subattr: value
                            }
                        }
                    else:
                        new_val = {
                            attribute: value
                        }
                    stepattrs[component] = {**prev, **new_val}
                except (KeyError, IndexError):
                    pass
            elif '=' in name:
                try:
                    n, val = name.split('=')
                    if '.' in n:
                        new_val = {}
                        attrib, subattr = n.split('.')
                        try:
                            prev = attributes[attrib]
                        except KeyError:
                            prev = {}
                        new_val[subattr] = val
                        attributes[attrib] = {**prev, **new_val}
                    else:
                        attributes[n] = val
                except (KeyError, IndexError):
                    pass
            else:
                try:
                    attributes[name] = arguments[i+1]
                except (KeyError, IndexError):
                    pass
    return [attributes, stepattrs]


class ParseQS:
    separator: str = ','
    prefix: str = ''
    value: str = ''

    def parse(self):
        def remove_enclosing(value: str):
            return value[value.startswith(self.prefix) and len(self.prefix):-1]
        obj = remove_enclosing(self.value)
        elements = obj.split(self.separator)
        if self.instance_class is not None:
            return self.instance_class(elements)
        for key, val in enumerate(elements):
            try:
                self.result.append(_parseString(val))
            except ValueError:
                raise Exception(
                    'ParseQS: Cannot parse QueryString as Iterable'
                )
        return self.result

    def __new__(cls, value, instance_class: Type = None):
        cls.instance_class = instance_class
        cls.value = value
        return cls.parse(cls)


class ParseList(ParseQS):
    separator: str = ','
    prefix: str = '['
    result: list = []


class ParseTuple(ParseQS):
    separator: str = ','
    prefix: str = '('
    result: tuple = []


class ParseDict(ParseQS):
    result: dict = {}
    def parse(self):
        try:
            self.result = orjson.loads(self.value)
            if self.instance_class is not None:
                return self.instance_class(self.result)
            else:
                return self.result
        except Exception as err:
            raise Exception(
                f'ParseDict: Cannot parse QueryString as Dictionary: {err}'
            )
