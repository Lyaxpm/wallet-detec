from __future__ import annotations

from agent.hermes_client import HermesClient
from agent.investigator import HermesInvestigator
from config import Settings
from providers.bitcoin_provider import BitcoinProvider
from providers.evm_provider import EVMProvider
from providers.http_client import HTTPClient
from providers.hyperliquid_provider import HyperliquidProvider
from providers.solana_provider import SolanaProvider
from tools.evidence_tools import EvidenceToolRegistry


def build_investigator() -> HermesInvestigator:
    settings = Settings()
    http_client = HTTPClient()

    tool_registry = EvidenceToolRegistry(
        evm_provider=EVMProvider(http_client),
        solana_provider=SolanaProvider(http_client),
        bitcoin_provider=BitcoinProvider(http_client),
        hyperliquid_provider=HyperliquidProvider(http_client),
    )

    hermes = HermesClient(settings)
    return HermesInvestigator(hermes_client=hermes, tool_registry=tool_registry)
