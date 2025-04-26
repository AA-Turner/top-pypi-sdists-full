import os
import re
from typing import NamedTuple
# pip dependency
from mkdocs.config.config_options import Type
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
# local files
from . import debug, warning
from .utils import translate_glob_to_regex

PLACEHOLDER_REGEX = re.compile(r"\{\d+\}")

class MyConfig(Config):
    enabled = Type(bool, default=True)
    globs = Type(dict, default={})
    regex = Type(dict, default={})


class Rule(NamedTuple):
    # Human readable ID to use in errr messages to identify the rule
    id: str
    # pattern to check the path against
    regex: re.Pattern
    # static tags
    tags_static: list[str]
    # tags that contain placeholders that need to be replaced with the capture groups of the regex
    tags_with_placeholders: list[str]


def ensure_string_or_list(value_to_validate: object) -> list[str]:
    ALLOWED_TYPES = [str, float, int]
    if type(value_to_validate) in ALLOWED_TYPES:
        return [str(value_to_validate)]
    elif type(value_to_validate) == list:
        for list_item in value_to_validate:
            if type(list_item) not in ALLOWED_TYPES:
                raise PluginError(f"List element should be a string, but is a {type(list_item)}. Problematic value: {list_item} which is part of the list {value_to_validate}")
        return [str(x) for x in value_to_validate]
    else:
        raise PluginError(f"Expected a string or a list of strings, but got {type(value_to_validate)}. Problematic value: ")


def parse_rule(pattern: str, tags: object, type: str) -> Rule:
    try:
        id = f"{type}:{pattern}"
        if type == "regex":
            regex = re.compile(pattern, re.IGNORECASE)
            tag_list = ensure_string_or_list(tags)
            tags_static = []
            tags_with_placeholders = []
            for tag in tag_list:
                # Sort tags ahead of time, so that it is faster later on
                if PLACEHOLDER_REGEX.search(tag):
                    tags_with_placeholders.append(tag)
                else:
                    tags_static.append(tag)
            return Rule(id=id, regex=regex, tags_static=tags_static, tags_with_placeholders=tags_with_placeholders)
        elif type == "glob":
            regex_str = translate_glob_to_regex(pattern)
            regex = re.compile(regex_str, re.IGNORECASE)
            tag_list = ensure_string_or_list(tags)
            # Globs have no capture groups, so all tags are static
            return Rule(id=id, regex=regex, tags_static=tag_list, tags_with_placeholders=[])
        else:
            raise PluginError(f"Unexpected type parameter: {type}")
    except Exception:
        raise PluginError(f"Error while parsing rule: (pattern={pattern}, tags={tags}, tyep={type})")


def add_tags_to_page(page: Page, tag_list: list[str]) -> None:
    if "tags" in page.meta:
        page_tags = page.meta["tags"]
        for tag in tag_list:
            # Only add tags if they do not already exist
            if tag not in page_tags:
                page_tags.append(tag)
    else:
        # we need to copy it, otherwise subsequent changes will affect all pages
        page.meta["tags"] = list(tag_list)


def replace_placeholders(string_with_placeholders: str, values: list[str]) -> str:
    debug("replace_placeholders - %r - %r", string_with_placeholders, values)
    return string_with_placeholders.format(*values)

class Plugin(BasePlugin[MyConfig]):
    def on_config(self, config: MkDocsConfig, **kwargs) -> MkDocsConfig:
        """
        Called once when the config is loaded.
        It will make modify the config and initialize this plugin.
        """
        self.rules: list[Rule] = []

        for key, value in self.config.globs.items():
            self.rules.append(parse_rule(key, value, "glob"))
        for key, value in self.config.regex.items():
            self.rules.append(parse_rule(key, value, "regex"))

        for rule in self.rules:
            debug("Rule: %s - %r - %r", rule.id, rule.tags_static, rule.tags_with_placeholders)

        if not self.rules:
            warning("No rules were specified")
        return config


    def on_page_markdown(self, markdown: str, page: Page, config: MkDocsConfig, files: Files) -> str:
        """
        The page_markdown event is called after the page's markdown is loaded from file and can be used to alter the Markdown source text. The meta- data has been stripped off and is available as page.meta at this point.
        See: https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
        """
        try:
            self.handle_page(page, config)
            return markdown
        except Exception as error:
            raise PluginError(f"Error in on_page_markdown: {error}")


    def handle_page(self, page: Page, config: MkDocsConfig) -> None:
        if self.config.enabled:
            file_path = page.file.src_path
            # If necessary convert the paths to Unix format (so that it works cross platform. And backslashes are always a pain to work with)
            if os.path.sep != "/":
                file_path = file_path.replace(os.path.sep, "/")
            # print(file_path)
            for rule in self.rules:
                try:
                    if match := rule.regex.fullmatch(file_path):
                        if rule.tags_with_placeholders:
                            actual_tags = list(rule.tags_static)
                            # we need to replace the placeholders in the dynamic tags
                            values = [str(x) for x in match.groups()]
                            for tag in rule.tags_with_placeholders:
                                tag = replace_placeholders(tag, values)
                                actual_tags.append(tag)

                            # print(file_path, rule.id, actual_tags)
                            add_tags_to_page(page, actual_tags)
                        else:
                            # No dynamic tags -> we just need to add the static ones
                            # print(file_path, rule.id, rule.tags_static)
                            add_tags_to_page(page, rule.tags_static)
                        
                        # print("--> matches", re_pattern.pattern, ":", tag_name)
                except Exception as ex:
                    raise PluginError(f"Error when applying rule {rule.id}: {ex}")


