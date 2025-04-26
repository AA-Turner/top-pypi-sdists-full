use std::io::Cursor;
use quick_xml::{events::{BytesEnd, BytesStart, BytesText, Event}, Writer};
use crate::{SIRI_NS, SW_NS, SOAP_NS, create_soap_envelope};
use super::SoapRequestParams;


pub struct EstimatedTableRequest {
    pub writer: Writer<Cursor<Vec<u8>>>,
    pub params: SoapRequestParams,
}


/// Write an element with the given name and value to the writer.
/// 
/// # Parameters
/// 
/// - `writer` - The writer to write the element to.
/// - `name` - The name of the element.
/// - `value` - The value of the element.
/// 
/// # Returns
/// 
/// Ok if the element was written successfully.
fn write_element(
    writer: &mut Writer<Cursor<Vec<u8>>>,
    name: &str,
    value: &str,
) -> Result<(), quick_xml::Error> {
    writer.write_event(Event::Start(BytesStart::new(name)))?;
    writer.write_event(Event::Text(BytesText::new(value)))?;
    writer.write_event(Event::End(BytesEnd::new(name)))?;
    Ok(())
}


impl EstimatedTableRequest {
    pub fn new(params: SoapRequestParams) -> Self {
        let writer = Writer::new(Cursor::new(Vec::new()));
        Self { params, writer }
    }
    
    /// Create a SOAP request to get the estimated timetable for the given lines.
    /// 
    /// # Parameters
    /// 
    /// - `lines` - The lines to get the estimated timetable for.
    /// 
    /// # Returns
    /// 
    /// The XML string for the SOAP request.
    pub fn create_estimated_table_request(&self, lines: Vec<String>) -> Result<String, quick_xml::Error> {
        let mut writer = create_soap_envelope(SOAP_NS)?;

        // Body
        writer.write_event(Event::Start(BytesStart::new("S:Body")))?;

        // GetEstimatedTimetable element
        let mut get_estimated = BytesStart::new("sw:GetEstimatedTimetable");
        get_estimated.push_attribute(("xmlns:sw", SW_NS));
        get_estimated.push_attribute(("xmlns:siri", SIRI_NS));
        writer.write_event(Event::Start(get_estimated))?;

        // ServiceRequestInfo
        writer.write_event(Event::Start(BytesStart::new("ServiceRequestInfo")))?;
        
        write_element(&mut writer, "siri:RequestTimestamp", &self.params.timestamp)?;
        write_element(&mut writer, "siri:RequestorRef", &self.params.requestor_ref)?;
        write_element(&mut writer, "siri:MessageIdentifier", &self.params.message_id)?;
        
        writer.write_event(Event::End(BytesEnd::new("ServiceRequestInfo")))?;

        // Request
        writer.write_event(Event::Start(BytesStart::new("Request")))?;
        
        write_element(&mut writer, "siri:RequestTimestamp", &self.params.timestamp)?;
        write_element(&mut writer, "siri:MessageIdentifier", &self.params.message_id)?;

        // Lines
        writer.write_event(Event::Start(BytesStart::new("siri:Lines")))?;
        for line_ref in lines {
            writer.write_event(Event::Start(BytesStart::new("siri:LineDirection")))?;
            write_element(&mut writer, "siri:LineRef", &line_ref)?;
            writer.write_event(Event::End(BytesEnd::new("siri:LineDirection")))?;
        }
        writer.write_event(Event::End(BytesEnd::new("siri:Lines")))?;

        writer.write_event(Event::End(BytesEnd::new("Request")))?;

        // RequestExtension
        writer.write_event(Event::Empty(BytesStart::new("RequestExtension")))?;

        // Close all elements
        writer.write_event(Event::End(BytesEnd::new("sw:GetEstimatedTimetable")))?;
        writer.write_event(Event::End(BytesEnd::new("S:Body")))?;
        writer.write_event(Event::End(BytesEnd::new("S:Envelope")))?;

        let result = writer.into_inner().into_inner();
        let result = String::from_utf8(result).unwrap();
        Ok(result)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_estimated_table_request() {
        let request = EstimatedTableRequest::new(SoapRequestParams {
            timestamp: "2021-09-01T12:00:00Z".to_string(),
            requestor_ref: "Hove".to_string(),
            message_id: "Hove::Message::1234".to_string(),
        });

        let lines = vec!["1".to_string(), "2".to_string()];
        let result = request.create_estimated_table_request(lines).unwrap();
        let expected = r#"<?xml version="1.0" encoding="UTF-8"?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><sw:GetEstimatedTimetable xmlns:sw="http://wsdl.siri.org.uk" xmlns:siri="http://www.siri.org.uk/siri"><ServiceRequestInfo><siri:RequestTimestamp>2021-09-01T12:00:00Z</siri:RequestTimestamp><siri:RequestorRef>Hove</siri:RequestorRef><siri:MessageIdentifier>Hove::Message::1234</siri:MessageIdentifier></ServiceRequestInfo><Request><siri:RequestTimestamp>2021-09-01T12:00:00Z</siri:RequestTimestamp><siri:MessageIdentifier>Hove::Message::1234</siri:MessageIdentifier><siri:Lines><siri:LineDirection><siri:LineRef>1</siri:LineRef></siri:LineDirection><siri:LineDirection><siri:LineRef>2</siri:LineRef></siri:LineDirection></siri:Lines></Request><RequestExtension/></sw:GetEstimatedTimetable></S:Body></S:Envelope>"#;
        assert_eq!(result, expected);
    }
}