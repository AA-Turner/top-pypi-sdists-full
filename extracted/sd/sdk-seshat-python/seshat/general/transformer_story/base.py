import copy
import dataclasses
import inspect
import re
from abc import ABC, abstractmethod
from copy import deepcopy
from types import ModuleType
from typing import Callable, Dict, List, Tuple, Any, Type, Optional

from seshat.data_class import GroupSFrame, SFrame
from seshat.transformer import Transformer
from seshat.utils.analyze_method_call import analyze_method_calls
from seshat.utils.validation import NumericColumnValidator, TimeStampColumnValidator


def safe_import_testcase(module_name: str, class_name: str) -> Optional[Type]:
    """
    Safely import a test case class. Returns None if the test module is not available.
    This allows the package to work without test dependencies in production.
    """
    try:
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)
    except (ImportError, ModuleNotFoundError, AttributeError):
        return None


class Empty:
    """
    Because of `None` itself can be default value.
    """


class Describable(ABC):
    @abstractmethod
    def generate_doc(self) -> str:
        pass


class TransformerScenario:
    _result: SFrame
    transformer: Transformer

    def __init__(
        self,
        transformer: Transformer = None,
        sf_input: SFrame = None,
        description: str = None,
    ):
        self.transformer = transformer
        self.sf_input = sf_input
        self.description = description

    def get_result(self):
        if hasattr(self, "_result"):
            return self._result
        self._result = self.transformer(copy.deepcopy(self.sf_input))
        return self._result

    @classmethod
    def get_attributes(cls, transformer: Transformer):
        return {
            k: cls._format_attr(v)
            for k, v in transformer.__dict__.items()
            if not k.startswith("_")
            and not isinstance(k, SFrame)
            and k not in transformer.__class__.__dict__
        }

    def as_json(self):
        sf_input_dict = {}
        if self.sf_input is not None:
            group = self.sf_input.make_group()
            if (
                group is not None
                and hasattr(group, "children")
                and group.children is not None
            ):
                sf_input_dict = {
                    k: sf.to_dict()
                    for k, sf in group.children.items()
                    if sf is not None
                }
        return {
            "description": self.description,
            "sf_input": sf_input_dict,
            "attributes": self.get_attributes(self.transformer),
            "result": self.format_result(),
        }

    def format_result(self):
        result = self.get_result()
        if result is None:
            return {}
        group = result.make_group()
        if group is None or not hasattr(group, "children") or group.children is None:
            return {}
        return {k: sf.to_dict() for k, sf in group.children.items() if sf is not None}

    def find_output_changes(self):
        """
        Automatically detect changes in the group SFrame and the addition or removal of columns in the result.
        This function does not support all types of changes, such as reordering or trimming rows.
        """
        in_ = self.sf_input
        out = self.get_result()
        if isinstance(out, GroupSFrame):
            out.children = {
                k: out.get(v)
                for k, v in self.transformer.group_keys.items()
                if out.get(v)
            }

        result = []
        if isinstance(in_, GroupSFrame) and isinstance(out, GroupSFrame):
            # Find group sframe changes
            differences = set(in_.keys).symmetric_difference(set(out.keys))
            for diff in differences:
                result.append(
                    f"sframe {diff} {'added to' if diff in out.children else 'dropped'} output"
                )
        elif isinstance(out, GroupSFrame):
            result.append(
                f"convert to group sframe with keys {', '.join(list(out.keys))}"
            )

        in_keys = set(in_.keys) if isinstance(in_, GroupSFrame) else {"default"}
        out_keys = set(out.keys) if isinstance(out, GroupSFrame) else {"default"}

        # Find changes in columns
        for sf_key in in_keys.intersection(out_keys):
            if in_ is None:
                continue
            diff_cols = set(in_.get_columns(sf_key)).symmetric_difference(
                set(out.get_columns(sf_key))
            )
            if not diff_cols:
                continue
            for col in diff_cols:
                status = "added to" if col in out.get_columns(sf_key) else "removed in"
                result.append(f"column {col} in sframe {sf_key} {status} output")

        return result

    @classmethod
    def _format_attr(cls, attr):
        if isinstance(attr, list):
            return [cls._format_attr(a) for a in attr]
        elif isinstance(attr, tuple):
            return tuple(cls._format_attr(a) for a in attr)
        elif isinstance(attr, dict):
            return {cls._format_attr(k): cls._format_attr(v) for k, v in attr.items()}
        elif isinstance(attr, Transformer):
            return f"Transformer: {attr.__class__.__name__} with attributes: {cls.get_attributes(attr)}"
        elif inspect.isfunction(attr):
            return inspect.getsource(attr).strip()
        return str(attr)

    @classmethod
    def from_testcase(
        cls, testcase: Type | ModuleType, transformer: type[Transformer]
    ) -> List["TransformerScenario"]:
        """
        Patch the __call__ method of the transformer at runtime, then for target transformer
        keep the inputs, outputs and target instance.
        Supports both unittest.TestCase and pytest test classes.
        """
        import unittest

        scenarios = []
        description = [""]  # Use list to can update it inplace.
        transformer.__call__ = cls.get_call_wrapper(
            transformer, description, scenarios
        )(transformer.__call__)
        if inspect.isclass(testcase) and issubclass(testcase, unittest.TestCase):
            return cls._from_unittest_testcase(testcase, description, scenarios)
        else:
            return cls._from_pytest_testcase(testcase, description, scenarios)

    @classmethod
    def _from_unittest_testcase(cls, testcase: Type, description, scenarios):
        import unittest

        suite = unittest.TestLoader().loadTestsFromTestCase(testcase)
        for test in suite:
            # Remove `test_` from the beginning of the test name, make it readable
            # and update description value inplace.
            description[0] = test._testMethodName[5:].replace("_", " ")
            test.run()
        return scenarios

    @classmethod
    def _from_pytest_testcase(cls, testcase: Type | ModuleType, description, scenarios):
        """
        Process a pytest test case to extract transformer scenarios.
        """
        import pytest

        test_module_path = inspect.getfile(testcase)

        test_methods = cls._find_pytest_method(testcase)

        for method_name in test_methods:
            description[0] = method_name[5:].replace("_", " ")
            test = test_module_path
            if inspect.isclass(testcase):
                test += f"::{testcase.__name__}"
            test += f"::{method_name}"
            pytest_args = [test, "--quiet", "--no-summary"]
            pytest.main(pytest_args)

        return scenarios

    @classmethod
    def _find_pytest_method(cls, testcase):
        test_methods = []
        test_instance = testcase() if inspect.isclass(testcase) else testcase
        for attr_name in dir(test_instance):
            attr = getattr(test_instance, attr_name)
            if attr_name.startswith("test_") and callable(attr):
                if inspect.isfunction(attr) or inspect.ismethod(attr):
                    test_methods.append(attr_name)
        return test_methods

    @classmethod
    def get_call_wrapper(cls, transformer, description, scenarios):
        def call_wrapper(call):
            def inner(self, *args, **kwargs):
                sf_input = kwargs.get("sf_input")
                if sf_input is None and args:
                    sf_input = args[0]

                copied_sf_input = deepcopy(sf_input)
                result = call(self, sf_input)
                if isinstance(self, transformer):
                    scenario = cls(
                        sf_input=copied_sf_input,
                        transformer=self,
                        description=description[0],
                    )
                    scenario._result = result
                    scenarios.append(scenario)
                return result

            return inner

        return call_wrapper


