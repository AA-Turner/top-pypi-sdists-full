"""Read browser cookies with V2 ``driver_query_script`` parity.

Port of the V2 source ``driver_query_script`` (type == "cookie") +
``find_dict_with_kv``. ``attributes``/``field`` semantics are identical to V2.
"""
import logging

_log = logging.getLogger(__name__)


def find_dict_with_kv(data, key, value):
    if isinstance(data, dict):
        if data.get(key) == value:
            return data
        for v in data.values():
            result = find_dict_with_kv(v, key, value)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_dict_with_kv(item, key, value)
            if result:
                return result
    return None


def get_cookies(driver, attributes=None, field=""):
    attributes = attributes or []
    _log.info("    [get_cookies] attributes=%s field=%r", attributes, field)
    queried_content = driver.get_cookies()

    for attr in attributes:
        for key, value in attr.items():
            if key == "index":
                queried_content = queried_content[int(value)]
            else:
                query_arr = value
                if len(query_arr) == 1:
                    queried_content = queried_content.get(query_arr[0], "")
                else:
                    queried_content = find_dict_with_kv(queried_content, query_arr[0], query_arr[1])
                    if queried_content is None:
                        raise ValueError(
                            f"Key {query_arr[0]} with value {query_arr[1]} not found in queried content."
                        )

    if field == "len":
        return len(queried_content)
    elif field == "keys":
        return list(queried_content.keys())
    elif field == "values":
        return list(queried_content.values())
    return queried_content
