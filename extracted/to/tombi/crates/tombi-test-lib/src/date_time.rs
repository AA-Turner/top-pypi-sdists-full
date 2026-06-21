pub fn today_offset_date_time() -> String {
    let mut today = chrono::Local::now();
    if let Some(time) = chrono::NaiveTime::from_hms_opt(0, 0, 0) {
        today = match today.with_time(time) {
            chrono::LocalResult::Single(today) => today,
            _ => today,
        };
    };
    today.format("%Y-%m-%dT%H:%M:%S%.3f%:z").to_string()
}

pub fn today_local_date_time() -> String {
    let mut today = chrono::Local::now();
    if let Some(time) = chrono::NaiveTime::from_hms_opt(0, 0, 0) {
        today = match today.with_time(time) {
            chrono::LocalResult::Single(today) => today,
            _ => today,
        };
    };
    today.format("%Y-%m-%dT%H:%M:%S%.3f").to_string()
}

pub fn today_local_date() -> String {
    chrono::Local::now().format("%Y-%m-%d").to_string()
}

pub fn today_local_time() -> String {
    let mut today = chrono::Local::now();
    if let Some(time) = chrono::NaiveTime::from_hms_opt(0, 0, 0) {
        today = match today.with_time(time) {
            chrono::LocalResult::Single(today) => today,
            _ => today,
        };
    };
    today.format("%H:%M:%S%.3f").to_string()
}
