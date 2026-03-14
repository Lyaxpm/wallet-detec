from __future__ import annotations

from providers.http_client import HTTPClient


class SolanaProvider:
    def __init__(self, client: HTTPClient):
        self.client = client
        self.rpc_url = "https://api.mainnet-beta.solana.com"

    def _rpc(self, method: str, params: list):
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        return self.client.post_json(self.rpc_url, payload)

    def account_snapshot(self, address: str) -> dict:
        bal_res = self._rpc("getBalance", [address, {"commitment": "confirmed"}])
        acct_res = self._rpc("getAccountInfo", [address, {"encoding": "base64"}])
        sig_res = self._rpc("getSignaturesForAddress", [address, {"limit": 5}])

        value = acct_res.get("result", {}).get("value")
        return {
            "chain": "solana",
            "lamports": bal_res.get("result", {}).get("value", 0),
            "exists": value is not None,
            "executable": bool(value and value.get("executable")),
            "owner": value.get("owner") if value else None,
            "recent_signatures": sig_res.get("result", []),
        }
