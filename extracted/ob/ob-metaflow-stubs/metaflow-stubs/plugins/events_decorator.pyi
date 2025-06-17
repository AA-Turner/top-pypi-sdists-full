######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.903056                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ..metaflow_current import current as current
from ..exception import MetaflowException as MetaflowException
from ..parameters import DeployTimeField as DeployTimeField
from ..parameters import deploy_time_eval as deploy_time_eval

class TriggerDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Specifies the event(s) that this flow depends on.
    
    ```
    @trigger(event='foo')
    ```
    or
    ```
    @trigger(events=['foo', 'bar'])
    ```
    
    Additionally, you can specify the parameter mappings
    to map event payload to Metaflow parameters for the flow.
    ```
    @trigger(event={'name':'foo', 'parameters':{'flow_param': 'event_field'}})
    ```
    or
    ```
    @trigger(events=[{'name':'foo', 'parameters':{'flow_param_1': 'event_field_1'},
                     {'name':'bar', 'parameters':{'flow_param_2': 'event_field_2'}])
    ```
    
    'parameters' can also be a list of strings and tuples like so:
    ```
    @trigger(event={'name':'foo', 'parameters':['common_name', ('flow_param', 'event_field')]})
    ```
    This is equivalent to:
    ```
    @trigger(event={'name':'foo', 'parameters':{'common_name': 'common_name', 'flow_param': 'event_field'}})
    ```
    
    Parameters
    ----------
    event : Union[str, Dict[str, Any]], optional, default None
        Event dependency for this flow.
    events : List[Union[str, Dict[str, Any]]], default []
        Events dependency for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    
    MF Add To Current
    -----------------
    trigger -> metaflow.events.Trigger
        Returns `Trigger` if the current run is triggered by an event
    
        @@ Returns
        -------
        Trigger
            `Trigger` if triggered by an event
    """
    def process_event_name(self, event):
        ...
    def process_parameters(self, parameters):
        ...
    def flow_init(self, flow_name, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    def format_deploytime_value(self):
        ...
    ...

class TriggerOnFinishDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Specifies the flow(s) that this flow depends on.
    
    ```
    @trigger_on_finish(flow='FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['FooFlow', 'BarFlow'])
    ```
    This decorator respects the @project decorator and triggers the flow
    when upstream runs within the same namespace complete successfully
    
    Additionally, you can specify project aware upstream flow dependencies
    by specifying the fully qualified project_flow_name.
    ```
    @trigger_on_finish(flow='my_project.branch.my_branch.FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['my_project.branch.my_branch.FooFlow', 'BarFlow'])
    ```
    
    You can also specify just the project or project branch (other values will be
    inferred from the current project or project branch):
    ```
    @trigger_on_finish(flow={"name": "FooFlow", "project": "my_project", "project_branch": "branch"})
    ```
    
    Note that `branch` is typically one of:
      - `prod`
      - `user.bob`
      - `test.my_experiment`
      - `prod.staging`
    
    Parameters
    ----------
    flow : Union[str, Dict[str, str]], optional, default None
        Upstream flow dependency for this flow.
    flows : List[Union[str, Dict[str, str]]], default []
        Upstream flow dependencies for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    
    MF Add To Current
    -----------------
    trigger -> metaflow.events.Trigger
        Returns `Trigger` if the current run is triggered by an event
    
        @@ Returns
        -------
        Trigger
            `Trigger` if triggered by an event
    """
    def flow_init(self, flow_name, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    def format_deploytime_value(self):
        ...
    def get_top_level_options(self):
        ...
    ...

