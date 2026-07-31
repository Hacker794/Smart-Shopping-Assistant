"""
KNULL · Work Experience Programme · Day 6 · Lab 6.2
MOCK LLM ENDPOINT

A stand-in for a real language model. It speaks the same JSON as the
Anthropic Messages API, so the code in your Learning Guide works against it
with ONE change: the URL. Nothing else moves.

    "https://api.anthropic.com/v1/messages"   ->   "http://127.0.0.1:5050/v1/messages"

It does not think. It reads the product list out of your prompt, picks items
that match what the shopper asked for, respects a budget if you gave it one,
and returns a bulleted basket with a running total. That is enough to build
and test the whole Smart Assistant feature — the integration, the grounding,
the budget guardrail and the retry — without a key and without spending
anything.

RUN IT
    pip install flask
    python mock_llm_server.py

Leave it running in its own terminal while you work on your app.

WHY YOU ARE USING THIS
Building against a fake service first is not a downgrade, it is normal
professional practice. It is free, it is instant, it never rate-limits you,
and it gives the same answer every time so you can tell whether a change you
made actually worked. Your brief accepts a recorded demo against mocked keys
as a complete submission.
"""

import re

from flask import Flask, jsonify, request

app = Flask(__name__)

FALLBACK = [("Semi-skimmed milk 2L", 1.45), ("Wholemeal loaf", 1.10),
            ("Free-range eggs (6)", 2.20)]


INSTRUCTION_WORDS = ("suggest", "budget", "running total", "stay under",
                     "return a", "you are a", "basket for")


def parse_products(prompt):
    """Pull '<name> ... £<price>' pairs out of whatever the app sent.

    A product line ends with its price. Instruction lines that happen to
    mention money ("...under £5. Stay under budget if given.") do not, and
    are filtered out as well, so the shopper's budget is never mistaken
    for an item.
    """
    found = []
    for line in prompt.splitlines():
        if any(w in line.lower() for w in INSTRUCTION_WORDS):
            continue
        m = re.match(r"^(.+?)[\s\-–:,]*£\s*(\d+(?:\.\d{1,2})?)\s*$", line.strip())
        if m:
            name = m.group(1).strip(" -–:,•*\t")
            if name and len(name) < 80:
                found.append((name, float(m.group(2))))
    return found


def parse_need(prompt):
    m = re.search(r'for:\s*"([^"]*)"', prompt)
    if m:
        return m.group(1)
    return prompt[-160:]


def parse_budget(prompt):
    m = re.search(r"(?:under|budget of|max(?:imum)?)\s*£\s*(\d+(?:\.\d{1,2})?)",
                  prompt, re.I)
    return float(m.group(1)) if m else None


def choose(products, need, budget):
    """Keyword-match against the need, then fill, then respect the budget."""
    words = {w for w in re.findall(r"[a-z]{4,}", need.lower())}
    scored = sorted(
        products,
        key=lambda p: -sum(1 for w in words if w in p[0].lower()),
    )
    basket, total = [], 0.0
    for name, price in scored:
        if budget is not None and total + price > budget:
            continue
        basket.append((name, price))
        total = round(total + price, 2)
        if len(basket) >= 5:
            break
    return basket, total


def render(basket, total, budget):
    if not basket:
        return ("I couldn't put a basket together from that product list. "
                "Try sending the products with prices, one per line.")
    lines = [f"- {name} — £{price:.2f}" for name, price in basket]
    lines.append(f"\n**Running total: £{total:.2f}**")
    if budget is not None:
        headroom = round(budget - total, 2)
        lines.append(f"Budget £{budget:.2f} — £{headroom:.2f} remaining.")
    return "\n".join(lines)

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "ok",
        "service": "mock-llm"
    }

@app.post("/v1/messages")
def messages():
    body = request.get_json(force=True, silent=True) or {}
    try:
        prompt = body["messages"][-1]["content"]
    except (KeyError, IndexError, TypeError):
        return jsonify({"type": "error", "error": {
            "type": "invalid_request_error",
            "message": "messages must be a non-empty list of {role, content}"
        }}), 400

    if not isinstance(prompt, str):
        prompt = str(prompt)

    products = parse_products(prompt) or FALLBACK
    basket, total = choose(products, parse_need(prompt), parse_budget(prompt))
    text = render(basket, total, parse_budget(prompt))

    # Same envelope the real API returns, so resp.json()["content"][0]["text"]
    # works here and in production without a code change.
    return jsonify({
        "id": "msg_mock_knull_d6",
        "type": "message",
        "role": "assistant",
        "model": body.get("model", "mock-model"),
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": len(prompt) // 4,
                  "output_tokens": len(text) // 4},
    })

if __name__ == "__main__":
    print("Mock LLM on http://127.0.0.1:5050/v1/messages  (Ctrl-C to stop)")
    app.run(port=5050, debug=False)
