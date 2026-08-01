"""bingo/tools/cognito_srp.py — AWS Cognito SRP 인증 (v1.1.0)

기록.md에서 반복 실패한 SRP 버그 수정:
  1. k값 오류: pad_hex(N) | pad_hex(g) SHA256 으로 재계산
  2. pad_hex: high-bit set 시 '00' prefix 필요
  3. pool_name: user_pool_id.split('_')[1] (언더스코어 뒤)
  4. x 계산: H(pad(salt) | H(pool_name + username + ':' + password))
  5. HKDF salt: pad_hex(u_value) bytes
  6. 서명 메시지: pool_name + username + secret_block_bytes + timestamp
  7. TIMESTAMP: 서버가 아닌 클라이언트에서 생성

참고: warrant / amazon-cognito-identity-js 구현
"""
from __future__ import annotations

import base64
import binascii
import datetime
import hashlib
import hmac
import os
import re
from dataclasses import dataclass
from typing import Any

import httpx


# ── SRP 상수 ────────────────────────────────────────────────────────────────

N_HEX = (
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64"
    "ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7"
    "ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6B"
    "F12FFA06D98A0864D87602733EC86A64521F2B18177B200C"
    "BBE117577A615D6C770988C0BAD946E208E24FA074E5AB31"
    "43DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF"
)

N = int(N_HEX, 16)
g = 2

# k = SHA256(pad(N) | pad(g))  — warrant 방식
def _compute_k() -> int:
    padded_n = _pad_hex_str(N_HEX)
    padded_g = _pad_hex_str(format(g, 'x'))
    return int(hashlib.sha256(
        binascii.unhexlify(padded_n) + binascii.unhexlify(padded_g)
    ).hexdigest(), 16)


# ── 헬퍼 함수 ────────────────────────────────────────────────────────────────

def _pad_hex_str(h: str) -> str:
    """hex 문자열 정규화: 홀수 길이 보정 + high-bit 시 00 prefix"""
    if len(h) % 2 == 1:
        h = '0' + h
    elif h[0] in '89ABCDEFabcdef':
        h = '00' + h
    return h


def _int_to_padded_hex(n: int) -> str:
    return _pad_hex_str(format(n, 'x'))


def _hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _hex_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _compute_hkdf(ikm: bytes, salt: bytes) -> bytes:
    """Cognito HKDF — 16바이트 반환"""
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    info = b"Caldera Derived Key\x01"
    return hmac.new(prk, info, hashlib.sha256).digest()[:16]


def _get_timestamp() -> str:
    """Cognito 요구 timestamp 형식: 'Thu Jul  3 12:00:00 UTC 2026'"""
    now = datetime.datetime.utcnow()
    ts = now.strftime("%a %b %d %H:%M:%S UTC %Y")
    # 날짜 앞 0 제거 (01 → ' 1', but some impls keep space)
    ts = re.sub(r" 0(\d) ", r"  \1 ", ts)
    return ts


# ── 핵심 SRP 계산 ────────────────────────────────────────────────────────────

def _compute_srp_response(
    username: str,
    password: str,
    user_pool_id: str,
    srp_b_hex: str,
    salt_hex: str,
    secret_block_b64: str,
    a: int,
    A: int,
) -> tuple[str, str]:
    """SRP PASSWORD_VERIFIER 응답 계산

    Returns:
        (PASSWORD_CLAIM_SIGNATURE, TIMESTAMP)
    """
    k = _compute_k()

    # pool_name = 언더스코어 뒤 부분 ("eu-central-1_W7ZDh3Al1" → "W7ZDh3Al1")
    pool_name = user_pool_id.split('_')[1]

    B = int(srp_b_hex, 16)
    salt_bytes = binascii.unhexlify(salt_hex)

    # u = SHA256(pad(A) | pad(B))
    a_hex = _int_to_padded_hex(A)
    b_hex = _pad_hex_str(srp_b_hex)
    u = int(hashlib.sha256(
        binascii.unhexlify(a_hex) + binascii.unhexlify(b_hex)
    ).hexdigest(), 16)

    # x = SHA256(pad(salt) | SHA256(pool_name + username + ":" + password))
    auth_str = f"{pool_name}{username}:{password}"
    auth_hash = hashlib.sha256(auth_str.encode('utf-8')).digest()
    salt_padded = binascii.unhexlify(_pad_hex_str(salt_hex))
    x = int(hashlib.sha256(salt_padded + auth_hash).hexdigest(), 16)

    # S = (B - k * g^x) ^ (a + u * x) mod N
    g_mod_pow_xn = pow(g, x, N)
    int2 = (B - k * g_mod_pow_xn) % N
    S = pow(int2, a + u * x, N)

    # HKDF(ikm=pad(S), salt=pad(u))
    ikm = bytearray.fromhex(_int_to_padded_hex(S))
    salt_u = bytearray.fromhex(_int_to_padded_hex(u))
    hkdf_key = _compute_hkdf(bytes(ikm), bytes(salt_u))

    # 서명 = HMAC(hkdf_key, pool_name | username | secret_block_bytes | timestamp)
    timestamp = _get_timestamp()
    secret_block_bytes = base64.standard_b64decode(secret_block_b64)

    msg = (
        pool_name.encode('utf-8') +
        username.encode('utf-8') +
        secret_block_bytes +
        timestamp.encode('utf-8')
    )
    sig = base64.standard_b64encode(
        hmac.new(hkdf_key, msg, hashlib.sha256).digest()
    ).decode('utf-8')

    return sig, timestamp


