######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.31                                                                                #
# Generated on 2026-06-01T01:50:49.601356                                                            #
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

