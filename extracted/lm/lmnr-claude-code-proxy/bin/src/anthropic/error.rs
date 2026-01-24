use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct ApiError {
    #[serde(rename = "type")]
    pub error_type: ErrorType,
    pub message: String,
}

#[derive(Debug, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub enum ErrorType {
    InvalidRequestError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    RateLimitError,
    ApiError,
    OverloadedError,
}
