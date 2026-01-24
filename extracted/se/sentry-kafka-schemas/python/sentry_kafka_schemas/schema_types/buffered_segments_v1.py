from typing import Required, Union, Any, TypedDict, Literal, List, Dict


class BufferedSegment(TypedDict, total=False):
    """ buffered_segment. """

    spans: Required["_SegmentSpans"]
    """
    minItems: 1

    Required property
    """



class SpanEvent(TypedDict, total=False):
    """ span_event. """

    event_id: "_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUuid"
    """
    minLength: 32
    maxLength: 36
    """

    organization_id: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUint"]
    """
    minimum: 0

    Required property
    """

    project_id: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUint"]
    """
    minimum: 0

    Required property
    """

    key_id: "_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUint"
    """ minimum: 0 """

    trace_id: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUuid"]
    """
    minLength: 32
    maxLength: 36

    Required property
    """

    span_id: Required[str]
    """
    The span ID is a unique identifier for a span within a trace. It is an 8 byte hexadecimal string.

    Required property
    """

    parent_span_id: Union[str, None]
    """ The parent span ID is the ID of the span that caused this span. It is an 8 byte hexadecimal string. """

    start_timestamp: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsPositivefloat"]
    """
    minimum: 0

    Required property
    """

    end_timestamp: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsPositivefloat"]
    """
    minimum: 0

    Required property
    """

    retention_days: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUint16"]
    """
    minimum: 0
    maximum: 65535

    Required property
    """

    downsampled_retention_days: "_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUint16"
    """
    minimum: 0
    maximum: 65535
    """

    received: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsPositivefloat"]
    """
    minimum: 0

    Required property
    """

    name: Required[Union[str, None]]
    """ Required property """

    status: Required[str]
    """ Required property """

    is_segment: Union[bool, None]
    links: Union[List["_SpanEventLinksArrayItem"], None]
    """
    items:
      oneOf:
      - $ref: file://ingest-spans.v1.schema.json#/definitions/SpanLink
      - type: 'null'
      used: !!set
        $ref: null
        oneOf: null
    """

    attributes: "_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributes"
    """
    additionalProperties:
      oneOf:
      - $ref: file://ingest-spans.v1.schema.json#/definitions/AttributeValue
      - type: 'null'
      used: !!set
        $ref: null
        oneOf: null
    """

    _meta: Dict[str, Any]


class SpanLink(TypedDict, total=False):
    """ span_link. """

    trace_id: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUuid"]
    """
    minLength: 32
    maxLength: 36

    Required property
    """

    span_id: Required[str]
    """ Required property """

    attributes: "_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributes"
    """
    additionalProperties:
      oneOf:
      - $ref: file://ingest-spans.v1.schema.json#/definitions/AttributeValue
      - type: 'null'
      used: !!set
        $ref: null
        oneOf: null
    """

    sampled: Union[bool, None]


_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributes = Union[Dict[str, "_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributesObjectAdditionalproperties"], None]
"""
additionalProperties:
  oneOf:
  - $ref: file://ingest-spans.v1.schema.json#/definitions/AttributeValue
  - type: 'null'
  used: !!set
    $ref: null
    oneOf: null
"""



_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributesObjectAdditionalproperties = Union["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalue", None]
""" Aggregation type: oneOf """



class _FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalue(TypedDict, total=False):
    type: Required["_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType"]
    """ Required property """

    value: Required[Union[Union[int, float], None, str, bool, List[Any], Dict[str, Any]]]
    """ Required property """



_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType = Union[Literal['boolean'], Literal['integer'], Literal['double'], Literal['string'], Literal['array'], Literal['object']]
_FILECOLONINGESTSPANSFULLSTOPV1FULLSTOPSCHEMAFULLSTOPJSONNUMBERSIGNDEFINITIONSATTRIBUTEVALUETYPE_BOOLEAN: Literal['boolean'] = "boolean"
"""The values for the '_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType' enum"""
_FILECOLONINGESTSPANSFULLSTOPV1FULLSTOPSCHEMAFULLSTOPJSONNUMBERSIGNDEFINITIONSATTRIBUTEVALUETYPE_INTEGER: Literal['integer'] = "integer"
"""The values for the '_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType' enum"""
_FILECOLONINGESTSPANSFULLSTOPV1FULLSTOPSCHEMAFULLSTOPJSONNUMBERSIGNDEFINITIONSATTRIBUTEVALUETYPE_DOUBLE: Literal['double'] = "double"
"""The values for the '_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType' enum"""
_FILECOLONINGESTSPANSFULLSTOPV1FULLSTOPSCHEMAFULLSTOPJSONNUMBERSIGNDEFINITIONSATTRIBUTEVALUETYPE_STRING: Literal['string'] = "string"
"""The values for the '_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType' enum"""
_FILECOLONINGESTSPANSFULLSTOPV1FULLSTOPSCHEMAFULLSTOPJSONNUMBERSIGNDEFINITIONSATTRIBUTEVALUETYPE_ARRAY: Literal['array'] = "array"
"""The values for the '_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType' enum"""
_FILECOLONINGESTSPANSFULLSTOPV1FULLSTOPSCHEMAFULLSTOPJSONNUMBERSIGNDEFINITIONSATTRIBUTEVALUETYPE_OBJECT: Literal['object'] = "object"
"""The values for the '_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsAttributevalueType' enum"""



_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsPositivefloat = Union[int, float]
""" minimum: 0 """



_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUint = int
""" minimum: 0 """



_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUint16 = int
"""
minimum: 0
maximum: 65535
"""



_FileColonIngestSpansFullStopV1FullStopSchemaFullStopJsonNumberSignDefinitionsUuid = str
"""
minLength: 32
maxLength: 36
"""



_SegmentSpans = List["SpanEvent"]
""" minItems: 1 """



_SpanEventLinksArrayItem = Union["SpanLink", None]
""" Aggregation type: oneOf """

