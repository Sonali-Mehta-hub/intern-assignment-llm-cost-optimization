
# ShopAssist – LLM Cost Optimization

## Overview

This project focuses on optimizing the ShopAssist support copilot by reducing LLM token consumption and billing costs while maintaining the expected ticket-resolution results.

The primary objective is to reduce unnecessary prompt tokens, minimize LLM calls, and use relevant context under the assignment's billing rules.

The project contains two optimization tasks implemented in Python.

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

**Optimizations implemented:**

- Selective knowledge-base retrieval instead of including the entire knowledge base.
- Dynamic few-shot example selection based on ticket and order information.
- Reduced unnecessary prompt context.
- Single LLM call per ticket.

**Results:**

| Metric | Baseline | Optimized |
|---|---:|---:|
| Total billing points | 35,427 | 6,012 |
| Points saved | - | 29,415 |
| Cost reduction | - | 83.03% |

[View Question 1 Implementation](question1/README.md)

### Question 2 – Four-Node Support Pipeline

The pipeline follows four logical stages:

1. **Triage:** Processes ticket information using Python.
2. **Retrieve:** Selects relevant knowledge-base articles.
3. **Compose:** Generates the final response using one LLM call.
4. **Audit:** Validates the generated response using Python.

**Optimizations implemented:**

- Replaced separate LLM calls for triage, retrieval, and audit with Python processing.
- Limited unnecessary ticket conversation context.
- Retrieved only relevant policy information.
- Used a single LLM call per ticket for response composition.

**Results:**

All four public tickets were resolved within the target of 2,500 billing points per ticket.

| Ticket | Billing Points |
|---|---:|
| T-1001 | 1,359 |
| T-1002 | 1,206 |
| T-1003 | 1,278 |
| T-1004 | 1,605 |
| **Total** | **5,448** |

[View Question 2 Implementation](question2/README.md)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sonali-Mehta-hub/intern-assignment-llm-cost-optimization.git

cd intern-assignment-llm-cost-optimization
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

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

Question 2 – Public ticket correctness test:

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
