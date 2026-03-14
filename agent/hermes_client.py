from __future__ import annotations

import logging
from typing import Any, Dict, List

import httpx

from config import Settings

logger = logging.getLogger(__name__)


class HermesClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = settings.hermes_base_url.rstrip("/")
        self.model = settings.hermes_model
        self.api_key = settings.hermes_api_key
        self.client = httpx.Client(timeout=45.0)

    def chat(self, messages: List[Dict[str, Any]], tools: list | None = None, temperature: float = 0.2) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = self.client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        body = response.json()
        logger.debug("Hermes response: %s", body)
        return body

    def close(self) -> None:
        self.client.close()
