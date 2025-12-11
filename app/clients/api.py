import os
from typing import Any

import httpx


class ApiClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        self.timeout = float(os.getenv("API_TIMEOUT_SECONDS", "10"))
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def send_callback(self, path: str, payload: dict[str, Any]) -> None:
        """
        Send orchestration results back to the API.
        """
        url = path if path.startswith("http") else f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        response = await self._client.post(url, json=payload)
        response.raise_for_status()

    async def close(self) -> None:
        await self._client.aclose()


api_client = ApiClient()
