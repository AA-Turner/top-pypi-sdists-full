"""Google Docs API request builder."""

from .parser import Paragraph, TextRun

# Heading style mapping
HEADING_STYLES = {
    1: "HEADING_1",
    2: "HEADING_2",
    3: "HEADING_3",
    4: "HEADING_4",
    5: "HEADING_5",
    6: "HEADING_6",
}


class DocsRequestBuilder:
    """Builds Google Docs API batchUpdate requests from parsed paragraphs."""

    def __init__(self, start_index: int = 1):
        self.insert_requests: list[dict] = []
        self.style_requests: list[dict] = []
        self.start_index = start_index
        self.current_index = start_index

    def build(self, paragraphs: list[Paragraph]) -> list[dict]:
        """Convert paragraphs to Docs API requests.

        Returns requests in the correct order:
        1. Insert text in reverse order (last paragraph first) at start_index
        2. Apply all styling after text is inserted
        """
        self.insert_requests = []
        self.style_requests = []
        self.current_index = self.start_index

        for para in paragraphs:
            self._add_paragraph(para)

        # Insert in reverse order so each insert at start_index pushes previous content down
        # Then apply styles (which reference the final positions)
        return list(reversed(self.insert_requests)) + self.style_requests

    def _add_paragraph(self, para: Paragraph) -> None:
        text_content = "".join(run.text for run in para.runs) + "\n"
        start_index = self.current_index

        # Insert text (all inserts happen at start_index, reversed later)
        self.insert_requests.append(
            {
                "insertText": {
                    "location": {"index": self.start_index},
                    "text": text_content,
                }
            }
        )

        # Apply run styles
        current_pos = start_index
        for run in para.runs:
            run_end = current_pos + len(run.text)
            self._apply_run_style(run, current_pos, run_end)
            current_pos = run_end

        para_end = start_index + len(text_content) - 1

        # Apply paragraph-level styling
        if para.heading_level > 0:
            self._apply_heading_style(para.heading_level, start_index, para_end + 1)

        if para.is_list_item:
            self._apply_list_style(para.list_type, start_index, para_end + 1)

        if para.is_code_block:
            self._apply_code_block_style(start_index, para_end)

        if para.is_blockquote:
            self._apply_blockquote_style(start_index, para_end + 1)

        self.current_index += len(text_content)

    def _apply_run_style(self, run: TextRun, start: int, end: int) -> None:
        """Apply text-level styling for a run."""
        if run.bold or run.italic or run.strikethrough or run.code:
            style: dict = {}
            fields: list[str] = []

            if run.bold:
                style["bold"] = True
                fields.append("bold")
            if run.italic:
                style["italic"] = True
                fields.append("italic")
            if run.strikethrough:
                style["strikethrough"] = True
                fields.append("strikethrough")
            if run.code:
                style["weightedFontFamily"] = {"fontFamily": "Courier New"}
                style["backgroundColor"] = {
                    "color": {"rgbColor": {"red": 0.95, "green": 0.95, "blue": 0.95}}
                }
                fields.extend(["weightedFontFamily", "backgroundColor"])

            self.style_requests.append(
                {
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "textStyle": style,
                        "fields": ",".join(fields),
                    }
                }
            )

        if run.link:
            self.style_requests.append(
                {
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "textStyle": {"link": {"url": run.link}},
                        "fields": "link",
                    }
                }
            )

    def _apply_heading_style(self, level: int, start: int, end: int) -> None:
        self.style_requests.append(
            {
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": HEADING_STYLES[level]},
                    "fields": "namedStyleType",
                }
            }
        )

    def _apply_list_style(self, list_type: str, start: int, end: int) -> None:
        preset = "BULLET_DISC_CIRCLE_SQUARE" if list_type == "BULLET" else "NUMBERED_DECIMAL_NESTED"
        self.style_requests.append(
            {
                "createParagraphBullets": {
                    "range": {"startIndex": start, "endIndex": end},
                    "bulletPreset": preset,
                }
            }
        )

    def _apply_code_block_style(self, start: int, end: int) -> None:
        self.style_requests.append(
            {
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": "Courier New"},
                        "backgroundColor": {
                            "color": {"rgbColor": {"red": 0.95, "green": 0.95, "blue": 0.95}}
                        },
                    },
                    "fields": "weightedFontFamily,backgroundColor",
                }
            }
        )

    def _apply_blockquote_style(self, start: int, end: int) -> None:
        self.style_requests.append(
            {
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {
                        "indentFirstLine": {"magnitude": 36, "unit": "PT"},
                        "indentStart": {"magnitude": 36, "unit": "PT"},
                        "borderLeft": {
                            "color": {
                                "color": {"rgbColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}
                            },
                            "width": {"magnitude": 3, "unit": "PT"},
                            "padding": {"magnitude": 8, "unit": "PT"},
                            "dashStyle": "SOLID",
                        },
                    },
                    "fields": "indentFirstLine,indentStart,borderLeft",
                }
            }
        )
