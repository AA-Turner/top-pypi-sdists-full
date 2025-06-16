"""
seeq_onnx_helper.py

This module provides client and utilities for interacting with the Seeq Server and handling ONNX models.
It includes functionality for authentication, ONNX model description and model listing, registration, update and
archiving in Seeq.
"""

import base64
import io
import json
from abc import ABC
from typing import List, Dict
from urllib.parse import urljoin

import onnx
import pandas as pd
import requests


class PropertyNames:
    Name = "Name"
    Description = "Description"
    Inputs = "Inputs"
    ResultType = "Result Type"
    ScopedTo = "Scoped To"


class FormulaType:
    OnnxPredictionModel = "OnnxPredictionModel"
    OnnxAnomalyModel = "OnnxAnomalyModel"


def get_auth_token(host: str, username: str, password: str) -> str:
    """
    Authenticates with the Seeq server and retrieves an authentication token.

    Parameters:
        host (str): The base URL of the Seeq server.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The authentication token (x-sq-auth).

    Example:
        >>> token = get_auth_token("https://tenant.seeq.com", "my_username", "my_password")
    """
    endpoint = urljoin(host, "/api/auth/login")
    response = requests.post(
        endpoint,
        headers={
            "Content-Type": "application/vnd.seeq.v1+json",
            "Accept": "application/vnd.seeq.v1+json",
        },
        data=json.dumps(
            {
                "username": username,
                "password": password,
                "authProviderClass": "Auth",
                "authProviderId": "Seeq",
            }
        ),
    )
    response.raise_for_status()
    return response.headers["x-sq-auth"]


def describe_onnx(model: onnx.ModelProto) -> None:
    """
    Prints a description of the ONNX model, including its inputs and outputs.

    Parameters:
        model (onnx.ModelProto): The ONNX model to describe.

    Returns:
        None

    Example:
        >>> import onnx
        >>> model = onnx.load("model.onnx")
        >>> describe_onnx(model)
    """

    def repr_tensor(tensor):
        name = tensor.name
        elem_type = onnx.TensorProto.DataType.Name(tensor.type.tensor_type.elem_type)
        shape = [
            dim.dim_value if (dim.dim_value > 0) else "?"
            for dim in tensor.type.tensor_type.shape.dim
        ]
        print(f"  - {name}: type={elem_type}, shape={shape}")

    graph = model.graph
    print(f"\n=== Model: {graph.name} ===")

    # Inputs
    print("\nInputs:")
    for input_tensor in graph.input:
        repr_tensor(input_tensor)

    # Outputs
    print("\nOutputs:")
    for output_tensor in graph.output:
        repr_tensor(output_tensor)


def cast_double_to_float(model: onnx.ModelProto) -> onnx.ModelProto:
    """
    Modifies an ONNX model to cast its input from double (float64) to float (float32).

    This function inserts a `Cast` node at the beginning of the model's graph to convert
    the input tensor's data type from double (float64) to float (float32). It also updates
    the input tensor's type and adjusts the input references in subsequent nodes.

    Parameters:
        model (onnx.ModelProto): The ONNX model to modify.

    Returns:
        onnx.ModelProto: The modified ONNX model with the cast operation added.

    Example:
        >>> import onnx
        >>> model = onnx.load("model.onnx")
        >>> modified_model = cast_double_to_float(model)
        >>> onnx.save(modified_model, "modified_model.onnx")
    """
    input_name = model.graph.input[0].name
    cast_node = onnx.helper.make_node(
        "Cast",
        inputs=[input_name],
        outputs=["cast_float_input"],
        to=onnx.TensorProto.FLOAT,  # Target type is float32
    )
    for node in model.graph.node:
        for i, input_name in enumerate(node.input):
            if input_name == model.graph.input[0].name:
                node.input[i] = "cast_float_input"

    model.graph.input[0].type.tensor_type.elem_type = onnx.TensorProto.DOUBLE
    model.graph.node.insert(0, cast_node)
    return model


