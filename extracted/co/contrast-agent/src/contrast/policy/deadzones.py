# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.registry import register_deadzone_nodes


deadzone_nodes = [
    {
        # Prevent recursive propagation when logging in assess
        # We run the risk of recursively logging propagation events inside of log
        # statements. This is because the logging module sometimes uses streams to
        # output logs, and these logging events can inadvertently cause additional
        # log output that we use for debugging within our assess code. We want to
        # prevent this from occurring. Part of the reason for this is that we now
        # instrument stream reads and writes, but we also are aware that StringIO
        # is implemented with a lot of string building under the hood.
        "module": "logging",
        "class_name": "StreamHandler",
        "method_name": "emit",
        "policy_patch": True,
    },
    {
        "module": "contrast_vendor.structlog._output",
        "class_name": "WriteLogger",
        "method_name": "msg",
        "policy_patch": True,
    },
    {
        "module": "loguru._logger",
        "class_name": "Logger",
        "method_name": "_log",
    },
    {
        # Werkzeug's request body parser (used by flask.request.files) causes a lot of
        # propagation. We deadzone this, but we have source nodes / logic for tracking
        # all resulting objects.
        "module": "werkzeug.formparser",
        "class_name": "FormDataParser",
        "method_name": "parse",
    },
    {
        # This method causes potential false positives for unsafe-code-execution.
        # It is presumed safe to deadzone since it is implemented by the framework.
        # The actual issue is caused by the .name attribute but we don't currently
        # support deadzones for properties.
        "module": "werkzeug.exceptions",
        "class_name": "HTTPException",
        "method_name": "get_body",
    },
    {
        # This is django's request body parser. We have source nodes for the objects
        # storing data that is parsed out of the request body here. This deadzone saves
        # us from performing needless propagation without sacrificing any correctness.
        "module": "django.http.request",
        "class_name": "HttpRequest",
        "method_name": "_load_post_and_files",
    },
    {
        # This is DRF's request body parser. See comments for other body parsers.
        "module": "rest_framework.request",
        "class_name": "Request",
        "method_name": "_parse",
    },
    {
        # Built-in request body parser used by at least Bottle and Pyramid. This patch
        # is actually handled explicitly, but the deadzone here is for clarity. We also
        # use cgi.FieldStorage.__init__ as an entrypoint for explicitly patching the
        # relevant attributes of the FieldStorage object itself (as sources).
        "module": "cgi",
        "class_name": "FieldStorage",
        "method_name": "__init__",
        "policy_patch": False,
    },
    {
        # See FieldStorage. It's not essential that we deadzone this, but it keeps
        # MiniFieldStorage and FieldStorage consistent.
        "module": "cgi",
        "class_name": "MiniFieldStorage",
        "method_name": "__init__",
        "policy_patch": False,
    },
    {
        # UUIDs aren't controllable and they're hex encoded. It is essentially
        # impossible for a UUID to trigger a real vulnerability
        "module": "uuid",
        "class_name": "UUID",
        "method_name": "__str__",
    },
    {
        # load_tzdata was reporting false positive vulnerabilities for path traversal
        # and unsafe code execution. The function accesses the filesystem and loads
        # binary data if the provided key is found under the "tzdata.zoneinfo" namespace.
        # That package namespace is within the standard library, so this is effective
        # validation.
        "module": "zoneinfo._common",
        "method_name": "load_tzdata",
    },
    {
        # This currently causes an unvalidated-redirect in the case where the
        # middleware appends a '/' to the request path and redirects. It also
        # causes an unvalidated-redirect in the case where the middleware
        # inserts a "www" subdomain into the request host and redirects.
        "module": "django.middleware.common",
        "class_name": "CommonMiddleware",
        "method_name": "process_request",
    },
    {
        # This currently causes an unvalidated-redirect in the case where the
        # middleware appends a '/' to the request path and redirects on a 404
        # response.
        "module": "django.middleware.common",
        "class_name": "CommonMiddleware",
        "method_name": "process_response",
    },
    {
        # This code is responsible for rendering the django debug page.
        "module": "django.views.debug",
        "class_name": "ExceptionReporter",
        "method_name": "get_traceback_data",
    },
    {
        # This function gets the User ORM object associated with the request's session.
        # To do this, it ends up importing an "authentication backend" based on a string
        # stored in session data. However, the string representing the class being
        # imported is first checked against settings.AUTHENTICATION_BACKENDS, so it's
        # impossible for this function to lead to unsafe code execution. See PYT-3165.
        "module": "django.contrib.auth",
        "method_name": "get_user",
    },
    {
        # `django-enumfields` is an extension that provides extra django-specific
        # behavior for enum database types when using the django ORM. `from_db_value`
        # is a special method to be defined by concrete classes based on
        # django.db.models.Field - it is used to convert values directly from the
        # database into python objects. We're not concerned about deadzoning this
        # function for enumfields for two main reasons:
        #
        # 1. It should never be possible to receive tracked data from a database. There
        #    might be an exception for stored XSS but we're accepting that gap if it
        #    exists. This means that no meaningful dataflow should be able to take place
        #    within this function in the first place.
        # 2. The only actual dataflow in `from_db_value` occurs when formatting the
        #    exception message for its failure case. Even if tracked data somehow enters
        #    this function, we would only lose propagation into this exception message.
        #    It's unlikely this message would find its way to a trigger (xss is probably
        #    the only possibility, if http responses for server exceptions include
        #    unsanitized error messages, but this seems like a stretch).
        #
        # See PYT-3321.
        "module": "enumfields.fields",
        "class_name": "EnumFieldMixin",
        "method_name": "from_db_value",
    },
    {
        # Too much propagation / source creation occurs here. It is not necessary for
        # body tracking since we accomplish this with higher-level source nodes
        "module": "quart.wrappers.request",
        "class_name": "Request",
        "method_name": "_load_form_data",
    },
    {
        # Prevents our rewriter from being applied to assertion rewrites in pytest
        "module": "_pytest.assertion.rewrite",
        "class_name": "AssertionRewritingHook",
        "method_name": "exec_module",
    },
]


register_deadzone_nodes(deadzone_nodes)
