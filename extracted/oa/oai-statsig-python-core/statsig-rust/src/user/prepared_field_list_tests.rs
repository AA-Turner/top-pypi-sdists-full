use crate::{
    PreparedUserBase, StatsigUserValue,
    user::{StatsigUserInternal, fast_statsig_user::FastUserData},
};
use serde_json::json;
use std::sync::Arc;

#[test]
fn prepared_fields_preserve_custom_ids_and_typed_values() {
    let base = PreparedUserBase::from(Arc::new(FastUserData {
        user_id: Some("base-only-id".into()),
        custom_ids: Some([("podID".into(), "pod-42".into())].into_iter().collect()),
        custom: Some([("region".into(), "west".into())].into_iter().collect()),
        ..Default::default()
    }));
    let values: [(&str, StatsigUserValue); 5] = [
        ("attempt", 1.into()),
        ("region", "east".into()),
        ("Region", true.into()),
        ("attempt", 3.into()),
        ("labels", json!(["a", "b"]).into()),
    ];
    let user = base.prepare_with_fields(None, values);
    let public = user.to_public_user();
    let copy = user.clone();
    let empty = base.prepare_with_fields(None, []);
    let loggable = StatsigUserInternal::from_prepared_user(&copy, None).to_loggable();
    drop((copy, user, base));
    let encoded = serde_json::to_string(&loggable).unwrap();
    assert_eq!(encoded.matches("\"attempt\"").count(), 1);
    let output: serde_json::Value = serde_json::from_str(&encoded).unwrap();
    let expected = json!({
        "customIDs": {"podID": "pod-42"},
        "custom": {"attempt": 3, "region": "east", "Region": true, "labels": ["a", "b"]}
    });
    assert_eq!(output, expected);
    assert_eq!(json!(&*public.data), expected);
    assert_eq!(
        json!(StatsigUserInternal::from_prepared_user(&empty, None).to_loggable())["custom"],
        json!({"region":"west"})
    );
}

#[test]
fn empty_field_list_preserves_an_explicit_empty_overlay() {
    let base = PreparedUserBase::from(Arc::new(FastUserData::default()));
    let user = base.prepare_with_fields(None, []);
    assert!(user.to_public_user().get_custom().unwrap().is_empty());
    assert_eq!(
        json!(StatsigUserInternal::from_prepared_user(&user, None).to_loggable()),
        json!({"custom": {}})
    );
}
