#
# Copyright 2025 DataRobot, Inc. and its affiliates.
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

import re
from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot._compat import String
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate

variable_trafaret = t.Dict({
    t.Key("name"): String(),
    t.Key("type"): String(),
    t.Key("description"): String(allow_blank=True),
}).ignore_extra("*")


prompt_template_version_trafaret = t.Dict({
    t.Key("id"): String(),
    t.Key("prompt_template_id"): String(),
    t.Key("prompt_text"): String(),
    t.Key("commit_comment"): String(allow_blank=True),
    t.Key("version"): t.Int,
    t.Key("variables"): t.List(variable_trafaret),
    t.Key("creation_date"): String(),
    t.Key("creation_user_id"): String(),
    t.Key("user_name"): String(allow_blank=True),
}).ignore_extra("*")


prompt_template_trafaret = t.Dict({
    t.Key("id"): String(),
    t.Key("name"): String(),
    t.Key("description"): String(allow_blank=True),
    t.Key("creation_date"): String(),
    t.Key("creation_user_id"): String(),
    t.Key("last_update_date"): String(),
    t.Key("last_update_user_id"): String(),
    t.Key("user_name"): String(allow_blank=True),
    t.Key("version_count"): t.Int,
}).ignore_extra("*")


class Variable(APIObject):
    """
    A variable used in prompt templates.

    Attributes
    ----------
    name : str
        Variable name.
    type : str
        Variable type (e.g., "str", "int").
    description : str
        Description of the variable.
    """

    _converter = variable_trafaret

    def __init__(self, name: str, type: str = "str", description: str = ""):
        self.name = name
        self.type = type
        self.description = description

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, type={self.type!r})"

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "type": self.type, "description": self.description}


