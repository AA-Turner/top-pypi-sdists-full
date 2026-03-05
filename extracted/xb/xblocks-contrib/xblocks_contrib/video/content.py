"""
Video Block Static Content.

Class copied from StaticContent class in edx-platform/xmodule/contentstore/content.py
"""
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import AssetKey
from opaque_keys.edx.locator import AssetLocator


class VideoBlockStaticContent:
    """
    Represents static content associated with a video block (such as video files or related assets).
    """
    def __init__(  # pylint: disable=too-many-positional-arguments
        self, loc, name, content_type, data, last_modified_at=None,
        thumbnail_location=None, import_path=None, length=None, locked=False, content_digest=None
    ):
        self.location = loc
        # a display string which can be edited, and thus not part of the location which needs to be fixed
        self.name = name
        self.content_type = content_type
        self._data = data
        self.length = length
        self.last_modified_at = last_modified_at
        self.thumbnail_location = thumbnail_location
        # optional information about where this file was imported from. This is needed to support import/export
        # cycles
        self.import_path = import_path
        self.locked = locked
        self.content_digest = content_digest

    @staticmethod
    def compute_location(course_key, path, revision=None, is_thumbnail=False):  # pylint: disable=unused-argument
        """
        Constructs a location object for static content.

        - course_key: the course that this asset belongs to
        - path: is the name of the static asset
        - revision: is the object's revision information
        - is_thumbnail: is whether or not we want the thumbnail version of this
            asset
        """
        path = path.replace('/', '_')
        return course_key.make_asset_key(
            'asset' if not is_thumbnail else 'thumbnail',
            AssetLocator.clean_keeping_underscores(path)
        ).for_branch(None)

    @staticmethod
    def get_location_from_path(path):
        """
        Generate an AssetKey for the given path (old c4x/org/course/asset/name syntax)
        """
        try:
            return AssetKey.from_string(path)
        except InvalidKeyError:
            # TODO - re-address this once LMS-11198 is tackled.
            if path.startswith('/') or path.endswith('/'):
                # try stripping off the leading slash and try again
                return AssetKey.from_string(path.strip('/'))
            return None

    @staticmethod
    def serialize_asset_key_with_slash(asset_key):
        """
        Legacy code expects the serialized asset key to start w/ a slash; so, do that in one place
        :param asset_key:
        """
        url = str(asset_key)
        if not url.startswith('/'):
            url = '/' + url  # TODO - re-address this once LMS-11198 is tackled.
        return url
