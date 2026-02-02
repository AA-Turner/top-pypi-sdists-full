import uuid

from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.decorator.entity import Entity


@Entity(
    table_name="restlib2.escopo",
    pk_field="id",
    default_order_fields=["codigo", "id"],
)
class EscopoEntity(EntityBase):
    id: uuid.UUID = None
    codigo: str = None
    service_account: str = None
