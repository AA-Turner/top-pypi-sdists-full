"""Every external import hugpy-core uses, in one place: a missing dependency fails here, at load.

hugpy_resources is the one function library: the database connection and the settings table, one JSON exchange
with a service, who is calling a door, and the steps of a system install. Nothing of hugpy-wrapper, hugpy-discovery
or hugpy-engine is imported: a wrapper is asked over its own API (wrappers/ask.py)."""
from abstract_flask import register_categories, spec
from flask import Blueprint, Flask
from werkzeug.exceptions import MethodNotAllowed, NotFound
from werkzeug.routing import RoutingException

from hugpy_resources import (
    account_ids,
    archive_path,
    bearer,
    check_reply,
    check_rule,
    compute_arguments,
    compute_model_rows,
    run_compute,
    connect_wal,
    DoorServer,
    ensure_account,
    ensure_folder,
    ensure_secret,
    env_setting,
    file_under,
    fmt_bytes,
    health_record,
    HOST_DATA_DIR,
    host_data_dir,
    http_json,
    read_json,
    JsonRequestHandler,
    key_digest,
    key_matches,
    KNOB_SCHEMA,
    new_key,
    open_readonly,
    PLACEMENT_RENAMES,
    PLACEMENT_TERMS,
    PLACEMENTS,
    quant_token,
    read_endpoint,
    read_secret,
    read_settings,
    remove_unit,
    reply_shown,
    service_interpreter,
    system_say,
    systemctl,
    tool_version,
    unit_installed,
    unit_state,
    with_no_think,
    write_endpoint,
    write_settings,
    write_unit,
)

__all__ = ['Blueprint', 'Flask', 'MethodNotAllowed', 'NotFound', 'RoutingException', 'register_categories', 'spec', 'account_ids', 'archive_path', 'bearer', 'check_reply', 'check_rule', 'connect_wal', 'DoorServer', 'ensure_account', 'ensure_folder', 'ensure_secret',
           'compute_arguments', 'compute_model_rows', 'run_compute', 'env_setting', 'file_under', 'fmt_bytes', 'health_record', 'HOST_DATA_DIR', 'host_data_dir', 'http_json', 'read_json', 'JsonRequestHandler',
           'key_digest', 'key_matches', 'KNOB_SCHEMA', 'new_key', 'open_readonly', 'PLACEMENT_RENAMES', 'PLACEMENT_TERMS', 'PLACEMENTS', 'quant_token', 'read_endpoint', 'read_secret', 'read_settings', 'remove_unit', 'reply_shown',
           'service_interpreter', 'system_say', 'systemctl', 'tool_version', 'unit_installed', 'unit_state', 'with_no_think',
           'write_endpoint', 'write_settings', 'write_unit']