class PromptTemplateVersion(APIObject):
    """
    A specific version of a prompt template.

    Attributes
    ----------
    id : str
        Version ID.
    prompt_template_id : str
        ID of the parent prompt template.
    prompt_text : str
        The prompt text with variables in {{variable}} format.
    commit_comment : str
        Comment describing this version.
    version : int
        Version number.
    variables : List[Variable]
        List of variables used in the prompt.
    creation_date : str
        ISO-8601 formatted timestamp of when the version was created.
    creation_user_id : str
        ID of the user who created the version.
    user_name : str
        Name of the user who created the version.
    """

    _path = "api/v2/genai/promptTemplates"
    _converter = prompt_template_version_trafaret

    def __init__(
        self,
        id: str,
        prompt_template_id: Optional[str] = None,
        prompt_text: Optional[str] = None,
        commit_comment: Optional[str] = None,
        version: Optional[int] = None,
        variables: Optional[List[Dict[str, str]]] = None,
        creation_date: Optional[str] = None,
        creation_user_id: Optional[str] = None,
        user_name: Optional[str] = None,
    ):
        self.id = id
        self.prompt_template_id = prompt_template_id
        self.prompt_text = prompt_text
        self.commit_comment = commit_comment
        self.version = version
        self.variables = [Variable.from_server_data(v) for v in variables] if variables else []
        self.creation_date = creation_date
        self.creation_user_id = creation_user_id
        self.user_name = user_name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id!r}, "
            f"prompt_template_id={self.prompt_template_id!r}, version={self.version})"
        )

    @classmethod
    def get(cls, prompt_template_id: str, prompt_template_version_id: str) -> PromptTemplateVersion:
        """
        Get a specific prompt template version by ID.

        Parameters
        ----------
        prompt_template_id : str
            The ID of the prompt template.
        prompt_template_version_id : str
            The ID of the version to retrieve.

        Returns
        -------
        PromptTemplateVersion
            The requested prompt template version.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> version = dr.genai.PromptTemplateVersion.get("prompt_template_id", "prompt_template_version_id")
        """
        url = f"{cls._client.domain}/{cls._path}/{prompt_template_id}/versions/{prompt_template_version_id}/"
        r_data = cls._client.get(url)
        return cls.from_server_data(r_data.json())

    @classmethod
    def create(
        cls,
        prompt_template_id: str,
        prompt_text: str,
        variables: Optional[List[Variable]] = None,
        commit_comment: str = "",
    ) -> PromptTemplateVersion:
        """
        Create a new version of a prompt template.

        Parameters
        ----------
        prompt_template_id : str
            The ID of the prompt template.
        prompt_text : str
            The prompt text with variables in {{variable}} format.
        variables : List[Variable], optional
            List of Variable objects defining the variables used in the prompt template.
        commit_comment : str, optional
            Comment describing this version.

        Returns
        -------
        PromptTemplateVersion
            The created version.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.genai.prompt_template import Variable
            >>> version = dr.genai.PromptTemplateVersion.create(
            ...     prompt_template_id="507f1f77bcf86cd799439011",
            ...     prompt_text="Hello {{name}}, regarding {{issue}}",
            ...     variables=[
            ...         Variable(name="name", type="str", description="Customer name"),
            ...         Variable(name="issue", type="str", description="Issue type")
            ...     ],
            ...     commit_comment="Initial version"
            ... )
        """
        payload = {
            "promptText": prompt_text,
            "variables": [v.to_dict() for v in variables] if variables else [],
            "commitComment": commit_comment,
        }
        url = f"{cls._client.domain}/{cls._path}/{prompt_template_id}/versions/"
        response = cls._client.post(url, data=payload)
        return cls.from_server_data(response.json())

    @classmethod
    def list(
        cls,
        prompt_template_id: str,
    ) -> List[PromptTemplateVersion]:
        """
        List all versions of a prompt template.

        Parameters
        ----------
        prompt_template_id : str
            The ID of the prompt template.

        Returns
        -------
        List[PromptTemplateVersion]
            A list of versions for the template.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> versions = dr.genai.PromptTemplateVersion.list(
            ...     prompt_template_id="507f1f77bcf86cd799439011"
            ... )
        """
        url = f"{cls._client.domain}/{cls._path}/{prompt_template_id}/versions/"
        data = unpaginate(url, None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def list_all(
        cls,
        prompt_template_ids: Optional[List[str]] = None,
    ) -> List[PromptTemplateVersion]:
        """
        List prompt template versions across multiple templates.

        Parameters
        ----------
        prompt_template_ids : List[str], optional
            Filter versions to only those belonging to these prompt template IDs.
            If not provided, returns versions for all accessible templates.

        Returns
        -------
        List[PromptTemplateVersion]
            A list of prompt template versions.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> # List all versions across all templates
            >>> versions = dr.genai.PromptTemplateVersion.list_all()
            >>> # List versions for specific templates
            >>> versions = dr.genai.PromptTemplateVersion.list_all(
            ...     prompt_template_ids=["template_id_1", "template_id_2"]
            ... )
        """
        params: Dict[str, List[str]] = {}
        if prompt_template_ids:
            params["promptTemplatesIds"] = prompt_template_ids

        url = f"{cls._client.domain}/{cls._path}/versions/"
        data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(item) for item in data]

    def render(self, variables: Optional[Dict[str, Any]] = None, **kwargs: Any) -> str:
        """
        Render the prompt text by substituting variables.

        Parameters
        ----------
        variables : Optional[Dict[str, Any]]
            Dictionary of variable names to values.
        **kwargs : Any
            Variable values as keyword arguments. These override values in the variables dict.

        Returns
        -------
        str
            Rendered prompt text with variables substituted.

        Raises
        ------
        ValueError
            If required variables are missing.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> version = dr.genai.PromptTemplateVersion.get("template_id", "version_id")
            >>> version.render(name="Alice", issue="billing")
            'Hello Alice, regarding billing...'
        """
        all_vars = {}
        if variables:
            all_vars.update(variables)
        all_vars.update(kwargs)

        if self.prompt_text is None:
            raise ValueError("Cannot render template: prompt_text is None")

        required_vars = {var.name for var in self.variables}
        provided_vars = set(all_vars.keys())
        missing = required_vars - provided_vars

        if missing:
            raise ValueError(f"Missing required variables: {', '.join(sorted(missing))}")

        rendered_text = self.prompt_text
        for var_name, var_value in all_vars.items():
            pattern = r"\{\{\s*" + re.escape(var_name) + r"\s*\}\}"
            rendered_text = re.sub(pattern, str(var_value), rendered_text)

        return rendered_text

    def to_fstring(self) -> str:
        """
        Convert the prompt text from {{variable}} format to Python f-string {variable} format.

        This method transforms template placeholders from double-brace format ({{variable}})
        to single-brace format ({variable}), making the template compatible with Python
        f-string syntax. Whitespace around variable names is automatically stripped.

        Returns
        -------
        str
            Prompt text with variables in f-string format.

        Raises
        ------
        ValueError
            If prompt_text is None.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> version = dr.genai.PromptTemplateVersion.get("template_id", "version_id")
            >>> # Original: "Hello {{name}}, regarding {{issue}}"
            >>> fstring_template = version.to_fstring()
            >>> # Result: "Hello {name}, regarding {issue}"
            >>> # Can now be used with f-string evaluation:
            >>> name = "Alice"
            >>> issue = "billing"
            >>> result = eval(f'f"{fstring_template}"')
        """
        if self.prompt_text is None:
            raise ValueError("Cannot convert template: prompt_text is None")

        import re

        fstring_text = re.sub(r'\{\{\s*(\w+)\s*\}\}', r'{\1}', self.prompt_text)

        return fstring_text


