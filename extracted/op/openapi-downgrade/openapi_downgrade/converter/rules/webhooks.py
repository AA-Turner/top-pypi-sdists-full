from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..warnings import WarningCollector

def drop_webhooks(spec: dict, warnings: "WarningCollector") -> dict:
    if "webhooks" not in spec:
        return spec

    try:
        webhooks = spec["webhooks"]
        callback_map = {}

        for name, path_item in webhooks.items():
            # Create a callback object. The key is a runtime expression.
            # We'll use '{$request.body#/callbackUrl}' as a default.
            callback_object = {
                '{$request.body#/callbackUrl}': path_item
            }
            callback_map[name] = callback_object

        if not callback_map:
            # No webhooks to convert, but the key exists.
            if "webhooks" in spec:
                del spec["webhooks"]
            return spec

        # Attach the callbacks to relevant operations
        operations_to_update = ["post", "put", "patch", "delete"]
        paths = spec.get("paths", {})
        updated = False
        for path_item in paths.values():
            if isinstance(path_item, dict):
                for method, operation in path_item.items():
                    if method in operations_to_update and isinstance(operation, dict):
                        if "callbacks" not in operation:
                            operation["callbacks"] = {}
                        operation["callbacks"].update(callback_map)
                        updated = True
        
        if updated:
            warnings.add("Webhooks were converted to callbacks on POST, PUT, PATCH, and DELETE operations using a default URL expression '{$request.body#/callbackUrl}'. Please review for correctness.")
        else:
            warnings.add("Webhooks section found, but no suitable operations (POST, PUT, PATCH, DELETE) to attach them to as callbacks.")

        del spec["webhooks"]

    except Exception as e:
        if "webhooks" in spec:
            del spec["webhooks"]
        warnings.add(f"Failed to convert webhooks to callbacks, so they were dropped. Error: {e}")

    return spec

