from typing import Dict, Any, Union, Optional, List, cast


def save_builder() -> '_SaveRequestBuilder':
    builder = _SaveRequestBuilder()
    return builder


class _SaveRequestBuilder:
    """
    Builds a save request, that can be used to trigger saves on the UI
    """

    def __init__(self) -> None:
        self._component: Optional[dict] = None
        self._uuid: Optional[str] = None
        self._context: Optional[dict] = None
        self._value: Optional[Union[dict, list]] = None
        self._identifier: Optional[Dict[str, Any]] = None

    def component(self, component: Dict[str, Any]) -> '_SaveRequestBuilder':
        self._component = component
        return self

    def uuid(self, uuid: str) -> '_SaveRequestBuilder':
        self._uuid = uuid
        return self

    def context(self, context: Dict[str, Any]) -> '_SaveRequestBuilder':
        self._context = context
        return self

    def value(self, value: Optional[Union[dict, list]]) -> '_SaveRequestBuilder':
        self._value = value
        return self

    def identifier(self, identifier: Optional[Dict[str, Any]]) -> '_SaveRequestBuilder':
        self._identifier = identifier
        return self

    def build(self) -> Dict[str, Any]:
        if self._component is None:
            raise Exception("Component not set")
        if self._uuid is None:
            raise Exception("uuid not set")
        if self._context is None:
            raise Exception("context not set")

        if self._value is None:
            self._value = self._component.get("value", "")

        if 'saveInto' not in self._component:
            # Support onSubmitSaveInto
            if 'onSubmitSaveInto' in self._component:
                save_into = self._component['onSubmitSaveInto']
            elif 'saveInto' not in self._component.get('contents', {}):
                raise Exception("saveInto not set")
            else:
                save_into = self._component['contents']['saveInto']
        else:
            save_into = self._component['saveInto']

        payload = {
            "#t": "UiConfig",
            "context": self._context,
            "uuid": self._uuid,
            "updates": {
                "#t": "SaveRequest?list",
                "#v": [
                    {
                        "_cId": self._component["_cId"],
                        "model": {"#t": self._component.get("#t")},
                        "value": self._value,
                        "saveInto": save_into,
                        "saveType": "PRIMARY",
                    }
                ],
            },
        }
        # We need to add the label for dynamicLink: async_timer for it to be evaluated as an async request
        if self._component.get('label') == 'async_timer':
            updates = cast(Dict[str, Any], payload["updates"])
            v_list = cast(List[Dict[str, Any]], updates["#v"])
            v_list[0].update({"label": self._component["label"]})
        if self._identifier:
            payload.update(
                {"identifier": self._identifier}
            )
        return payload
