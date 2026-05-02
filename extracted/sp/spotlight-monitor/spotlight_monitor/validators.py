"""
Spotlight Validators

Define custom business logic validators that run on responses.
"""
import re
import time
from typing import Callable, Optional, Tuple, Dict, Any, List
from .models import ValidationResult


class ValidatorRegistry:
    """Registry of validators for a service."""

    def __init__(self):
        self._validators: List[Dict[str, Any]] = []

    def add(
        self,
        name: str,
        func: Callable[[dict, dict], Tuple[bool, Optional[str]]],
        endpoint_pattern: Optional[str] = None,
        methods: Optional[List[str]] = None,
    ):
        """
        Register a validator.

        Args:
            name: Unique name for this validator
            func: Function that takes (request_data, response_data) and returns (passed, failure_reason)
            endpoint_pattern: Regex or glob pattern to match endpoints (e.g., "/pills/*" or "/pills/.*")
            methods: HTTP methods to match (e.g., ["GET", "POST"]), None means all
        """
        # Convert glob-style patterns to regex
        if endpoint_pattern:
            # Replace * with .* for glob-style matching
            regex_pattern = endpoint_pattern.replace("*", ".*")
            if not regex_pattern.startswith("^"):
                regex_pattern = "^" + regex_pattern
            if not regex_pattern.endswith("$"):
                regex_pattern = regex_pattern + "$"
        else:
            regex_pattern = None

        self._validators.append({
            "name": name,
            "func": func,
            "endpoint_pattern": regex_pattern,
            "methods": [m.upper() for m in methods] if methods else None,
        })

    def get_validators_for(self, endpoint: str, method: str) -> List[Dict[str, Any]]:
        """Get all validators that match this endpoint and method."""
        matching = []
        for v in self._validators:
            # Check method
            if v["methods"] and method.upper() not in v["methods"]:
                continue
            
            # Check endpoint pattern
            if v["endpoint_pattern"]:
                if not re.match(v["endpoint_pattern"], endpoint):
                    continue
            
            matching.append(v)
        
        return matching

    def run_validators(
        self,
        endpoint: str,
        method: str,
        request_data: dict,
        response_data: dict,
    ) -> List[ValidationResult]:
        """Run all matching validators and return results."""
        results = []
        validators = self.get_validators_for(endpoint, method)

        for v in validators:
            start = time.perf_counter()
            try:
                passed, failure_reason = v["func"](request_data, response_data)
                execution_ms = int((time.perf_counter() - start) * 1000)
                results.append(ValidationResult(
                    name=v["name"],
                    passed=passed,
                    failure_reason=failure_reason if not passed else None,
                    execution_ms=execution_ms,
                ))
            except Exception as e:
                execution_ms = int((time.perf_counter() - start) * 1000)
                results.append(ValidationResult(
                    name=v["name"],
                    passed=False,
                    failure_reason=f"Validator error: {str(e)}",
                    execution_ms=execution_ms,
                ))

        return results


def validator(
    registry: ValidatorRegistry,
    name: Optional[str] = None,
    endpoint: Optional[str] = None,
    methods: Optional[List[str]] = None,
):
    """
    Decorator to register a validator function.

    Usage:
        @validator(spotlight.validators, name="pill_check", endpoint="/pills/*")
        def check_pills(request, response):
            if not response.get("pills"):
                return False, "No pills returned"
            return True, None
    """
    def decorator(func: Callable):
        validator_name = name or func.__name__
        registry.add(
            name=validator_name,
            func=func,
            endpoint_pattern=endpoint,
            methods=methods,
        )
        return func
    return decorator
