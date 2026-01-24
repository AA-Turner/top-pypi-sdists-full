import json
from contentstack_utils.helper.converter import convert_style
from contentstack_utils.helper.metadata import Metadata
from contentstack_utils.helper.node_to_html import NodeToHtml
from contentstack_utils.render.options import Options


class Automate:

    @staticmethod
    def _str_from_embed_items(metadata, entry, option):
        if isinstance(entry, list):
            for node in entry:
                uid = node['node']['uid']
                if uid == metadata.get_item_uid:
                    return option.render_options(node['node'], metadata)
        elif isinstance(entry, dict) and '_embedded_items' in entry:
            items = entry['_embedded_items'].keys()
            for item in items:
                items_array = entry['_embedded_items'][item]
                content = Automate._find_embedded_entry(items_array, metadata)
                if content is not None:
                    return option.render_options(content, metadata)
        else:
            node_style = entry['type']
            def call(children):
                    return Automate._raw_processing(children, entry, option)
            
            return option.render_node(node_style, entry, callback=call)
        return ''

    @staticmethod
    def _get_embedded_keys(entry, key_path, option: Options, render_callback):
        if '_embedded_items' in entry:
            if key_path is not None:
                for path in key_path:
                    Automate._find_embed_keys(entry, path, option, render_callback)
            else:
                _embedded_items = entry['_embedded_items']
                available_keys: list = _embedded_items.keys()
                for path in available_keys:
                    Automate._find_embed_keys(entry, path, option, render_callback)

    @staticmethod
    def _find_embed_keys(entry, path, option: Options, render_callback):
        keys = path.split('.')
        Automate._get_content(keys, entry, option, render_callback)

    @staticmethod
    def _get_content(keys_array, entry, option: Options, render_callback):
        if keys_array is not None and len(keys_array) > 0:
            key = keys_array[0]
            if len(keys_array) == 1 and keys_array[0] in entry:
                var_content = entry[key]
                if isinstance(var_content, (list, str, dict)):
                    entry[key] = render_callback(var_content, entry, option)
            else:
                keys_array.remove(key)
                if key in entry and isinstance(entry[key], dict):
                    Automate._get_content(keys_array, entry[key], option, render_callback)
                elif key in entry and isinstance(entry[key], list):
                    list_json = entry[key]
                    for node in list_json:
                        Automate._get_content(keys_array, node, option, render_callback)

    @staticmethod
    def is_json(self: object) -> bool:
        try:
            json.dumps(self)
            return True
        except ValueError:
            return False

    @staticmethod
    def find_embed_keys(entry, paths, option: Options, render_callback):
        Automate.get_content(paths, entry, option, render_callback)

    @staticmethod
    def get_content(keys_array, entry, option: Options, render_callback):
        if keys_array is not None and len(keys_array) > 0:
            key = keys_array[0]
            if len(keys_array) == 1 and keys_array[0] in entry:
                var_content = entry[key]
                if isinstance(var_content, (list, str, dict)):
                    entry[key] = render_callback(var_content, entry, option)
                else:
                    keys_array.remove(key)
                    if key in entry and isinstance(entry[key], dict):
                        Automate.get_content(keys_array, entry[key], option, render_callback)
                    elif key in entry and isinstance(entry[key], list):
                        list_json = entry[key]
                        for node in list_json:
                            Automate.get_content(keys_array, node, option, render_callback)

    @staticmethod
    def _enumerate_content(content, entry, option):
        if len(content) > 0:
            if isinstance(content, list):
                array_content = []
                for item in content:
                    result = Automate._enumerate_content(item, entry, option)
                    array_content.append(result)
                return array_content
            if isinstance(content, dict):
                content_entry = content[entry]
                if isinstance(content_entry, dict):
                    if 'type' and 'children' in content_entry:
                        if content_entry['type']:
                            return Automate._raw_processing(content_entry['children'], entry, option)
                elif isinstance(content_entry, list):
                    for entry_item in content_entry:
                        if 'type' and 'children' in entry_item:
                            if entry_item['type']:
                                return Automate._raw_processing(entry_item['children'], entry, option)

        return ''

    @staticmethod
    def _raw_processing(children, entry, option):
        array_container = []
        for item in children:
            if isinstance(item, dict):
                array_container.append(Automate._extract_keys(item, entry, option))
        temp = ''.join(array_container)
        return temp

    @staticmethod
    def _extract_keys(item, entry, option: Options):
        if 'type' not in item.keys() and 'text' in item.keys():
            return NodeToHtml.text_node_to_html(item, option)

        elif 'type' in item.keys():
            node_style = item['type']
            if node_style == 'reference':
                metadata = Automate._return_metadata(item, node_style)
                return Automate._str_from_embed_items(metadata=metadata, entry=item, option=option)
            else:
                def call(children):
                    return Automate._raw_processing(children, entry, option)

                return option.render_node(node_style, item, callback=call)
        return ''

    @staticmethod
    def _find_embedded_entry(list_json: list, metadata: Metadata):
        for obj in list_json:
            if obj['uid'] == metadata.get_item_uid:
                return obj
        return None

    @staticmethod
    def _return_metadata(item, node_style):
        attr = item['attrs']
        text = Automate._get_child_text(item)
        style = convert_style(attr['display-type'])
        if attr['type'] == 'asset':
            return Metadata(text, node_style,
                            attr['asset-uid'],
                            'sys-asset',
                            style, '', '')
        else:
            return Metadata(text, node_style,
                            attr['entry-uid'],
                            attr['content-type-uid'],
                            style, '', '')

    @staticmethod
    def _get_child_text(item):
        text = ''
        if 'children' in item.keys() and len(item['children']) > 0:
            children = item['children']
            for child in children:
                if text in child.keys():
                    text = child['text']
                    break
        return text
