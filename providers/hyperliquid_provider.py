from __future__ import annotations

from providers.http_client import HTTPClient


class HyperliquidProvider:
    def __init__(self, client: HTTPClient):
        self.client = client
        self.url = "https://api.hyperliquid.xyz/info"

    def user_state(self, address: str) -> dict:
        payload = {"type": "clearinghouseState", "user": address}
        try:
            data = self.client.post_json(self.url, payload)
            return {"chain": "hyperliquid", "found": True, "state": data}
        except Exception as exc:
            return {"chain": "hyperliquid", "found": False, "error": str(exc)}
