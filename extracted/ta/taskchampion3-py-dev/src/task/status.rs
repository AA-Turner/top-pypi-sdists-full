use pyo3::{exceptions::PyValueError, prelude::*};
pub use taskchampion::Status as TCStatus;

#[pyclass(from_py_object, eq, eq_int)]
#[derive(Clone, Copy, PartialEq)]
pub enum Status {
    Pending,
    Completed,
    Deleted,
    Recurring,
    // Read-only sentinel. `TCStatus::Unknown(String)` carries a free-form
    // string that this unit-only enum cannot represent; writing back via
    // `Status::Unknown` is rejected by `TryFrom` to avoid silent corruption.
    Unknown,
}

impl From<TCStatus> for Status {
    fn from(status: TCStatus) -> Self {
        match status {
            TCStatus::Pending => Status::Pending,
            TCStatus::Completed => Status::Completed,
            TCStatus::Deleted => Status::Deleted,
            TCStatus::Recurring => Status::Recurring,
            _ => Status::Unknown,
        }
    }
}

impl TryFrom<Status> for TCStatus {
    type Error = PyErr;

    fn try_from(status: Status) -> Result<Self, Self::Error> {
        match status {
            Status::Pending => Ok(TCStatus::Pending),
            Status::Completed => Ok(TCStatus::Completed),
            Status::Deleted => Ok(TCStatus::Deleted),
            Status::Recurring => Ok(TCStatus::Recurring),
            Status::Unknown => Err(PyValueError::new_err(
                "Status.Unknown cannot be set: the original status string is not preserved on read. \
                 Use Task.set_value(\"status\", \"<value>\", ops) to set a custom status.",
            )),
        }
    }
}
