import requests
import time
from typing import Optional


class LLMRequester:
    """Abstract base class for LLM API requests."""
    def request(self, prompt: str) -> str:
        """
        Send a single prompt to the LLM and return the response.
        Override in subclasses if supported.
        """
        pass

    def request_batch(self, input_file_path: str) -> str:
        """
        Send a batch of prompts to the LLM using a file.
        Override in subclasses if supported.
        Args:
            input_file_path: Path to the file containing batch prompts (e.g., .jsonl)
        Returns:
            Batch job ID, status, or output file path (implementation dependent)
        """
        pass


class OpenAIRequester(LLMRequester):
    """Concrete implementation of LLMRequester for OpenAI API single requests."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def request(self, prompt: str) -> str:
        """Send a prompt to the OpenAI API and return the response as a string."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]


class OpenAIBatchRequester(LLMRequester):
    """Concrete implementation of LLMRequester for OpenAI API batch requests."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.files_url = "https://api.openai.com/v1/files"
        self.batches_url = "https://api.openai.com/v1/batches"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def _upload_file(self, file_path: str) -> str:
        """Upload a .jsonl file to OpenAI and return the file ID."""
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/jsonl")}
            data = {"purpose": "batch"}
            response = requests.post(self.files_url, headers=self.headers, files=files, data=data)
            response.raise_for_status()
            return response.json()["id"]

    def _create_batch(self, input_file_id: str) -> str:
        """Create a batch job and return the batch ID."""
        data = {
            "input_file_id": input_file_id,
            "endpoint": "/v1/chat/completions",
            "completion_window": "24h"
        }
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        response = requests.post(self.batches_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["id"]

    def _poll_batch_status(self, batch_id: str, poll_interval: int = 10, timeout: int = 3600) -> dict:
        """Poll the batch status until completed or failed. Returns the final batch object."""
        url = f"{self.batches_url}/{batch_id}"
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        start_time = time.time()
        while True:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            batch_obj = response.json()
            status = batch_obj.get("status")
            if status in ("completed", "failed", "cancelled", "expired"):
                return batch_obj
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Batch {batch_id} did not complete in {timeout} seconds.")
            time.sleep(poll_interval)

    def _download_output_file(self, output_file_id: str, output_path: str) -> None:
        """Download the output file from OpenAI and save it to output_path."""
        url = f"https://api.openai.com/v1/files/{output_file_id}/content"
        response = requests.get(url, headers=self.headers, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def request_batch(self, input_file_path: str, output_path: Optional[str] = None) -> str:
        """
        Send a batch of prompts to the OpenAI API using a file.
        Args:
            input_file_path: Path to the file containing batch prompts (e.g., .jsonl)
            output_path: Where to save the output file (optional)
        Returns:
            Path to the output file or batch job ID if not completed
        """
        # 1. Upload file
        input_file_id = self._upload_file(input_file_path)
        # 2. Create batch
        batch_id = self._create_batch(input_file_id)
        # 3. Poll for status
        batch_obj = self._poll_batch_status(batch_id)
        status = batch_obj.get("status")
        if status != "completed":
            return batch_id  # Return batch ID for further status checking
        # 4. Download output file
        output_file_id = batch_obj.get("output_file_id")
        if not output_file_id:
            raise RuntimeError("Batch completed but no output_file_id found.")
        if output_path is None:
            output_path = f"batch_output_{batch_id}.jsonl"
        self._download_output_file(output_file_id, output_path)
        return output_path