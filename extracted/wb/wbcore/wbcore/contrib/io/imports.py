import enum
from collections.abc import Iterable
from contextlib import suppress
from decimal import Decimal
from typing import Any, Dict, List, Optional, Type

import numpy as np
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import Model
from tqdm import tqdm

from .exceptions import DeserializationError, ImportError
from .models import ImportedObjectProviderRelationship, ImportSource
from .utils import nest_row


class ImportState(enum.Enum):
    CREATED = 0
    MODIFIED = 1
    UNMODIFIED = 2


class ImportExportHandler:
    MAX_ALLOWED_LOG_SIZE: int = 2e6
    MODEL_APP_LABEL: str = None

    def __init__(self, import_source: ImportSource, **kwargs):
        self.import_source: ImportSource = import_source
        self.model: Type[Model] = apps.get_model(self.MODEL_APP_LABEL)

    def _inject_internal_id_from_data(self, data: dict[str, Any]) -> tuple[int, ContentType] | None:
        if provider_id := data.pop("provider_id", None):
            if content_type_id := data.pop("content_type", None):
                content_type = ContentType.objects.get(id=content_type_id)
            else:
                content_type = ContentType.objects.get_for_model(self.model)

            if internal_object := self.import_source.source.data_backend.get_internal_object(
                content_type, provider_id
            ):
                data["id"] = internal_object.id
            else:
                return provider_id, content_type

    def _model_dict_diff(self, model: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Given a model and its dictionary representation, compare them and find out the fields that are different
        Args:
            model: The base instance
            data: The updated instance as a dictionary representation

        Returns:
            a dictionary containing the changed field and its value
        """
        change_data = dict()
        for k, v in data.items():
            if v is not None and hasattr(model, k):
                field = getattr(model, k)
                if isinstance(field, models.Manager):
                    res_list = []
                    if not isinstance(v, Iterable):
                        v = [v]
                    for vv in v:
                        if vv is not None and vv not in field.all():
                            res_list.append(vv)
                    if res_list:
                        change_data[k] = res_list
                else:
                    with suppress(FieldDoesNotExist):
                        field_obj = model._meta.get_field(k)
                        if v in [np.nan, np.inf, -np.inf]:
                            v = None
                        if v is not None:
                            if isinstance(field_obj, models.DecimalField):
                                v = round(Decimal(v), field_obj.decimal_places)
                            if isinstance(field_obj, models.FloatField):
                                v = float(v)
                            if isinstance(field_obj, models.IntegerField):
                                v = int(v)
                            if isinstance(field_obj, models.CharField):
                                v = str(v)
                            if isinstance(field, models.Model) and isinstance(v, models.Model):
                                if v.pk != field.pk:
                                    change_data[k] = v
                                # v = field.__class__.objects.get(id=v.pk) # not sure why this was there. We comment it out and monitor
                    if k not in change_data and field != v:
                        change_data[k] = v
        return change_data

    def _deserialize(self, data: Dict[str, Any]):
        """
        Convert the data from the parser to a valid model representation
        Args:
            import_source: The import source
            data: the serialized data

        Returns:
            The deserialized data
        """
        pass

    def _save_object(self, _object, **kwargs):
        save_kwargs = {}
        from wbcore.models import DynamicModel  # TODO: circular dependency

        if isinstance(_object, DynamicModel):
            save_kwargs = {
                "set_dynamic_field_on_save": getattr(self, "set_dynamic_field_on_save", True),
                "update_all_dynamic_fields": getattr(self, "update_all_dynamic_fields", True),
                "update_exclude_fields": set(
                    getattr(self, "update_exclude_fields", []) + kwargs.get("update_exclude_fields", [])
                ),
            }
        _object.save(**save_kwargs)
        return _object

    def _data_changed(
        self,
        _object,
        change_data: Dict[str, Any],
        initial_data: Dict[str, Any],
        include_update_fields: list[str] | None = None,
        exclude_update_fields: list[str] | None = None,
    ):
        """
        When data has changed, this function is called and handle the logic to update the instance
        Args:
            _object: The instance that needs to be updated
            change_data: The changed data
            initial_data: The initial data
            include_update_fields: If specified, only these fields will be updated
            exclude_update_fields: If specified, will exclude these fields from being updated
        """
        if not include_update_fields:
            include_update_fields = getattr(self, "include_update_fields", None)
        if not exclude_update_fields:
            exclude_update_fields = getattr(self, "exclude_update_fields", None)
        first_level_dict = dict()
        for k, v in change_data.items():
            if (include_update_fields is not None and k not in include_update_fields) or (
                exclude_update_fields is not None and k in exclude_update_fields and getattr(_object, k)
            ):
                pass
            else:
                if v is not None:
                    _v = getattr(_object, k)
                    if getattr(_v, "add", None) and v:
                        if isinstance(v, Iterable):
                            for elem in v:
                                if elem:
                                    _v.add(elem)
                        else:
                            _v.add(v)
                        self.import_source.log += f"\n{k}: Add {v} to manytomany list"
                    else:
                        setattr(_object, k, v)
                        self.import_source.log += f"\n{k}: {_v} => {v}"
                    first_level_dict[k] = v
        if first_level_dict:
            _object.import_source = self.import_source
            try:
                self._save_object(_object, update_exclude_fields=list(initial_data.keys()))
            except Exception as e:
                error_msg = f"\nError {e} while saving data {change_data} for object id {_object.pk}"
                self.import_source.log += error_msg
                if not getattr(self, "allow_update_save_failure", False):
                    raise ImportError(error_msg)
            return True
        return False

    def _create_instance(self, data: Dict[str, Any], **kwargs) -> models.Model:
        """
        Resource function to create the object given its deserialized data
        Args:
            data: The deserialized data

        Returns:
            The created object
        """
        self.import_source.log += f"\nCreate {self.model.__class__.__name__}."
        _object = self.model(import_source=self.import_source, **data)
        return self._save_object(_object)

    def _get_instance(self, data: Dict[str, Any], history: Optional[models.QuerySet] = None, **kwargs) -> Any | None:
        """
        Usually overriden by the resource to define how the object needs to be query given the deserialized data
        Args:
            data: deserialized data
            history: In case of historical import, specify a dictionary of history datapoints

        Returns:
            Thre retreived object (if it exists), None otherwise
        """
        return None

    def _get_history(self, history: Dict[str, str]) -> models.QuerySet | None:
        return self.model.objects.none()

    def _pre_processing_object(self, data: Dict[str, str]):
        pass

    def _process_raw_data(self, data: Dict[str, Any]):
        pass

    def _post_processing_created_object(self, _object: models.Model):
        pass

    def _post_processing_updated_object(self, _object: models.Model):
        pass

    def _post_processing_history(self, history: models.QuerySet):
        pass

    def _post_processing_objects(
        self,
        created_objs: List[models.Model],
        modified_objs: List[models.Model],
        unmodified_objs: List[models.Model],
    ):
        pass

    def process_object(
        self,
        data: Dict[str, Any],
        history: Optional[models.QuerySet] = None,
        read_only=False,
        include_update_fields=None,
        raise_exception: bool = True,
        **kwargs,
    ):
        data = nest_row(data)
        inject_internal_id_res = self._inject_internal_id_from_data(data)
        if history is None:
            history = self.model.objects.none()
        self._deserialize(data)
        if not data:
            raise DeserializationError("Data dictionary is empty")
        self._pre_processing_object(data)
        import_state = ImportState.UNMODIFIED
        _object = self._get_instance(data, history=history, **kwargs)
        if _object:
            change_data = self._model_dict_diff(_object, data)
            different = len(change_data.keys()) > 0
            if different and not read_only:
                is_modified = self._data_changed(
                    _object, change_data, data, include_update_fields=include_update_fields
                )
                if is_modified:
                    import_state = ImportState.MODIFIED
                self._post_processing_updated_object(_object)
        elif not read_only:
            _object = self._create_instance(data, **kwargs)
            self._post_processing_created_object(_object)
            import_state = ImportState.CREATED
        if not _object and raise_exception:
            data_repr = " ".join([f'{k}="{v}"' for k, v in data.items()])
            raise DeserializationError(f"{self.model._meta.verbose_name} data couldn't be parsed ({data_repr})")
        if inject_internal_id_res:
            ImportedObjectProviderRelationship.objects.get_or_create(
                object_id=_object.pk,
                content_type=inject_internal_id_res[1],
                provider=self.import_source.source.data_backend.provider,
                defaults={"provider_identifier": inject_internal_id_res[0]},
            )

        return _object, import_state

    def process(self, import_data, debug: bool = False, with_post_processing: bool = True, **kwargs):
        data = import_data["data"]
        self._process_raw_data(import_data)

        if history_data := import_data.get("history", None):
            history = self._get_history(history_data)
        else:
            history = self.model.objects.none()

        created_objs = []
        modified_objs = []
        unmodified_objs = []
        gen = data if not debug else tqdm(data, total=len(data))
        for _data in gen:
            try:
                _object, import_state = self.process_object(_data, history=history)
                if history.exists() and _object:
                    history = history.exclude(id=_object.pk)

                if import_state == ImportState.CREATED:
                    created_objs.append(_object)
                elif import_state == ImportState.MODIFIED:
                    modified_objs.append(_object)
                else:
                    unmodified_objs.append(_object)
                if (
                    len(self.import_source.log) > self.MAX_ALLOWED_LOG_SIZE
                ):  # In case we are exceedning the max log size, we reset the log to avoid issue when saving it
                    self.import_source.log = ""
            except DeserializationError as e:
                self.import_source.errors_log += f"Row {self.import_source.progress_index}: {str(e)}\n"
            self.import_source.progress_index += 1
        if with_post_processing:
            if history.exists():
                self._post_processing_history(history)
            self._post_processing_objects(created_objs, modified_objs, unmodified_objs)

        self.import_source.save()
