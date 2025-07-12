"""
The purpose of this file is a little bit of cleverness to allow us to use the CLI in this package across
metaflow and outerbounds projects.

The issue is that since outerbounds and metaflow both vendor click, we can't use object from one import path
and expect them to work with objects created from the other import path.

Meaning `outerbounds._vendor.click.Group` and `metaflow._vendor.click.Group` are different classes.
So we need to ensure that based on when the import is taking place, we import the correct class.

Overall, this ONLY affects constructs in click we are using to construct related to the  cli decorators but
it doesn't affect any capabilities in click for logging.
"""
import os

# Import Hacks
if os.environ.get("APPS_CLI_LOADING_IN_OUTERBOUNDS", None):
    from outerbounds._vendor import click as outerbounds_click

    click = outerbounds_click  # type: ignore
else:
    from metaflow._vendor import click as metaflow_click

    click = metaflow_click  # type: ignore
