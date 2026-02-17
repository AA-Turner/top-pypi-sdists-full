from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

from django.utils.http import urlencode
from rest_framework.request import Request
from rest_framework.reverse import reverse


@dataclass
class ItemPermission:
    permissions: List[str] = field(default_factory=list)
    method: Optional[Callable] = None
    include_superuser: bool = True

    def has_permission(self, request: Request) -> bool:
        if self.include_superuser and request.user.is_superuser:
            return True

        # We want permissions+ method to act as cumualtive (i.e. if any of this return False, then user does not have permission to access this menu item)
        # We default to True because in case a ItemPermission is defined without a method nor permissions, we assume, it acts as Allow Any
        has_permission = True
        for permission in self.permissions:
            if not request.user.has_perm(permission):
                has_permission &= False

        if self.method:
            has_permission &= self.method(request=request)

        return has_permission


@dataclass
class MenuItem:
    label: str

    endpoint: str
    endpoint_args: List[str] = field(default_factory=list)
    endpoint_kwargs: Dict[str, str] = field(default_factory=dict)
    endpoint_get_parameters: Callable | Dict[str, Any] = field(default_factory=dict)
    reverse: bool = True

    permission: Optional[ItemPermission] = None
    add: Optional["MenuItem"] = None

    index: Optional[int] = None
    new_mode: bool = False

    def __iter__(self):
        request = getattr(self, "request", None)

        if self.permission is None or self.permission.has_permission(request=request):
            if self.reverse:
                endpoint = reverse(
                    viewname=self.endpoint,
                    args=self.endpoint_args,
                    kwargs=self.endpoint_kwargs,
                    request=request,
                )
            else:
                endpoint = self.endpoint

            endpoint_get_parameters = self.endpoint_get_parameters
            if callable(endpoint_get_parameters):
                endpoint_get_parameters = endpoint_get_parameters(request)
            if self.new_mode:
                endpoint_get_parameters["new_mode"] = True

            if endpoint_get_parameters:
                endpoint_get_parameters = {
                    k: str(v).lower() if isinstance(v, bool) else v for k, v in endpoint_get_parameters.items()
                }
                endpoint += f"?{urlencode(endpoint_get_parameters)}"
            yield "label", self.label
            yield "endpoint", endpoint
            if self.add:
                self.add.request = request
                self.add.new_mode = True
                if dict(self.add):
                    yield "add", dict(self.add)


@dataclass
class Menu:
    label: str
    items: List[Union[MenuItem, "Menu"]] = field(default_factory=list)

    index: Optional[int] = None

    def __iter__(self):
        request = getattr(self, "request", None)
        items = list()
        for item in filter(lambda x: bool(x), self.items):
            item.request = request
            serialized_item = dict(item)
            if serialized_item:
                items.append(serialized_item)

        if len(items) > 0:
            yield "label", self.label
            yield "items", items
