import json
from datetime import datetime

from _qwak_proto.qwak.builds.builds_pb2 import BuildStatus, ValueType
from _qwak_proto.qwak.deployment.deployment_pb2 import ModelDeploymentStatus
from google.protobuf.json_format import MessageToDict
from qwak.clients.build_orchestrator import BuildOrchestratorClient
from qwak.clients.deployment.client import DeploymentManagementClient
from qwak.clients.model_management import ModelsManagementClient
from tabulate import tabulate


def execute_model_describe(model_id, interface, show_list_builds, output_format):
    model = _model_data(model_id)
    deployment_data = _get_deployment_data(model)
    list_builds = _builds_data(show_list_builds, model)
    schema_data = _schema_data(interface, deployment_data)
    if output_format == "text":
        print_text_data(model, list_builds, schema_data, deployment_data)
    elif output_format == "json":
        print_json_data(model, list_builds, schema_data)


def _get_deployment_data(model):
    return DeploymentManagementClient().get_deployment_details(
        model_id=model.model_id, model_uuid=model.uuid
    )


def _model_data(model_id):
    models_management = ModelsManagementClient()
    return models_management.get_model(model_id)


def _builds_data(list_builds, model):
    if list_builds:
        builds_orchestrator = BuildOrchestratorClient()
        return builds_orchestrator.list_builds(model.uuid)
    return None


def _schema_data(interface, deployment_data):
    if interface and deployment_data.current_deployment_details.build_id:
        build_response = BuildOrchestratorClient().get_build(
            deployment_data.current_deployment_details.build_id
        )
        if build_response.build.HasField("model_schema"):
            return build_response.build.model_schema
    return None


def print_json_data(model, list_builds, schema_data):
    output = MessageToDict(model)
    if list_builds:
        output["builds"] = MessageToDict(list_builds)
    if schema_data:
        output["interface"] = MessageToDict(schema_data)
    print(json.dumps(output, indent=4, sort_keys=True))


def print_text_data(model, list_builds, schema_data, deployment_data):
    print(
        f"Model id: {model.model_id}\nDisplay name: {model.display_name}\nDescription: {model.model_description}\n"
        + f'Creation Date: {datetime.fromtimestamp(model.created_at.seconds + model.created_at.nanos / 1e9).strftime("%A, %B %d, %Y %I:%M:%S")}\n'
        + f'Last update: {datetime.fromtimestamp(model.created_at.seconds + model.last_modified_at.nanos / 1e9).strftime("%A, %B %d, %Y %I:%M:%S")}'
    )
    if list_builds:
        _print_text_builds(deployment_data, list_builds)
    if schema_data:
        _print_text_schema(schema_data)


def _print_text_schema(schema_data):
    columns = [
        "Parameter name",
        "Parameter type",
        "Parameter source",
        "Parameter category",
    ]
    data = []
    for entity in schema_data.entities:
        data.append(
            [
                entity.name,
                ValueType.Types.Name(entity.type.type),
                None,
                "Input",
            ]
        )
    for feature in schema_data.features:
        parsed_feature = _parse_feature(feature)
        if parsed_feature:
            data.append(parsed_feature)

    for prediction in schema_data.predictions:
        data.append(
            [
                prediction.name,
                ValueType.Types.Name(prediction.type.type),
                None,
                "Output",
            ]
        )
    print("\n" + tabulate(data, headers=columns))


def _parse_feature(feature):
    if feature.HasField("explicit_feature"):
        return [
            feature.explicit_feature.name,
            ValueType.Types.Name(feature.explicit_feature.type.type),
            None,
            "Input",
        ]
    elif feature.HasField("batch_feature"):
        return [
            feature.batch_feature.name,
            None,
            feature.batch_feature.entity.name,
            "Batch Feature",
        ]
    elif feature.HasField("on_the_fly_feature"):
        return [
            feature.on_the_fly_feature.name,
            None,
            str(
                [
                    source.explicit_feature.name
                    for source in feature.on_the_fly_feature.source_features
                ]
            ),
            "On-The-Fly Feature",
        ]


def _print_text_builds(deployment_data, list_builds):
    columns = [
        "Build id",
        "Commit id",
        "Last modified date",
        "Build Status",
        "Deployment build status",
    ]
    data = []
    for build in list_builds.build:
        deployments = deployment_data.build_to_environment_deployment_status.get(
            build.buildId
        )
        if deployments:
            deployment_status = ModelDeploymentStatus.Name(
                number=list(deployments.environment_to_deployment_brief.values())[
                    0
                ].status
            )
        else:
            deployment_status = ""
        data.append(
            [
                build.buildId,
                build.commitId,
                datetime.fromtimestamp(
                    build.audit.last_modified_at.seconds
                    + build.audit.last_modified_at.nanos / 1e9
                ).strftime("%A, %B %d, %Y %I:%M:%S"),
                BuildStatus.Name(number=build.build_status),
                deployment_status,
            ]
        )
    print("\n" + tabulate(data, headers=columns))
