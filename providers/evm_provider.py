from __future__ import annotations

from typing import Dict

from providers.http_client import HTTPClient


CHAIN_RPCS: Dict[str, str] = {
    "ethereum": "https://cloudflare-eth.com",
    "base": "https://mainnet.base.org",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "bsc": "https://bsc-dataseed.binance.org",
    "polygon": "https://polygon-rpc.com",
}


class EVMProvider:
    def __init__(self, client: HTTPClient):
        self.client = client

    def _rpc(self, chain: str, method: str, params: list):
        url = CHAIN_RPCS[chain]
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        return self.client.post_json(url, payload)

    def account_snapshot(self, chain: str, address: str) -> dict:
        balance = self._rpc(chain, "eth_getBalance", [address, "latest"]).get("result")
        code = self._rpc(chain, "eth_getCode", [address, "latest"]).get("result")
        nonce = self._rpc(chain, "eth_getTransactionCount", [address, "latest"]).get("result")
        chain_id = self._rpc(chain, "eth_chainId", []).get("result")
        return {
            "chain": chain,
            "chain_id": int(chain_id, 16) if chain_id else None,
            "balance_wei": int(balance, 16) if balance else 0,
            "nonce": int(nonce, 16) if nonce else 0,
            "has_code": bool(code and code != "0x"),
            "code_size": (len(code) - 2) // 2 if code and code.startswith("0x") else 0,
        }
