//! What matters is the `connect` instruction that goes on the wire, not the parameter map
//! we assembled beforehand.
//!
//! The instruction is positional: guacd sends an `args` list, and every value is placed by
//! index. A parameter guacd never listed has nowhere to go and is dropped. That is not
//! hypothetical - the gateway set `server-alive-interval` for RDP for months, and because
//! that name only exists in the SSH argument list the value was discarded on every single
//! session in silence.
//!
//! These tests drive a real client-side handshake against a mock guacd that advertises an
//! argument list for the protocol, then assert on the bytes the client emitted.
//!
//! The mock advertises `args::get_protocol_arg_names`, which is our mirror of guacd's
//! `GUAC_*_CLIENT_ARGS`. Against a real guacd the list arrives on the wire instead, so the
//! authority for what guacd accepts is the Guacamole manual, not this crate:
//! <https://guacamole.apache.org/doc/gug/configuring-guacamole.html>. Both facts these
//! tests rely on are documented there - RDP has `domain` ("The domain to use when
//! attempting authentication, if any"), and `server-alive-interval` appears only under
//! SSH's network parameters, described as the interval at which the *SSH* client sends
//! keepalive packets. There is no RDP equivalent to reach for.

use crate::args::get_protocol_arg_names;
use crate::client::perform_guacd_handshake;
use guacr_protocol::{GuacdInstruction, GuacdParser, OwnedInstruction, PeekError};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::Mutex;

fn encode(opcode: &str, args: &[String]) -> bytes::Bytes {
    GuacdParser::guacd_encode_instruction(&GuacdInstruction::new(opcode.to_string(), args.to_vec()))
}

/// Read one complete instruction from `reader`, accumulating until it parses.
async fn read_instruction<R>(reader: &mut R, buf: &mut Vec<u8>) -> OwnedInstruction
where
    R: AsyncReadExt + Unpin,
{
    loop {
        // Try to parse what we already hold before reading more.
        let parsed = match GuacdParser::peek_instruction(buf) {
            Ok(instr) => Some((
                OwnedInstruction::new(
                    instr.opcode.to_string(),
                    instr.args.iter().map(|a| a.to_string()).collect(),
                ),
                instr.total_length_in_buffer,
            )),
            Err(PeekError::Incomplete) => None,
            Err(e) => panic!("mock guacd could not parse client data: {e:?}"),
        };

        if let Some((instr, len)) = parsed {
            buf.drain(..len);
            return instr;
        }

        let mut chunk = [0u8; 1024];
        let n = reader
            .read(&mut chunk)
            .await
            .expect("mock guacd read failed");
        assert_ne!(n, 0, "client closed the connection mid-handshake");
        buf.extend_from_slice(&chunk[..n]);
    }
}

/// Run a full handshake for `protocol` and return the `connect` instruction the client sent,
/// paired with the argument names the mock guacd advertised (same order, so the two zip).
async fn emitted_connect(
    protocol: &str,
    params: &[(&str, &str)],
) -> (Vec<&'static str>, OwnedInstruction) {
    let arg_names = get_protocol_arg_names(protocol);
    assert!(
        !arg_names.is_empty(),
        "no argument descriptors for protocol {protocol}"
    );

    let mut map: HashMap<String, String> = params
        .iter()
        .map(|(k, v)| (k.to_string(), v.to_string()))
        .collect();
    map.insert("protocol".to_string(), protocol.to_string());

    let (client, server) = tokio::io::duplex(64 * 1024);
    let (mut client_read, mut client_write) = tokio::io::split(client);

    let advertised: Vec<String> = arg_names.iter().map(|n| n.to_string()).collect();
    let server_task = tokio::spawn(async move {
        let (mut sr, mut sw) = tokio::io::split(server);
        let mut buf = Vec::new();

        let select = read_instruction(&mut sr, &mut buf).await;
        assert_eq!("select", select.opcode);

        let mut args = vec!["VERSION_1_5_0".to_string()];
        args.extend(advertised.iter().cloned());
        sw.write_all(&encode("args", &args)).await.unwrap();
        sw.flush().await.unwrap();

        // size / audio / video / image precede connect.
        let connect = loop {
            let instr = read_instruction(&mut sr, &mut buf).await;
            if instr.opcode == "connect" {
                break instr;
            }
        };

        sw.write_all(&encode("ready", &["$mock-guacd-id".to_string()]))
            .await
            .unwrap();
        sw.flush().await.unwrap();

        connect
    });

    perform_guacd_handshake(
        &mut client_read,
        &mut client_write,
        "test-channel",
        "test-conversation",
        1,
        Arc::new(Mutex::new(map)),
    )
    .await
    .expect("handshake failed");

    let connect = server_task.await.expect("mock guacd task panicked");
    (arg_names, connect)
}

