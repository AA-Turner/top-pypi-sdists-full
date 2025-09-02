"""Read operation's metadata and extract function definition"""
import botocore.client
import botocore.docs.docstring
from dict_tools.data import NamespaceDict


def parse(
    hub,
    client,
    aws_service_name: str,
    resource_name: str,
    func_name: str,
):
    if not func_name:
        return {
            "doc": "",
            "params": {},
            "hardcoded": {
                "aws_service_name": aws_service_name,
                "resource_name": resource_name,
                "boto3_documentation": f"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{aws_service_name}.html",
            },
        }

    function = getattr(client, func_name)
    doc: botocore.docs.docstring.ClientMethodDocstring = function.__doc__
    docstring = hub.tool.format.html.parse(doc._gen_kwargs["method_description"])

    function_doc = "\n".join(hub.tool.format.wrap.wrap(docstring, width=112))
    is_idempotent = "idempotent" in function_doc.lower()

    # Parse request params
    parameters = hub.pop_create.aws.function.resolve_request_params(
        aws_service_name, func_name, doc
    )
    hub.pop_create.aws.function.normalize_name_param(parameters)

    function_input_param_names = list(parameters.keys())
    function_resource_to_input_param_mappings = dict(
        map(
            lambda x: (hub.tool.format.case.snake(x), x),
            parameters.keys(),
        )
    )

    # Parse response
    (
        response_key,
        raw_resource_mappings,
    ) = hub.pop_create.aws.function.resolve_response_metadata(
        aws_service_name, func_name, doc
    )

    possible_response_keys = []
    if not response_key:
        possible_response_keys = list(raw_resource_mappings.keys())

    # This is helpful when resolving params
    boto3_documentation = f"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{aws_service_name}/client/{func_name}.html"

    # Build function definition
    ret = {
        "doc": f"{function_doc}",
        "params": parameters,
        "hardcoded": {
            "aws_service_name": aws_service_name,
            "resource_name": resource_name,
            "function": func_name,
            "boto3_function": f"hub.exec.boto3.client.{aws_service_name}.{func_name}",
            "boto3_documentation": boto3_documentation,
            "function_input_param_names": function_input_param_names,
            "function_resource_to_input_param_mappings": function_resource_to_input_param_mappings,
            "response_key": response_key,
            "possible_response_keys": possible_response_keys,
            "resource_to_raw_resource_mappings": {
                v: k for k, v in raw_resource_mappings.items()
            },
            "raw_resource_to_resource_mapping": raw_resource_mappings,
            "resource_attributes": list(raw_resource_mappings.keys()),
            "has_client_token": bool(parameters.get("ClientToken", None)),
            "is_idempotent": is_idempotent,
        },
    }

    return ret


def resolve_request_params(
    hub,
    aws_service_name,
    func_name,
    doc: "botocore.docs.docstring.ClientMethodDocstring",
):
    parameters = NamespaceDict()
    try:
        input_param_struct = doc._gen_kwargs["operation_model"].input_shape

        if not input_param_struct:
            return parameters

        params = input_param_struct.members
        required_params = doc._gen_kwargs[
            "operation_model"
        ].input_shape.required_members

        # these params are not used in idem-aws, should be skipped
        unused_params = ["DryRun", "Marker", "MaxRecords", "MaxResults", "NextToken"]

        for p, data in params.items():
            # Unwrap TagSpecification and get tags
            if "TagSpecifications" in p:
                p = "tags"
                data = data.member.members["Tags"]
            elif p in unused_params:
                # skip these params as idem-aws don't make use of it
                continue
            parameters[p] = hub.pop_create.aws.param.parse(
                param=data, required=p in required_params, parsed_nested_params=[]
            )
    except AttributeError as e:
        hub.log.error(
            f"Error reading parameters for {aws_service_name}.{func_name}: {e}"
        )

    return parameters


def normalize_name_param(hub, parameters: dict):
    # Normalize the name parameter
    name = None
    if "Name" in parameters:
        name = parameters.pop("Name")
    elif "name" in parameters:
        name = parameters.pop("name")

    if bool(name):
        parameters["Name"] = name


def resolve_response_metadata(
    hub,
    aws_service_name,
    func_name,
    doc: "botocore.docs.docstring.ClientMethodDocstring",
):
    response_metadata = doc._gen_kwargs["operation_model"].output_shape

    if response_metadata is None:
        return None, {}

    response_key = None
    raw_resource_mappings = {}

    try:
        # these params are not used in idem-aws, should be skipped
        paginated_response_unused_params = [
            "Marker",
            "MaxRecords",
            "MaxResults",
            "NextToken",
            "TotalCount",
        ]

        response_params = response_metadata.members
        is_paginated_response = any(
            p in paginated_response_unused_params for p in response_params.keys()
        )
        if is_paginated_response:
            for p, data in response_params.items():
                if p in paginated_response_unused_params:
                    # skip "Marker" as idem-aws don't make use of it
                    continue

                if isinstance(data, botocore.model.StructureShape):
                    # Example:
                    #   {
                    #     'Certificate': {
                    #           .....
                    #      }
                    #   }
                    raw_resource_mappings = dict(
                        map(
                            lambda x: (x, hub.tool.format.case.snake(x)),
                            data.members.keys(),
                        )
                    )
                elif isinstance(data, botocore.model.ListShape):
                    # Example:
                    #   {
                    #     'Vpcs': [
                    #         {
                    #               .....
                    #         },
                    #     ]
                    #   }
                    raw_resource_mappings = dict(
                        map(
                            lambda x: (x, hub.tool.format.case.snake(x)),
                            data.member.members.keys(),
                        )
                    )

                # This should be the only remaining response param after discarding pagination params
                response_key = p
        else:
            raw_resource_mappings = dict(
                map(
                    lambda x: (x, hub.tool.format.case.snake(x)), response_params.keys()
                )
            )
    except AttributeError as e:
        hub.log.error(
            f"Error reading return fields for {aws_service_name}.{func_name}: {e}"
        )

    return response_key, raw_resource_mappings
