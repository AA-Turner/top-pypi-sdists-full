use quick_xml::de::from_str;
use serde::Deserialize;

#[derive(Debug, Deserialize, PartialEq, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct SoapEnvelope {
    #[serde(rename = "Header")]
    pub header: String,
    #[serde(rename = "Body")]
    pub body: SoapBody,
}

#[derive(Debug, Deserialize, PartialEq, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct SoapBody {
    pub siri: Siri,
}

#[derive(Debug, Deserialize, PartialEq, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct Siri {
    #[serde(rename = "LinesDelivery")]
    pub lines_delivery: LinesDelivery,
}

#[derive(Debug, Deserialize, PartialEq, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct LinesDelivery {
    pub response_timestamp: String,
    #[serde(rename = "AnnotatedLineRef")]
    pub annotated_line_refs: Vec<AnnotatedLineRef>,
}

#[derive(Debug, Deserialize, PartialEq, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct AnnotatedLineRef {
    #[serde(rename = "LineRef")]
    pub line_ref: String,
    #[serde(rename = "LineName")]
    pub line_name: String,
    #[serde(rename = "Monitored")]
    pub monitored: bool,
    #[serde(rename = "Destinations")]
    pub destinations: Destinations,
}

#[derive(Debug, Deserialize, PartialEq, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct Destinations {
    #[serde(rename = "Destination")]
    pub destination: Vec<Destination>,
}

#[derive(Debug, Deserialize, PartialEq, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct Destination {
    #[serde(rename = "DestinationRef")]
    pub destination_ref: String,
    #[serde(rename = "DirectionRef")]
    pub direction_ref: String,
}

/// Deserialize a LinesDelivery response from XML.
/// 
/// # Parameters
/// 
/// - `xml` - The XML to deserialize.
pub fn deserialize_lines_delivery(xml: &str) -> Result<SoapEnvelope, quick_xml::DeError> {
    from_str(xml)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_deserialize_lines_delivery() {
        let xml = r#"
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope/" soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding">
              <soap:Header></soap:Header>
              <soap:Body>
                <Siri xmlns="http://www.siri.org.uk/siri" xmlns:ns5="http://www.opengis.net/gml/3.2" xmlns:ns2="http://www.ifopt.org.uk/acsb" xmlns:ns4="http://datex2.eu/schema/2_0RC1/2_0" xmlns:ns3="http://www.ifopt.org.uk/ifopt">
                  <LinesDelivery version="1.0">
                    <ResponseTimestamp>2025-03-19T12:23:28.81575356Z</ResponseTimestamp>
                    <AnnotatedLineRef>
                      <LineRef>101</LineRef>
                      <LineName>T1</LineName>
                      <Monitored>true</Monitored>
                      <Destinations>
                        <Destination>
                          <DestinationRef>t_chal</DestinationRef>
                          <DirectionRef>Aller</DirectionRef>
                        </Destination>
                        <Destination>
                          <DestinationRef>t_hdc2</DestinationRef>
                          <DirectionRef>Retour</DirectionRef>
                        </Destination>
                      </Destinations>
                    </AnnotatedLineRef>
                  </LinesDelivery>
                </Siri>
              </soap:Body>
            </soap:Envelope>
        "#;

        let expected = SoapEnvelope {
            header: "".to_string(),
            body: SoapBody {
                siri: Siri {
                    lines_delivery: LinesDelivery {
                        response_timestamp: "2025-03-19T12:23:28.81575356Z".to_string(),
                        annotated_line_refs: vec![
                            AnnotatedLineRef {
                                line_ref: "101".to_string(),
                                line_name: "T1".to_string(),
                                monitored: true,
                                destinations: Destinations {
                                    destination: vec![
                                        Destination {
                                            destination_ref: "t_chal".to_string(),
                                            direction_ref: "Aller".to_string(),
                                        },
                                        Destination {
                                            destination_ref: "t_hdc2".to_string(),
                                            direction_ref: "Retour".to_string(),
                                        },
                                    ],
                                },
                            },
                        ],
                    },
                },
            },
        };

        let result: SoapEnvelope = from_str(xml).unwrap();
        assert_eq!(result, expected);
    }
}