"""Read & extract service metadata and its available operations"""
import copy
import re

import boto3
from botocore.exceptions import UnknownServiceError


def parse_resource_and_operations(
    hub, service_name: str, session: "boto3.session.Session"
):
    """
    Get resource and their available operations for client initialized for a given service

    @returns
        Mapping of resource to its methods and corresponding boto3 operation_name.
        {
            "resource": {
                { "method" : "operation_name" }
            }
        }
    """
    operations = {}

    try:
        client = session.client(service_name=service_name, region_name="us-west-2")
    except UnknownServiceError as ex:
        hub.log.error(f"{ex.__class__.__name__}: {ex}")
        return {}

    # Attempt 1: Lookup resources from service model
    # Supported services: cloudformation, cloudwatch, dynamodb, ec2, glacier, iam, opsworks, s3, sns, sqs
    try:
        service = session.resource(service_name=service_name, region_name="us-west-2")
        service_resources = [
            hub.tool.format.case.snake(r.name)
            for r in service.meta.resource_model.subresources
        ]
        for op in sorted(client.meta.method_to_api_mapping):
            try:
                if "tag" in op:
                    # No need to parse tag functions here
                    continue

                _, resource = op.split("_", maxsplit=1)
                singular = None
                if re.match(rf"\w+[^aoius]s$", resource):
                    singular = hub.tool.format.inflect.singular(resource)
                if resource in service_resources or singular in service_resources:
                    if resource not in operations:
                        operations[resource] = []

                    if op not in operations[resource]:
                        operations[resource].append(op)

            except ValueError:
                continue
    except Exception:
        # It is okay if we cannot get resources from service model, we fall back to default operations lookup
        pass

    # Attempt 2: Now let's look up using all available operations
    for op in sorted(client.meta.method_to_api_mapping):
        try:
            if "tag" in op:
                # No need to parse tag functions here
                continue

            _, resource = op.split("_", maxsplit=1)

            if resource.endswith("apis"):
                resource = resource[:-1]

            # Check for singularity of the resource
            if re.match(rf"\w+[^aoius]s$", resource):
                resource = hub.tool.format.inflect.singular(resource)

            # No need for empty resource to go further
            if resource == "":
                continue

            if resource not in operations:
                operations[resource] = []

            if op not in operations[resource]:
                operations[resource].append(op)

        except ValueError:
            hub.log.error("Failure in extracting operation metadata")

    # Get all potential resource operations (GET/CREATE/UPDATE/DELETE/LIST and TOOL module operations)
    return hub.pop_create.aws.service.get_resource_and_operations(operations)


def get_resource_and_operations(hub, aws_operations: dict):
    resource_and_operations = {}
    for r, ops in aws_operations.items():
        resource_and_operations[r] = {}
        # This will hold all tools operations for a resource
        resource_and_operations[r]["tools"] = []
        for op in sorted(ops):
            # Determine if it is a reserved function or a utility method.
            func_type = hub.pop_create.aws.possible_functions.get_possible_func_type(
                resource_name=r, operation=op
            )

            if func_type == "tools":
                resource_and_operations[r]["tools"].append(op)
            else:
                resource_and_operations[r][func_type] = op

        if (
            "get" not in resource_and_operations[r]
            and "list" in resource_and_operations[r]
        ):
            # majority cases, this is going to be okay. There could be some exceptions.
            resource_and_operations[r]["get"] = resource_and_operations[r]["list"]

        if (
            "update" not in resource_and_operations[r]
            and "create" in resource_and_operations[r]
            and resource_and_operations[r]["create"].startswith("put")
        ):
            # Many "put" operations do support both create and update.
            resource_and_operations[r]["update"] = resource_and_operations[r]["create"]

    for r, ops in resource_and_operations.items():
        # 1. If there is no create operation, most likely, all operations are utility methods on the resource.
        # 2. If there is only single reserved operation other than tools functions, they go into tools module.
        non_utility_ops = copy.copy(ops)
        del non_utility_ops["tools"]
        if "create" not in ops or len(non_utility_ops) < 2:
            other_operations = {
                operation for key, operation in ops.items() if key not in "tools"
            }
            if "tools" in resource_and_operations[r]:
                resource_and_operations[r]["tools"].extend(list(other_operations))
            else:
                resource_and_operations[r] = {"tools": other_operations}

            resource_and_operations[r] = {k: v for k, v in ops.items() if k == "tools"}

    # format :
    # "resource_name": {
    #     "create": ".....",
    #     "delete": "....",
    #     "list": ".....",
    #     "update": ".....",
    #     "get": ".....",
    #     "tools": [
    #         ".....",
    #         ".....",
    #     ]
    # },
    return resource_and_operations


def parse_docstring(hub, session: "boto3.session.Session", service_name: str):
    """
    Get service description
    """
    client = session.client(service_name=service_name, region_name="us-west-2")
    plugin_docstring = hub.tool.format.html.parse(client._service_model.documentation)
    return "\n".join(hub.tool.format.wrap.wrap(plugin_docstring, width=120))


def parse_service_tag_methods(
    hub, session: "boto3.session.Session", aws_service_name: str
):
    """
    Parses service tag method definitions. There is usually a common method at service level which can be used for
    tagging. Sometimes it is single method for update and sometimes there are separate add/remove methods.
    Capture them all here.
    """
    tag_methods = dict()
    try:
        client = session.client(service_name=aws_service_name, region_name="us-west-2")
        for op in client.meta.method_to_api_mapping:
            if re.match("(add|create|put|tag).*_(resource|tags|tagging)", op):
                tag_methods["tag_resource"] = hub.pop_create.aws.function.parse(
                    client=client,
                    aws_service_name=aws_service_name,
                    resource_name=None,
                    func_name=op,
                )
            elif re.match("(remove|delete|untag).*_(resource|tags|tagging)", op):
                tag_methods["untag_resource"] = hub.pop_create.aws.function.parse(
                    client=client,
                    aws_service_name=aws_service_name,
                    resource_name=None,
                    func_name=op,
                )
            elif re.match("(list|get|describe).*_(tags|tagging)", op):
                tag_methods["list_tags"] = hub.pop_create.aws.function.parse(
                    client=client,
                    aws_service_name=aws_service_name,
                    resource_name=None,
                    func_name=op,
                )
            elif re.match("(change).*_(tags)", op):
                tag_methods["update_tags"] = hub.pop_create.aws.function.parse(
                    client=client,
                    aws_service_name=aws_service_name,
                    resource_name=None,
                    func_name=op,
                )
            else:
                continue
    except Exception as err:
        hub.log.error(
            f"Error when generating tag action definitions for {aws_service_name}: {err.__class__.__name__}: {err}"
        )

    return tag_methods
