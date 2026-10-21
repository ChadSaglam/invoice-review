import re
import litellm

MODEL = "ollama/qwen2.5:7b"

CHART = """6510 Telephone and internet
6570 IT and software
6200 Vehicle expenses
5830 Travel expenses (staff)
6500 Office supplies and administration
6600 Advertising"""

DATA = [
    ("Swisscom Mobile Abo März CHF 89.50", "6510"),
    ("Sunrise Internet Business CHF 69.00", "6510"),
    ("Salt Mobile Roaming CHF 24.90", "6510"),
    ("Microsoft 365 Business CHF 12.60", "6570"),
    ("GitHub Team Abo CHF 21.00", "6570"),
    ("Adobe Creative Cloud CHF 66.90", "6570"),
    ("Notion Plan CHF 10.00", "6570"),
    ("SBB Zugticket Zürich-Bern CHF 52.00", "5830"),
    ("SBB Tageskarte Geschäftsreise Basel CHF 76.00", "5830"),
    ("Hotel Bern Übernachtung Kundentermin CHF 180.00", "5830"),
    ("Taxi Zürich Flughafen Geschäftsreise CHF 58.00", "5830"),
    ("Mobility Carsharing Kundenbesuch CHF 34.50", "6200"),
    ("Shell Benzin Firmenwagen CHF 95.00", "6200"),
    ("Garage Service Firmenwagen CHF 480.00", "6200"),
    ("Autobahnvignette Firmenwagen CHF 40.00", "6200"),
    ("Papeterie Papier und Toner CHF 120.00", "6500"),
    ("Post Briefmarken Versand CHF 38.00", "6500"),
    ("Ordner und Stifte Büro CHF 45.00", "6500"),
    ("Google Ads Kampagne Oktober CHF 300.00", "6600"),
    ("Flyer Druck Werbung CHF 210.00", "6600"),
]

VALID = set(re.findall(r"^\d{4}", CHART, flags=re.M))


def classify(line):
    prompt = (
        f"Chart of accounts:\n{CHART}\n\n"
        f"Invoice line: {line}\n\n"
        "Reply with ONLY the 4-digit account number from the chart."
    )
    r = litellm.completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    m = re.search(r"\d{4}", r.choices[0].message.content)
    return m.group(0) if m else "none"


correct, invalid, misses = 0, 0, []
for text, expected in DATA:
    got = classify(text)
    if got not in VALID:
        invalid += 1
    if got == expected:
        correct += 1
    else:
        misses.append((text, expected, got))

print(f"Model: {MODEL}")
print(f"Accuracy: {correct}/{len(DATA)} = {correct / len(DATA):.0%}")
print(f"Invalid accounts: {invalid}")
for text, exp, got in misses:
    print(f"MISS  {text}  expected {exp}  got {got}")