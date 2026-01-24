from typing import Any, List, Optional

from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.core import checks
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import cached_property
from django_better_admin_arrayfield.models.fields import ArrayField
from igraph import Graph

from wbcore.signals.models import get_dependant_dynamic_fields_instances

from ..workers import Queue
from .fields import DynamicDecimalField, DynamicFloatField


class DynamicMetaClass(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        # Construct dependencies graph
        dynamic_field_names = {
            field.name: field.dependencies
            for field in new_class._meta.fields
            if type(field) in [DynamicFloatField, DynamicDecimalField]
        }
        ordered_dependencies_fields = []
        if dynamic_field_names:
            g = Graph(len(dynamic_field_names), directed=True)
            # label vertices
            g.vs["name"] = list(dynamic_field_names.keys())
            for field_name, dependencies in dynamic_field_names.items():
                for dependency in dependencies:
                    g[dependency, field_name] = 1
            # Store dynamic field ordered by topological sorting
            ordered_dependencies_fields = [g.vs[v_id]["name"] for v_id in g.topological_sorting()]
        new_class.add_to_class("ordered_dependencies_fields", ordered_dependencies_fields)
        return new_class


class DynamicModel(models.Model, metaclass=DynamicMetaClass):
    DATE_RANGE_UPPER_FIELD_NAME = "date"
    DATE_RANGE_LOWER_FIELD_NAME = "date"

    lock_all_dynamic_fields = models.BooleanField(
        default=False, help_text="If True, will not allow dynamic fields to be updated"
    )
    locked_dynamic_fields = ArrayField(
        models.CharField(
            max_length=128,
        ),
        blank=True,
        default=list,
    )
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_static_locked_fields(cls) -> list[str]:
        """
        Override if the model needs to define a set of dynamic fields that can only be set when the value is null

        Returns:
            Return a list of field names
        """
        return []

    @cached_property
    def _locked_fields(self) -> set[str]:
        return set(self.locked_dynamic_fields + self.get_static_locked_fields())

    def set_dynamic_field(
        self,
        update_all_dynamic_fields: bool,
        update_only_fields: list[str] | None = None,
        update_exclude_fields: list[str] | None = None,
    ):
        if not update_only_fields:
            update_only_fields = []
        if not update_exclude_fields:
            update_exclude_fields = []
        # Loop over the dynamic field ordered by their place in the dependency graph
        for dynamic_field_name in self.ordered_dependencies_fields:
            # Check if field value is not assigned or if we explicitly want to override its value
            if (
                not self.lock_all_dynamic_fields
                and (
                    getattr(self, dynamic_field_name, None) is None
                    or (
                        dynamic_field_name not in self._locked_fields
                        and (update_all_dynamic_fields or dynamic_field_name in update_only_fields)
                    )
                )
            ) and dynamic_field_name not in update_exclude_fields:
                # call the appropriate callback and check if this is a function
                if (
                    (compute_function := getattr(self, f"_compute_{dynamic_field_name}", None))
                    and (callable(compute_function))
                    and (res := compute_function()) is not None
                ):
                    setattr(self, dynamic_field_name, res)

    @classmethod
    def update_dynamic_fields_of_dependant_objects(
        cls,
        updated_instance,
        already_visited_instances: set[Any] | None = None,
        update_all_dynamic_fields: bool | None = True,
    ):
        if not already_visited_instances:
            already_visited_instances = set()
        for _, dependant_instance_generator in get_dependant_dynamic_fields_instances.send(
            sender=updated_instance.__class__, instance=updated_instance
        ):
            for dependant_instance in dependant_instance_generator:
                if dependant_instance not in already_visited_instances:
                    dependant_instance.set_dynamic_field(update_all_dynamic_fields)
                    already_visited_instances.add(updated_instance)
                    DynamicModel.update_dynamic_fields_of_dependant_objects(
                        dependant_instance, already_visited_instances=already_visited_instances
                    )

    def save(
        self,
        *args,
        update_all_dynamic_fields: Optional[bool] = False,
        update_only_fields: Optional[List] = None,
        update_exclude_fields: Optional[List] = None,
        set_dynamic_field_on_save: Optional[bool] = True,
        **kwargs,
    ):
        if set_dynamic_field_on_save:
            self.set_dynamic_field(update_all_dynamic_fields, update_only_fields, update_exclude_fields)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


@shared_task(queue=Queue.DEFAULT.value)
def set_dynamic_field_as_task(content_type_id, object_id, **kwargs):
    content_type = ContentType.objects.get(id=content_type_id)
    instance = content_type.model_class().objects.get(id=object_id)
    instance.set_dynamic_field(True, **kwargs)
    instance.save()


class WBModel(models.Model):
    """Implements checks on the model class"""

    id: int

    class Meta:
        abstract = True

    @classmethod
    def _check_model_methods(cls) -> list[checks.Error]:
        methods_to_check = [
            "get_endpoint_basename",
            "get_representation_value_key",
            "get_representation_endpoint",
            "get_representation_label_key",
        ]
        method_errors = []
        for method in methods_to_check:
            if not hasattr(cls._meta.model, method):
                method_errors.append(checks.Error(f"{cls._meta.model.__name__} does not have method {method}"))
        return method_errors

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_model_methods())
        return errors
