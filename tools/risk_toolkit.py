from __future__ import annotations

from typing import Dict, List

# Minimal local blocklist for demo-ready signal checks.
SANCTIONED_EXAMPLES = {
    "0xd90e2f925da726b50c4ed8d0fb90ad053324f31b": "Tornado Cash-related sanction sample",
    "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh": "Demo sanctioned sample",
}


def run_basic_risk_checks(address: str, evidence: Dict) -> Dict:
    lower = address.lower()
    signals: List[Dict] = []

    if lower in SANCTIONED_EXAMPLES:
        signals.append(
            {
                "level": "high",
                "title": "Address appears on local sanction watch sample",
                "description": SANCTIONED_EXAMPLES[lower],
            }
        )

    if evidence.get("has_code") and evidence.get("nonce", 0) == 0:
        signals.append(
            {
                "level": "medium",
                "title": "Dormant contract",
                "description": "Contract bytecode exists but nonce is zero; verify deployment context.",
            }
        )

    if evidence.get("tx_count", 0) == 0 and evidence.get("balance_wei", 0) == 0 and evidence.get("lamports", 0) == 0:
        signals.append(
            {
                "level": "low",
                "title": "No observed activity",
                "description": "Address currently appears inactive on checked network paths.",
            }
        )

    return {"signals": signals, "signal_count": len(signals)}
