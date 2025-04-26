import agilicus

from agilicus.agilicus_api import (
    ResourceConfig,
)


def map_resource_published(mapping, published):
    if published is not None:
        config = mapping.spec.resource_config
        if config is None:
            config = ResourceConfig()
            mapping.spec.resource_config = config
        mapping.spec.resource_config["published"] = published
    return mapping


def add_display_info_icon(info_container, uri, purpose, height_px, width_px):
    display_info = info_container.display_info
    if display_info is None:
        display_info = agilicus.DisplayInfo(icons=[])
        info_container.display_info = display_info

    purposes = [agilicus.IconPurpose(p) for p in purpose]
    new_icon = agilicus.Icon(uri=uri, purposes=purposes)
    if height_px is not None and width_px is not None:
        new_icon.dimensions = agilicus.IconDimensions(width=width_px, height=height_px)
    display_info.icons.append(new_icon)


def delete_display_info_icon(info_container, uri):
    if not info_container:
        return False

    display_info = info_container.display_info
    if not info_container:
        return False

    icons = [icon for icon in display_info.icons if icon.uri != uri]
    display_info.icons = icons
    return True
