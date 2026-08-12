from typing import Any, Optional


class AlternativeIDParser:
    """ALTERNATIVE-ID, which the schema allows on every identified element.

    The element is a wrapper around a single self-closed
    <ALTERNATIVE-ID IDENTIFIER="..."/>, so its whole content is one identifier:

        <ALTERNATIVE-ID>
          <ALTERNATIVE-ID IDENTIFIER="ALT_ID"/>
        </ALTERNATIVE-ID>
    """

    @staticmethod
    def parse(xml_node: Any) -> Optional[str]:
        xml_wrapper = xml_node.find("ALTERNATIVE-ID")
        if xml_wrapper is None:
            return None
        xml_inner = xml_wrapper.find("ALTERNATIVE-ID")
        if xml_inner is None:
            # The schema permits an empty wrapper. It carries no identifier, so
            # there is nothing to model and the empty element is not preserved.
            return None
        # Bound to a typed local: xml nodes are Any, and returning that directly
        # trips mypy --strict's no-any-return.
        identifier: str = xml_inner.attrib["IDENTIFIER"]
        return identifier

    @staticmethod
    def unparse(alternative_id: Optional[str], indent: str) -> str:
        if alternative_id is None:
            return ""
        return (
            f"{indent}<ALTERNATIVE-ID>\n"
            f'{indent}  <ALTERNATIVE-ID IDENTIFIER="{alternative_id}"/>\n'
            f"{indent}</ALTERNATIVE-ID>\n"
        )
