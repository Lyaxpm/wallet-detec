from __future__ import annotations

import re
from typing import Dict

BASE58_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]+$")
HEX_EVM_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
BTC_RE = re.compile(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{20,90}$")


def inspect_address_format(address: str) -> Dict:
    signals = []
    families = []

    if HEX_EVM_RE.match(address):
        families.append("evm")
        signals.append("Matches 0x-prefixed 20-byte hex format")

    if BTC_RE.match(address):
        families.append("bitcoin")
        signals.append("Matches common Bitcoin legacy/bech32 address shape")

    if BASE58_RE.match(address) and 32 <= len(address) <= 44 and not address.startswith("0x"):
        families.extend(["solana_like", "hyperliquid_like"])
        signals.append("Looks like base58 address/account identifier")

    return {
        "address": address,
        "length": len(address),
        "candidate_families": sorted(list(set(families))),
        "format_signals": signals,
        "is_probably_valid": len(families) > 0,
    }
