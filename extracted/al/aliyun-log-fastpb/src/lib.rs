use pyo3::exceptions::{PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyList};

use quick_protobuf::{MessageWrite, Writer};
use std::borrow::Cow;

mod proto;
use proto::*;

// Trait for parsing content from Python dict
trait ParseContent<'a>: Sized {
    fn parse_from_dict(dict: &Bound<'_, PyDict>) -> PyResult<Self>;
}

// Trait for parsing log entries from Python dict
trait ParseLog<'a>: Sized {
    type Content: ParseContent<'a>;

    fn new(time: u32, contents: Vec<Self::Content>, time_ns: Option<u32>) -> Self;
}

// Trait for log groups
trait ParseLogGroup<'a>: Sized + MessageWrite {
    type LogType: ParseLog<'a>;

    fn new(
        logs: Vec<Self::LogType>,
        topic: Option<Cow<'a, str>>,
        source: Option<Cow<'a, str>>,
        log_tags: Vec<LogTag<'a>>,
    ) -> Self;
}

// Helper function to extract string from Python object
fn extract_string(obj: &Bound<'_, PyAny>, _field_name: &str) -> PyResult<String> {
    if obj.is_none() {
        return Ok(String::new());
    }

    obj.extract::<String>()
        .map_err(|_| PyTypeError::new_err("Value must be a string"))
}

// Helper function to extract optional string from Python object
fn extract_optional_string(obj: &Bound<'_, PyAny>, _field_name: &str) -> PyResult<Option<String>> {
    if obj.is_none() {
        return Ok(None);
    }

    obj.extract::<String>()
        .map(Some)
        .map_err(|_| PyTypeError::new_err("Value must be a string"))
}

// Helper function to extract bytes from Python object
fn extract_bytes(obj: &Bound<'_, PyAny>, _field_name: &str) -> PyResult<Vec<u8>> {
    if obj.is_none() {
        return Ok(Vec::new());
    }

    if let Ok(bytes) = obj.cast::<PyBytes>() {
        return Ok(bytes.as_bytes().to_vec());
    }

    if let Ok(s) = obj.extract::<String>() {
        return Ok(s.into_bytes());
    }

    Err(PyTypeError::new_err("Value must be bytes or string"))
}

// Helper function to extract u32 from Python object
fn extract_u32(obj: &Bound<'_, PyAny>, _field_name: &str) -> PyResult<u32> {
    if obj.is_none() {
        return Ok(0);
    }

    obj.extract::<u32>()
        .map_err(|_| PyTypeError::new_err("Value must be an unsigned integer"))
}

// Helper function to extract optional u32 from Python object
fn extract_optional_u32(obj: &Bound<'_, PyAny>, _field_name: &str) -> PyResult<Option<u32>> {
    if obj.is_none() {
        return Ok(None);
    }

    obj.extract::<u32>()
        .map(Some)
        .map_err(|_| PyTypeError::new_err("Value must be an unsigned integer"))
}

// Implement ParseContent for LogContent
impl<'a> ParseContent<'a> for LogContent<'a> {
    fn parse_from_dict(dict: &Bound<'_, PyDict>) -> PyResult<Self> {
        let key_obj = dict
            .get_item("Key")
            .map_err(|_| PyValueError::new_err("LogContent missing 'Key' field"))?
            .ok_or_else(|| PyValueError::new_err("LogContent missing 'Key' field"))?;

        let value_obj = dict
            .get_item("Value")
            .map_err(|_| PyValueError::new_err("LogContent missing 'Value' field"))?
            .ok_or_else(|| PyValueError::new_err("LogContent missing 'Value' field"))?;

        let key = extract_string(&key_obj, "Key")?;
        let value = extract_string(&value_obj, "Value")?;

        Ok(LogContent {
            key: Cow::Owned(key),
            value: Cow::Owned(value),
        })
    }
}

