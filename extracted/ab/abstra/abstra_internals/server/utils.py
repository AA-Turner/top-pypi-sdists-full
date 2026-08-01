import inspect
import mimetypes
import typing
from pathlib import Path

import flask
import werkzeug.exceptions as wz_ex

import abstra_statics

dist_folder = Path(inspect.getfile(abstra_statics)).joinpath("../dist").resolve()
_DIST_FOLDER = dist_folder  # stable reference for the bundle check below

_IMMUTABLE_CACHE_CONTROL = "public, max-age=31536000, immutable"


def _immutable_cache_control(
    *, from_bundle: bool, filename: str
) -> typing.Optional[str]:
    if from_bundle and filename.startswith("assets/"):
        return _IMMUTABLE_CACHE_CONTROL
    return None


def send_from_dist(
    filename: str,
    fallback: typing.Optional[str] = None,
    dist_folder: Path = dist_folder,
):
    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("text/html", ".html")

    try:
        response = flask.send_from_directory(dist_folder, filename)
    except wz_ex.NotFound:
        if fallback is None:
            return flask.Response(status=404)
        return flask.send_from_directory(dist_folder, fallback)

    cache_control = _immutable_cache_control(
        from_bundle=dist_folder == _DIST_FOLDER, filename=filename
    )
    if cache_control is not None:
        response.headers["Cache-Control"] = cache_control

    return response
