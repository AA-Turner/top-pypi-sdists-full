"""Tests for the deep-merge resolution algorithm."""

from smplkit._resolver import deep_merge, resolve


# ---------------------------------------------------------------
# deep_merge
# ---------------------------------------------------------------


class TestDeepMerge:
    def test_disjoint_keys(self):
        assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_override_scalar(self):
        assert deep_merge({"a": 1}, {"a": 2}) == {"a": 2}

    def test_nested_dict_merge(self):
        base = {"db": {"host": "localhost", "port": 5432}}
        override = {"db": {"host": "prod.example.com"}}
        result = deep_merge(base, override)
        assert result == {"db": {"host": "prod.example.com", "port": 5432}}

    def test_deeply_nested_merge(self):
        base = {"a": {"b": {"c": 1, "d": 2}}}
        override = {"a": {"b": {"c": 99}}}
        result = deep_merge(base, override)
        assert result == {"a": {"b": {"c": 99, "d": 2}}}

    def test_array_replaced_not_merged(self):
        base = {"tags": ["a", "b"]}
        override = {"tags": ["x"]}
        assert deep_merge(base, override) == {"tags": ["x"]}

    def test_null_overrides_dict(self):
        base = {"config": {"key": "value"}}
        override = {"config": None}
        assert deep_merge(base, override) == {"config": None}

    def test_dict_overrides_scalar(self):
        base = {"key": "string_value"}
        override = {"key": {"nested": True}}
        assert deep_merge(base, override) == {"key": {"nested": True}}

    def test_empty_override(self):
        base = {"a": 1, "b": 2}
        assert deep_merge(base, {}) == {"a": 1, "b": 2}

    def test_empty_base(self):
        override = {"a": 1}
        assert deep_merge({}, override) == {"a": 1}

    def test_both_empty(self):
        assert deep_merge({}, {}) == {}

    def test_does_not_mutate_inputs(self):
        base = {"a": {"b": 1}}
        override = {"a": {"c": 2}}
        result = deep_merge(base, override)
        assert result == {"a": {"b": 1, "c": 2}}
        assert base == {"a": {"b": 1}}
        assert override == {"a": {"c": 2}}


# ---------------------------------------------------------------
# resolve
# ---------------------------------------------------------------


