"""Build CRUD function definitions for a resource to be used in resource plugins"""
from typing import Any
from typing import Dict


def parse_functions(
    hub,
    session: "boto3.session.Session",
    aws_service_name: str,
    resource_name: str,
    functions: dict,
) -> Dict[str, Any]:
    resource_methods = {}
    try:
        client = session.client(service_name=aws_service_name, region_name="us-west-2")

        resource_methods["get"] = hub.pop_create.aws.function.parse(
            client=client,
            aws_service_name=aws_service_name,
            resource_name=resource_name,
            func_name=functions.get("get"),
        )

        resource_methods["list"] = hub.pop_create.aws.function.parse(
            client=client,
            aws_service_name=aws_service_name,
            resource_name=resource_name,
            func_name=functions.get("list"),
        )

        resource_methods["create"] = hub.pop_create.aws.function.parse(
            client=client,
            aws_service_name=aws_service_name,
            resource_name=resource_name,
            func_name=functions.get("create"),
        )

        resource_methods["delete"] = hub.pop_create.aws.function.parse(
            client=client,
            aws_service_name=aws_service_name,
            resource_name=resource_name,
            func_name=functions.get("delete"),
        )

        resource_methods["update"] = hub.pop_create.aws.function.parse(
            client=client,
            aws_service_name=aws_service_name,
            resource_name=resource_name,
            func_name=functions.get("update"),
        )

        for func_name in functions.get("tools", []):
            try:
                resource_methods[func_name] = hub.pop_create.aws.function.parse(
                    client=client,
                    aws_service_name=aws_service_name,
                    resource_name=resource_name,
                    func_name=func_name,
                )
            except Exception as err:
                hub.log.error(
                    f"Error when generating resource's action definitions for {resource_name}:{func_name}: {err.__class__.__name__}: {err}"
                )

    except Exception as err:
        hub.log.error(
            f"Error when generating resource's action definitions for {resource_name}: {err.__class__.__name__}: {err}"
        )

    return resource_methods
