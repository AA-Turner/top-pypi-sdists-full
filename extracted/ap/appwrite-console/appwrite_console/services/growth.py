from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..enums.conversation_type import ConversationType
from ..input_file import InputFile
from ..models.growth_conversation import GrowthConversation


class Growth(Service):

    def __init__(self, client) -> None:
        super(Growth, self).__init__(client)

    def create_conversation(
        self,
        type: ConversationType,
        email: Optional[str] = None,
        name: Optional[str] = None,
        subject: Optional[str] = None,
        message: Optional[str] = None,
        organization_id: Optional[str] = None,
        project_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        attachment: Optional[InputFile] = None,
        on_progress=None,
    ) -> GrowthConversation:
        """
        Create a conversation with the Appwrite team: support requests, product and docs feedback, enterprise, startup and partner applications, and event sponsorship requests. Signed in console users are identified by their session or JWT; everyone else must pass an email. Attach a file of up to 5MB to support and feedback conversations.

        Parameters
        ----------
        type : ConversationType
            Conversation type.
        email : Optional[str]
            Email address to reply to. Required without a console session, ignored with one.
        name : Optional[str]
            Name of the person filing the conversation. Required for enterprise, startup, partner and sponsorship.
        subject : Optional[str]
            Conversation subject.
        message : Optional[str]
            Conversation message. Required for support, feedback, enterprise and partner.
        organization_id : Optional[str]
            Organization ID the conversation is about. Kept only when the session user is a member.
        project_id : Optional[str]
            Project ID the conversation is about. Kept only when it belongs to the kept organization.
        attributes : Optional[Dict[str, Any]]
            Additional attributes for the conversation type, as an object or a JSON string.
        attachment : Optional[InputFile]
            File attachment, support and feedback only, max 5MB.
        on_progress : callable, optional
            Optional callback for upload progress

        Returns
        -------
        GrowthConversation
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/growth/conversations'
        api_params = {}
        if type is None:
            raise AppwriteException('Missing required parameter: "type"')
        api_params['type'] = self._normalize_value(type)
        if email is not None:
            api_params['email'] = self._normalize_value(email)
        if name is not None:
            api_params['name'] = self._normalize_value(name)
        if subject is not None:
            api_params['subject'] = self._normalize_value(subject)
        if message is not None:
            api_params['message'] = self._normalize_value(message)
        if organization_id is not None:
            api_params['organizationId'] = self._normalize_value(organization_id)
        if project_id is not None:
            api_params['projectId'] = self._normalize_value(project_id)
        if attributes is not None:
            api_params['attributes'] = self._normalize_value(attributes)
        if attachment is not None:
            api_params['attachment'] = self._normalize_value(attachment)

        param_name = 'attachment'

        upload_id = ''

        response = self.client.chunked_upload(
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'multipart/form-data',
                'accept': 'application/json',
            },
            api_params,
            param_name,
            on_progress,
            upload_id,
            method='post',
        )

        return self._parse_response(response, model=GrowthConversation)

    def create_installation(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        domain: Optional[str] = None,
        database: Optional[str] = None,
        host_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
        os: Optional[str] = None,
        arch: Optional[str] = None,
        cpus: Optional[float] = None,
        ram: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Record a self-hosted installation. Every report is stored as its own row; the admin email is optional because headless CLI installs create no account.

        Parameters
        ----------
        email : Optional[str]
            Admin email from the installation, when an account was created.
        name : Optional[str]
            Admin name.
        version : Optional[str]
            Appwrite version.
        domain : Optional[str]
            Installation domain.
        database : Optional[str]
            Database adapter.
        host_ip : Optional[str]
            Resolved installation host IP address.
        user_agent : Optional[str]
            Installation user agent.
        os : Optional[str]
            Installation operating system.
        arch : Optional[str]
            Installation CPU architecture.
        cpus : Optional[float]
            Installation CPU count.
        ram : Optional[float]
            Installation RAM in MB.
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/growth/installations'
        api_params = {}
        if email is not None:
            api_params['email'] = self._normalize_value(email)
        if name is not None:
            api_params['name'] = self._normalize_value(name)
        if version is not None:
            api_params['version'] = self._normalize_value(version)
        if domain is not None:
            api_params['domain'] = self._normalize_value(domain)
        if database is not None:
            api_params['database'] = self._normalize_value(database)
        if host_ip is not None:
            api_params['hostIp'] = self._normalize_value(host_ip)
        if user_agent is not None:
            api_params['userAgent'] = self._normalize_value(user_agent)
        if os is not None:
            api_params['os'] = self._normalize_value(os)
        if arch is not None:
            api_params['arch'] = self._normalize_value(arch)
        if cpus is not None:
            api_params['cpus'] = self._normalize_value(cpus)
        if ram is not None:
            api_params['ram'] = self._normalize_value(ram)

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response
