# Responsible AI Note

## Risk: Hallucinated products

A language model may confidently suggest products that are not actually sold by the store. This could mislead users and make the basket impossible to purchase.

## Mitigation

The Smart Assistant is grounded using the current `PRODUCTS` list. Only real product names and prices are included in the prompt.

In a production version, every product returned by the assistant would also be checked against valid product IDs before the suggestion was displayed. Any invented or unavailable product would be rejected.

The assistant's output is treated as a suggestion rather than guaranteed factual information.