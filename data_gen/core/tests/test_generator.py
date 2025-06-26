# Pytest style tests. Max line length: 120 (see .flake8, .pylintrc, pyproject.toml)
import pytest
from typing import List, Dict, Any

from ..generator import DataGenerator


class TestDataGenerator(DataGenerator):
    """Concrete implementation of DataGenerator for testing."""
    def generate_data(self, requirement: str, num_records: int) -> List[Dict[str, Any]]:
        return [{"test": f"record_{i}"} for i in range(num_records)]


@pytest.fixture
def generator():
    return TestDataGenerator()


def test_initialization_with_api_key():
    api_key = "test_api_key"
    generator = TestDataGenerator(api_key=api_key)
    assert generator.api_key == api_key


def test_initialization_without_api_key():
    generator = TestDataGenerator()
    assert generator.api_key is None


def test_convert_requirement_to_prompts_basic(generator):
    requirement = "Generate user profiles"
    num_records = 3
    prompts = generator._convert_requirement_to_prompts(requirement, num_records)
    assert len(prompts) == num_records
    assert requirement in prompts[0]
    assert "JSON" in prompts[0]
    assert "synthetic data" in prompts[0]


def test_convert_requirement_to_prompts_variation(generator):
    requirement = "Generate product data"
    num_records = 5
    prompts = generator._convert_requirement_to_prompts(requirement, num_records)
    assert "record #" not in prompts[0]
    for i in range(1, num_records):
        assert f"record #{i+1}" in prompts[i]
        assert "distinct" in prompts[i]


def test_convert_requirement_to_prompts_single_record(generator):
    requirement = "Generate a single user"
    num_records = 1
    prompts = generator._convert_requirement_to_prompts(requirement, num_records)
    assert len(prompts) == 1
    assert "record #" not in prompts[0]


def test_convert_requirement_to_prompts_empty_requirement(generator):
    requirement = ""
    num_records = 2
    prompts = generator._convert_requirement_to_prompts(requirement, num_records)
    assert len(prompts) == num_records
    assert "JSON" in prompts[0]


def test_convert_requirement_to_prompts_zero_records(generator):
    requirement = "Generate data"
    num_records = 0
    prompts = generator._convert_requirement_to_prompts(requirement, num_records)
    assert len(prompts) == 0


def test_generate_data_abstract_method(generator):
    requirement = "Generate test data"
    num_records = 3
    result = generator.generate_data(requirement, num_records)
    assert len(result) == num_records
    assert isinstance(result, list)
    assert isinstance(result[0], dict)