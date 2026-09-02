use crate::error::HandlerError;
use crate::events::{EventCallback, HandlerEvent, InstructionSender};
use bytes::Bytes;
use std::sync::{Arc, Mutex};

struct TestCallback {
    events: Arc<Mutex<Vec<HandlerEvent>>>,
    instructions: Arc<Mutex<Vec<Bytes>>>,
}

#[async_trait::async_trait]
impl EventCallback for TestCallback {
    fn on_event(&self, event: HandlerEvent) {
        self.events.lock().unwrap().push(event);
    }

    async fn send_instruction(&self, instruction: Bytes) -> Result<(), HandlerError> {
        self.instructions.lock().unwrap().push(instruction);
        Ok(())
    }
}

#[tokio::test]
async fn test_event_callback() {
    let events = Arc::new(Mutex::new(Vec::new()));
    let instructions = Arc::new(Mutex::new(Vec::new()));

    let callback = Arc::new(TestCallback {
        events: events.clone(),
        instructions: instructions.clone(),
    });

    let sender = InstructionSender::new(callback.clone());

    // Send instruction
    sender.send(Bytes::from("test")).await.unwrap();
    assert_eq!(instructions.lock().unwrap().len(), 1);

    // Send error
    sender.send_error("test error".to_string(), Some(1));
    assert_eq!(events.lock().unwrap().len(), 1);

    // Send threat
    sender.send_threat("critical".to_string(), "threat detected".to_string());
    assert_eq!(events.lock().unwrap().len(), 2);
}
