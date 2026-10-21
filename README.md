# Invoice Review Crew

Three CrewAI agents review Swiss SME invoice lines (synthetic data only):

1. Classifier: assigns each line to one account from a chart you supply.
2. VAT checker: flags lines whose VAT rate is not in the allowed list.
3. Reporter: writes a short review for a business owner, with confidence per line.

Low-confidence or flagged lines are routed to a human. The crew never books anything.

## Run locally

Needs Ollama and a pulled model:

    ollama pull qwen2.5:7b
    uv sync
    uv run python -m crewai run

Edit the invoice lines, chart and VAT rates in src/invoice_review/main.py.
Agents and tasks are in src/invoice_review/config/. No API key is needed for local Ollama.
If you use a hosted model instead, put its key in a local .env file (never committed).

## Measure accuracy

    uv run python eval.py

Prompted qwen2.5:7b scored 85% (17/20) on a 20-line smoke test. This is not a benchmark.

## Related

- Fine-tuned 0.5B account suggester: https://github.com/ChadSaglam/swiss-bookkeeping-ai
- Dataset: https://huggingface.co/datasets/ChadSaglam/swiss-sme-bookkeeping-dataset

## Limits

Synthetic data and a simplified six-account test chart. A 7B model follows instructions
imperfectly (it sometimes adds alternatives or extra text). Not accounting or tax advice.
