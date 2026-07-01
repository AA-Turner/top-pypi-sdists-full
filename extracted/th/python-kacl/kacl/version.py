import re

import semver

from kacl.changes import KACLChanges
from kacl.element import KACLElement
from kacl.parser import KACLParser
from kacl.validation import KACLValidationError


class KACLVersion(KACLElement):
    def __init__(
        self, element=KACLElement(), version="", date="", sections=None, link=None
    ):
        KACLElement.__init__(
            self,
            raw=element.raw(),
            title=element.title(),
            body=element.body(),
            line_number=element.line_number(),
        )
        self.__date = date
        self.__version = version
        if sections is None:
            self.__sections = dict()
        else:
            self.__sections = sections
        self.__link_reference = None
        self.set_link(link)

    def __lt__(self, obj):
        if self.version().lower() == "unreleased":
            return False
        elif obj.version().lower() == "unreleased":
            return False
        else:
            return (self.semver()) < (obj.semver())

    def __eq__(self, obj):
        return self.version() == obj.version()

    def __repr__(self):
        return self.__version

    def link(self):
        if self.__link_reference:
            return self.__link_reference.body()

    def set_link(self, link):
        if not link or isinstance(link, KACLElement):
            self.__link_reference = link
        else:
            self.__link_reference = KACLElement(title=self.version(), body=link)

    def has_link_reference(self):
        if not self.__link_reference:
            return False
        else:
            return bool(
                self.__link_reference.body() is not None
                and self.__link_reference.body()
            )

    def date(self):
        if not len(self.__date):
            title = self.title()
            m = re.search(r"\d\d\d\d-\d\d-\d\d", title)
            if m:
                self.__date = m.group().strip()

        return self.__date

    def version(self):
        if not len(self.__version):
            title = self.title()
            version = KACLParser.parse_sem_ver(title)
            if version:
                self.__version = version
            elif "unreleased" in title.lower():
                self.__version = "Unreleased"

        return self.__version

    def semver(self):
        return semver.VersionInfo.parse(self.version())

    def set_version(self, version):
        self.__version = version

    def sections(self):
        if not self.__sections and self.body().strip():
            self.__sections = dict()
            sections = KACLParser.parse_header(
                text=self.body(),
                start_depth=3,
                end_depth=3,
                line_offset=self.line_number(),
            )
            for section in sections:
                sec = KACLChanges(section)
                if sec.title() in self.__sections:
                    raise ValueError(
                        f"Version '{self.version()}' has multiple sections with title '{sec.title()}'"
                    )
                self.__sections[sec.title()] = sec
        return self.__sections

    def changes(self, section):
        sections = self.sections()
        if sections and section in sections:
            return sections[section]

        return None

    def add(self, section, change):
        if section not in self.sections():
            self.__sections[section] = KACLChanges(
                KACLElement(title=section, body="", line_number=None)
            )
        self.__sections[section].add(change)

    def validate(self, config):
        errors = []
        errors.extend(self.__validate_semver())
        errors.extend(self.__validate_date())
        errors.extend(self.__validate_sections(config))
        errors.extend(self.__validate_links())
        return errors

    def __validate_semver(self):
        errors = []
        if "Unreleased" != self.version():
            raw = self.raw()
            regex = KACLParser.semver_regex
            regex_error = r"#\s+(.*)\s+"
            if self.link():
                regex = f"#\\s+\\[{KACLParser.semver_regex}\\]"
                regex_error = r"#\s+\[(.*)\]"
            if not KACLParser.parse_sem_ver(raw, regex):
                start_pos = 0
                end_pos = 0
                m = re.match(regex_error, raw)
                if m:
                    start_pos = raw.find(m.group(1))
                    end_pos = start_pos + len(m.group(1))
                errors.append(
                    KACLValidationError(
                        line=raw,
                        line_number=self.line_number(),
                        start_character_pos=start_pos,
                        end_character_pos=end_pos,
                        error_message="Version is not a valid semantic version.",
                    )
                )
        return errors

    def __validate_date(self):
        errors = []
        if "Unreleased" != self.version():
            if not self.date() or len(self.date()) < 1:
                errors.append(
                    KACLValidationError(
                        line=self.raw(),
                        line_number=self.line_number(),
                        error_message="Versions need to be decorated with a release date in the following format 'YYYY-MM-DD'",
                        start_character_pos=0,
                        end_character_pos=len(self.raw()),
                    )
                )
            if self.date() and not re.match(
                r"\d\d\d\d-[0-1][\d]-[0-3][\d]", self.date()
            ):
                start_pos = self.raw().find(self.date())
                end_pos = start_pos + len(self.date())
                errors.append(
                    KACLValidationError(
                        line=self.raw(),
                        line_number=self.line_number(),
                        error_message="Date does not match format 'YYYY-MM-DD'",
                        start_character_pos=start_pos,
                        end_character_pos=end_pos,
                    )
                )
        return errors

    def __validate_sections(self, config):
        errors = []

        # 3.1 check that there is no text outside of a section
        body = self.body().replace("\n", "").strip()
        if body and not body.startswith("###"):
            errors.append(
                KACLValidationError(
                    error_message=f"Version '{self.version()}' has content outside of a section.",
                    line_number=self.line_number(),
                )
            )

        # 3.3 check that only allowed sections are in the version
        try:
            sections = self.sections()
        except ValueError as e:
            errors.append(
                KACLValidationError(
                    error_message=str(e), line_number=self.line_number()
                )
            )
            return errors

        for title, element in sections.items():
            if title not in config.allowed_version_sections:
                start_pos = element.raw().find(title)
                end_pos = start_pos + len(title)
                errors.append(
                    KACLValidationError(
                        line=element.raw(),
                        line_number=element.line_number(),
                        error_message=f'"{title}" is not a valid section for a version. Options are [{",".join(config.allowed_version_sections)}]',
                        start_character_pos=start_pos,
                        end_character_pos=end_pos,
                    )
                )

            # 3.4 check that only list elements are in the sections
            # 3.4.1 bring everything into a single line
            body = element.body()
            body_clean = re.sub(r"\n\s+", "", body)
            lines = body_clean.split("\n\n")
            non_list_lines = [
                x for x in lines if not x.strip().startswith("-") and len(x.strip()) > 0
            ]
            if len(non_list_lines) > 0:
                errors.append(
                    KACLValidationError(
                        line=body.strip(),
                        line_number=element.line_number(),
                        error_message="Section does contain more than only listings.",
                    )
                )

        # 3.5 make sure that every version that has content has it's content in a section
        if len(self.sections()) == 0 and len(self.body().strip()) != 0:
            errors.append(
                KACLValidationError(
                    line=self.raw(),
                    line_number=self.line_number(),
                    error_message=f'Version "{self.version()}" has change elements outside of a change section.',
                )
            )
        return errors

    def __validate_links(self):
        errors = []
        # 3.6 Check that a link exists for linked versions
        if "[" in self.raw() and "]" in self.raw() and not self.has_link_reference():
            errors.append(
                KACLValidationError(
                    line=self.raw(),
                    line_number=self.line_number(),
                    error_message=f'Version "{self.version()}" is linked, but no link reference found in changelog file.',
                    start_character_pos=self.raw().find("["),
                    end_character_pos=self.raw().find("]"),
                )
            )
        return errors
