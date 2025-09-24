from __future__ import annotations

from datetime import datetime
from typing import Any, List

from chalk.ml.utils import ModelEncoding, ModelType

MODEL_HOOKS = {
    (ModelType.PYTORCH, ModelEncoding.PICKLE): lambda f: __import__("torch").load(f),
    (ModelType.SKLEARN, ModelEncoding.PICKLE): lambda f: __import__("joblib").load(f),
    (ModelType.TENSORFLOW, ModelEncoding.HDF5): lambda f: __import__("tensorflow").keras.models.load_model(f),
    (ModelType.TENSORFLOW, ModelEncoding.SAFETENSOR): lambda f: __import__("tensorflow").keras.models.load_model(f),
    (ModelType.XGBOOST, ModelEncoding.JSON): lambda f: __import__("xgboost").XGBModel().load_model(f),
    (ModelType.LIGHTGBM, ModelEncoding.TEXT): lambda f: __import__("lightgbm").Booster(model_file=f),
    (ModelType.CATBOOST, ModelEncoding.CBM): lambda f: __import__("catboost").CatBoost().load_model(f),
    (ModelType.ONNX, ModelEncoding.PROTOBUF): lambda f: __import__("onnxruntime").InferenceSession(f),
}

PREDICT_HOOKS = {
    (ModelType.PYTORCH, ModelEncoding.PICKLE): lambda model, X: model(X).detach().numpy(),
    (ModelType.SKLEARN, ModelEncoding.PICKLE): lambda model, X: model.predict(X),
    (ModelType.TENSORFLOW, ModelEncoding.HDF5): lambda model, X: model.predict(X),
    (ModelType.TENSORFLOW, ModelEncoding.SAFETENSOR): lambda model, X: model.predict(X),
    (ModelType.XGBOOST, ModelEncoding.JSON): lambda model, X: model.predict(X),
    (ModelType.LIGHTGBM, ModelEncoding.TEXT): lambda model, X: model.predict(X),
    (ModelType.CATBOOST, ModelEncoding.CBM): lambda model, X: model.predict(X),
    (ModelType.ONNX, ModelEncoding.PROTOBUF): lambda model, X: model.run(None, {"input": X.astype("float32")})[0],
}


class ModelVersion:
    def __init__(
        self,
        *,
        name: str,
        filename: str | None = None,
        model_type: ModelType | None = None,
        model_encoding: ModelEncoding | None = None,
        version: int | None = None,
        alias: str | None = None,
        as_of_date: datetime | None = None,
    ):
        """Specifies the model version that should be loaded into the deployment.

        Examples
        --------
        >>> from chalk.ml import ModelVersion
        >>> ModelVersion(
        ...     name="fraud_model",
        ...     version=1,
        ... )
        """
        super().__init__()
        self.filename = filename
        self.name = name
        self.version = version
        self.alias = alias
        self.as_of_date = as_of_date
        self.model_type = model_type
        self.model_encoding = model_encoding

        self._model = None
        self._predict_fn = None

    def get_model_file(self) -> str | None:
        """Returns the filename of the model."""
        if self.filename is None:
            return None
        return self.filename

    def load_model(self):
        """Loads the model from the specified filename using the appropriate hook."""
        if self.model_type and self.model_encoding:
            load_function = MODEL_HOOKS.get((self.model_type, self.model_encoding))
            if load_function is not None:
                self._model = load_function(self.filename)
            else:
                raise ValueError(
                    f"No load function defined for type {self.model_type} and extension {self.model_encoding}"
                )

    def predict(self, X: List[List[float]]):
        """Loads the model from the specified filename using the appropriate hook."""

        if self._predict_fn is None:
            if self.model_type is None or self.model_encoding is None:
                raise ValueError("Model type and encoding must be specified to use predict.")
            self._predict_fn = PREDICT_HOOKS.get((self.model_type, self.model_encoding), None)
            if self._predict_fn is None:
                raise ValueError(
                    f"No predict function defined for type {self.model_type} and extension {self.model_encoding}"
                )
        return self._predict_fn(self.model, X)

    @property
    def model(self) -> Any:
        """Returns the loaded model instance

        Parameters
        ----------
        name
            The name of the model.
        when
            The datetime to use for creating the model version identifier.

        Returns
        -------
        loaded_model
            A new ModelReference instance with a time-based identifier.

        Examples
        --------
        >>> import datetime
        >>> model = ModelVersion(
        """
        if self._model is None:
            self.load_model()

        return self._model
