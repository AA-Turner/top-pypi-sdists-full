# pylint: disable=missing-function-docstring

import json
from typing import Any, Dict, List, Optional, Union

from lxml import etree

from contentstack_utils.automate import Automate
from contentstack_utils.entry_editable import addEditableTags as _addEditableTags
from contentstack_utils.entry_editable import addTags as _addTags
from contentstack_utils.entry_editable import getTag as _getTag
from contentstack_utils.helper.converter import convert_style
from contentstack_utils.helper.metadata import Metadata
from contentstack_utils.render.options import Options


class Utils(Automate):
    # JS parity helpers (moved to `contentstack_utils/entry_editable.py`)
    @staticmethod
    def addTags(  # pylint: disable=invalid-name
        entry: dict,
        contentTypeUid: str,
        tagsAsObject: Optional[bool] = None,
        locale: str = "en-us",
        options: Optional[dict] = None,
        **kwargs,
    ) -> None:
        # Support pythonic kwarg name too (backward compatibility with earlier port).
        if tagsAsObject is None and "tags_as_object" in kwargs:
            tagsAsObject = bool(kwargs["tags_as_object"])
        if tagsAsObject is None:
            tagsAsObject = False
        return _addTags(entry, contentTypeUid, tagsAsObject, locale, options)

    @staticmethod
    def addEditableTags(  # pylint: disable=invalid-name
        entry: dict,
        contentTypeUid: str,
        tagsAsObject: Optional[bool] = None,
        locale: str = "en-us",
        options: Optional[dict] = None,
        **kwargs,
    ) -> None:
        if tagsAsObject is None and "tags_as_object" in kwargs:
            tagsAsObject = bool(kwargs["tags_as_object"])
        if tagsAsObject is None:
            tagsAsObject = False
        return _addEditableTags(entry, contentTypeUid, tagsAsObject, locale, options)

    @staticmethod
    def getTag(  # pylint: disable=invalid-name
        content: Any,
        prefix: str,
        tagsAsObject: bool,
        locale: str,
        appliedVariants: Optional[dict],
        shouldApplyVariant: bool,
        metaKey: str = "",
    ) -> Dict[str, Any]:
        # Keep JS argument names for parity.
        return _getTag(content, prefix, tagsAsObject, locale, appliedVariants, shouldApplyVariant, metaKey)

    # Pythonic aliases
    add_tags = addTags
    get_tags = getTag
    get_tag = getTag

    @staticmethod
    def _variants_map_from_entry(entry: dict) -> dict:
        publish_details = entry.get("publish_details")
        if not isinstance(publish_details, dict):
            return {}
        raw = publish_details.get("variants")
        return raw if isinstance(raw, dict) else {}

    @staticmethod
    def _aliases_from_variants_map(variants_map: dict) -> List[str]:
        aliases: List[str] = []
        for _variant_uid, value in variants_map.items():
            if not isinstance(value, dict):
                continue
            alias = value.get("alias")
            if alias is None:
                continue
            alias_str = str(alias).strip()
            if alias_str:
                aliases.append(alias_str)
        return aliases

    @staticmethod
    def _variant_aliases_for_entry(entry: dict, content_type_uid: str = "") -> Dict[str, Any]:
        if entry is None:
            raise ValueError("entry cannot be None")
        if not isinstance(entry, dict):
            raise TypeError("entry must be a dict")
        uid = entry.get("uid")
        if uid is None or (isinstance(uid, str) and uid.strip() == ""):
            raise ValueError("entry must contain a non-empty uid")
        entry_uid = str(uid)
        ct = entry.get("_content_type_uid")
        if ct is None or ct == "":
            ct = content_type_uid or ""
        contenttype_uid = "" if ct is None else str(ct)
        variants_map = Utils._variants_map_from_entry(entry)
        aliases = Utils._aliases_from_variants_map(variants_map)
        return {
            "entry_uid": entry_uid,
            "contenttype_uid": contenttype_uid,
            "variants": aliases,
        }

    @staticmethod
    def get_variant_aliases(
        entry_or_entries: Union[dict, List[dict]],
        content_type_uid: str = "",
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Extract variant aliases from a CDA entry (or list of entries).

        The entry must have been fetched with ``x-cs-variant-uid`` set to variant
        aliases (not UIDs) for ``publish_details.variants`` to be present.

        :param entry_or_entries: A single entry dict, or a list of entry dicts.
        :param content_type_uid: Used when ``entry._content_type_uid`` is absent;
            ignored when ``entry_or_entries`` is a list (each entry supplies its own).
        :raises ValueError: if ``entry_or_entries`` is None, an entry is None, or an
            entry has no non-empty ``uid``.
        :raises TypeError: if a single entry is not a dict, or a list is expected but
            another type was passed for the multi-entry overload.
        """
        if entry_or_entries is None:
            raise ValueError("entry is required and cannot be None")
        if isinstance(entry_or_entries, list):
            return [Utils._variant_aliases_for_entry(e, "") for e in entry_or_entries]
        if isinstance(entry_or_entries, dict):
            return Utils._variant_aliases_for_entry(entry_or_entries, content_type_uid or "")
        raise TypeError("entry must be a dict or a list of dicts")

    @staticmethod
    def get_variant_metadata_tags(entries: List[dict]) -> Dict[str, str]:
        """
        Build a ``data-csvariants`` HTML data-attribute payload from entry objects.

        :param entries: List of CDA entry dicts (same shape as for multi-entry
            :meth:`get_variant_aliases`).
        :raises ValueError: if ``entries`` is None.
        :raises TypeError: if ``entries`` is not a list.
        """
        if entries is None:
            raise ValueError("entries is required and cannot be None")
        if not isinstance(entries, list):
            raise TypeError("entries must be a list")
        results = Utils.get_variant_aliases(entries)
        payload = json.dumps(results, separators=(",", ":"))
        return {"data-csvariants": payload}

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
