"""
spotilyzer requests CSV
"""

# system imports
import csv

# project imports
from ..json.requests import REQUESTS_KEY, POD_NAME_KEY, REPLICAS_KEY, \
    CORE_LIMIT_KEY, MEM_LIMIT_KEY

# constants
_types = (str, int, float, float)


def load_requests(frequests):
    """
    Load requests CSV file. Formatting checks are performed
    :param frequests: path to CSV file.
    :return: requests object
    """
    request_list = []
    with open(frequests, mode='r', encoding='utf-8-sig') as fobj:
        reader = csv.reader(fobj)
        header = reader.__next__()
        _validate_header(header, frequests)
        rowlen = len(header)
        line = 2
        for row in reader:
            _validate_row(rowlen, row, frequests, line)
            request = _get_request(rowlen, header, row, frequests, line)
            request_list.append(request)
            line += 1
    _validate_pod_names(request_list, frequests)
    return {REQUESTS_KEY: request_list}


def _validate_header(header, frequests):
    if header != [POD_NAME_KEY, REPLICAS_KEY, CORE_LIMIT_KEY, MEM_LIMIT_KEY]:
        raise SyntaxError(f"invalid header in {frequests}")


def _validate_row(rowlen, row, frequests, line):
    if len(row) != rowlen:
        raise SyntaxError("incorrect number of entries in "
                          f"{frequests}, line {line}")


def _get_request(rowlen, header, row, frequests, line):
    try:
        return {header[i]: _types[i](row[i]) for i in range(rowlen)}
    except ValueError as err:
        raise SyntaxError(f"invalid type in {frequests}, line {line}") from err


def _validate_pod_names(request_list, frequests):
    if len(request_list) != len(set(r[POD_NAME_KEY] for r in request_list)):
        raise SyntaxError(f"pod names in {frequests} are not unique")
