import time
from datetime import datetime

from cnvrgv2.config import routes
from cnvrgv2.config.error_messages import ARGUMENT_BAD_TYPE, EMPTY_ARGUMENT, NOT_LIST
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.data import ArtifactsDownloader
from cnvrgv2.errors import CnvrgArgumentsError, CnvrgError
from cnvrgv2.modules.base.workflow_instance_base import TagTypes, WorkflowInstanceBase
from cnvrgv2.modules.file import File
from cnvrgv2.modules.workflows.workflow_utils import WorkflowStatuses, WorkflowUtils
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.chart_utils import BarChart, Chart, Heatmap, LineChart, ScatterPlot
from cnvrgv2.utils.env_helper import ENV_KEYS
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.utils.log_utils import (
    LOGS_TYPE_ERROR, LOGS_TYPE_INFO, LOGS_TYPE_OUTPUT, LOGS_TYPE_WARNING,
    timestamp_for_logs
)
from cnvrgv2.utils.url_utils import urljoin


class Experiment(WorkflowInstanceBase):
    available_attributes = {
        "input": str,
        "href": str,
        "full_href": str,
        "remote": str,
        "ma": str,
        "tags": dict,
        "is_running": bool,
        "terminal_url": str,
        "termination_time": datetime,
        "end_commit": str,
        "last_successful_commit": str,
        "flow_slug": str,
        "flow_version_slug": str,
        "flow_version_id": str,

        **WorkflowInstanceBase.available_attributes
    }

    CHART_CLASSES = {
        'none': LineChart,
        'scatter': ScatterPlot,
        'bar': BarChart,
        'heatmap': Heatmap
    }

    def __init__(self, context=None, slug=None, attributes=None):
        super().__init__()
        self._context = Context(context=context)

        # Set current context scope to current project
        if slug:
            self._context.set_scope(SCOPE.EXPERIMENT, slug)

        self.scope = self._context.get_scope(SCOPE.EXPERIMENT)

        self._proxy = Proxy(context=self._context)
        self._route = routes.EXPERIMENT_BASE.format(
            self.scope["organization"],
            self.scope["project"],
            self.scope["experiment"]
        )
        self._attributes = attributes or {}
        self._type = "Experiment"
        self.slug = self.scope["experiment"]

    def finish(self, exit_status):
        # TODO: Remove after uniting finish and stop in server.
        #  Ask Leah if experiment should have finish as syntax (product wise)
        """
        Finishes the current experiment
        @param exit_status: exit status of the experiment
        @return: The finished experiment
        """
        finish_url = urljoin(self._route, routes.EXPERIMENT_FINISH_SUFFIX)
        attributes = {
            "exit_status": exit_status
        }

        return self._proxy.call_api(
            route=finish_url,
            http_method=HTTP.POST,
            payload=JAF.serialize(type=self._type, attributes=attributes)
        )

    def start(self):
        """
        Override start from workflows_base to remove functionality.
        start() is only relevant for Endpoints & Workspaces
        """
        raise AttributeError("'Experiment' object has no attribute 'start'")

    def restart(self):
        """
        Override restart from workflows_base to remove functionality.
        restart() is only relevant for webapps
        """
        raise AttributeError("'Experiment' object has no attribute 'restart'")

    def log_metric(self, chart: Chart):
        """
        Logs a chart of metrics for the current experiment
        @param chart: A chart object
        @return: The created chart object
        """

        create_chart_url = urljoin(self._route, routes.EXPERIMENT_CHARTS_SUFFIX)

        response = self._proxy.call_api(
            route=create_chart_url,
            http_method=HTTP.POST,
            payload=JAF.serialize(type=self._type, attributes=chart.to_dict())
        )

        NewChartClass = self.CHART_CLASSES.get(chart.chart_type)

        chart_kwargs = {**response.attributes, **response.attributes.get('settings')}
        chart_kwargs.pop('chart_type', None)

        new_chart = NewChartClass(**chart_kwargs)

        return new_chart

    def as_env(self):
        """
        @return: A dict representing current experiment for env use
        """
        return {
            ENV_KEYS["current_job_id"]: self.slug,
            ENV_KEYS["current_job_type"]: self._type,
            ENV_KEYS["current_project"]: self.scope["project"],
            ENV_KEYS["current_organization"]: self.scope["organization"],
        }

    def pull_artifacts(self, wait_until_success=False, poll_interval=10, commit_sha1=None):
        """
        pulls current experiment's artifacts to the local working dir
        @param wait_until_success: Wait until current experiment is done before pulling artifacts
        @param poll_interval: Is wait_until_success is True, time between status poll loops
        @return: None
        """
        if wait_until_success:
            WorkflowUtils.wait_for_statuses(self, WorkflowStatuses.SUCCESS, poll_interval=poll_interval)

        self.reload()

        commit = commit_sha1 if commit_sha1 is not None else self.last_commit
        # Start commit for git project is null
        base_commit = self.start_commit["sha1"] if self.start_commit else None
        downloader = ArtifactsDownloader(self, base_commit_sha1=base_commit, commit_sha1=commit, ignore_branches=True)
        while downloader.in_progress:
            time.sleep(1)

        if downloader.errors:
            raise CnvrgError(downloader.errors.args)
        return downloader

    def log_param(self, key, value=None):
        """
        Adds the given tag to the current experiment
        @param key: [String] The tag name
        @param value: [String] The tag value
        @return: None
        """
        # TODO: Add run async to this function and rest of log functions
        return self.tag(tag_type=TagTypes.SINGLE_TAG, key=key, value=value)

    def log_images(self, file_paths):
        """
        Saves the given images to the current experiment as a new commit
        Note that only images that will be saved via this function
        Will show as experiment visuals
        @param file_paths: list of paths of artifacts to save
        @return: None
        """
        commit_msg = "Log Images Commit"
        self.put_files(file_paths, message=commit_msg, job_slug=self.slug, tag_images=True)

    def log_artifacts(self, paths=None, git_diff=False, work_dir=None):
        """
        Saves the given artifacts to the current experiment as a new commit
        @param paths: list of paths of artifacts to save
        @param git_diff: upload files from git diff output in addition to the given paths
        @param work_dir: working directory param, path to files. i.e running command from dir A, files are in dir A/B.
        instead of sending paths B/*.*, set working_dir to B, and send path as *.*
        @return: None
        """
        if not paths and not git_diff:
            raise CnvrgArgumentsError(EMPTY_ARGUMENT.format("file_paths"))
        if not isinstance(paths, list):
            raise CnvrgArgumentsError(NOT_LIST.format("paths"))

        if work_dir:
            self.working_dir = work_dir

        commit_msg = "Log Artifacts Commit"
        self.put_files(paths, message=commit_msg, job_slug=self.slug, git_diff=git_diff)
        self.reload()

    def get_utilization(self):
        """
        Get experiment's utilization stats
        @return: Experiment's system stats data
        """
        return self._proxy.call_api(
            route=urljoin(self._route, routes.EXPERIMENT_GET_UTILIZATION_SUFFIX),
            http_method=HTTP.GET
        )

    def log(self, logs, log_level=LOGS_TYPE_INFO, timestamp=None):
        """
        Method to add logs to the experiment log
        @param logs: an array of logs you want to send
        @param log_level: level of the logs, exists in log_utils
        @param timestamp: timestamp for the logs, UTC now by default
        """
        if timestamp is None:
            timestamp = timestamp_for_logs()

        if type(timestamp) is not str:
            raise CnvrgArgumentsError({"timestamp": ARGUMENT_BAD_TYPE % ("str", type(timestamp))})

        if log_level not in (LOGS_TYPE_OUTPUT, LOGS_TYPE_ERROR, LOGS_TYPE_INFO, LOGS_TYPE_WARNING):
            raise CnvrgArgumentsError({"level": ARGUMENT_BAD_TYPE % ("logs level enum", log_level)})

        if type(logs) is not list:
            if type(logs) is str:
                # Give the user the option to only send one string
                logs = [logs]
            else:
                raise CnvrgArgumentsError({"level": ARGUMENT_BAD_TYPE % ("str", type(logs))})

        return self._proxy.call_api(
            route=urljoin(self._route, routes.EXPERIMENT_WRITE_LOGS),
            http_method=HTTP.POST,
            payload={
                "logs": logs,
                "log_level": log_level,
                "timestamp": timestamp
            }
        )

    def _generate_logs_route(self, offset, search, filter, page):
        """
        Generates the route for the logs api
        @param offset: Logs offset [int]
        @param search: searches through the logs and returns any logs that contain the specified string  [string]
        @param filter: list of logs type to filter ('cnvrg-info', 'cnvrg-error') [string]
        @param page: Logs pagination hash [hash]
        @return: route
        """
        if type(offset) is not int and offset is not None:
            raise CnvrgArgumentsError({"offset": ARGUMENT_BAD_TYPE.format("int", type(offset))})

        if type(page) is not dict and page is not None:
            raise CnvrgArgumentsError({"page": ARGUMENT_BAD_TYPE.format("dict", type(page))})

        if filter is None:
            filter = '["all"]'

        if page:
            offset = ""

        page_after = ""
        page_before = ""
        if page is not None:
            if "after" in page:
                page_after = page["after"]
            if "before" in page:
                page_before = page["before"]

        return routes.EXPERIMENT_LOGS_SUFFIX.format(offset, search, filter, page_after, page_before)

    def logs(self, offset=-1, search="", filter=None, page=None):
        """
        Retrieval of the last 40 logs of the experiment
        or
        use pagination
        @param offset: Logs offset [int]
        @param search: searches through the logs and returns any logs that contain the specified string  [string]
        @param filter: list of logs type to filter ('cnvrg-info', 'cnvrg-error') [string]
        @param page: Logs pagination hash [hash]
        @return: a list of the last 40 logs
        """

        route = self._generate_logs_route(offset, search, filter, page)

        response = self._proxy.call_api(
            route=urljoin(self._route, route),
            http_method=HTTP.GET,
        )

        return response

    def _rerun(self, sync=True, prerun=False, requirements=False):
        """
        Rerun experiment that's currently in debug mode
        @param sync: sync before rerunning
        @param prerun: run prerun.sh script
        @param requirements: install requirements file
        @return: None
        """
        rerun_url = urljoin(self._route, routes.EXPERIMENT_RERUN_SUFFIX)
        attributes = {
            "sync": sync,
            "prerun": prerun,
            "requirements": requirements
        }

        self._proxy.call_api(
            route=rerun_url,
            http_method=HTTP.POST,
            payload=JAF.serialize(type=self._type, attributes=attributes)
        )

    def list_charts(self):
        """
        List charts of an experiment
        @return: List of charts for the experiment
        """
        charts_url = urljoin(self._route, routes.EXPERIMENT_CHARTS_SUFFIX)

        response = self._proxy.call_api(
            route=charts_url,
            http_method=HTTP.GET
        )

        charts_list = []
        for chart_jaf in response.items:
            chart_type = chart_jaf.attributes.get('settings').get('chart_type')
            ChartClass = self.CHART_CLASSES.get(chart_type)

            chart_kwargs = {**chart_jaf.attributes, **chart_jaf.attributes.get('settings')}
            chart_kwargs.pop('chart_type', None)

            chart = ChartClass(**chart_kwargs)
            charts_list.append(chart)

        return charts_list

    def get_chart(self, key):
        """
        Get charts of an experiment
        @param key: key of chart we wish to get
        @return: Chart with given key
        """
        chart_url = urljoin(self._route, routes.EXPERIMENT_CHART_SUFFIX.format(key))

        response = self._proxy.call_api(
            route=chart_url,
            http_method=HTTP.GET
        )

        # If we couldn't find a chart with given key
        if not len(response.attributes):
            return None

        chart_type = response.attributes.get('settings').get('chart_type')
        ChartClass = self.CHART_CLASSES.get(chart_type)

        chart_kwargs = {**response.attributes, **response.attributes.get('settings')}
        chart_kwargs.pop('chart_type', None)

        chart = ChartClass(**chart_kwargs)

        return chart

    def update_chart(self, key, data, series_name=None):
        """
        Add data to an existing series in a chart
        @param key: key of chart we wish to update
        @param data: new data to add to series
        @param series_name: name of series to update (optional, will update default series without name)
        @return: Chart with given key
        """

        current_chart = self.get_chart(key)

        # Do nothing if we couldn't find given chart
        if not current_chart:
            return None

        # This will validate our data is in the right format for our chart
        formatted_data = current_chart.validate_series(data)

        update_chart_url = urljoin(self._route, routes.EXPERIMENT_CHARTS_SUFFIX)

        attributes = {
            "key": key,
            "series": [{"data": formatted_data, "name": series_name}]
        }

        response = self._proxy.call_api(
            route=update_chart_url,
            http_method=HTTP.PUT,
            payload=JAF.serialize(type=self._type, attributes=attributes)
        )

        ChartClass = self.CHART_CLASSES.get(current_chart.chart_type)

        chart_kwargs = {**response.attributes, **response.attributes.get('settings')}
        chart_kwargs.pop('chart_type', None)

        chart = ChartClass(**chart_kwargs)

        return chart

    def _wait_until_experiment_finish(self, poll_interval=10):
        """
        Busy waits until current experiment run is done
        @param poll_interval: time between status poll loops
        @return: The status of the experiment when done.
        """
        while self.is_running:
            time.sleep(poll_interval)
            self.reload()
        return self.status

    def merge_to_master(self, commit_sha1=None):
        """
        Merge commit to master (used to merge experiment artifacts to master)
        @param commit_sha1: default is latest
        @return: The new commit sha1
        """

        # Importing here to avoid circular dependencies (experiment <-> project)
        from cnvrgv2 import Project
        project = Project(context=self._context, slug=self.scope["project"])
        if project.git:
            return None
        if not commit_sha1:
            commit_sha1 = self.last_commit
        merge_to_master_route = routes.PROJECT_COMMIT_BASE.format(self.scope["organization"], self.scope["project"])
        response = self._proxy.call_api(
            route=urljoin(merge_to_master_route, commit_sha1, "merge_to_master"),
            http_method=HTTP.POST,
            payload={'sha1': commit_sha1}
        )
        return response.attributes['sha1']

    def start_tensorboard(self):
        """
        Starts a tensorboard server in the current experiment
        """
        url = urljoin(self._route, routes.WORKflOW_START_TENSORBOARD_SUFFIX)

        self._proxy.call_api(
            route=url,
            http_method=HTTP.POST,
            payload=JAF.serialize(type=self._type, attributes={})
        )

    def stop_tensorboard(self):
        """
        Stop the tensorboard session in the current experiment
        """
        url = urljoin(self._route, routes.WORKflOW_STOP_TENSORBOARD_SUFFIX)

        self._proxy.call_api(
            route=url,
            http_method=HTTP.POST,
            payload=JAF.serialize(type=self._type, attributes={})
        )

    def list_artifacts(self, commit_sha1=None):
        """
        List artifacts of an experiment
        @return: List of artifacts for the experiment
        """
        artifacts_url = urljoin(self._route, routes.WORKFLOW_ARTIFACTS_SUFFIX)
        list_object = File
        response = api_list_generator(
            context=self._context,
            route=artifacts_url,
            object=list_object,
            identifier="fullpath",
            pagination_type="cursor",
            data={
                "sha1": commit_sha1 or self.last_commit
            }
        )

        return response

    def delete(self, delete_artifacts=False):
        """
        Deletes the current experiment
        @param delete_artifacts: Delete workflow artifacts
        @return: None
        """

        payload = {
            "permanent": delete_artifacts
        }

        self._proxy.call_api(
            route=self._route,
            http_method=HTTP.DELETE,
            payload=payload
        )

    def info(self, end_pos=0):
        """
        Get info about the current experiment
        @param end_pos: end position of the logs
        @return: Info JAF object
        """

        return self._proxy.call_api(
            route=urljoin(self._route, routes.EXPERIMENT_INFO_SUFFIX),
            http_method=HTTP.GET,
            payload={
                "pos": end_pos,
                "exit_status": True
            })
