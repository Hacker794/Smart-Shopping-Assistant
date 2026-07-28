import re
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://hacker794.github.io",
                "http://localhost:5500",
                "http://127.0.0.1:5500"
            ]
        }
    }
)

PRODUCTS = [
    {
        "id": 1,
        "name": "Oat Milk 1L",
        "price": 1.35,
        "aisle": "Dairy Alternatives",
        "image": "🥛"
    },
    {
        "id": 2,
        "name": "Sourdough Loaf",
        "price": 2.20,
        "aisle": "Bakery",
        "image": "🥖"
    },
    {
        "id": 3,
        "name": "Bananas 5 Pack",
        "price": 1.10,
        "aisle": "Fruit and Vegetables",
        "image": "🍌"
    },
    {
        "id": 4,
        "name": "Free Range Eggs",
        "price": 2.75,
        "aisle": "Dairy",
        "image": "🥚"
    },
    {
        "id": 5,
        "name": "Penne Pasta 500g",
        "price": 1.25,
        "aisle": "Cupboard",
        "image": "🍝"
    },
    {
        "id": 6,
        "name": "Tomato Pasta Sauce",
        "price": 1.80,
        "aisle": "Cupboard",
        "image": "🍅"
    },
    {
        "id": 7,
        "name": "Chicken Breast 500g",
        "price": 4.50,
        "aisle": "Meat",
        "image": "🍗"
    },
    {
        "id": 8,
        "name": "Greek Yoghurt",
        "price": 1.95,
        "aisle": "Dairy",
        "image": "🥣"
    },
    {
        "id": 9,
        "name": "Orange Juice 1L",
        "price": 2.10,
        "aisle": "Drinks",
        "image": "🧃"
    },
    {
        "id": 10,
        "name": "Dark Chocolate",
        "price": 1.60,
        "aisle": "Snacks",
        "image": "🍫"
    },
    {
        "id": 11,
        "name": "Avocado Twin Pack",
        "price": 1.85,
        "aisle": "Fruit and Vegetables",
        "image": "🥑"
    },
    {
        "id": 12,
        "name": "Cheddar Cheese 350g",
        "price": 3.25,
        "aisle": "Dairy",
        "image": "🧀"
    },
    {
        "id": 13,
        "name": "Still Water 1.5L",
        "price": 0.85,
        "aisle": "Drinks",
        "image": "💧"
    },
    {
        "id": 14,
        "name": "Salted Crisps",
        "price": 1.50,
        "aisle": "Snacks",
        "image": "🥔"
    },
    {
        "id": 15,
        "name": "Plant-Based Burgers",
        "price": 3.75,
        "aisle": "Dairy Alternatives",
        "image": "🍔"
    },
    {
        "id": 16,
        "name": "Frozen Mixed Berries",
        "price": 3.40,
        "aisle": "Frozen",
        "image": "🫐"
    }
]

def extract_budget(need):
    """Return a budget such as £20 from the shopper's request."""

    match = re.search(
        r"(?:under|budget(?:\s+of)?|maximum|max)\s*£\s*(\d+(?:\.\d{1,2})?)",
        need,
        re.IGNORECASE
    )

    if not match:
        return None

    return float(match.group(1))


def extract_suggestion_total(suggestion):
    """Read the final total from the assistant's response."""

    matches = re.findall(
        r"(?:running\s+total|total)\s*:\s*£\s*(\d+(?:\.\d{1,2})?)",
        suggestion,
        re.IGNORECASE
    )

    if not matches:
        return None

    return float(matches[-1])


def call_mock_assistant(prompt):
    """Send one request to the supplied mock assistant."""

    response = requests.post(
        "http://127.0.0.1:5050/v1/messages",
        headers={
            "anthropic-version": "2023-06-01"
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 400,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["content"][0]["text"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "Smart Shopping Assistant API"
    }), 200


@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(PRODUCTS), 200

@app.route("/api/suggestions", methods=["POST"])
def suggest_basket():
    body = request.get_json(silent=True) or {}
    need = body.get("need", "").strip()

    if not need:
        return jsonify({
            "error": "Please describe what you are shopping for."
        }), 400

    if len(need) > 300:
        return jsonify({
            "error": "Your request must be 300 characters or fewer."
        }), 400

    product_summary = "\n".join(
        [
            f"{product['name']} - £{product['price']:.2f}"
            for product in PRODUCTS
        ]
    )

    budget = extract_budget(need)

    prompt = f"""
You are a practical shopping assistant.

Available products:
{product_summary}

Suggest a basket for: "{need}"

Rules:
- Use only products from the available list.
- Choose products that match the shopper's meal or purpose.
- Do not include unrelated products just to spend more.
- Prefer a small, coherent basket.
- Include each selected product's price.
- If a budget is mentioned, stay within it.
- End with the total cost.

Return a short bulleted list followed by:
Total: £0.00
""".strip()

    try:
        suggestion = call_mock_assistant(prompt)
        total = extract_suggestion_total(suggestion)
        retried = False

        # Budget guardrail: reject and retry once if the total is too high.
        if (
            budget is not None
            and total is not None
            and total > budget
        ):
            retried = True

            retry_prompt = f"""
Your previous basket cost £{total:.2f}, which exceeded the budget.

Available products:
{product_summary}

Suggest a basket for: "{need}"

Maximum budget: £{budget:.2f}

Rules:
- The total must not exceed £{budget:.2f}.
- Use only products from the available list.
- Remove lower-priority items if necessary.
- Include each selected product's price.
- End with the corrected total.

Return a short bulleted list followed by:
Total: £0.00
""".strip()

            suggestion = call_mock_assistant(retry_prompt)
            total = extract_suggestion_total(suggestion)

        # Reject the second response if it is still over budget.
        if (
            budget is not None
            and total is not None
            and total > budget
        ):
            return jsonify({
                "error": (
                    "The assistant could not create a basket "
                    "within the stated budget."
                )
            }), 422

        return jsonify({
            "suggestion": suggestion,
            "budget": budget,
            "checked_total": total,
            "guardrail_retried": retried
        }), 200

    except requests.Timeout:
        return jsonify({
            "error": "The assistant took too long to respond."
        }), 504

    except requests.RequestException as error:
        app.logger.error(
            "Mock assistant request failed: %s",
            error
        )

        return jsonify({
            "error": "The assistant is unavailable right now."
        }), 502

    except (KeyError, IndexError, TypeError, ValueError) as error:
        app.logger.error(
            "Unexpected assistant response: %s",
            error
        )

        return jsonify({
            "error": "The assistant returned an unexpected response."
        }), 502

@app.errorhandler(404)
def route_not_found(error):
    return jsonify({
        "error": "Route not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)