# pylint: disable=missing-function-docstring

from lxml import etree

from contentstack_utils.automate import Automate
from contentstack_utils.helper.converter import convert_style
from contentstack_utils.helper.metadata import Metadata
from contentstack_utils.render.options import Options


class Utils(Automate):

    @staticmethod
    def render(entry_obj, key_path: list, option: Options):
        valid = Automate.is_json(entry_obj)
        if not valid:
            raise FileNotFoundError('Invalid file found')

        if isinstance(entry_obj, list):
            for entry in entry_obj:
                Utils.render(entry, key_path, option)

        if isinstance(entry_obj, dict):
            Automate._get_embedded_keys(entry_obj, key_path, option, render_callback=Utils.render_content)

    @staticmethod
    def render_content(rte_content, embed_obj: dict, option: Options) -> object:
        if isinstance(rte_content, str):
            return Utils.__get_embedded_objects(rte_content, embed_obj, option)
        elif isinstance(rte_content, list):
            render_callback = []
            for rte in rte_content:
                render_callback.append(Utils.render_content(rte, embed_obj, option))
            return render_callback
        return rte_content

    @staticmethod
    def __get_embedded_objects(html_doc, entry, option):
        import re
        document = f"<items>{html_doc}</items>"
        tag = etree.fromstring(document)
        html_doc = etree.tostring(tag).decode('utf-8')
        html_doc = re.sub('(?ms)<%s[^>]*>(.*)</%s>' % (tag.tag, tag.tag), '\\1', html_doc)
        elements = tag.xpath("//*[contains(@class, 'embedded-asset') or contains(@class, 'embedded-entry')]")
        metadata = Utils.__get_metadata(elements)
        string_content = Utils._str_from_embed_items(metadata=metadata, entry=entry, option=option)
        html_doc = html_doc.replace(metadata.outer_html, string_content)
        return html_doc

    @staticmethod
    def _str_from_embed_items(metadata, entry, option):
        if '_embedded_items' in entry:
            items = entry['_embedded_items'].keys()
            for item in items:
                items_array = entry['_embedded_items'][item]
                content = Automate._find_embedded_entry(items_array, metadata)
                if content is not None:
                    return option.render_options(content, metadata)
        return ''

    @staticmethod
    def __get_metadata(elements):
        for element in elements:
            content_type = None
            typeof = element.attrib['type']
            if typeof == 'asset':
                uid = element.attrib['data-sys-asset-uid']
            else:
                uid = element.attrib['data-sys-entry-uid']
                content_type = element.attrib['data-sys-content-type-uid']
            style = element.attrib['sys-style-type']
            outer_html = etree.tostring(element).decode('utf-8')
            attributes = element.attrib
            style = convert_style(style)
            metadata = Metadata(element.text, typeof, uid, content_type, style, outer_html, attributes)
            return metadata

    ####################################################
    #                   SUPERCHARGED                   #
    ####################################################

    @staticmethod
    def json_to_html(entry_obj, key_path: list, option: Options):
        if not Automate.is_json(entry_obj):
            raise FileNotFoundError('Could not process invalid content')
        if isinstance(entry_obj, list):
            for entry in entry_obj:
                return Utils.json_to_html(entry, key_path, option)
        if isinstance(entry_obj, dict):
            if key_path is not None:
                for path in key_path:
                    render_callback = Automate._enumerate_content(entry_obj, path, option)
                    # Automate._find_embed_keys(entry_obj, path, option, render_callback) This method used in GQL class.
            return render_callback
