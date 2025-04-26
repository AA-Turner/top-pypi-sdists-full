use tokio::sync::mpsc::UnboundedSender;

use crate::{siri_xml_requests::{estimated_table::EstimatedTableRequest, SoapRequestParams}, send_soap_request, Notification};


pub struct EstimatedTableListerner;


impl EstimatedTableListerner {
    /// Run the estimated timetable listener with the given URL, lines, interval, and sender.
    /// 
    /// 
    /// # Parameters
    /// 
    /// - `url` - The URL to send the request to.
    /// - `lines` - The lines to get the estimated timetable for.
    /// - `interval` - The interval to wait between requests.
    /// - `sender` - The sender to send the notifications to.
    /// 
    /// # Returns
    /// 
    /// The handle to the spawned task.
    /// 
    /// # Errors
    /// 
    /// If there is an error sending the request.
    pub fn run(url: String, lines: Vec<String>, interval: u64, sender: UnboundedSender<Notification>) -> tokio::task::JoinHandle<()> {
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(tokio::time::Duration::from_secs(interval));
            loop {
                interval.tick().await;
                let id = uuid::Uuid::new_v4();
                let date = chrono::Utc::now();
                let requestor_ref = "Hove";
                let message_id = format!("{}::Message::{}", requestor_ref, id.to_string());
                let soap_params = SoapRequestParams {
                    timestamp: date.to_rfc3339(),
                    requestor_ref: "HOVE".to_string(),
                    message_id,
                };

                let request = EstimatedTableRequest::new(soap_params);
                let result = request.create_estimated_table_request(lines.clone()).unwrap();

                let client = reqwest::Client::new();
                let response = send_soap_request(&client, &url, &result).await.expect("Failed to send request");
                let xml = response.text().await.expect("Failed to get response body");
                
                sender.send(Notification {
                    message: xml.replace("ns2:", ""), // Remove the ns2: prefix as it create issues with the XML parser
                    _type: "EstimatedTable".to_string(),
                }).expect("Failed to send notification");
            }
        })
    }
}