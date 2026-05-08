"""End-to-end test of the KDE Connect takeover listener.

Simulates a paired Android phone TCP-connecting to SAGE's listener,
sending a fake SMS via the KDE Connect protocol, and verifies the
listener's callback fires with the right sender + body.

If this test passes, the wire protocol code is correct end-to-end and
any failure on a real user's machine is environmental (firewall,
kdeconnectd respawn, network reachability, plugin permissions). If it
fails, there's a real bug in the listener.

Run: python3 -m sage.core.kdeconnect_e2e_check
"""
from __future__ import annotations

import json
import socket
import ssl
import sys
import tempfile
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sage.core.kdeconnect_listener import (
    KDC_PORT,
    KDEConnectInboundListener,
    _identity_packet,
    _recv_packet,
    _send_packet,
)


def _ensure_cryptography() -> None:
    """Auto-install `cryptography` if missing (it's not a hard dep of sage)."""
    try:
        import cryptography  # noqa: F401
        return
    except ImportError:
        pass
    print("Installing `cryptography` for cert generation (one-time)...")
    import subprocess
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", "cryptography"]
    try:
        from sage.core.updater import _is_user_install
        if _is_user_install():
            cmd.insert(-1, "--user")
    except Exception:
        pass
    try:
        subprocess.run(cmd, check=True, timeout=180)
    except subprocess.CalledProcessError as exc:
        # Try with --user if the plain install failed (PEP 668 distros, etc.)
        if "--user" not in cmd:
            cmd.insert(-1, "--user")
            subprocess.run(cmd, check=True, timeout=180)
        else:
            raise
    import cryptography  # noqa: F401


def _gen_cert(common_name: str, tmpdir: Path) -> tuple[Path, Path]:
    """Generate a self-signed cert+key with the given CN."""
    _ensure_cryptography()
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "KDE"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "KDE Connect"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc) - timedelta(days=1))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=30))
        .sign(key, hashes.SHA256())
    )
    cert_path = tmpdir / f"{common_name}.cert.pem"
    key_path = tmpdir / f"{common_name}.key.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    return cert_path, key_path


