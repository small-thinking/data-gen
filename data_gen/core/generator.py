from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .llm_requester import LLMRequester


class DataGenerator(ABC):
    """Abstract base class for multi-step data generation using LLMRequester."""

    def __init__(self, llm_requester: LLMRequester):
        self.llm_requester = llm_requester

    def generate_data(self, requirement: str, num_topics: int, num_requests_per_topic: int) -> List[Dict[str, Any]]:
        """Main entry for the template pattern: orchestrates the data generation process.

        Args:
            requirement: Natural language description of data requirements
            num_topics: Number of broad topics to generate
            num_requests_per_topic: Number of requests/questions per topic
        Returns:
            List of generated data records
        """
        topics = self.generate_broad_topics(requirement, num_topics)
        all_data = []
        for topic in topics:
            requests = self.generate_requests_for_topic(topic, num_requests_per_topic)
            for req in requests:
                prompt = self.generate_prompt_for_request(req)
                response = self.llm_requester.request(prompt)
                data = self.parse_llm_response(response)
                all_data.append(data)
        return all_data

    @abstractmethod
    def generate_broad_topics(self, requirement: str, num_topics: int) -> List[str]:
        """Generate a list of broad topics from the requirement."""
        pass

    @abstractmethod
    def generate_requests_for_topic(self, topic: str, num_requests: int) -> List[str]:
        """Generate a list of requests/questions for a given topic."""
        pass

    @abstractmethod
    def generate_prompt_for_request(self, request: str) -> str:
        """Generate a prompt for the LLM based on the request/question."""
        pass

    @abstractmethod
    def parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into a data record."""
        pass