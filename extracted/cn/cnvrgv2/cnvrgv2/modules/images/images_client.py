import re

from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.images.image import Image
from cnvrgv2.modules.images.utils import ImageLogos, TAG_VALIDATION_REGEX, NAME_VALIDATION_REGEX
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.utils.url_utils import urljoin


class ImagesClient:
    def __init__(self, organization):
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._proxy = Proxy(context=self._context)
        self._route = routes.IMAGES_BASE.format(scope["organization"])

    def list(self, sort="-id"):
        """
        List all images in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields image objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=Image,
            sort=sort
        )

    def create(self, name, tag, registry="local", logo="", custom=False, dockerfile="", readme=""):
        """
        Create a new image
        @param name: [String] The image name
        @param tag: [String] The image tag
        @param registry: [String] The registry slug (Must be a custom registry to build a custom image)
        @param logo: [String] The image logo (to be displayed in the UI) - defaults to docker
        @param custom: [String] whether the image is custom (needs to be built)
        @param dockerfile: [String] The dockerfile with which to build the image
        @param readme: [String] Image readme (will be displayed in the UI)
        @return: [Image object] The newly created image
        """

        if not tag or not isinstance(tag, str) or not re.match(TAG_VALIDATION_REGEX, tag):
            raise CnvrgArgumentsError(error_messages.IMAGE_BAD_TAG)

        if not name or not isinstance(name, str) or not re.match(NAME_VALIDATION_REGEX, name):
            raise CnvrgArgumentsError(error_messages.IMAGE_BAD_NAME)

        if not registry or not isinstance(registry, str):
            raise CnvrgArgumentsError(error_messages.IMAGE_BAD_REGISTRY)

        if not ImageLogos.validate_icon(logo):
            raise CnvrgArgumentsError(error_messages.IMAGE_BAD_LOGO)

        if custom and not dockerfile:
            raise CnvrgArgumentsError(error_messages.IMAGE_CUSTOM_DOCKERFILE_REQUIRED)

        attributes = {
            "tag": tag,
            "name": name,
            "logo": logo,
            "is_custom": bool(custom),
            "registry_slug": registry,
            "readme": readme,
            "dockerfile": dockerfile,
        }
        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="image", attributes=attributes)
        )

        slug = response.attributes['slug']
        return Image(context=self._context, slug=slug)

    def get(self, slug=None, name=None, tag=None):
        """
        Retrieves an Image by the given slug, or name and tag
        @param slug: [String] The slug of the requested image
        @param tag: [String] The image tag
        @param name: [String] The image name
        @return: Image object
        """

        if slug and isinstance(slug, str):
            return Image(context=self._context, slug=slug)
        elif not slug and (name and tag):
            res_attributes = self._proxy.call_api(
                route=urljoin(self._route, routes.GET_BY_NAME_SUFFIX),
                http_method=HTTP.GET,
                payload={"image_name": name, "image_tag": tag}
            ).attributes

            return Image(context=self._context, slug=res_attributes['slug'], attributes=res_attributes)
        else:
            raise CnvrgArgumentsError(error_messages.IMAGE_GET_FAULTY_PARAMS)

    def delete(self, slug):
        """
        Delete an image by its slug
        @param slug: [String] Image slug
        @return: None
        """

        Image(context=self._context, slug=slug).delete()
