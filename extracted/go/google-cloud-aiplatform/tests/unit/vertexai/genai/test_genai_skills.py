# //third_party/py/google/cloud/aiplatform/tests/unit/vertexai/genai/test_genai_skills.py
import json
from unittest import mock
import google.auth.credentials
from vertexai import _genai as genai
from vertexai._genai import client as vertexai_client
from google.genai import types as genai_types
import pytest


@pytest.fixture
def skills_client():
    creds = mock.create_autospec(google.auth.credentials.Credentials, instance=True)
    creds.token = "test_token"
    client = vertexai_client.Client(
        project="test-project", location="test-location", credentials=creds
    )
    return client.skills


@pytest.fixture
def async_skills_client():
    creds = mock.create_autospec(google.auth.credentials.Credentials, instance=True)
    creds.token = "test_token"
    client = vertexai_client.Client(
        project="test-project", location="test-location", credentials=creds
    )
    return client.aio.skills


class TestGenaiSkills:
    mock_get_skill_response = {
        "name": "projects/test-project/locations/test-location/skills/test-skill",
        "displayName": "My Test Skill",
    }

    def test_get_skill(self, skills_client):
        with mock.patch.object(
            skills_client._api_client, "request", autospec=True
        ) as request_mock:
            request_mock.return_value = genai_types.HttpResponse(
                body=json.dumps(self.mock_get_skill_response)
            )
            skill_name = (
                "projects/test-project/locations/test-location/skills/test-skill"
            )
            skill = skills_client.get(name=skill_name)
            request_mock.assert_called_once_with(
                "get",
                skill_name,
                {"_url": {"name": skill_name}},
                None,
            )
            assert isinstance(skill, genai.types.Skill)
            assert skill.name == skill_name
            assert skill.display_name == "My Test Skill"

    def test_retrieve_skills_response(self, skills_client):
        mock_retrieve_response = {
            "retrievedSkills": [
                {
                    "skillName": (
                        "projects/test-project/locations/test-location/skills/skill-1"
                    ),
                    "description": "Skill 1 Description",
                },
                {
                    "skillName": (
                        "projects/test-project/locations/test-location/skills/skill-2"
                    ),
                    "description": "Skill 2 Description",
                },
            ]
        }

        with mock.patch.object(
            skills_client._api_client, "request", autospec=True
        ) as request_mock:
            request_mock.return_value = genai_types.HttpResponse(
                body=json.dumps(mock_retrieve_response)
            )

            response = skills_client.retrieve(query="test query", config={"top_k": 5})

            assert isinstance(response, genai.types.RetrieveSkillsResponse)
            assert len(response.retrieved_skills) == 2
            assert response.retrieved_skills[0].skill_name == (
                "projects/test-project/locations/test-location/skills/skill-1"
            )
            assert response.retrieved_skills[0].description == "Skill 1 Description"

    def test_retrieve_skills_request_params(self, skills_client):
        mock_retrieve_response = {"retrievedSkills": []}

        with mock.patch.object(
            skills_client._api_client, "request", autospec=True
        ) as request_mock:
            request_mock.return_value = genai_types.HttpResponse(
                body=json.dumps(mock_retrieve_response)
            )

            skills_client.retrieve(query="test query", config={"top_k": 5})

            request_mock.assert_called_once_with(
                "get",
                "skills:retrieve?query=test+query&topK=5",
                {"_query": {"query": "test query", "topK": 5}},
                None,
            )

    @pytest.mark.asyncio
    async def test_retrieve_skills_async(self, async_skills_client):
        mock_retrieve_response = {
            "retrievedSkills": [
                {
                    "skillName": (
                        "projects/test-project/locations/test-location/skills/skill-1"
                    ),
                    "description": "Skill 1 Description",
                }
            ]
        }

        with mock.patch.object(
            async_skills_client._api_client, "async_request", autospec=True
        ) as request_mock:
            request_mock.return_value = genai_types.HttpResponse(
                body=json.dumps(mock_retrieve_response)
            )

            response = await async_skills_client.retrieve(
                query="test query", config={"top_k": 1}
            )

            assert isinstance(response, genai.types.RetrieveSkillsResponse)
            assert len(response.retrieved_skills) == 1
            assert response.retrieved_skills[0].skill_name == (
                "projects/test-project/locations/test-location/skills/skill-1"
            )

            request_mock.assert_called_once_with(
                "get",
                "skills:retrieve?query=test+query&topK=1",
                {"_query": {"query": "test query", "topK": 1}},
                None,
            )
