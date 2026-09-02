from typing import Any, Dict, List, Union
from collections.abc import Callable
import asyncio
import json
import pandas as pd
from io import BytesIO
from pathlib import Path
from PIL import Image
from asyncdb import AsyncDB
from querysource.conf import default_dsn
import re
from parrot.clients.google import GoogleGenAIClient
from parrot.models.google import GoogleModel
from parrot_pipelines.models import PlanogramConfig, EndcapGeometry
from ..interfaces.flow import FlowComponent
from ..interfaces.pipelines.parrot import AIPipeline
from ..exceptions import ComponentError, ConfigError

_MAX_REF_IMAGES_PER_KEY = 5
_TABLE_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_.]*$')


class PlanogramCompliance(AIPipeline, FlowComponent):
    """
    PlanogramCompliance

    Overview:
        FlowTask component for executing planogram compliance analysis using AI pipelines.
        This component extends FlowComponent and AIPipeline to process retail shelf images
        and verify compliance with planogram specifications.

    Properties:
        planogram_config (dict): Configuration defining the planogram specifications including
            brand, category, aisle info, shelf requirements, and compliance thresholds.
        reference_images_path (str|List[str]): Path(s) to reference product images for identification.
        image_column (str): Name of the DataFrame column containing BytesIO image data.
        llm_config (dict): Configuration for the LLM to use in the pipeline.
        detection_model (str): YOLO model to use for object detection.
        confidence_threshold (float): Confidence threshold for object detection.
        overlay_output_path (str): Base path for saving overlay images.

    Returns:
        DataFrame: Enhanced with new columns:
            - overall_compliance_score: Float compliance score (0-1)
            - overall_compliant: Boolean compliance status
            - compliance_analysis_markdown: Detailed markdown report
            - compliance_analysis_json: JSON structured results
            - overlay_image: PIL.Image of the analyzed image with overlays

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PlanogramCompliance:
          # attributes here
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
        """Initialize the PlanogramCompliance component.

        Args:
            loop: Optional event loop.
            job: Optional job callable.
            stat: Optional stat callable.
            **kwargs: Component configuration. Recognized keys:
                name (str): Planogram configuration name to load from DB.
                planogram_config_table (str): Fully-qualified table name for
                    planogram configurations (e.g. ``"myschema.planogram_configs"``).
                    Required — no default.
                planogram_type (str): Composable type selector (e.g.
                    ``"product_on_shelves"``, ``"ink_wall"``). YAML value
                    acts as emergency override over the DB value. Defaults
                    to ``"product_on_shelves"``.
                reference_images (dict): Mapping of label → image path.
                image_column (str): DataFrame column with BytesIO image data.
                id_column (str): DataFrame column used as per-row identifier.
                llm_config (dict): LLM client configuration overrides.
                detection_model (str): YOLO model filename.
                confidence_threshold (float): Detection confidence threshold.
                overlay_output_path (str): Sub-directory for overlay images.
        """
        # Planogram-specific configuration
        self._planogram_name: str = kwargs.get('name', None)
        # planogram_type: YAML kwarg acts as emergency override over the DB value.
        # Fallback chain: DB result → YAML kwarg → default "product_on_shelves".
        self._planogram_type: str = kwargs.get('planogram_type', 'product_on_shelves')
        _table = kwargs.get('planogram_config_table')
        if _table and not _TABLE_RE.match(_table):
            raise ConfigError(
                "Invalid planogram_config_table name: %r" % _table
            )
        self._planogram_config_table: str = _table
        self.planogram_config: PlanogramConfig = None
        self.reference_images: Dict[str, Path] = kwargs.get(
            'reference_images', {}
        )
        self.image_column: str = kwargs.get(
            'image_column', 'image_data'
        )
        # per-row ID:
        self._id_column: str = kwargs.get(
            'id_column', 'photo_id'
        )

        # Pipeline configuration
        self.llm_config: Dict[str, Any] = kwargs.get('llm_config', {})
        self.detection_model: str = kwargs.get(
            'detection_model', 'yolo11l.pt'
        )
        self.confidence_threshold: float = kwargs.get(
            'confidence_threshold',
            0.15  # Lower confidence threshold for better detection
        )
        self.overlay_output: str = kwargs.get('overlay_output_path', 'identified')

        # Safe default so get_planogram_config() never raises AttributeError
        # before start() is called.
        self._reference_images: list = []

        # Set pipeline name for AIPipeline
        kwargs['pipeline'] = 'planogram_compliance'

        # Initialize parent classes
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def get_planogram_config(self, reference_images: list = None) -> PlanogramConfig:
        """Retrieve and validate the planogram configuration."""
        if not self._planogram_name:
            raise ConfigError(
                "Planogram name is not specified"
            )
        if not self._planogram_config_table:
            raise ConfigError(
                "planogram_config_table is not specified"
            )
        planogram_query = f"SELECT * FROM {self._planogram_config_table} WHERE config_name = $1"
        planogram_config = None
        db = AsyncDB('pg', dsn=default_dsn)
        async with await db.connection() as conn:
            result = await conn.fetch_one(planogram_query, self._planogram_name)
            if not result:
                raise ConfigError(
                    f"Planogram configuration '{self._planogram_name}' not found"
                )
            # Convert each part of planogram_configuration to PlanogramConfig
            planogram_id = result['planogram_id']
            try:
                geometry = EndcapGeometry(
                    aspect_ratio=result['aspect_ratio'],
                    left_margin_ratio=result['left_margin_ratio'],
                    right_margin_ratio=result['right_margin_ratio'],
                    top_margin_ratio=result['top_margin_ratio'],
                    bottom_margin_ratio=result['bottom_margin_ratio'],
                    inter_shelf_padding=result['inter_shelf_padding'],
                    width_margin_percent=result['width_margin_percent'],
                    height_margin_percent=result['height_margin_percent'],
                    top_margin_percent=result['top_margin_percent'],
                    side_margin_percent=result['side_margin_percent'],
                )
            except Exception as e:
                raise ConfigError(
                    f"Invalid geometry configuration: {e}"
                )
            # extract the planogram_config:
            planogram_config = result['planogram_config']
            roi_detection_prompt = result.get('roi_detection_prompt', None)
            object_prompt = result.get('object_identification_prompt', None)
            self.confidence_threshold = result.get('confidence_threshold', self.confidence_threshold)
            self.detection_model = result.get('detection_model', self.detection_model)
            # Resolve planogram_type: DB value takes precedence, YAML kwarg is fallback.
            resolved_type: str = result.get('planogram_type', self._planogram_type)
            try:
                planogram_config = PlanogramConfig(
                    planogram_id=planogram_id,
                    config_name=self._planogram_name,
                    planogram_type=resolved_type,
                    planogram_config=planogram_config,
                    endcap_geometry=geometry,
                    roi_detection_prompt=roi_detection_prompt,
                    object_identification_prompt=object_prompt,
                    confidence_threshold=self.confidence_threshold,
                    detection_model=self.detection_model,
                    reference_images=reference_images or self._reference_images,
                )
                self._logger.debug('Planogram config loaded: %s', planogram_config)
            except Exception as e:
                raise ConfigError(
                    f"Invalid planogram configuration: {e}"
                )
        if not isinstance(planogram_config, PlanogramConfig):
            raise ConfigError(
                "Invalid planogram configuration format"
            )
        self._logger.notice(
            f"Successfully loaded planogram configuration: {self._planogram_name}"
        )
        return planogram_config

    async def start(self, **kwargs):
        """Initialize the component."""
        if self.previous:
            self.data = self.input

        # Storage Directory:
        self.directory = self._taskstore.get_path().joinpath(self._program)
        # The Store Directory is used for saving overlays and other outputs
        self.store_directory = self._filestore.get_directory('').joinpath('compliance')
        self.store_directory.mkdir(parents=True, exist_ok=True)
        self.overlay_output_path = self.store_directory.joinpath(self.overlay_output)
        # create directory if it doesn't exist
        self.overlay_output_path.mkdir(parents=True, exist_ok=True)

        # Validate DataFrame has required image column
        if self.image_column not in self.data.columns:
            raise ComponentError(
                f"Image column '{self.image_column}' not found in DataFrame"
            )

        # Prepare reference images list - convert to string paths as expected by pipeline
        self._reference_images = self._prepare_reference_images()

        # Initialize LLM for pipeline
        self._llm = self._initialize_llm()

        # Generate Planogram Configuration:
        self.planogram_config = await self.get_planogram_config(
            reference_images=self._reference_images
        )

        self._logger.info(
            f"PlanogramPipeline started with {len(self.data)} rows to process"
        )
        return True

    def _prepare_reference_images(self) -> dict:
        """Convert reference image paths to Path objects as expected by pipeline.

        Returns:
            dict: Mapping of label keys to single Path objects. When a directory
                is given, expands into ``{key}_0``, ``{key}_1``, … entries (max
                ``_MAX_REF_IMAGES_PER_KEY`` per key), one Path per entry.
        """
        reference_images = {}
        for key, image in self.reference_images.items():
            image = self.mask_replacement(image)
            image_path = self.directory.joinpath('images', image)
            if not image_path.exists():
                raise ComponentError(
                    "Reference image not found: %s" % image_path
                )
            elif image_path.is_dir():
                # Collect all supported image files across all extensions.
                found = []
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']:
                    found.extend(image_path.glob(ext))
                if not found:
                    raise ComponentError(
                        "No images found in directory: %s" % image_path
                    )
                for i, p in enumerate(sorted(found)[:_MAX_REF_IMAGES_PER_KEY]):
                    reference_images["%s_%d" % (key, i)] = p
            else:
                reference_images[key] = image_path
        return reference_images

    def _initialize_llm(self):
        """Initialize the LLM client based on configuration."""
        # Default LLM configuration
        default_config = {
            'model': GoogleModel.GEMINI_3_PRO_PREVIEW,
        }
        # Merge with user configuration
        final_config = {**default_config, **self.llm_config}
        return GoogleGenAIClient(**final_config)

    def _convert_bytes_to_pil(self, image_data: BytesIO) -> Image.Image:
        """Convert BytesIO image data to PIL Image."""
        try:
            if isinstance(image_data, BytesIO):
                image_data.seek(0)
                return Image.open(image_data)
            elif isinstance(image_data, bytes):
                return Image.open(BytesIO(image_data))
            else:
                raise ComponentError(
                    f"Unsupported image data type: {type(image_data)}"
                )
        except Exception as e:
            raise ComponentError(
                f"Failed to convert image data to PIL Image: {e}"
            ) from e

    def _create_markdown_report(self, result: Dict[str, Any], overlay_path: str = "") -> str:
        """Generate a markdown report from pipeline results."""
        md = []
        md.append("# Planogram Compliance Analysis")
        md.append("")

        # Overall compliance
        compliance_emoji = "✅" if result.get('overall_compliant', False) else "❌"
        md.append(f"## Overall Compliance: {compliance_emoji}")
        md.append(f"**Score:** {result.get('overall_compliance_score', 0):.1%}")
        md.append("")

        # Shelf-by-shelf results
        md.append("\n## SHELF-BY-SHELF RESULTS:")
        shelf_results = result.get('step3_compliance_results', [])

        for shelf_result in shelf_results:
            level = shelf_result.shelf_level.upper()
            status = "✅" if shelf_result.compliance_score >= 1.0 else "❌"
            missing_prods = getattr(shelf_result, 'missing_products', []) or []

            md.append(f"### {level} Shelf: {status}")
            md.append(f"- **Product Score:** {shelf_result.compliance_score:.1%}")
            md.append(f"- **Expected Products:** {', '.join(shelf_result.expected_products)}")
            md.append(f"- **Found Products:** {', '.join(shelf_result.found_products) or 'None'}")
            if missing_prods:
                md.append(f"- **Issues:** {', '.join(missing_prods)}")

            if hasattr(shelf_result, 'text_compliance_results') and shelf_result.text_compliance_results:
                md.append("- **Text Requirements:**")
                for text_result in shelf_result.text_compliance_results:
                    status_emoji = "✅" if text_result.found else "❌"
                    md.append(
                        f"  - {status_emoji} '{text_result.required_text}' (confidence: {text_result.confidence:.2f})"
                    )
                    if text_result.matched_features:
                        md.append(f"    - Matched: {text_result.matched_features}")
            md.append("")

        # Analysis artifacts
        md.append("Analysis Artifacts")
        if overlay_path:
            md.append(f"**Overlay Image:**")
            md.append(overlay_path)
        md.append("")
        md.append("*Report generated by AI-Parrot Planogram Compliance Pipeline*")

        return "\n".join(md)

    async def _process_dataframe_rows(
        self,
        df: pd.DataFrame,
        pipeline_method: str = 'run'
    ) -> List[Dict[str, Any]]:
        """
        Override the generic processing to use our specific pipeline execution logic.

        Args:
            df: DataFrame to process
            pipeline_method: Ignored for this implementation

        Returns:
            List of results from pipeline execution
        """
        results = []

        for idx, row in df.iterrows():
            result = await self._execute_pipeline_on_row(row, idx)
            results.append(result)

        return results

    async def _execute_pipeline_on_row(
        self,
        row: pd.Series,
        row_index: int
    ) -> Dict[str, Any]:
        """
        Execute the pipeline on a single DataFrame row.

        Args:
            row: pandas Series representing a row
            row_index: Index of the row being processed

        Returns:
            Dictionary containing pipeline results
        """
        try:
            # Convert BytesIO to PIL Image
            image_data = row[self.image_column]
            pil_image = self._convert_bytes_to_pil(image_data)

            # Initialize overlay_path - will be populated from pipeline result
            overlay_path = ""

            # Grab the photo ID to use as filename suffix in pipeline outputs.
            photo_id = row.get(self._id_column, row_index) if hasattr(row, 'get') else getattr(row, self._id_column, row_index)
        except Exception as e:
            self._logger.error(
                f"Error preparing data for row {row_index}: {e}"
            )
            return {
                'row_index': row_index,
            }
        try:
            # Execute pipeline (following the reference script pattern)
            result = await self._pipeline.run(
                image=pil_image,
                output_dir=str(self.overlay_output_path),
                image_id=str(photo_id),
            )

            # Serialize the result directly to JSON (handling non-serializable objects)
            json_report = json.dumps({
                'overall_compliance_score': result.get('overall_compliance_score', 0.0),
                'overall_compliant': result.get('overall_compliant', False),
                'step3_compliance_results': [
                    {
                        'shelf_level': cr.shelf_level,
                        'compliance_status': cr.compliance_status.value if hasattr(cr.compliance_status, 'value') else str(cr.compliance_status),
                        'compliance_score': cr.compliance_score,
                        'expected_products': cr.expected_products,
                        'found_products': cr.found_products,
                        'missing_products': getattr(cr, 'missing_products', []) or [],
                        'text_compliance_score': getattr(cr, 'text_compliance_score', 0.0),
                        'text_compliance_results': [
                            {
                                'required_text': tcr.required_text,
                                'found': tcr.found,
                                'confidence': tcr.confidence,
                                'matched_features': getattr(tcr, 'matched_features', [])
                            }
                            for tcr in getattr(cr, 'text_compliance_results', [])
                        ] if hasattr(cr, 'text_compliance_results') else []
                    }
                    for cr in result.get('step3_compliance_results', [])
                ]
            }, indent=2)

            # parsing the results:
            overall_compliance_score = result.get('overall_compliance_score', 0.0)
            overall_compliant = result.get('overall_compliant', False)
            overlay_image = None
            compliance_by_shelf = {}
            detections = []

            # list of ComplianceResult objects
            compliance_results = result.get('step3_compliance_results', [])
            # 1. Compliance by shelf
            for compliance in compliance_results:
                compliance_by_shelf[compliance.shelf_level] = {
                    "compliance_status": compliance.compliance_status.value,
                    "compliance_score": compliance.compliance_score,
                    "expected_products": compliance.expected_products,
                    "found_products": compliance.found_products
                }

            # Load overlay image from pipeline result
            # 'rendered_image' is a PIL Image object, 'overlay_path' is the file path string
            overlay_image = None
            rendered_image = result.get('rendered_image')
            actual_overlay_path = result.get('overlay_path')
            if isinstance(rendered_image, Image.Image):
                overlay_image = rendered_image
                overlay_path = actual_overlay_path or ""
            elif actual_overlay_path and Path(actual_overlay_path).exists():
                overlay_image = Image.open(actual_overlay_path)
                overlay_path = actual_overlay_path
            else:
                overlay_path = ""

            # 2. A simplified list of identified products (detections)
            # Pipeline returns 'identified_products' (not 'step2_identified_products')
            raw_detections = result.get('identified_products', result.get('step2_identified_products', []))
            self._logger.debug(
                f"Row {row_index}: pipeline result keys={list(result.keys())}, "
                f"identified_products count={len(raw_detections)}, "
                f"overall_compliance_score={overall_compliance_score:.3f}, "
                f"overall_compliant={overall_compliant}, "
                f"overlay_path='{actual_overlay_path}', "
                f"rendered_image type={type(rendered_image).__name__}"
            )
            for shelf_r in compliance_results:
                self._logger.debug(
                    f"  shelf={shelf_r.shelf_level} status={shelf_r.compliance_status} "
                    f"score={shelf_r.compliance_score:.3f} "
                    f"expected={shelf_r.expected_products} "
                    f"found={shelf_r.found_products}"
                )
            detections = []
            for p in raw_detections:
                det = {}
                for attr in ('product_type', 'product_model', 'brand', 'reference_match',
                             'visual_features', 'confidence', 'shelf_location', 'position_on_shelf'):
                    det[attr] = getattr(p, attr, None)
                detections.append(det)
                self._logger.debug(
                    f"  detection: model={p.product_model!r} type={p.product_type!r} "
                    f"shelf={p.shelf_location!r} bbox={getattr(p, 'detection_box', None)}"
                )

            # Create markdown and JSON reports (pass overlay_path for inclusion in report)
            summary_report = self._create_markdown_report(result, overlay_path=overlay_path)
            markdown_report = summary_report
            return {
                'row_index': row_index,
                'planogram_id': self.planogram_config.planogram_id,
                'overall_compliance_score': overall_compliance_score,
                'overall_compliant': overall_compliant,
                'compliance_analysis': summary_report,
                'compliance_analysis_json': json_report,
                'compliance_analysis_markdown': markdown_report,
                'overlay_path': overlay_path,
                'overlay_image': overlay_image,
                # Add the new fields to the return dictionary
                'compliance_by_shelf': compliance_by_shelf,
                'detections': detections,
                'status': 'success',
                'error': None
            }

        except Exception as e:
            self._logger.error(
                f"Error processing row {row_index}: {e}"
            )
            return {
                'row_index': row_index,
                'planogram_id': self.planogram_config.planogram_id,
                'overall_compliance_score': 0.0,
                'overall_compliant': False,
                'compliance_analysis': f"# Error\nFailed to process: {str(e)}",
                'compliance_analysis_markdown': f"# Error\nFailed to process: {str(e)}",
                'compliance_analysis_json': json.dumps({"error": str(e)}),
                'overlay_image': None,
                'overlay_path': '',
                # Add new fields with error state
                'compliance_by_shelf': {"error": str(e)},
                'detections': [{"error": str(e)}],
                'status': 'error',
                'error': str(e)
            }

    def _post_process_results(self, results: List[Dict[str, Any]], df: pd.DataFrame) -> pd.DataFrame:
        """
        Integrate pipeline results back into the DataFrame.

        Args:
            results: List of pipeline execution results
            df: Original DataFrame

        Returns:
            DataFrame with new columns added
        """
        # Create a copy of the original DataFrame
        enhanced_df = df.copy()
        # Initialize existing and new columns
        new_cols = {
            'overall_compliance_score': 0.0,
            'overall_compliant': False,
            'planogram_id': None,
            'compliance_analysis': "",
            'compliance_analysis_markdown': "",
            'compliance_analysis_json': "",
            'overlay_image': None,
            # NEW: Initialize columns for the new data
            'compliance_by_shelf': None,
            'detections': None,
            'overlay_path': ""
        }

        for col, default in new_cols.items():
            # Use pd.NA for object types to allow for proper handling of missing values
            enhanced_df[col] = pd.NA if default is None else default
            if col in ['overlay_image', 'compliance_by_shelf', 'detections']:
                enhanced_df[col] = enhanced_df[col].astype('object')

        # Populate results
        for result in results:
            idx = result['row_index']
            enhanced_df.at[idx, 'overall_compliance_score'] = result['overall_compliance_score']
            enhanced_df.at[idx, 'overall_compliant'] = result['overall_compliant']
            enhanced_df.at[idx, 'compliance_analysis'] = result.get('compliance_analysis', '')
            enhanced_df.at[idx, 'compliance_analysis_markdown'] = result['compliance_analysis_markdown']
            enhanced_df.at[idx, 'compliance_analysis_json'] = result['compliance_analysis_json']
            enhanced_df.at[idx, 'overlay_image'] = result['overlay_image']
            enhanced_df.at[idx, 'overlay_path'] = result.get('overlay_path', '')

            # NEW: Populate the new columns
            enhanced_df.at[idx, 'compliance_by_shelf'] = result['compliance_by_shelf']
            enhanced_df.at[idx, 'detections'] = result.get('detections', [])
            enhanced_df.at[idx, 'planogram_id'] = result.get('planogram_id', None)

        return enhanced_df

    async def run(self):
        """
        Execute the planogram compliance pipeline on all DataFrame rows.

        Returns:
            Enhanced DataFrame with compliance analysis results
        """
        if self.data is None or self.data.empty:
            raise ComponentError(
                "No data available for processing"
            )

        # Initialize pipeline with configuration
        pipeline_kwargs = {
            'llm': self._llm,
            'planogram_config': self.planogram_config,
        }

        # Execute pipeline on DataFrame
        self._result = await self.execute_pipeline(
            self.data,
            **pipeline_kwargs
        )

        # Log summary statistics
        total_rows = len(self._result)
        compliant_rows = self._result['overall_compliant'].sum()
        avg_score = self._result['overall_compliance_score'].mean()

        self._logger.info(
            f"Processed {total_rows} images"
        )
        self._logger.info(
            f"Compliant images: {compliant_rows}/{total_rows} ({compliant_rows/total_rows:.1%})"
        )
        self._logger.info(
            f"Average compliance score: {avg_score:.1%}"
        )

        # print the dataframe execution:
        self._print_data_(self._result, 'Compliance Results')
        return self._result

    async def close(self):
        """Clean up resources."""
        if hasattr(self, '_pipeline'):
            self._pipeline = None
        if hasattr(self, '_llm'):
            await self._llm.close() if hasattr(self._llm, 'close') else None
        return True
