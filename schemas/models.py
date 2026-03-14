from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    tool: str
    summary: str
    raw: Dict[str, Any] = Field(default_factory=dict)


class RiskSignal(BaseModel):
    level: str
    title: str
    description: str


class InvestigationReport(BaseModel):
    address: str
    most_likely_chain: str
    classification: str
    address_family: str
    confidence: float
    evidence: List[EvidenceItem] = Field(default_factory=list)
    risk_signals: List[RiskSignal] = Field(default_factory=list)
    final_verdict: str
    reasoning_trace: List[str] = Field(default_factory=list)
    compared_with: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class AgentRunResult(BaseModel):
    report: InvestigationReport
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    raw_agent_messages: List[Dict[str, Any]] = Field(default_factory=list)
