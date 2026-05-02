#!/usr/bin/env python3

import argparse
import base64
import hashlib
from typing import Union, Optional
from urllib.parse import urlparse, parse_qs
import pymongo
import yaml
from perun.connector import AdaptersManager
from pymongo.errors import OperationFailure
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


def get_collection(cfg):
    client = pymongo.MongoClient(cfg["database"]["connection_string"])
    database_name = cfg["database"]["database_name"]
    collection_name = cfg["database"]["collection_name"]
    return client[database_name][collection_name]


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_filepath", type=str, help="path_to_config_file")
    arguments = parser.parse_args()
    return load_yaml_from_file(arguments.config_filepath)


def load_yaml_from_file(filepath):
    with open(filepath, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        return cfg


def get_attr_perun_names(cfg):
    names = []
    for attribute in cfg["attributes"].values():
        if isinstance(attribute, list):
            for val in attribute:
                names.append(val)
        else:
            names.append(attribute)
    return names


def get_data(cfg):
    attributes_map = load_yaml_from_file(cfg["attrs_cfg_path"])
    adapters_manager = AdaptersManager(cfg["adapters_manager"], attributes_map)

    facilities_list = adapters_manager.get_facilities_by_attribute_with_attributes(
        cfg["attributes"]["proxy_identifier"],
        cfg["proxy_identifier_value"],
        get_attr_perun_names(cfg),
    )

    present_client_ids = []
    collection = get_collection(cfg)
    for facility in facilities_list:
        attrs_dict = get_attr_dict(cfg, facility.attributes)
        if attrs_dict["client_id"] is None:
            print(
                f"Cannot process client with client_id: None "
                f"for facility facility_id: {facility.id}"
            )
            continue
        print("Processing client_id: {}.".format(attrs_dict["client_id"]))
        try:
            result = collection.replace_one(
                {"client_id": attrs_dict["client_id"]}, attrs_dict, True
            )
            if result.upserted_id:
                print("Client {} upserted.".format(attrs_dict["client_id"]))
            else:
                print("Client {} updated.".format(attrs_dict["client_id"]))

        except OperationFailure as e:
            print(
                "Processing of client_id failure code: {} details: {}".format(
                    attrs_dict["client_id"], e.code
                )
            )
        present_client_ids.append(attrs_dict["client_id"])
    if cfg["delete_not_present_clients"]:
        try:
            print("Processing delete of not present clients.")
            result = collection.delete_many({"client_id": {"$nin": present_client_ids}})
            print("Deleted {} not present clients.".format(result.deleted_count))
        except OperationFailure as e:
            print(
                "Processing of delete not present clients,"
                + " failure code: {} details: {}".format(e.code, e.details)
            )


def get_issue_refresh_tokens_value(cfg, facility_attrs):
    value = facility_attrs.get(cfg["attributes"]["issue_refresh_tokens"])
    return value is True


def parse_uris_to_uri_params(
    uris: list[str],
) -> dict[str, Optional[dict[str, list[str]]]]:
    result_uris = {}
    for uri in uris:
        parsed_url = urlparse(uri)
        uri = parsed_url._replace(query="")._replace(fragment="").geturl()
        if uri in result_uris:
            print(f"Skipping duplicate URL {uri}" + " with different query params")
        else:
            params = parse_qs(parsed_url.query)
            result_uris[uri] = params or None
    return result_uris


def get_attr_dict(
    cfg, facility_attrs: dict[str, Union[str, int, bool, list[str], dict[str, str]]]
):
    result = {}
    for key, value in cfg["static_attributes"].items():
        result[key] = value

    for perun_attr_name, perun_attr_value in facility_attrs.items():
        for key, value in cfg["attributes"].items():
            if isinstance(value, list) and perun_attr_name in value:
                if key in result:
                    result[key].append(perun_attr_value)
                else:
                    result[key] = [perun_attr_value]
            elif value == perun_attr_name:
                if key == "redirect_uris" or key == "post_logout_redirect_uri":
                    if perun_attr_value:
                        uris = parse_uris_to_uri_params(perun_attr_value)
                        result[key] = [[uri, params] for uri, params in uris.items()]
                    else:
                        result[key] = []
                elif key == "client_secret":
                    result[key] = (
                        None
                        if perun_attr_value is None or perun_attr_value == "null"
                        else decrypt_secret(perun_attr_value, cfg["encryption_key"])
                    )
                elif key == "flow_types":
                    issue_refresh_tokens = get_issue_refresh_tokens_value(
                        cfg, facility_attrs
                    )
                    grant_types, response_types = set_grant_and_response_types(
                        perun_attr_value, issue_refresh_tokens
                    )
                    result["grant_types_supported"] = grant_types
                    result["response_types"] = response_types
                elif key in [
                    "client_name",
                    "tos_uri",
                    "policy_uri",
                    "logo_uri",
                    "client_uri",
                ]:
                    if not perun_attr_value or isinstance(perun_attr_value, str):
                        result[key] = perun_attr_value
                    else:
                        for lan, trans in perun_attr_value.items():
                            if key not in result:
                                result[key] = trans
                            result[key + "#" + lan] = trans
                elif key == "code_challenge_type":
                    if perun_attr_value and perun_attr_value != "none":
                        result["pkce_essential"] = True
                elif key not in [
                    "master_proxy_identifier",
                    "proxy_identifier",
                ]:
                    result[key] = perun_attr_value
    return result


def set_grant_and_response_types(flow_types_list, issue_refresh_tokens):
    grant_types = set()
    response_types = set()

    authorization_code = "authorization code"
    device = "device"
    implicit = "implicit"
    hybrid = "hybrid"

    grant_authorization_code = "authorization_code"
    grant_implicit = "implicit"
    grant_device = "urn:ietf:params:oauth:grant-type:device_code"
    grant_hybrid = "hybrid"
    grant_refresh_token = "refresh_token"

    response_code = "code"
    response_token = "token"
    response_id_token = "id_token"
    response_token_id_token = response_token + " " + response_id_token
    response_id_token_token = response_id_token + " " + response_token
    response_code_id_token = response_code + " " + response_id_token
    response_code_token = response_code + " " + response_token
    response_code_token_id_token = response_code_token + " " + response_id_token
    response_code_id_token_token = response_code_id_token + " " + response_token

    response_type_auth_code = {response_code}
    response_type_implicit = {
        response_id_token,
        response_token,
        response_id_token_token,
        response_token_id_token,
    }
    response_type_hybrid = {
        response_code_token,
        response_code_id_token,
        response_code_id_token,
        response_code_id_token_token,
        response_code_token_id_token,
    }
    if flow_types_list:
        if authorization_code in flow_types_list:
            grant_types.add(grant_authorization_code)
            response_types.update(response_type_auth_code)
        if implicit in flow_types_list:
            grant_types.add(grant_implicit)
            response_types.update(response_type_implicit)
        if hybrid in flow_types_list:
            grant_types.add(grant_hybrid)
            grant_types.add(grant_authorization_code)
            response_types.update(response_type_hybrid)
        if device in flow_types_list:
            grant_types.add(grant_device)
    if issue_refresh_tokens:
        grant_types.add(grant_refresh_token)
    return list(grant_types), list(response_types)


def decrypt_secret(client_secret, encryption_key):
    encryption_key = generate_secret_key_spec(encryption_key)
    decoded = base64.urlsafe_b64decode(client_secret)
    cipher = AES.new(encryption_key, AES.MODE_ECB)
    return unpad(cipher.decrypt(decoded), 16).decode("utf-8")


def generate_secret_key_spec(secret):
    secret = fix_secret(secret)
    key = secret.encode("utf-8")
    my_hash = hashlib.sha1()
    my_hash.update(key)
    key = my_hash.digest()
    return key[0:16]


def fix_secret(secret):
    if len(secret) < 32:
        missing_length = 32 - len(secret)
        for i in range(missing_length):
            secret += "A"
    return secret[0:32]


def main():
    get_data(get_config())


if __name__ == "__main__":
    main()
