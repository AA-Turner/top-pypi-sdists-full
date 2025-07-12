#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from functools import partial
import json
from typing import cast, Dict, List, Optional, Union

import trafaret as t
from typing_extensions import TypedDict

from datarobot._compat import String
from datarobot.enums import (
    ComplianceDocTemplateProjectType,
    ComplianceDocTemplateType,
    ComplianceDocType,
    enum_to_list,
)
from datarobot.models.api_object import APIObject

# Make sure validator stays insync with main repo
OptKey = partial(t.Key, optional=True)
TitleString = String(max_length=500)
SectionDict = t.Forward()
SectionDict.provide(
    t.Or(
        t.Dict(
            {
                "type": t.Atom("datarobot"),
                "title": TitleString,
                "content_id": String(),
                OptKey("sections"): t.Or(t.List(SectionDict), t.Null),
                OptKey("description"): t.Or(String(allow_blank=True), t.Null),
                OptKey("instructions"): t.Or(
                    t.Dict({"owner": String(allow_blank=True), "user": String(allow_blank=True)}),
                    t.Null,
                ),
                OptKey("locked"): t.Bool,
            }
        ),
        t.Dict(
            {
                "type": t.Atom("user"),
                "title": TitleString,
                "regular_text": String(max_length=5000, allow_blank=True),
                "highlighted_text": String(max_length=5000, allow_blank=True),
                OptKey("sections"): t.Or(t.List(SectionDict), t.Null),
                OptKey("description"): t.Or(String(allow_blank=True), t.Null),
                OptKey("instructions"): t.Or(
                    t.Dict({"owner": String(allow_blank=True), "user": String(allow_blank=True)}),
                    t.Null,
                ),
                OptKey("locked"): t.Bool,
            }
        ),
        t.Dict(
            {
                "type": t.Atom("custom"),
                "title": TitleString,
                "regular_text": String(max_length=5000, allow_blank=True),
                "highlighted_text": String(max_length=5000, allow_blank=True),
                OptKey("sections"): t.Or(t.List(SectionDict), t.Null),
                OptKey("description"): t.Or(String(allow_blank=True), t.Null),
                OptKey("instructions"): t.Or(
                    t.Dict({"owner": String(allow_blank=True), "user": String(allow_blank=True)}),
                    t.Null,
                ),
                OptKey("locked"): t.Bool,
            }
        ),
        t.Dict(
            {"type": t.Atom("table_of_contents"), "title": TitleString, OptKey("locked"): t.Bool}
        ),
    )
)


class Instructions(TypedDict):
    owner: str
    user: str


class Section(TypedDict):
    title: str
    type: ComplianceDocType
    locked: bool


class DataRobotSection(Section):
    content_id: str
    sections: Optional[List["Section"]]
    description: Optional[str]
    instructions: Optional[Instructions]


class UserSection(Section):
    regular_test: str
    highlighted_test: str
    sections: Optional[List["Section"]]
    description: Optional[str]
    instructions: Optional[Instructions]


class CustomSection(Section):
    regular_test: str
    highlighted_test: str
    sections: Optional[List["Section"]]
    description: Optional[str]
    instructions: Optional[Instructions]


class TableOfContentsSection(Section):
    """
    Table of Contents Sections only have the base fields available to all Section classes
    """


def make_url(root: str, template_id: str) -> str:
    return f"{root}{template_id}/"


def load_sections_from_path(path: str) -> List[Section]:
    with open(path) as f:  # pylint: disable=unspecified-encoding
        sections = json.loads(f.read())
        return cast(List[Section], sections)


