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

## Smoke test (classifier only)

    uv run python eval.py

eval.py sends 20 hand-written, clean invoice lines to qwen2.5:7b in a single prompt
(chart in the prompt, temperature 0). It tests the classification step only, not the VAT checker,
the reporter or the crew. Result: 17/20 = 85% (95% interval roughly 64-95%). This is not a benchmark,
and it is not comparable to the 74-row held-out test of the fine-tuned 0.5B model.
A sample crew output is in output/review.md.

## Related

- Fine-tuned 0.5B account suggester: https://github.com/ChadSaglam/swiss-bookkeeping-ai
- Dataset: https://huggingface.co/datasets/ChadSaglam/swiss-sme-bookkeeping-dataset
- Local MCP agent and attack evaluation: https://github.com/ChadSaglam/bookkeeping-mcp-agent

## Limits

Synthetic data and a simplified six-account test chart. A 7B model follows instructions
imperfectly (it sometimes adds alternatives or extra text).

- Confidence values in the report are written by the model. They are not calibrated or validated.
- Not tested against invoice text that tries to steer the model. In a related test, short suffixes
  such as "(advertising)" changed the answer of the fine-tuned 0.5B model in many cases
  (https://github.com/ChadSaglam/bookkeeping-mcp-agent/blob/main/REPORT.md). The same risk
  may apply here but was not measured.
- Not accounting or tax advice.
