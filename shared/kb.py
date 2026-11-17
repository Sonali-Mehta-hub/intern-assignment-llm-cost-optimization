from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from shared.tokens import count_tokens

KB_DIR = Path(__file__).resolve().parents[1] / "data" / "kb"


@lru_cache
def article_ids() -> list[str]:
    return sorted(p.stem for p in KB_DIR.glob("*.md"))


@lru_cache
def load_article(article_id: str) -> str:
    return (KB_DIR / f"{article_id}.md").read_text()


@lru_cache
def all_articles_blob() -> str:
    """Concatenated help-center articles for Question 1."""
    parts = []
    for aid in article_ids():
        parts.append(f"--- {aid} ---\n{load_article(aid)}\n")
    return "\n".join(parts)


@lru_cache
def expanded_help_center_blob() -> str:
    """Expanded help center for Question 2."""
    base = all_articles_blob()
    filler = (
        "## Internal routing note\n"
        "Carrier pickup windows, warehouse bin labels, and CS macro catalog. "
        "Does not change customer policy unless an article id is cited.\n"
    )
    chunks = [base]
    i = 0
    while count_tokens("\n".join(chunks)) < 210_000:
        chunks.append(filler + f"Batch {i}\n" + ("-" * 40 + "\n") * 30)
        i += 1
    return "\n".join(chunks)


def title_index(limit: int | None = 400) -> str:
    ids = article_ids()
    if limit:
        ids = ids[:limit]
    return "\n".join(f"{aid}" for aid in ids)



def relevant_articles(ticket: dict, order: dict) -> str:
    selected = set()

    message = " ".join(
        str(msg.get("text", ""))
        for msg in ticket.get("messages", [])
    ).lower()

    product_type = str(order.get("product_type", "")).lower()

    if product_type == "digital" and order.get("license_revealed"):
        selected.add("digital-license-no-refund")

    if product_type == "physical":
        selected.add("returns-within-30-days")

        if order.get("opened"):
            # The referenced opened-goods policy is not available.
            # Keep the full KB to avoid missing relevant policy context.
            return all_articles_blob()

    if order.get("damage_reported"):
        selected.add("damage-replacement-7-days")

    if order.get("customized"):
        selected.add("custom-items-no-replace")

    if (
        product_type == "subscription"
        or "subscription" in message
        or "annual plan" in message
    ):
        selected.add("subscription-cooling-off")

    if not selected:
        return all_articles_blob()

    return "\n".join(
        f"--- {aid} ---\n{load_article(aid)}"
        for aid in sorted(selected)
        if aid in article_ids()
    )
