use quick_xml::events::{Event, BytesEnd};
use quick_xml::reader::Reader;
use quick_xml::writer::Writer;
use std::io::Cursor;

#[derive(Debug, PartialEq)]
enum State {
    Initial,            // Before entering the frame
    InFrame,            // Inside EstimatedJourneyVersionFrame
    InRecordedAtTime,   // Inside RecordedAtTime
    InJourney,          // Inside EstimatedVehicleJourney
}

pub fn split_soap_envelopes(xml: &str) -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let mut reader = Reader::from_str(xml);
    let mut envelopes = Vec::new();
    let mut prefix = Vec::new();
    let mut recorded_at_time = Vec::new();
    let mut journeys = Vec::new();
    let mut suffix = Vec::new();

    let mut state = State::Initial;
    let mut depth = 0;
    let mut current_journey: Option<Vec<Event>> = None;

    // Parse the XML structure
    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => {
                match state {
                    State::Initial => {
                        if e.name().as_ref() == b"ns2:EstimatedJourneyVersionFrame" {
                            state = State::InFrame;
                            depth = 1;
                            // Capture frame start
                            prefix.push(Event::Start(e.clone()));
                        } else {
                            prefix.push(Event::Start(e.clone()));
                        }
                    }
                    State::InFrame => {
                        depth += 1;
                        if e.name().as_ref() == b"ns2:RecordedAtTime" {
                            state = State::InRecordedAtTime;
                            recorded_at_time.push(Event::Start(e.clone()));
                        } else if e.name().as_ref() == b"ns2:EstimatedVehicleJourney" {
                            state = State::InJourney;
                            current_journey = Some(vec![Event::Start(e.clone())]);
                        }
                    }
                    State::InRecordedAtTime => {
                        recorded_at_time.push(Event::Start(e.clone()));
                    }
                    State::InJourney => {
                        if let Some(ref mut journey) = current_journey {
                            journey.push(Event::Start(e.clone()));
                        }
                    }
                }
            }
            Ok(Event::End(e)) => {
                match state {
                    State::Initial => {
                        prefix.push(Event::End(e.clone()));
                    }
                    State::InFrame => {
                        depth -= 1;
                        if depth == 0 {
                            loop {
                                match reader.read_event() {
                                    Ok(Event::Eof) => break,
                                    Ok(ev) => suffix.push(ev),
                                    Err(e) => return Err(e.into()),
                                }
                            }
                            break;
                        }
                    }
                    State::InRecordedAtTime => {
                        recorded_at_time.push(Event::End(e.clone()));
                        state = State::InFrame;
                    }
                    State::InJourney => {
                        if let Some(ref mut journey) = current_journey {
                            journey.push(Event::End(e.clone()));
                        }
                        if e.name().as_ref() == b"ns2:EstimatedVehicleJourney" {
                            state = State::InFrame;
                            if let Some(journey) = current_journey.take() {
                                journeys.push(journey);
                            }
                        }
                    }
                }
            }
            Ok(Event::Text(e)) => {
                match state {
                    State::InRecordedAtTime => {
                        recorded_at_time.push(Event::Text(e.clone()));
                    }
                    State::InJourney => {
                        if let Some(ref mut journey) = current_journey {
                            journey.push(Event::Text(e.clone()));
                        }
                    }
                    State::Initial => prefix.push(Event::Text(e.clone())),
                    State::InFrame => {},
                }
            }
            Ok(Event::Eof) => break,
            Ok(e) => {
                match state {
                    State::InRecordedAtTime => recorded_at_time.push(e.clone()),
                    State::InJourney => {
                        if let Some(ref mut journey) = current_journey {
                            journey.push(e.clone());
                        }
                    }
                    State::Initial => {},
                    State::InFrame => {},
                }
            }
            Err(e) => return Err(e.into()),
        }
    }

    // Generate output files
    for (_i, journey) in journeys.iter().enumerate() {
        let mut writer = Writer::new(Cursor::new(Vec::new()));
        
        // Write prefix (includes envelope and frame start)
        for event in &prefix {
            writer.write_event(event.clone())?;
        }
        
        // Write RecordedAtTime section
        for event in &recorded_at_time {
            writer.write_event(event.clone())?;
        }
        
        // Write the journey
        for event in journey {
            writer.write_event(event.clone())?;
        }
        
        // Close the EstimatedJourneyVersionFrame
        writer.write_event(Event::End(BytesEnd::new("ns2:EstimatedJourneyVersionFrame")))?;

        // close Anwser element
        writer.write_event(Event::End(BytesEnd::new("Answer")))?;

        // close GetEstimatedTimetableResponse element
        writer.write_event(Event::End(BytesEnd::new("GetEstimatedTimetableResponse")))?;

        // close Body element
        writer.write_event(Event::End(BytesEnd::new("soap:Body")))?;

        // close Envelope element
        writer.write_event(Event::End(BytesEnd::new("soap:Envelope")))?;
    
        // Write suffix (rest of the document)
        for event in suffix.iter().cloned() {
            writer.write_event(event.clone())?;
        }
        
        let result = writer.into_inner().into_inner();
        let raw: String = String::from_utf8(result)?;
        // First replace \n with actual newlines, then remove escaped quotes.
        let intermediate = raw
            .replace("\\n", "\n")
            .replace("\\\"", "\"");

        // Finally, trim each line and re-join with newlines.
        let cleaned = intermediate
            .lines()
            .map(|line| line.trim())
            .collect::<Vec<_>>()
            .join("\n");
        envelopes.push(cleaned);
    }
    Ok(envelopes)
}


#[cfg(test)]
mod tests {
    use super::*;
    use quick_xml::Reader;
    use quick_xml::events::Event;

    #[test]
    fn test_split_soap_envelopes() {
        let file_path = "textfile.txt";
        let xml = std::fs::read_to_string(file_path).unwrap();
        let envelopes = split_soap_envelopes(&xml).unwrap();
        assert_eq!(envelopes.len(), 44);
    }

    
    #[test]
    fn test_if_tags_all_have_close_tag() {
        let file_path = "textfile.txt";
        let xml = std::fs::read_to_string(file_path).expect("Failed to read file");
        let envelopes = split_soap_envelopes(&xml).expect("Failed to split SOAP envelopes");
    
        for envelope in envelopes {
            let mut reader = Reader::from_str(&envelope);
            let mut stack: Vec<Vec<u8>> = Vec::new();
            loop {
                match reader.read_event() {
                    Ok(Event::Start(e)) => {
                        // Push the tag name onto the stack
                        stack.push(e.name().as_ref().to_vec());
                    }
                    Ok(Event::Empty(_e)) => {
                    }
                    Ok(Event::End(e)) => {
                        if let Some(start) = stack.pop() {
                            assert_eq!(start.as_ref() as &[u8], e.name().as_ref(), "Mismatched tag found");
                        } else {
                            panic!("Encountered an end tag {:?} with no corresponding start tag", e.name());
                        }
                    }
                    Ok(Event::Eof) => break,
                    Err(e) => panic!("Error at position {}: {:?}", reader.buffer_position(), e),
                    _ => {}
                }
            }
            assert!(stack.is_empty(), "Not all tags were closed in the envelope.");
        }
    }
    
}