# ── 공개 API ─────────────────────────────────────────────────────────────────

@dataclass
class CognitoSRPResult:
    success: bool
    id_token: str = ""
    access_token: str = ""
    refresh_token: str = ""
    error: str = ""
    raw: dict | None = None


def authenticate_srp(
    username: str,
    password: str,
    client_id: str,
    user_pool_id: str,
    region: str = "eu-central-1",
    timeout: float = 30.0,
) -> CognitoSRPResult:
    """AWS Cognito USER_SRP_AUTH 전체 플로우

    Args:
        username:     Cognito 사용자명
        password:     비밀번호
        client_id:    App Client ID
        user_pool_id: User Pool ID (예: eu-central-1_W7ZDh3Al1)
        region:       AWS 리전
        timeout:      HTTP 타임아웃(초)
    """
    endpoint = f"https://cognito-idp.{region}.amazonaws.com/"
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
    }

    client = httpx.Client(timeout=timeout, verify=True)

    try:
        # ── Step 1: InitiateAuth ──────────────────────────────────────────
        a = int.from_bytes(os.urandom(128), 'big') % N
        A = pow(g, a, N)

        r1 = client.post(
            endpoint,
            headers={**headers, "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth"},
            json={
                "AuthFlow": "USER_SRP_AUTH",
                "ClientId": client_id,
                "AuthParameters": {
                    "USERNAME": username,
                    "SRP_A": format(A, 'x'),
                },
            },
        )

        if r1.status_code != 200:
            return CognitoSRPResult(
                success=False,
                error=f"InitiateAuth {r1.status_code}: {r1.text[:300]}",
            )

        data1 = r1.json()
        if data1.get("ChallengeName") != "PASSWORD_VERIFIER":
            return CognitoSRPResult(
                success=False,
                error=f"Unexpected challenge: {data1.get('ChallengeName')} | {data1}",
                raw=data1,
            )

        params = data1["ChallengeParameters"]
        # Cognito가 반환하는 실제 username 사용 (alias 처리)
        srp_username = params.get("USER_ID_FOR_SRP", username)

        # ── Step 2: 서명 계산 ─────────────────────────────────────────────
        sig, timestamp = _compute_srp_response(
            username=srp_username,
            password=password,
            user_pool_id=user_pool_id,
            srp_b_hex=params["SRP_B"],
            salt_hex=params["SALT"],
            secret_block_b64=params["SECRET_BLOCK"],
            a=a,
            A=A,
        )

        # ── Step 3: RespondToAuthChallenge ────────────────────────────────
        respond_body: dict[str, Any] = {
            "ChallengeName": "PASSWORD_VERIFIER",
            "ClientId": client_id,
            "ChallengeResponses": {
                "USERNAME": srp_username,
                "PASSWORD_CLAIM_SECRET_BLOCK": params["SECRET_BLOCK"],
                "PASSWORD_CLAIM_SIGNATURE": sig,
                "TIMESTAMP": timestamp,
            },
        }
        if "Session" in data1:
            respond_body["Session"] = data1["Session"]

        r2 = client.post(
            endpoint,
            headers={**headers, "X-Amz-Target": "AWSCognitoIdentityProviderService.RespondToAuthChallenge"},
            json=respond_body,
        )

        if r2.status_code != 200:
            return CognitoSRPResult(
                success=False,
                error=f"RespondToAuthChallenge {r2.status_code}: {r2.text[:300]}",
                raw=r2.json() if r2.text else None,
            )

        data2 = r2.json()
        auth = data2.get("AuthenticationResult")
        if not auth:
            return CognitoSRPResult(
                success=False,
                error=f"No AuthenticationResult: {data2}",
                raw=data2,
            )

        return CognitoSRPResult(
            success=True,
            id_token=auth.get("IdToken", ""),
            access_token=auth.get("AccessToken", ""),
            refresh_token=auth.get("RefreshToken", ""),
            raw=data2,
        )

    except Exception as exc:
        return CognitoSRPResult(
            success=False,
            error=f"{type(exc).__name__}: {exc}",
        )
    finally:
        client.close()


def cognito_srp_login(
    username: str,
    password: str,
    client_id: str,
    user_pool_id: str,
    region: str = "eu-central-1",
) -> dict[str, Any]:
    """Executor tool wrapper — 모델이 호출하는 도구 진입점"""
    result = authenticate_srp(username, password, client_id, user_pool_id, region)
    return {
        "success": result.success,
        "tokens": {
            "id_token": result.id_token,
            "access_token": result.access_token,
            "refresh_token": result.refresh_token,
        } if result.success else {},
        "error": result.error,
    }
