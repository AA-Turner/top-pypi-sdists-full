use std::{fs, path::Path};

pub struct TestCase {
    pub user_agent: String,
    pub expected_os_family: Option<String>,
    pub expected_browser_family: Option<String>,
}

pub fn load_test_cases_from_file(file_name: &str) -> Vec<TestCase> {
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join(file_name);
    let contents =
        fs::read_to_string(&path).unwrap_or_else(|err| panic!("{}: {err}", path.display()));
    contents.lines().skip(1).map(parse_test_case).collect()
}

fn parse_test_case(row: &str) -> TestCase {
    let columns: Vec<_> = row.split('|').collect();
    // Each family is followed by four version columns.
    let [agent, os, _, _, _, _, browser, _, _, _, _, ..] = columns.as_slice() else {
        panic!("incomplete user-agent fixture row: {row}");
    };
    let family = |name: &str| (name != "None").then(|| name.to_owned());
    TestCase {
        user_agent: (*agent).to_owned(),
        expected_os_family: family(os),
        expected_browser_family: family(browser),
    }
}
