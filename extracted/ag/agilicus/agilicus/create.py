import json

from dataclasses import dataclass
from typing import Callable, Optional, Any, Union
from agilicus_api import ApiException
from . import input_helpers


def find_guid(obj: dict):
    guid = obj.get("id", None)
    if guid:
        return guid
    md = obj.get("metadata", {})
    guid = md.get("id", None)
    if guid:
        return guid
    raise Exception(f"GUID cannot be found in obj {obj}")


def create_or_update(
    obj,
    create_method: Callable,
    update_method: Optional[Callable] = None,
    to_dict=True,
    guid_finder=find_guid,
) -> tuple[Union[dict, object], int]:
    """A helper method that handles duplicate (409)
    creation of objects. On 409, if the update_method is provided,
    it will apply a PUT on the resource to update it with
    the new requested data. The guid is searched for in the object
    returned from the 409, and this is then provided
    to the update method as an argument, along with the original
    object that should be applied.
        param: obj: the object to be created or updated
        param: create_method(obj, ...)
        param: update_method(guid, obj, ...)
        returns: tuple, the object, with the status code.

        Note the status code could be:
           409: a duplicate, no update was performed
           201: a create was succesfully made
           200: a duplicate occured, and the object was updated accordingly
    """
    result = None
    try:
        result = create_method(obj)
        if to_dict:
            return result.to_dict(), 201
        else:
            return result, 201
    except ApiException as exc:
        if exc.status == 409:
            body = exc.body
            if not body:
                raise
            result = json.loads(body)
            if update_method:
                guid = guid_finder(result)
                if to_dict:
                    return update_method(guid, obj).to_dict(), 200
                else:
                    return update_method(guid, obj), 200
            else:
                return result, 409
        else:
            raise
    return result


def handle_api_409(exc: ApiException, klass=None):
    body = exc.body
    if not body:
        raise
    result = json.loads(body)
    if klass is not None:
        return input_helpers.model_from_dict(klass, result)
    return result


def add_list_resources(objs, add_info):
    results: list[AddResult] = []
    for obj in objs:
        result, status = create_or_update(
            obj,
            add_info.create_fn,
            add_info.replace_fn,
            to_dict=False,
            guid_finder=add_info.guid_finder,
        )
        results.append(
            AddResult(
                obj=result,
                result_name=add_info.name_getter(result),
                result_id=add_info.guid_finder(result),
                created=status != 409,
            )
        )

    return results


class AddInfo:
    def __init__(self):
        super().__init__()
        self.name_getter = name_in_spec
        self.guid_finder = find_guid


@dataclass
class AddResult:
    obj: Any
    result_name: str
    created: bool
    result_id: Optional[str] = None
    exc: Optional[str] = None


def name_in_spec(obj):
    return obj.spec.name
