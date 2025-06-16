from datetime import datetime
from uuid import uuid4

import pytest
from datadoc_model.required.model import (
    DatadocMetadata,
    Dataset,
    LanguageStringType,
    LanguageStringTypeItem,
    MetadataContainer,
)
from pydantic import ValidationError


def test_instantiate_no_values_container():
    container = MetadataContainer()
    assert isinstance(container, MetadataContainer)


def test_instantiate_no_values_datadoc():
    with pytest.raises(ValidationError):
        DatadocMetadata()


def test_instantiate_all_required_values_datadoc():
    DatadocMetadata(
        dataset=Dataset(
            short_name="person_testdata",
            name=LanguageStringType(
                [
                    LanguageStringTypeItem(
                        languageCode="nb",
                        languageText="Person test data",
                    ),
                ],
            ),
            description=LanguageStringType(
                [
                    LanguageStringTypeItem(
                        languageCode="nb",
                        languageText="Person test data",
                    ),
                ],
            ),
            population_description=LanguageStringType(
                [
                    LanguageStringTypeItem(
                        languageCode="nb",
                        languageText="Person test data",
                    ),
                ],
            ),
            version="1",
            unit_type="20",
            subject_field="20",
            contains_personal_data=True,
            id=uuid4(),
            owner="team-metadata",
            file_path="path/to/dataset",
            metadata_created_by="mmw",
            metadata_created_date=datetime.now(),
            metadata_last_updated_by="mmw",
            metadata_last_updated_date=datetime.now(),
            assessment="PROTECTED",
            dataset_status="DRAFT",
            dataset_state="PROCESSED_DATA",
        ),
        variables=[],
    )


def test_unknown_field():
    with pytest.raises(ValidationError):
        DatadocMetadata(unknown_field="random_value")
