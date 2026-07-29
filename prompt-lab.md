# Prompt Lab

## Task

Create a shopping basket for a simple lunch for two people with a maximum budget of £15.

## Weak Prompt

```text
Suggest some food for lunch.
```

## Weak Prompt Output

```text
- Oat Milk 1L — £1.35
- Bananas 5 Pack — £1.10
- Penne Pasta 500g — £1.25
- Dark Chocolate — £1.60
- Orange Juice 1L — £2.10

Total: £7.40
```

## Strong Prompt

```text
You are a practical shopping assistant.

Available products:
Oat Milk 1L - £1.35
Sourdough Loaf - £2.20
Bananas 5 Pack - £1.10
Free Range Eggs - £2.75
Penne Pasta 500g - £1.25
Tomato Pasta Sauce - £1.80
Chicken Breast 500g - £4.50
Greek Yoghurt - £1.95
Orange Juice 1L - £2.10
Dark Chocolate - £1.60
Avocado Twin Pack - £1.85
Cheddar Cheese 350g - £3.25
Still Water 1.5L - £0.85
Salted Crisps - £1.50
Plant-Based Burgers - £3.75
Frozen Mixed Berries - £3.40

The shopper needs a simple lunch for two people with a maximum budget of £15.

Rules:
- Use only products from the available list.
- Choose products that work together as a sensible lunch.
- Do not add unrelated products just to use more of the budget.
- Include each product's price.
- Keep the total at or below £15.
- End with the total cost.

Return a short bulleted list.
```

## Strong Prompt Output

```text
- Sourdough Loaf — £2.20
- Chicken Breast 500g — £4.50
- Avocado Twin Pack — £1.85
- Cheddar Cheese 350g — £3.25
- Still Water 1.5L — £0.85

Total: £12.65
```

## What Changed

The weak prompt gave no product list, budget rule or required format, so the result could include unsuitable or unavailable items. The strong prompt gave the assistant a clear role, real product data and a precise budget. It also required products that work together and specified how the answer should be formatted. This made the result more relevant, easier to check and less likely to contain invented products.