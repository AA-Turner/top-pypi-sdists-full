//! A connect parameter guacd never asked for is discarded by the positional `connect`
//! instruction. It must be reported, not swallowed: a parameter that looks configured
//! but has no effect is indistinguishable from a working one.

use crate::client::dropped_connect_params;
use crate::server::excess_connect_values;
use std::collections::HashMap;

fn supplied(pairs: &[(&str, &str)]) -> HashMap<String, String> {
    pairs
        .iter()
        .map(|(k, v)| {
            (
                k.replace(['-', '_'], "").to_ascii_lowercase(),
                (*v).to_string(),
            )
        })
        .collect()
}

fn guacd_args(names: &[&str]) -> Vec<String> {
    let mut v = vec!["VERSION_1_5_0".to_string()];
    v.extend(names.iter().map(|n| n.to_string()));
    v
}

#[test]
fn reports_a_parameter_guacd_did_not_request() {
    let params = supplied(&[
        ("hostname", "host.example"),
        ("username", "svc"),
        ("server-alive-interval", "30"),
    ]);
    let args = guacd_args(&["hostname", "username", "password"]);

    assert_eq!(
        vec!["serveraliveinterval"],
        dropped_connect_params(&params, &args)
    );
}

#[test]
fn requested_parameters_are_not_reported() {
    let params = supplied(&[("hostname", "host.example"), ("domain", "ad.example.com")]);
    let args = guacd_args(&["hostname", "domain", "username"]);

    assert!(dropped_connect_params(&params, &args).is_empty());
}

#[test]
fn hyphen_and_underscore_spellings_both_match() {
    // guacd advertises "server-alive-interval"; a caller may send "server_alive_interval".
    let params = supplied(&[("server_alive_interval", "30")]);
    let args = guacd_args(&["server-alive-interval"]);

    assert!(dropped_connect_params(&params, &args).is_empty());
}

#[test]
fn out_of_band_parameters_are_not_reported_as_dropped() {
    // These are sent via their own handshake instructions (size/audio/video/image) or
    // consumed by us, so guacd never lists them in `args`.
    let params = supplied(&[
        ("protocol", "rdp"),
        ("connectionid", "abc"),
        ("readonly", "false"),
        ("size", "1024,768,96"),
        ("width", "1024"),
        ("height", "768"),
        ("dpi", "96"),
        ("audio", "audio/L16"),
        ("video", ""),
        ("image", "image/jpeg"),
    ]);
    let args = guacd_args(&["hostname"]);

    assert!(dropped_connect_params(&params, &args).is_empty());
}

#[test]
fn report_is_sorted_for_a_stable_log_line() {
    let params = supplied(&[("zeta", "1"), ("alpha", "2"), ("mu", "3")]);
    let args = guacd_args(&["hostname"]);

    assert_eq!(
        vec!["alpha", "mu", "zeta"],
        dropped_connect_params(&params, &args)
    );
}

// The mirror of the above, for the direction where we are the server: a client that
// sends more `connect` values than we advertised in `args` has the tail discarded by
// the positional mapping. Same silent-discard class, opposite direction.

fn values(v: &[&str]) -> Vec<String> {
    v.iter().map(|s| (*s).to_string()).collect()
}

#[test]
fn counts_non_empty_values_past_the_advertised_list() {
    let sent = values(&["host.example", "svc", "secret", "30", "yes"]);
    let advertised = ["hostname", "username", "password"];

    assert_eq!(2, excess_connect_values(&sent, &advertised));
}

#[test]
fn empty_excess_values_are_not_counted() {
    // A client padding the connect instruction to our full arg count discards nothing.
    let sent = values(&["host.example", "svc", "secret", "", ""]);
    let advertised = ["hostname", "username", "password"];

    assert_eq!(0, excess_connect_values(&sent, &advertised));
}

#[test]
fn only_the_non_empty_tail_entries_count() {
    let sent = values(&["host.example", "", "30"]);
    let advertised = ["hostname"];

    assert_eq!(1, excess_connect_values(&sent, &advertised));
}

#[test]
fn nothing_is_excess_when_the_client_sends_no_more_than_advertised() {
    let sent = values(&["host.example", "svc"]);
    let advertised = ["hostname", "username", "password"];

    assert_eq!(0, excess_connect_values(&sent, &advertised));
}

#[test]
fn empty_values_inside_the_advertised_range_are_not_excess() {
    // Empties within range are simply omitted from params, not discarded overflow.
    let sent = values(&["host.example", "", ""]);
    let advertised = ["hostname", "username", "password"];

    assert_eq!(0, excess_connect_values(&sent, &advertised));
}
