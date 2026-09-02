import uuid
from matrx_ai.db._registry import get_model
RenderDefinition = get_model("RenderDefinition")
from matrx_utils import vcprint, clear_terminal


def is_valid_uuid(value):
    """Check if a string is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError):
        return False


def fetch_content_blocks_direct(value):
    if is_valid_uuid(value):
        content_block = RenderDefinition.get_or_none_sync(id=value)
        text = content_block.template
    else:
        content_block = RenderDefinition.get_or_none_sync(block_id=value)
        text = content_block.template

    return text


def fetch_content_block(field_name: str, value: str):
    field_name = field_name.lower()
    content_block = RenderDefinition.get_or_none_sync(**{field_name: value})
    text = content_block.template
    return text


def fetch_content_blocks(field_name: str, value: str):
    field_name = field_name.lower()
    content_blocks = RenderDefinition.filter_sync(**{field_name: value})
    text = ""
    for content_block in content_blocks:
        text += f"{content_block.template}\n\n"
    return text


def fetch_content_blocks_flexible(
    field_name: str, value: str, template_fn: callable = lambda cb: cb.template
):
    field_name = field_name.lower()
    content_blocks = RenderDefinition.filter_sync(**{field_name: value})
    text = ""
    for content_block in content_blocks:
        text += f"{template_fn(content_block)}\n\n"
    return text


def fetch_content_blocks_by_attribute(field_name: str, value: str, content_attr: str):
    field_name = field_name.lower()
    content_blocks = RenderDefinition.filter_sync(**{field_name: value})
    text = ""
    for content_block in content_blocks:
        attr_value = getattr(content_block, content_attr, "")
        text += f"{attr_value}\n\n"
    return text


def fetch_content_blocks_by_attributes(
    field_name: str, value: str, content_attrs: str | list[str]
):
    field_name = field_name.lower()
    content_blocks = RenderDefinition.filter_sync(**{field_name: value})

    # Normalize to list
    attrs = [content_attrs] if isinstance(content_attrs, str) else content_attrs

    text = ""
    for content_block in content_blocks:
        for attr in attrs:
            attr_value = getattr(content_block, attr, "")
            if attr_value:  # Only add if there's content
                text += f"{attr_value}\n\n"

    return text


if __name__ == "__main__":
    clear_terminal()
    # content_block = fetch_content_blocks_direct("flashcards")
    # vcprint(content_block, "Content Blocks 1", color="green")

    # content_block = fetch_content_blocks_direct("b46e284e-ccb0-4d32-8a96-07f85d50d134")
    # vcprint(content_block, "Content Blocks 2", color="green")

    # content_block = fetch_content_blocks("BLOCK_ID", "flashcards")
    # vcprint(content_block, "Content Block 3 - Block ID", color="blue")

    # content_block = fetch_content_blocks("id", "b46e284e-ccb0-4d32-8a96-07f85d50d134")
    # vcprint(content_block, "Content Block 4 - ID", color="green")

    # content_blocks = fetch_content_blocks("CATEGORY_ID", "9980e68f-97fc-4f71-bf1d-22583b6cdf38")
    # vcprint(content_blocks, "Content Blocks 5 - Category ID", color="magenta")

    # content = fetch_content_blocks_flexible(
    #     "CATEGORY_ID",
    #     "9980e68f-97fc-4f71-bf1d-22583b6cdf38",
    #     lambda cb: f"\n==============\n**{cb.label}**\n==============\n\n{cb.template}",
    # )
    # vcprint(content, "Content 7 - Category ID - Template - Flexible", color="cyan")

    # content = fetch_content_blocks_by_attribute(
    #     "CATEGORY_ID", "9980e68f-97fc-4f71-bf1d-22583b6cdf38", "template"
    # )
    # vcprint(content, "Content 6 - Category ID - Template", color="cyan")

    content = fetch_content_blocks_by_attributes(
        "CATEGORY_ID", "9980e68f-97fc-4f71-bf1d-22583b6cdf38", ["template", "label"]
    )
    vcprint(content, "Content 6 - Category ID - Template and Label", color="yellow")
