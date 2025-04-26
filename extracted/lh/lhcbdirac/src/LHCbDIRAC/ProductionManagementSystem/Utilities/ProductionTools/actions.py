###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from abc import ABCMeta, abstractmethod

from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequestClient import ProductionRequestClient


class Action(metaclass=ABCMeta):
    # Should this action be ran without prompting the user?
    safe = False

    @abstractmethod
    def message(self): ...

    @abstractmethod
    def run(self): ...


class UpdateRequestStateAction(Action):
    def __init__(self, request_id, state):
        self.request_id = request_id
        self.state = state

    def message(self):
        return f"{self.__class__.__name__}({self.request_id}, {self.state})"

    def run(self):
        returnValueOrRaise(
            ProductionRequestClient().updateProductionRequest(int(self.request_id), {"RequestState": self.state})
        )
        print(f"Request {self.request_id} set to {self.state}")


class ExtendEndRunAction(Action):
    def __init__(self, issue, transform_id, end_run):
        self.issue = issue
        self.transform_id = transform_id
        self.new_end_run = end_run

    def message(self):
        return f"{self.__class__.__name__}({self.transform_id}, {self.new_end_run})"

    def run(self):
        returnValueOrRaise(TransformationClient().setBookkeepingQueryEndRun(self.transform_id, self.new_end_run))


class UpdateIssueStateLabel(Action):
    def __init__(self, issue, old_state, new_state):
        self.issue = issue
        self.old_state = old_state
        self.new_state = new_state

    def message(self):
        return f"{self.__class__.__name__}({self.issue}, {self.new_state})"

    def run(self):
        self.issue.labels.pop(self.issue.labels.index(f"state::{self.old_state}"))
        self.issue.labels.append(f"state::{self.new_state}")
        self.issue.issue.save()
        print(f"Issue {self.issue} set to {self.new_state}")


class SubmitProductionsAction(Action):
    def __init__(self, issue):
        self.issue = issue

    def message(self):
        return f"{self.__class__.__name__}({self.issue}, validation={'state::ready' not in self.issue.labels})"

    def run(self):
        from .launching import start_productions
        from .integrations import OperationsLogbook

        logbook = OperationsLogbook()
        start_productions(logbook, self.issue)


class SubmitRemovalTransformationAction(Action):
    def __init__(self, issue, request_id: int):
        self.issue = issue
        self.request_id = request_id

    def message(self):
        return f"{self.__class__.__name__}({self.issue})"

    def run(self):
        from .launching import start_removal_transformation
        from .integrations import OperationsLogbook

        logbook = OperationsLogbook()
        start_removal_transformation(logbook, self.issue, self.request_id)


class CheckValidationAction(Action):
    def __init__(self, issue, request_id):
        self.issue = issue
        self.request_id = request_id

    def message(self):
        return f"{self.__class__.__name__}({self.issue}, {self.request_id})"

    def run(self):
        from .launching import check_validation

        check_validation(self.issue, self.request_id)


class UpdateTransformationStatusAction(Action):
    def __init__(self, transform_id, status):
        self.transform_id = transform_id
        self.status = status

    def message(self):
        return f"{self.__class__.__name__}({self.transform_id}, {self.status})"

    def run(self):
        tc = TransformationClient()
        returnValueOrRaise(tc.setTransformationParameter(self.transform_id, "Status", self.status))
        print(f"Transformation {self.transform_id} set to {self.status}")


class CleanValidationAction(Action):
    def __init__(self, issue, request_id):
        self.issue = issue
        self.request_id = request_id

    def message(self):
        return f"{self.__class__.__name__}({self.issue}, {self.request_id})"

    def run(self):
        tc = TransformationClient()
        for tid in self.issue.metadata.validations[self.request_id].transform_ids:
            # Safety check
            if returnValueOrRaise(tc.getAdditionalParameters(tid))["configName"] != "validation":
                raise ValueError(f"Transformation {tid} is not a validation")
            returnValueOrRaise(tc.setTransformationParameter(tid, "Status", "Cleaning"))
            print(f"Transformation {tid} set to Cleaning")

        self.issue.metadata.validations[self.request_id].cleaned = True
        self.issue.update_metadata()


class CompleteTransformationAction(Action):
    def __init__(self, issue, transform_id):
        self.issue = issue
        self.transform_id = transform_id

    def message(self):
        return f"{self.__class__.__name__}({self.issue}, {self.transform_id})"

    def run(self):
        tc = TransformationClient()
        returnValueOrRaise(tc.setTransformationParameter(self.transform_id, "Status", "Completed"))
        print(f"Transformation {self.transform_id} set to Completed")


class CloseIssueAction(Action):
    def __init__(self, issue):
        self.issue = issue

    def message(self):
        return f"{self.__class__.__name__}({self.issue})"

    def run(self):
        self.issue.issue.state_event = "close"
        self.issue.issue.save()
        print(f"Issue {self.issue} closed")


class AddLabelAction(Action):
    safe = True

    def __init__(self, repo, issue, label):
        self.repo = repo
        self.issue = issue
        self.label = label

    def message(self):
        return f"{self.__class__.__name__}({self.issue}, {self.label})"

    def run(self):
        if self.label not in self.repo.known_labels:
            prefix, _ = self.label.split("::")
            for project_label, color in self.repo.known_labels.items():
                if project_label.startswith(prefix):
                    break
            else:
                raise ValueError(f"Unknown label prefix {prefix}")
            self.repo.project.labels.create({"name": self.label, "color": color})
            # Clear the cache
            del self.repo.known_labels
        self.issue.labels.append(self.label)
        self.issue.issue.save()
