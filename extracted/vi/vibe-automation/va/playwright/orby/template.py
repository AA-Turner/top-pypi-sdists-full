import re
import os
import json
from jinja2 import Environment, StrictUndefined, Template as Jinja2Template


class Template:
    SUPPORTED_IMAGE_PREFIXES = ["image:"]
    SUPPORTED_IMAGE_ITERABLE_PREFIXES = ["images:"]

    def __init__(self, template_str_or_file_name: str):
        """
        Initialize a Template object from a Jinja2 template string or file.

        :param template_str_or_file_name: The Jinja2 template content as a string or the path to a template file.
        """
        if os.path.exists(template_str_or_file_name):
            self.template_str = load_template(template_str_or_file_name)
        else:
            self.template_str = template_str_or_file_name
        self.template = create_template(self.template_str)

    def render(
        self,
        *,
        replace_image_placeholders_as: str | None = None,
        block: str | None = None,
        **kwargs,
    ):
        """
        Render the template with the given keyword arguments.

        :param replace_image_placeholders_as: If provided, replace the image placeholders with the given string and return the images as a list.
        :param block: If provided, render the specified block from the template.
        :param kwargs: The keyword arguments to be passed to the template, including any image objects.

        :return:
            A string, rendered prompt with image placeholders
            A list or dictionary of images, depending on the value of replace_image_placeholders_as
        """

        if block:
            rendered_prompt = render_block(self.template, block, kwargs)
        else:
            rendered_prompt = self.template.render(**kwargs)

        image_pattern = re.compile(
            rf"<({'|'.join(self.SUPPORTED_IMAGE_PREFIXES + self.SUPPORTED_IMAGE_ITERABLE_PREFIXES)})([^>]*)>"
        )
        image_dict = {}

        new_prompt = ""
        last_index = 0
        for image_tag in image_pattern.finditer(rendered_prompt):
            image_prefix = image_tag.group(1)
            new_prompt += rendered_prompt[last_index : image_tag.start()]
            if image_prefix in self.SUPPORTED_IMAGE_ITERABLE_PREFIXES:
                # Expand the iterable into individual images
                iterable_name = image_tag.group(2)
                images = kwargs[iterable_name]
                for i, image in enumerate(images):
                    image_dict[f"{iterable_name}.{i}"] = image
                    new_prompt += (
                        f"<{self.SUPPORTED_IMAGE_PREFIXES[0]}{iterable_name}.{i}>"
                    )
            else:
                image_name = image_tag.group(2)
                new_prompt += image_tag.group(0)

                image_dict[image_name] = kwargs[image_name]

            last_index = image_tag.end()

        new_prompt += rendered_prompt[last_index:]

        if replace_image_placeholders_as:
            image_list = []
            for image_tag in image_pattern.finditer(new_prompt):
                image_name = image_tag.group(2)
                image_list.append(image_dict[image_name])
            new_prompt = re.sub(
                image_pattern, replace_image_placeholders_as, new_prompt
            )

            return new_prompt, image_list
        else:
            return new_prompt, image_dict


def load_template(template_path: str) -> str:
    """
    Load a Jinja2 template from the specified path within the installed package.

    :param template_path: Path to the Jinja2 template (relative to the package).
    :return: The template content as a string.
    """
    base_path = os.path.join(os.path.dirname(__file__), "templates")
    full_path = os.path.join(base_path, template_path)
    if not os.path.exists(full_path):
        available_templates = os.listdir(base_path)
        raise FileNotFoundError(
            f"Template file not found: {full_path}. Available templates: {available_templates}"
        )
    with open(full_path, "r", encoding="utf-8") as file:
        return file.read()


def create_template(template_str: str) -> Jinja2Template:
    """
    Create a Jinja2 template from the provided template string.

    :param template_str: The Jinja2 template content as a string.
    :return: A Jinja2 Template object.
    """
    env = Environment(undefined=StrictUndefined)
    env.filters["json_loads"] = json.loads
    return env.from_string(template_str)


def render_block(template: Jinja2Template, block_name: str, context: dict) -> str:
    """
    Render a specific block from a Jinja2 template.

    :param template: The Jinja2 Template object.
    :param block_name: The name of the block to render.
    :param context: The context to render the block with.
    :return: The rendered block as a string.
    """
    block = template.blocks[block_name]
    return "".join(block(template.new_context(context)))
