use super::*;

#[test]
fn startup_lists_match_their_id_types() {
    let allowlist = RemoteIdListAllowlist::from_lists(HashMap::from([
        ("people".to_owned(), "userid".to_owned()),
        ("teams".to_owned(), "workspaceID".to_owned()),
    ]));
    assert!(allowlist.allows("people", "UserID"));
    assert!(allowlist.allows("teams", "workspaceID"));
    assert!(!allowlist.allows("teams", "workspaceid"));
    assert!(!allowlist.allows("other", "userID"));

    let invalid = RemoteIdListAllowlist::from_lists(HashMap::from([
        ("people".to_owned(), "userID".to_owned()),
        ("teams".to_owned(), String::new()),
    ]));
    assert!(invalid.is_empty());
}
