######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.019564                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException
from ..kubernetes.kubernetes_client import KubernetesClient as KubernetesClient

class ArgoClientException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class ArgoResourceNotFound(metaflow.exception.MetaflowException, metaclass=type):
    ...

class ArgoNotPermitted(metaflow.exception.MetaflowException, metaclass=type):
    ...

class ArgoClient(object, metaclass=type):
    def __init__(self, namespace = None):
        ...
    def get_workflow(self, name):
        ...
    def get_workflow_template(self, name):
        ...
    def get_workflow_templates(self):
        ...
    def register_workflow_template(self, name, workflow_template):
        ...
    def delete_cronworkflow(self, name):
        """
        Issues an API call for deleting a cronworkflow
        
        Returns either the successful API response, or None in case the resource was not found.
        """
        ...
    def delete_workflow_template(self, name):
        """
        Issues an API call for deleting a cronworkflow
        
        Returns either the successful API response, or None in case the resource was not found.
        """
        ...
    def terminate_workflow(self, name):
        ...
    def suspend_workflow(self, name):
        ...
    def unsuspend_workflow(self, name):
        ...
    def trigger_workflow_template(self, name, usertype, username, parameters = {}):
        ...
    def schedule_workflow_template(self, name, schedule = None, timezone = None):
        ...
    def register_sensor(self, name, sensor = None):
        ...
    def delete_sensor(self, name):
        """
        Issues an API call for deleting a sensor
        
        Returns either the successful API response, or None in case the resource was not found.
        """
        ...
    ...

def wrap_api_error(error):
    ...

