# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_source_nodes
from contrast.agent.policy.utils import CompositeNode

django_sources = [
    CompositeNode(
        {
            "module": "django.http.request",
            "class_name": "HttpRequest",
        },
        [
            {
                "method_name": [
                    "get_host",
                    "get_port",
                    "get_full_path",
                    "get_full_path_info",
                    "get_raw_uri",
                    "build_absolute_uri",
                ],
                "node_type": "URI",
                "tags": ["CROSS_SITE"],
            },
            {
                "method_name": ["body", "read"],
                "node_type": "BODY",
                "tags": ["CROSS_SITE"],
            },
            {
                "method_name": ["encoding"],
                "node_type": "OTHER",
                "tags": ["CROSS_SITE"],
            },
        ],
    ),
    CompositeNode(
        {
            "module": "django.http.request",
            "class_name": "HttpHeaders",
        },
        [
            {
                # Header can't trigger XSS unless the key is Referer
                "method_name": "__getitem__",
                "node_type": "HEADER",
                "tags": ["NO_NEWLINES"],
            },
            {
                # Header key can't trigger XSS
                "method_name": "keys",
                "node_type": "HEADER_KEY",
                "tags": ["NO_NEWLINES"],
            },
        ],
    ),
    {
        "module": "django.utils.datastructures",
        "class_name": "MultiValueDict",
        "method_name": "__getitem__",
        "node_type": "PARAMETER",
        "tags": ["CROSS_SITE"],
    },
    {
        # This was added to handle file uploads in Django REST Framework.
        # For regular Django, this is redundant with the file tracker in middleware
        "module": "django.core.files.uploadedfile",
        "class_name": "UploadedFile",
        "method_name": "__init__",
        "target": "ARG_0,KWARG:file",
        "node_type": "MULTIPART_CONTENT_DATA",
        "tags": ["CROSS_SITE"],
    },
]


register_source_nodes(django_sources)
