# Copyright 2025 Kienan Stewart <kstewart@efficios.com>
#
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
The view category module handles creating Jenkins Categorized views.
To create a categorized view specify ``categorized`` in the ``view-type`` attribute
to the :ref:`view_categorized` definition.

Requires the Jenkins :jenkins-plugins:`Categorized Views<categorized-view>`.

Inherits paraemeters from the :ref:`view_list` definition.

:View Parameters:
    * **name** (`str`): The name of the view
    * **view-type** (`str`): Set to `categorized`
    * **regex_to_ignore_on_color_computing** (`str`): The regex of jobs to ignore when computing color and status
    * **categorization_criteria** (`list`): A list dictionaries for the different categorization criteria

The entries in categorization criteria default to `grouping_rule`.

:GroupingRule Parameters:
    * **type** (`str`): The type ("grouping_rule")
    * **group_regex** (`str`): The regex for grouping items
    * **naming_rule** (`str`): The naming rule
    * **use_display_name** (`bool`): If the display name should be used for the group

Example:

    .. literalinclude::
        /../../tests/views/fixtures/view_categorized-minimal.yaml

Example:

    .. literalinclude::
        /../../tests/views/fixtures/view_categorized-full.yaml
"""

import xml.etree.ElementTree as XML

from jenkins_jobs.errors import InvalidAttributeError
import jenkins_jobs.modules.view_list as view_list
import jenkins_jobs.modules.helpers as helpers


class Categorized(view_list.List):

    criterium_types = ["grouping_rule"]

    def root_xml(self, data):
        root = super().root_xml(data)
        root.tag = "org.jenkinsci.plugins.categorizedview.CategorizedJobsView"
        root.set("plugin", "categorized-view")

        XML.SubElement(root, "regexToIgnoreOnColorComputing").text = data.get(
            "regex_to_ignore_on_color_computing", ""
        )

        criteria = XML.SubElement(root, "categorizationCriteria")
        for criterium in data.get("categorization_criteria", []):
            if not criterium.get("type", None):
                criterium["type"] = "grouping_rule"
            self.add_criterium(criterium, criteria)
        return root

    def add_criterium(self, criterium, criteria):
        if criterium["type"] == "grouping_rule":
            mapping = [
                ("group_regex", "groupRegex", ""),
                ("naming_rule", "namingRule", ""),
                ("use_display_name", "useDisplayName", False),
            ]
            helpers.convert_mapping_to_xml(
                XML.SubElement(
                    criteria, "org.jenkinsci.plugins.categorizedview.GroupingRule"
                ),
                criterium,
                mapping,
                fail_required=True,
            )
        else:
            raise InvalidAttributeError(
                "type", criterium["type"], Categorized.criterium_types
            )
