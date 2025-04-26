from packaging.specifiers import SpecifierSet

from safety_schemas.models.specification import PythonSpecification


def test_python_specification():
    prerelease_version = "3.9.0b0"
    vulnerable_spec = SpecifierSet("<3.9.4")
    requirement_line = f"aiohttp=={prerelease_version}"

    print("Creating PythonSpecification instance...")
    spec = PythonSpecification(requirement_line, found=None)

    print("Calling is_vulnerable...")
    result = spec.is_vulnerable(vulnerable_spec, insecure_versions=[prerelease_version])
    print(f"Result: {result}")

    # Assert that the prerelease version is vulnerable
    assert result is True, "Expected to find vulnerability in aiohttp==3.9.0b0"

    # Now test with a non-vulnerable prerelease version
    safe_prerelease_version = "3.9.5b0"
    safe_requirement_line = f"aiohttp=={safe_prerelease_version}"

    print("Testing with a non-vulnerable prerelease version...")
    safe_spec = PythonSpecification(safe_requirement_line, found=None)
    safe_result = safe_spec.is_vulnerable(vulnerable_spec, insecure_versions=[safe_prerelease_version])
    print(f"Result: {safe_result}")

    # Assert that the non-vulnerable prerelease version is not flagged as vulnerable
    assert safe_result is False, "Expected aiohttp==3.9.5b0 not to be considered vulnerable"

if __name__ == "__main__":
    test_python_specification()
    print("All tests passed!")
