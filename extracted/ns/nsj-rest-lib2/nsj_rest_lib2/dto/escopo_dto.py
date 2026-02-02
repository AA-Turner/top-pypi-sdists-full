import uuid

from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.descriptor.dto_field_validators import DTOFieldValidators
from nsj_rest_lib.dto.dto_base import DTOBase


def _validate_service_account(dto_field: DTOField, value):
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError(
            f"{dto_field.storage_name} deve ser do tipo string. Valor recebido: {value}."
        )

    value = value.strip()

    if not value.startswith("serv_acc_"):
        raise ValueError(
            f"{dto_field.storage_name} deve comecar com \"serv_acc_\". Valor recebido: {value}."
        )

    return DTOFieldValidators().validate_email(dto_field, value)


@DTO()
class EscopoDTO(DTOBase):

    id: uuid.UUID = DTOField(
        pk=True,
        resume=True,
        not_null=True,
        default_value=uuid.uuid4,
        strip=True,
        min=36,
        max=36,
        validator=DTOFieldValidators().validate_uuid,
    )

    codigo: str = DTOField(
        resume=True,
        not_null=True,
        strip=True,
        min=1,
        max=100,
        unique="escopo_codigo",
        candidate_key=True,
    )

    service_account: str = DTOField(
        resume=True,
        strip=True,
        min=5,
        max=320,
        validator=_validate_service_account,
    )
