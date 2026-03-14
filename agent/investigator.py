from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from agent.hermes_client import HermesClient
from agent.prompts import SYSTEM_PROMPT, build_mission
from schemas.models import AgentRunResult, InvestigationReport
from tools.evidence_tools import EvidenceToolRegistry

logger = logging.getLogger(__name__)


class HermesInvestigator:
    def __init__(self, hermes_client: HermesClient, tool_registry: EvidenceToolRegistry):
        self.hermes_client = hermes_client
        self.tool_registry = tool_registry

    def run(self, address: str, mode: str = "investigate", address2: str | None = None) -> AgentRunResult:
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_mission(address, mode=mode, address2=address2)},
        ]

        tool_calls: List[Dict[str, Any]] = []
        tools = self.tool_registry.as_openai_tool_schema()

        for _ in range(8):
            response = self.hermes_client.chat(messages=messages, tools=tools)
            msg = response["choices"][0]["message"]
            messages.append(msg)

            if not msg.get("tool_calls"):
                content = msg.get("content", "{}")
                report = self._parse_report(content, address)
                if address2:
                    report.compared_with = address2
                return AgentRunResult(report=report, tool_calls=tool_calls, raw_agent_messages=messages)

            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"].get("arguments", "{}"))
                tool_fn = self.tool_registry.tools.get(name)
                if not tool_fn:
                    output = {"error": f"Unknown tool: {name}"}
                else:
                    try:
                        output = tool_fn(**args)
                    except Exception as exc:
                        output = {"error": str(exc), "tool": name, "args": args}

                tool_calls.append({"tool": name, "args": args, "output": output})
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "name": name,
                        "content": json.dumps(output),
                    }
                )

        fallback = InvestigationReport(
            address=address,
            most_likely_chain="unknown",
            classification="unknown",
            address_family="unknown",
            confidence=0.1,
            evidence=[],
            risk_signals=[],
            final_verdict="Unable to finalize within tool-call budget.",
            reasoning_trace=["Agent exceeded step budget before producing final JSON report."],
        )
        return AgentRunResult(report=fallback, tool_calls=tool_calls, raw_agent_messages=messages)

    def _parse_report(self, raw_content: str, address: str) -> InvestigationReport:
        text = raw_content.strip()
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("json", "", 1).strip()

        try:
            data = json.loads(text)
            if "address" not in data:
                data["address"] = address
            return InvestigationReport(**data)
        except Exception as exc:
            logger.warning("Failed to parse Hermes JSON output: %s", exc)
            return InvestigationReport(
                address=address,
                most_likely_chain="unknown",
                classification="unknown",
                address_family="unknown",
                confidence=0.2,
                evidence=[{"tool": "agent_output", "summary": "Raw response fallback", "raw": {"content": raw_content}}],
                risk_signals=[
                    {
                        "level": "medium",
                        "title": "Parsing failure",
                        "description": "Model output was not valid JSON; fallback report generated.",
                    }
                ],
                final_verdict="Incomplete automated analysis due to parsing issue.",
                reasoning_trace=["Hermes response parsing failed; returned defensive fallback report."],
            )
