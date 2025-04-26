import json
from .data_quality import CheckResult, CollectionResult
from ..exceptions import DataQualityException

def resolve_object_from_json_dict(json_dict):

    if isinstance(json_dict, str):
        json_dict = json.loads(json_dict)

    # CheckResult object
    if json_dict.get('check'):
        return CheckResult(json_dict)

    # CollectionResult object
    elif json_dict.get('checks'):
        return CollectionResult(json_dict)

    return DataQualityException('Could not resolve object from json dict.')