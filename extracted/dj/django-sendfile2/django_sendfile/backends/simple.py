from datetime import datetime, timezone
import hashlib

from django.core.files.base import File
from django.http import HttpResponse
from django.views.decorators.http import condition


def generate_etag(request, filepath, **kwargs):
    stat_obj = filepath.stat()
    return hashlib.md5(b"%i%i" % (stat_obj.st_size, stat_obj.st_mtime_ns)).hexdigest()


def last_modified(request, filepath, **kwargs):
    return datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc)


@condition(etag_func=generate_etag, last_modified_func=last_modified)
def sendfile(request, filepath, **kwargs):
    '''Use the SENDFILE_ROOT value composed with the path arrived as argument
    to build an absolute path with which resolve and return the file contents.
    '''
    with File(filepath.open('rb')) as f:
        response = HttpResponse(f.chunks())

    return response
