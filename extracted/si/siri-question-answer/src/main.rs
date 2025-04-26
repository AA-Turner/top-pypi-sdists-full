use siri_question_response::{listeners::estimated_time_table::EstimatedTableListerner, Notification};
use tokio::sync::mpsc::unbounded_channel;



#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let lines = vec!["7".to_string()];
    let (tx, _rx) = unbounded_channel::<Notification>();
    let handle = EstimatedTableListerner::run("".to_string(), lines, 60, tx.clone());
    handle.await?;
    Ok(())
}