class ONNXClient(ABC):
    _BINARY_DATA_OP = "binaryData()"
    _RESULT_TYPE_TO_MODEL_TYPE = {
        "OnnxPredictionModel": "PREDICTION",
        "OnnxAnomalyModel": "ANOMALY",
    }

    def _build_options(self, model_type: str, options: Dict[str, str]) -> str:
        allowed_options = {
            "PREDICTION": {"valueUnits"},
            "ANOMALY": {"outlierValue", "outlierPredicate"},
        }
        allowed_prefixes = {
            "ANOMALY": {"singleValue", "featureValue"},
        }

        if model_type not in allowed_options:
            raise ValueError(
                f"Invalid model type: '{model_type}'. Must be one of {list(allowed_options.keys())}."
            )

        valid_options = allowed_options[model_type]
        valid_prefixes = allowed_prefixes.get(model_type, set())
        invalid_keys = [
            k
            for k in options
            if k not in valid_options and not any(k.startswith(p) for p in valid_prefixes)
        ]
        if invalid_keys:
            raise ValueError(f"Invalid options for {model_type}: {invalid_keys}")

        formatted_options = [
            f'"{key}", "{value}"' for key, value in options.items() if value is not None
        ]
        return f"options({', '.join(formatted_options)})"

    def _generate_formula(self, model_type: str, labels: List[str], options: Dict[str, str]) -> str:

        operator_map = {
            "PREDICTION": "toPredictionModel",
            "ANOMALY": "toAnomalyModel",
        }

        if model_type not in operator_map:
            raise ValueError(
                f"Invalid model type: '{model_type}'. Must be one of {list(operator_map.keys())}."
            )

        operator = operator_map[model_type]
        options_str = self._build_options(model_type, options)
        return f"{self._BINARY_DATA_OP}.{operator}({len(labels)}, {options_str})"

    def _build_inputs(self, labels) -> List[Dict[str, str]]:
        value = json.dumps([{"name": label} for label in labels])
        prop = {"name": PropertyNames.Inputs, "value": value}
        return [prop]

    def _base64encoded_model(self, model: onnx.ModelProto) -> str:
        model_bytes = io.BytesIO()
        onnx.save(model, model_bytes)
        model_bytes.seek(0)
        return base64.b64encode(model_bytes.read()).decode("utf-8")

    def _list_formated(self, items) -> pd.DataFrame:
        records = []
        for item in items:
            base = {
                "ID": item.get("id"),
                "Name": item.get("name"),
                "Description": item.get("description"),
                "Archived": item.get("isArchived"),
            }
            props = item.get("includedProperties")
            inps = [inp["name"] for inp in json.loads(props.get(PropertyNames.Inputs, {}).get("value", "[]"))]
            base["Input Labels"] = inps
            base["Feature Count"] = len(inps)
            base["Type"] = self._RESULT_TYPE_TO_MODEL_TYPE[props.get(PropertyNames.ResultType, {}).get("value")]
            base["Scoped To"] = props.get(PropertyNames.ScopedTo, {}).get("value")
            records.append(base)

        column_order = ["ID", "Name", "Description", "Type", "Input Labels", "Feature Count", "Scoped To", "Archived"]

        return pd.DataFrame.from_records(records, columns=column_order)

    def register(self, name: str, description: str, model: onnx.ModelProto, model_type: str, labels: List[str],
                 scope: str = None, **kwargs) -> str:
        """
        Registers an ONNX in Seeq.

        Parameters:
            name: The name of the ONNX to register.
            description: The description of the ONNX.
            model: The ONNX to register. Must be a valid ONNX.
            model_type: The type of the ONNX. Must be one of "PREDICTION" or "ANOMALY".
            labels: The labels for the ONNX inputs. Must be provided as a list of strings.
            scope: The ID of the workbook to scope the ONNX to. If not provided, the ONNX will not be scoped.
            kwargs: Additional options for the ONNX, such as `valueUnits`, `outlierValue`, etc.

        Returns:
            ID of the registered ONNX.
        """
        raise NotImplementedError("Method 'register' must be implemented in subclasses.")

    def update(self, id: str, name: str = None, description: str = None, model: onnx.ModelProto = None,
               labels: List[str] = None, scope: str = None, **kwargs) -> None:
        """
        Updates an existing ONNX in Seeq.

        Parameters:
            id: The ID of the ONNX to update.
            name: The new name for the ONNX.
            description: The new description for the ONNX.
            model: The ONNX to update. If provided, the model must be a valid ONNX.
            labels: The labels for the ONNX inputs. Must be provided if `model` is provided.
            scope: The ID of the workbook to scope the ONNX to. If not provided, the ONNX scope will be left unchanged. Note: Globally scoped ONNX cannot be updated to a workbook scope.
            kwargs: Additional options for the ONNX, such as `valueUnits`, `outlierValue`, etc.

        Returns:
            None
        """
        raise NotImplementedError("Method 'update' must be implemented in subclasses.")

    def list(self, scope: str = None, include_archived: bool = False) -> pd.DataFrame:
        """
        Lists all ONNX models registered in Seeq.

        Parameters:
            scope: The ID of the workbook to filter the ONNX by. If not provided, all ONNX will be listed.
            include_archived: If True, includes archived ONNX in the list. Defaults to False.

        Returns:
            pd.DataFrame containing the ONNX with their details.
        """
        raise NotImplementedError("Method 'list' must be implemented in subclasses.")

    def archive(self, id: str, delete: bool = False) -> None:
        """
        Archives or deletes an ONNX by its ID.

        Parameters:
            id: The ID of the ONNX to archive or delete.
            delete: If True, the ONNX will be deleted; otherwise, it will be archived.
        Returns:
            None
        """
        raise NotImplementedError("Method 'archive' must be implemented in subclasses.")


