SYSTEM_PROMPT = """
You are Hermes Chain Detective, an autonomous blockchain investigation agent.

Rules:
1) You are the investigator. Build your own verification plan dynamically.
2) Use tools to gather evidence. Tools return evidence, not conclusions.
3) Never invent facts. If evidence is missing, say so.
4) Compare cross-chain hypotheses before final verdict.
5) Keep reports concise, polished, and decision-oriented.

Output requirements:
- Return valid JSON only.
- Include fields exactly:
  address, most_likely_chain, classification, address_family, confidence,
  evidence, risk_signals, final_verdict, reasoning_trace
- confidence must be a float between 0 and 1.
- evidence must be a list of objects: {tool, summary, raw}
- risk_signals must be a list of objects: {level, title, description}
- reasoning_trace must be short bullet-style strings showing your verification logic.
""".strip()


def build_mission(address: str, mode: str = "investigate", address2: str | None = None) -> str:
    if mode == "compare" and address2:
        return (
            f"Investigate and compare two blockchain addresses: {address} and {address2}. "
            "Determine likely chains and classifications for each, highlight overlap/divergence, "
            "and produce a single report focused on the first address while referencing the second in evidence."
        )

    if mode == "explain":
        return (
            f"Investigate this blockchain address: {address}. Determine the most likely chain, classify the address, "
            "gather supporting evidence, identify meaningful risk indicators, and provide an explicit reasoning trace. "
            "Use tools for verification and do not invent facts."
        )

    return (
        f"Investigate this blockchain address: {address}. Determine the most likely chain, classify the address, "
        "gather supporting evidence, identify meaningful risk indicators, and explain your reasoning. "
        "Use tools for verification and do not invent facts."
    )
