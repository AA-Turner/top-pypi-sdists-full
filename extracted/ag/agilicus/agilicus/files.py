import datetime
import json
import shutil
import urllib.parse

import agilicus
import requests

from . import context, hash, response
from .input_helpers import get_org_from_input_or_ctx, strip_none
from .input_helpers import update_org_from_input_or_ctx
from .output.table import column, spec_column, format_table, metadata_column, subtable

FILES_BASE_URI = "/v1/files"

OPER_STATUS_OPTIONS = ["active", "pending_delete", "deleted", "down"]


def query(ctx, org_id=None, tag=None, **kwargs):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}

    if org_id:
        params["org_id"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org_id"] = org_id

    if tag:
        params["tag"] = tag

    kwargs = strip_none(kwargs)
    params.update(**kwargs)
    query = urllib.parse.urlencode(params)
    uri = "{}?{}".format(FILES_BASE_URI, query)
    resp = requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)["files"]


def upload(
    ctx,
    filename,
    region=None,
    org_id=None,
    tag=None,
    name=None,
    label=None,
    visibility=None,
    **kwargs,
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    if not name:
        name = filename

    if not label:
        label = datetime.datetime.utcnow().isoformat()

    md5_hash = hash.get_base64_md5(filename)

    multipart_form_data = {}
    multipart_form_data["md5_hash"] = md5_hash
    multipart_form_data["file_zip"] = (name, open(filename, "rb"))

    if org_id:
        multipart_form_data["org_id"] = (None, org_id)
    else:
        multipart_form_data["org_id"] = (None, context.get_org_id(ctx, token))

    if tag:
        multipart_form_data["tag"] = (None, tag)

    if region:
        multipart_form_data["region"] = (None, region)

    if name:
        multipart_form_data["name"] = (None, name)

    if label:
        multipart_form_data["label"] = (None, label)

    if visibility:
        multipart_form_data["visibility"] = (None, visibility)

    uri = "{}".format(FILES_BASE_URI)
    resp = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        files=multipart_form_data,
        verify=context.get_cacert(ctx),
        timeout=60,
    )
    response.validate(resp)
    return json.loads(resp.text)


def reupload(
    ctx,
    file_id,
    filename,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    result = apiclient.files_api.reupload_file(
        file_id=file_id, file_zip=open(filename, "rb"), org_id=org_id
    )
    return result.to_dict()


def delete(ctx, file_id, org_id=None, _continue_on_error=False):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}

    if org_id:
        params["org_id"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org_id"] = org_id

    query = urllib.parse.urlencode(params)
    uri = "{}/{}?{}".format(FILES_BASE_URI, file_id, query)
    resp = requests.delete(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp, _continue_on_error=_continue_on_error)
    return resp.text


def get(ctx, file_id, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}

    if org_id:
        params["org_id"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org_id"] = org_id

    query = urllib.parse.urlencode(params)
    uri = "{}/{}?{}".format(FILES_BASE_URI, file_id, query)
    resp = requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def download(ctx, file_id, org_id=None, destination=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}

    if org_id:
        params["org_id"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org_id"] = org_id

    if not destination:
        _file = get(ctx, file_id, org_id)
        destination = _file["name"]

    query = urllib.parse.urlencode(params)
    uri = "{}_download/{}?{}".format(FILES_BASE_URI, file_id, query)
    with requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
        stream=True,
    ) as handle:
        handle.raise_for_status()
        with open(destination, "wb") as f:
            shutil.copyfileobj(handle.raw, f)


def list_file_associations(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    params = strip_none(kwargs)
    query_results = apiclient.files_api.list_file_associations(**params)
    return query_results.file_associations


def show_file_association(ctx, association_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    params = strip_none(kwargs)
    return apiclient.files_api.get_file_association(
        file_association_id=association_id, **params
    )


def delete_file_association(ctx, association_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    params = strip_none(kwargs)
    return apiclient.files_api.delete_file_association(
        file_association_id=association_id, **params
    )


def add_file_association(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    kwargs = strip_none(kwargs)
    spec = agilicus.FileAssociationSpec(**kwargs)
    assoc = agilicus.FileAssociation(spec=spec)
    return apiclient.files_api.create_file_association(assoc)


def clear_file_associations(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    params = strip_none(kwargs)
    req = agilicus.ClearFileAssociationRequest(**params)
    return apiclient.files_api.create_file_association_clear_task(req)


_ASSOC_COLUMNS = [
    metadata_column("id"),
    spec_column("org_id"),
    spec_column("file_id"),
    spec_column("object_id"),
]


def format_file_associations(ctx, file_associations):
    columns = _ASSOC_COLUMNS
    return format_table(ctx, file_associations, columns)


def format_cleared_associations(ctx, cleared_associations):
    file_columns = [
        column("id"),
        column("name"),
        column("tag"),
    ]
    columns = [
        subtable(ctx, "deleted_associations", _ASSOC_COLUMNS),
        subtable(ctx, "pending_delete_files", file_columns),
    ]

    return format_table(ctx, cleared_associations, columns)
