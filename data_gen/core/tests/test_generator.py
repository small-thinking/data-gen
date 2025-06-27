"""
Test the DataGenerator class.
Run the tests with:
    uv run pytest data_gen/core/tests/test_generator.py
"""

import pytest
from typing import List, Dict, Any
from ..generator import DataGenerator
from ..llm_requester import LLMRequester


class MockLLMRequester(LLMRequester):
    def request(self, prompt: str) -> str:
        # Return a simple JSON string for testing
        return '{"mock_key": "mock_value", "prompt": "%s"}' % prompt


class MockBatchLLMRequester(LLMRequester):
    def request_batch(self, input_file_path: str) -> str:
        return "mock_batch_id"


class TestDataGenerator(DataGenerator):
    def generate_broad_topics(self, requirement: str, num_topics: int) -> List[str]:
        return [f"Topic {i+1}" for i in range(num_topics)]

    def generate_requests_for_topic(self, topic: str, num_requests: int) -> List[str]:
        return [f"Request {i+1} for {topic}" for i in range(num_requests)]

    def generate_prompt_for_request(self, request: str) -> str:
        return f"Prompt for {request}"

    def parse_llm_response(self, response: str) -> Dict[str, Any]:
        # For testing, just parse the mock JSON string
        import json
        return json.loads(response)


@pytest.fixture
def generator():
    llm_requester = MockLLMRequester()
    return TestDataGenerator(llm_requester)


def test_generate_data_process(generator):
    requirement = "Generate synthetic data for users"
    num_topics = 2
    num_requests_per_topic = 3
    data = generator.generate_data(requirement, num_topics, num_requests_per_topic)
    assert len(data) == num_topics * num_requests_per_topic
    for record in data:
        assert isinstance(record, dict)
        assert "mock_key" in record
        assert "prompt" in record


def test_generate_broad_topics(generator):
    topics = generator.generate_broad_topics("req", 2)
    assert topics == ["Topic 1", "Topic 2"]


def test_generate_requests_for_topic(generator):
    requests = generator.generate_requests_for_topic("Topic 1", 2)
    assert requests == ["Request 1 for Topic 1", "Request 2 for Topic 1"]


def test_generate_prompt_for_request(generator):
    prompt = generator.generate_prompt_for_request("Request 1")
    assert prompt == "Prompt for Request 1"


def test_parse_llm_response(generator):
    response = '{"mock_key": "mock_value", "prompt": "Prompt for test"}'
    parsed = generator.parse_llm_response(response)
    assert parsed["mock_key"] == "mock_value"
    assert parsed["prompt"] == "Prompt for test"