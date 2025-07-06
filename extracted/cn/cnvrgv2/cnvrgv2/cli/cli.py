import codecs
import locale
import os
import sys

import click
from cnvrgv2._version import __version__

from cnvrgv2.cli.logger.logger import CnvrgLogger
from cnvrgv2.cli.modules.config import config
from cnvrgv2.cli.modules.dataset.dataset import dataset_group
from cnvrgv2.cli.modules.images.images import image_group
from cnvrgv2.cli.modules.libraries.library import library_group
from cnvrgv2.cli.modules.logs.logs import logs
from cnvrgv2.cli.modules.members.members import members_group
from cnvrgv2.cli.modules.labels.labels import labels_group
from cnvrgv2.cli.modules.organization_settings.organization_settings import organization_settings_group
from cnvrgv2.cli.modules.project.endpoint import endpoint_group
from cnvrgv2.cli.modules.project.experiment import experiment_group
from cnvrgv2.cli.modules.project.project import project_group
from cnvrgv2.cli.modules.project.workspace import workspace_group
from cnvrgv2.cli.modules.project.webapp import webapp_group
from cnvrgv2.cli.modules.project.flows import flow_group
from cnvrgv2.cli.modules.registries.registries import registry_group
from cnvrgv2.cli.modules.ssh.ssh import ssh_group
from cnvrgv2.cli.modules.storage_class.storage_class import storage_class_group
from cnvrgv2.cli.modules.datasource.datasource import datasource_group
from cnvrgv2.cli.modules.users import users
from cnvrgv2.cli.modules.volumes.volume import volume_group
from cnvrgv2.cli.utils import messages
from cnvrgv2.errors import CnvrgLoginError


"""
To avoid issues reading unicode chars from stdin or writing to stdout, we need to ensure that the
python3 runtime is correctly configured, if not, we try to force to utf-8.
"""
if codecs.lookup(locale.getpreferredencoding()).name == 'ascii':
    utf_8_locales = set([loc for loc in locale.locale_alias.values() if loc.lower().endswith((".utf-8", ".utf8"))])
    english_locales = [loc for loc in utf_8_locales if loc.lower().startswith('en_us')]

    if len(english_locales) > 0:
        os.environ['LANG'] = english_locales[0]
        os.environ['LC_ALL'] = english_locales[0]

    if codecs.lookup(locale.getpreferredencoding()).name == 'ascii':
        print("Could not set locale variable automatically.")
        print("Please set the LANG and LC_ALL env variables to a proper value before calling this script.")
        print("The following suitable locales were discovered:")
        print(', '.join('{}'.format(k) for k in utf_8_locales))
        sys.exit(-1)


@click.group()
@click.version_option(__version__, "-v", "--version",
                      message="%(prog)s %(version)s")
def entry_point():
    pass


def safe_entry_point():
    try:
        entry_point()
    except CnvrgLoginError as e:
        click.echo(str(e), err=True)
        exit(1)
    except Exception as e:
        click.echo(messages.CLI_UNEXPECTED_ERROR.format(str(e)), err=True)
        exit(1)


entry_point.add_command(logs)
entry_point.add_command(config)
entry_point.add_command(ssh_group)
entry_point.add_command(image_group)
entry_point.add_command(users.login)
entry_point.add_command(users.logout)
entry_point.add_command(users.me)
entry_point.add_command(flow_group)
entry_point.add_command(project_group)
entry_point.add_command(library_group)
entry_point.add_command(members_group)
entry_point.add_command(labels_group)
entry_point.add_command(dataset_group)
entry_point.add_command(endpoint_group)
entry_point.add_command(registry_group)
entry_point.add_command(workspace_group)
entry_point.add_command(experiment_group)
entry_point.add_command(webapp_group)
entry_point.add_command(organization_settings_group)
entry_point.add_command(CnvrgLogger.set_logs_keep_duration)
entry_point.add_command(storage_class_group)
entry_point.add_command(volume_group)
entry_point.add_command(datasource_group)
