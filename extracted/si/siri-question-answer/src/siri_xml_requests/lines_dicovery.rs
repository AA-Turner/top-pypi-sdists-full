use quick_xml::events::{BytesEnd, BytesStart, BytesText, Event};
use serde::Serialize;
use crate::{create_soap_envelope, SIRI_NS, SOAP_NS, SW_NS};
use super::SoapRequestParams;

#[derive(Debug, Serialize)]
pub struct LinesDiscoveryRequest {
    pub params: SoapRequestParams,
}

impl LinesDiscoveryRequest {
    pub fn new(params: SoapRequestParams) -> Self {
        Self { params}
    }

    pub fn create_lines_discovery_request(
        &mut self,
    ) -> Result<String, quick_xml::Error> {
        let mut writer = create_soap_envelope(SOAP_NS)?;
        let body = BytesStart::new("S:Body");
        writer.write_event(Event::Start(body))?;
    
        // LinesDiscovery element
        let mut lines_discovery = BytesStart::new("sw:LinesDiscovery");
        lines_discovery.push_attribute(("xmlns:sw", SW_NS));
        lines_discovery.push_attribute(("xmlns:siri", SIRI_NS));
        writer.write_event(Event::Start(lines_discovery))?;
    
        // Request section
        writer.write_event(Event::Start(BytesStart::new("Request")))?;
    
        // RequestTimestamp
        writer.write_event(Event::Start(BytesStart::new("siri:RequestTimestamp")))?;
        writer.write_event(Event::Text(BytesText::new(&self.params.timestamp)))?;
        writer.write_event(Event::End(BytesEnd::new("siri:RequestTimestamp")))?;
    
        // RequestorRef
        writer.write_event(Event::Start(BytesStart::new("siri:RequestorRef")))?;
        writer.write_event(Event::Text(BytesText::new(&self.params.requestor_ref)))?;
        writer.write_event(Event::End(BytesEnd::new("siri:RequestorRef")))?;
    
        // MessageIdentifier
        writer.write_event(Event::Start(BytesStart::new("siri:MessageIdentifier")))?;
        writer.write_event(Event::Text(BytesText::new(&self.params.message_id)))?;
        writer.write_event(Event::End(BytesEnd::new("siri:MessageIdentifier")))?;
    
        // Close Request element
        writer.write_event(Event::End(BytesEnd::new("Request")))?;
    
        // Empty RequestExtension
        writer.write_event(Event::Empty(BytesStart::new("RequestExtension")))?;
    
        // Close all elements
        writer.write_event(Event::End(BytesEnd::new("sw:LinesDiscovery")))?;
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
    fn test_create_lines_discovery_request() {
        let mut request = LinesDiscoveryRequest::new(SoapRequestParams {
            timestamp: "2021-09-01T12:00:00Z".to_string(),
            requestor_ref: "test".to_string(),
            message_id: "1234".to_string(),
        });

        let result = request.create_lines_discovery_request().unwrap();
        let expected = r#"<?xml version="1.0" encoding="UTF-8"?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><sw:LinesDiscovery xmlns:sw="http://wsdl.siri.org.uk" xmlns:siri="http://www.siri.org.uk/siri"><Request><siri:RequestTimestamp>2021-09-01T12:00:00Z</siri:RequestTimestamp><siri:RequestorRef>test</siri:RequestorRef><siri:MessageIdentifier>1234</siri:MessageIdentifier></Request><RequestExtension/></sw:LinesDiscovery></S:Body></S:Envelope>"#;
        assert_eq!(result, expected);
    }
}