class PromptTemplate(APIObject):
    """
    A prompt template that can have multiple versions.

    Attributes
    ----------
    id : str
        Prompt template ID.
    name : str
        Prompt template name.
    description : str
        Description of the prompt template.
    creation_date : str
        ISO-8601 formatted timestamp of when the template was created.
    creation_user_id : str
        ID of the user who created the template.
    last_update_date : str
        ISO-8601 formatted timestamp of when the template was last updated.
    last_update_user_id : str
        ID of the user who last updated the template.
    user_name : str
        Name of the user who created the template.
    version_count : int
        Number of versions this template has.
    """

    _path = "api/v2/genai/promptTemplates"
    _converter = prompt_template_trafaret

    def __init__(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        creation_date: Optional[str] = None,
        creation_user_id: Optional[str] = None,
        last_update_date: Optional[str] = None,
        last_update_user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        version_count: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.creation_date = creation_date
        self.creation_user_id = creation_user_id
        self.last_update_date = last_update_date
        self.last_update_user_id = last_update_user_id
        self.user_name = user_name
        self.version_count = version_count

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"

    @classmethod
    def create(cls, name: str, description: str = "") -> PromptTemplate:
        """
        Create a new prompt template.

        Parameters
        ----------
        name : str
            Name of the prompt template.
        description : str, optional
            Description of the prompt template.

        Returns
        -------
        PromptTemplate
            The created prompt template.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> template = dr.genai.PromptTemplate.create(
            ...     name="Customer Support",
            ...     description="Template for support responses"
            ... )
        """
        payload = {"name": name, "description": description}
        url = f"{cls._client.domain}/{cls._path}/"
        response = cls._client.post(url, data=payload)
        return cls.from_server_data(response.json())

    @classmethod
    def list(
        cls,
        sort: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[PromptTemplate]:
        """
        List all prompt templates available to the user.

        Parameters
        ----------
        sort : str, optional
            Prefix the attribute name with a dash to sort in descending order,
            e.g. sort='-creationDate'.
        search : str, optional
            Filter templates by name containing this string.

        Returns
        -------
        List[PromptTemplate]
            A list of prompt templates.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> templates = dr.genai.PromptTemplate.list(sort="-creationDate")
        """
        params: Dict[str, Any] = {}
        if sort is not None:
            params["sort"] = sort
        if search is not None:
            params["search"] = search

        url = f"{cls._client.domain}/{cls._path}/"
        data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, prompt_template_id: str) -> PromptTemplate:
        """
        Get a prompt template by ID.

        Parameters
        ----------
        prompt_template_id : str
            The ID of the prompt template to retrieve.

        Returns
        -------
        PromptTemplate
            The requested prompt template.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> template = dr.genai.PromptTemplate.get("507f1f77bcf86cd799439011")
        """
        url = f"{cls._client.domain}/{cls._path}/{prompt_template_id}/"
        r_data = cls._client.get(url)
        return cls.from_server_data(r_data.json())

    def create_version(
        self,
        prompt_text: str,
        variables: Optional[List[Variable]] = None,
        commit_comment: str = "",
    ) -> PromptTemplateVersion:
        """
        Create a new version of this prompt template.

        Parameters
        ----------
        prompt_text : str
            The prompt text with variables in {{variable}} format.
        variables : List[Variable], optional
            List of Variable objects defining the variables used in the prompt template.
            Defaults to None, which sends an empty list to the API.
        commit_comment : str, optional
            Comment describing this version.

        Returns
        -------
        PromptTemplateVersion
            The created version.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.models.genai.prompt_template import Variable
            >>> template.create_version(
            ...     prompt_text="Hello {{name}}, regarding {{issue}}",
            ...     variables=[
            ...         Variable(name="name", type="str", description="Customer name"),
            ...         Variable(name="issue", type="str", description="Issue type")
            ...     ],
            ...     commit_comment="Initial version"
            ... )
        """
        return PromptTemplateVersion.create(self.id, prompt_text, variables, commit_comment)

    def list_versions(self) -> List[PromptTemplateVersion]:
        """
        List all versions of this prompt template.

        Returns
        -------
        List[PromptTemplateVersion]
            A list of versions for this template.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> versions = template.list_versions()
        """
        return PromptTemplateVersion.list(self.id)

    def get_version(self, prompt_template_version_id: str) -> PromptTemplateVersion:
        """
        Get a specific version of this prompt template.

        Parameters
        ----------
        prompt_template_version_id : str
            The ID of the version to retrieve.

        Returns
        -------
        PromptTemplateVersion
            The requested version.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> template = dr.genai.PromptTemplate.get("507f1f77bcf86cd799439011")
            >>> version = template.get_version("507f1f77bcf86cd799439012")
        """
        return PromptTemplateVersion.get(self.id, prompt_template_version_id)

    def get_latest_version(self) -> Optional[PromptTemplateVersion]:
        """
        Get the latest version of this prompt template.

        Returns
        -------
        Optional[PromptTemplateVersion]
            The latest version, or None if no versions exist.

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> template = dr.genai.PromptTemplate.get("507f1f77bcf86cd799439011")
            >>> latest = template.get_latest_version()
            >>> if latest:
            ...     print(f"Version {latest.version}")
        """
        versions = self.list_versions()
        if not versions:
            return None
        return max(versions, key=lambda v: v.version)  # type: ignore[arg-type, return-value]
