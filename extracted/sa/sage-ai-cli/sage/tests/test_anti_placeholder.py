"""Tests for the anti-placeholder content validator.

The user reported sage emitting stub functions: empty bodies, TODO
comments, return values that don't reflect any real logic. This test
file pins the contract that the content validator rejects these
patterns BEFORE they hit the user's filesystem.
"""

from __future__ import annotations

import pytest


class TestPythonPlaceholderRejection:

    def test_pass_only_function_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
def get_user(user_id):
    """Get a user."""
    pass
'''
        r = validate_content("src/users.py", bad)
        assert not r.ok
        assert "placeholder" in r.reason.lower() or "stub" in r.reason.lower()

    def test_ellipsis_body_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
def process(data):
    ...
'''
        r = validate_content("src/x.py", bad)
        assert not r.ok

    def test_only_todo_comment_body_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
def authenticate(token):
    # TODO: implement this
    return None
'''
        r = validate_content("src/auth.py", bad)
        assert not r.ok

    def test_raise_not_implemented_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
def parse_input(raw):
    raise NotImplementedError("implement parse_input")
'''
        r = validate_content("src/x.py", bad)
        assert not r.ok

    def test_real_implementation_passes(self):
        from sage.core.content_validator import validate_content
        good = '''
def get_user(user_id: str) -> dict:
    """Look up a user by ID."""
    if not user_id:
        raise ValueError("user_id required")
    return _users_db[user_id]
'''
        r = validate_content("src/users.py", good)
        assert r.ok, f"expected valid, got: {r.reason}"

    def test_abstract_method_in_class_body_is_allowed(self):
        """Abstract methods like `@abstractmethod def foo(): ...` are
        legitimate even though they have only an ellipsis body — they
        define an interface for subclasses."""
        from sage.core.content_validator import validate_content
        good = '''
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def find(self, id: str) -> dict:
        ...

    @abstractmethod
    def save(self, entity: dict) -> None:
        ...
'''
        r = validate_content("src/repo.py", good)
        assert r.ok, f"abstract methods should be allowed: {r.reason}"


class TestJavaScriptPlaceholderRejection:

    def test_empty_function_body_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
export function handler(req, res) {}
'''
        r = validate_content("src/handler.js", bad)
        assert not r.ok

    def test_only_todo_comment_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
export function authenticate(token) {
  // TODO: implement
  return null;
}
'''
        r = validate_content("src/auth.js", bad)
        assert not r.ok

    def test_real_jsx_passes(self):
        from sage.core.content_validator import validate_content
        good = '''
import { useState } from 'react';

export default function Counter() {
  const [n, setN] = useState(0);
  return (
    <button onClick={() => setN(n + 1)}>
      {n}
    </button>
  );
}
'''
        r = validate_content("src/Counter.jsx", good)
        assert r.ok, f"expected valid JSX: {r.reason}"


class TestRustPlaceholderRejection:

    def test_todo_macro_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
pub fn parse_config(raw: &str) -> Config {
    todo!("implement parsing")
}
'''
        r = validate_content("src/config.rs", bad)
        assert not r.ok

    def test_unimplemented_macro_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
pub fn run() {
    unimplemented!()
}
'''
        r = validate_content("src/main.rs", bad)
        assert not r.ok


class TestGoPlaceholderRejection:

    def test_panic_todo_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
package main

func parseConfig(raw string) Config {
    panic("TODO: implement")
}
'''
        r = validate_content("src/config.go", bad)
        assert not r.ok

    def test_real_go_passes(self):
        from sage.core.content_validator import validate_content
        good = '''
package main

import "fmt"

func parseConfig(raw string) (Config, error) {
    if raw == "" {
        return Config{}, fmt.Errorf("empty input")
    }
    return Config{Raw: raw}, nil
}
'''
        r = validate_content("src/config.go", good)
        assert r.ok, f"expected valid Go: {r.reason}"


class TestJavaPlaceholderRejection:

    def test_throw_unsupported_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
public class UserService {
    public User findUser(String id) {
        throw new UnsupportedOperationException("not implemented");
    }
}
'''
        r = validate_content("src/UserService.java", bad)
        assert not r.ok

    def test_todo_comment_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
public class A {
    // TODO: implement
    public void foo() {}
}
'''
        r = validate_content("src/A.java", bad)
        assert not r.ok


class TestCSharpPlaceholderRejection:

    def test_throw_notimplemented_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
public class UserService {
    public User FindUser(string id) {
        throw new NotImplementedException();
    }
}
'''
        r = validate_content("src/UserService.cs", bad)
        assert not r.ok


class TestRubyPlaceholderRejection:

    def test_raise_notimplemented_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
class UserService
  def find_user(id)
    raise NotImplementedError, "implement me"
  end
end
'''
        r = validate_content("src/user_service.rb", bad)
        assert not r.ok


class TestPHPPlaceholderRejection:

    def test_throw_notimplemented_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
<?php

class UserService {
    public function findUser(string $id): User {
        throw new \\Exception("Not implemented");
    }
}
'''
        r = validate_content("src/UserService.php", bad)
        assert not r.ok


class TestSwiftPlaceholderRejection:

    def test_fatalerror_is_rejected(self):
        from sage.core.content_validator import validate_content
        bad = '''
import Foundation

struct UserService {
    func findUser(_ id: String) -> User {
        fatalError("not implemented")
    }
}
'''
        r = validate_content("src/UserService.swift", bad)
        assert not r.ok


class TestRuntimeRejection:
    """Verifies the validator is wired into pre_validate_content so
    sage's FILE: handler actually blocks placeholder writes."""

    def test_pre_validate_rejects_placeholder(self):
        from sage.core.validation import pre_validate_content
        bad = '''
def handle(req):
    pass
'''
        ok, err = pre_validate_content("src/handler.py", bad)
        assert ok is False
        assert err  # has a message
        # The error should explain WHY
        assert "placeholder" in err.lower() or "stub" in err.lower()

    def test_pre_validate_accepts_real_code(self):
        from sage.core.validation import pre_validate_content
        good = '''
def handle(req):
    if not req:
        raise ValueError("empty request")
    return {"ok": True, "echo": req}
'''
        ok, err = pre_validate_content("src/handler.py", good)
        assert ok is True, f"got rejection: {err}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