def _custom_response_hook(response: requests.Response, *args, **kwargs) -> None:
    http_error_msg = ""
    reason = response.json().get("statusMessage", "Unknown error")
    if 400 <= response.status_code < 500:
        http_error_msg = f"{response.status_code} Client Error: {reason} for url: {response.url}"

    elif 500 <= response.status_code < 600:
        http_error_msg = f"{response.status_code} Server Error: {reason} for url: {response.url}"

    if http_error_msg:
        raise requests.exceptions.HTTPError(http_error_msg, response=response)


class SeeqONNXClient(ONNXClient):
    def __init__(self, host: str, auth_token: str):
        self._host = host
        self._auth_token = auth_token
        self._session = requests.Session()
        self._session.hooks = {'response': _custom_response_hook}
        self._session.headers.update({
            "Content-Type": "application/vnd.seeq.v1+json",
            "Accept": "application/vnd.seeq.v1+json",
            "x-sq-auth": self._auth_token})

    def list(self, scope: str = None, include_archived: bool = False) -> pd.DataFrame:
        url = urljoin(self._host, "api/items")
        filters = [f"{PropertyNames.ResultType}=={FormulaType.OnnxPredictionModel}",
                   f"{PropertyNames.ResultType}=={FormulaType.OnnxAnomalyModel}"]
        if include_archived:
            filters.append("@includeUnsearchable")
        params = {
            "includeProperties": [PropertyNames.Inputs, PropertyNames.ResultType, PropertyNames.ScopedTo],
            "filters": filters,
            "types": ["FormulaItem"]
        }
        if scope:
            params["scope"] = scope
        items = self._session.get(url, params=params)
        return self._list_formated(items.json().get("items", []))

    def register(self, name: str, description: str, model: onnx.ModelProto, model_type: str, labels: List[str],
                 scope: str = None, **kwargs) -> str:
        url = urljoin(self._host, "api/formulas/items")
        payload = {
            "name": name,
            "description": description,
            "formula": self._generate_formula(model_type, labels, kwargs),
            "additionalProperties": self._build_inputs(labels),
            "binaryData": self._base64encoded_model(model),
            "scopedTo": scope,
        }
        response = self._session.post(url, data=json.dumps(payload)).json()
        print(f"Successfully registered ONNX '{response['name']}' (ID: {response['id']}) (Scoped to: {scope})")
        return response['id']

    def update(self, id: str, name: str = None, description: str = None, model: onnx.ModelProto = None,
               labels: List[str] = None, scope: str = None, **kwargs) -> None:
        result_type_prop_url = urljoin(self._host, f"api/items/{id}/properties/{PropertyNames.ResultType}")
        result_type = self._session.get(result_type_prop_url).json().get("value")
        if result_type not in self._RESULT_TYPE_TO_MODEL_TYPE.keys():
            raise ValueError(f"Item with id {id} is not a valid ONNX. Result Type: {result_type}")
        model_type = self._RESULT_TYPE_TO_MODEL_TYPE[result_type]
        if model:
            if not labels:
                raise ValueError("Labels must be provided when updating the model.")
            set_formula_url = urljoin(self._host, f"api/items/{id}/formula")
            payload = {
                "binaryData": self._base64encoded_model(model),
                "formula": self._generate_formula(model_type, labels, kwargs)
            }
            self._session.post(set_formula_url, data=json.dumps(payload))
        properties = []
        if name:
            properties.append({"name": PropertyNames.Name, "value": name})
        if description:
            properties.append({"name": PropertyNames.Description, "value": description})
        if labels:
            properties.extend(self._build_inputs(labels))
        if properties:
            set_properties_url = urljoin(self._host, f"api/items/{id}/properties")
            self._session.post(set_properties_url, data=json.dumps(properties))
        if scope:
            set_scope_url = urljoin(self._host, f"api/items/{id}/scope")
            params = {"workbookId": scope}
            self._session.post(set_scope_url, params=params)
        print(f"Successfully updated ONNX (ID: {id})")

    def archive(self, id: str, delete: bool = False) -> None:
        url = urljoin(self._host, f"api/items/{id}")
        params = {
            "delete": False,
            "archivedReason": "BY_USER"
        }
        self._session.delete(url, params=params)
        if delete:
            params["delete"] = True
            self._session.delete(url, params=params)
            print(f"Successfully deleted ONNX (ID: {id})")
            return
        print(f"Successfully archived ONNX (ID: {id})")
