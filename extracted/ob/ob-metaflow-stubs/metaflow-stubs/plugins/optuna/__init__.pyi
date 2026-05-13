######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.29.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-05-12T17:11:58.000345                                                            #
######################################################################################################

from __future__ import annotations



def auth():
    ...

def get_deployment_db_access_endpoint(name: str, project: str = None, branch: str = None):
    ...

def get_db_url(app_name: str, project: str = None, branch: str = None):
    """
    Example usage:
        >>> from metaflow.plugins.optuna import get_db_url
        >>> s = optuna.create_study(..., storage=get_db_url("optuna-dashboard"))
    """
    ...