// Implement ParseContent for LogContentRaw
impl<'a> ParseContent<'a> for LogContentRaw<'a> {
    fn parse_from_dict(dict: &Bound<'_, PyDict>) -> PyResult<Self> {
        let key_obj = dict
            .get_item("Key")
            .map_err(|_| PyValueError::new_err("LogContentRaw missing 'Key' field"))?
            .ok_or_else(|| PyValueError::new_err("LogContentRaw missing 'Key' field"))?;

        let value_obj = dict
            .get_item("Value")
            .map_err(|_| PyValueError::new_err("LogContentRaw missing 'Value' field"))?
            .ok_or_else(|| PyValueError::new_err("LogContentRaw missing 'Value' field"))?;

        let key = extract_string(&key_obj, "Key")?;
        let value = extract_bytes(&value_obj, "Value")?;

        Ok(LogContentRaw {
            key: Cow::Owned(key),
            value: Cow::Owned(value),
        })
    }
}

// Implement ParseLog for Log
impl<'a> ParseLog<'a> for Log<'a> {
    type Content = LogContent<'a>;

    fn new(time: u32, contents: Vec<Self::Content>, time_ns: Option<u32>) -> Self {
        Log {
            time,
            contents,
            time_ns,
        }
    }
}

// Implement ParseLog for LogRaw
impl<'a> ParseLog<'a> for LogRaw<'a> {
    type Content = LogContentRaw<'a>;

    fn new(time: u32, contents: Vec<Self::Content>, time_ns: Option<u32>) -> Self {
        LogRaw {
            time,
            contents,
            time_ns,
        }
    }
}

// Implement ParseLogGroup for LogGroup
impl<'a> ParseLogGroup<'a> for LogGroup<'a> {
    type LogType = Log<'a>;

    fn new(
        logs: Vec<Self::LogType>,
        topic: Option<Cow<'a, str>>,
        source: Option<Cow<'a, str>>,
        log_tags: Vec<LogTag<'a>>,
    ) -> Self {
        LogGroup {
            logs,
            topic,
            source,
            log_tags,
        }
    }
}

// Implement ParseLogGroup for LogGroupRaw
impl<'a> ParseLogGroup<'a> for LogGroupRaw<'a> {
    type LogType = LogRaw<'a>;

    fn new(
        logs: Vec<Self::LogType>,
        topic: Option<Cow<'a, str>>,
        source: Option<Cow<'a, str>>,
        log_tags: Vec<LogTag<'a>>,
    ) -> Self {
        LogGroupRaw {
            logs,
            topic,
            source,
            log_tags,
        }
    }
}

