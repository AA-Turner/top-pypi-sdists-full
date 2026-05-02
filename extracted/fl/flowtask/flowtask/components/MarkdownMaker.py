import asyncio
from typing import Callable, Dict, List, Optional, Any
import pandas as pd
from .flow import FlowComponent
from ..exceptions import ComponentError, DataNotFound


class MarkdownMaker(FlowComponent):
    """
    MarkdownMaker

    Overview
        Build a Markdown snippet per product (row/dict) using fields produced by gorillashed parser
        (url, name, price, image, description_list, variants, features, faqs, specs, footprint_sqft).

    Parameters
        | output_column | No  | Name of the column/key where markdown will be stored. Default: "markdown" |
        | template      | No  | Custom template string. If not provided, a default gorillashed template is used. |

    Input
        Pandas DataFrame, list of dicts, or dict with product fields.

    Output
        Same structure plus a new markdown field/column.
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.output_column: str = kwargs.get("output_column", "markdown")
        self.template: Optional[str] = kwargs.get("template")
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.input is not None:
            self.data = self.input
        else:
            raise DataNotFound("MarkdownMaker: No input data received.")
        return True

    async def run(self):
        self._result = None
        data = self.data

        if isinstance(data, pd.DataFrame):
            df = data.copy()
            df[self.output_column] = df.apply(lambda row: self._render(row.to_dict()), axis=1)
            self._result = df
        elif isinstance(data, list):
            if not all(isinstance(item, dict) for item in data):
                raise ComponentError("MarkdownMaker: list input must contain dict items.")
            rendered = []
            for item in data:
                itm = dict(item)
                itm[self.output_column] = self._render(itm)
                rendered.append(itm)
            self._result = rendered
        elif isinstance(data, dict):
            result = dict(data)
            result[self.output_column] = self._render(result)
            self._result = result
        else:
            raise ComponentError(f"MarkdownMaker: Unsupported input type {type(data)}")

        if self._result is None:
            raise DataNotFound("MarkdownMaker: empty result")
        return self._result

    async def close(self):
        """No-op close to satisfy abstract interface."""
        return True

    def _render(self, product: Dict[str, Any]) -> str:
        """Render markdown with either a custom template or the default builder."""
        if self.template:
            try:
                return self.template.format(**product)
            except Exception as exc:  # pylint: disable=broad-except
                self._logger.error(f"MarkdownMaker template error: {exc}")
        return self._default_markdown(product)

    def _default_markdown(self, p: Dict[str, Any]) -> str:
        lines: List[str] = []

        def fmt(val: Any) -> str:
            return str(val) if val is not None else ""

        url = p.get("product_url") or p.get("url")
        name = p.get("product_name") or p.get("name")
        price = p.get("price")
        image = p.get("image_url")

        lines.append(f"url: {fmt(url)}")
        lines.append(f"Name: {fmt(name)}")
        if price is not None:
            try:
                lines.append(f"price: ${float(price):,.2f}")
            except Exception:  # pylint: disable=broad-except
                lines.append(f"price: {fmt(price)}")
        else:
            lines.append("price: ")
        lines.append(f"image: {fmt(image)}")
        lines.append("")  # spacer

        # Description bullets
        bullets = p.get("description_list") or []
        if bullets:
            lines.append("product bullet list:")
            for item in bullets:
                lines.append(f"* {item}")
            lines.append("")

        # Sizes from variants
        variants = p.get("product_variants") or p.get("variants") or []
        sizes = []
        for var in variants:
            size_val = var.get("public_title") or var.get("title") or var.get("option1")
            if size_val:
                sizes.append(str(size_val))
        if sizes:
            lines.append("sizes:")
            lines.append(f"* {', '.join(sorted(set(sizes)))}")
            lines.append("")

        # Features
        features = p.get("features") or []
        if features:
            lines.append("Features:")
            for feat in features:
                title = feat.get("title")
                subtitle = feat.get("subtitle")
                head = f"- **{title}**" if title else "-"
                if subtitle:
                    head += f": {subtitle}"
                lines.append(head)
                for b in feat.get("bullets") or []:
                    lines.append(f"  * {b}")
            lines.append("")

        # FAQ
        faqs = p.get("faqs") or []
        if faqs:
            lines.append("FAQ:")
            for item in faqs:
                q = item.get("question")
                a = item.get("answer")
                if q:
                    lines.append(f"- Q: {q}")
                if a:
                    lines.append(f"  A: {a}")
            lines.append("")

        # Specs as tables
        specs = p.get("specs") or {}
        if specs:
            lines.append("Specs:")
            for section, items in specs.items():
                lines.append(f"**{section}**")
                lines.append("| Field | Value |")
                lines.append("| --- | --- |")
                for key, val in items.items():
                    lines.append(f"| {key} | {val} |")
                lines.append("")

        # Footprint
        if p.get("footprint_sqft") is not None:
            lines.append(f"Footprint (sqft): {p.get('footprint_sqft')}")

        return "\n".join(lines).strip()
