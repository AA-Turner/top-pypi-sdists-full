use pyo3::prelude::*;
use pyo3::types::PyString;
use siri_question_response::listeners::estimated_time_table::EstimatedTableListerner;
use tokio::sync::mpsc::unbounded_channel;
use std::sync::Arc;
use tracing::{error, info};

#[pyclass]
#[derive(Debug, Clone)]
pub struct EstimatedTableConsumer {
    url: String,
}

#[pymethods]
impl EstimatedTableConsumer {
    #[new]
    pub fn new(url: String) -> Self {
        EstimatedTableConsumer { url }
    }

    fn listen_estimated_timetable(
        &self,
        interval: u64,
        callback: PyObject,
    ) -> PyResult<()> {
        info!("Starting listener for estimated timetable");
        let url = self.url.clone();
        let callback = Arc::new(callback);

        std::thread::spawn(move || {

            let rt = tokio::runtime::Runtime::new().expect("Failed to create Tokio runtime");
            rt.block_on(async move {
                let (tx, mut rx) = unbounded_channel();
                let line_discovery = siri_question_response::get_line_discovery(&url, "Hove").await;
                
                let lines_unfiltered = match line_discovery {
                    Ok(response) => match response.text().await {
                        Ok(body) => body,
                        Err(e) => {
                            error!("Failed to get response body: {:?}", e);
                            return;
                        }
                    },
                    Err(e) => {
                        error!("Failed to get line discovery: {:?}", e);
                        return;
                    }
                };
                
                let lines_deserialized = match siri_question_response::deserializers::line_discovery_ginko::deserialize_lines_delivery(&lines_unfiltered) {
                    Ok(deserialized) => deserialized,
                    Err(e) => {
                        error!("Failed to deserialize line discovery response: {:?}", e);
                        return;
                    }
                };
                
                let lines: Vec<String> = lines_deserialized
                    .body
                    .siri.lines_delivery.annotated_line_refs
                    .into_iter()
                    .map(|line| line.line_ref.clone())
                    .collect();
                
                if lines.is_empty() {
                    info!("No lines found in line discovery response");
                    return;
                }
                
                let listener_handle = EstimatedTableListerner::run(
                    url,
                    lines,
                    interval,
                    tx.clone(),
                );

                // Handle incoming notifications
                let receiver_handle = tokio::spawn(async move {
                    while let Some(notification) = rx.recv().await {                        
                        Python::with_gil(|py| {
                            let args = (
                                PyString::new(py, &notification.message).into_pyobject(py),
                                PyString::new(py, &notification._type).into_pyobject(py),
                                PyString::new(py, &uuid::Uuid::new_v4().to_string()).into_pyobject(py),
                            );
                            
                            let args = (args.0.unwrap(), args.1.unwrap(), args.2.unwrap());
                            std::thread::sleep(std::time::Duration::from_secs(1));
                            if let Err(e) = callback.call1(py, args) {
                                e.print_and_set_sys_last_vars(py);
                            }
                        });
                    }
                });
                
                let _ = tokio::join!(listener_handle, receiver_handle);
            });
        });

        Ok(())
    }
}

#[pymodule]
fn siri_question_answer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<EstimatedTableConsumer>()?;
    Ok(())
}