# -*- coding: utf-8 -*-
"""kacl.kacl-cli: provides entry point main()."""
import json
import os
import sys
import traceback
from datetime import datetime

import click
import git
import semver

import kacl
from kacl.config import KACLConfig
from kacl.exception import KACLException


def check_auto_increment(version):
    # check if the version string indicates automatic increment
    increment = None
    if version in ["major", "minor", "patch", "post"]:
        increment = version
        version = None  # reset
    else:
        # check if version is a valid semantic version
        try:
            semver.VersionInfo.parse(version)
        except Exception:
            click.echo(
                click.style("Error: ", fg="red")
                + f'"{version}" not a valid semantic version.'
            )
            sys.exit(1)

    return version, increment


def raise_on_invalid(kacl_changelog):
    if not kacl_changelog.is_valid():
        click.echo(
            click.style("Error: ", fg="red")
            + "Changelog is not valid. Run 'kacl-cli verify' for more information."
        )
        sys.exit(1)


def load_changelog(ctx, load_stash_files=True):
    config_file_path = ctx.obj["config"]
    input_file = ctx.obj["file"]

    default_config_path = os.path.join(os.getcwd(), ".kacl.yml")
    if not config_file_path and os.path.exists(default_config_path):
        kacl_config = KACLConfig(default_config_path)
    elif config_file_path:
        kacl_config = KACLConfig(config_file_path)
    else:
        kacl_config = KACLConfig()

    if input_file:
        kacl_config.changelog_file_path = input_file

    if not os.path.exists(kacl_config.changelog_file_path):
        click.echo(
            click.style("Error: ", fg="red")
            + f"{kacl_config.changelog_file_path} not found"
        )
        sys.exit(1)

    # read the changelog
    kacl_changelog = kacl.load(kacl_config.changelog_file_path)
    kacl_changelog.config = kacl_config
    if load_stash_files:
        kacl_changelog.load_stash()

    # share the objects
    return kacl_changelog


def prefixed_environ():
    return dict((("${}".format(key), value) for key, value in os.environ.items()))


@click.group(invoke_without_command=True)
@click.option(
    "-v",
    "--version",
    is_flag=True,
    required=False,
    help="Prints the current version of the CLI.",
)
@click.option(
    "-c",
    "--config",
    required=False,
    default=None,
    type=click.Path(exists=False, dir_okay=False, file_okay=True),
    help="Path to kacl config file.",
    show_default=True,
)
@click.option(
    "-f",
    "--file",
    required=False,
    default=None,
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="Path to changelog file.",
    show_default=True,
)
@click.pass_context
def cli(ctx, version=None, config=None, file=None):
    if ctx.obj is None:
        ctx.obj = dict()

    ctx.obj["config"] = config
    ctx.obj["file"] = file

    # if --version was given, print version and exit directly
    if version:
        click.echo(kacl.__version__)
        sys.exit(0)


@cli.command()
@click.pass_context
@click.argument("section", type=str)
@click.argument("message", type=str)
@click.option(
    "-m",
    "--modify",
    is_flag=True,
    help="This option will add the changes directly into changelog file.",
)
@click.option(
    "-s",
    "--stash",
    is_flag=True,
    help="This option will stash changes instead of applying them.",
)
def add(ctx, section, message, modify, stash):
    """Adds a given message to a specified unreleased section. Use '--modify' to directly modify the changelog file."""
    kacl_changelog = load_changelog(ctx)

    if not modify:
        stash = False
    else:
        # check if we need to stash
        stash = stash or kacl_changelog.config.stash_always

    # add changes to changelog
    kacl_changelog.add(section=section, data=message, stash=stash)

    kacl_changelog_content = kacl.dump(kacl_changelog)
    # if stashing is enabled, do not modify the changelog file
    if modify:
        if not stash:
            with open(kacl_changelog.config.changelog_file_path, "w") as f:
                f.write(kacl_changelog_content)
            f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.pass_context
