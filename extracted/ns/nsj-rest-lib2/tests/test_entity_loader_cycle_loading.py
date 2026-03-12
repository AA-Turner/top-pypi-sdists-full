import json
import sys

from nsj_rest_lib.entity.entity_base import EntityBase

from nsj_rest_lib2.service.entity_loader import EntityLoader, namespaces_dict


def _build_entity_config() -> str:
    return json.dumps(
        {
            "dto_class_name": "TargetDTO",
            "entity_class_name": "TargetEntity",
            "source_dto": "class TargetDTO: pass",
            "source_entity": "class TargetEntity: pass",
            "entity_hash": "hash-target",
            "api_expose": True,
            "api_verbs": ["GET"],
            "service_account": None,
            "insert_function_class_name": None,
            "insert_function_name": None,
            "source_insert_function": None,
            "update_function_class_name": None,
            "update_function_name": None,
            "source_update_function": None,
            "get_function_name": None,
            "list_function_name": None,
            "delete_function_name": None,
            "get_function_type_class_name": None,
            "list_function_type_class_name": None,
            "delete_function_type_class_name": None,
            "retrieve_after_insert": False,
            "retrieve_after_update": False,
            "retrieve_after_partial_update": False,
            "post_response_dto_class_name": None,
            "put_response_dto_class_name": None,
            "patch_response_dto_class_name": None,
            "custom_json_post_response": False,
            "custom_json_put_response": False,
            "custom_json_patch_response": False,
            "custom_json_get_response": False,
            "custom_json_list_response": False,
            "custom_json_delete_response": False,
            "source_get_function_type": None,
            "source_list_function_type": None,
            "source_delete_function_type": None,
            "relations_dependencies": [
                {
                    "tenant": 0,
                    "grupo_empresarial": None,
                    "entity_resource": "dependency",
                    "entity_scope": "folha",
                }
            ],
        }
    )


def test_execute_entity_source_primes_entity_and_dto_before_dependency_load(monkeypatch):
    loader = EntityLoader()
    loader.clear_namespaces()
    sys.modules.pop("dynamic", None)
    sys.modules.pop("dynamic.default", None)

    calls: list[str] = []

    def fake_safe_exec(source_code, context, description):
        calls.append(description)
        if description == "Entity source":
            context["TargetEntity"] = type(
                "TargetEntity",
                (EntityBase,),
                {
                    "pk_field": "target",
                    "fields_map": {"target": object()},
                },
            )
        elif description == "DTO source":
            context["TargetDTO"] = type("TargetDTO", (), {})

    def fake_load_entity_source(*args, **kwargs):
        namespace = namespaces_dict["default"]
        assert "TargetEntity" in namespace.entities_dict
        assert namespace.entities_dict["TargetEntity"].pk_field == "target"
        assert "TargetDTO" in namespace.entities_dict
        assert getattr(
            namespace.entities_dict["TargetDTO"], "__dynamic_placeholder__", False
        )
        calls.append("dependency load")
        return None

    monkeypatch.setattr(loader, "_safe_exec", fake_safe_exec)
    monkeypatch.setattr(loader, "load_entity_source", fake_load_entity_source)

    loader._execute_entity_source(
        _build_entity_config(),
        "default",
        "target-resource",
    )

    assert calls[:2] == ["Entity source", "dependency load"]

    loader.clear_namespaces()
    sys.modules.pop("dynamic.default", None)
    sys.modules.pop("dynamic", None)
