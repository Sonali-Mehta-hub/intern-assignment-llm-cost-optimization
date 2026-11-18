# ShopAssist — support copilot cost lab

# LLM Cost Optimization

## Overview

This project focuses on reducing LLM token consumption and billing costs while maintaining the expected output and correctness of support ticket resolution.

It contains two optimization tasks implemented using Python.

## Project Structure

```text
.
├── question1/
│   ├── agent.py
│   ├── run.py
│   └── README.md
│
├── question2/
│   ├── agent.py
│   ├── run.py
│   └── README.md
│
├── shared/
│   ├── billing.py
│   ├── kb.py
│   └── llm.py
│
└── tests/
```

## Optimization Summary

### Question 1 – SupportCopilot

- Implemented selective knowledge-base retrieval.
- Added dynamic few-shot example selection.
- Reduced unnecessary prompt context.
- Used a single LLM call per ticket.

**Result:** Reduced billing points from 35,427 to 6,012 (83.03% reduction).

[View Question 1 Implementation](question1/README.md)

### Question 2 – Four-Node Support Pipeline

- Implemented a four-stage pipeline: Triage, Retrieve, Compose, and Audit.
- Used Python for triage, retrieval, and validation.
- Reduced the pipeline to one LLM call per ticket.
- Included only relevant policy information in the composition prompt.

**Result:** All four public tickets were resolved within the 2,500-point target.

| Ticket | Billing Points |
|---|---:|
| T-1001 | 1,359 |
| T-1002 | 1,206 |
| T-1003 | 1,278 |
| T-1004 | 1,605 |
| **Total** | **5,448** |

[View Question 2 Implementation](question2/README.md)

## Installation

Clone the repository:

```bash
git clone https://github.com/Sonali-Mehta-hub/intern-assignment-llm-cost-optimization.git
cd intern-assignment-llm-cost-optimization
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

Run Question 1:

```bash
python question1/run.py
```

Run Question 2:

```bash
python question2/run.py
```

## Run Tests

Question 1:

```bash
python -m pytest tests/test_question1.py
```

Question 2 correctness test:

```bash
python -m pytest tests/test_question2.py -k "pipeline_resolves_public_tickets" -v
```

## Technologies Used

- Python
- LLM Prompt Engineering
- Token and Cost Optimization
- Pytest

## Note

Billing results are based on the local LLM and billing simulator provided with the assignment. They represent simulator billing points, not actual API charges.
