from __future__ import annotations

from providers.http_client import HTTPClient


class BitcoinProvider:
    def __init__(self, client: HTTPClient):
        self.client = client
        self.base_url = "https://blockstream.info/api"

    def address_summary(self, address: str) -> dict:
        data = self.client.get_json(f"{self.base_url}/address/{address}")
        chain_stats = data.get("chain_stats", {})
        mempool_stats = data.get("mempool_stats", {})
        return {
            "chain": "bitcoin",
            "funded_txo_count": chain_stats.get("funded_txo_count", 0),
            "spent_txo_count": chain_stats.get("spent_txo_count", 0),
            "tx_count": chain_stats.get("tx_count", 0),
            "funded_txo_sum": chain_stats.get("funded_txo_sum", 0),
            "spent_txo_sum": chain_stats.get("spent_txo_sum", 0),
            "mempool_tx_count": mempool_stats.get("tx_count", 0),
        }
