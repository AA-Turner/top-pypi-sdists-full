/// Macro to create JSON values in a convenient way.
///
/// # Examples
///
/// ```
/// use tombi_json_value::{json, Value};
///
/// // Create a simple JSON object
/// let obj = json!({
///     "name": "John",
///     "age": 30,
///     "is_active": true,
///     "hobbies": ["Reading", "Running"]
/// });
///
/// // Variable interpolation
/// let name = "Jane";
/// let age = 25;
/// let user = json!({
///     "name": name,
///     "age": age
/// });
/// ```
#[macro_export]
macro_rules! json {
    // null
    (null) => {
        $crate::Value::Null
    };

    // Boolean
    (true) => {
        $crate::Value::Bool(true)
    };
    (false) => {
        $crate::Value::Bool(false)
    };

    // Array
    ([$($value:tt),* $(,)?]) => {
        $crate::Value::Array(vec![$($crate::json!($value)),*])
    };

    // Object
    ({$($key:tt : $value:tt),* $(,)?}) => {
        {
            let mut object = $crate::Object::new();
            $(
                object.insert($crate::json_key!($key), $crate::json!($value));
            )*
            $crate::Value::Object(object)
        }
    };

    // String literals
    ($value:literal) => {
        $crate::Value::from($value)
    };

    // Variables
    ($value:expr) => {
        $crate::Value::from($value)
    };
}

#[macro_export]
macro_rules! json_key {
    ($key:literal) => {
        $key.to_string()
    };
    ($key:expr) => {
        $key.to_string()
    };
}

#[cfg(test)]
mod tests {
    use crate::{Number, Value};

    #[test]
    fn test_json_macro() {
        // Test null
        let null_value = json!(null);
        assert!(null_value.is_null());

        // Test boolean
        let bool_value = json!(true);
        pretty_assertions::assert_eq!(bool_value, Value::Bool(true));

        // Test number
        let num_value = json!(42);
        pretty_assertions::assert_eq!(num_value, Value::Number(Number::from(42)));

        // Test float
        let float_value = json!(42.5);
        pretty_assertions::assert_eq!(float_value, Value::Number(Number::from(42.5)));

        // Test string
        let str_value = json!("hello");
        pretty_assertions::assert_eq!(str_value, Value::String("hello".to_string()));

        // Test array
        let array_value = json!([1, 2, "three", false]);
        if let Value::Array(arr) = array_value {
            pretty_assertions::assert_eq!(arr.len(), 4);
            pretty_assertions::assert_eq!(arr[0], Value::Number(Number::from(1)));
            pretty_assertions::assert_eq!(arr[1], Value::Number(Number::from(2)));
            pretty_assertions::assert_eq!(arr[2], Value::String("three".to_string()));
            pretty_assertions::assert_eq!(arr[3], Value::Bool(false));
        } else {
            panic!("Expected array");
        }

        // Test object
        let obj_value = json!({
            "name": "John",
            "age": 30,
            "is_active": true
        });
        if let Value::Object(obj) = obj_value {
            pretty_assertions::assert_eq!(obj.len(), 3);
            pretty_assertions::assert_eq!(
                obj.get_str("name"),
                Some(&Value::String("John".to_string()))
            );
            pretty_assertions::assert_eq!(
                obj.get_str("age"),
                Some(&Value::Number(Number::from(30)))
            );
            pretty_assertions::assert_eq!(obj.get_str("is_active"), Some(&Value::Bool(true)));
        } else {
            panic!("Expected object");
        }

        // Test variable interpolation
        let name = "Jane";
        let age = 25;
        let user = json!({
            "name": name,
            "age": age
        });
        if let Value::Object(obj) = user {
            pretty_assertions::assert_eq!(
                obj.get_str("name"),
                Some(&Value::String("Jane".to_string()))
            );
            pretty_assertions::assert_eq!(
                obj.get_str("age"),
                Some(&Value::Number(Number::from(25)))
            );
        } else {
            panic!("Expected object");
        }

        // Test nested structure
        let nested = json!({
            "user": {
                "name": "Bob",
                "hobbies": ["Reading", "Running"]
            }
        });
        if let Value::Object(obj) = nested {
            if let Some(Value::Object(user)) = obj.get_str("user") {
                pretty_assertions::assert_eq!(
                    user.get_str("name"),
                    Some(&Value::String("Bob".to_string()))
                );
                if let Some(Value::Array(hobbies)) = user.get_str("hobbies") {
                    pretty_assertions::assert_eq!(hobbies.len(), 2);
                    pretty_assertions::assert_eq!(hobbies[0], Value::String("Reading".to_string()));
                    pretty_assertions::assert_eq!(hobbies[1], Value::String("Running".to_string()));
                } else {
                    panic!("Expected hobbies array");
                }
            } else {
                panic!("Expected user object");
            }
        } else {
            panic!("Expected object");
        }

        // Test integer vs float distinction
        let int_value = json!(42);
        let float_value = json!(42.0);

        assert!(int_value.is_i64());
        assert!(!int_value.is_f64());
        pretty_assertions::assert_eq!(int_value.as_i64(), Some(42));

        // Default behavior is to convert whole number floats to integers
        assert!(float_value.is_i64());
        assert!(!float_value.is_f64());
        pretty_assertions::assert_eq!(float_value.as_i64(), Some(42));
        pretty_assertions::assert_eq!(float_value.as_f64(), Some(42.0));

        // Explicit float
        let explicit_float = json!(42.5);
        assert!(!explicit_float.is_i64());
        assert!(explicit_float.is_f64());
        pretty_assertions::assert_eq!(explicit_float.as_i64(), None);
        pretty_assertions::assert_eq!(explicit_float.as_f64(), Some(42.5));
    }
}
