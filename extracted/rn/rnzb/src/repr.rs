use chrono::SecondsFormat;

use crate::tuple::Tuple;

pub(crate) trait PyRepr {
    /// Provides a string representation intended to mimic Python's built-in `__repr__` method.
    fn pyrepr(&self) -> String;
}

impl PyRepr for String {
    fn pyrepr(&self) -> String {
        format!("'{}'", &self.replace("'", "\\'"))
    }
}

impl PyRepr for str {
    fn pyrepr(&self) -> String {
        format!("'{}'", &self.replace("'", "\\'"))
    }
}

impl PyRepr for bool {
    fn pyrepr(&self) -> String {
        if *self {
            "True".to_string()
        } else {
            "False".to_string()
        }
    }
}

impl PyRepr for u32 {
    fn pyrepr(&self) -> String {
        self.to_string()
    }
}

impl<T: PyRepr> PyRepr for Option<T> {
    fn pyrepr(&self) -> String {
        match self {
            Some(value) => value.pyrepr(),
            None => "None".to_string(),
        }
    }
}

impl PyRepr for chrono::DateTime<chrono::Utc> {
    fn pyrepr(&self) -> String {
        self.to_rfc3339_opts(SecondsFormat::AutoSi, true).pyrepr()
    }
}

impl<T: PyRepr> PyRepr for Tuple<T> {
    fn pyrepr(&self) -> String {
        // Handle empty tuple
        if self.0.is_empty() {
            return "()".to_string();
        }

        // Handle single element tuple (with trailing comma)
        if self.0.len() == 1 {
            return format!("({},)", self.0[0].pyrepr());
        }

        // Handle multiple elements
        format!(
            "({})",
            self.0
                .iter()
                .map(|x| x.pyrepr())
                .collect::<Vec<_>>()
                .join(", ")
        )
    }
}
