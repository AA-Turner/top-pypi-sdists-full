# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_source_nodes
from contrast.agent.policy.utils import CompositeNode

flask_sources = [
    CompositeNode(
        {
            "module": "flask.wrappers",
            "class_name": "Request",
        },
        [
            {
                "method_name": "form",
                "node_type": "MULTIPART_FORM_DATA",
                "tags": ["CROSS_SITE"],
            },
            {
                "method_name": "get_data",
                "node_type": "BODY",
                "tags": ["CROSS_SITE"],
            },
            {
                "method_name": "cookies",
                "node_type": "COOKIE",
                "tags": ["NO_NEWLINES"],
            },
            {
                "method_name": [
                    "path",
                    "full_path",
                    "base_url",
                    "host_url",
                    "url",
                    "url_root",
                ],
                "node_type": "URI",
                "tags": ["CROSS_SITE"],
            },
        ],
    ),
    CompositeNode(
        {
            "module": "werkzeug.datastructures",
            "class_name": "MultiDict",
        },
        [
            {
                # MultiDict is the storage class for user input parsed from
                # wsgi.input and other sources of user input from environ.
                # Parsing of wsgi.input is deadzoned so we need to track
                # what comes out of this dict.
                # getlist uses the Python dict
                # __getitem__ so we cannot rely on __getitem__ for patching
                "method_name": ["__getitem__", "getlist"],
                "node_type": "PARAMETER",
                "tags": ["CROSS_SITE"],
            },
        ],
    ),
    {
        # Flask uses werkzeug TypeConversionDict as its dict storage class.
        # Cannot patch __getitem__ as it uses Python's dict __getitem__
        "module": "werkzeug.datastructures",
        "class_name": "TypeConversionDict",
        "method_name": "get",
        "node_type": "PARAMETER",
        "tags": ["CROSS_SITE"],
    },
]


register_source_nodes(flask_sources)
