from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.filter(name='search_field_display')
def search_field_display(search_field):
    if search_field is not None:
        return search_field.replace('__', ' -> ').replace('_', ' ').title()
    return ''


@register.filter(name='generate_query_string')
def generate_query_string(search_field, change_list_obj):
    NON_SEARCH_PARAMS = ['p', 'o']
    search_fields = change_list_obj.search_fields

    return f'?{search_field}__contains='
    """
    params = []
    for param, value in change_list_obj.params.items():
        params.append(f'{param}={value}')
    if params:
        return '?' + '&'.join(params)
    return ''
    """


@register.simple_tag(name='render_search_field')
def render_search_field(search_field, change_list_obj):
    qs = generate_query_string(search_field, change_list_obj)
    sf = search_field_display(search_field)
    selected = ' selected="selected"' if search_field + '__contains' in change_list_obj.params.keys() else ''

    return mark_safe(f'<option value="{qs}"{selected}>{sf}</option>')


@register.simple_tag(name='render_search_value')
def render_search_value(change_list_obj):
    for param, value in change_list_obj.params.items():
        if '__contains' in param:
            return value

    return ''
