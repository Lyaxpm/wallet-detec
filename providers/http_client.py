from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


class HTTPClient:
    def __init__(self, timeout: float = 15.0):
        self._client = httpx.Client(timeout=timeout)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    def get_json(self, url: str, params: dict | None = None, headers: dict | None = None) -> dict:
        response = self._client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    def post_json(self, url: str, payload: dict, headers: dict | None = None) -> dict:
        response = self._client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        self._client.close()
