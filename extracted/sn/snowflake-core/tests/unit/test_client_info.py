import json
import warnings

from unittest.mock import PropertyMock, patch

from snowflake.core._internal.client_info import ClientInfo


@patch("snowflake.core._internal.client_info.ClientInfo.client_version", new_callable=PropertyMock)
def test_client_info(mock_client_version, fake_root):
    mock_client_version.return_value = "1.0.0"

    # Test Case 1: PyCore entry is missing from client_support_version_info
    # It only has entries for other clients.
    fake_root._query_for_client_info.return_value = json.loads("""
    [
      {
        "clientId": "DOTNETDriver",
        "clientAppId": ".NET",
        "minimumSupportedVersion": "2.0.15",
        "minimumNearingEndOfSupportVersion": "2.0.17",
        "recommendedVersion": "4.1.0",
        "deprecatedVersions": [],
        "_customSupportedVersions_": []
    },
    {
        "clientId": "GO",
        "clientAppId": "Go",
        "minimumSupportedVersion": "1.6.12",
        "minimumNearingEndOfSupportVersion": "1.6.14",
        "recommendedVersion": "1.11.1",
        "deprecatedVersions": [],
        "_customSupportedVersions_": ["1.1.5"]
    }
  ]""")

    fake_root._initialize_client_info()

    # In this case, if an entry for PyCore isn't there, the
    # ClientInfo should be conservative and always say that the current
    # version is supported.
    client_info = fake_root._client_info

    assert client_info.client_version == "1.0.0"
    assert client_info.version_is_supported()
    assert not client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version is None
    assert client_info.end_of_support_version is None
    assert client_info.recommended_version is None

    # Test Case 2: PyCore entry is present in client_support_version_info,
    # PyCore and the current version is newer than the recommended version
    fake_root._query_for_client_info.return_value = json.loads("""
    [
      {
        "clientId": "DOTNETDriver",
        "clientAppId": ".NET",
        "minimumSupportedVersion": "2.0.15",
        "minimumNearingEndOfSupportVersion": "2.0.17",
        "recommendedVersion": "4.1.0",
        "deprecatedVersions": [],
        "_customSupportedVersions_": []
    },
    {
        "clientId": "PyCore",
        "clientAppId": "PyCore",
        "minimumSupportedVersion": "0.7.0",
        "minimumNearingEndOfSupportVersion": "0.8.0",
        "recommendedVersion": "0.9.0",
        "deprecatedVersions": [],
        "_customSupportedVersions_": ["1.1.5"]
    }
  ]""")

    fake_root._initialize_client_info()
    client_info = fake_root._client_info

    # Information is present and the current version is supported
    assert client_info.client_version == "1.0.0"
    assert client_info.version_is_supported()
    assert not client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version == "0.7.0"
    assert client_info.end_of_support_version == "0.8.0"
    assert client_info.recommended_version == "0.9.0"

    # Test Case 3: PyCore entry is present in client_support_version_info,
    # but the current version is too old.
    fake_root._query_for_client_info.return_value = json.loads("""
       [
       {
           "clientId": "PyCore",
           "clientAppId": "PyCore",
           "minimumSupportedVersion": "1.7.0",
           "minimumNearingEndOfSupportVersion": "1.8.0",
           "recommendedVersion": "1.9.0",
           "deprecatedVersions": [],
           "_customSupportedVersions_": ["1.1.5"]
       }
     ]""")

    # Verify that the unsupported warning is triggered
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        # This should trigger a warning.
        fake_root._initialize_client_info()
        assert len(w) == 1
        assert "not supported" in str(w[-1].message)

    client_info = fake_root._client_info

    # This version is not supported, which means it is also nearing end of support.
    assert client_info.client_version == "1.0.0"
    assert not client_info.version_is_supported()
    assert client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version == "1.7.0"
    assert client_info.end_of_support_version == "1.8.0"
    assert client_info.recommended_version == "1.9.0"

    # Test Case 4: PyCore entry is present in client_support_version_info,
    # but the current version is lower than the nearing-end-of-support version.
    fake_root._query_for_client_info.return_value = json.loads("""
          [
          {
              "clientId": "PyCore",
              "clientAppId": "PyCore",
              "minimumSupportedVersion": "0.7.0",
              "minimumNearingEndOfSupportVersion": "1.8.0",
              "recommendedVersion": "1.9.0",
              "deprecatedVersions": [],
              "_customSupportedVersions_": ["1.1.5"]
          }
        ]""")

    # Verify that the nearing-end-of-life warning is triggered
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        # This should trigger a warning.
        fake_root._initialize_client_info()
        assert len(w) == 1
        assert "nearing the end of support" in str(w[-1].message)

    client_info = fake_root._client_info

    # This version is not supported, but it is nearing the end of support.
    assert client_info.client_version == "1.0.0"
    assert client_info.version_is_supported()
    assert client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version == "0.7.0"
    assert client_info.end_of_support_version == "1.8.0"
    assert client_info.recommended_version == "1.9.0"

    # Test Case 5: No client support info is returned from the server
    # Things should default to being supported.
    fake_root._query_for_client_info.return_value = json.loads("""
    [
    ]""")

    fake_root._initialize_client_info()

    # In this case, ClientInfo should be conservative and always say that the current
    # version is supported.
    client_info = fake_root._client_info

    # Test the case where the client support version info for PyCore is not available;
    # In this case, ClientInfo should be conservative and always say that the current
    # version is supported.
    assert client_info.client_version == "1.0.0"
    assert client_info.version_is_supported()
    assert not client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version is None
    assert client_info.end_of_support_version is None
    assert client_info.recommended_version is None

    # Test Case 6: PyCore entry is present in client_support_version_info,
    # but is incomplete (missing required fields).
    fake_root._query_for_client_info.return_value = json.loads("""
       [
       {
           "clientId": "PyCore",
           "clientAppId": "PyCore",
           "minimumSupportedVersion": "0.7.0",
           "deprecatedVersions": [],
           "_customSupportedVersions_": ["1.1.5"]
       }
     ]""")

    fake_root._initialize_client_info()
    client_info = fake_root._client_info

    # Since fields are missing, we should fall back to assuming the client is supported.
    assert client_info.client_version == "1.0.0"
    assert client_info.version_is_supported()
    assert not client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version is None
    assert client_info.end_of_support_version is None
    assert client_info.recommended_version is None

    # Test Case 7: PyCore entry is present in client_support_version_info,
    # but has poorly formatted version numbers.
    fake_root._query_for_client_info.return_value = json.loads("""
      [
      {
          "clientId": "PyCore",
          "clientAppId": "PyCore",
          "minimumSupportedVersion": "0.7.0-dev",
          "minimumNearingEndOfSupportVersion": "0.f.0",
          "recommendedVersion": "0.9..0",
          "deprecatedVersions": [],
          "_customSupportedVersions_": ["1.1.5"]
      }
    ]""")

    fake_root._initialize_client_info()
    client_info = fake_root._client_info

    # Since fields are poorly formatted, we should fall back to assuming the client is supported.
    assert client_info.client_version == "1.0.0"
    assert client_info.version_is_supported()
    assert not client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version is None
    assert client_info.end_of_support_version is None
    assert client_info.recommended_version is None

    # Test Case 8: Test for None as ClientInfo
    client_info = ClientInfo(None)

    # Since fields are poorly formatted, we should fall back to assuming the client is supported.
    assert client_info.client_version == "1.0.0"
    assert client_info.version_is_supported()
    assert not client_info.version_is_nearing_end_of_support()

    assert client_info.minimum_supported_version is None
    assert client_info.end_of_support_version is None
    assert client_info.recommended_version is None
