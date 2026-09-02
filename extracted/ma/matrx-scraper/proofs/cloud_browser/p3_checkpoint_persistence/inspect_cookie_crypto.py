"""P3 addendum — what actually protects the cookies INSIDE a checkpoint.

PHASE-0 PROOF HARNESS. NOT SHIPPED CODE.
Run AFTER run_proof.py:  python3 inspect_cookie_crypto.py

PLAN.md's threat model says a profile is "a credential bundle even when the Chrome
password manager is disabled". This script measures exactly how weak the inner layer
is on a keyring-less Linux worker, and reports the cookie encryption scheme in use,
because that scheme decides whether a checkpoint is portable at all.

  v10 = Chromium "basic" password store: key = PBKDF2-SHA1('peanuts', 'saltysalt', 1).
        A PUBLIC CONSTANT. Portable across hosts -> restore works anywhere.
        Also: anyone holding the plaintext archive reads every session cookie.
  v11 = key held by gnome-keyring / kwallet, OUTSIDE the profile directory.
        NOT portable -> a checkpoint restored on another worker decrypts to garbage
        and the user is silently signed out while every hash/manifest check passes.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from matrx_orm import read_local_sqlite_rows

HERE = Path(__file__).parent
DEFAULT = HERE / "out" / "work" / "restore_target" / "profile"


def main(profile: Path) -> int:
    local_state = profile / "Local State"
    if local_state.exists():
        osc = json.loads(local_state.read_text()).get("os_crypt", "ABSENT")
        print(f"Local State os_crypt: {json.dumps(osc)[:200]}")

    ck = profile / "Default" / "Cookies"
    if not ck.exists():
        print(f"no Cookies db at {ck}")
        return 1
    tmp = HERE / "out" / "cookies.readcopy"
    shutil.copy2(ck, tmp)
    rows = read_local_sqlite_rows(
        tmp,
        table="cookies",
        columns=("host_key", "name", "encrypted_value"),
    )
    tmp.unlink(missing_ok=True)
    if not rows:
        print("Cookies db has ZERO rows.")
        return 1

    for host, name, enc in rows:
        scheme = enc[:3].decode(errors="replace")
        print(f"\ncookie {name}@{host}: scheme={scheme} len={len(enc)}")
        if scheme != "v10":
            print(
                "  -> NOT the basic store; key lives outside the profile. "
                "This checkpoint is NOT portable to another worker."
            )
            continue
        key = PBKDF2HMAC(
            algorithm=hashes.SHA1(), length=16, salt=b"saltysalt", iterations=1
        ).derive(b"peanuts")
        dec = Cipher(algorithms.AES(key), modes.CBC(b" " * 16)).decryptor()
        pt = dec.update(enc[3:]) + dec.finalize()
        # Modern Chromium prepends a 32-byte SHA-256 domain binding to the value.
        print(f"  decrypted with the PUBLIC CONSTANT 'peanuts': {pt!r}")
        print(
            "  -> the inner layer protects nothing against anyone holding the "
            "plaintext archive. Envelope encryption is the ONLY real protection."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT))
