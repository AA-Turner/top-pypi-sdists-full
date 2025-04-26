pub mod siri_xml_requests;
pub mod listeners;
pub mod transformers;
pub mod deserializers;

use std::io::Cursor;
use quick_xml::{events::{BytesDecl, BytesStart, Event}, Writer};
use reqwest::header;
use siri_xml_requests::SoapRequestParams;


pub const SOAP_NS: &str = "http://schemas.xmlsoap.org/soap/envelope/";
pub const SIRI_NS: &str = "http://www.siri.org.uk/siri";
pub const SW_NS: &str = "http://wsdl.siri.org.uk";


#[derive(Debug)]
pub struct Notification {
    pub message: String,
    pub _type: String,
}


/// Create a SOAP envelope with the given namespace.
/// 
/// # Parameters
/// 
/// - `soap_ns` - The namespace to use for the SOAP envelope.
/// 
/// # Returns
/// 
/// A quick-xml writer with the SOAP envelope written to it.
/// 
/// # Errors
/// 
/// If there is an error writing the envelope.
pub fn create_soap_envelope(soap_ns: &str) -> Result<Writer<Cursor<Vec<u8>>>, quick_xml::Error> {
    let mut writer = Writer::new(Cursor::new(Vec::new()));
    // XML declaration
    writer.write_event(Event::Decl(BytesDecl::new("1.0", Some("UTF-8"), None)))?;

    // SOAP Envelope
    let mut envelope = BytesStart::new("S:Envelope");
    envelope.push_attribute(("xmlns:S", soap_ns));
    envelope.push_attribute(("xmlns:SOAP-ENV", soap_ns));
    writer.write_event(Event::Start(envelope))?;
    Ok(writer)
}

/// Send a SOAP request to the given URL with the given XML string as the body.
/// 
/// # Parameters
/// 
/// - `client` - The reqwest client to use for the request.
/// - `url` - The URL to send the request to.
/// - `xml_string` - The XML string to use as the body of the request.
/// 
/// # Returns
/// 
/// The response from the server.
/// 
/// # Errors
/// 
/// If there is an error sending the request.
pub async fn send_soap_request<'a>(
    client: &reqwest::Client,
    url: &'a str,
    xml_string: &'a str,
) -> Result<reqwest::Response, reqwest::Error> {
    client
    .post(url)
    .header(header::CONTENT_TYPE, "text/xml; charset=utf-8")
    .header(header::ACCEPT, "text/xml")
    .body(xml_string.to_owned())
    .send()
    .await
}

/// Run the estimated timetable listener with the given URL, lines, interval, and sender.
/// 
/// # Parameters
/// 
/// - `url` - The URL to send the request to.
/// - `lines` - The lines to get the estimated timetable for.
/// - `interval` - The interval to wait between requests.
/// - `sender` - The sender to send the notifications to.
pub async fn run_estimated_table_listener(url: String, lines: Vec<String>, interval: u64, sender: tokio::sync::mpsc::UnboundedSender<Notification>) -> Result<(), Box<dyn std::error::Error>> {
    let handle = listeners::estimated_time_table::EstimatedTableListerner::run(url, lines, interval, sender);
    handle.await?;
    Ok(())
}


/// Launch a request to get the line discovery for a specific url.
/// 
/// # Parameters
/// 
/// - `client` - The reqwest client to use for the request.
/// - `url` - The URL to send the request to.
/// - `requestor_ref` - The requestor reference to use in the request.
/// 
/// # Returns
/// 
/// The response from the server.
/// 
/// # Errors
/// 
/// If there is an error sending the request.
pub async fn get_line_discovery(url: &str, requestor_ref: &str) -> Result<reqwest::Response, reqwest::Error> {
    let client = reqwest::Client::new();
    let id = uuid::Uuid::new_v4();
    let date = chrono::Utc::now();
    let message_id = format!("{}::Message::{}", requestor_ref, id.to_string());
    let soap_params = SoapRequestParams {
        timestamp: date.to_rfc3339(),
        requestor_ref: requestor_ref.to_uppercase().to_string(),
        message_id,
    };

    let mut line_request = siri_xml_requests::lines_dicovery::LinesDiscoveryRequest::new(soap_params);
    client
    .post(url)
    .header(header::CONTENT_TYPE, "text/xml; charset=utf-8")
    .header(header::ACCEPT, "text/xml")
    .body(line_request.create_lines_discovery_request().unwrap())
    .send()
    .await
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_soap_envelope() {
        let result = create_soap_envelope(SOAP_NS).unwrap();
        let expected = r#"<?xml version="1.0" encoding="UTF-8"?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">"#;
        assert_eq!(result.into_inner().into_inner(), expected.as_bytes());
    }
}