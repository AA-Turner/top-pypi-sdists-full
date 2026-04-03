use crate::chrome_session::ChromeSession;

#[test]
fn test_chrome_session_new() {
    let session = ChromeSession::new(1920, 1080, 30, "/usr/bin/chromium");
    assert_eq!(session.width, 1920);
    assert_eq!(session.height, 1080);
}
