# Copyright 2024 Openstack Foundation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The view dashboard module handles creating Jenkins Dashboard views.

To create a dashboard view specify ``dashboard`` in the ``view-type``
attribute to the :ref:`view_dashboard` definition.
Requires the Jenkins :jenkins-plugins:`Dashboard View <dashboard-view>`.

:View Parameters:
    * **name** (`str`): The name of the view.
    * **view-type** (`str`): The type of view (``dashboard``).
    * **description** (`str`): A description of the view. (default '')
    * **filter-executors** (`bool`): Show only executors that can
      execute the included views. (default false)
    * **filter-queue** (`bool`): Show only included jobs in the build
      queue. (default false)
    * **job-name** (`list`): List of jobs to be included in the view.
    * **job-filters** (`dict`): Job filters to be included. Requires
      :jenkins-plugins:`View Job Filters <view-job-filters>`.
      See :ref:`view_list` for supported filter types.
    * **columns** (`list`): List of columns to show. (default: status,
      weather, job, last-success, last-failure, last-duration,
      build-button)
    * **regex** (`str`): Regular expression for selecting jobs. (optional)
    * **recurse** (`bool`): Recurse into subfolders. (default false)
    * **status-filter** (`bool`): Filter job list by enabled/disabled
      status. (optional)
    * **include-std-job-list** (`bool`): Show the standard Jenkins job
      list at the top of the dashboard. (default false)
    * **hide-jenkins-panels** (`bool`): Hide the standard Jenkins
      top/side panels for a full-screen dashboard view. (default false)
    * **use-css-style** (`bool`): Use the dashboard CSS styling.
      (default false)
    * **left-portlet-width** (`str`): CSS width of the left portlet
      column. (default '50%')
    * **right-portlet-width** (`str`): CSS width of the right portlet
      column. (default '50%')
    * **top-portlets** (`list`): Portlets to display across the top.
    * **left-portlets** (`list`): Portlets to display in the left column.
    * **right-portlets** (`list`): Portlets to display in the right column.
    * **bottom-portlets** (`list`): Portlets to display across the bottom.

:Portlet types and their parameters:

    * **hudson-std-jobs** - Standard Jenkins jobs list portlet.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.

    * **jobs-grid** - Jobs grid portlet showing jobs in a grid layout.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.
            * **column-count** (`int`): Number of columns. (default 3)
            * **fill-column-first** (`bool`): Fill columns before rows.
              (default false)

    * **unstable-jobs** - Lists unstable (and optionally failed) jobs.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.
            * **show-only-failed-jobs** (`bool`): Show only failed jobs
              instead of all unstable jobs. (default false)
            * **recurse** (`bool`): Recurse into subfolders. (default false)

    * **iframe** - Embeds an external page via an iframe.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.
            * **iframe-source** (`str`): URL of the page to embed.
              (default '')
            * **div-style** (`str`): Inline CSS style applied to the
              container div (e.g. ``width:100%;height:500px;``).
              (default '')

    * **image** - Displays an image from a URL.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.
            * **image-url** (`str`): URL of the image to display.
              (default '')

    * **latest-builds** - Shows the most recent builds across all jobs
      in the view.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.
            * **num-builds** (`int`): Number of builds to show.
              (default 10)

    * **test-statistics-chart** - Pie chart of passing/failing/skipped
      test results.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.

    * **test-statistics-grid** - Grid showing per-job test statistics.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.
            * **hide-zero-test-projects** (`bool`): Hide jobs with no
              tests. (default false)
            * **success-color** (`str`): Hex color for passing tests,
              without ``#``. (default '71E66D')
            * **failure-color** (`str`): Hex color for failing tests,
              without ``#``. (default 'E86850')
            * **skipped-color** (`str`): Hex color for skipped tests,
              without ``#``. (default 'FDB813')
            * **use-background-colors** (`bool`): Use background colors
              in the grid cells. (default false)
            * **use-alternate-percentages-on-limits** (`bool`): Use
              alternate percentage display at limits. (default false)

    * **test-trend-chart** - Line chart of aggregated test results over
      time.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.
            * **graph-width** (`int`): Chart width in pixels. (default 300)
            * **graph-height** (`int`): Chart height in pixels.
              (default 220)
            * **date-range** (`int`): Number of days of history to show.
              (default 365)
            * **date-shift** (`int`): Shift start of date range by this
              many days. (default 0)
            * **display-status** (`str`): Which test results to include.
              (default 'ALL')

    * **stat-jobs** - Shows statistics based on job health scores.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.

    * **stat-builds** - Shows statistics based on build status.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.

    * **stat-slaves** - Shows agent/node statistics.

        :portlet-params:
            * **name** (`str`): Display name for the portlet.

