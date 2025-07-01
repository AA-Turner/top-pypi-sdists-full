import logging

from django.contrib.messages import get_messages, warning
from django_fsm import FSMField, Transition, TransitionNotAllowed
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from wbcore.messages import InMemoryMessageStorage

logger = logging.getLogger(__name__)


# We have to move the method generation into a method, because we need a real new instance of this method everytime
def get_method(transition, fsm_field_name):
    def method(self, request: Request, transition=transition, pk=None, **kwargs) -> Response:
        return self.fsm_route(request, transition, fsm_field_name, transition.custom.get("serializer", None))

    return method


class FSMViewSetMixinMetaclass(type):
    """Metaclass for dynamically creating all FSM Routes"""

    def __new__(cls, name, bases, dct):
        _class = super().__new__(cls, name, bases, dct)

        # The class needs the field FSM_MODELFIELDS to know which transitions it needs to add
        if hasattr(_class, "get_model"):
            model = _class.get_model()

            if model:
                setattr(_class, "FSM_BUTTONS", getattr(_class, "FSM_BUTTONS", set()))
                # The model potentially has multiple FSMFields, which needs to be iterated over
                for field in filter(lambda f: isinstance(f, FSMField), model._meta.fields):
                    # Get all transitions, by calling the partialmethod defined by django-fsm
                    transitions = getattr(model, f"get_all_{field.name}_transitions")(model())

                    # Since the method above can potentially return a transition multiple times
                    # i.e. when a transitions has multiple sources, we need to filter out those transitions
                    _discovered_transitions = list()

                    for transition in transitions:
                        if transition.name in _discovered_transitions:
                            continue
                        else:
                            _discovered_transitions.append(transition.name)

                        # Get the Transition Button and add it to the front of the instance buttons
                        button = transition.custom.get("_transition_button")
                        _class.FSM_BUTTONS.add(button)

                        # Create a method that calls fsm_route with the request and the action name
                        method = get_method(transition, field.name)

                        # We need to manually change the method name, otherwise django-fsm won't
                        # Add this method to the URLs

                        # Wrap the above defined method in the action decorator
                        # IMPORTANT: This needs to happen after we changed the method name
                        # therefore we cannot use the proper decorator
                        method.__name__ = transition.name
                        method.__doc__ = transition.method.__doc__

                        wrapped_method = action(detail=True, methods=["GET", "PATCH"])(method)

                        # Set the method as a attribute of the class that implements this
                        # metaclass
                        setattr(_class, transition.name, wrapped_method)

        return _class


class FSMViewSetMixin(metaclass=FSMViewSetMixinMetaclass):
    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, TransitionNotAllowed):
            return Response({"non_field_errors": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)

    def fsm_route(
        self, request: Request, transition: Transition, fsm_field_name: str, serializer_class=None
    ) -> Response:
        action = transition.name
        obj = self.get_object()

        if not serializer_class:
            serializer_class = self.get_serializer_class()
        serializer_context = self.get_serializer_context()

        if request.method == "GET":
            return Response(serializer_class(instance=obj, context=serializer_context).data)

        serializer = serializer_class(instance=obj, data=request.data, partial=True, context=serializer_context)
        if serializer.is_valid():
            if len(serializer.validated_data) > 0:
                obj = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        errors = None
        if (can_action_method := getattr(obj, f"can_{action}", None)) and callable(can_action_method):
            errors = can_action_method()

        if errors is None or len(errors.keys()) == 0:
            obj.fsm_context = {"current_user": request.user, "request": request}
            if getattr(obj, fsm_field_name) != transition.target:
                if (action_method := getattr(obj, action, None)) and callable(action_method):
                    warnings = action_method(by=request.user)
                    obj.save()
                    if (post_action_method := getattr(obj, f"post_{action}", None)) and callable(post_action_method):
                        post_action_method(by=request.user)
                    # we extend the framework to allow action to successfully return but notify any possible warning. We use the message framework to communicate these warnings to the user
                    if warnings:
                        html = "<ul>" + "".join(f"<li>{e}</li>" for e in warnings) + "</ul>"
                        warning(request, html, extra_tags="auto_close=0")

            serializer = serializer_class(instance=obj, context=serializer_context)
            storage = get_messages(request._request)
            data = {"instance": serializer.data}
            if isinstance(storage, InMemoryMessageStorage):
                data["messages"] = list(storage.serialize_messages())
            return Response(data)

        return Response(errors, status=status.HTTP_412_PRECONDITION_FAILED)
