######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.903656                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException
from ..metaflow_current import current as current

VALID_NAME_RE: str

VALID_NAME_LEN: int

class ProjectDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Specifies what flows belong to the same project.
    
    A project-specific namespace is created for all flows that
    use the same `@project(name)`.
    
    Parameters
    ----------
    name : str
        Project name. Make sure that the name is unique amongst all
        projects that use the same production scheduler. The name may
        contain only lowercase alphanumeric characters and underscores.
    
    branch : Optional[str], default None
        The branch to use. If not specified, the branch is set to
        `user.<username>` unless `production` is set to `True`. This can
        also be set on the command line using `--branch` as a top-level option.
        It is an error to specify `branch` in the decorator and on the command line.
    
    production : bool, default False
        Whether or not the branch is the production branch. This can also be set on the
        command line using `--production` as a top-level option. It is an error to specify
        `production` in the decorator and on the command line.
        The project branch name will be:
          - if `branch` is specified:
            - if `production` is True: `prod.<branch>`
            - if `production` is False: `test.<branch>`
          - if `branch` is not specified:
            - if `production` is True: `prod`
            - if `production` is False: `user.<username>`
    
    MF Add To Current
    -----------------
    project_name -> str
        The name of the project assigned to this flow, i.e. `X` in `@project(name=X)`.
    
        @@ Returns
        -------
        str
            Project name.
    
    project_flow_name -> str
        The flow name prefixed with the current project and branch. This name identifies
        the deployment on a production scheduler.
    
        @@ Returns
        -------
        str
            Flow name prefixed with project information.
    
    branch_name -> str
        The current branch, i.e. `X` in `--branch=X` set during deployment or run.
    
        @@ Returns
        -------
        str
            Branch name.
    
    is_user_branch -> bool
        True if the flow is deployed without a specific `--branch` or a `--production`
        flag.
    
        @@ Returns
        -------
        bool
            True if the deployment does not correspond to a specific branch.
    
    is_production -> bool
        True if the flow is deployed with the `--production` flag
    
        @@ Returns
        -------
        bool
            True if the flow is deployed with `--production`.
    """
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    def get_top_level_options(self):
        ...
    ...

def format_name(flow_name, project_name, deploy_prod, given_branch, user_name):
    ...

