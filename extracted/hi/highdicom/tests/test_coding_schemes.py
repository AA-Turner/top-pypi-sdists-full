import pytest

from pydicom.dataset import Dataset

from highdicom.enum import CodingSchemeURLTypeValues
from highdicom.coding_schemes import (
    CodingSchemeIdentificationItem,
    CodingSchemeResourceItem,
)


class TestCodingSchemeResourceItem:

    def test_construction(self):
        item = CodingSchemeResourceItem(
            url='https://example.com/scheme.owl',
            url_type=CodingSchemeURLTypeValues.OWL,
        )
        assert item.CodingSchemeURL == 'https://example.com/scheme.owl'
        assert item.CodingSchemeURLType == 'OWL'

    def test_url_type_string(self):
        item = CodingSchemeResourceItem(
            url='https://example.com/scheme.csv',
            url_type='CSV',
        )
        assert item.CodingSchemeURLType == 'CSV'

    def test_invalid_url_type(self):
        with pytest.raises(ValueError):
            CodingSchemeResourceItem(
                url='https://example.com',
                url_type='PDF',
            )


class TestCodingSchemeIdentificationItem:

    def test_designator_only(self):
        item = CodingSchemeIdentificationItem(designator='99TEST')
        assert item.CodingSchemeDesignator == '99TEST'
        for keyword in (
            'CodingSchemeName',
            'CodingSchemeVersion',
            'CodingSchemeRegistry',
            'CodingSchemeUID',
            'CodingSchemeExternalID',
            'CodingSchemeResponsibleOrganization',
            'CodingSchemeResourcesSequence',
        ):
            assert keyword not in item

    def test_optional_attributes(self):
        item = CodingSchemeIdentificationItem(
            designator='99TEST',
            name='Test Scheme',
            version='1.0',
            responsible_organization='Test Organization',
        )
        assert item.CodingSchemeDesignator == '99TEST'
        assert item.CodingSchemeName == 'Test Scheme'
        assert item.CodingSchemeVersion == '1.0'
        assert item.CodingSchemeResponsibleOrganization == 'Test Organization'
        assert 'CodingSchemeRegistry' not in item

    def test_registered_with_uid(self):
        item = CodingSchemeIdentificationItem(
            designator='SCT',
            registry='HL7',
            uid='2.16.840.1.113883.6.96',
        )
        assert item.CodingSchemeRegistry == 'HL7'
        assert item.CodingSchemeUID == '2.16.840.1.113883.6.96'
        assert 'CodingSchemeExternalID' not in item

    def test_registered_with_external_id(self):
        item = CodingSchemeIdentificationItem(
            designator='SCT',
            registry='HL7',
            external_id='SNOMED-CT',
        )
        assert item.CodingSchemeRegistry == 'HL7'
        assert item.CodingSchemeExternalID == 'SNOMED-CT'
        assert 'CodingSchemeUID' not in item

    def test_registered_without_uid_or_external_id(self):
        with pytest.raises(ValueError):
            CodingSchemeIdentificationItem(
                designator='SCT',
                registry='HL7',
            )

    def test_registered_with_uid_and_external_id(self):
        with pytest.raises(ValueError):
            CodingSchemeIdentificationItem(
                designator='SCT',
                registry='HL7',
                uid='2.16.840.1.113883.6.96',
                external_id='SNOMED-CT',
            )

    def test_resources(self):
        resources = [
            CodingSchemeResourceItem(
                'https://example.com/scheme.html',
                CodingSchemeURLTypeValues.DOC,
            ),
            CodingSchemeResourceItem(
                'https://example.com/scheme.owl',
                CodingSchemeURLTypeValues.OWL,
            ),
        ]
        item = CodingSchemeIdentificationItem(
            designator='99TEST',
            resources=resources,
        )
        assert len(item.CodingSchemeResourcesSequence) == 2
        assert item.CodingSchemeResourcesSequence[0].CodingSchemeURLType == (
            'DOC'
        )
        assert item.CodingSchemeResourcesSequence[1].CodingSchemeURL == (
            'https://example.com/scheme.owl'
        )

    def test_resources_wrong_type(self):
        with pytest.raises(TypeError):
            CodingSchemeIdentificationItem(
                designator='99TEST',
                resources=[Dataset()],  # type: ignore[list-item]
            )
