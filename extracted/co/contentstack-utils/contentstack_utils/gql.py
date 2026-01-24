from contentstack_utils import Utils
from contentstack_utils.automate import Automate
from contentstack_utils.render.options import Options


class GQL(Automate):

    @staticmethod
    def json_to_html(gql_entry: dict, paths: list, option: Options):
        if not Automate.is_json(gql_entry):
            raise FileNotFoundError("Can't process invalid object")
        if len(paths) > 0:
            for path in paths:
                Automate.find_embed_keys(gql_entry, path, option, render_callback=GQL._json_matcher)
                return Automate._enumerate_content(gql_entry, path, option)

    @staticmethod
    def __filter_content(content_dict):
        embedded_items = None
        if content_dict is not None and 'embedded_itemsConnection' in content_dict:
            embedded_connection = content_dict['embedded_itemsConnection']
            if 'edges' in embedded_connection:
                embedded_items = embedded_connection['edges']
        return embedded_items

    @staticmethod
    def _json_matcher(content_dict, entry, option):
        embedded_items = GQL.__filter_content(content_dict)
        if 'json' in content_dict:
            json = content_dict['json']
            if isinstance(json, dict):
                return Automate._enumerate_content(json, entry=embedded_items, option=option)
            elif isinstance(json, list):
                json_container = []
                for item in json:
                    json_container.append(Automate._enumerate_content(item, entry=embedded_items, option=option))
                return json_container
