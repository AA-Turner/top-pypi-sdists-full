# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request Files ui views module."""

from flask import Blueprint, current_app, render_template

from invenio_requests.services.files.errors import RequestFileNotFoundError

from .requests import read_file


def not_found_error(_):
    """Handler for 'Not Found' errors."""
    return render_template(current_app.config["THEME_404_TEMPLATE"]), 404


def create_ui_blueprint(app):
    """Register blueprint routes on app."""
    routes = app.config.get("REQUESTS_ROUTES")

    blueprint = Blueprint(
        "invenio_requests_files",
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # Here we add a non-API endpoint for HTML embedding and downloads,
    # which unlike the API endpoint is not for programmatic file access.
    blueprint.add_url_rule(
        routes["download_file_html"],
        view_func=read_file,
    )

    blueprint.register_error_handler(
        RequestFileNotFoundError,
        not_found_error,
    )

    return blueprint
