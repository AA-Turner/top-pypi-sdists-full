from cnvrgv2.config import routes
from cnvrgv2.config.error_messages import LOCAL_COMMIT_DOESNT_EXIST_ERROR
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.base.data_owner import DataOwner
from cnvrgv2.modules.commits.project_commit import ProjectCommit
from cnvrgv2.modules.flows.flows_client import FlowsClient
from cnvrgv2.modules.labels.project_labels_client import ProjectLabelsClient
from cnvrgv2.modules.project_settings import ProjectSettings
from cnvrgv2.modules.workflows import EndpointsClient, ExperimentsClient, WebappsClient, WorkspacesClient
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator


class Project(DataOwner):
    available_attributes = {
        "title": str,
        "p_tags": list,
        "git": bool,
        "start_commit": str,
        "commit": str,
        "git_url": str,
        "git_branch": str,
        "num_files": int,
        "last_commit": str,
        "public": bool
    }

    def __init__(self, context=None, slug=None, attributes=None):
        # Init data attributes
        super().__init__()

        self._context = Context(context=context)

        # Set current context scope to current project
        if slug:
            self._context.set_scope(SCOPE.PROJECT, slug)

        scope = self._context.get_scope(SCOPE.PROJECT)

        self._proxy = Proxy(context=self._context)
        self._route = routes.PROJECT_BASE.format(scope["organization"], scope["project"])
        self._attributes = attributes or {}
        self.slug = scope["project"]

        self._init_clients()

    def save(self):
        pass

    def delete(self):
        """
        Deletes the current project
        @return: None
        """
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE)

    def _init_clients(self):
        self.workspaces = WorkspacesClient(self)
        self.endpoints = EndpointsClient(self)
        self.webapps = WebappsClient(self)
        self.experiments = ExperimentsClient(self)
        self.settings = ProjectSettings(self)
        self.flows = FlowsClient(self._context)
        self.labels = ProjectLabelsClient(self)

    def _validate_config_ownership(self):
        return self.slug == self._config.project_slug

    def save_config(self, local_config_path=None):
        """
        Saves the project configuration in the local folder
        @return: None
        """

        if not self.local_commit:
            raise CnvrgError(LOCAL_COMMIT_DOESNT_EXIST_ERROR)

        self._config.update(local_config_path=local_config_path, **{
            "project_slug": self.slug,
            "organization": self._context.organization,
            "git": getattr(self, "git", False),
            "commit_sha1": self.local_commit
        })

    def list_commits(self, filter={}, sort="-id"):
        """
        List all commits in a specific project
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields commit objects
        """
        scope = self._context.get_scope(SCOPE.PROJECT)
        list_commits_url = routes.PROJECT_COMMITS_BASE.format(scope["organization"], scope["project"])

        return api_list_generator(
            context=self._context,
            route=list_commits_url,
            filter=self._get_filter_object(filter),
            object=ProjectCommit,
            sort=sort,
            identifier="sha1"
        )

    def _get_filter_object(self, filter):

        conditions = [{
            'key': key if key != 'job_id' else 'job_slug',
            'operator': 'is',
            'value': filter[key]} for key in filter.keys()]

        return {
            "operator": 'AND',
            "conditions": conditions,
        }
