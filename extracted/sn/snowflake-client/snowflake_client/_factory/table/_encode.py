from redshift_client.core.data_type.core import (
    DataType,
    StaticTypes,
)


def _handle_static(static: StaticTypes) -> str:
    if static is StaticTypes.SUPER:
        return "VARIANT"
    return str(static.value)  # type: ignore[misc]


def encode_data_type(d_type: DataType) -> str:
    return d_type.map(
        _handle_static,
        lambda p: f"{p.data_type.value}({p.precision})",
        lambda d: f"DECIMAL({d.precision},{d.scale})",
    )