@click.option(
    "-m",
    "--modify",
    is_flag=True,
    help="This option will modify the changelog file directly.",
)
def stash(ctx, modify):
    """Moves all unreleased changes from the changelog to the stash."""
    # Load changelog WITHOUT loading stash files to avoid circular stashing
    kacl_changelog = load_changelog(ctx, load_stash_files=False)

    # Check if there are changes to stash
    if not kacl_changelog.has_changes():
        click.echo(
            click.style("Info: ", fg="yellow") + "No unreleased changes to stash."
        )
        return

    # Stash the unreleased changes
    kacl_changelog.stash_unreleased()

    stash_file = kacl_changelog._get_stash_file()
    click.echo(
        click.style("Success: ", fg="green")
        + f"Unreleased changes have been moved to {stash_file}"
    )

    # Update the changelog file if modify flag is set
    if modify:
        kacl_changelog_content = kacl.dump(kacl_changelog)
        with open(kacl_changelog.config.changelog_file_path, "w") as f:
            f.write(kacl_changelog_content)
        f.close()
        click.echo(
            click.style("Success: ", fg="green")
            + f"Changelog file {kacl_changelog.config.changelog_file_path} has been updated."
        )
    else:
        # Just print the modified changelog
        kacl_changelog_content = kacl.dump(kacl_changelog)
        click.echo(kacl_changelog_content)


@cli.command()
@click.pass_context
def current(ctx):
    """Returns the current version from the Changelog."""
    kacl_changelog = load_changelog(ctx)

    current_version = kacl_changelog.current_version()
    click.echo(current_version)


@cli.command()
@click.pass_context
@click.argument("version", type=str)
def next(ctx, version):
    """Returns the next version based on the current version from the Changelog."""
    kacl_changelog = load_changelog(ctx)
    raise_on_invalid(kacl_changelog)

    version, increment = check_auto_increment(version)

    if increment:
        version = kacl_changelog.next_version(increment=increment)

    # check that version is a valid semantic version
    future_version = semver.VersionInfo.parse(
        version
    )  # --> will throw a ValueError if version is not a valid semver

    click.echo(future_version)


@cli.command()
@click.pass_context
@click.argument("version", type=str)
@click.option(
    "--no-link",
    is_flag=True,
    help="This option suppresses a link, even if available.",
)
@click.option(
    "--no-header",
    is_flag=True,
    help="This option suppresses the header and link.",
)
def get(ctx, version, no_link, no_header):
    """Returns a given version from the Changelog."""
    kacl_changelog = load_changelog(ctx)

    # add changes to changelog
    kacl_version = kacl_changelog.get(version)

    if kacl_version:
        if no_header:
            kacl_changelog_content = kacl.dump(kacl_version.sections())
            click.echo(kacl_changelog_content)
        else:
            if no_link:
                kacl_version.set_link(None)
            kacl_changelog_content = kacl.dump(kacl_version)
            click.echo(kacl_changelog_content)
    else:
        click.echo(
            click.style("Error: ", fg="red")
            + f'"{version}" could not be found in changelog.'
        )
        sys.exit(1)


@cli.group(invoke_without_command=True)
@click.pass_context
def link(ctx):
    """Lets you modify version links"""
    pass


@link.command()
@click.pass_context
@click.option(
    "-m",
    "--modify",
    is_flag=True,
    help="This option will add the changes directly into changelog file.",
)
@click.option(
    "--host-url",
    required=False,
    default=None,
    type=str,
    help="Host url to the git service. (i.e https://github.com/mschmieder/python-kacl)",
    show_default=True,
)
@click.option(
    "--compare-versions-template",
    required=False,
    default=None,
    type=str,
    help="Template string for version comparison link.",
    show_default=True,
)
@click.option(
    "--unreleased-changes-template",
    required=False,
    default=None,
    type=str,
    help="Template string for unreleased changes link.",
    show_default=True,
)
@click.option(
    "--initial-version-template",
    required=False,
    default=None,
    type=str,
    help="Template string for initial version link.",
    show_default=True,
)
def generate(
    ctx,
    modify,
    host_url,
    compare_versions_template,
    unreleased_changes_template,
    initial_version_template,
):
    kacl_changelog = load_changelog(ctx)

    kacl_changelog.generate_links(
        host_url=host_url,
        compare_versions_template=compare_versions_template,
        unreleased_changes_template=unreleased_changes_template,
        initial_version_template=initial_version_template,
    )

    kacl_changelog_content = kacl.dump(kacl_changelog)
    if modify:
        with open(kacl_changelog.config.changelog_file_path, "w") as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.pass_context
