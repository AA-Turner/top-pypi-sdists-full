import os

import requests

from cnvrgv2.config import Config, CONFIG_VERSION
from cnvrgv2.config import error_messages, routes
from cnvrgv2.config.config import SSO_VERSION
from cnvrgv2.errors import CnvrgArgumentsError, CnvrgError, CnvrgHttpError, CnvrgLoginError
from cnvrgv2.modules.users.users_client import UsersClient
from cnvrgv2.proxy import HTTP, Proxy


class SCOPE:
    PROJECT = {
        "key": "project",
        "dependencies": ["organization", "user"]
    }
    IMAGE = {
        "key": "image",
        "dependencies": ["organization", "user"]
    }
    REGISTRY = {
        "key": "registry",
        "dependencies": ["organization", "user"]
    }
    LABEL = {
        "key": "label",
        "dependencies": ["organization", "user"]
    }
    VOLUME = {
        "key": "volume",
        "dependencies": ["organization", "user"]
    }
    STORAGE_CLASS = {
        "key": "storage_class",
        "dependencies": ["organization", "user"]
    }
    DATASET = {
        "key": "dataset",
        "dependencies": ["organization", "user"]
    }
    MEMBER = {
        "key": "member",
        "dependencies": ["organization"]
    }
    LIBRARY = {
        "key": "library",
        "dependencies": ["organization", "user"]
    }
    LIBRARY_VERSION = {
        "key": "library_version",
        "dependencies": ["library", "organization", "user"]
    }
    COMMIT = {
        "key": "commit",
        "dependencies": ["dataset", "organization", "user"]
    }
    QUERY = {
        "key": "query",
        "dependencies": ["dataset", "organization", "user"]
    }
    RESOURCE = {
        "key": "resource",
        "dependencies": ["organization", "user"]
    }
    TEMPLATE = {
        "key": "template",
        "dependencies": ["resource", "organization", "user"]
    }
    EXPERIMENT = {
        "key": "experiment",
        "dependencies": ["project", "organization", "user"]
    }
    WORKSPACE = {
        "key": "notebooksession",
        "dependencies": ["project", "organization", "user"]
    }
    WEBAPP = {
        "key": "webapp",
        "dependencies": ["project", "organization", "user"]
    }
    ENDPOINT = {
        "key": "endpoint",
        "dependencies": ["project", "organization", "user"]
    }
    FLOW = {
        "key": "flow",
        "dependencies": ["project", "organization", "user"]
    }
    FLOW_VERSION = {
        "key": "flow-version",
        "dependencies": ["flow", "project", "organization", "user"]
    }
    ORGANIZATION = {
        "key": "organization",
        "dependencies": ["user"]
    }
    DATASOURCE = {
        "key": "datasource",
        "dependencies": ["organization", "user"]
    }

    @classmethod
    def scopes(cls):
        """
        Calculates all of the scopes from the class attributes
        @return: scope list
        """
        scopes = []
        for attr in dir(cls):
            if not callable(getattr(cls, attr)) and not attr.startswith("__"):
                scopes.append(getattr(cls, attr)["key"])
        return scopes


