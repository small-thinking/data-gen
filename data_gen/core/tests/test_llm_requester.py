"""
Tests for LLMRequester and related utilities.
Run with:
    uv run pytest data_gen/core/tests/test_llm_requester.py
"""

from data_gen.core.llm_requester import LLMRequester, upload_file_to_openai


class MockLLMRequester(LLMRequester):
    def request(self, prompt: str) -> str:
        # Return a simple JSON string for testing
        return '{"mock_key": "mock_value", "prompt": "%s"}' % prompt


class MockBatchLLMRequester(LLMRequester):
    def request_batch(self, input_file_path: str) -> str:
        return "mock_batch_id"


def test_upload_file_to_openai(monkeypatch):
    """
    Test upload_file_to_openai to ensure it sends the correct request and parses the file ID.
    Uses monkeypatch to mock requests.post and avoid real API calls.
    """
    import requests

    class DummyResponse:
        def raise_for_status(self) -> None:
            pass
        def json(self) -> dict:
            return {"id": "file-1234"}

    def mock_post(url: str, headers: dict, files: dict, data: dict):
        assert url == "https://api.openai.com/v1/files"
        assert headers["Authorization"].startswith("Bearer ")
        assert data["purpose"] == "batch"
        assert "file" in files
        return DummyResponse()

    monkeypatch.setattr(requests, "post", mock_post)

    # Create a dummy file
    dummy_path = "dummy.jsonl"
    with open(dummy_path, "w") as f:
        f.write("{}\n")
    try:
        file_id = upload_file_to_openai(dummy_path, api_key="sk-test")
        assert file_id == "file-1234"
    finally:
        import os
        os.remove(dummy_path) 