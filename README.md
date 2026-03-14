# Hermes Chain Detective

Hermes Chain Detective is a **Hermes-native blockchain intelligence agent** for hackathon demos. It investigates arbitrary blockchain addresses and produces a concise intelligence report with evidence, risk hints, and a reasoning trace.

## Why this is Hermes-native

This project does **not** hardcode a rigid investigation pipeline. Instead:

- Hermes receives a mission.
- Hermes dynamically decides which evidence tools to call and in what order.
- Tools only fetch raw evidence (format signals, chain probes, account metadata, etc.).
- Hermes interprets evidence and produces the final conclusion.

## Supported chains (initial)

- Ethereum
- Base
- Arbitrum
- BSC
- Polygon
- Solana
- Hyperliquid
- Bitcoin (basic)

---

## Architecture

```text
main.py
 ├─ interfaces/
 │   ├─ cli.py              # CLI commands
 │   └─ telegram_bot.py     # Telegram commands
 ├─ services.py             # Shared dependency wiring
 ├─ agent/
 │   ├─ investigator.py     # Dynamic Hermes tool-calling loop
 │   ├─ hermes_client.py    # OpenAI-compatible chat client
 │   └─ prompts.py          # Mission + output contract
 ├─ tools/
 │   ├─ evidence_tools.py   # Tool registry (evidence-only)
 │   ├─ address_toolkit.py  # Format heuristics
 │   └─ risk_toolkit.py     # Lightweight risk checks
 ├─ providers/
 │   ├─ evm_provider.py
 │   ├─ solana_provider.py
 │   ├─ hyperliquid_provider.py
 │   ├─ bitcoin_provider.py
 │   └─ http_client.py
 ├─ schemas/models.py       # Pydantic report schema
 └─ formatters/report_formatter.py
```

### Dynamic investigation flow

1. Hermes gets mission: investigate/compare/explain an address.
2. Hermes calls tools based on hypotheses (format -> likely chain families -> chain probes -> risk checks).
3. Tool outputs are fed back to Hermes as evidence.
4. Hermes decides whether to collect more evidence or finalize.
5. Hermes returns final JSON report with:
   - Most Likely Chain
   - Classification
   - Confidence
   - Evidence
   - Risk Signals
   - Final Verdict
   - Reasoning Trace

No provider contains decision logic; intelligence stays in Hermes.

---

## Ubuntu setup

```bash
git clone <repo_url>
cd wallet-detec
cp .env.example .env
# Fill HERMES_API_KEY and TELEGRAM_BOT_TOKEN
bash install.sh
```

## Environment configuration

Set in `.env`:

- `HERMES_BASE_URL` (default points to Hermes endpoint)
- `HERMES_API_KEY`
- `HERMES_MODEL`
- `TELEGRAM_BOT_TOKEN`
- `LOG_LEVEL`

---

## CLI usage

### Investigate
```bash
python main.py investigate <address>
```

### Explain (explicit reasoning trace emphasis)
```bash
python main.py explain <address>
```

### Compare
```bash
python main.py compare <address1> <address2>
```

### Start Telegram bot
```bash
python main.py bot
```

You can also use helper scripts:

```bash
./run_cli.sh investigate <address>
./run_bot.sh
```

---

## Telegram bot commands

- `/start`
- `/help`
- `/investigate <address>`
- `/explain <address>`
- `/compare <address1> <address2>`

Both CLI and Telegram route into the same `HermesInvestigator` engine.

---

## Demo instructions

1. Start with a known EVM address:
   ```bash
   python main.py investigate 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
   ```
2. Try explain mode for richer reasoning trace:
   ```bash
   python main.py explain Vote111111111111111111111111111111111111111
   ```
3. Compare two addresses:
   ```bash
   python main.py compare 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 Vote111111111111111111111111111111111111111
   ```
4. Open Telegram and run `/investigate <address>`.

See `examples/demo_inputs.md` and `examples/example_output.md`.

---

## Notes

- Risk signals are intentionally lightweight and evidence-based for demo speed.
- If a provider is unavailable, Hermes should explicitly mention evidence limitations.
- Designed for hackathon demos: polished output, dynamic reasoning, and modular extension points.
