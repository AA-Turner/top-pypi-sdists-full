import asyncio
from collections.abc import Callable
from typing import List, Dict, Any, Optional, Tuple
import re
import json
import yaml
from pathlib import Path
import pandas as pd
from ..interfaces.powerpoint import PowerPointClient
from .flow import FlowComponent
from ..exceptions import DataNotFound


class PowerPointSlide(FlowComponent, PowerPointClient):
    """
    PowerPointSlide

    Overview:
        This component dynamically generates PowerPoint slides from a Pandas DataFrame and a .pptx template.
        It supports multiple custom modes (e.g., `single`, `double`, `retailer_view`, `overview_3up`, etc.)
        defined declaratively via a YAML configuration. Each mode specifies the layout and number of images per slide.

        You can name your modes arbitrarily — e.g., `single`, `double`, `quadruple`, `1x1`, `retailer_block`, etc.
        The logic does not assume or enforce fixed names. What matters is that each mode entry in `mode_content`
        defines a valid layout index and list of image placeholders.

        The component intelligently splits grouped rows into chunks based on the selected mode’s image capacity.
        If there are leftover rows that don’t fill a full chunk, the component will automatically fall back to
        another mode with fewer images, based on availability.

    Configuration Parameters (YAML):

    :widths: auto

    | template_path       |   Yes    | Absolute path to the `.pptx` PowerPoint template file.          |
    | output_file_path    |   Yes    | Output path where the final `.pptx` will be saved.              |
    | mode                |   Yes    | Primary mode to use (e.g., `double`, `retailer_block`, etc.)    |
    |                     |          | Controls the layout and chunking logic for slides.              |
    | mode_content        |   Yes    | Either a dict of modes, or a dict with key `file` pointing to a |
    |                     |          | `.yaml` or `.json` file containing the full mode structure.     |


    Variable Masking:
        Text and image fields in the YAML configuration can embed dynamic variables using curly-brace syntax.
        These placeholders are automatically replaced at runtime using each row's values from the DataFrame.

        Example:
            text: "{retailer} #{location_code}, {city}, {state_code}"
            → becomes: "Target #1234, Miami, FL"

        Missing columns will leave the placeholder unresolved (e.g., `{missing_key}`).

    Text and Image Rendering:
        Each `images:` block must define:
            - an image placeholder name
            - a `scale_factor`
            - a `path` (can include variable masks)
            - an optional nested `text:` block:
                - `placeholder_id`: text placeholder where the caption will be rendered
                - `text`: masked string
                - plus optional formatting: `font_size`, `font_color`, `bold`, etc.

        Text content shared across the slide (like headers) is defined in `text_content:`
        and rendered using the first row in the chunk.

    Grouping and Fallback Logic:
        - If `group_by` is defined, rows will be grouped accordingly.
        - Each group is divided into chunks of size N, where N = number of images in the selected mode.
        - Leftover rows that don’t fill a full slide are rendered using another mode that supports
          exactly the number of remaining images.
        - The fallback is automatically selected by checking all other modes and picking the one
          with the largest number of images ≤ remaining.

    Example mode_content (YAML snippet):

    Returns:
        str: Absolute path to the saved PowerPoint presentation file.

    Raises:
        DataNotFound: If the DataFrame input is empty or not provided.
        ValueError: If no suitable fallback layout is available for remaining records in a group.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          mode: double
          mode_content:
          # file: "slides_mode_content.yaml" (Optional, excludes following mode declarations)
          single:
          default_master_index: 0
          default_layout_index: 1
          text_content:
          - "Text Placeholder 3":
          text: "{retailer} | "
          - "Text Placeholder 3":
          text: "{category}"
          font_size: 24
          font_color: "808080"
          bold: False
          images:
          - "Picture Placeholder 1":
          scale_factor: 0.32 (optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 2"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          double:
          group_by: ["retailer", "category"]
          default_master_index: 0
          default_layout_index: 2
          text_content:
          - "Text Placeholder 5":
          text: "{retailer} | "
          - "Text Placeholder 5":
          text: "{category}"
          font_size: 24
          font_color: "808080"
          bold: False
          images:
          - "Picture Placeholder 2":
          scale_factor: 0.32 (optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 1"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          - "Picture Placeholder 3":
          scale_factor: 0.32 (optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 4"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          triple:
          group_by: ["retailer", "category"]
          default_master_index: 0
          default_layout_index: 3
          text_content:
          - "Text Placeholder 5":
          text: "{retailer} | "
          - "Text Placeholder 5":
          text: "{category}"
          font_size: 24
          font_color: "808080"
          bold: False
          images:
          - "Picture Placeholder 2":
          scale_factor: 0.32 (optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 1"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          - "Picture Placeholder 3":
          scale_factor: 0.32(optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 4"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          - "Picture Placeholder 6":
          scale_factor: 0.32(optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 7"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          quadruple:
          group_by: ["retailer", "category"]
          default_master_index: 0
          default_layout_index: 4
          text_content:
          - "Text Placeholder 5":
          text: "{retailer} | "
          - "Text Placeholder 5":
          text: "{category}"
          font_size: 24
          font_color: "808080"
          bold: False
          images:
          - "Picture Placeholder 2":
          scale_factor: 0.32(optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 1"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          - "Picture Placeholder 3":
          scale_factor: 0.32(optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 4"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          - "Picture Placeholder 6":
          scale_factor: 0.32(optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 8"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          - "Picture Placeholder 7":
          scale_factor: 0.32(optional)
          path: "{file_path}"
          # data: "{file_data}" (optional, excludes using path)
          text:
          placeholder_id: "Text Placeholder 9"
          text: "{retailer} #{location_code}, {city}, {state_code}"

          retailer_4up:
          default_layout_index: 4
          ...
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.mode: Optional[str] = kwargs.get("mode", 'double')
        self.template_path: Optional[Path] = None
        self.output_file_path: Optional[Path] = None
        self.mode_content: Optional[Dict[str, Any]] = None
        # Internal attributes
        self.all_modes: Dict[str, Any] = {}
        self.current_mode: Dict[str, Any] = {}
        self.slide_contents: List[Dict[str, Any]] = []
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        # Validate required base configuration attributes
        required_fields = ['template_path', 'output_file_path', 'mode', 'mode_content']
        for field in required_fields:
            if not getattr(self, field, None):
                raise ValueError(f"Missing required parameter: `{field}`")

        if not self.previous or self.input.empty:
            raise DataNotFound("No Data Provided to create slides from.")

        # Validate template path
        self.template_path = Path(self.template_path).resolve()
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found at: {self.template_path}")

        # Validate output file path
        self.output_file_path = self.mask_replacement(self.output_file_path)
        self.output_file_path = Path(self.output_file_path).resolve()
        self.output_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.output_file_path.parent.exists():
            raise FileNotFoundError(
                f"Output directory not found at: {self.output_file_path.parent}"
            )

        # Load external YAML/JSON if mode_content is a file reference
        if "file" in self.mode_content:
            file_path = self._taskstore.get_path().joinpath(self._program, self.mode_content["file"])

            if not file_path.exists():
                raise FileNotFoundError(f"mode_content file not found at: {file_path}")

            self.mode_content = self._parse_file(file_path)

        # Now validate that the mode exists inside mode_content
        if self.mode not in self.mode_content:
            raise ValueError(f"Mode '{self.mode}' not found in `mode_content` configuration.")

        # Assign parsed configuration
        self.all_modes = self.mode_content
        self.current_mode = self.all_modes[self.mode]
        self.data = self.input

        # Generate structured slide content
        self.slide_contents = self._parse_slide_contents(self.data)

    async def run(self):
        result_file_path = self.create_presentation_from_template(
            template_path=self.template_path,
            slide_contents=self.slide_contents,
            file_path=self.output_file_path,
            default_master_index=self.current_mode.get("default_master_index", 0),
            default_layout_index=self.current_mode.get("default_layout_index", 1),
        )
        self._result = result_file_path
        self.add_metric("Slides Result Path", f"{self._result!s}")
        # Please return the number of slides if you need a metric.
        # self.add_metric("# of Slides created", len(prs.slides))
        return self._result

    def _parse_file(self, file_path: Path) -> dict:
        """
        Load a file (YAML, JSON, or TOML) and return its parsed content as a dictionary.

        Args:
            file_path (Path): Path to the external config file.

        Returns:
            dict: Parsed content.

        Raises:
            ValueError: If the file extension is unsupported.
        """
        with file_path.open("r", encoding="utf-8") as f:
            if file_path.suffix in [".yaml", ".yml"]:
                return yaml.safe_load(f)
            if file_path.suffix == ".json":
                return json.load(f)
            raise ValueError(f"Unsupported mode_content file type: {file_path.suffix}")

    async def close(self):
        pass

    def _parse_slide_contents(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        def resolve_template(template: str, row: Dict[str, Any]) -> Any:
            """
            If template is a plain key like "{file_path}", return row['file_path'] as-is,
            which may be a BytesIO. Otherwise, perform full substitution and return a string.
            """
            # Direct match for single variable placeholder only
            match = re.fullmatch(r"\{(\w+)\}", template)
            if match:
                key = match.group(1)
                return row.get(key, f"{{{key}}}")

            # Generic substitution for text templates
            return re.sub(r"\{(\w+)\}", lambda m: str(row.get(m.group(1), f"{{{m.group(1)}}}")), template)

        def resolve_image_entry(row: Dict[str, Any], entry: Dict[str, Any]) \
                -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
            image_conf: Dict[str, Any] = {}
            text_conf: Optional[Dict[str, Any]] = None

            for placeholder_id, props in entry.items():
                for key, val in props.items():
                    if key == "text" and isinstance(val, dict):
                        pid = val["placeholder_id"]
                        text_conf = {
                            pid: {
                                k: resolve_template(v, row)
                                for k, v in val.items()
                                if k != "placeholder_id"
                            }
                        }
                    else:
                        image_conf[key] = resolve_template(val, row) if isinstance(val, str) else val
                image_conf["placeholder_id"] = placeholder_id

            return image_conf, text_conf

        slides: List[Dict[str, Any]] = []
        mode_cfg = self.current_mode
        primary_image_count = len(mode_cfg.get("images", []))

        # Map number of images per mode
        image_mode_map = {
            len(cfg.get("images", [])): cfg
            for _, cfg in self.all_modes.items()
        }

        group_keys = mode_cfg.get("group_by", [])
        groups = data.groupby(group_keys) if group_keys else [(None, data)]

        for _, df_group in groups:
            records = df_group.to_dict(orient="records")
            idx = 0
            total = len(records)

            # Always start with the user-selected mode
            while idx < total:
                remaining = total - idx

                # For single mode, always use the selected mode without fallback
                if self.mode == "single":
                    sub_cfg = mode_cfg
                    chunk_size = 1
                else:
                    # For other modes, use the original logic with fallback
                    if idx == 0 and remaining >= primary_image_count:
                        sub_cfg = mode_cfg
                        chunk_size = primary_image_count
                    else:
                        # For the remaining, find best fallback that fits
                        possible_sizes = sorted([n for n in image_mode_map if n <= remaining], reverse=True)
                        if not possible_sizes:
                            raise ValueError(f"No fallback mode defined for remaining chunk size {remaining}")
                        chunk_size = possible_sizes[0]
                        sub_cfg = image_mode_map[chunk_size]

                slide = {
                    "master_index": sub_cfg.get("default_master_index", 0),
                    "layout_index": sub_cfg.get("default_layout_index", 0),
                    "text_content": [],
                    "image": []
                }

                row0 = records[idx]
                for txt in sub_cfg.get("text_content", []):
                    for pid, props in txt.items():
                        resolved = {
                            k: resolve_template(v, row0) if isinstance(v, str) else v
                            for k, v in props.items()
                        }
                        slide["text_content"].append({pid: resolved})

                # For single mode, only use the first image configuration
                if self.mode == "single":
                    if sub_cfg.get("images"):
                        img_conf, txt_conf = resolve_image_entry(records[idx], sub_cfg["images"][0])
                        slide["image"].append(img_conf)
                        if txt_conf:
                            slide["text_content"].append(txt_conf)
                else:
                    # Original logic for other modes
                    for j, img_entry in enumerate(sub_cfg["images"]):
                        if idx + j >= total:
                            break
                        img_conf, txt_conf = resolve_image_entry(records[idx + j], img_entry)
                        slide["image"].append(img_conf)
                        if txt_conf:
                            slide["text_content"].append(txt_conf)

                slides.append(slide)
                idx += chunk_size

        return slides
