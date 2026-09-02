#![cfg(feature = "onnx-classifier")]
use crate::classifier::{argmax, softmax, ActionEffectClassifier, LABELS};

#[test]
fn test_softmax_basic() {
    let logits = vec![2.0, 1.0, 0.1];
    let probs = softmax(&logits);
    assert!(probs.iter().all(|&p| p > 0.0));
    let sum: f32 = probs.iter().sum();
    assert!((sum - 1.0).abs() < 1e-6);
    assert!(probs[0] > probs[1]);
    assert!(probs[1] > probs[2]);
}

#[test]
fn test_softmax_numerical_stability() {
    // Large logits that would overflow without max subtraction.
    let logits = vec![1000.0, 1000.0, 1000.0];
    let probs = softmax(&logits);
    for &p in &probs {
        assert!(
            (p - 1.0_f32 / 3.0_f32).abs() < 1e-5_f32,
            "got {} expected ~0.333",
            p
        );
    }
}

#[test]
fn test_softmax_single_element() {
    let probs = softmax(&[5.0]);
    assert!((probs[0] - 1.0).abs() < 1e-6);
}

#[test]
fn test_argmax() {
    assert_eq!(argmax(&[0.1, 0.7, 0.15, 0.05]), 1);
    assert_eq!(argmax(&[0.9, 0.05, 0.03, 0.02]), 0);
    assert_eq!(argmax(&[0.1, 0.2, 0.3, 0.4]), 3);
}

#[test]
fn test_argmax_equal() {
    // When values are equal, returns the first occurrence
    let idx = argmax(&[0.5, 0.5]);
    assert!(idx == 0 || idx == 1);
}

#[test]
fn test_is_enabled_for_protocol() {
    assert!(ActionEffectClassifier::is_enabled_for_protocol("ssh"));
    assert!(!ActionEffectClassifier::is_enabled_for_protocol("rdp"));
    assert!(!ActionEffectClassifier::is_enabled_for_protocol("vnc"));
    assert!(!ActionEffectClassifier::is_enabled_for_protocol("telnet"));
}

#[test]
fn test_labels_order() {
    assert_eq!(LABELS.len(), 4);
    assert_eq!(LABELS[0], "Critical");
    assert_eq!(LABELS[1], "High");
    assert_eq!(LABELS[2], "Medium");
    assert_eq!(LABELS[3], "Low");
}

#[test]
fn test_new_missing_dir() {
    let classifier = ActionEffectClassifier::new("/nonexistent/path/to/model");
    assert!(classifier.is_none());
}
