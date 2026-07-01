import datetime
import os

import git
import semver

import kacl
from kacl.config import KACLConfig
from kacl.element import KACLElement
from kacl.exception import KACLException
from kacl.jira_client import KACLJiraClient
from kacl.link_provider import LinkProvider
from kacl.parser import KACLParser
from kacl.utils import convert_markdown_to_jira
from kacl.utils import extract_issue_ids
from kacl.utils import replace_env_variables
from kacl.validation import KACLValidation
from kacl.version import KACLVersion

WINDOWS_LINE_ENDING = r"\r\n"
UNIX_LINE_ENDING = r"\n"


class KACLDocument:
    def __init__(
        self,
        data="",
        headers=None,
        versions=None,
        link_references=None,
        meta_data=None,
        file_path=None,
        config=KACLConfig(),
    ):
        self.__data = data
        self.__headers = headers if headers else []
        self.__versions = versions if versions else []
        self.__link_references = link_references
        if not self.__link_references:
            self.__link_references = dict()
        self.__meta_data = meta_data
        self.config = config
        self.stash = []
        self.file_path = file_path

    @property
    def stash_directory(self):
        return self._ensure_stash_directory()

    def load_stash(self):
        self._refresh_stash()
        # get all unreleased changes from stash
        for stashed_changelog in self.stash:
            unreleased_stash_version = stashed_changelog.get("Unreleased")
            for title, change in unreleased_stash_version.sections().items():
                for change_item in change.items():
                    self.add(section=title, data=change_item)

    def _refresh_stash(self):
        if not self.file_path:
            return

        self.stash = []
        if self.file_path is None:
            local_stash_dir = os.path.join(
                os.path.abspath(os.getcwd()), self.config.stash_dir
            )
        else:
            # the stash needs always to be relative to the current file_path
            local_stash_dir = os.path.join(
                os.path.abspath(os.path.dirname(self.file_path)), self.config.stash_dir
            )

        if not os.path.isdir(local_stash_dir):
            return

        # read all md files in the stash directory
        for f in os.listdir(local_stash_dir):
            if f.endswith(".md"):
                md_file = os.path.join(local_stash_dir, f)
                with open(md_file, "r") as fh:
                    data = fh.read()
                    try:
                        doc = KACLDocument.parse(data, None)
                        self.stash.append(doc)
                    except Exception:
                        continue

    def _ensure_stash_directory(self):
        # the stash needs always to be relative to the current file_path
        local_stash_dir = os.path.join(
            os.path.abspath(os.path.dirname(self.file_path)), self.config.stash_dir
        )

        if not os.path.isdir(local_stash_dir):
            os.makedirs(local_stash_dir, exist_ok=True)

        return local_stash_dir

    def _get_stash_file(self):
        # the stash file should be named after the current git branch
        local_stash_dir = self._ensure_stash_directory()
        try:
            repo = git.Repo(
                os.path.abspath(os.path.dirname(self.file_path)),
                search_parent_directories=True,
            )
            branch_name = repo.active_branch.name
            # sanitize branch name for filename
            branch_name = branch_name.replace("/", "__").replace("\\", "_")
            stash_file_name = f"{branch_name}.md"
        except Exception:
            # fallback to with date
            stash_file_name = f"{datetime.datetime.now().strftime('%Y%m%d')}.md"

        return os.path.join(local_stash_dir, stash_file_name)

    def validate(self):
        """Validates the current changelog and returns KACLValidation object containing all information

        Returns:
            [KACLValidation] -- object holding all error information
        """
        validation = KACLValidation()

        # first load the stash
        self._refresh_stash()
        for stashed_changelog in self.stash:
            val = stashed_changelog.validate()
            for e in val.errors():
                validation.add(e)

        # 1. assert only one header and starts on first line
        if len(self.__headers) == 0:
            validation.add_error(
                line=None,
                line_number=None,
                error_message="No 'Changelog' header found.",
            )

            # we can stop here already
            return validation
        else:
            if self.header().raw() != self.header().raw().lstrip():
                validation.add_error(
                    line=None,
                    line_number=None,
                    error_message="Changelog header not placed on first line.",
                )

        if len(self.__headers) > 1:
            for header in self.__headers[1:]:
                validation.add_error(
                    line=header.raw(),
                    line_number=header.line_number(),
                    error_message="Unexpected additional top-level heading found.",
                    start_character_pos=0,
                    end_character_pos=len(header.raw()),
                )

        # 1.1 assert header title is in allowed list of header titles
        if self.header().title() not in self.config.allowed_header_titles:
            header = self.header()
            start_pos = header.raw().find(header.title())
            end_pos = start_pos + len(header.title())
            validation.add_error(
                line=header.raw(),
                line_number=header.line_number(),
                error_message=f"Header title not valid. Options are [{','.join(self.config.allowed_header_titles)}]",
                start_character_pos=start_pos,
                end_character_pos=end_pos,
            )

        # 1.2 assert default content is in the header section
        for default_line in self.config.default_content:
            if default_line not in self.header().body().replace("\n", " "):
                header = self.header()
                start_pos = header.raw().find(header.title())
                end_pos = start_pos + len(header.title())
                validation.add_error(
                    line=header.raw(),
                    line_number=header.line_number(),
                    error_message=f"Missing default content '{default_line}'",
                    start_character_pos=start_pos,
                    end_character_pos=end_pos,
                )

        # 2. assert 'unreleased' version is available
        # if self.get('Unreleased') == None:
        #     validation.add_error(
        #         line=None,
        #         line_number=None,
        #         error_message="'Unreleased' section is missing from the Changelog"
        #     )

        # 3. assert versions in valid format
        versions = self.versions()
        for v in versions:
            validation_errors = v.validate(self.config)
            for e in validation_errors:
                validation.add(e)

        # 3.1 assert versions in descending order
        for i in range(len(versions) - 1):
            try:
                v0 = versions[i]
                v1 = versions[i + 1]
                if semver.compare(v0.version(), v1.version()) < 1:
                    validation.add_error(
                        line=v1.raw(),
                        line_number=v1.line_number(),
                        error_message="Versions are not in descending order.",
                        start_character_pos=0,
                        end_character_pos=len(v1.raw()),
                    )
            except Exception:
                pass

        # 4 link references
        # 4.1 check that there are only linked references
        version_strings = [v.version().lower() for v in versions]
        for v, link in self.__link_references.items():
            if v.lower() not in version_strings:
                validation.add_error(
                    line=link.raw(),
                    line_number=link.line_number(),
                    error_message="Link not referenced anywhere in the document",
                    start_character_pos=0,
                    end_character_pos=len(link.raw()),
                )

        return validation

    def is_valid(self):
        """Checks if the current changelog is valid
        Returns:
            [bool] -- true if valid false if not
        """
        validation_results = self.validate()
        return validation_results.is_valid()

    def squash(self, version_start, version_end, keep_version_info=True):

        if isinstance(version_start, str):
            version_start = semver.VersionInfo.parse(version_start)
        if isinstance(version_end, str):
            version_end = semver.VersionInfo.parse(version_end)

        versions = self.versions()
        versions.sort(reverse=True)
        versions_to_squash = []
        versions_unsquashed = []
        for v in versions:
            if "unreleased" in v.version().lower():
                versions_unsquashed.append(v)
            elif v.semver() >= version_start and v.semver() <= version_end:
                versions_to_squash.append(v)
            else:
                versions_unsquashed.append(v)

        # sort versions descending
        versions_to_squash.sort(reverse=True)

        # get the version that will be the new version
        squash_version = versions_to_squash[0]

        # remove version from the squashed list
        versions_to_squash.remove(squash_version)

        # add all sections from the squashed versions to the new version
        for v in versions_to_squash:
            for section, changes in v.sections().items():
                for change in changes.items():
                    if keep_version_info:
                        if v.has_link_reference():
                            change = f"[[{v.version()}]({v.link()})] {change}"
                        else:
                            change = f"[{v.version()}] {change}"
                    squash_version.add(section, change)

        versions_unsquashed.append(squash_version)
        versions_unsquashed.sort(reverse=True)
        self.__versions = versions_unsquashed

    def has_changes(self):
        unreleased_version = self.get("Unreleased")
        if not unreleased_version:
            return False

        sections = unreleased_version.sections()
        if not sections or len(sections) == 0:
            return False

        for pair in sections.items():
            if pair[1] and len(pair[1].items()) > 0:
                return True

        return False

    def add(self, section, data, stash=False):
        """adds a new change to a given section in the 'unreleased' version

        Arguments:
            section {[str]} -- section to add data to
            data {[str]} -- change information
            stash {[bool]} -- if true the change will be stashed instead of added to the changelog (default: {False})
        """

        if stash:
            # check if the stash directory already contains the required changelog file, if not initialize it
            stash_file = self._get_stash_file()

            if not os.path.exists(stash_file):
                kacl_changelog = kacl.new()
                kacl_changelog_content = kacl.dump(kacl_changelog)
                with open(stash_file, "w") as f:
                    f.write(kacl_changelog_content)
                f.close()

            kacl_changelog = kacl.load(stash_file)
            kacl_changelog.add(section.capitalize(), data)
            kacl_changelog_content = kacl.dump(kacl_changelog)
            with open(stash_file, "w") as f:
                f.write(kacl_changelog_content)
            f.close()
        else:
            unreleased_version = self.get("Unreleased")
            if unreleased_version is None:
                unreleased_version = KACLVersion(version="Unreleased")
                self.__versions.insert(0, unreleased_version)
            unreleased_version.add(section.capitalize(), data)

    def stash_unreleased(self):
        """Moves all unreleased changes to the stash file.

        This method takes all changes from the Unreleased section and writes them to
        the stash file, then clears the Unreleased section from the changelog.
        """
        # Check if there are any unreleased changes
        if not self.has_changes():
            return False

        # Get the unreleased version
        unreleased_version = self.get("Unreleased")
        if not unreleased_version:
            return False

        # Get or create the stash file
        stash_file = self._get_stash_file()

        if os.path.exists(stash_file):
            # Load the stash file
            kacl_changelog = kacl.load(stash_file)
        else:
            # Create a new stash file with an empty changelog
            kacl_changelog = kacl.new()

        # Add all unreleased changes to the stash
        sections = unreleased_version.sections()
        if sections:
            for section_title, section_changes in sections.items():
                for change_item in section_changes.items():
                    kacl_changelog.add(section=section_title, data=change_item)

        # Write the updated stash file
        kacl_changelog_content = kacl.dump(kacl_changelog)
        with open(stash_file, "w") as f:
            f.write(kacl_changelog_content)
        f.close()

        # Clear the unreleased section by replacing it with an empty one
        # Find and remove the current unreleased version but keep the link reference if it exists
        link = None

        for i, version in enumerate(self.__versions):
            if version.version() == "Unreleased":
                link = version.link()
                self.__versions.pop(i)
                break

        # Add a new empty unreleased version
        new_unreleased = KACLVersion(version="Unreleased", link=link)
        self.__versions.insert(0, new_unreleased)

        return True

    def release(
        self,
        version=None,
        link=None,
        auto_link=False,
        increment=None,
        allow_no_changes=False,
    ):
        """Creates a new release version by copying the 'unreleased' changes into the
        new version

        Keyword Arguments:
            link {[str]} -- url the version will be linked with (default: {None})
            version {[str]} -- semantic versioning string
            increment {[str]} -- use either 'patch', 'minor', or 'major' to automatically increment the last version
            allow_no_changes {[bool]} -- allow releasing a version without changes (default: {False})
        """

        # check if 'post_release_version_prefix' is set
        post_release_version_prefix = self.config.post_release_version_prefix

        if increment:
            version = self.next_version(increment=increment)

        # check that version is a valid semantic version
        future_version = semver.VersionInfo.parse(
            version
        )  # --> will throw a ValueError if version is not a valid semver

        # check if there are changes to release
        if not allow_no_changes and not self.has_changes():
            raise KACLException(
                "The current changelog has no changes. You can only release if changes are available."
            )

        # check if the version already exists
        if self.get(version) is not None:
            raise KACLException(
                f"The version '{version}' already exists in the changelog. You cannot release the same version twice."
            )

        # check if new version is greater than the last one
        #   1. there has to be an 'unreleased' section
        #   2. All other versions are in descending order
        version_list = self.versions()
        if len(version_list) > 1:  # versions[0] --> unreleased
            last_version = semver.VersionInfo.parse(version_list[1].version())

            last_version_base = semver.VersionInfo(
                major=last_version.major,
                minor=last_version.minor,
                patch=last_version.patch,
            )
            future_version_base = semver.VersionInfo(
                major=future_version.major,
                minor=future_version.minor,
                patch=future_version.patch,
            )

            comp_result = 0
            if post_release_version_prefix:
                #   2.1 Check if 'future version' is a 'post version'
                if (
                    future_version.prerelease
                    and post_release_version_prefix in future_version.prerelease
                ):
                    #   2.2 if 'last version' was a 'post version' continue
                    if (
                        last_version.prerelease
                        and post_release_version_prefix in last_version.prerelease
                    ):
                        comp_result = future_version.compare(last_version)
                    #   2.3 if 'last version' was NOT a 'post version' ensure 'post version' has same 'base version'
                    else:
                        comp_result = future_version_base.compare(last_version_base)
                        #  2.4 if 'last version' has same 'base version' as 'future version' this is ok, because we
                        #  define post version as 'higher' than base version
                        if comp_result == 0:
                            comp_result = 1
                elif (
                    last_version.prerelease
                    and post_release_version_prefix in last_version.prerelease
                ):
                    comp_result = future_version_base.compare(last_version_base)
                else:
                    comp_result = future_version.compare(last_version)
            else:
                comp_result = future_version.compare(last_version)

            if comp_result < 1:
                raise KACLException(
                    f"The version '{version}' cannot be released since it is smaller than the preceding version '{last_version}'."
                )

        # get current unreleased changes
        unreleased_version = self.get("Unreleased")

        # remove current unrelease version from list
        self.__versions.pop(0)

        # convert unreleased version to version
        self.__versions.insert(
            0,
            KACLVersion(
                version=version,
                link=KACLElement(title=version, body=link),
                date=datetime.datetime.now().strftime("%Y-%m-%d"),
                sections=unreleased_version.sections(),
            ),
        )

        if self.config.add_unreleased:
            self.__versions.insert(
                0, KACLVersion(version="Unreleased", link=unreleased_version.link())
            )

        if auto_link:
            link_provider = self.__get_link_provider()
            # Only process the versions we just added/modified
            # If add_unreleased=True: process Unreleased (index 0) and new version (index 1)
            # If add_unreleased=False: only process new version (index 0)
            versions_to_link = 2 if self.config.add_unreleased else 1
            for i in range(versions_to_link):
                fargs = {
                    "version": self.__versions[i].version(),
                    "previous_version": None,
                    "latest_version": version,
                }

                if len(self.__versions) > i + 1:
                    fargs["previous_version"] = self.__versions[i + 1].version()

                if "unreleased" in self.__versions[i].version().lower():
                    self.__versions[i].set_link(
                        link_provider.unreleased_changes(**fargs)
                    )
                else:
                    if fargs["previous_version"]:
                        self.__versions[i].set_link(
                            link_provider.compare_versions(**fargs)
                        )
                    else:
                        self.__versions[i].set_link(
                            link_provider.initial_version(**fargs)
                        )

    def get(self, version) -> KACLVersion:
        """Returns the selected version

        Arguments:
            version {[str]} -- semantic versioning string

        Returns:
            [KACLVersion] -- version object with all information
        """
        res = [
            x
            for x in self.__versions
            if x.version() and version.capitalize() == x.version()
        ]
        if res and len(res):
            return res[0]

    def next_version(self, increment="patch"):
        """returns the current version (last released)
        increment {[str]} -- use either 'patch', 'minor', or 'major' to automatically increment the last version
        Returns:
            [str] -- latest released version, None if none is available
        """
        v = self.current_version()
        next_version = None
        if v:
            sv = semver.VersionInfo.parse(v)
            if "post" == increment:
                if not self.config.post_release_version_prefix:
                    raise KACLException(
                        "No 'post_release_version_prefix' set in the config. Incrementing not possible"
                    )
                sv = sv.bump_prerelease(token=self.config.post_release_version_prefix)
            elif "patch" == increment:
                sv = sv.bump_patch()
            elif "minor" == increment:
                sv = sv.bump_minor()
            elif "major" == increment:
                sv = sv.bump_major()
            next_version = str(sv)
        else:
            raise KACLException(
                "No previously released version found. Incrementing not possible"
            )

        return next_version

    def current_version(self):
        """returns the current version (last released)

        Returns:
            [str] -- latest released version, None if none is available
        """
        version_list = self.versions()
        for v in version_list:
            if v.version().lower() != "unreleased":
                return v.version()

    def generate_links(
        self,
        host_url=None,
        compare_versions_template=None,
        unreleased_changes_template=None,
        initial_version_template=None,
    ):
        """automatically generates links for all versions

        Returns: None
        """
        link_provider = self.__get_link_provider(
            host_url=host_url,
            compare_versions_template=compare_versions_template,
            unreleased_changes_template=unreleased_changes_template,
            initial_version_template=initial_version_template,
        )

        versions = self.versions()
        if len(versions) > 1:
            for i in range(len(versions) - 1):
                fargs = {
                    "version": versions[i].version(),
                    "previous_version": versions[i + 1].version(),
                    "latest_version": self.current_version(),
                }

                if "unreleased" in versions[i].version().lower():
                    versions[i].set_link(link_provider.unreleased_changes(**fargs))
                else:
                    versions[i].set_link(link_provider.compare_versions(**fargs))
            versions[-1].set_link(link_provider.initial_version(**fargs))
        elif len(versions) == 1:
            fargs = {
                "version": versions[0].version(),
                "latest_version": self.current_version(),
            }

            if "unreleased" in versions[0].version().lower():
                versions[0].set_link(link_provider.initial_version(version="master"))
            else:
                versions[0].set_link(link_provider.initial_version(**fargs))

    def get_associated_issues(self, version=None):
        """returns all issues for the given version"""
        kacl_version = None
        if not version:
            # if no version is given, we will use the current version
            kacl_version = self.get(self.current_version())
        else:
            kacl_version = self.get(version)

        patterns = {"jira": self.config.issue_tracker_jira_issue_patterns}

        # get all issue ids
        return extract_issue_ids(kacl_version, patterns)

    def render_comments(self, version=None) -> dict[str:str]:
        if version is None:
            version = self.current_version()

        changes = self.get(version)
        link_provider = self.__get_link_provider()

        format_string = {
            "new_version": version,
            "changes": changes.body(),
            "link": link_provider.version_link(version),
        }

        comments = {}

        if self.config.issue_tracker_jira_comment_template:
            jira_comment = replace_env_variables(
                self.config.issue_tracker_jira_comment_template
            )
            jira_comment = jira_comment.format(**format_string)
            jira_comment = convert_markdown_to_jira(jira_comment)
            comments["jira"] = jira_comment

        return comments

    def add_comments(self, version=None) -> dict[str : dict[str:bool]]:
        # This function will parse all versions for known issue ids and search the defined
        # issue tracking system for the issue. If the issue is found, a comment will be added to the
        # issue with the changelog/release information

        issue_ids = self.get_associated_issues(version)

        jira_client = None
        if "jira" in issue_ids and len(issue_ids["jira"]) > 0:
            client = KACLJiraClient(self.config)
            if client.is_authenticated():
                jira_client = client

        rendered_comments = self.render_comments(version)

        report = {"jira": {}}

        if jira_client:
            # comment on jira tickets
            for jira_issue in issue_ids["jira"]:
                try:
                    jira_client.add_comment(jira_issue, rendered_comments["jira"])
                    report["jira"][jira_issue] = True
                except Exception:
                    report["jira"][jira_issue] = False
                    continue

        return report

    def header(self):
        """Gives access to the top level heading element

        Returns:
            [KACLElement] -- object holding all information of the top level heading
        """
        if self.__headers and len(self.__headers) > 0:
            return self.__headers[0]

    def title(self):
        """Returns the title of the changelog

        Returns:
            [str] -- title of the changelog
        """
        if self.__headers and len(self.__headers) > 0:
            return self.__headers[0].title()
        return None

    def versions(self):
        """Returns a list of all available versions

        Returns:
            [list] -- list of KACLVersions
        """
        return self.__versions

    def metadata(self):
        """Returns the metadata as dict or None if not available

        Returns:
            [dict|None] -- metadata of the document
        """
        return self.__meta_data

    @staticmethod
    def init():
        return KACLDocument.parse(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
        """
        )

    @staticmethod
    def parse(data, file=None):
        """Parses a given text object and returns the KACLDocument

        Arguments:
            data {[str]} -- markdown text holding the changelog

        Returns:
            [KACLDocument] -- object holding all information
        """

        data_lf = data.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

        # First check if there are link references and split the document where they begin
        link_reference_begin, link_references = KACLParser.parse_link_references(
            data_lf
        )

        meta_data = KACLParser.parse_metadata(data_lf)

        changelog_body = data_lf
        if link_reference_begin:
            changelog_body = data_lf[:link_reference_begin]

        # read header
        headers = KACLParser.parse_header(changelog_body, 1, 2)

        # read versions
        versions = KACLParser.parse_header(changelog_body, 2, 2)
        versions = [KACLVersion(element=x) for x in versions]

        # set link references into versions if available
        for v in versions:
            v.set_link(link_references.get(v.version().lower(), None))

        return KACLDocument(
            data=data,
            headers=headers,
            versions=versions,
            link_references=link_references,
            meta_data=meta_data,
            file_path=file,
        )

    def __get_link_provider(
        self,
        host_url=None,
        compare_versions_template=None,
        unreleased_changes_template=None,
        initial_version_template=None,
    ):
        host_url = host_url if host_url else self.config.link_host_url
        compare_versions_template = (
            compare_versions_template
            if compare_versions_template
            else self.config.links_compare_versions_template
        )
        unreleased_changes_template = (
            unreleased_changes_template
            if unreleased_changes_template
            else self.config.links_unreleased_changes_template
        )
        initial_version_template = (
            initial_version_template
            if initial_version_template
            else self.config.links_initial_version_template
        )

        if host_url is None:
            if "CI_PROJECT_URL" in os.environ:
                host_url = os.environ["CI_PROJECT_URL"]
            else:
                try:
                    repo = git.Repo(os.getcwd())
                    remote = repo.remote()
                    for url in remote.urls:
                        host_url = url
                        break
                except Exception:
                    raise KACLException(
                        "ERROR: Could not determine project url. Update your config or run within a valid git repository"
                    )

        host_url = host_url.removesuffix(".git")

        return LinkProvider(
            host_url=host_url,
            compare_versions_template=compare_versions_template,
            unreleased_changes_template=unreleased_changes_template,
            initial_version_template=initial_version_template,
        )
