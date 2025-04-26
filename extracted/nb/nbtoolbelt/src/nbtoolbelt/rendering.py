"""
Functions for rendering

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.

Parts of this code are reworked from the rendernb checklet for Momotor <momotor.org>.
"""

from argparse import Namespace
from typing import Any, Dict

from nbconvert import HTMLExporter
from nbformat import NotebookNode
from traitlets.config import Config

from .inline_attachments import InlineAttachmentsPreprocessor


# ADDITIONAL_STYLES = dedent("""\
#     div.inner_cell, div.output_subarea {
#       flex: 1 auto !important;
#     }
#     """)
#
# HTML_FRAME = dedent("""\
#     <html>
#     <head>
#     <style>
#     {css}
#     </style>
#     <script>
#     {javascript}
#     </script>
#     </head>
#     <body>
#     {body}
#     </body>
#     </html>
#     """)


def render_nb(notebook: NotebookNode, args: Namespace) -> Dict[str, Any]:
    """Render notebook as html.
    Uses ``args.template`` as template name.

    :param notebook: notebook to render
    :param args: options
    :return: html
    """
    resources = {}

    iapp = InlineAttachmentsPreprocessor()
    notebook, resources = iapp.preprocess(notebook, resources)

    c = Config()
    c.HTMLExporter.template_name = args.template
    # TODO also set extra_template_basedirs from option?
    html_exporter = HTMLExporter(config=c)

    html, resources = html_exporter.from_notebook_node(notebook)

    # properties = {
    #     'body': html,
    #     'css': '',
    #     'javascript': ''
    # }

    # return HTML_FRAME.format(**properties)
    return html
