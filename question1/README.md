# Question 1 – SupportCopilot Optimization

## Overview

This implementation optimizes the SupportCopilot agent to reduce token usage while maintaining the expected ticket resolution.

The main optimization is to avoid sending the complete knowledge base and all few-shot examples to the LLM for every ticket.

## Optimizations Implemented

### 1. Selective Knowledge Base Retrieval

Instead of including the entire knowledge base in the prompt, the implementation uses:

```python
kb_context = relevant_articles(ticket, order)
```

Only the relevant help-center articles are added to the prompt based on the ticket and order information.

### 2. Dynamic Few-Shot Selection

The implementation uses `select_few_shot(ticket, order)` to select examples according to the ticket context.

| Ticket condition | Selected example |
|---|---|
| Digital product or license revealed | Example 2 |
| Customized product | Examples 3 and 4 |
| Damage reported | Example 4 |
| Physical product | Example 1 |
| No matching condition | All examples |

This avoids sending unnecessary examples to the LLM.

### 3. Compact Prompt Construction

The prompt contains only:

- Relevant few-shot examples
- Relevant knowledge-base articles
- Ticket conversation
- Order snapshot
- Required JSON response instructions

The model is instructed to return a concise JSON response.

### 4. Single LLM Call

The optimized implementation uses one LLM call per ticket:

```python
messages = self.build_messages(ticket_id)
response = self.llm.chat("handle_ticket", messages)
```

The response is then parsed using `parse_resolution()`.

## Results

| Metric | Baseline | Optimized |
|---|---:|---:|
| Total points | 35,427 | 6,012 |
| Points saved | - | 29,415 |
| Reduction | - | 83.03% |

The optimization reduces the total token-based billing points by approximately 83%.

## How to Run

Run from the project root directory:

```bash
python question1/run.py
```

## How to Run Tests

```bash
pytest -q tests/test_question1.py
```

## Key Takeaway

The optimization focuses on sending only the context required for each ticket instead of repeatedly sending the complete knowledge base and every example. This reduces prompt size and billing points while preserving the expected ticket resolutions.