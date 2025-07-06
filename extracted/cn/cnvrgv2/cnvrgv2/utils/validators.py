import os
import re

import yaml

from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgArgumentsError, CnvrgFileError
from cnvrgv2.modules.users.user import ROLES


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def validate_email(email):
    regex = r'^[\w.-]+[@]\w+(\.\w+)*\.\w{2,5}$'
    return re.search(regex, email) is not None


def validate_user_role(role):
    return role in ROLES.ALL_ROLES


def validate_secret_key(key):
    regex = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return re.match(regex, key) is not None


def validate_username(username):
    regex = r'^[A-Za-z0-9_-]+$'
    return re.search(regex, username) is not None


def validate_directory_name(path):
    regex = r"^[a-zA-Z0-9_.()'!\/-]+$"
    is_dir = os.path.isdir(path)
    if is_dir and not re.match(regex, path):
        raise CnvrgArgumentsError(error_messages.NOT_A_VALID_DIRECTORY_NAME.format(path))


def validate_types_in_list(input_list, input_type):
    """
    Validates that the input is a list of objects from the given type
    @param input_list: The input (should be a list of input_type objects)
    @param input_type: The type of the objects in input_list
    @return: Whenever input_list is a list of input_types
    """
    if not isinstance(input_list, list):
        return False
    for obj in input_list:
        if not isinstance(obj, input_type):
            return False
    return True


def attributes_validator(
        available_attributes,
        attributes,
        required_values=None,
):
    """
    @param available_attributes: Attributes available to the object that is being validated
    @param attributes: Attributes to validate
    @param required_values: Attributes that must be presented in the action
    @return: void, will raise errors on failed validations
    """

    required_values = required_values or []

    # Validates all the required attributes were received (and are not None or equivalent)
    for key in required_values:
        if key not in attributes.keys() or not attributes[key]:
            raise CnvrgArgumentsError(error_messages.MISSING_REQUIRED_VALUE.format(key))

    for key, value in attributes.items():
        # Validates that only allowed attributes were received
        if key == 'slug' or key not in available_attributes.keys():
            raise CnvrgArgumentsError(error_messages.FAULTY_KEY.format(key))
        # Validate received attribute types
        if value and not isinstance(value, available_attributes[key]):
            raise CnvrgArgumentsError(error_messages.FAULTY_VALUE.format(key))


# COMPUTES
def validate_gpu(gpu_obj):
    AVAILABLE_MIG_TYPES = [
        None,
        'mig-1g.5g',
        'mig-2g.20g',
        'mig-3g.25g'
    ]

    gpu = gpu_obj["count"]
    mig_device = gpu_obj["mig_device"]
    if mig_device not in AVAILABLE_MIG_TYPES:
        raise CnvrgArgumentsError(error_messages.TEMPLATE_FAULTY_MIG_VALUE)
    if gpu and not isinstance(gpu, float):
        raise CnvrgArgumentsError(error_messages.TEMPLATE_FAULTY_GPU.format(gpu))
    if mig_device and not isinstance(mig_device, str):
        raise CnvrgArgumentsError(error_messages.TEMPLATE_FAULTY_MIG.format(mig_device))


def validate_template_type(template_type):
    AVAILABLE_TEMPLATE_TYPES = [
        'regular',
        'mpi',
        'kubernetes',
        'pytorch',
        'spark_on_kubernetes',
        'ray',
        'ray_modin'
    ]

    if template_type and template_type not in AVAILABLE_TEMPLATE_TYPES:
        raise CnvrgArgumentsError(error_messages.TEMPLATE_FAULTY_TYPE)


def validate_hyper_parameters(parameters):
    types = ["discrete", "float", "integer", "categorical"]
    if parameters and not isinstance(parameters, list):
        raise CnvrgArgumentsError(error_messages.EXPERIMENT_FAULTY_PARAMETERS)

    # Check if there is duplicates in the parameters key
    keys = [param.get("key") for param in parameters]
    if len(keys) != len(set(keys)):
        raise CnvrgArgumentsError(error_messages.EXPERIMENT_DUPLICATE_PARAMETERS.format(keys))

    for param in parameters:
        # Validate parameter name
        if not param.get("key"):
            raise CnvrgArgumentsError(error_messages.EXPERIMENT_FAULTY_PARAMETERS_KEY)
        # Validate parameter type
        if param.get("type") not in types:
            raise CnvrgArgumentsError(error_messages.EXPERIMENT_FAULTY_PARAMETERS_TYPE)
        # Validate parameter values
        if param.get("type") == "discrete":
            validate_discrete_params(param.get("values"))
        # Validate parameter step is positive
        if param.get("steps") and param.get("steps") < 0:
            raise CnvrgArgumentsError(error_messages.EXPERIMENT_FAULTY_PARAMETERS_STEPS)


def validate_discrete_params(values):
    if not values:
        raise CnvrgArgumentsError(error_messages.EXPERIMENT_FAULTY_PARAMETERS_VALUES)
    if not isinstance(values, list):
        raise CnvrgArgumentsError(error_messages.EXPERIMENT_FAULTY_PARAMETERS_LIST)
    for value in values:
        if not isinstance(value, int) and not isinstance(value, float):
            raise CnvrgArgumentsError(error_messages.EXPERIMENT_FAULTY_PARAMETERS_INT)


def has_potential_csv_injection(user_input):
    """
    Validates that the given input doesn't start with characters that might indicate a csv injection
    @param user_input: The input to validate
    @return: bool. Whenever the first character might indicate a csv injection
    """
    forbidden_start_characters = re.compile(r'^[=+\-@\s\t\n\r,;\'"]+')
    return bool(forbidden_start_characters.match(user_input))


def _validate_yaml_path(yaml_path):
    """
    Checks the correctness of a YAML file
    @param yaml_path: Path of the yaml file
    @return: True or False
    """
    if not os.path.exists(yaml_path):
        raise CnvrgFileError(error_messages.NO_FILE)
    try:
        with open(yaml_path, 'r') as f:
            yaml.safe_load(f)
    except Exception:
        raise CnvrgFileError(error_messages.FLOW_GET_FAULTY_YAML)


def _validate_yaml_string(yaml_string):
    """
    Checks the correctness of a YAML string
    @param yaml_string: string of the yaml
    @return: True or False
    """
    if not yaml_string:
        raise CnvrgArgumentsError(error_messages.EMPTY_ARGUMENT.format("yaml_string"))
    try:
        yaml.safe_load(yaml_string)
    except Exception:
        raise CnvrgArgumentsError(error_messages.FLOW_GET_FAULTY_YAML)


def validate_storage_class_title(key):
    regex = r'^[a-z0-9-]+$'
    return re.match(regex, key) is not None


def validate_volume_title(key):
    regex = r'^[a-z0-9-]+$'
    return re.match(regex, key) is not None
