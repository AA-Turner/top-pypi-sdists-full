from django.db import models

from wbcore.models.orderable import OrderableModel


class ForeignKeyClass(models.Model):  # noqa
    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbcore:foreignkeyclass"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"


class OrderableChild(OrderableModel):
    PARTITION_BY = "partition_fk"

    partition_fk = models.ForeignKey(
        to=ForeignKeyClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbcore:orderablechild"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"