// Generic function to parse LogTag from Python dict
fn parse_log_tag(item: &Bound<'_, PyAny>) -> PyResult<LogTag<'static>> {
    let dict = item
        .cast::<PyDict>()
        .map_err(|_| PyTypeError::new_err("LogTag must be a dict"))?;

    let key_obj = dict
        .get_item("Key")
        .map_err(|_| PyValueError::new_err("LogTag missing 'Key' field"))?
        .ok_or_else(|| PyValueError::new_err("LogTag missing 'Key' field"))?;

    let value_obj = dict
        .get_item("Value")
        .map_err(|_| PyValueError::new_err("LogTag missing 'Value' field"))?
        .ok_or_else(|| PyValueError::new_err("LogTag missing 'Value' field"))?;

    let key = extract_string(&key_obj, "Key")?;
    let value = extract_string(&value_obj, "Value")?;

    Ok(LogTag {
        key: Cow::Owned(key),
        value: Cow::Owned(value),
    })
}

// Generic function to parse Log/LogRaw from Python dict
fn parse_log_generic<L>(item: &Bound<'_, PyAny>) -> PyResult<L>
where
    L: ParseLog<'static>,
{
    let dict = item
        .cast::<PyDict>()
        .map_err(|_| PyTypeError::new_err("Log must be a dict"))?;

    let time_obj = dict
        .get_item("Time")
        .map_err(|_| PyValueError::new_err("Log missing 'Time' field"))?
        .ok_or_else(|| PyValueError::new_err("Log missing 'Time' field"))?;
    let time = extract_u32(&time_obj, "Time")?;

    let contents_obj = dict
        .get_item("Contents")
        .map_err(|_| PyValueError::new_err("Log missing 'Contents' field"))?
        .ok_or_else(|| PyValueError::new_err("Log missing 'Contents' field"))?;
    let contents_list = contents_obj
        .cast::<PyList>()
        .map_err(|_| PyTypeError::new_err("Contents must be a list"))?;

    let mut contents = Vec::new();
    for content_item in contents_list.iter() {
        let content_dict = content_item
            .cast::<PyDict>()
            .map_err(|_| PyTypeError::new_err("Content must be a dict"))?;
        contents.push(L::Content::parse_from_dict(content_dict)?);
    }

    let time_ns = if let Ok(Some(time_ns_obj)) = dict.get_item("TimeNs") {
        extract_optional_u32(&time_ns_obj, "TimeNs")?
    } else {
        None
    };

    Ok(L::new(time, contents, time_ns))
}

// Generic function to serialize LogGroup/LogGroupRaw
fn serialize_log_group_generic<G>(
    py: Python<'_>,
    log_group_dict: &Bound<'_, PyDict>,
) -> PyResult<Py<PyBytes>>
where
    G: ParseLogGroup<'static>,
{
    // Parse LogItems - if not present, default to empty list
    let logs = if let Ok(Some(log_items_obj)) = log_group_dict.get_item("LogItems") {
        let log_items_list = log_items_obj
            .cast::<PyList>()
            .map_err(|_| PyTypeError::new_err("LogItems must be a list"))?;

        let mut logs = Vec::with_capacity(log_items_list.len());
        for log_item in log_items_list.iter() {
            logs.push(parse_log_generic::<G::LogType>(&log_item)?);
        }
        logs
    } else {
        Vec::new()
    };

    // Parse LogTags - if not present, default to empty list
    let log_tags = if let Ok(Some(log_tags_obj)) = log_group_dict.get_item("LogTags") {
        let log_tags_list = log_tags_obj
            .cast::<PyList>()
            .map_err(|_| PyTypeError::new_err("LogTags must be a list"))?;

        let mut log_tags = Vec::with_capacity(log_tags_list.len());
        for tag_item in log_tags_list.iter() {
            log_tags.push(parse_log_tag(&tag_item)?);
        }
        log_tags
    } else {
        Vec::new()
    };

    let topic = if let Ok(Some(topic_obj)) = log_group_dict.get_item("Topic") {
        extract_optional_string(&topic_obj, "Topic")?.map(Cow::Owned)
    } else {
        None
    };

    let source = if let Ok(Some(source_obj)) = log_group_dict.get_item("Source") {
        extract_optional_string(&source_obj, "Source")?.map(Cow::Owned)
    } else {
        None
    };

    let log_group = G::new(logs, topic, source, log_tags);

    let mut buf = Vec::new();
    let mut writer = Writer::new(&mut buf);
    log_group
        .write_message(&mut writer)
        .map_err(|e| PyValueError::new_err(format!("Serialization failed: {e}")))?;

    Ok(PyBytes::new(py, &buf).into())
}

/// Serialize a LogGroup Python dict to protobuf bytes.
///
/// Args:
///     log_group_dict: A dict that may contain LogItems, LogTags, Topic, and Source.
///
/// Returns:
///     bytes: The serialized protobuf data.
///
/// Raises:
///     TypeError: If the input types are incorrect.
///     ValueError: If required fields within Log entries are missing.
#[pyfunction]
fn serialize_log_group(
    py: Python<'_>,
    log_group_dict: &Bound<'_, PyDict>,
) -> PyResult<Py<PyBytes>> {
    serialize_log_group_generic::<LogGroup>(py, log_group_dict)
}

/// Serialize a LogGroupRaw Python dict to protobuf bytes.
///
/// Args:
///     log_group_dict: A dict that may contain LogItems, LogTags, Topic, and Source.
///
/// Returns:
///     bytes: The serialized protobuf data.
///
/// Raises:
///     TypeError: If the input types are incorrect.
///     ValueError: If required fields within Log entries are missing.
#[pyfunction]
fn serialize_log_group_raw(
    py: Python<'_>,
    log_group_dict: &Bound<'_, PyDict>,
) -> PyResult<Py<PyBytes>> {
    serialize_log_group_generic::<LogGroupRaw>(py, log_group_dict)
}

/// A Python module implemented in Rust for fast protobuf serialization of Aliyun Log.
#[pymodule]
fn aliyun_log_fastpb(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(serialize_log_group, m)?)?;
    m.add_function(wrap_pyfunction!(serialize_log_group_raw, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_log_content_cow_owned() {
        // Test that LogContent uses Cow::Owned correctly
        let content = LogContent {
            key: Cow::Owned("test_key".to_string()),
            value: Cow::Owned("test_value".to_string()),
        };

        assert_eq!(content.key, "test_key");
        assert_eq!(content.value, "test_value");
    }

    #[test]
    fn test_log_structure() {
        // Test that Log structure can be created
        let log = Log {
            time: 1234567890,
            contents: vec![LogContent {
                key: Cow::Owned("k1".to_string()),
                value: Cow::Owned("v1".to_string()),
            }],
            time_ns: Some(123456789),
        };

        assert_eq!(log.time, 1234567890);
        assert_eq!(log.contents.len(), 1);
        assert_eq!(log.time_ns, Some(123456789));
    }

    #[test]
    fn test_log_group_serialization() {
        // Test that LogGroup can be serialized
        let log_group = LogGroup {
            logs: vec![Log {
                time: 1000,
                contents: vec![LogContent {
                    key: Cow::Owned("key".to_string()),
                    value: Cow::Owned("value".to_string()),
                }],
                time_ns: None,
            }],
            topic: Some(Cow::Owned("test-topic".to_string())),
            source: Some(Cow::Owned("test-source".to_string())),
            log_tags: vec![LogTag {
                key: Cow::Owned("tag_key".to_string()),
                value: Cow::Owned("tag_value".to_string()),
            }],
        };

        let mut buf = Vec::new();
        let mut writer = Writer::new(&mut buf);
        let result = log_group.write_message(&mut writer);

        assert!(result.is_ok());
        assert!(!buf.is_empty());
    }

    #[test]
    fn test_log_group_raw_with_binary() {
        // Test LogGroupRaw with binary data
        let log_group_raw = LogGroupRaw {
            logs: vec![LogRaw {
                time: 2000,
                contents: vec![LogContentRaw {
                    key: Cow::Owned("binary_key".to_string()),
                    value: Cow::Owned(vec![0x00, 0x01, 0x02, 0xFF]),
                }],
                time_ns: None,
            }],
            topic: None,
            source: None,
            log_tags: vec![],
        };

        let mut buf = Vec::new();
        let mut writer = Writer::new(&mut buf);
        let result = log_group_raw.write_message(&mut writer);

        assert!(result.is_ok());
        assert!(!buf.is_empty());
    }

    #[test]
    fn test_empty_log_group() {
        // Test that empty LogGroup can be serialized (may be 0 bytes)
        let log_group = LogGroup {
            logs: vec![],
            topic: None,
            source: None,
            log_tags: vec![],
        };

        let mut buf = Vec::new();
        let mut writer = Writer::new(&mut buf);
        let result = log_group.write_message(&mut writer);

        assert!(result.is_ok());
        // Empty protobuf message is valid and may be 0 bytes
    }

    #[test]
    fn test_unicode_in_log_content() {
        // Test Unicode handling
        let content = LogContent {
            key: Cow::Owned("中文键".to_string()),
            value: Cow::Owned("中文值 🚀".to_string()),
        };

        assert!(content.key.contains("中文"));
        assert!(content.value.contains("🚀"));
    }

    #[test]
    fn test_large_log_group() {
        // Test with many log entries
        let mut logs = Vec::with_capacity(100);
        for i in 0..100 {
            logs.push(Log {
                time: 1000 + i,
                contents: vec![LogContent {
                    key: Cow::Owned(format!("key_{}", i)),
                    value: Cow::Owned(format!("value_{}", i)),
                }],
                time_ns: None,
            });
        }

        let log_group = LogGroup {
            logs,
            topic: Some(Cow::Owned("large-test".to_string())),
            source: None,
            log_tags: vec![],
        };

        let mut buf = Vec::new();
        let mut writer = Writer::new(&mut buf);
        let result = log_group.write_message(&mut writer);

        assert!(result.is_ok());
        assert!(buf.len() > 1000); // Should be a decent size
    }
}
