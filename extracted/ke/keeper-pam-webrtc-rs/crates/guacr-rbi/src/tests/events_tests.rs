use crate::events::{DisplayRect, InputEvent, UrlPattern};

#[test]
fn test_display_rect_intersects() {
    let rect1 = DisplayRect::new(10, 10, 20, 20);
    let rect2 = DisplayRect::new(20, 20, 20, 20);
    let rect3 = DisplayRect::new(50, 50, 10, 10);

    assert!(rect1.intersects(&rect2));
    assert!(!rect1.intersects(&rect3));
}

#[test]
fn test_display_rect_union() {
    let rect1 = DisplayRect::new(10, 10, 20, 20);
    let rect2 = DisplayRect::new(20, 20, 20, 20);

    let union = rect1.union(&rect2);
    assert_eq!(union.x, 10);
    assert_eq!(union.y, 10);
    assert_eq!(union.width, 30);
    assert_eq!(union.height, 30);
}

#[test]
fn test_url_pattern_parse() {
    let pattern = UrlPattern::parse("https://example.com:443/path").unwrap();
    assert_eq!(pattern.scheme, Some("https".to_string()));
    assert_eq!(pattern.host, "example.com");
    assert_eq!(pattern.port, Some(443));
    assert_eq!(pattern.path, Some("/path".to_string()));
}

#[test]
fn test_url_pattern_matches() {
    let pattern = UrlPattern::parse("*.google.com").unwrap();
    assert!(pattern.matches("https://www.google.com/search"));
    assert!(pattern.matches("http://mail.google.com"));
    assert!(!pattern.matches("https://example.com"));
}

#[test]
fn test_input_events() {
    let event = InputEvent::navigate_back();
    if let InputEvent::NavigateHistory(details) = event {
        assert_eq!(details.position, -1);
    } else {
        panic!("Expected NavigateHistory event");
    }
}
