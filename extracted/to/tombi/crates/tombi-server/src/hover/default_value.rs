#[derive(Debug, Clone)]
pub enum DefaultValue {
    Boolean(bool),
    Integer(i64),
    Float(f64),
    String(String),
    OffsetDateTime(String),
    LocalDateTime(String),
    LocalDate(String),
    LocalTime(String),
    Array(Vec<DefaultValue>),
    Table(Vec<(String, DefaultValue)>),
}

impl std::fmt::Display for DefaultValue {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DefaultValue::Boolean(boolean) => write!(f, "{}", boolean),
            DefaultValue::Integer(integer) => write!(f, "{}", integer),
            DefaultValue::Float(float) => write!(f, "{}", float),
            DefaultValue::String(string) => write!(f, "\"{}\"", string.replace("\"", "\\\"")),
            DefaultValue::OffsetDateTime(offset_date_time) => write!(f, "{}", offset_date_time),
            DefaultValue::LocalDateTime(local_date_time) => write!(f, "{}", local_date_time),
            DefaultValue::LocalDate(local_date) => write!(f, "{}", local_date),
            DefaultValue::LocalTime(local_time) => write!(f, "{}", local_time),
            DefaultValue::Array(array) => {
                write!(f, "[")?;
                for (i, value) in array.iter().enumerate() {
                    if i > 0 {
                        write!(f, ", ")?;
                    }
                    write!(f, "{}", value)?;
                }
                write!(f, "]")
            }
            DefaultValue::Table(table) => {
                write!(f, "{{ ")?;
                for (i, (key, value)) in table.iter().enumerate() {
                    if i > 0 {
                        write!(f, ", ")?;
                    }
                    write!(f, "{}: {}", key, value)?;
                }
                write!(f, " }}")
            }
        }
    }
}
