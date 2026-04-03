use crate::channel_handler::RdpChannelHandler;

#[test]
fn test_channel_handler_new() {
    let handler = RdpChannelHandler::new(1024 * 1024, false, false);
    assert!(!handler.disable_copy);
    assert!(!handler.disable_paste);
}

#[test]
fn test_disp_resize() {
    let handler = RdpChannelHandler::new(1024 * 1024, false, false);
    let msg = handler.prepare_disp_resize(1920, 1080);
    assert_eq!(msg.width, 1920);
    assert_eq!(msg.height, 1080);
}
