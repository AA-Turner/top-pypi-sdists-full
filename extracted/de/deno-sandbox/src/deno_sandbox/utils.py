import re


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_to_camel_case(data):
    if isinstance(data, dict):
        return {to_camel_case(k): convert_to_camel_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_camel_case(i) for i in data]
    else:
        return data


def to_snake_case(camel_str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def convert_to_snake_case(data):
    if isinstance(data, dict):
        return {to_snake_case(k): convert_to_snake_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_snake_case(i) for i in data]
    else:
        return data


def parse_link_header(header: str) -> dict[str, str]:
    links = {}
    parts = header.split(",")
    for part in parts:
        section = part.split(";")
        if len(section) < 2:
            continue
        url = section[0].strip()[1:-1]
        name = section[1].strip().split("=")[1][1:-1]
        links[name] = url
    return links
