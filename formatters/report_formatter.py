from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from schemas.models import InvestigationReport


def render_cli_report(report: InvestigationReport) -> None:
    console = Console()

    summary = Table.grid(padding=(0, 2))
    summary.add_row("Address", report.address)
    summary.add_row("Most Likely Chain", report.most_likely_chain)
    summary.add_row("Classification", report.classification)
    summary.add_row("Address Family", report.address_family)
    summary.add_row("Confidence", f"{report.confidence:.2f}")
    summary.add_row("Final Verdict", report.final_verdict)

    console.print(Panel(summary, title="🕵️ Hermes Chain Detective", border_style="cyan"))

    evidence_table = Table(title="Evidence", show_lines=True)
    evidence_table.add_column("Tool", style="green")
    evidence_table.add_column("Summary", style="white")
    for item in report.evidence:
        evidence_table.add_row(item.tool, item.summary)
    console.print(evidence_table)

    risk_table = Table(title="Risk Signals", show_lines=True)
    risk_table.add_column("Level", style="yellow")
    risk_table.add_column("Title", style="red")
    risk_table.add_column("Description")
    if report.risk_signals:
        for signal in report.risk_signals:
            risk_table.add_row(signal.level.upper(), signal.title, signal.description)
    else:
        risk_table.add_row("NONE", "No meaningful risk flags", "No explicit signals from available checks")
    console.print(risk_table)

    reasoning = "\n".join(f"• {step}" for step in report.reasoning_trace)
    console.print(Panel(reasoning or "No reasoning trace provided", title="Reasoning Trace", border_style="magenta"))


def telegram_text(report: InvestigationReport) -> str:
    lines = [
        "🕵️ *Hermes Chain Detective*",
        f"*Address:* `{report.address}`",
        f"*Most Likely Chain:* {report.most_likely_chain}",
        f"*Classification:* {report.classification}",
        f"*Address Family:* {report.address_family}",
        f"*Confidence:* {report.confidence:.2f}",
        f"*Verdict:* {report.final_verdict}",
    ]

    if report.risk_signals:
        lines.append("*Risk Signals:*")
        lines.extend([f"- {r.level.upper()}: {r.title}" for r in report.risk_signals[:3]])

    if report.reasoning_trace:
        lines.append("*Reasoning Trace:*")
        lines.extend([f"- {step}" for step in report.reasoning_trace[:4]])

    return "\n".join(lines)
