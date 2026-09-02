#!/usr/bin/env python3
import copy
import logging
import os
import re

from jinja2 import Environment
from jinja2 import FileSystemLoader

logger = logging.getLogger(__name__)


class MetricsCollection:
    """Prometheus like metrics collection

    This class handles a collection of metrics not necessarily of the same metric name.
    """

    class Metric:
        """Collection of metrics of the same name

        Set of metrics of the same name with multiple instances, differenciated by the set labels
        """

        validMetricTypes = ["counter", "gauge", "histogram", "summary", None]

        class MetricInstance:
            """single metric

            This is a single representation of one metric.
            """

            labelRegEx = "[a-zA-Z_][a-zA-Z0-9_]*"

            def __init__(self, name, value, labels={}):
                """initialize the metric instance

                Args:
                    value (mixed): actual value of the metric instance
                    labels (dict): set of labels for the metric instance (default: `{}`)
                """
                self.setName(name)
                self.setValue(value)
                for k in labels:
                    if not re.match(re.compile(f"^{self.labelRegEx}$"), k):
                        logger.error(
                            f"Label with name “{k}” does not match the Prometheus specifications. Please adjust!"
                        )
                self.labels = labels

            def __eq__(self, other):
                """check equality even down to the metrics value

                Args:
                    other (MetricInstance): metric instance to compare with
                """
                return self.same(other) and self.value == other.value

            def setName(self, name):
                """set / change name

                Args:
                    name (str): name to be set
                """
                self.name = name

            def setValue(self, value):
                """set / change value

                Args:
                    value (mixed / number): value to be set for Metric
                """
                self.value = value

            def same(self, other):
                """check if metric instance equals other metric instance

                ATTENTION: this method does not (!) compare the actual value of the instance.
                It only checks in the manner of Prometheus metrics if the instances have the same
                set of labels and if so, they are assumed to be equal, so the new metric can replace
                the old one.

                Args:
                    other (MetricInstance): metric instance to compare with

                Returns:
                    bool: `True` if label set is same, `False` if not or other typed object given.
                """
                if type(self) == type(other):
                    return (self.labels == other.labels) and (self.name == other.name)
                else:
                    return False

        nameRegEx = "[a-zA-Z_:][a-zA-Z0-9_:]*"

        def __init__(self, name, helpText=None, metricType=None):
            """initialize Metric by name

            Args:
                name (str): name of metric to be used
                helpText (str): short description about the metric identified by name
                metricType (str): type of metric to be used (default: `gauge`)
            """
            self.instances = []
            self.comments = []
            self.setType(metricType)
            self.setName(name)
            self.setHelp(helpText)

        def __getitem__(self, index):
            """iterate through instances

            Args:
                index (int): get instance by index

            Returns:
                MetricInstance: instance at index
            """
            return self.instances[index]

        def __len__(self):
            """count metric instances

            Returns:
                int: count of instances in this Metric
            """
            return len(self.instances)

        def setName(self, name):
            """change name

            Args:
                name (str): name to change the metrics to
            """
            name = name.strip()
            if not re.match(re.compile(f"^{self.nameRegEx}$"), name):
                logger.error(
                    f"“{name}” does not match the Prometheus specifications. Please adjust!"
                )
            if self.type == "counter" and not name.endswith("_total"):
                logger.warning(
                    f"For a “counter” type metric, the name should have “_total” suffix, but “{name}” does not."
                )
            if self.type not in ("histogram", "summary") and name.endswith("_count"):
                logger.warning(
                    f"Non-histogram and non-summary metrics like “{name}” should not end with “_count” suffix."
                )
            self.name = name
            for i in self.instances:
                i.setName(name)

        def setHelp(self, helpText):
            """change help information about metric

            Args:
                helpText (str): help information about the metrics
            """
            if type(helpText) == str:
                helpText = helpText.strip()
            self.helpText = helpText

        def setType(self, metricType):
            """change metric type

            Args:
                metricType (str): type to change metric to
            """
            if type(metricType) == str:
                metricType = metricType.strip()
            if metricType not in self.validMetricTypes:
                logger.error(
                    f"“{metricType}” is not a valid type, which are defined by {self.validMetricTypes}"
                )
            self.type = metricType

        def addComment(self, comment):
            """add additional comments to metrics

            Args:
                comment (str): comment to add
            """
            if comment not in self.comments:
                self.comments.append(comment)

        def getComments(self):
            """return comments

            Returns:
                list: list of comments
            """
            return self.comments

        def popComment(self, commentIndex):
            """pop a comment by ID in list

            Args:
                commentIndex (int): index to pop

            Returns:
                str: popped comment
            """
            return self.comments.pop(commentIndex)

        def addMetric(self, value, labels={}):
            """add a metric instance

            Only a single metric with the same label set can be contained, so
            those “duplicates” will overwrite existing ones.

            Args:
                value (mixed): value of metric instance
                labels (mixed): labels that will identify instance
            """
            m = self.MetricInstance(self.name, value, labels)
            valueChanged = False
            for i, e in enumerate(self.instances):
                if e.same(m):
                    logger.debug(
                        f"Update value of a `{self.name}` metric from `{e.value}` to `{value}`."
                    )
                    e.setValue(value)
                    valueChanged = True
                    break
            if not valueChanged:
                self.instances.append(m)

        def representation(self):
            """get directory representation for further work with metrics

            Returns:
                dict: representation of metrics
            """
            return {
                self.name: {
                    "type": self.type or "",
                    "help": self.helpText or "",
                    "instances": self.instances,
                    "comments": self.comments,
                }
            }

    def __init__(self):
        """create set of metrics"""
        self.metrics = {}

    def ensureMetric(self, metricName, helpText=None, metricType=None):
        """ensure metric existing also if no instances are present

        Args:
            metricName (str): name of metric to be added (see https://prometheus.io/docs/concepts/data_model/ for data model)
            helpText (str): help information for the metric collection of name metricName (default: `None`)
            metricType (str): type of metric to be used – see https://prometheus.io/docs/concepts/metric_types/
                              (default: None, will default to `gauge` on creation)
        """
        if metricName not in self.metrics:
            self.metrics[metricName] = self.Metric(
                name=metricName, helpText=helpText, metricType=metricType
            )
            logger.debug(f"Created metric “{metricName}” with no instances for now.")
        else:
            logger.debug(f"Metric “{metricName}” already exists.")

    def addMetric(
        self, metricName, value=None, labels={}, helpText=None, metricType=None
    ):
        """add a (new) metric instance

        Args:
            metricName (str): name of metric to be added (see https://prometheus.io/docs/concepts/data_model/ for data model)
            value (mixed): value of actual metric set (default: `None`)
            labels (dict): labels to be set for actual metric set – they identify a metric! (default: `{}`)
            helpText (str): help information for the metric collection of name metricName (default: `None`)
            metricType (str): type of metric to be used – see https://prometheus.io/docs/concepts/metric_types/
                              (default: None, will default to `gauge` on creation)
        """
        if not metricName in self.metrics:
            if metricType == None:
                logger.info(f"No TYPE defined for new created metric “{metricName}”.")
            if helpText == None:
                logger.info(
                    f"No HELP information passed for new metric “{metricName}”."
                )
            self.metrics[metricName] = self.Metric(
                name=metricName, helpText=helpText, metricType=metricType
            )
            logger.debug(f"Added new metric “{metricName}”")
        else:
            if helpText != None:
                self.setHelp(metricName, helpText)
                logger.info(f"Changed help for metric `{metricName}`.")
            if metricType != None:
                self.setType(metricName, metricType)
                logger.warning(f"Changed type for metric `{metricName}`.")
        if value != None:
            self.metrics[metricName].addMetric(value, labels)
        else:
            logger.debug(
                f"Not adding metric instance for “{metricName}” due to missing value!"
            )

    def addComment(self, metricName, comment):
        """add a comment

        Args:
            metricName (string): [description]
            comment (string): comment to add
        """
        self.metrics[metricName].addComment(comment)

    def renameMetrics(self, oldName, newName, force=False):
        """rename metrics

        Args:
            oldName (str): old name to be renamed
            newName (str): new name to be used
            force (bool): [description] (default: `False`)

        Returns:
            bool: was the rename successful?
        """
        if newName in self.metrics:
            log = f"Metric “{newName}” already exists."
            if force:
                logger.info(f"{log} Doing a merge.")
                oldType = self.metrics[oldName].type
                oldHelp = self.metrics[oldName].helpText
                self.mergeMetrics(newName, oldName)
                if self.metrics[newName].type != oldType:
                    logger.info(
                        f"Changing metric type for “{newName}” back to “{oldType}”"
                    )
                    self.metrics[newName].setType(oldType)
                if self.metrics[newName].helpText != oldHelp:
                    logger.info(
                        f"Changing metric help for “{newName}” back to “{oldHelp}”"
                    )
                    self.metrics[newName].setHelp(oldHelp)
                return True

            logger.error(f"{log} No force so no change here.")
            return False

        logger.debug(f"Renaming “{oldName}” to “{newName}”.")
        self.metrics[oldName].setName(newName)
        self.metrics[newName] = self.metrics[oldName]
        self.metrics.pop(oldName)
        return True

    def mergeMetrics(self, mainName, mergeName):
        """merge metrics

        `TYPE`, `HELP` and metric name of `mainName` metrics stay valid and
        `mergeName` metrics will be integrated into `mainName`.
        Integration will override / update metrics with the same labels by mergeName ones!

        Args:
            mainName (str): metrics name to merge `mergeName` into
            mergeName (str): metrics name to get metrics to merge into `mainName`
        """
        if mainName not in self.metrics:
            logger.warning(
                f"“{mainName}” metrics do not exist – will rename “{mergeName}” to that name."
            )
            self.renameMetrics(mergeName, mainName)
        else:
            logger.debug(f"Merging “{mergeName}” metrics into “{mainName}”.")
            oldHelp = self.metrics[mergeName].helpText
            if oldHelp != None:
                logger.info(f"Help “{oldHelp}” for merged metrics will be abandonned.")
            oldType = self.metrics[mergeName].type
            newType = self.metrics[mainName].type
            if oldType != newType:
                logger.warning(
                    f"Type “{oldType}” differs from type “{newType}” where last one is type of destination metric."
                )
            merge = self.metrics.pop(mergeName)
            for i in merge.instances:
                self.addMetric(mainName, i.value, i.labels)

    def setHelp(self, metricName, helpText):
        """change help for metric

        Args:
            metricName (str): name of metric to set the help information
            helpText (str): help information about what the metric is to say
        """
        self.ensureMetric(metricName)
        self.metrics[metricName].setHelp(helpText)

    def setType(self, metricName, metricType=None):
        """change metric type

        Args:
            metricName (str): name of metric to set type for
            metricType (str): type to be set for metric (default: `"gauge"`)
        """
        self.ensureMetric(metricName)
        self.metrics[metricName].setType(metricType)

    def prepare(self):
        """Helper function to transform list of metric objects of class above into usable object

        Returns:
            dict: dictionary to be pushed into template of this module to be rendered
        """
        finalized = {}
        for m in self.metrics.values():
            finalized.update(m.representation())
        return finalized

    def load(self, metricsString, dismissComments=True):
        """load (additional) metrics

        Load data from given metrics string to merge with current collection or to manipulate, ...
        By default, comments will be dismissed – otherwise they will probably be relocated to the nearest metrics since this
        module only supports comments connected to metrics not floating around in the final metrics string.

        Args:
            metricsString (str): metrics string to load
            dismissComments (bool): set `True` if comments (other than `# HELP` and `# TYPE`, which are mandatory) should be dismissed
        """
        # will work with comment assigning to metrics by distance in file, so first remove all blank lines
        self._worklist = [l.strip() for l in metricsString.splitlines()]
        # working variable for initialisation of metrics
        self._createMetrics = {}
        # working variable to store lines where which metric names were found
        self._metricLines = {}
        # working variable to store line indices which already were processed
        self._lineRange = list(range(len(self._worklist)))
        self._processedLines = [i for i in self._lineRange if self._worklist[i] == ""]
        # find types
        self._findTypes()
        # find help notes
        self._findHelps()
        # create the metric collections
        for metricName in self._createMetrics:
            mt = None
            mh = None
            if "type" in self._createMetrics[metricName].keys():
                mt = self._createMetrics[metricName]["type"]
            if "help" in self._createMetrics[metricName].keys():
                mh = self._createMetrics[metricName]["help"]
            self.addMetric(
                metricName=metricName,
                helpText=mh,
                metricType=mt,
            )
        # find actual metric instances
        self._findMetricInstances()
        # find comments
        self._findComments(dismissComments=dismissComments)

        # add metric instances
        # check if any string is left over and warn about it
        self._checkForLeftovers()
        # clean create metrics variables
        del self._createMetrics
        del self._metricLines
        del self._processedLines
        del self._lineRange
        del self._worklist
        # print(self)

    def _findTypes(self):
        """find types in metrics string

        helper method for `load` function which collects metric names and types in `self._worklist`
        """
        try:
            self._worklist
        except AttributeError:
            logger.error("Method “_findTypes” is not meant to be called manually.")
            return

        regex = r"^#\s*TYPE\s+([^\s]+)\s+([^\s]+)\s*$"
        for lineIndex in [i for i in self._lineRange if i not in self._processedLines]:
            line = self._worklist[lineIndex]
            typeRow = re.fullmatch(regex, line)
            if typeRow != None:
                self._processedLines.append(lineIndex)
                groups = typeRow.groups()
                # note down line as metric relevant line
                if groups[0] not in self._metricLines:
                    self._metricLines[groups[0]] = []
                self._metricLines[groups[0]].append(lineIndex)
                # store type of metric
                if groups[0] not in self._createMetrics:
                    self._createMetrics[groups[0]] = {}
                if "type" in self._createMetrics[groups[0]]:
                    logger.error(
                        f"Type for metric with name {groups[0]} defined multiple times.\n"
                        f"Only first occurence (“{self._createMetrics[groups[0]]['type']}”) in given metric definition will be applied."
                    )
                else:
                    self._createMetrics[groups[0]]["type"] = groups[1]

    def _findHelps(self):
        """find help notices in metrics string

        helper method for `load` function which collects help notices in `self._worklist` and adds them to corresponding names and types
        """
        try:
            self._worklist
        except AttributeError:
            logger.error("Method “_findHelps” is not meant to be called manually.")
            return

        regex = r"^#\s*HELP\s+([^\s]+)\s+(.*)$"
        for lineIndex in [i for i in self._lineRange if i not in self._processedLines]:
            line = self._worklist[lineIndex]
            helpRow = re.fullmatch(regex, line)
            if helpRow != None:
                self._processedLines.append(lineIndex)
                groups = helpRow.groups()
                # note down line as metric relevant line
                if groups[0] not in self._metricLines:
                    self._metricLines[groups[0]] = []
                self._metricLines[groups[0]].append(lineIndex)
                # store help of metric
                if groups[0] not in self._createMetrics:
                    self._createMetrics[groups[0]] = {}
                if "help" in self._createMetrics[groups[0]]:
                    logger.error(
                        f"Help for metric with name {groups[0]} defined multiple times.\n"
                        f"Only first occurence (“{self._createMetrics[groups[0]]['help']}”) in given metric definition will be applied."
                    )
                else:
                    self._createMetrics[groups[0]]["help"] = (
                        MetricsCollection.decodeOneliner(groups[1])
                    )

    def _findComments(self, dismissComments=True):
        """find comments and sort them to nearest metrics names

        Args:
            dismissComments (bool): should comments just be dropped? Yes => `True`, No => `False`
        """
        try:
            self._worklist
        except AttributeError:
            logger.error("Method “_findComments” is not meant to be called manually.")
            return

        commentLineIndex = [
            i
            for i in self._lineRange
            if i not in self._processedLines and self._worklist[i].startswith("#")
        ]
        self._processedLines += commentLineIndex

        if not dismissComments:
            start = {}
            end = {}
            for metricName in self._metricLines.keys():
                start[metricName] = min(self._metricLines[metricName])
                end[metricName] = max(self._metricLines[metricName])

            for cl in commentLineIndex:
                sd = {}
                ed = {}
                for metricName in self._metricLines.keys():
                    sd[metricName] = abs(start[metricName] - cl)
                    ed[metricName] = abs(end[metricName] - cl)
                ls = min(sd.values())
                le = min(ed.values())
                if ls <= le:
                    name = [k for k, v in sd.items() if v == ls][0]
                else:
                    name = [k for k, v in ed.items() if v == le][0]

                self.addComment(name, self._worklist[cl].lstrip("#").strip())

    def _findMetricInstances(self):
        """find actual metric instances"""
        try:
            self._worklist
        except AttributeError:
            logger.error(
                "Method “_findMetricInstances” is not meant to be called manually."
            )
            return

        lineRegex = (
            r"^("
            + self.Metric.nameRegEx
            + r")\s*(\{(.*)\})?\s+(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)$"
        )
        commaSplitRegex = r""",(?=(?:[^"']*["'][^"']*["'])*[^"']*$)"""
        unquoteRegex = r"""((^"(.*)"$)|(^'(.*)'$))"""
        for lineIndex in [i for i in self._lineRange if i not in self._processedLines]:
            line = self._worklist[lineIndex]
            metricLine = re.fullmatch(lineRegex, line)
            if metricLine != None:
                self._processedLines.append(lineIndex)
                groups = metricLine.groups()
                # note down line as metric relevant line
                if groups[0] not in self._metricLines:
                    self._metricLines[groups[0]] = []
                self._metricLines[groups[0]].append(lineIndex)

                # retrieve labels
                labels = {}
                if groups[2] != None:
                    labelHelp = re.split(commaSplitRegex, groups[2])
                    for l in labelHelp:
                        l = l.split("=", 1)
                        labels[l[0]] = re.sub(unquoteRegex, r"\3\5", l[1])

                # add actual metric
                if groups[0] not in self._createMetrics:
                    self._createMetrics[groups[0]] = {}
                    logger.info(
                        f"It seems there is a metric “{groups[0]}” without any TYPE or HELP defined in imported metrics."
                    )

                self.addMetric(groups[0], value=groups[3], labels=labels)

    def _checkForLeftovers(self):
        """check if the Metric string holds unknown, unallowed additional lines of code and warn about occurences"""
        try:
            self._worklist
        except AttributeError:
            logger.error(
                "Method “_checkForLeftovers” is not meant to be called manually."
            )
            return

    def decodeOneliner(singleLine):
        """decode single line

        Args:
            singleLine (string): one single line – in Prometheus metrics, `\\` has
                                 to be encoded as `\\\\` and newlines as `\\n`.

        Returns:
            string: decoded text, possibly multiline
        """
        if "\n" in singleLine:
            logger.error("Single line has to be given to be able to decode anything!")
        else:
            singleLine = singleLine.replace("\\n", "\n").replace("\\\\", "\\")
        return singleLine

    def __str__(self):
        """string representation

        The string representation of a metrics collection is meant to be fetched by
        Prometheus or to be pushed to a Prometheus Push Gateway.

        Returns:
            str: prometheus metrics data
        """
        file_loader = FileSystemLoader(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "tpl")
        )
        env = Environment(loader=file_loader)
        template = env.get_template("metrics.j2")

        output = template.render(metrics=self.prepare()).strip() + "\n"
        return output
