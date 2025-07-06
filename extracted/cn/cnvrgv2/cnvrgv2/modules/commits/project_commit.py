from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes


class ProjectCommit(DynamicAttributes):
    available_attributes = {
        "sha1": str,
        "source": str,
        "message": str,
        "created_at": str
    }

    def __init__(self, context=None, slug=None, attributes=None):
        self._context = context
        self._slug = slug
        self._attributes = attributes or {}
