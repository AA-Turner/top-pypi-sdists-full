use crate::tabs::{TabManager, MAX_TABS};

#[test]
fn test_create_tab() {
    let mut manager = TabManager::new();

    let id = manager.create_tab("https://example.com");
    assert_eq!(id, Some(0));
    assert_eq!(manager.count(), 1);

    let tab = manager.get_tab(0).unwrap();
    assert!(tab.is_active);
    assert_eq!(tab.url, "https://example.com");
}

#[test]
fn test_switch_tabs() {
    let mut manager = TabManager::new();

    manager.create_tab("https://tab1.com");
    manager.create_tab("https://tab2.com");

    assert!(manager.get_tab(0).unwrap().is_active);
    assert!(!manager.get_tab(1).unwrap().is_active);

    manager.switch_to_tab(1);
    assert!(!manager.get_tab(0).unwrap().is_active);
    assert!(manager.get_tab(1).unwrap().is_active);
}

#[test]
fn test_close_tab() {
    let mut manager = TabManager::new();

    manager.create_tab("https://tab1.com");
    manager.create_tab("https://tab2.com");
    manager.switch_to_tab(0);

    manager.close_tab(0);

    assert_eq!(manager.count(), 1);
    assert!(manager.get_tab(1).unwrap().is_active);
}

#[test]
fn test_max_tabs() {
    let mut manager = TabManager::new();

    for i in 0..MAX_TABS {
        assert!(manager
            .create_tab(&format!("https://tab{}.com", i))
            .is_some());
    }

    assert!(manager.create_tab("https://overflow.com").is_none());
}

#[test]
fn test_tabs_instruction() {
    let mut manager = TabManager::new();
    manager.create_tab("https://example.com");

    manager.update_tab_title(0, "Example");

    let instr = manager.format_tabs_instruction();
    assert!(instr.starts_with("4.tabs,"));
    assert!(instr.contains("Example"));
}
