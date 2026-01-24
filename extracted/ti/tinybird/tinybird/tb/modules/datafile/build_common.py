from typing import Any, Dict, List, Optional, Tuple

import click

from tinybird.tb.client import DoesNotExistException, TinyB
from tinybird.tb.modules.feedback_manager import FeedbackManager


def update_tags(resource_id: str, resource_name: str, resource_type: str, tags: List[str], tb_client: TinyB):
    def get_tags_for_resource(all_tags: dict, resource_id: str, resource_name: str) -> List[str]:
        tag_names = []

        for tag in all_tags.get("tags", []):
            for resource in tag.get("resources", []):
                if resource.get("id") == resource_id or resource.get("name") == resource_name:
                    tag_names.append(tag.get("name"))
                    break  # No need to check other resources in this tag

        return tag_names

    def get_tag(all_tags: dict, tag_name: str) -> Optional[dict]:
        for tag in all_tags.get("tags", []):
            if tag.get("name") == tag_name:
                return tag
        return None

    def compare_tags(current_tags: List[str], new_tags: List[str]) -> Tuple[List[str], List[str]]:
        tags_to_add = list(set(new_tags) - set(current_tags))
        tags_to_remove = list(set(current_tags) - set(new_tags))
        return tags_to_add, tags_to_remove

    try:
        all_tags = tb_client.get_all_tags()
    except Exception as e:
        raise Exception(FeedbackManager.error_getting_tags(error=str(e)))

    # Get all tags of that resource
    current_tags = get_tags_for_resource(all_tags, resource_id, resource_name)

    # Get the tags to add and remove
    tags_to_add, tags_to_remove = compare_tags(current_tags, tags)

    # Tags to add
    for tag_name in tags_to_add:
        tag = get_tag(all_tags, tag_name)

        if not tag:
            # Create new tag
            try:
                tb_client.create_tag_with_resource(
                    name=tag_name,
                    resource_id=resource_id,
                    resource_name=resource_name,
                    resource_type=resource_type,
                )
            except Exception as e:
                raise Exception(FeedbackManager.error_creating_tag(error=str(e)))
        else:
            # Update tag with new resource
            resources = tag.get("resources", [])
            resources.append({"id": resource_id, "name": resource_name, "type": resource_type})
            try:
                tb_client.update_tag(tag.get("name", tag_name), resources)
            except Exception as e:
                raise Exception(FeedbackManager.error_updating_tag(error=str(e)))

    # Tags to delete
    for tag_name in tags_to_remove:
        tag = get_tag(all_tags, tag_name)

        if tag:
            resources = tag.get("resources", [])
            resources = [resource for resource in resources if resource.get("name") != resource_name]
            try:
                tb_client.update_tag(tag.get("name", tag_name), resources)
            except Exception as e:
                raise Exception(FeedbackManager.error_updating_tag(error=str(e)))


def update_tags_in_resource(rs: Dict[str, Any], resource_type: str, client: TinyB):
    filtering_tags = rs.get("filtering_tags", [])

    if not filtering_tags:
        return

    resource_id = ""
    resource_name = ""

    if resource_type == "datasource":
        ds_name = rs["params"]["name"]
        try:
            persisted_ds = client.get_datasource(ds_name)
            resource_id = persisted_ds.get("id", "")
            resource_name = persisted_ds.get("name", "")
        except DoesNotExistException:
            click.echo(
                FeedbackManager.error_tag_generic("Could not get the latest data source info for updating its tags.")
            )
    elif resource_type == "pipe":
        pipe_name = rs["name"]
        try:
            persisted_pipe = client.pipe(pipe_name)
            resource_id = persisted_pipe.get("id", "")
            resource_name = persisted_pipe.get("name", "")
        except DoesNotExistException:
            click.echo(FeedbackManager.error_tag_generic("Could not get the latest Pipe info for updating its tags."))

    if resource_id and resource_name:
        try:
            update_tags(
                resource_id=resource_id,
                resource_name=resource_name,
                resource_type=resource_type,
                tags=filtering_tags,
                tb_client=client,
            )
        except Exception as e:
            click.echo(FeedbackManager.error_tag_generic(error=str(e)))
