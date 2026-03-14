from __future__ import annotations

import logging
from typing import Any, Callable, Dict

from providers.bitcoin_provider import BitcoinProvider
from providers.evm_provider import CHAIN_RPCS, EVMProvider
from providers.hyperliquid_provider import HyperliquidProvider
from providers.solana_provider import SolanaProvider
from tools.address_toolkit import inspect_address_format
from tools.risk_toolkit import run_basic_risk_checks

logger = logging.getLogger(__name__)


class EvidenceToolRegistry:
    def __init__(
        self,
        evm_provider: EVMProvider,
        solana_provider: SolanaProvider,
        bitcoin_provider: BitcoinProvider,
        hyperliquid_provider: HyperliquidProvider,
    ):
        self.evm_provider = evm_provider
        self.solana_provider = solana_provider
        self.bitcoin_provider = bitcoin_provider
        self.hyperliquid_provider = hyperliquid_provider

        self.tools: Dict[str, Callable[..., Dict[str, Any]]] = {
            "inspect_address_format": self.inspect_address_format,
            "probe_supported_chains": self.probe_supported_chains,
            "evm_account_snapshot": self.evm_account_snapshot,
            "solana_account_snapshot": self.solana_account_snapshot,
            "bitcoin_address_summary": self.bitcoin_address_summary,
            "hyperliquid_user_state": self.hyperliquid_user_state,
            "basic_risk_checks": self.basic_risk_checks,
        }

    def inspect_address_format(self, address: str) -> Dict[str, Any]:
        return inspect_address_format(address)

    def probe_supported_chains(self, address: str) -> Dict[str, Any]:
        results: Dict[str, Any] = {"address": address, "probes": {}}
        fmt = inspect_address_format(address)
        candidates = fmt.get("candidate_families", [])

        if "evm" in candidates:
            for chain in CHAIN_RPCS:
                try:
                    results["probes"][chain] = self.evm_provider.account_snapshot(chain, address)
                except Exception as exc:
                    logger.debug("EVM probe failed for %s: %s", chain, exc)
                    results["probes"][chain] = {"chain": chain, "error": str(exc)}

        if "solana_like" in candidates:
            try:
                results["probes"]["solana"] = self.solana_provider.account_snapshot(address)
            except Exception as exc:
                results["probes"]["solana"] = {"chain": "solana", "error": str(exc)}

        if "bitcoin" in candidates:
            try:
                results["probes"]["bitcoin"] = self.bitcoin_provider.address_summary(address)
            except Exception as exc:
                results["probes"]["bitcoin"] = {"chain": "bitcoin", "error": str(exc)}

        if "hyperliquid_like" in candidates or "evm" in candidates:
            results["probes"]["hyperliquid"] = self.hyperliquid_provider.user_state(address)

        return results

    def evm_account_snapshot(self, chain: str, address: str) -> Dict[str, Any]:
        return self.evm_provider.account_snapshot(chain, address)

    def solana_account_snapshot(self, address: str) -> Dict[str, Any]:
        return self.solana_provider.account_snapshot(address)

    def bitcoin_address_summary(self, address: str) -> Dict[str, Any]:
        return self.bitcoin_provider.address_summary(address)

    def hyperliquid_user_state(self, address: str) -> Dict[str, Any]:
        return self.hyperliquid_provider.user_state(address)

    def basic_risk_checks(self, address: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
        return run_basic_risk_checks(address, evidence)

    def as_openai_tool_schema(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "inspect_address_format",
                    "description": "Inspect address syntax and return candidate address families.",
                    "parameters": {
                        "type": "object",
                        "properties": {"address": {"type": "string"}},
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "probe_supported_chains",
                    "description": "Probe supported chains opportunistically and return raw evidence snapshots.",
                    "parameters": {
                        "type": "object",
                        "properties": {"address": {"type": "string"}},
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "evm_account_snapshot",
                    "description": "Get EVM account metadata for one chain.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {"type": "string", "enum": ["ethereum", "base", "arbitrum", "bsc", "polygon"]},
                            "address": {"type": "string"},
                        },
                        "required": ["chain", "address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "solana_account_snapshot",
                    "description": "Get Solana account metadata and recent signature hints.",
                    "parameters": {
                        "type": "object",
                        "properties": {"address": {"type": "string"}},
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "bitcoin_address_summary",
                    "description": "Get Bitcoin address summary stats.",
                    "parameters": {
                        "type": "object",
                        "properties": {"address": {"type": "string"}},
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "hyperliquid_user_state",
                    "description": "Get Hyperliquid user state if account exists.",
                    "parameters": {
                        "type": "object",
                        "properties": {"address": {"type": "string"}},
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "basic_risk_checks",
                    "description": "Run lightweight risk checks over accumulated evidence.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {"type": "string"},
                            "evidence": {"type": "object"},
                        },
                        "required": ["address", "evidence"],
                    },
                },
            },
        ]
