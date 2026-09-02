use crate::file_browser::{format_size, FileBrowser, FileEntry, CHAR_HEIGHT, DATA_ROW_PIXEL_START};

fn make_entry(name: &str, size: u64, is_dir: bool) -> FileEntry {
    FileEntry {
        name: name.to_string(),
        size,
        is_directory: is_dir,
        permissions: if is_dir { "drwxr-xr-x" } else { "rw-r--r--" }.to_string(),
        modified: "2024-01-01".to_string(),
    }
}

#[test]
fn test_file_browser_new() {
    let entries = vec![make_entry("file1.txt", 1024, false)];
    let browser = FileBrowser::new("/home/user".to_string(), entries);
    assert_eq!(browser.current_path, "/home/user");
    assert_eq!(browser.entries.len(), 1);
}

#[test]
fn test_file_browser_render() {
    let browser = FileBrowser::new("/".to_string(), vec![]);
    let jpeg = browser.render_to_jpeg(800, 600);
    assert!(jpeg.is_ok());
    assert!(!jpeg.unwrap().is_empty());
}

#[test]
fn test_file_browser_selection() {
    let entries = vec![make_entry("file1.txt", 1024, false)];
    let mut browser = FileBrowser::new("/".to_string(), entries);
    // First data row starts at DATA_ROW_PIXEL_START (90px)
    browser.handle_click(DATA_ROW_PIXEL_START);
    assert_eq!(browser.selected_index, Some(0));
    assert!(browser.get_selected().is_some());
}

#[test]
fn test_file_browser_multiple_entries() {
    let entries = vec![
        make_entry("file1.txt", 1024, false),
        make_entry("dir1", 0, true),
        make_entry("file2.txt", 2048, false),
    ];
    let mut browser = FileBrowser::new("/".to_string(), entries);

    // Second data row: DATA_ROW_PIXEL_START + CHAR_HEIGHT
    browser.handle_click(DATA_ROW_PIXEL_START + CHAR_HEIGHT);
    assert_eq!(browser.selected_index, Some(1));
    assert_eq!(browser.get_selected().unwrap().name, "dir1");
    assert!(browser.get_selected().unwrap().is_directory);

    // Third data row: DATA_ROW_PIXEL_START + 2 * CHAR_HEIGHT
    browser.handle_click(DATA_ROW_PIXEL_START + 2 * CHAR_HEIGHT);
    assert_eq!(browser.selected_index, Some(2));
    assert_eq!(browser.get_selected().unwrap().name, "file2.txt");
}

#[test]
fn test_file_browser_click_path_bar() {
    let entries = vec![make_entry("file1.txt", 1024, false)];
    let mut browser = FileBrowser::new("/".to_string(), entries);
    browser.handle_click(DATA_ROW_PIXEL_START); // Select first file
    assert_eq!(browser.selected_index, Some(0));
    // Click anywhere above DATA_ROW_PIXEL_START should not change selection
    browser.handle_click(20);
    assert_eq!(browser.selected_index, Some(0)); // Unchanged
}

#[test]
fn test_file_browser_click_out_of_bounds() {
    let entries = vec![make_entry("file1.txt", 1024, false)];
    let mut browser = FileBrowser::new("/".to_string(), entries);
    browser.handle_click(10000); // Way beyond any entries
    assert_eq!(browser.selected_index, None);
}

#[test]
fn test_file_entry_structure() {
    let entry = FileEntry {
        name: "test.txt".to_string(),
        size: 12345,
        is_directory: false,
        permissions: "rw-r--r--".to_string(),
        modified: "2024-01-01 12:00".to_string(),
    };
    assert_eq!(entry.name, "test.txt");
    assert_eq!(entry.size, 12345);
    assert!(!entry.is_directory);
    assert_eq!(entry.permissions, "rw-r--r--");
}

#[test]
fn test_file_entry_directory() {
    let entry = FileEntry {
        name: "mydir".to_string(),
        size: 0,
        is_directory: true,
        permissions: "drwxr-xr-x".to_string(),
        modified: "2024-01-01".to_string(),
    };
    assert!(entry.is_directory);
    assert_eq!(entry.size, 0);
    assert!(entry.permissions.starts_with('d'));
}

#[test]
fn test_format_size() {
    assert_eq!(format_size(0), "0 B");
    assert_eq!(format_size(512), "512 B");
    assert_eq!(format_size(1024), "1.0 KB");
    assert_eq!(format_size(1536), "1.5 KB");
    assert_eq!(format_size(1024 * 1024), "1.0 MB");
    assert_eq!(format_size(1024 * 1024 * 1024), "1.0 GB");
}

#[test]
fn test_render_with_entries() {
    let entries = vec![
        make_entry("Documents", 0, true),
        make_entry("notes.txt", 1234, false),
        make_entry("photo.jpg", 2_500_000, false),
    ];
    let browser = FileBrowser::new("/home/user".to_string(), entries);
    let jpeg = browser.render_to_jpeg(1024, 768);
    assert!(jpeg.is_ok());
    assert!(jpeg.unwrap().len() > 1000);
}
