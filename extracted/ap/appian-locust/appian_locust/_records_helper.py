import json
from typing import Any, Dict, Tuple, Optional

from .utilities import extract_values, find_component_by_attribute_in_dict, logger
from re import match

log = logger.getLogger(__name__)


def get_all_record_types_from_json(json_response: Dict[str, Any]) -> Dict[str, Any]:
    response = dict()
    for current_record_type in json_response["ui"]["contents"][0]["feedItems"]:
        title = current_record_type['title'].strip()
        response[title] = current_record_type
    return response


def get_all_records_from_json(json_response: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    is_grid = _is_grid(json_response)
    records = {}
    error_key_string = "ERROR::"
    error_key_count = 0
    if is_grid:
        all_record_items = extract_values(json_response, "#t", "RecordLink")
        # extract all RecordLinks out of the response directly
        for record_item in all_record_items:
            try:
                opaque_id = record_item["_recordRef"]
                label = record_item["label"]
                key = label + "::" + opaque_id
                records[key] = record_item
            except Exception as e:
                error_key_count += 1
                records[error_key_string + str(error_key_count)] = {}
                raise e
    else:
        all_items = extract_values(json_response, "#t", "LinkedItem")
        label_extractor = _get_linkedItem_label
        if len(all_items) == 0:
            all_items = extract_values(json_response, "#t", "FeedItemLayout")
            label_extractor = _get_feedItemLayout_label
        for current_item in all_items:
            record_link_raw = extract_values(current_item, "#t", "RecordLink")
            if len(record_link_raw) > 0:
                record_item = record_link_raw[0]
                try:
                    opaque_id = record_item["_recordRef"]
                    label = label_extractor(current_item)
                    record_item["label"] = label
                    key = label + "::" + opaque_id
                    records[key] = record_item
                except Exception as e:
                    error_key_count += 1
                    records[error_key_string + str(error_key_count)] = {}
                    log.error(f"Corrupt Record Error: {record_item}")
    return records, error_key_count


def get_records_from_json_by_column(json_response: Dict[str, Any], column_index: int) -> Tuple[Dict[str, Any], int]:
    is_grid = _is_grid(json_response)
    records = {}
    error_key_string = "ERROR::"
    error_key_count = 0
    if is_grid:
        all_row_layouts = extract_values(json_response, "#t", "RowLayout")
        column_headers = all_row_layouts.pop(0)
        num_columns = len(column_headers)
        for row in all_row_layouts:
            record_link_raw = extract_values(row, "#t", "RecordLink")
            if len(record_link_raw) > 0:
                if column_index > (num_columns-1):
                    error_key_count += 1
                    error_message = f'Column index ({column_index}) is out of bounds. Please provide a column index between 0 and {num_columns-1}.'
                    raise Exception(error_message)
                else:
                    record_item = record_link_raw[0]
                    try:
                        opaque_id = row["contents"][column_index]["links"][0]["_recordRef"]
                        label = row["contents"][column_index]["links"][0]["label"]
                        record_item["label"] = label
                        key = label + "::" + opaque_id
                        records[key] = record_item
                    except Exception as e:
                        error_key_count += 1
                        records[error_key_string + str(error_key_count)] = {}
                        raise e
            else:
                error_key_count += 1
                raise Exception('No record links found.')

    return records, error_key_count


def get_record_summary_view_response(form_json: Dict[str, Any]) -> Dict[str, Any]:
    """
        This returns the contents of "x-embedded-summary" from Record Instance's Feed response
    """
    # SAIL Code for the Record Summary View is embedded within the response.
    record_summary_response = find_component_by_attribute_in_dict("name", "x-embedded-summary", form_json).get("children")
    if not record_summary_response or len(record_summary_response) < 1:
        raise Exception("Parser was not able to find embedded SAIL code within JSON response for the requested Record Instance")
    return json.loads(record_summary_response[0])


def get_record_header_response(form_json: Dict[str, Any]) -> Dict[str, Any]:
    """
        This returns the contents of "x-embedded-header" from Record Instance's Feed response.
        Header response is needed in cases like clicking on a related action.
    """
    # SAIL Code for the Record Header is embedded within the response.
    record_header_response = find_component_by_attribute_in_dict("name", "x-embedded-header", form_json).get("children")
    if not record_header_response or len(record_header_response) < 1:
        raise Exception("Parser was not able to find embedded SAIL code within JSON response for the requested Record Instance")
    return json.loads(record_header_response[0])


def _is_grid(res_dict_var: Dict[str, Any]) -> bool:
    return any([len(extract_values(res_dict_var, "testLabel", "recordGrid")) != 0,
                len(extract_values(res_dict_var, "testLabel", "recordGridInstances")) != 0])


def get_url_stub_from_record_list_url_path(url: Optional[str]) -> Optional[str]:
    """
        Attempts to parse the url stub the url of a record list.
        It should only be able to parse the url stub if the page is a record list.
        If the url stub cannot be parsed, returns None.

        Args:
            url: url path to attempt to parse the record list URL stub from

        Returns: The url stub if post_url matches a record list url, otherwise None
    """
    record_url_match = None
    if url:
        record_url_match = match(r'tempo/records/type/([\w]+)/view/all', url)
    return record_url_match.groups()[0] if record_url_match else None


def get_url_stub_from_record_list_post_request_url(post_url: Optional[str]) -> Optional[str]:
    """
        Given post_url, returns the URL stub IF the url matches the url for a record list.
        If not, returns None.

        Args:
            post_url: the post request url (not including the host and domain) to post to

        Returns: The url stub if post_url matches a record instance list url, otherwise None
    """
    record_url_match = None
    if post_url:
        record_url_match = match(r'[\S]+\/pages\/records\/recordType\/([\w]+)', post_url)
    return record_url_match.groups()[0] if record_url_match else None


def _get_linkedItem_label(item: Dict[str, Any]) -> str:
    return extract_values(item["values"], "#t", "string")[0]["#v"]


def _get_feedItemLayout_label(item: Dict[str, Any]) -> str:
    return item["title"]
