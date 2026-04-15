use chalk_proto::chalk::arrow::v1::{arrow_type::ArrowTypeEnum, ArrowType, Field};

/// Convert an ArrowType proto to a Python type annotation string.
pub fn arrow_type_to_python(arrow: &ArrowType) -> String {
    let Some(ref variant) = arrow.arrow_type_enum else {
        return "Any".to_string();
    };
    arrow_type_enum_to_python(variant)
}

fn arrow_type_enum_to_python(variant: &ArrowTypeEnum) -> String {
    match variant {
        ArrowTypeEnum::None(_) => "None".to_string(),
        ArrowTypeEnum::Bool(_) => "bool".to_string(),

        ArrowTypeEnum::Int8(_)
        | ArrowTypeEnum::Int16(_)
        | ArrowTypeEnum::Int32(_)
        | ArrowTypeEnum::Int64(_)
        | ArrowTypeEnum::Uint8(_)
        | ArrowTypeEnum::Uint16(_)
        | ArrowTypeEnum::Uint32(_)
        | ArrowTypeEnum::Uint64(_) => "int".to_string(),

        ArrowTypeEnum::Float16(_) | ArrowTypeEnum::Float32(_) | ArrowTypeEnum::Float64(_) => {
            "float".to_string()
        }

        ArrowTypeEnum::Utf8(_) | ArrowTypeEnum::LargeUtf8(_) => "str".to_string(),

        ArrowTypeEnum::Binary(_) | ArrowTypeEnum::LargeBinary(_) | ArrowTypeEnum::FixedSizeBinary(_) => {
            "bytes".to_string()
        }

        ArrowTypeEnum::Timestamp(_) => "datetime.datetime".to_string(),
        ArrowTypeEnum::Date32(_) | ArrowTypeEnum::Date64(_) => "datetime.date".to_string(),
        ArrowTypeEnum::Time32(_) | ArrowTypeEnum::Time64(_) => "datetime.time".to_string(),
        ArrowTypeEnum::Duration(_) => "datetime.timedelta".to_string(),

        ArrowTypeEnum::Decimal128(_) | ArrowTypeEnum::Decimal256(_) => {
            "decimal.Decimal".to_string()
        }

        ArrowTypeEnum::List(list) | ArrowTypeEnum::LargeList(list) => {
            let elem_type = list
                .field_type
                .as_ref()
                .and_then(|f| f.arrow_type.as_ref())
                .map(|at| arrow_type_to_python(at))
                .unwrap_or_else(|| "Any".to_string());
            format!("list[{elem_type}]")
        }

        ArrowTypeEnum::FixedSizeList(fsl) => {
            let elem_type = fsl
                .field_type
                .as_ref()
                .and_then(|f| f.arrow_type.as_ref())
                .map(|at| arrow_type_to_python(at))
                .unwrap_or_else(|| "Any".to_string());
            format!("list[{elem_type}]")
        }

        ArrowTypeEnum::Map(map) => {
            let key_type = map
                .key_field
                .as_ref()
                .and_then(|f| f.arrow_type.as_ref())
                .map(|at| arrow_type_to_python(at))
                .unwrap_or_else(|| "Any".to_string());
            let val_type = map
                .item_field
                .as_ref()
                .and_then(|f| f.arrow_type.as_ref())
                .map(|at| arrow_type_to_python(at))
                .unwrap_or_else(|| "Any".to_string());
            format!("dict[{key_type}, {val_type}]")
        }

        ArrowTypeEnum::Struct(s) => struct_to_python(&s.sub_field_types),

        ArrowTypeEnum::Extension(ext) => {
            if ext.name == "arrow.json" {
                "Any".to_string()
            } else if let Some(ref storage) = ext.storage_type {
                arrow_type_to_python(storage)
            } else {
                "Any".to_string()
            }
        }
    }
}

/// Convert a struct type to a Python TypedDict-style annotation.
/// For simplicity, we use `dict[str, Any]` — the caller can generate
/// a proper TypedDict if needed.
fn struct_to_python(_fields: &[Field]) -> String {
    "dict[str, Any]".to_string()
}
