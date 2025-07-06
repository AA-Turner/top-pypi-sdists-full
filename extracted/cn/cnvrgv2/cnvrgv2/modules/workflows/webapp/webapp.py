import os
import shutil
import time
from datetime import datetime

from cnvrgv2.config import routes, error_messages
from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.base.workflow_instance_base import WorkflowInstanceBase
from cnvrgv2.modules.workflows.workflow_utils import WorkflowStatuses
from cnvrgv2.proxy import Proxy
from cnvrgv2.context import Context, SCOPE


class WebappType:
    SHINY = "rshiny"
    DASH = "dash"
    VOILA = "voila"
    TENSORBOARD = "tensorboard"


class Webapp(WorkflowInstanceBase):
    available_attributes = {
        "webapp_type": str,
        "template_ids": list,
        "template_id": int,
        "compute": str,
        "num_of_exps": int,
        "updated_at": datetime,
        "iframe_url": str,
        "is_public": bool,
        "last_opened": datetime,
        "current_step": int,
        "strip_sources": bool,
        "copy_frequency": int,
        "file_name": str,
        "experiments": list,
        **WorkflowInstanceBase.available_attributes
    }

    def __init__(self, context=None, slug=None, attributes=None):
        self._context = Context(context=context)

        # Set current context scope to current project
        if slug:
            self._context.set_scope(SCOPE.WEBAPP, slug)

        self.scope = self._context.get_scope(SCOPE.WEBAPP)

        self._proxy = Proxy(context=self._context)
        self._route = routes.WEBAPP_BASE.format(self.scope["organization"], self.scope["project"], self.scope["webapp"])
        self._attributes = attributes or {}
        self._type = "Webapp"
        self.slug = self.scope["webapp"]

    def start(self):
        """
        Override start from workflows_base to remove functionality.
        start() is only relevant for Endpoints & Workspaces
        """
        raise AttributeError("'Webapp' object has no attribute 'start'")

    def sync_remote(self, commit_msg=None):
        raise NotImplementedError()

    def compare_experiments(self, frequency=5):
        """
        Used for tensorboard, Download tfevents to predefined location {exp_slug}/{project}/{files}
        New experiments can be added to the webapp experiments attribute in server side.
        @param frequency: [integer] number in seconds used for interval between each commit download
        """
        # Importing here to avoid circular dependencies (webapp <-> project)
        from cnvrgv2 import Project
        project = Project(context=self._context, slug=self.scope["project"])

        exps_map = {}

        while True:
            self.reload()
            slugs = self.experiments
            if not slugs:
                raise CnvrgError(error_messages.EXPERIMENT_SLUGS_NOT_FOUND)

            for slug in slugs:
                if slug not in exps_map:
                    exp = project.experiments.get(slug)
                else:
                    # end commit already cloned, skipping it
                    continue
                if exp.end_commit is not None and exp.status != WorkflowStatuses.ONGOING:
                    self._download_tfevents_from_experiment(exp, project, exp.end_commit)
                    exps_map[slug] = exp
                else:
                    self._download_tfevents_from_experiment(exp, project, exp.last_successful_commit)
            time.sleep(frequency)

    def _download_tfevents_from_experiment(self, exp, project, commit_sha1):
        """
        Download tensorflow events to predefined location {exp_slug}/{project}/{files} using %tfevents% filter
        New experiments can be added to the webapp experiments attribute in server side.
        @param exp: [Experiment] Experiment object
        @param project: [Project] Project object
        @param commit_sha1: [String] the sha1 of the commit to download
        """
        # Check if commit_sh1 exists
        if commit_sha1 is None:
            return

        # Set destination folder
        base_dir = exp.slug

        # Clear previous logs
        if os.path.isdir(base_dir):
            shutil.rmtree(base_dir)

        # Change working_dir to destination folder
        old_working_dir = project.working_dir
        project.working_dir = base_dir

        # Download the commit with the requested filter
        project.clone(commit=commit_sha1, fullpath_filter="%tfevents%")

        # Revert to the previous working_dir
        project.working_dir = old_working_dir
