
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from question1.agent import SupportCopilot
from shared.billing import CostSession

PUBLIC = ["T-1001", "T-1002", "T-1003", "T-1004"]


def main() -> None:
    copilot = SupportCopilot()
    rows = []

    for ticket_id in PUBLIC:
        before = copilot.session.total_points()

        result = copilot.handle_ticket(ticket_id)

        after = copilot.session.total_points()
        ticket_points = after - before

        rows.append({
            "ticket_id": ticket_id,
            "action": result.action,
            "kb_article": result.kb_article,
            "points": ticket_points,
        })

    print(json.dumps({
        "resolutions": rows,
        "total_points": copilot.session.total_points(),
        "average_points": copilot.session.total_points() / len(PUBLIC),
    }, indent=2))


if __name__ == "__main__":
    main()
