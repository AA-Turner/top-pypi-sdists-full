use super::*;

#[test]
fn startup_lists_match_their_id_types() {
    let allowlist =
        RemoteIdListAllowlist::from_json(r#"{"people":"userid","teams":"workspaceID"}"#).unwrap();
    assert!(allowlist.allows("people", "UserID"));
    assert!(allowlist.allows("teams", "workspaceID"));
    assert!(!allowlist.allows("teams", "workspaceid"));
    assert!(!allowlist.allows("other", "userID"));

    for invalid in [
        "{}",
        "invalid",
        r#"{"people":"userID","teams":""}"#,
        r#"{"teams":42}"#,
    ] {
        assert!(RemoteIdListAllowlist::from_json(invalid).is_none());
    }
}
