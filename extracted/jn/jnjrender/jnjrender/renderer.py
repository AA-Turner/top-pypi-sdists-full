# jnjrender/renderer.py

from jinja2 import Template

def render_jinja_to_yaml(jinja_content, variables):
    template = Template(jinja_content)
    rendered_output = template.render(variables)
    return rendered_output
