# Example CLI Output (abridged)

```text
🕵️ Hermes Chain Detective
Address: 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
Most Likely Chain: ethereum
Classification: wallet
Address Family: evm
Confidence: 0.93
Final Verdict: High-confidence EVM wallet with confirmed on-chain activity.

Evidence:
- inspect_address_format: Matches 0x-prefixed 20-byte hex format
- probe_supported_chains: Ethereum nonce and balance are non-zero; no code detected
- basic_risk_checks: No high-risk sanction hit from local sample list

Risk Signals:
- LOW: No explicit high-risk indicators found in lightweight checks

Reasoning Trace:
- Tested syntax first to establish candidate families.
- Queried multiple EVM chains and compared activity footprints.
- Selected Ethereum due to strongest activity evidence and consistency.
```
