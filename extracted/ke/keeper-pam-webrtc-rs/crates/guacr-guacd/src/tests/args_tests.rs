use crate::args::{get_protocol_arg_names, get_protocol_args, ArgDescriptor};

#[test]
fn test_get_protocol_args() {
    assert!(get_protocol_args("ssh").is_some());
    assert!(get_protocol_args("rdp").is_some());
    assert!(get_protocol_args("vnc").is_some());
    assert!(get_protocol_args("mysql").is_some());
    assert!(get_protocol_args("unknown").is_none());
}

#[test]
fn test_get_protocol_arg_names() {
    let ssh_args = get_protocol_arg_names("ssh");
    assert!(ssh_args.contains(&"hostname"));
    assert!(ssh_args.contains(&"username"));
    assert!(ssh_args.contains(&"password"));

    let rdp_args = get_protocol_arg_names("rdp");
    assert!(rdp_args.contains(&"hostname"));
    assert!(rdp_args.contains(&"domain"));
}

#[test]
fn test_arg_descriptor() {
    let required = ArgDescriptor::required("hostname");
    assert!(required.required);
    assert_eq!(required.name, "hostname");

    let optional = ArgDescriptor::optional("port");
    assert!(!optional.required);
    assert_eq!(optional.name, "port");
}