Minimal Example:

    .. literalinclude::
        /../../tests/views/fixtures/view_dashboard-minimal.yaml

Full Example:

    .. literalinclude::
        /../../tests/views/fixtures/view_dashboard-full.yaml
"""

import xml.etree.ElementTree as XML

import jenkins_jobs.modules.base
import jenkins_jobs.modules.helpers as helpers
import jenkins_jobs.modules.view_jobfilters as view_jobfilters
from jenkins_jobs.modules.view_list import COLUMN_DICT, DEFAULT_COLUMNS


# Maps JJB portlet type keys to Jenkins class names
PORTLET_CLASS_DICT = {
    "hudson-std-jobs": "hudson.plugins.view.dashboard.core.HudsonStdJobsPortlet",
    "jobs-grid": "hudson.plugins.view.dashboard.core.JobsPortlet",
    "unstable-jobs": "hudson.plugins.view.dashboard.core.UnstableJobsPortlet",
    "iframe": "hudson.plugins.view.dashboard.core.IframePortlet",
    "image": "hudson.plugins.view.dashboard.core.ImagePortlet",
    "latest-builds": "hudson.plugins.view.dashboard.builds.LatestBuilds",
    "test-statistics-chart": "hudson.plugins.view.dashboard.test.TestStatisticsChart",
    "test-statistics-grid": "hudson.plugins.view.dashboard.test.TestStatisticsPortlet",
    "test-trend-chart": "hudson.plugins.view.dashboard.test.TestTrendChart",
    "stat-jobs": "hudson.plugins.view.dashboard.stats.StatJobs",
    "stat-builds": "hudson.plugins.view.dashboard.stats.StatBuilds",
    "stat-slaves": "hudson.plugins.view.dashboard.stats.StatSlaves",
}


def _portlet_xml(parent, portlet_data):
    """Append a single portlet XML element to *parent*.

    :arg xml.etree.ElementTree.Element parent: the portlet-list element
        (e.g. ``<leftPortlets>``) to attach the new portlet to.
    :arg dict portlet_data: the portlet configuration dict from YAML.
    """
    ptype = portlet_data.get("type")
    if ptype not in PORTLET_CLASS_DICT:
        raise ValueError(
            "Unknown dashboard portlet type '%s'. Supported types: %s"
            % (ptype, ", ".join(sorted(PORTLET_CLASS_DICT)))
        )

    class_name = PORTLET_CLASS_DICT[ptype]
    portlet = XML.SubElement(parent, class_name)

    # All portlets share a <name> element
    XML.SubElement(portlet, "name").text = portlet_data.get("name", "")

    if ptype == "jobs-grid":
        mapping = [
            ("column-count", "columnCount", 3),
            ("fill-column-first", "fillColumnFirst", False),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )

    elif ptype == "unstable-jobs":
        mapping = [
            ("show-only-failed-jobs", "showOnlyFailedJobs", False),
            ("recurse", "recurse", False),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )

    elif ptype == "iframe":
        iframe_source = portlet_data.get("iframe-source", "")
        mapping = [
            ("iframe-source", "iframeSource", ""),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )
        XML.SubElement(portlet, "effectiveUrl").text = iframe_source
        mapping = [
            ("div-style", "divStyle", ""),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )

    elif ptype == "image":
        mapping = [
            ("image-url", "url", ""),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )

    elif ptype == "latest-builds":
        mapping = [
            ("num-builds", "numBuilds", 10),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )

    elif ptype == "test-statistics-grid":
        mapping = [
            ("use-background-colors", "useBackgroundColors", False),
            ("skipped-color", "skippedColor", "FDB813"),
            ("success-color", "successColor", "71E66D"),
            ("failure-color", "failureColor", "E86850"),
            ("hide-zero-test-projects", "hideZeroTestProjects", False),
            (
                "use-alternate-percentages-on-limits",
                "useAlternatePercentagesOnLimits",
                False,
            ),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )

    elif ptype == "test-trend-chart":
        mapping = [
            ("graph-width", "graphWidth", 300),
            ("graph-height", "graphHeight", 220),
            ("date-range", "dateRange", 365),
            ("date-shift", "dateShift", 0),
            ("display-status", "displayStatus", "ALL"),
        ]
        helpers.convert_mapping_to_xml(
            portlet, portlet_data, mapping, fail_required=False
        )

    # hudson-std-jobs, test-statistics-chart, stat-jobs, stat-builds,
    # stat-slaves have no fields beyond <name>

    return portlet


class Dashboard(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        root = XML.Element(
            "hudson.plugins.view.dashboard.Dashboard",
            {"plugin": "dashboard-view"},
        )

        # Standard view fields inherited from ListView
        mapping = [
            ("name", "name", None),
            ("description", "description", ""),
            ("filter-executors", "filterExecutors", False),
            ("filter-queue", "filterQueue", False),
        ]
        helpers.convert_mapping_to_xml(root, data, mapping, fail_required=True)

        XML.SubElement(root, "properties", {"class": "hudson.model.View$PropertyList"})

        jn_xml = XML.SubElement(root, "jobNames")
        XML.SubElement(
            jn_xml, "comparator", {"class": "hudson.util.CaseInsensitiveComparator"}
        )
        jobnames = data.get("job-name", None)
        if jobnames is not None:
            for jobname in sorted(jobnames, key=str.lower):
                XML.SubElement(jn_xml, "string").text = str(jobname)

        job_filter_xml = XML.SubElement(root, "jobFilters")
        jobfilters = data.get("job-filters", [])
        for jobfilter in jobfilters:
            f = getattr(view_jobfilters, jobfilter.replace("-", "_"))
            f(job_filter_xml, jobfilters.get(jobfilter))

        c_xml = XML.SubElement(root, "columns")
        columns = data.get("columns", DEFAULT_COLUMNS)
        for column in columns:
            if isinstance(column, dict):
                if "extra-build-parameter" in column:
                    p_name = column["extra-build-parameter"]
                    x = XML.SubElement(
                        c_xml,
                        "jenkins.plugins.extracolumns.BuildParametersColumn",
                        plugin="extra-columns",
                    )
                    x.append(XML.fromstring("<singlePara>true</singlePara>"))
                    x.append(
                        XML.fromstring("<parameterName>%s</parameterName>" % p_name)
                    )
            else:
                if column in COLUMN_DICT:
                    if isinstance(COLUMN_DICT[column], list):
                        x = XML.SubElement(
                            c_xml,
                            COLUMN_DICT[column][0][0],
                            **COLUMN_DICT[column][0][1],
                        )
                        for tag in COLUMN_DICT[column][1:]:
                            x.append(XML.fromstring(tag))
                    else:
                        XML.SubElement(c_xml, COLUMN_DICT[column])

        mapping = [
            ("regex", "includeRegex", None),
            ("recurse", "recurse", False),
            ("status-filter", "statusFilter", None),
        ]
        helpers.convert_mapping_to_xml(root, data, mapping, fail_required=False)

        # Dashboard specific view fields
        mapping = [
            ("use-css-style", "useCssStyle", False),
            ("include-std-job-list", "includeStdJobList", False),
            ("hide-jenkins-panels", "hideJenkinsPanels", False),
            ("left-portlet-width", "leftPortletWidth", "50%"),
            ("right-portlet-width", "rightPortletWidth", "50%"),
        ]
        helpers.convert_mapping_to_xml(root, data, mapping, fail_required=False)

        for yaml_key, xml_tag in (
            ("left-portlets", "leftPortlets"),
            ("right-portlets", "rightPortlets"),
            ("top-portlets", "topPortlets"),
            ("bottom-portlets", "bottomPortlets"),
        ):
            portlets_xml = XML.SubElement(root, xml_tag)
            for portlet in data.get(yaml_key, []):
                _portlet_xml(portlets_xml, portlet)

        return root
