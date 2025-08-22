######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.17.1.0+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-21T23:31:59.760892                                                            #
######################################################################################################

from __future__ import annotations


from ...exception import MetaflowException as MetaflowException

DISALLOWED_SECRETS_ENV_VAR_PREFIXES: list

def get_default_secrets_backend_type():
    ...

def validate_env_vars_across_secrets(all_secrets_env_vars):
    ...

def validate_env_vars_vs_existing_env(all_secrets_env_vars):
    ...

def validate_env_vars(env_vars):
    ...

def get_secrets_backend_provider(secrets_backend_type):
    ...

