
from __future__ import annotations

import json
from dataclasses import dataclass

from shared.billing import CostSession
from shared.kb import relevant_articles
from shared.llm import ChatMessage, LlmClient
from shared.tools import format_thread, get_order, get_ticket

from question1.agent import parse_resolution


@dataclass
class TicketResolution:
    action: str
    kb_article: str


class SupportPipeline:
    """Four-node ShopAssist pipeline with one LLM call."""

    def __init__(self, session: CostSession | None = None):
        self.session = session or CostSession()
        self.llm = LlmClient(self.session)

    def handle_ticket(self, ticket_id: str) -> TicketResolution:
        ticket = get_ticket(ticket_id)
        order = get_order(ticket["order_id"])
        thread = format_thread(ticket)
        snapshot = json.dumps(order, indent=2)

        triage = self._triage(ticket_id, thread)
        retrieved = self._retrieve(ticket, order)
        draft = self._compose(ticket_id, snapshot, triage, retrieved)
        return self._audit(draft)

    # Node 1: Triage
    def _triage(self, ticket_id: str, thread: str) -> str:
        return (
            f"Ticket: {ticket_id}\n"
            f"Customer issue: {thread[:500]}"
        )

    # Node 2: Retrieve
    def _retrieve(self, ticket: dict, order: dict) -> str:
        return relevant_articles(ticket, order)

    # Node 3: Compose
    def _compose(
        self,
        ticket_id: str,
        snapshot: str,
        triage: str,
        retrieved: str,
    ) -> str:
        messages = [
            ChatMessage(
                "system",
                "Compose a concise ShopAssist resolution. "
                "Return JSON with action, kb_article and customer_reply.",
            ),
            ChatMessage(
                "user",
                f"TICKET: {ticket_id}\n"
                f"{triage}\n"
                f"RELEVANT POLICY:\n{retrieved}\n"
                f"ORDER_SNAPSHOT:\n{snapshot}\nEND_SNAPSHOT",
            ),
        ]

        return self.llm.chat("compose", messages)

    # Node 4: Audit
    def _audit(self, draft: str) -> TicketResolution:
        parsed = parse_resolution(draft)

        allowed_actions = {
            "REFUND",
            "REPLACE",
            "SEND_ARTICLE",
            "ESCALATE_TIER2",
        }

        if parsed.action not in allowed_actions:
            raise ValueError(f"Invalid action: {parsed.action}")

        if not parsed.kb_article:
            raise ValueError("Missing knowledge-base article")

        return TicketResolution(
            action=parsed.action,
            kb_article=parsed.kb_article,
        )
