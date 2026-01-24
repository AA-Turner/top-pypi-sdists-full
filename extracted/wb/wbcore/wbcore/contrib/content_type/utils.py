from contextlib import suppress

from django.contrib.contenttypes.models import ContentType


def get_ancestors_content_type(content_type):
    """
    Utility function to gather the ascendant models content types
    Returns a generator
    class A:
        ...

    Class B(A):
        ...

    get_ascendant_content_types(ContentType.objects.get_for_model(B)) = [
        ContentType.objects.get_for_model(A),
        ContentType.objects.get_for_model(B)
    ]
    """
    for _class in content_type.model_class().__mro__:
        with suppress(Exception):
            ancestor_content_type = ContentType.objects.get_for_model(_class)
            if ancestor_content_type.model_class():
                yield ancestor_content_type


def get_view_content_type_id(view):
    model = view.get_queryset().model
    return ContentType.objects.get_for_model(model).id
