from django.views.static import serve


def sendfile(request, filepath, **kwargs):
    """
    Send file using Django dev static file server.

    .. warning::

        Do not use in production. This is only to be used when developing and
        is provided for convenience only
    """
    return serve(request, filepath.name, document_root=filepath.parent)
