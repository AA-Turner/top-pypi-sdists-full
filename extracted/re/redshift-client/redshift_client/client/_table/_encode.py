from redshift_client.core.data_type.core import (
    DataType,
)


def encode_data_type(d_type: DataType) -> str:
    return d_type.map(
        lambda s: s.value,
        lambda p: f"{p.data_type.value}({p.precision})",
        lambda d: f"DECIMAL({d.precision},{d.scale})",
    )
