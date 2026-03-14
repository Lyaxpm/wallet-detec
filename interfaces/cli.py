from __future__ import annotations

import argparse

from formatters.report_formatter import render_cli_report
from services import build_investigator


def run_cli() -> None:
    parser = argparse.ArgumentParser(prog="Hermes Chain Detective")
    sub = parser.add_subparsers(dest="command", required=True)

    p_inv = sub.add_parser("investigate", help="Investigate a single address")
    p_inv.add_argument("address")

    p_exp = sub.add_parser("explain", help="Investigate with explicit reasoning trace")
    p_exp.add_argument("address")

    p_cmp = sub.add_parser("compare", help="Compare two addresses")
    p_cmp.add_argument("address1")
    p_cmp.add_argument("address2")

    sub.add_parser("bot", help="Run Telegram bot")

    args = parser.parse_args()

    if args.command == "bot":
        from interfaces.telegram_bot import run_bot

        run_bot()
        return

    investigator = build_investigator()

    if args.command == "investigate":
        result = investigator.run(args.address, mode="investigate")
    elif args.command == "explain":
        result = investigator.run(args.address, mode="explain")
    else:
        result = investigator.run(args.address1, mode="compare", address2=args.address2)

    render_cli_report(result.report)
