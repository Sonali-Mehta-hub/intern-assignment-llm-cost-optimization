# Question 2 – Four-Node Support Pipeline Optimization

## Overview

This implementation optimizes the ShopAssist support pipeline using four logical stages:

1. Triage
2. Retrieve
3. Compose
4. Audit

The objective is to reduce the billing points per ticket while maintaining the expected `action` and `kb_article` values.

## Optimizations Implemented

### 1. Triage – Python Processing

The ticket is processed using Python instead of an additional LLM call.

Only a limited portion of the conversation is used:

```python
thread = ticket.get("thread", "")
thread = thread[:500]
```

This avoids sending the complete conversation unnecessarily.

### 2. Retrieve – Relevant Article Selection

Instead of including the complete help center, the implementation retrieves relevant articles using:

```python
articles = relevant_articles(ticket, order)
```

Only the selected policy information is passed to the composition stage.

### 3. Compose – Single LLM Call

The composition stage creates the final response using:

- Ticket ID
- Triage information
- Relevant policy articles
- Order snapshot

Only this stage makes an LLM call:

```python
draft = self.llm.chat("compose", messages)
```

This avoids the overhead of making separate LLM calls for triage and retrieval.

### 4. Audit – Python Validation

The audit stage parses the generated response and validates the required fields.

It checks that:

- The action belongs to the allowed action set.
- The `kb_article` field is present.

Allowed actions:

```python
{
    "REFUND",
    "REPLACE",
    "SEND_ARTICLE",
    "ESCALATE_TIER2"
}
```

The audit stage uses Python validation rather than another LLM call.

## Cost Results

The target was to keep every public ticket below 2,500 billing points.

| Ticket | Input Tokens | Output Tokens | Total Points |
|---|---:|---:|---:|
| T-1001 | 223 | 46 | 1,359 |
| T-1002 | 207 | 39 | 1,206 |
| T-1003 | 231 | 39 | 1,278 |
| T-1004 | 355 | 36 | 1,605 |
| **Total** | **1,016** | **160** | **5,448** |

All four public tickets are below the 2,500-point target.

## Detailed Cost Breakdown

### T-1004 – Physical Fulfillment Path

This ticket follows the replacement path.

| Component | Calculation | Points |
|---|---:|---:|
| Input cost | 355 × 3 | 1,065 |
| Output cost | 36 × 15 | 540 |
| **Total** | | **1,605** |

### T-1003 – Escalation Path

This ticket follows the escalation path.

| Component | Calculation | Points |
|---|---:|---:|
| Input cost | 231 × 3 | 693 |
| Output cost | 39 × 15 | 585 |
| **Total** | | **1,278** |

## How to Run

Run from the project root directory:

```bash
python question2/run.py
```

## How to Run the Correctness Test

```bash
python -m pytest tests/test_question2.py -k "pipeline_resolves_public_tickets" -v
```

The targeted correctness test verifies that all four public tickets return the expected action and knowledge-base article.

## Key Takeaway

The main optimization is replacing separate LLM calls for triage, retrieval, and audit with lightweight Python processing. Only the composition stage uses the LLM, and it receives the relevant ticket and policy context instead of the complete help center.