/// Value the client actually emitted for `name`, read out of the positional connect args.
fn emitted_value<'a>(
    arg_names: &[&'static str],
    connect: &'a OwnedInstruction,
    name: &str,
) -> Option<&'a str> {
    let idx = arg_names.iter().position(|n| *n == name)?;
    // connect args are [version, <value per advertised arg>...]
    connect.args.get(idx + 1).map(|s| s.as_str())
}

#[tokio::test]
async fn rdp_domain_reaches_the_connect_instruction() {
    // The AD ephemeral fix: bare sAMAccountName in username, domain in its own parameter.
    // NTLM resolves the account name against sAMAccountName and has no notion of a UPN, so
    // the two must travel separately.
    let (arg_names, connect) = emitted_connect(
        "rdp",
        &[
            ("hostname", "ch1kproct.eu.belimonet.com"),
            ("username", "keeper_r6yot49hm"),
            ("password", "secret"),
            ("domain", "eu.belimonet.com"),
        ],
    )
    .await;

    assert_eq!("connect", connect.opcode);
    assert!(
        arg_names.contains(&"domain"),
        "guacd's RDP argument list has no `domain` slot, so the value would be discarded"
    );
    assert_eq!(
        Some("eu.belimonet.com"),
        emitted_value(&arg_names, &connect, "domain")
    );
    assert_eq!(
        Some("keeper_r6yot49hm"),
        emitted_value(&arg_names, &connect, "username"),
        "username must stay the bare sAMAccountName, not a UPN"
    );
}

#[tokio::test]
async fn rdp_username_is_never_silently_turned_into_a_upn() {
    // Guards the regression directly: an '@' in the emitted username means we are back to
    // sending a UPN, which NTLM answers with STATUS_NO_SUCH_USER (0xC0000064).
    let (arg_names, connect) = emitted_connect(
        "rdp",
        &[
            ("hostname", "host.example"),
            ("username", "keeper_abc123"),
            ("domain", "ad.example.com"),
        ],
    )
    .await;

    let username = emitted_value(&arg_names, &connect, "username").unwrap();
    assert!(
        !username.contains('@'),
        "emitted username is a UPN: {username}"
    );
}

#[tokio::test]
async fn rdp_has_no_slot_for_server_alive_interval() {
    // Why the gateway-side default was removed rather than "fixed": there is no RDP slot to
    // put it in, and no RDP parameter that means the same thing. The Guacamole manual lists
    // server-alive-interval only under SSH, as an SSH-client keepalive toward the SSH
    // server. RDP's keepalive concern is the Guacamole *user* socket, which is guacd/guacr's
    // own periodic sync, not a connect parameter.
    let rdp = get_protocol_arg_names("rdp");
    let ssh = get_protocol_arg_names("ssh");

    assert!(!rdp.contains(&"server-alive-interval"));
    assert!(ssh.contains(&"server-alive-interval"));
}

#[tokio::test]
async fn an_unrequested_parameter_is_dropped_from_the_wire() {
    // The failure mode itself: supplied, accepted without complaint, absent from connect.
    // guacr now warns when this happens; this test pins the behaviour it warns about.
    let (arg_names, connect) = emitted_connect(
        "rdp",
        &[
            ("hostname", "host.example"),
            ("username", "svc"),
            ("server-alive-interval", "30"),
        ],
    )
    .await;

    // Exactly one value per advertised argument, plus the leading version.
    assert_eq!(arg_names.len() + 1, connect.args.len());
    assert!(
        !connect.args.iter().any(|a| a == "30"),
        "a parameter guacd never asked for still reached the wire"
    );
}

#[tokio::test]
async fn ssh_does_carry_server_alive_interval() {
    // Same value, same map, different protocol: on SSH it has a slot and arrives.
    let (arg_names, connect) = emitted_connect(
        "ssh",
        &[
            ("hostname", "host.example"),
            ("username", "svc"),
            ("server-alive-interval", "30"),
        ],
    )
    .await;

    assert_eq!(
        Some("30"),
        emitted_value(&arg_names, &connect, "server-alive-interval")
    );
}
