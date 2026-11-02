import base64
import unicodedata

from jinja2 import Environment, PackageLoader
from pkg_resources import resource_string


def html_report(markdown, title, links=[]):
    """"""
    environment = {}
    environment['title'] = title
    environment['raw_data'] = base64.b64encode(markdown.encode('utf-8')).decode('utf-8')
    environment.update({
        'custom_style': __style("custom.css"),
        'custom_script': __script("custom"),
        'bootstrap_style': __style("bootstrap.min.css"),
        'jquery_script': __script("jquery.min"),
        'bootstrap_script': __script("bootstrap.min"),
        'markdown_it_script': __script('markdown-it.min'),
        'links': links,
    })
    return render(None, 'report_html.tpl', environment)


def strip_control_characters(s):
    """Strip unicode control characters from a string."""
    return "".join(c for c in s if unicodedata.category(c) != "Cc")


def render(jinja_env, template_name, environment):
    jinja_env = jinja_env or Environment(loader=PackageLoader('mir', '.'))
    template = jinja_env.get_template(template_name)
    return template.render(**environment)



def __style(filename):
    resource = __load_resource(filename)
    return "<style>%s</style>" % resource


def __script(short_name):
    resource = __load_resource("%s.js" % short_name)
    return "<script>%s</script>" % resource


def __load_resource(name):
    return resource_string(
        __name__, name
    ).decode('UTF-8')
