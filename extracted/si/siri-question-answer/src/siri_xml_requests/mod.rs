use serde::Serialize;

pub mod lines_dicovery;
pub mod estimated_table;


#[derive(Debug, Serialize)]
pub struct SoapRequestParams {
    pub timestamp: String,
    pub requestor_ref: String,
    pub message_id: String,
}