def run() -> bool:
    received: list[dict] = []
    expected_sender = "+14085073140"
    expected_body = "Hello sage — e2e test"

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        desktop_id = "desktopdeadbeef00000000000000aaaa"
        phone_id   = "phonecafef00d00000000000000000bbb"
        desktop_cert, desktop_key = _gen_cert(desktop_id, td_path)
        phone_cert, phone_key     = _gen_cert(phone_id, td_path)

        # Skip listener.start() — that kills kdeconnectd which we don't have.
        # Set the internal state the protocol code reads from.
        listener = KDEConnectInboundListener(callback=lambda p: received.append(p))
        listener._device_id  = desktop_id
        listener._cert       = desktop_cert
        listener._key        = desktop_key
        listener._actual_name = "Test Desktop"

        listener_thread = threading.Thread(target=listener._run, daemon=True)
        listener_thread.start()
        # Let the listener bind UDP+TCP. If kdeconnectd is running on this
        # host the bind will fail and the test is invalid for that reason.
        time.sleep(1.5)

        # Connect as "phone" — plain TCP first, identity exchange, then
        # TLS upgrade. This matches the "plain text path" in
        # `_handle_inbound_tcp`.
        try:
            sock = socket.create_connection(("127.0.0.1", KDC_PORT), timeout=5)
        except OSError as exc:
            print(f"FAIL: Couldn't connect to listener — {exc}")
            print("(Is kdeconnectd or another process holding port 1716 on this host?)")
            return False

        try:
            sock.settimeout(8)

            # Step 1: send our identity. Phone deviceType must be "phone"
            # so the listener treats us as a paired peer.
            ident = _identity_packet(phone_id, "Test Pixel", KDC_PORT)
            ident["body"]["deviceType"] = "phone"
            _send_packet(sock, ident)

            # Step 2: receive desktop's identity reply.
            buf = bytearray()
            desktop_pkt = _recv_packet(sock, buf)
            if not desktop_pkt or desktop_pkt.get("type") != "kdeconnect.identity":
                print(f"FAIL: didn't get desktop identity, got {desktop_pkt!r}")
                return False
            print(f"  ✓ desktop identity received: deviceId={desktop_pkt['body'].get('deviceId')}")

            # Step 3: TLS upgrade — phone is the TLS CLIENT here.
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.load_cert_chain(certfile=str(phone_cert), keyfile=str(phone_key))
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE  # KDE Connect pins out-of-band
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2

            try:
                tls = ctx.wrap_socket(
                    sock,
                    server_hostname=desktop_id or "kdeconnect",
                    do_handshake_on_connect=True,
                )
            except ssl.SSLError as exc:
                print(f"FAIL: TLS handshake failed — {exc}")
                return False
            print("  ✓ TLS handshake completed")

            # Step 4: drain any subscribe packets from the desktop
            # (request_conversations, notification.request).
            tls.settimeout(2)
            ssl_buf = bytearray()
            saw_subs: list[str] = []
            for _ in range(4):
                try:
                    pkt = _recv_packet(tls, ssl_buf)
                    if pkt:
                        saw_subs.append(pkt.get("type", ""))
                except socket.timeout:
                    break
                except Exception:
                    break
            if saw_subs:
                print(f"  ✓ subscribe requests from desktop: {saw_subs}")
            else:
                print("  ! no subscribe requests received (test still proceeds)")

            # Step 5: send three fake SMS packets to verify all the cases
            # we care about — type=1 (regular inbound), type=2 (sent;
            # self-SMS scenario), and a sage-feedback packet that should
            # be filtered out.
            tls.settimeout(5)
            now_ms = int(time.time() * 1000)

            # Case A: regular inbound (type=1)
            _send_packet(tls, {
                "id":   now_ms,
                "type": "kdeconnect.sms.messages",
                "body": {"messages": [{
                    "type":      1,
                    "addresses": [{"address": expected_sender}],
                    "body":      expected_body,
                    "date":      now_ms,
                    "thread_id": 12345,
                    "_id":       67890,
                }]},
            })
            print("  ✓ sent type=1 (regular inbound) SMS")

            # Case B: self-SMS surfacing as type=2 (sent). Used to be dropped.
            self_sms_body = "@help from self-text"
            _send_packet(tls, {
                "id":   now_ms + 1,
                "type": "kdeconnect.sms.messages",
                "body": {"messages": [{
                    "type":      2,
                    "addresses": [{"address": expected_sender}],
                    "body":      self_sms_body,
                    "date":      now_ms + 1,
                    "thread_id": 12345,
                    "_id":       67891,
                }]},
            })
            print("  ✓ sent type=2 (self-SMS) packet")

            # Case C: sage's own reply echoed back — should be filtered.
            _send_packet(tls, {
                "id":   now_ms + 2,
                "type": "kdeconnect.sms.messages",
                "body": {"messages": [{
                    "type":      1,
                    "addresses": [{"address": expected_sender}],
                    "body":      "[SAGE — Test Desktop] Help: any text → run as task",
                    "date":      now_ms + 2,
                    "thread_id": 12345,
                    "_id":       67892,
                }]},
            })
            print("  ✓ sent feedback-loop packet (should be filtered)")

            # Step 6: wait for the listener's callback to fire.
            # Expect 2 dispatches: type=1 + type=2. Feedback packet dropped.
            for _ in range(40):
                if len(received) >= 2:
                    break
                time.sleep(0.1)
        finally:
            try: sock.close()
            except Exception: pass

        listener.stop()

    if not received:
        print("FAIL: callback never fired — listener didn't dispatch any SMS")
        return False
    # Expect exactly 2 dispatches: the regular inbound AND the type=2
    # self-SMS. The "[SAGE — …]" feedback packet should be filtered out.
    if len(received) != 2:
        print(f"FAIL: expected 2 callbacks, got {len(received)}:")
        for r in received:
            print(f"   - {r}")
        return False

    bodies = [p.get("text") for p in received]
    if expected_body not in bodies:
        print(f"FAIL: regular inbound SMS missing — got {bodies!r}")
        return False
    if "@help from self-text" not in bodies:
        print(f"FAIL: type=2 self-SMS got dropped — got {bodies!r}")
        return False
    if any(b and b.startswith("[SAGE") for b in bodies):
        print(f"FAIL: feedback-loop packet wasn't filtered — got {bodies!r}")
        return False

    print(f"  ✓ callback dispatched 2 messages, feedback filtered:")
    for p in received:
        print(f"      • from={p['from']!r} text={p['text']!r}")
    return True


if __name__ == "__main__":
    print("E2E test: KDE Connect takeover listener")
    print("=" * 50)
    ok = run()
    print("=" * 50)
    print("PASS ✅" if ok else "FAIL ❌")
    sys.exit(0 if ok else 1)
