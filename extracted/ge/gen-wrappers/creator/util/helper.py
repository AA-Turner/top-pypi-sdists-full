import importlib
import pkgutil
import sys
from typing import Union, Type, Dict, List, Any

from creator.base.base_app import BaseApp
from creator.base.base_request import BaseRequest


def get_creators():
    package = sys.modules['creator']  # Make sure 'src.sb_api.creator' is the correct package path
    creator_names = []
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        # Filter out unwanted modules
        if "creator_" not in modname or "base" in modname:
            continue

        # Try to import the module
        try:
            module = importlib.import_module(modname)
            # Find all subclasses of BaseApp in the imported module
            for name, obj in vars(module).items():
                if isinstance(obj, type) and issubclass(obj, BaseApp) and obj is not BaseApp:
                    base_app_name = obj.__name__.replace("App", "")
                    base_app_name = ''.join(['_' + i.lower() if i.isupper() else i for i in base_app_name]).lstrip('_')
                    creator_names.append(base_app_name)
        except Exception as e:
            print(f"Error importing {modname}: {e}")
    return creator_names


def get_creator_examples(openapi_output=False):
    creators = get_creators()
    examples = []
    openapi_examples = {}
    for creator in creators:
        examples.append({"name": creator, "description": f"Example for {creator} creator."})
        openapi_examples[creator] = {
            "summary": f"{creator}",
            "value": creator
        }
    return examples if not openapi_output else openapi_examples


def get_use_cases(return_creator_names: bool = False, return_param_names: bool = False) -> Union[
    Dict[str, List[BaseRequest]], Dict[BaseApp, List[BaseRequest]]]:
    package = sys.modules['creator']  # Make sure 'src.sb_api.creator' is the correct package path
    use_case_dict = {}

    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        # Filter out unwanted modules
        if "creator_" not in modname or "base" in modname:
            continue

        # Try to import the module
        try:
            module = importlib.import_module(modname)
            # Find all subclasses of BaseApp in the imported module
            for name, obj in vars(module).items():
                if isinstance(obj, type) and issubclass(obj, BaseApp) and obj is not BaseApp:
                    params = getattr(obj, "param_classes", [])
                    if return_param_names:
                        params = [param.__name__ for param in params]
                    if not return_creator_names:
                        use_case_dict[obj] = params
                    else:
                        use_case_dict[obj.__name__] = params
        except Exception as e:
            print(f"Error importing {modname}: {e}")

    return use_case_dict


def get_use_case_examples(return_class_name=False, openapi_output=False):
    use_cases = get_use_cases(True, False)  # Always fetch class objects
    examples = []
    openapi_examples = {}
    for creator, use_case_list in use_cases.items():
        for use_case in use_case_list:
            example_param = use_case().example()
            example_execution_params = {
                "params": example_param,
                "callback_url": "http://example.com/callback"
            }
            summary = f"Execute {creator}/{use_case.__name__}_async with optional callback"
            example_name = use_case.__name__ + ("_async" if return_class_name else "")
            examples.append({"name": example_name, "value": example_execution_params})
            openapi_examples[example_name] = {
                "summary": summary,
                "value": example_execution_params
            }
    return examples if not openapi_output else openapi_examples


def get_method_examples(openapi_output=False) -> Union[Dict[str, Any], list[Dict[str, Any]]]:
    use_cases = get_use_cases(True, True)
    examples = []
    openapi_examples = {}
    for creator, use_case_list in use_cases.items():
        for method in use_case_list:
            examples.append({"name": method, "description": f"Example for {method} method."})
            openapi_examples[method] = {
                "summary": f"{method}",
                "value": method
            }
    return examples if not openapi_output else openapi_examples


def get_use_case(app_name: str, method: str) -> Union[None, Type[BaseRequest]]:
    use_cases = get_use_cases(True, False)
    method = method.replace("_async", "")
    # Convert app_name to CamelCase
    app_name = ''.join([i.capitalize() for i in app_name.split('_')])
    app_name = f"App{app_name}"
    use_case_list = use_cases.get(app_name, [])
    for use_case in use_case_list:
        if use_case.__name__.split("_")[-1] == method:
            return use_case
    return None