class BaseTransformerStory(Describable):
    validation_summaries: List[str]
    outputs: List[str]
    tags: List[str]
    use_cases: List[str]
    scenarios: List[TransformerScenario] = []
    input_output_scenarios: List[Dict]
    transformer: Transformer
    logic_overview: str
    steps: List[str]
    interactions: List[Tuple[Any, str]] = []

    # Flag to determine whether to automatically find and track transformer outputs
    find_outputs: bool = True

    _required_fields = [
        "tags",
        "use_cases",
        "logic_overview",
        "steps",
    ]
    _fields = {
        "validation_summaries",
        "transformer_name",
        "general_description",
        "inferred",
        "input_output_scenarios",
        "interactions",
    } | set(_required_fields)

    def __init__(self):
        self.input_output_scenarios = getattr(self, "input_output_scenarios", [])
        self.outputs = getattr(self, "outputs", [])
        self.validation_summaries = getattr(self, "validation_summaries", [])

    def get_scenarios(self) -> List[TransformerScenario]:
        return self.scenarios

    @property
    def transformer_name(self):
        return self.transformer.__name__

    @property
    def general_description(self):
        if not self.transformer.__doc__:
            return None
        pattern = r"^(.*?)(?:\n\s*Parameters|\Z)"
        match = re.search(pattern, self.transformer.__doc__, flags=re.DOTALL)
        if match:
            return match.group(1).strip().replace("\n", "")
        return None

    @property
    def inferred(self):
        parent = self.transformer.__bases__[-1]
        return {
            "transformer_name": self.transformer_name,
            "transformer_parent_class": parent.__name__,
            "inputs": self._get_inputs(),
            "outputs": self.outputs,
        }

    def _get_doc_inputs(self) -> dict:
        if not self.transformer.__doc__:
            return {}

        # Extract the parameters from doc string
        pattern = (
            r"Parameters\s*-+\s*(.*?)(?=\n\s*(?:Raises|Returns|Examples|Attributes|Notes|See "
            r"Also|References)\s*-+|$)"
        )
        match = re.search(pattern, self.transformer.__doc__, flags=re.DOTALL)
        if not match:
            return {}

        lines = match.group(1).strip().split("\n ")

        doc_params = {}
        current_param = None
        description_lines = []
        for line in lines:
            if line.strip() == "":
                continue
            if not line.startswith(" " * 5):
                if current_param:
                    doc_params[current_param] = [
                        Empty,
                        " ".join(description_lines).strip(),
                        Empty,
                    ]
                parts = line.strip().split(":", 1)
                current_param = parts[0].strip()
                description_lines = []
            else:
                description_lines.append(line.strip())

        if current_param:
            doc_params[current_param] = [
                Empty,
                " ".join(description_lines).strip(),
                Empty,
            ]
        return doc_params

    def _get_inputs(self):
        # Add default value of parameters and add params that maybe miss in doc
        doc_params = self._get_doc_inputs()

        sig = inspect.signature(self.transformer.__init__)
        params = list(sig.parameters.values())[1:]
        for param in params:
            annotation = (
                param.annotation if param.annotation != inspect._empty else Empty
            )
            default = param.default if param.default != inspect._empty else Empty
            if param.name in doc_params:
                doc_params[param.name][0] = annotation
                doc_params[param.name][2] = default
                continue

            doc_params[param.name] = [
                annotation,
                "",
                default,
            ]

        result = []
        for k, v in doc_params.items():
            d = {
                "key": k,
                "description": v[1],
            }
            if v[0] != Empty:
                d["type"] = str(v[0])
            if v[2] != Empty:
                d["default"] = v[2]
            result.append(d)
        return result

    def setup(self):
        scenarios = []
        scenario_outputs = set()

        for scenario in self.get_scenarios():
            scenarios.append(scenario.as_json())
            if self.find_outputs:
                changes = scenario.find_output_changes()
                if changes:
                    scenario_outputs |= set(changes)
        self.input_output_scenarios += scenarios
        self.outputs += scenario_outputs

        # Find validations
        self.find_validations(
            {
                Transformer()._validate_columns: (
                    "Validate the the columns {cols} exists in sframe with key {key}"
                ),
                NumericColumnValidator().validate: (
                    "Ensure that the column {col} in {raw} is numeric, "
                    "if not try to convert it."
                ),
                TimeStampColumnValidator().validate: (
                    "Ensure that the column {col} in {raw} is date time, "
                    "if not try to convert it."
                ),
            }
        )

    def find_validations(self, validators: Dict[Callable, str]):
        analyze_res = analyze_method_calls(self.transformer, validators.keys())
        result = set()
        for validator, calls in analyze_res.items():
            [result.add(validators[validator].format(**call)) for call in calls]
        self.validation_summaries += list(result)

    def generate_doc(self):
        self.setup()
        return {field: getattr(self, field) for field in self._fields}

    def __init_subclass__(cls, **kwargs):
        for field in cls._required_fields:
            if not hasattr(cls, field):
                raise NotImplementedError(
                    "field %s is not defined in %s" % (field, cls.__name__)
                )
        return super().__init_subclass__(**kwargs)


@dataclasses.dataclass
class Approach:
    description: str
    involved_transformers: Dict[Type[Transformer], str]

    def as_json(self):
        return {
            "description": self.description,
            "involved transformers": {
                k.__name__: v for k, v in self.involved_transformers.items()
            },
        }


class BaseChallenge(Describable):
    goal: str
    approaches: List[Approach]
    criteria: str

    def generate_doc(self):
        return {
            "goal": self.goal,
            "approaches": [a.as_json() for a in self.approaches],
            "criteria": self.criteria,
        }
