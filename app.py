import os
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

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "Smart Shopping Assistant API"
    }), 200


@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(PRODUCTS), 200


@app.errorhandler(404)
def route_not_found(error):
    return jsonify({
        "error": "Route not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)