@click.option(
    "--json", "as_json", is_flag=True, help="Print validation output as json."
)
def verify(ctx, as_json):
    """Verifies if the changelog is in "keep-a-changelog" format.
    Use '--json' get JSON formatted output that can be easier integrated into CI workflows.
    Exit code is the number of identified errors.
    """
    kacl_changelog = load_changelog(ctx)
    kacl_changelog_filepath = os.path.basename(
        kacl_changelog.config.changelog_file_path
    )

    validation = kacl_changelog.validate()
    valid = len(validation.errors()) < 1

    if as_json:
        validation_map = validation.convert_to_dict()
        click.echo(json.dumps(validation_map, sort_keys=True, indent=4))
    else:
        for error in validation.errors():
            start_char_pos, end_char_pos = error.position()

            char_indicator = start_char_pos
            if start_char_pos is None:
                char_indicator = 0

            click.echo(
                click.style(
                    kacl_changelog_filepath
                    + ":"
                    + f"{error.line_number()}:{char_indicator}: "
                    + click.style("error: ", fg="red")
                    + error.error_message(),
                    bold=True,
                )
            )

            if error.line():
                click.echo(error.line())
                if start_char_pos is not None and end_char_pos is not None:
                    mark_length = end_char_pos - start_char_pos - 1
                    click.echo(
                        " " * start_char_pos
                        + click.style("^" + "~" * (mark_length), fg="green")
                    )
        if not valid:
            click.echo(f"{len(validation.errors())} error(s) generated.")
        else:
            click.secho("Success", fg="green")

    if not valid:
        sys.exit(len(validation.errors()))


