import glob
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas
import pyarrow

from tecton._internals import model_utils
from tecton._internals import type_utils
from tecton._internals.tecton_pydantic import StrictModel
from tecton.types import Field
from tecton_core.embeddings.artifacts_provider import InferenceDeviceHardware
from tecton_core.embeddings.python_model import PythonModelContainer
from tecton_core.embeddings.python_model import python_model_inference
from tecton_core.errors import TectonValidationError
from tecton_core.schema import Column


_CUSTOM_MODELS: List["ModelConfig"] = []
_LOCAL_CUSTOM_MODELS: Dict[str, "ModelConfig"] = {}


class ModelConfig(StrictModel):
    """A Custom Model in Tecton

    ```python
    from tecton import ModelConfig

    model_config = ModelConfig(
        name=”mymodel_text_embedder”,
        model_type="pytorch",
        model_file="model_file.py",
        environments=["custom-ml-env-01"],
        artifact_files=["model.safetensors", "tokenizer_config.json" …],
        input_schema=[Field(”my_text_col”, String), …],
        output_schema=Field(”text_embedding”)
    )
    ```

    :param name: Unique name of model
    :param model_type: Type of Model (pytorch or text embedding)
    :param description: Description of Model
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param model_file: Path of File containing model relative to where the Tecton object is defined.
    :param artifact_files: Path of other files needed to load and run model relative to where the Tecton object is defined.
    :param environments: All the environments allowed for this custom model to run in.
    :param input_schema: Input Schema for model. Each field in this schema corresponds to the `input_columns` specified in the `Inference` and is mapped by order.
    :param output_schema: Output Schema of model.

    :raises TectonValidationError: if the input non-parameters are invalid.
    """

    name: str
    model_type: str
    description: Optional[str]
    tags: Optional[Dict[str, str]]
    model_file: str
    artifact_files: Optional[List[str]]
    environments: List[str]
    input_schema: List[Field]
    output_schema: Field

    def __init__(
        self,
        *,
        name: str,
        model_type: str,
        model_file: str,
        environments: List[str],
        input_schema: List[Field],
        output_schema: Field,
        artifact_files: Optional[List[str]] = None,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            name=name,
            model_type=model_type,
            model_file=model_file,
            artifact_files=[] if artifact_files is None else artifact_files,
            environments=environments,
            input_schema=input_schema,
            output_schema=output_schema,
            description=description,
            tags=tags,
        )
        _CUSTOM_MODELS.append(self)

    def register(self):
        """Register a Model Locally so that it can be used in Local Feature Views."""
        if self.name in _LOCAL_CUSTOM_MODELS:
            print(f"`ModelConfig` with name {self.name} already exists in context, will be replaced.")
        _LOCAL_CUSTOM_MODELS[self.name] = self
        print(f"Successfully registered model: {self.name} locally.")

    def run(self, mock_inputs: Dict[str, List[Any]]) -> pandas.DataFrame:
        """Test Run a Model.

        :param mock_inputs: Mock Input for each column defined in input schema
        :return: pandas.Dataframe with inputs and output columns.

        :raises TectonValidationError: if the input non-parameters are invalid.
        """
        model_utils.validate(
            archive_root_path=Path("."), model_file=self.model_file, artifact_files=self.artifact_files
        )
        if self.model_type.lower() == "pytorch":
            return self._run_pytorch(mock_inputs)
        elif self.model_type.lower() == "python":
            return self._run_python(mock_inputs)
        else:
            msg = "Model Type not supported. Type must bhe [pytorch, python]"
            raise NotImplementedError(msg)

    def _run_python(self, mock_inputs: Dict[str, List[Any]]) -> pandas.DataFrame:
        self._validate_inputs(mock_inputs)

        with tempfile.TemporaryDirectory() as tmpdir:
            self._copy_artifacts(tmpdir)
            batch = pyarrow.RecordBatch.from_pydict(mock_inputs)
            model_container = PythonModelContainer(data_dir=Path(tmpdir), model_file_path=self._model_file_path)
            model_container.load()
            record_batch = python_model_inference(
                batch=batch,
                model=model_container,
                input_columns=self._input_columns,
                output_column=self._output_column,
                model_input_schema=self._input_columns,
            )
        return record_batch.to_pandas()

    def _run_pytorch(self, mock_inputs: Dict[str, List[Any]]) -> pandas.DataFrame:
        try:
            import torch

            from tecton_core.embeddings.pytorch_model import PytorchModelContainer
            from tecton_core.embeddings.pytorch_model import pytorch_model_inference
        except ImportError:
            msg = "Install tecton[ml-extras] to install additional packages needed to use Tecton Model Inference"
            raise ImportError(msg)

        self._validate_inputs(mock_inputs)

        with tempfile.TemporaryDirectory() as tmpdir:
            self._copy_artifacts(tmpdir)
            cuda_device = self._get_torch_cuda_device()
            batch = pyarrow.RecordBatch.from_pydict(mock_inputs)
            model_container = PytorchModelContainer(data_dir=Path(tmpdir), model_file_path=self._model_file_path)

            with torch.device(cuda_device):
                model_container.load()

            record_batch = pytorch_model_inference(
                batch=batch,
                model=model_container,
                input_columns=self._input_columns,
                output_column=self._output_column,
                model_input_schema=self._input_columns,
                cuda_device=cuda_device,
            )
            return record_batch.to_pandas()

    def _validate_inputs(self, mock_inputs):
        provided_keys = mock_inputs.keys()
        required_keys = {field.name for field in self.input_schema}

        if len(provided_keys - required_keys) != 0:
            msg = f"Input keys: {provided_keys - required_keys} are not in schema defined in ModelConfig"
            raise TectonValidationError(msg)

        if len(required_keys - provided_keys) != 0:
            msg = f"ModelConfig contains fields {required_keys - provided_keys} which are not provided in inputs"
            raise TectonValidationError(msg)

    def _copy_artifacts(self, target_dir: str):
        for file in self._all_file_paths:
            os.makedirs(Path(target_dir) / os.path.dirname(file), exist_ok=True)
            shutil.copy(file, Path(target_dir) / file)

    @property
    def _model_file_path(self) -> Path:
        return Path(".") / self.model_file

    @property
    def _input_columns(self) -> List[Column]:
        return [Column(name=field.name, dtype=field.dtype.tecton_type) for field in self.input_schema]

    @property
    def _output_column(self) -> Column:
        return Column.from_proto(type_utils.to_column(self.output_schema))

    @property
    def _all_file_paths(self):
        return [
            *[Path(file) for file_str in self.artifact_files for file in glob.glob(file_str)],
            self._model_file_path,
        ]

    @staticmethod
    def _get_torch_cuda_device() -> str:
        import torch

        cuda_device = InferenceDeviceHardware.CPU
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            if device_count > 0:
                cuda_device = "cuda:0"
        return cuda_device