class TestResolve:
    def test_single_config_base_values_only(self):
        chain = [{"values": {"retries": 3, "timeout": 5000}, "environments": {}}]
        result = resolve(chain, "production")
        assert result == {"retries": 3, "timeout": 5000}

    def test_single_config_with_env_override(self):
        chain = [
            {
                "values": {"retries": 3, "timeout": 5000},
                "environments": {
                    "production": {"retries": 5},
                },
            }
        ]
        result = resolve(chain, "production")
        assert result == {"retries": 5, "timeout": 5000}

    def test_env_not_present_uses_base(self):
        chain = [
            {
                "values": {"retries": 3},
                "environments": {
                    "production": {"retries": 5},
                },
            }
        ]
        result = resolve(chain, "staging")
        assert result == {"retries": 3}

    def test_two_level_inheritance(self):
        """child → parent, child overrides parent."""
        parent = {
            "values": {"app_name": "Acme", "retries": 3},
            "environments": {},
        }
        child = {
            "values": {"retries": 10, "db_host": "localhost"},
            "environments": {},
        }
        # chain is child-first, parent-last
        chain = [child, parent]
        result = resolve(chain, "production")
        assert result == {
            "app_name": "Acme",
            "retries": 10,
            "db_host": "localhost",
        }

    def test_two_level_with_env_overrides(self):
        parent = {
            "values": {"retries": 3},
            "environments": {"production": {"retries": 5}},
        }
        child = {
            "values": {"db": "dev_db"},
            "environments": {"production": {"db": "prod_db"}},
        }
        chain = [child, parent]
        result = resolve(chain, "production")
        assert result == {"retries": 5, "db": "prod_db"}

    def test_three_level_inheritance(self):
        root = {
            "values": {"a": 1, "b": 2, "c": 3},
            "environments": {},
        }
        mid = {
            "values": {"b": 20},
            "environments": {},
        }
        leaf = {
            "values": {"c": 300},
            "environments": {},
        }
        chain = [leaf, mid, root]
        result = resolve(chain, "any")
        assert result == {"a": 1, "b": 20, "c": 300}

    def test_deep_merge_across_chain(self):
        """Nested dicts are deep-merged across inheritance chain."""
        parent = {
            "values": {
                "credentials": {
                    "provider": "oauth",
                    "client_id": "default",
                    "secret": "base_secret",
                }
            },
            "environments": {"production": {"credentials": {"secret": "prod_secret", "scopes": ["read", "write"]}}},
        }
        child = {
            "values": {},
            "environments": {"production": {"credentials": {"secret": "child_prod_secret"}}},
        }
        chain = [child, parent]
        result = resolve(chain, "production")
        expected = {
            "credentials": {
                "provider": "oauth",
                "client_id": "default",
                "secret": "child_prod_secret",
                "scopes": ["read", "write"],
            }
        }
        assert result == expected

    def test_empty_chain(self):
        assert resolve([], "production") == {}

    def test_none_values_and_environments(self):
        chain = [{"values": None, "environments": None}]
        assert resolve(chain, "production") == {}

    def test_showcase_scenario(self):
        """Validate the showcase's expected user_service production resolution."""
        common = {
            "values": {
                "app_name": "Acme SaaS Platform",
                "support_email": "support@acme.dev",
                "max_retries": 3,
                "request_timeout_ms": 5000,
                "pagination_default_page_size": 25,
                "credentials": {
                    "oauth_provider": "https://auth.acme.dev",
                    "client_id": "acme_default_client",
                    "client_secret": "default_secret",
                    "scopes": ["read"],
                },
                "feature_flags": {
                    "provider": "smplkit",
                    "endpoint": "https://flags.smplkit.com",
                    "refresh_interval_seconds": 30,
                },
            },
            "environments": {
                "production": {
                    "max_retries": 5,
                    "request_timeout_ms": 10000,
                    "credentials": {
                        "client_secret": "PROD_SECRET_FROM_VAULT",
                        "scopes": ["read", "write", "admin"],
                    },
                }
            },
        }
        user_service = {
            "values": {
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "users_dev",
                    "pool_size": 5,
                    "ssl_mode": "prefer",
                },
                "cache_ttl_seconds": 300,
                "enable_signup": True,
                "allowed_email_domains": ["acme.dev", "acme.com"],
                "pagination_default_page_size": 50,
            },
            "environments": {
                "production": {
                    "database": {
                        "host": "prod-users-rds.internal.acme.dev",
                        "name": "users_prod",
                        "pool_size": 20,
                        "ssl_mode": "require",
                    },
                    "cache_ttl_seconds": 600,
                    "credentials": {
                        "client_secret": "USER_SVC_PROD_SECRET",
                    },
                    "enable_signup": False,
                }
            },
        }

        chain = [user_service, common]
        result = resolve(chain, "production")

        # Verify key expected values from the showcase comments
        assert result["max_retries"] == 5
        assert result["request_timeout_ms"] == 10000
        assert result["cache_ttl_seconds"] == 600
        assert result["pagination_default_page_size"] == 50
        assert result["support_email"] == "support@acme.dev"
        assert result["app_name"] == "Acme SaaS Platform"
        assert result["enable_signup"] is False

        # Database should be deep-merged
        assert result["database"] == {
            "host": "prod-users-rds.internal.acme.dev",
            "port": 5432,
            "name": "users_prod",
            "pool_size": 20,
            "ssl_mode": "require",
        }

        # Credentials should be deep-merged across the full chain
        assert result["credentials"] == {
            "oauth_provider": "https://auth.acme.dev",
            "client_id": "acme_default_client",
            "client_secret": "USER_SVC_PROD_SECRET",
            "scopes": ["read", "write", "admin"],
        }