class Context:
    def __init__(
            self, context=None, domain=None, user=None, password=None, organization=None, token=None,
            sso_version=SSO_VERSION.CAPI
    ):
        # Set the credentials variables:
        self.token = None
        self.domain = None
        self.user = None
        self.sso_version = sso_version
        self.digest = None

        # Set scope variables:
        for scope in SCOPE.scopes():
            setattr(self, scope, None)

        # If a context is passed, perform a deep copy and return
        if context:
            self._copy_context(context=context, organization=organization)
            return

        # Cannot pass username/password without a domain+username+password or domain + user + token
        if (user or password) and not all([domain, user, password]) and not all([domain, user, token]):
            raise CnvrgArgumentsError(error_messages.CONTEXT_BAD_ARGUMENTS)

        # If a domain is passed, init a blank Cnvrg client
        if domain:
            self.domain = domain

            # Attempt to authenticate using the credentials if they were passed
            if user:
                self._authenticate(domain, user, password, token)
        else:
            self._load_credentials()

        # Override organization if it was explicitly passed
        if organization:
            self.organization = organization

        self.ensure_organization_exist(self.organization)

    def get_scope(self, scope):
        """
        Checks if the current context contains the relevant scope
        @param scope: a SCOPE object constant
        @raise CnvrgError: if the context does not contain the required scope dependencies
        @return: scope dictionary
        """

        dependencies_dict = self._check_dependencies(scope)
        cur_scope = getattr(self, scope["key"], None)
        if cur_scope is None:
            error_msg = error_messages.CONTEXT_SCOPE_BAD_SCOPE.format(scope["key"])
            raise CnvrgError(error_msg)

        return {scope["key"]: cur_scope, **dependencies_dict}

    def set_scope(self, scope, slug):
        """
        Checks if the current context contains the relevant scope and sets new scope
        @param scope: a SCOPE object constant
        @param slug: scope object slug
        @raise CnvrgError: if the context does not contain the required scope dependencies
        @return: slug/None
        """
        if scope == SCOPE.ORGANIZATION:
            self.ensure_organization_exist(slug)

        self._check_dependencies(scope)
        setattr(self, scope["key"], slug)

    def save(self):
        """
        Creates a .cnvrg/config file to reuse authentication.
        Config save will only work in organization context, otherwise an error will be raised
        @raise CnvrgError: Tried to save without having at least organization context
        @return: Boolean depending if context save was successful
        """
        config = Config()
        # Will throw a CnvrgError if organization context is not present
        config_data = self._generate_context_dict()
        config.update(**config_data)

    def _copy_context(self, context, organization=None):
        """
        Performs a deep copy of the supplied context into the current one
        @param context: The source context
        @param organization: Organization name to override
        @return: None
        """
        self.token = context.token
        self.sso_version = context.sso_version
        self.domain = context.domain
        self.user = context.user
        self.digest = context.digest

        for scope in SCOPE.scopes():
            target_attr = getattr(context, scope, None)
            setattr(self, scope, target_attr)

        if organization:
            self.organization = organization

    def _check_dependencies(self, scope):
        """
        This function checks that the requested scope has all of its dependencies initialized
        @param scope: The scope const we want to check
        @return: dict of scopes and their slugs
        """
        # Build scope object
        scope_dict = {}
        for dependency in scope["dependencies"]:
            dependency_slug = getattr(self, dependency, None)
            if dependency_slug is None:
                error_msg = error_messages.CONTEXT_SCOPE_BAD_DEPENDENCIES.format(scope["key"], dependency)
                raise CnvrgError(error_msg)
            else:
                scope_dict[dependency] = dependency_slug

        return scope_dict

    def _authenticate(self, domain, user, password, user_token=None):
        """
        Performs authentication against Cnvrg and retrieves the auth token
        @param domain: Cnvrg app domain
        @param user: Email with which the user was registered
        @param password: Password with which the user was registered
        @param user_token: user authentication token instead of password
        @return: None
        """
        auth = UsersClient(domain=domain, token=user_token)
        self.sso_version = auth.sso_version

        if password is None:
            password = ""

        # Will raise an exception if login did not succeed
        token, organization, sso_enabled, digest = auth.login(user=user, password=password, token=user_token)

        if user_token is not None and sso_enabled:
            self.token = user_token
        else:
            self.token = token
        self.user = user
        self.organization = organization
        self.digest = digest

        # We don't allow users without an organization to use the context
        if organization is None:
            raise CnvrgError(error_messages.USER_NO_ORGANIZATION)

    def _load_credentials(self):
        """
        Attempts to login using either environment variables or the global Cnvrg config file
        @raise: CnvrgError if cannot login using either method
        @return: None
        """
        logged_in = self._load_from_env() or self._load_from_config()
        if not logged_in:
            raise CnvrgLoginError(error_messages.CONTEXT_BAD_ENV_VARIABLES)

    def _load_from_env(self):
        """
        Attempts to find credentials in environment variables
        @return: Boolean
        """
        # user token is the API token
        # In cnvrg jobs this can be the API token or the SSO token
        user_token = os.environ.get("CNVRG_TOKEN", None)
        jwt_token = os.environ.get("CNVRG_JWT_TOKEN", None)
        provided_token = user_token or jwt_token
        domain = os.environ.get("CNVRG_URL")
        user_email = os.environ.get("CNVRG_EMAIL")
        organization = os.environ.get("CNVRG_ORGANIZATION")
        digest = os.environ.get("CNVRG_SHA_DIGEST")

        if not all([provided_token, domain, user_email, organization]):
            return False

        self.domain = domain
        self.user = user_email
        self.organization = organization
        self.digest = digest
        self.sso_version = os.environ.get("CNVRG_SSO_VERSION", SSO_VERSION.CAPI)

        # Pod-specific env vars
        project = os.environ.get("CNVRG_PROJECT")
        dataset = os.environ.get("CNVRG_DATASET")

        if project:
            self.project = project
        if dataset:
            self.dataset = dataset

        job_slug = os.environ.get("CNVRG_JOB_ID")
        job_type = os.environ.get("CNVRG_JOB_TYPE")

        if job_type is not None:
            setattr(self, job_type.lower(), job_slug)

        # In case user is logging in using environment variables
        # This might be the user's simple token which should be exchanged for a JWT token
        if user_token and jwt_token is None:
            self._authenticate(self.domain, self.user, None, user_token)
        else:
            self.token = jwt_token
        return True

    def _load_from_config(self):
        """
        Attempts to find credentials in local/global config file
        @return: Boolean
        """
        config = Config()
        if not config:
            return False

        token, domain, user = config.get_credential_variables()

        # Context variables
        organization = config.organization
        digest = config.digest

        if not all([token, domain, user, organization]):
            return False

        self.token = token
        self.sso_version = config.sso_version
        self.domain = domain
        self.user = user
        self.organization = organization
        self.digest = digest

        if config.project_slug:
            self.project = config.project_slug
        if config.dataset_slug:
            self.dataset = config.dataset_slug

        return True

    def _generate_context_dict(self):
        """
        Generates a context dict to save in a local config file
        @return: dict
        """
        if not all([self.token, self.domain, self.user, self.organization]):
            raise CnvrgError(error_messages.CONTEXT_CANT_SAVE)

        context = {
            "user": self.user,
            "token": self.token,
            "domain": self.domain,
            "version": CONFIG_VERSION,
            "organization": self.organization,
            "check_certificate": False
        }

        if self.project:
            context["project_slug"] = self.project

        if self.dataset:
            context["dataset_slug"] = self.dataset

        return context

    def ensure_organization_exist(self, name):
        try:
            proxy = Proxy(domain=self.domain, token=self.token, sso_version=self.sso_version)
            organization_route = routes.ORGANIZATION_BASE.format(name)

            proxy.call_api(route=organization_route, http_method=HTTP.GET)

        except CnvrgHttpError as e:
            if e.status_code == requests.codes.not_found:
                raise CnvrgArgumentsError(error_messages.ORGANIZATION_DOESNT_EXIST)
            else:
                # Don't suppress unexpected exceptions
                raise e

    def get_env_variables(self):
        """
        Attempts to find credentials in environment variables
        @return: token, domain, user
        """
        # Credential variables
        token = self.token
        domain = self.domain
        user = self.user
        return token, domain, user
