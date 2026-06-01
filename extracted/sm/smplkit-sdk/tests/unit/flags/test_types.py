"""Tests for Context and Rule public types."""

import pytest

from smplkit.flags.types import Context, Rule


class TestContext:
    def test_kwargs_only(self):
        ctx = Context("user", "u-1", plan="enterprise", beta=True)
        assert ctx.type == "user"
        assert ctx.key == "u-1"
        assert ctx.attributes == {"plan": "enterprise", "beta": True}

    def test_dict_only(self):
        ctx = Context("account", "a-1", {"region": "us", "size": 100})
        assert ctx.type == "account"
        assert ctx.key == "a-1"
        assert ctx.attributes == {"region": "us", "size": 100}

    def test_mixed_dict_and_kwargs(self):
        ctx = Context("user", "u-1", {"plan": "free"}, plan="enterprise", extra="val")
        assert ctx.attributes["plan"] == "enterprise"  # kwargs win
        assert ctx.attributes["extra"] == "val"

    def test_no_attributes(self):
        ctx = Context("device", "d-1")
        assert ctx.attributes == {}

    def test_none_attributes(self):
        ctx = Context("device", "d-1", None)
        assert ctx.attributes == {}

    def test_name_keyword_only(self):
        ctx = Context("user", "u-1", name="Alice Smith", plan="enterprise")
        assert ctx.name == "Alice Smith"
        assert ctx.attributes == {"plan": "enterprise"}

    def test_name_defaults_to_none(self):
        ctx = Context("user", "u-1")
        assert ctx.name is None

    def test_repr(self):
        ctx = Context("user", "u-1", name="Alice", plan="enterprise")
        r = repr(ctx)
        assert "user" in r
        assert "u-1" in r
        assert "Alice" in r

    def test_int_key_raises_typeerror(self):
        with pytest.raises(TypeError, match="Context key must be a string"):
            Context("account", 1234)

    def test_int_type_raises_typeerror(self):
        with pytest.raises(TypeError, match="Context type must be a string"):
            Context(42, "key")  # type: ignore[arg-type]

    def test_setattr_unknown_field_blocked(self):
        ctx = Context("user", "u-1")
        with pytest.raises(AttributeError, match=r"ctx\.attributes\['plan'\]"):
            ctx.plan = "pro"  # type: ignore[attr-defined]

    def test_setattr_known_fields_still_work(self):
        ctx = Context("user", "u-1")
        ctx.name = "Alice"
        ctx.attributes = {"region": "us"}
        assert ctx.name == "Alice"
        assert ctx.attributes == {"region": "us"}

    def test_id_property(self):
        assert Context("user", "123").id == "user:123"

    def test_type_returns_slug_not_jsonapi_resource_type(self):
        # ctx.type is the context-type slug ("user"), not the JSON:API
        # resource type ("context") that lives on the wire.
        assert Context("user", "u-1").type == "user"
        assert Context("account", "acme").type == "account"

    def test_id_assignment_blocked(self):
        ctx = Context("user", "u-1")
        with pytest.raises(AttributeError):
            ctx.id = "other:x"  # type: ignore[misc]

    def test_type_key_mutable_pre_save(self):
        ctx = Context("user", "u-1")
        ctx.type = "account"
        ctx.key = "acme"
        assert ctx.id == "account:acme"

    def test_type_key_immutable_post_save(self):
        ctx = Context("user", "u-1", created_at="2026-01-01")
        with pytest.raises(AttributeError, match="persisted Context"):
            ctx.type = "account"
        with pytest.raises(AttributeError, match="persisted Context"):
            ctx.key = "x"


class TestRule:
    def test_single_when(self):
        result = Rule("test rule", environment="staging").when("user.plan", "==", "enterprise").serve(True)
        assert result == {
            "description": "test rule",
            "logic": {"==": [{"var": "user.plan"}, "enterprise"]},
            "value": True,
            "environment": "staging",
        }

    def test_multiple_when_and(self):
        result = (
            Rule("two conditions", environment="staging")
            .when("user.plan", "==", "enterprise")
            .when("account.region", "==", "us")
            .serve(True)
        )
        assert result["logic"] == {
            "and": [
                {"==": [{"var": "user.plan"}, "enterprise"]},
                {"==": [{"var": "account.region"}, "us"]},
            ]
        }

    def test_environment_carried_through(self):
        result = Rule("env rule", environment="staging").when("x", "==", 1).serve("yes")
        assert result["environment"] == "staging"
        assert result["description"] == "env rule"
        assert result["value"] == "yes"

    def test_environment_required(self):
        import pytest

        with pytest.raises(TypeError):
            Rule("missing env")  # type: ignore[call-arg]

    def test_operators(self):
        ops = ["==", "!=", ">", "<", ">=", "<=", "in"]
        for op in ops:
            result = Rule("op test", environment="staging").when("x", op, 42).serve(True)
            assert op in result["logic"]

    def test_contains_operator(self):
        result = Rule("contains", environment="staging").when("user.email", "contains", "@acme.com").serve(True)
        assert result["logic"] == {"in": ["@acme.com", {"var": "user.email"}]}

    def test_no_conditions(self):
        result = Rule("empty", environment="staging").serve("val")
        assert result["logic"] == {}

    def test_numeric_value(self):
        result = Rule("num", environment="staging").when("x", ">", 100).serve(5)
        assert result["value"] == 5

    def test_json_value(self):
        val = {"mode": "dark", "accent": "#000"}
        result = Rule("json", environment="staging").when("x", "==", "y").serve(val)
        assert result["value"] == val

    def test_when_raw_jsonlogic_dict(self):
        """The 1-arg form passes a raw JSON Logic expression through as-is."""
        expr = {"or": [{"==": [{"var": "user.plan"}, "enterprise"]}, {"==": [{"var": "user.beta"}, True]}]}
        result = Rule("or rule", environment="staging").when(expr).serve(True)
        assert result["logic"] == expr

    def test_when_mixes_raw_and_convenience(self):
        """A raw expression and a convenience call are AND'd together."""
        expr = {"or": [{"==": [{"var": "a"}, 1]}, {"==": [{"var": "a"}, 2]}]}
        result = Rule("mixed", environment="staging").when(expr).when("b", "==", 3).serve(True)
        assert result["logic"] == {
            "and": [
                expr,
                {"==": [{"var": "b"}, 3]},
            ]
        }

    def test_when_invalid_args_raises(self):
        """Two-arg or four-arg forms aren't supported."""
        import pytest

        with pytest.raises(TypeError, match="when"):
            Rule("bad", environment="staging").when("just-one-arg")
        with pytest.raises(TypeError, match="when"):
            Rule("bad", environment="staging").when("a", "b")
