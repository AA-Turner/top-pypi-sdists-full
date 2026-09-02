"""P3 — checkpoint persistence round trip. PHASE-0 PROOF HARNESS, NOT SHIPPED CODE.

Runs the PLAN.md Stop/Start sequence for real:

  live state  -> clean close -> archive -> AES-256-GCM envelope encrypt
              -> DESTROY the profile directory -> restore elsewhere -> relaunch
              -> assert still authenticated, localStorage/IndexedDB/history intact

plus the negative half: live-directory copy, byte flip, wrong encryption context,
truncation, and manifest hash mismatch must all fail closed.

Run with:   xvfb-run -a python3 run_proof.py
Results:    ./out/results.json  and  ./out/run.log
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright
from matrx_orm import read_local_sqlite_rows

sys.path.insert(0, str(Path(__file__).parent))
from envelope import (  # noqa: E402
    CheckpointVerificationError,
    LocalKmsSubstitute,
    decrypt_checkpoint,
    encrypt_checkpoint,
)

HERE = Path(__file__).parent
OUT = HERE / "out"
WORK = OUT / "work"
APP_PORT = 8731
BASE = f"http://127.0.0.1:{APP_PORT}"
PROFILE_ID = "p3-profile-0000-4000-8000-000000000001"
KEY_VERSION = "v1"
PURPOSE = "browser_profile_checkpoint"
KMS_KEY_ID = "alias/p3-stand-in-not-real-kms"

LS_VALUE = "p3-localstorage-value-9f2a"
IDB_VALUE = "p3-indexeddb-record-71c4"

RESULTS: dict = {"sub_claims": {}, "measurements": {}, "observations": {}}
LOG_LINES: list[str] = []


def log(msg: str = ""):
    line = str(msg)
    print(line, flush=True)
    LOG_LINES.append(line)


def section(t: str):
    log("")
    log("=" * 78)
    log(t)
    log("=" * 78)


def dir_bytes(p: Path) -> int:
    return sum(f.stat().st_size for f in Path(p).rglob("*") if f.is_file())


def dir_files(p: Path) -> int:
    return sum(1 for f in Path(p).rglob("*") if f.is_file())


def chromium_procs(user_data_dir: Path) -> list[str]:
    r = subprocess.run(
        ["pgrep", "-af", f"user-data-dir={user_data_dir}"],
        capture_output=True,
        text=True,
    )
    return [line for line in r.stdout.strip().splitlines() if line]


def tar_dir(src: Path, dest_tar: Path) -> float:
    t0 = time.perf_counter()
    with tarfile.open(dest_tar, "w") as tf:
        tf.add(src, arcname="profile")
    return time.perf_counter() - t0


def untar(src_tar: Path, dest_parent: Path) -> Path:
    dest_parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(src_tar, "r") as tf:
        tf.extractall(dest_parent)
    return dest_parent / "profile"


# ---------------------------------------------------------------- browser steps


def read_state(page) -> dict:
    page.goto(BASE + "/", wait_until="load")
    page.wait_for_function(
        "document.getElementById('authstate').dataset.auth !== undefined", timeout=15000
    )
    page.wait_for_function(
        "document.getElementById('idbstate').dataset.v !== undefined", timeout=15000
    )
    return page.evaluate(
        """() => ({
            auth: document.getElementById('authstate').dataset.auth === '1',
            authText: document.getElementById('authstate').textContent,
            ls: localStorage.getItem('p3_pref'),
            idb: document.getElementById('idbstate').dataset.v,
        })"""
    )


def launch(user_data_dir: Path):
    pw = sync_playwright().start()
    ctx = pw.chromium.launch_persistent_context(
        str(user_data_dir),
        headless=False,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
        viewport={"width": 1280, "height": 800},
    )
    return pw, ctx


def close_cleanly(pw, ctx, user_data_dir: Path) -> float:
    """PLAN.md Stop step 2: close Playwright/Chromium so SQLite files settle."""
    t0 = time.perf_counter()
    ctx.close()
    pw.stop()
    for _ in range(100):
        if not chromium_procs(user_data_dir):
            break
        time.sleep(0.1)
    return time.perf_counter() - t0


def history_rows(profile_dir: Path) -> list[str]:
    hist = profile_dir / "Default" / "History"
    if not hist.exists():
        return []
    tmp = profile_dir.parent / "History.readcopy"
    shutil.copy2(hist, tmp)
    try:
        return [
            str(row[0])
            for row in read_local_sqlite_rows(
                tmp,
                table="urls",
                columns=("url",),
                order_by=("id",),
            )
        ]
    finally:
        tmp.unlink(missing_ok=True)


# ---------------------------------------------------------------------- main


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    WORK.mkdir(parents=True)

    app = subprocess.Popen(
        [sys.executable, str(HERE / "testapp.py"), str(APP_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(1.0)
    if app.poll() is not None:
        log("FATAL: test app died: " + (app.stdout.read() if app.stdout else ""))
        return 1

    try:
        return run(app)
    finally:
        app.terminate()
        try:
            app.wait(timeout=5)
        except Exception:
            app.kill()
        (OUT / "run.log").write_text("\n".join(LOG_LINES) + "\n")
        (OUT / "results.json").write_text(json.dumps(RESULTS, indent=2, sort_keys=True))


def run(app) -> int:
    kms = LocalKmsSubstitute(WORK / "stand_in_master.key")
    orig = WORK / "profile_original"

    # ---------------------------------------------------------------- STEP 1/2
    section("STEP 1-2 — launch persistent context, establish real logged-in state")
    pw, ctx = launch(orig)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    chromium_version = ctx.browser.version if ctx.browser else "unknown"
    log(f"Chromium version: {chromium_version}")
    log(f"executable: {pw.chromium.executable_path}")

    before = read_state(page)
    log(f"pre-login state: {before}")

    page.goto(BASE + "/")
    page.click("#loginbtn")
    page.wait_for_load_state("load")
    page.evaluate(f"localStorage.setItem('p3_pref', '{LS_VALUE}')")
    page.evaluate(f"window.p3.idbPut('p3_record', '{IDB_VALUE}')")
    time.sleep(0.5)
    page.goto(BASE + "/page2")
    page.goto(BASE + "/page3")

    live = read_state(page)
    log(f"post-login state: {live}")
    RESULTS["observations"]["state_before_checkpoint"] = live
    assert live["auth"] and live["ls"] == LS_VALUE and live["idb"] == IDB_VALUE, (
        "could not establish the state under test"
    )

    cookies = ctx.cookies(BASE)
    log(
        f"cookies: {[{k: c[k] for k in ('name', 'domain', 'path', 'httpOnly', 'expires')} for c in cookies]}"
    )
    RESULTS["observations"]["cookie_httponly"] = any(
        c["name"] == "p3_session" and c["httpOnly"] for c in cookies
    )

    # ------------------------------------------------- STEP 3a: LIVE-COPY probe
    section("STEP 3a — archive attempt WHILE Chromium is still running (must be invalid)")
    live_procs = chromium_procs(orig)
    log(f"chromium processes matching this profile: {len(live_procs)}")
    for p in live_procs[:4]:
        log("  " + p[:150])

    live_tar = WORK / "live_copy.tar"
    live_tar_secs = tar_dir(orig, live_tar)
    log(f"live archive taken anyway: {live_tar.stat().st_size} bytes in {live_tar_secs:.2f}s")

    lockish_live = sorted(
        str(f.relative_to(orig))
        for f in orig.rglob("*")
        if any(s in f.name for s in ("lock", "Lock", "LOCK", "journal", "-wal", "-shm", ".tmp"))
    )
    log("lock/journal artefacts present WHILE RUNNING:")
    for f in lockish_live:
        fp = orig / f
        kind = "symlink->" + os.readlink(fp) if fp.is_symlink() else f"{fp.stat().st_size}B"
        log(f"  {f}  ({kind})")
    RESULTS["observations"]["live_lock_artifacts"] = lockish_live

    # ---------------------------------------------------------------- STEP 3b
    section("STEP 3b — clean close (PLAN.md Stop step 2)")
    t_stop0 = time.perf_counter()
    close_secs = close_cleanly(pw, ctx, orig)
    remaining = chromium_procs(orig)
    log(f"ctx.close() + process exit took {close_secs:.2f}s; remaining processes: {len(remaining)}")
    RESULTS["sub_claims"]["clean_close_chromium_exited"] = "PASS" if not remaining else "FAIL"

    lockish_closed = sorted(
        str(f.relative_to(orig))
        for f in orig.rglob("*")
        if any(s in f.name for s in ("lock", "Lock", "LOCK", "journal", "-wal", "-shm", ".tmp"))
    )
    log("lock/journal artefacts present AFTER CLEAN CLOSE:")
    for f in lockish_closed or ["  (none)"]:
        log(f"  {f}")
    RESULTS["observations"]["closed_lock_artifacts"] = lockish_closed

    sqlite_files = sorted(
        str(f.relative_to(orig))
        for f in orig.rglob("*")
        if f.is_file()
        and f.name
        in ("Cookies", "History", "Web Data", "Login Data", "Favicons", "Network Action Predictor")
    )
    log("key SQLite files: " + ", ".join(sqlite_files))
    RESULTS["observations"]["sqlite_files"] = sqlite_files
    hist = history_rows(orig)
    log(f"history rows in closed profile: {len(hist)} -> {hist}")
    RESULTS["observations"]["history_before"] = hist

    profile_size = dir_bytes(orig)
    RESULTS["measurements"]["profile_dir_bytes"] = profile_size
    RESULTS["measurements"]["profile_dir_files"] = dir_files(orig)
    RESULTS["measurements"]["clean_close_secs"] = round(close_secs, 3)
    log(f"profile dir: {profile_size} bytes / {dir_files(orig)} files")

    # ---------------------------------------------------------------- STEP 4
    section("STEP 4 — archive + AES-256-GCM envelope encrypt (KMS wrapper = LOCAL STAND-IN)")
    tar_path = WORK / "checkpoint.tar"
    tar_secs = tar_dir(orig, tar_path)
    tar_size = tar_path.stat().st_size
    log(f"tar: {tar_size} bytes in {tar_secs:.2f}s")

    ct_path = WORK / "checkpoint.bin"
    t0 = time.perf_counter()
    manifest = encrypt_checkpoint(
        tar_path,
        ct_path,
        kms,
        KMS_KEY_ID,
        PROFILE_ID,
        KEY_VERSION,
        PURPOSE,
        chromium_version,
        datetime.now(UTC).isoformat(),
    )
    enc_secs = time.perf_counter() - t0
    (WORK / "checkpoint.manifest.json").write_text(manifest.to_json())
    log(f"encrypt: {manifest.ciphertext_bytes} bytes in {enc_secs:.3f}s")
    log("manifest:")
    log(manifest.to_json())
    RESULTS["measurements"].update(
        tar_bytes=tar_size,
        tar_secs=round(tar_secs, 3),
        ciphertext_bytes=manifest.ciphertext_bytes,
        encrypt_secs=round(enc_secs, 3),
    )
    assert "dek" not in manifest.to_json().lower().replace("wrapped_dek", "")

    # ---------------------------------------------------------------- STEP 5
    section("STEP 5 — DESTROY the original profile directory, restore to a NEW path")
    shutil.rmtree(orig)
    log(f"original profile exists after rmtree: {orig.exists()}")
    RESULTS["sub_claims"]["original_destroyed"] = "PASS" if not orig.exists() else "FAIL"

    restored_tar = WORK / "restored.tar"
    t0 = time.perf_counter()
    n = decrypt_checkpoint(ct_path, manifest, restored_tar, kms)
    dec_secs = time.perf_counter() - t0
    log(f"decrypt+verify: {n} bytes in {dec_secs:.3f}s")
    new_profile = untar(restored_tar, WORK / "restore_target")
    t_restore_ready = time.perf_counter()
    log(f"restored to NEW path: {new_profile}")
    RESULTS["measurements"]["decrypt_secs"] = round(dec_secs, 3)

    hist_after = history_rows(new_profile)
    log(f"history rows in restored profile: {len(hist_after)} -> {hist_after}")
    RESULTS["observations"]["history_after"] = hist_after

    pw2, ctx2 = launch(new_profile)
    page2 = ctx2.pages[0] if ctx2.pages else ctx2.new_page()
    after = read_state(page2)
    total_stop_to_restore = time.perf_counter() - t_stop0
    log(f"post-restore state: {after}")
    close_cleanly(pw2, ctx2, new_profile)

    ok_auth = after["auth"] is True
    ok_ls = after["ls"] == LS_VALUE
    ok_idb = after["idb"] == IDB_VALUE
    ok_hist = set(hist) == set(hist_after) and len(hist_after) > 0
    RESULTS["observations"]["state_after_restore"] = after
    RESULTS["sub_claims"]["restore_still_authenticated"] = "PASS" if ok_auth else "FAIL"
    RESULTS["sub_claims"]["restore_localstorage"] = "PASS" if ok_ls else "FAIL"
    RESULTS["sub_claims"]["restore_indexeddb"] = "PASS" if ok_idb else "FAIL"
    RESULTS["sub_claims"]["restore_history"] = "PASS" if ok_hist else "FAIL"
    RESULTS["measurements"]["stop_to_restore_ready_secs"] = round(t_restore_ready - t_stop0, 3)
    RESULTS["measurements"]["stop_to_verified_relaunch_secs"] = round(total_stop_to_restore, 3)
    log(f"auth={ok_auth} ls={ok_ls} idb={ok_idb} history={ok_hist}")

    # ------------------------------------------------ STEP 5b: live-copy replay
    section("STEP 5b — restore the LIVE (mid-write) copy and launch it")
    live_profile = untar(live_tar, WORK / "live_restore_target")
    live_lock_after = sorted(
        str(f.relative_to(live_profile))
        for f in live_profile.rglob("*")
        if any(s in f.name for s in ("lock", "Lock", "LOCK", "journal", "-wal", "-shm"))
    )
    log("artefacts carried into the live-copy restore: " + json.dumps(live_lock_after))
    try:
        pw3, ctx3 = launch(live_profile)
        page3 = ctx3.pages[0] if ctx3.pages else ctx3.new_page()
        live_state = read_state(page3)
        log(f"live-copy restored state: {live_state}")
        close_cleanly(pw3, ctx3, live_profile)
        RESULTS["observations"]["live_copy_restored_state"] = live_state
    except Exception as exc:
        log(f"live-copy restore FAILED to launch: {type(exc).__name__}: {exc}")
        RESULTS["observations"]["live_copy_restored_state"] = f"launch failed: {exc}"

    # ---------------------------------------------------------------- STEP 6
    section("STEP 6 — negative tests: each must FAIL CLOSED and loudly")
    neg: dict = {}

    def negative(name: str, fn):
        target = WORK / f"neg_{name}.out"
        target.unlink(missing_ok=True)
        try:
            fn(target)
        except CheckpointVerificationError as exc:
            neg[name] = {
                "outcome": "FAIL_CLOSED",
                "error": f"CheckpointVerificationError: {exc}",
                "output_written": target.exists(),
            }
        except Exception as exc:
            neg[name] = {
                "outcome": "FAIL_CLOSED",
                "error": f"{type(exc).__name__}: {exc}",
                "output_written": target.exists(),
            }
        else:
            neg[name] = {
                "outcome": "!!! SILENTLY SUCCEEDED !!!",
                "error": None,
                "output_written": target.exists(),
            }
        log(f"[{name}] {neg[name]['outcome']}")
        log(f"    {neg[name]['error']}")
        log(f"    plaintext written? {neg[name]['output_written']}")

    raw_ct = ct_path.read_bytes()

    # (a) flip one byte of ciphertext
    flipped = WORK / "tampered_flip.bin"
    b = bytearray(raw_ct)
    b[len(b) // 2] ^= 0x01
    flipped.write_bytes(bytes(b))
    import dataclasses

    m_flip = dataclasses.replace(
        manifest, ciphertext_sha256=hashlib.sha256(bytes(b)).hexdigest()
    )  # attacker who ALSO rewrites the manifest hash: GCM must still catch it
    negative(
        "byteflip_hash_also_rewritten", lambda out: decrypt_checkpoint(flipped, m_flip, out, kms)
    )
    negative(
        "byteflip_manifest_untouched", lambda out: decrypt_checkpoint(flipped, manifest, out, kms)
    )

    # (b) wrong encryption context — at the KMS unwrap
    negative(
        "wrong_context_at_kms_unwrap",
        lambda out: decrypt_checkpoint(
            ct_path,
            manifest,
            out,
            kms,
            override_context={
                "profile_id": "SOMEONE-ELSES-PROFILE",
                "key_version": KEY_VERSION,
                "purpose": PURPOSE,
            },
        ),
    )
    negative(
        "wrong_purpose_at_kms_unwrap",
        lambda out: decrypt_checkpoint(
            ct_path,
            manifest,
            out,
            kms,
            override_context={
                "profile_id": PROFILE_ID,
                "key_version": KEY_VERSION,
                "purpose": "screenshot_artifact",
            },
        ),
    )

    # (b2) wrong encryption context at the PAYLOAD layer only (correct DEK obtained)
    def payload_ctx_only(out):
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from envelope import context_aad, unb64

        dek = kms.decrypt(
            unb64(manifest.wrapped_dek_b64), manifest.encryption_context, manifest.kms_key_id
        )
        bad = {
            "profile_id": "SOMEONE-ELSES-PROFILE",
            "key_version": KEY_VERSION,
            "purpose": PURPOSE,
        }
        AESGCM(dek).decrypt(unb64(manifest.nonce_b64), raw_ct, context_aad(bad))
        out.write_bytes(b"should never happen")

    negative("wrong_context_at_payload_aad", payload_ctx_only)

    # (c) truncated archive
    trunc = WORK / "truncated.bin"
    trunc.write_bytes(raw_ct[: int(len(raw_ct) * 0.9)])
    negative("truncated_object", lambda out: decrypt_checkpoint(trunc, manifest, out, kms))
    m_trunc = dataclasses.replace(
        manifest,
        ciphertext_bytes=len(raw_ct[: int(len(raw_ct) * 0.9)]),
        ciphertext_sha256=hashlib.sha256(raw_ct[: int(len(raw_ct) * 0.9)]).hexdigest(),
    )
    negative(
        "truncated_object_manifest_rewritten",
        lambda out: decrypt_checkpoint(trunc, m_trunc, out, kms),
    )

    # (d) manifest content hash does not match the checkpoint
    m_badhash = dataclasses.replace(manifest, content_sha256="0" * 64)
    negative(
        "manifest_content_hash_mismatch",
        lambda out: decrypt_checkpoint(ct_path, m_badhash, out, kms),
    )
    m_badcount = dataclasses.replace(manifest, plaintext_bytes=manifest.plaintext_bytes - 1)
    negative(
        "manifest_plaintext_bytecount_mismatch",
        lambda out: decrypt_checkpoint(ct_path, m_badcount, out, kms),
    )

    RESULTS["negative_tests"] = neg
    all_closed = all(
        v["outcome"] == "FAIL_CLOSED" and not v["output_written"] for v in neg.values()
    )
    RESULTS["sub_claims"]["negatives_all_fail_closed"] = "PASS" if all_closed else "FAIL"

    # ---------------------------------------------------------------- summary
    section("SUMMARY")
    for k, v in RESULTS["sub_claims"].items():
        log(f"  {v:5}  {k}")
    log("")
    for k, v in RESULTS["measurements"].items():
        log(f"  {k} = {v}")
    return 0 if all(v == "PASS" for v in RESULTS["sub_claims"].values()) else 2


if __name__ == "__main__":
    sys.exit(main())