class ComplianceDocTemplate(APIObject):
    """A :ref:`compliance documentation template <automated-documentation-overview>`. Templates
    are used to customize contents of :class:`AutomatedDocument
    <datarobot.models.automated_documentation.AutomatedDocument>`.

    .. versionadded:: v2.14

    Notes
    -----
    Each ``section`` dictionary has the following schema:

    * ``title`` : title of the section
    * ``type`` : type of section. Must be one of "datarobot", "user" or "table_of_contents".

    Each type of section has a different set of attributes described bellow.

    Section of type ``"datarobot"`` represent a section owned by DataRobot. DataRobot
    sections have the following additional attributes:

    * ``content_id`` : The identifier of the content in this section.
      You can get the default template with :meth:`get_default
      <datarobot.models.compliance_doc_template.ComplianceDocTemplate.get_default>`
      for a complete list of possible DataRobot section content ids.
    * ``sections`` :  list of sub-section dicts nested under the parent section.

    Section of type ``"user"`` represent a section with user-defined content.
    Those sections may contain text generated by user and have the following additional fields:

    * ``regularText`` : regular text of the section, optionally separated by
      ``\\n`` to split paragraphs.
    * ``highlightedText`` : highlighted text of the section, optionally separated
      by ``\\n`` to split paragraphs.
    * ``sections`` :  list of sub-section dicts nested under the parent section.

    Section of type ``"table_of_contents"`` represent a table of contents and has
    no additional attributes.

    Attributes
    ----------
    id : str
        The ID of the template.
    name : str
        The name of the template.
    creator_id : str
        The ID of the user who created the template.
    creator_username : str
        The username of the user who created the template.
    org_id : str
        The ID of the organization the template belongs to.
    sections : list of dicts
        The sections of the template describing the structure of the document. The section schema
        is described in Notes section, above.
    project_type : ComplianceDocTemplateProjectType
        The project type of the template.
    """

    _root_path = "complianceDocTemplates/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("creator_id"): String(),
            t.Key("creator_username"): String(),
            OptKey("org_id"): t.Or(String(), t.Null),
            t.Key("name"): String(),
            OptKey("sections"): t.Or(t.List(SectionDict), t.Null),
            OptKey("project_type"): t.Or(
                t.Enum(*enum_to_list(ComplianceDocTemplateProjectType)), t.Null
            ),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        creator_id: str,
        creator_username: str,
        name: str,
        org_id: Optional[str] = None,
        sections: Optional[List[Section]] = None,
        project_type: Optional[ComplianceDocTemplateProjectType] = None,
    ):
        self.id = id
        self.creator_id = creator_id
        self.creator_username = creator_username
        self.org_id = org_id
        self.name = name
        self.sections = sections
        self.project_type = project_type

    def __repr__(self) -> str:
        return f"ComplianceDocTemplate({self.name!r})"

    @classmethod
    def get_default(
        cls, template_type: Optional[ComplianceDocTemplateType] = None
    ) -> "ComplianceDocTemplate":
        """Get a default DataRobot template. This template is used for generating
        compliance documentation when no template is specified.


        Parameters
        ----------
        template_type : str or None
            Type of the template. Currently supported values are "normal" and "time_series"

        Returns
        -------
        template : ComplianceDocTemplate
            the default template object with ``sections`` attribute populated with default sections.
        """
        query_params = {"type": template_type} if template_type else None
        project_type = ComplianceDocTemplateType.to_project_type(template_type)
        response = cls._client.get("complianceDocTemplates/default/", params=query_params)
        return cls(
            id=cast(str, None),
            creator_id=cast(str, None),
            creator_username=cast(str, None),
            org_id=None,
            name="default",
            sections=response.json()["sections"],
            project_type=project_type,
        )

    @classmethod
    def create_from_json_file(
        cls, name: str, path: str, project_type: Optional[ComplianceDocTemplateProjectType] = None
    ) -> "ComplianceDocTemplate":
        """Create a template with the specified name and sections in a JSON file.

        This is useful when working with sections in a JSON file. Example:

        .. code-block:: python

            default_template = ComplianceDocTemplate.get_default()
            default_template.sections_to_json_file('path/to/example.json')
            # ... edit example.json in your editor
            my_template = ComplianceDocTemplate.create_from_json_file(
                name='my template',
                path='path/to/example.json'
            )

        Parameters
        ----------
        name : str
            the name of the template, which must be unique.
        path : str
            the path to find the JSON file at
        project_type : ComplianceDocTemplateProjectType
            The project type of the template.

        Returns
        -------
        template : ComplianceDocTemplate
            The created template.
        """
        payload = {
            "name": name,
            "sections": load_sections_from_path(path),
            "project_type": project_type,
        }
        resp = cls._client.post(cls._root_path, data=payload)
        return cls.from_location(resp.headers["Location"])

    @classmethod
    def create(
        cls,
        name: str,
        sections: List[Section],
        project_type: Optional[ComplianceDocTemplateProjectType] = None,
    ) -> "ComplianceDocTemplate":
        """Create a template with the specified name and sections.

        Parameters
        ----------
        name : str
            The name of the template, which must be unique.
        sections : list
            List of section objects
        project_type : ComplianceDocTemplateProjectType
            The project type of the template.

        Returns
        -------
        template : ComplianceDocTemplate
            The created template.
        """
        payload = {"name": name, "sections": sections, "project_type": project_type}
        resp = cls._client.post(cls._root_path, data=payload)
        return cls.from_location(resp.headers["Location"])

    @classmethod
    def get(cls, template_id: str) -> "ComplianceDocTemplate":
        """Retrieve a specific template.

        Parameters
        ----------
        template_id :  str
            the id of the template to retrieve

        Returns
        -------
        template : ComplianceDocTemplate
            the retrieved template
        """
        return cls.from_location(make_url(cls._root_path, template_id))

    @classmethod
    def list(
        cls,
        name_part: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        project_type: Optional[ComplianceDocTemplateProjectType] = None,
    ) -> List["ComplianceDocTemplate"]:
        """Get a paginated list of compliance documentation template objects.

        Parameters
        ----------
        name_part : str or None
            Return only the templates with names matching specified string. The matching is
            case-insensitive.
        limit : int
            The number of records to return. The server will use a (possibly finite) default if not
            specified.
        offset : int
            The number of records to skip.
        project_type : ComplianceDocTemplateProjectType
            The project type of the template.

        Returns
        -------
        templates : list of ComplianceDocTemplate
            The list of template objects.
        """
        params = {
            "limit": limit,
            "offset": offset,
            "namePart": name_part,
            "projectType": project_type,
        }
        r_data = cls._client.get(cls._root_path, params=params).json()
        return cast(
            List["ComplianceDocTemplate"], [cls.from_server_data(item) for item in r_data["data"]]
        )

    def sections_to_json_file(self, path: str, indent: int = 2) -> None:
        """Save sections of the template to a json file at the specified path

        Parameters
        ----------
        path : str
            the path to save the file to
        indent : int
            indentation to use in the json file.
        """
        with open(path, "w") as f:  # pylint: disable=unspecified-encoding
            f.write(json.dumps(self.sections, indent=indent))

    def update(
        self,
        name: Optional[str] = None,
        sections: Optional[List[Section]] = None,
        project_type: Optional[ComplianceDocTemplateProjectType] = None,
    ) -> None:
        """Update the name or sections of an existing doc template.

        Note that default or non-existent templates can not be updated.

        Parameters
        ----------
        name : Optional[str]
            the new name for the template
        sections : list of dicts
            The list of sections within the template.
        project_type : ComplianceDocTemplateProjectType
            The project type of the template
        """
        payload: Dict[str, Union[str, List[Section]]] = {}
        if name is not None:
            payload["name"] = name
        if sections is not None:
            payload["sections"] = sections
        if project_type is not None:
            payload["project_type"] = project_type

        self._client.patch(make_url(self._root_path, self.id), data=payload)

        if name is not None:
            self.name = name
        if sections is not None:
            self.sections = sections
        if project_type is not None:
            self.project_type = project_type

    def delete(self) -> None:
        """Delete the compliance documentation template."""
        self._client.delete(make_url(self._root_path, self.id))
