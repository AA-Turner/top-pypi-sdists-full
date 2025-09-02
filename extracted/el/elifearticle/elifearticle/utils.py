"""
Utility functions for converting content and some shared by other libraries
"""

from collections import OrderedDict
import re
import os
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from elifetools import utils as etoolsutils


def repl(match):
    "Convert hex to int to unicode character"
    chr_code = int(match.group(1), 16)
    return chr(chr_code)


def entity_to_unicode(string):
    """
    Quick convert unicode HTML entities to unicode characters
    using a regular expression replacement
    """
    # Selected character replacements that have been seen
    replacements = []
    replacements.append((r"&alpha;", "\u03b1"))
    replacements.append((r"&beta;", "\u03b2"))
    replacements.append((r"&gamma;", "\u03b3"))
    replacements.append((r"&delta;", "\u03b4"))
    replacements.append((r"&epsilon;", "\u03b5"))
    replacements.append((r"&ordm;", "\u00ba"))
    replacements.append((r"&iuml;", "\u00cf"))
    replacements.append((r"&ldquo;", '"'))
    replacements.append((r"&rdquo;", '"'))

    # First, replace numeric entities with unicode
    string = re.sub(r"&#x(....);", repl, string)
    # Second, replace some specific entities specified in the list
    for entity, replacement in replacements:
        string = re.sub(entity, replacement, string)
    return string


def remove_tag(tag_name, string):
    """
    Remove open and close tags - the tags themselves only - using
    a non-greedy angle bracket pattern match
    """
    if not string:
        return string
    pattern = re.compile("</?" + tag_name + ".*?>")
    string = pattern.sub("", string)
    return string


def replace_tags(string, from_tag="i", to_tag="italic"):
    """
    Replace tags such as <i> to <italic>
    <sup> and <sub> are allowed and do not need to be replaced
    This does not validate markup
    """
    string = string.replace("<" + from_tag + ">", "<" + to_tag + ">")
    string = string.replace("</" + from_tag + ">", "</" + to_tag + ">")
    return string


def attr_names(attr_map):
    """return a list of attribute names from the map"""
    if attr_map:
        return list(sorted(attr_map.keys()))
    return []


def attr_string(attr_map):
    """string of tag attributes and values"""
    string = ""
    if attr_map:
        for key, value in sorted(attr_map.items()):
            attr = '%s="%s"' % (
                key,
                etoolsutils.escape_ampersand(value).replace('"', "&quot;"),
            )
            string = " ".join([string, attr])
    return string


def set_attr_if_value(obj, attr_name, value):
    "shorthand method to set object values if the value is not none"
    if value is not None:
        setattr(obj, attr_name, value)


def is_year_numeric(value):
    "True if value is all digits"
    if value and re.match("^[0-9]+$", value):
        return True
    return False


def version_from_xml_filename(filename):
    "extract the numeric version from the xml filename"
    try:
        filename_parts = filename.split(os.sep)[-1].split("-")
    except AttributeError:
        return None
    if len(filename_parts) == 3 or (
        len(filename_parts) == 4 and filename_parts[1] == "preprint"
    ):
        try:
            return int(filename_parts[-1].lstrip("v").rstrip(".xml"))
        except ValueError:
            return None
    else:
        return None


def get_last_commit_to_master(repo_path="."):
    """
    returns the last commit on the master branch. It would be more ideal to get the commit
    from the branch we are currently on, but as this is a check mostly to help
    with production issues, returning the commit from master will be sufficient.
    """
    last_commit = None
    repo = None
    try:
        repo = Repo(repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError):
        repo = None
    if repo:
        try:
            last_commit = repo.commits()[0]
        except AttributeError:
            # Optimised for version 0.3.2.RC1
            last_commit = repo.head.commit
    return str(last_commit)


def calculate_journal_volume(pub_date, year):
    """
    volume value is based on the pub date year
    pub_date is a python time object
    """
    try:
        volume = str(pub_date.tm_year - year + 1)
    except TypeError:
        volume = None
    except AttributeError:
        volume = None
    return volume


def author_name_from_json(author_json):
    "concatenate an author name from json data"
    author_name = None
    if author_json.get("type"):
        if author_json.get("type") == "group" and author_json.get("name"):
            author_name = author_json.get("name")
        elif author_json.get("type") == "person" and author_json.get("name"):
            if author_json.get("name").get("preferred"):
                author_name = author_json.get("name").get("preferred")
    return author_name


def text_from_affiliation_elements(department, institution, city, country):
    "format an author affiliation from details"
    return ", ".join(
        element for element in [department, institution, city, country] if element
    )


def license_data_by_url(license_url):
    "boilerplate data to populate license XML"
    if license_url and re.match(
        r"^(http|https)://creativecommons.org/licenses/by/4.0/$", license_url
    ):
        return license_data(1)
    elif license_url and re.match(
        r"^(http|https)://creativecommons.org/publicdomain/zero/1.0/$", license_url
    ):
        return license_data(2)
    return license_data(None)


def license_data(license_id):
    "boilerplate data to populate a license object keyed on the license_id"
    data = OrderedDict()
    if not license_id:
        return data
    if int(license_id) == 1:
        data["license_id"] = 1
        data["license_type"] = "open-access"
        data["copyright"] = True
        data["href"] = "https://creativecommons.org/licenses/by/4.0/"
        data["name"] = "Creative Commons Attribution License"
        data["paragraph1"] = "This article is distributed under the terms of the "
        data["paragraph2"] = (
            ", which permits unrestricted use and redistribution provided that the"
            " original author and source are credited."
        )
    elif int(license_id) == 2:
        data["license_id"] = 2
        data["license_type"] = "open-access"
        data["copyright"] = False
        data["href"] = "https://creativecommons.org/publicdomain/zero/1.0/"
        data["name"] = "Creative Commons CC0 public domain dedication"
        data["paragraph1"] = (
            "This is an open-access article, free of all copyright, and may be"
            " freely reproduced, distributed, transmitted, modified, built upon, or"
            " otherwise used by anyone for any lawful purpose. The work is made"
            " available under the "
        )
        data["paragraph2"] = "."
    return data
