from pyld.nquads import escape, parse_nquads, serialize_nquads, unescape


def test_escaping():
    input = "\t\b\n\r\f\"'\\"
    unescaped = unescape(input)
    assert unescaped == "\t\u0008\n\r\u000c\"'\\"
    escaped = escape(unescaped)
    assert escaped == input


def test_parsing_with_unescaping():
    input = r"""<urn:ex:s> <urn:ex:000:empty> "" .
<urn:ex:s> <urn:ex:001:simple> "simple" .
<urn:ex:s> <urn:ex:002:quote> "\"" .
<urn:ex:s> <urn:ex:003:backslash> "\\" .
<urn:ex:s> <urn:ex:004:nl> "\n" .
<urn:ex:s> <urn:ex:005:cr> "\r" .
<urn:ex:s> <urn:ex:006:all> "\"\\\n\r" .
<urn:ex:s> <urn:ex:007:uchar> "\u0022\u005c" .
<urn:ex:s> <urn:ex:008:echar> "\t\b\n\r\f\"\'\\" .
<urn:ex:s> <urn:ex:009> "\\u0039" .
<urn:ex:s> <urn:ex:010> "\\n" .
<urn:ex:s> <urn:ex:011> "\\\\" .
<urn:ex:s> <urn:ex:012> "\"\"" .
<urn:ex:s> <urn:ex:013> "\\\\\\" .
<urn:ex:s> <urn:ex:014> "\"\"\"" .
<urn:ex:s> <urn:ex:015> "\u221e" .
<urn:ex:s> <urn:ex:016> "∞" .
    """
    parsed = parse_nquads(input)

    assert parsed["@default"][0]["object"]["value"] == ""
    assert parsed["@default"][1]["object"]["value"] == "simple"
    assert parsed["@default"][2]["object"]["value"] == '"'
    assert parsed["@default"][3]["object"]["value"] == "\\"
    assert parsed["@default"][4]["object"]["value"] == "\n"
    assert parsed["@default"][5]["object"]["value"] == "\r"
    assert parsed["@default"][6]["object"]["value"] == '"\\\n\r'
    assert parsed["@default"][7]["object"]["value"] == "\u0022\u005c"
    assert parsed["@default"][8]["object"]["value"] == "\t\u0008\n\r\u000c\"'\\"
    assert parsed["@default"][9]["object"]["value"] == "\\u0039"
    assert parsed["@default"][10]["object"]["value"] == "\\n"
    assert parsed["@default"][11]["object"]["value"] == "\\\\"
    assert parsed["@default"][12]["object"]["value"] == '""'
    assert parsed["@default"][13]["object"]["value"] == "\\\\\\"
    assert parsed["@default"][14]["object"]["value"] == '"""'
    assert parsed["@default"][15]["object"]["value"] == "∞"
    assert parsed["@default"][16]["object"]["value"] == "∞"


def test_serializing_with_escaping():
    input = {
        "@default": [
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:000:empty"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:001:simple"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "simple",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:002:quote"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": '"',
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:003:backslash"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\\",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:004:nl"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\n",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:005:cr"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\r",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:006:all"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": '"\\\n\r',
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:007:uchar"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": '"\\',
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:008:echar"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\t\u0008\n\r\u000c\"'\\",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:009"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\\u0039",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:010"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\\n",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:011"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\\\\",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:012"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": '""',
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:013"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\\\\\\",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:014"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": '"""',
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:015"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\u221e",
                },
            },
            {
                "subject": {"type": "IRI", "value": "urn:ex:s"},
                "predicate": {"type": "IRI", "value": "urn:ex:016"},
                "object": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    "value": "\u221e",
                },
            },
        ]
    }
    expected = r"""<urn:ex:s> <urn:ex:000:empty> "" .
<urn:ex:s> <urn:ex:001:simple> "simple" .
<urn:ex:s> <urn:ex:002:quote> "\"" .
<urn:ex:s> <urn:ex:003:backslash> "\\" .
<urn:ex:s> <urn:ex:004:nl> "\n" .
<urn:ex:s> <urn:ex:005:cr> "\r" .
<urn:ex:s> <urn:ex:006:all> "\"\\\n\r" .
<urn:ex:s> <urn:ex:007:uchar> "\"\\" .
<urn:ex:s> <urn:ex:008:echar> "\t\b\n\r\f\"\'\\" .
<urn:ex:s> <urn:ex:009> "\\u0039" .
<urn:ex:s> <urn:ex:010> "\\n" .
<urn:ex:s> <urn:ex:011> "\\\\" .
<urn:ex:s> <urn:ex:012> "\"\"" .
<urn:ex:s> <urn:ex:013> "\\\\\\" .
<urn:ex:s> <urn:ex:014> "\"\"\"" .
<urn:ex:s> <urn:ex:015> "∞" .
<urn:ex:s> <urn:ex:016> "∞" .
"""

    serialized = serialize_nquads(input)

    assert expected == serialized
