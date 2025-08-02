# arpakit

import json
from typing import Any, Iterable

import orjson

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def transfer_json_str_to_data(
        json_str: str, fast: bool = False
) -> dict[Any, Any] | list[Any] | None:
    if not isinstance(json_str, str):
        raise ValueError("not isinstance(json_str, str)")
    if fast:
        return orjson.loads(json_str)
    else:
        return json.loads(json_str)


def transfer_data_to_json_str(
        data: dict[Any, Any] | list[Any] | None, beautify: bool = True, fast: bool = False
) -> str:
    if not isinstance(data, dict) and not isinstance(data, list) and data is not None:
        raise ValueError("not isinstance(data, dict) and not isinstance(data, list) and data is not None")
    if fast:
        return orjson.dumps(data).decode()
    else:
        if beautify:
            return json.dumps(data, ensure_ascii=False, indent=2, default=str)
        else:
            return json.dumps(data, ensure_ascii=False, default=str)


def transfer_data_to_json_str_to_data(
        data: dict[Any, Any] | list[Any] | None, fast: bool = False
) -> dict[Any, Any] | list[Any] | None:
    return transfer_json_str_to_data(transfer_data_to_json_str(data=data, fast=fast), fast=fast)


def transfer_json_str_to_data_to_json_str(
        json_str: str, beautify: bool = True, fast: bool = False
) -> str:
    return transfer_data_to_json_str(
        transfer_json_str_to_data(json_str=json_str, fast=fast), beautify=beautify, fast=fast
    )


def write_dicts_iterly_in_json(
        *,
        filepath: str,
        dict_iterable: Iterable[dict],
        beautify: bool = False
):
    with open(filepath, "w", encoding="utf-8") as f:
        if beautify:
            f.write("[\n")
        else:
            f.write("[")
        first_item = True

        for dict_ in dict_iterable:
            if not first_item:
                if beautify:
                    f.write(",\n")
                else:
                    f.write(",")
            if beautify:
                json.dump(dict_, f, ensure_ascii=False, indent=2)
            else:
                json.dump(dict_, f, ensure_ascii=False)
            first_item = False

        if beautify:
            f.write("\n]")
        else:
            f.write("]")

    return filepath


def json_stream_iterator(
        dict_iterable: Iterable[dict],
):
    yield "["

    first = True
    for dict_ in dict_iterable:
        if not first:
            yield ","
        else:
            first = False
        yield transfer_data_to_json_str(dict_, fast=True, beautify=False)

    yield "]"


def __example():
    pass


if __name__ == '__main__':
    __example()