@cli.command()
@click.pass_context
@click.argument("version", type=str)
@click.option(
    "-m",
    "--modify",
    is_flag=True,
    help="This option will add the changes directly into changelog file.",
)
@click.option(
    "-l",
    "--link",
    required=False,
    default=None,
    type=str,
    help="A url that the version will be linked with.",
    show_default=True,
)
@click.option(
    "-g",
    "--auto-link",
    is_flag=True,
    help="Will automatically create and update necessary links.",
)
@click.option(
    "-c",
    "--commit",
    is_flag=True,
    help="If passed this will create a git commit with the changed Changelog.",
)
@click.option(
    "--no-commit",
    is_flag=True,
    help="This will disabled the commit option even if it is set in the config.",
)
@click.option(
    "--commit-message",
    required=False,
    default=None,
    type=str,
    help="The commit message to use when using --commit flag",
)
@click.option(
    "-t",
    "--tag",
    is_flag=True,
    help="If passed this will create a git tag for the newly released version.",
)
@click.option(
    "--tag-name",
    required=False,
    default=None,
    type=str,
    help="The tag name to use when using --tag flag",
)
@click.option(
    "--tag-description",
    required=False,
    default=None,
    type=str,
    help="The tag description text to use when using --tag flag",
)
@click.option(
    "-d",
    "--allow-dirty",
    is_flag=True,
    help='If passed this will allow to commit/tag even on a "dirty".',
)
@click.option(
    "--allow-no-changes",
    is_flag=True,
    help="If passed this will allow to release without any changes.",
)
def release(
    ctx,
    version,
    modify,
    link,
    auto_link,
    commit,
    no_commit,
    commit_message,
    tag,
    tag_name,
    tag_description,
    allow_dirty,
    allow_no_changes,
):
    """Creates a release for the latest 'unreleased' changes. Use '--modify' to directly modify the changelog file.
    You can automatically use the latest version by using the version keywords 'major', 'minor', 'patch', 'post'

    Example:

        kacl-cli release 1.0.0

        kacl-cli release major|minor|patch|post
    """
    kacl_changelog = load_changelog(ctx)
    kacl_config = kacl_changelog.config
    raise_on_invalid(kacl_changelog)

    version, increment = check_auto_increment(version)

    if not allow_no_changes and not kacl_changelog.has_changes():
        click.echo(
            click.style("Error: ", fg="red")
            + "The current changelog has no changes. You can only release if changes are available."
        )
        sys.exit(1)

    # get the latest_version before the release
    latest_version = kacl_changelog.current_version()

    # check config to see if we need to autogenerate changes
    if auto_link is False and kacl_config.link_auto_generate:
        auto_link = True

    kacl_changelog.release(
        version=version,
        link=link,
        auto_link=auto_link,
        increment=increment,
        allow_no_changes=allow_no_changes,
    )

    # get the new version
    new_version = kacl_changelog.current_version()

    # dump the content
    kacl_changelog_content = kacl.dump(kacl_changelog)

    # check if we should modify the file
    if modify:
        with open(kacl_changelog.config.changelog_file_path, "w") as f:
            f.write(kacl_changelog_content)
        f.close()

        if no_commit:
            return

        # delete all file in the stash directory
        stash_files = []
        for f in os.listdir(kacl_changelog.stash_directory):
            stash_file = os.path.join(kacl_changelog.stash_directory, f)
            os.remove(stash_file)
            stash_files.append(stash_file)

        if commit or tag or kacl_config.git_create_commit or kacl_config.git_create_tag:
            vcs_context = {
                "latest_version": latest_version,
                "new_version": new_version,
            }
            time_context = {
                "now": datetime.now(),
                "utcnow": datetime.utcnow(),
            }
            vcs_context.update(time_context)
            vcs_context.update(prefixed_environ())

            commit_message = (
                commit_message
                if commit_message is not None
                else kacl_config.git_commit_message
            )
            tag_name = tag_name if tag_name is not None else kacl_config.git_tag_name
            tag_description = (
                tag_description
                if tag_description is not None
                else kacl_config.git_tag_description
            )

            repo = None
            try:
                repo = git.Repo(os.getcwd())
            except git.InvalidGitRepositoryError:
                click.echo(
                    click.style("Error: ", fg="red")
                    + f'"{os.getcwd()}" is no valid git repository.'
                )

            if repo:
                if not repo.is_dirty() and not allow_dirty:
                    click.echo(
                        click.style("Error: ", fg="red")
                        + "Repository is marked 'dirty'. Use --allow-dirty if you want to commit/tag on a dirty repository"
                    )

                if commit or kacl_config.git_create_commit:
                    repo.git.add(kacl_config.changelog_file_path)
                    for f in kacl_config.git_commit_additional_files:
                        repo.git.add(f)
                    for f in stash_files:
                        try:
                            repo.git.add(f)
                        except git.GitCommandError:
                            pass
                    repo.git.commit("-m", commit_message.format(**vcs_context))

                if tag or kacl_config.git_create_tag:
                    repo.create_tag(
                        tag_name.format(**vcs_context),
                        message=tag_description.format(**vcs_context),
                    )
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.pass_context
@click.option(
    "-m",
    "--modify",
    is_flag=True,
    help="This option will add the changes directly into changelog file.",
)
@click.option(
    "--from-version",
    required=True,
    default=None,
    type=str,
    help="The version to start squashing from.",
)
@click.option(
    "--to-version",
    required=False,
    default=None,
    type=str,
    help="The version to squash to. If not given, the latest version will be used.",
)
def squash(
    ctx,
    modify,
    from_version,
    to_version,
):
    """Squshes all changes from a given version into a single section. Use '--modify' to directly modify the changelog file."""

    kacl_changelog = load_changelog(ctx)
    raise_on_invalid(kacl_changelog)

    if not to_version:
        to_version = kacl_changelog.current_version()
    else:
        try:
            to_version = semver.VersionInfo.parse(to_version)
        except Exception:
            click.echo(
                click.style("Error: ", fg="red")
                + f'"{to_version}" not a valid semantic version.'
            )
            sys.exit(1)

    try:
        from_version = semver.VersionInfo.parse(from_version)
    except Exception:
        click.echo(
            click.style("Error: ", fg="red")
            + f'"{from_version}" not a valid semantic version.'
        )
        sys.exit(1)

    # squash the changes
    kacl_changelog.squash(
        version_start=from_version, version_end=to_version, keep_version_info=True
    )

    # dump the content
    kacl_changelog_content = kacl.dump(kacl_changelog)

    # check if we should modify the file
    if modify:
        with open(kacl_changelog.config.changelog_file_path, "w") as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.option(
    "-o",
    "--output-file",
    required=False,
    type=click.Path(exists=False),
    help="File to write the created changelog to.",
)
def new(output_file):
    """Creates a new changelog."""
    kacl_changelog = kacl.new()
    kacl_changelog_content = kacl.dump(kacl_changelog)
    if output_file:
        with open(output_file, "w") as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.option(
    "-f",
    "--force",
    required=False,
    is_flag=True,
    help="Will overwrite existing files.",
)
def init(force):
    """Initializes a project with all necessary kacl setting."""
    kacl_changelog = kacl.new()
    kacl_changelog_content = kacl.dump(kacl_changelog)

    if os.path.exists("CHANGELOG.md") and not force:
        click.echo(
            click.style("Error: ", fg="red")
            + "CHANGELOG.md already exists. Use '--force' to overwrite."
        )
        sys.exit(1)

    if os.path.exists(".kacl.yml") and not force:
        click.echo(
            click.style("Error: ", fg="red")
            + ".kacl.yml already exists. Use '--force' to overwrite."
        )
        sys.exit(1)

    with open("CHANGELOG.md", "w") as f:
        f.write(kacl_changelog_content)
    f.close()

    default_config_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config", "kacl-default.yml"
    )

    # copy the default config file
    if os.path.exists(default_config_file):
        with open(default_config_file, "r") as df:
            default_config_content = df.read()
        df.close()

        with open(".kacl.yml", "w") as cf:
            cf.write(default_config_content)
        cf.close()


