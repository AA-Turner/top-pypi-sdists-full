#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025


def find_default_stage_definition(json_data: dict, stage_name: str) -> dict:
    stream_selector_definition = {}
    for stage in json_data["libraryDefinitions"]["stages"]:
        if stage["name"] == stage_name:
            stream_selector_definition = stage
            break

    return stream_selector_definition


def find_stage_definition(json_data: dict, stage_name: str) -> dict:
    stage_definition = {}
    for stage in json_data["pipelineConfig"]["stages"]:
        if stage["stageName"] == stage_name:
            stage_definition = stage
            break

    return stage_definition