@cli.command("add-comments")
@click.pass_context
@click.option(
    "--jira-username",
    required=False,
    type=str,
    default=os.getenv(
        "JIRA_USERNAME",
        None,
    ),
    help="JIRA username. Will also look for JIRA_USERNAME environment variable.",
)
@click.option(
    "--jira-password",
    required=False,
    type=str,
    default=os.getenv(
        "JIRA_PASSWORD",
        None,
    ),
    help="JIRA password. Will also look for JIRA_PASSWORD environment variable.",
)
@click.option(
    "--jira-host",
    required=False,
    type=str,
    default=os.getenv(
        "JIRA_HOST",
        None,
    ),
    help="JIRA host. Will also look for JIRA_HOST environment variable.",
)
@click.option(
    "--jira-issue-pattern",
    required=False,
    multiple=True,
    help="Issue pattern to search the changlog for. Can be specified multiple times.",
)
@click.option(
    "--jira-comment-template",
    required=False,
    default=None,
    type=str,
    help="JIRA comment template.",
)
@click.option(
    "--fail",
    is_flag=True,
    help="Will fail if comments could not be added.",
)
@click.argument("version", type=str)
def add_comments(
    ctx,
    version,
    jira_username,
    jira_password,
    jira_host,
    jira_issue_pattern,
    jira_comment_template,
    fail,
):
    """Will add comments to issues identified within the CHANGELOG. Currently supported systems are: [JIRA]"""
    kacl_changelog = load_changelog(ctx)
    kacl_config = kacl_changelog.config

    if jira_host:
        kacl_config.issue_tracker_jira_host = jira_host
    if jira_username:
        kacl_config.issue_tracker_jira_username = jira_username
    if jira_password:
        kacl_config.issue_tracker_jira_password = jira_password
    if jira_issue_pattern:
        kacl_config.issue_tracker_jira_issue_patterns = list(jira_issue_pattern)
    if jira_comment_template:
        kacl_config.issue_tracker_jira_comment_template = jira_comment_template

    raise_on_invalid(kacl_changelog)

    issues = kacl_changelog.get_associated_issues(version)
    for issue_type in issues.keys():
        click.secho(f"Found {len(issues[issue_type])} '{issue_type}' issues", fg="blue")
        for issue in issues[issue_type]:
            click.secho(f"{issue_type}: {issue}")

    report = kacl_changelog.add_comments(version)

    failed = False
    for issue_type in report.keys():
        for issue, success in report[issue_type].items():
            if not success:
                failed = True
                click.secho(f"Failed to add comment to {issue_type}: {issue}", fg="red")

    if fail and failed:
        sys.exit(1)


def start():
    try:
        cli(obj={})
    except SystemExit as e:
        sys.exit(e.code)
    except KACLException as e:
        click.secho(str(e), fg="red")
        sys.exit(1)
    except Exception:
        click.echo(traceback.format_exc())
        sys.exit(1)


# if __name__ == "__main__":
#     start()
