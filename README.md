# Smart Shopping Assistant

A responsive full-stack shopping application created as part of the Knull Work Experience Programme.

The application allows users to browse products, search and filter the catalogue, manage a shopping basket, view live weather information and request shopping suggestions from a Smart Assistant.

## Live Website

[View the Smart Shopping Assistant](https://hacker794.github.io/Smart-Shopping-Assistant/)

## Project Overview

The project began as a front-end website built with HTML, CSS and JavaScript.

It was later extended with:

- A public Flask products API
- Live weather data from Open-Meteo
- Loading, success and error states
- A Smart Assistant feature
- Grounding using the real product catalogue
- A budget validation guardrail
- Responsible-AI documentation
- A reusable prompt library

## Features

### Product catalogue

Users can:

- View products from a Flask REST API
- Search products by name
- Filter products by aisle
- Sort products by name or price
- View product names, prices and aisles

### Shopping basket

Users can:

- Add products to the basket
- Remove individual products
- Clear the complete basket
- View the number of basket items
- View a live-updating total

### Smart Assistant

Users can describe what they need, for example:

```text
I need a simple lunch for two people under £30.
```

The Smart Assistant returns:

- A suggested group of products
- The price of each product
- A running total
- The remaining budget

### Live weather

The application uses the Open-Meteo API to display the current outside temperature.

### Responsive design

The layout uses CSS Grid, Flexbox and media queries.

It was designed to work at:

- 360px mobile width
- 1200px desktop width

## Technologies Used

- HTML
- CSS
- JavaScript
- Python
- Flask
- Flask-CORS
- Requests
- Gunicorn
- Git
- GitHub
- GitHub Pages
- Render
- Open-Meteo API
- Mock LLM server

## Project Structure

```text
Smart-Shopping-Assistant/
├── app.py
├── index.html
├── mock_llm_server.py
├── prompt-library.md
├── README.md
├── requirements.txt
├── Responsible-AI.md
├── script.js
└── style.css
```

## How the Application Works

The public product flow is:

```text
GitHub Pages frontend
        ↓
Flask API hosted on Render
        ↓
Product data returned as JSON
        ↓
JavaScript renders the product cards
```

The local Smart Assistant flow is:

```text
Website on port 5500
        ↓
Flask API on port 5000
        ↓
Mock LLM server on port 5050
        ↓
Shopping suggestion returned
```

## Products API

The product catalogue is returned by the Flask endpoint:

```text
/api/products
```

The public API is hosted on Render:

```text
https://smart-shopping-assistant-api.onrender.com/api/products
```

The frontend uses `fetch()` to request the product data.

The request handles three states:

- Loading while waiting for the response
- Success when the products are returned
- Failure if the server or network is unavailable

If the request fails, the website displays a clear message instead of breaking.

## Weather API

The application uses the Open-Meteo API to retrieve live temperature data.

The request uses:

```javascript
fetch()
```

and handles:

- Loading while the request is running
- Success when the current temperature is returned
- Failure when the weather service cannot be reached

The weather API does not require an API key.

## Smart Assistant

The Smart Assistant allows a shopper to enter a need in natural language.

The frontend sends the request to:

```text
/api/suggestions
```

The Flask backend then creates a structured prompt containing:

- The shopper's request
- The available products
- Product prices
- Instructions not to invent products
- Instructions to respect a stated budget
- A required response format

The result is returned to the page and displayed in an accessible result area.

## Grounding

The assistant is grounded using the real `PRODUCTS` list.

The backend creates a product summary such as:

```text
Oat Milk 1L - £1.35
Sourdough Loaf - £2.20
Bananas 5 Pack - £1.10
```

This product information is included in the prompt before the request is sent.

The assistant is instructed to:

- Use only products from the provided list
- Avoid inventing unavailable products
- Show each product's price
- Keep suggestions relevant to the shopper's need

Grounding reduces hallucination because the assistant receives the real catalogue instead of guessing which products exist.

## Budget Guardrail

The assistant is asked to stay within any budget mentioned by the user.

The backend also performs an independent budget check.

The process is:

```text
Extract the budget from the shopper's request
        ↓
Request a basket suggestion
        ↓
Read the returned total
        ↓
Compare the total with the budget
        ↓
Accept the answer or reject and retry
```

If the first response exceeds the budget, the backend rejects it and sends a corrected prompt.

If the second response still exceeds the budget, the application returns a clear error instead of showing an invalid suggestion.

This is safer than trusting the assistant's response without checking it.

## Loading and Error Handling

The application assumes that network requests can fail.

The Smart Assistant handles:

- Empty user input
- Requests longer than 300 characters
- Slow responses
- Connection failures
- Unexpected API responses
- Assistant service failures
- Suggestions that exceed the stated budget

While the request is running, the button displays:

```text
Thinking...
```

The result area displays:

```text
Creating your shopping suggestions...
```

If the service cannot be reached, the page displays a clear error message.

## Mock LLM Server

The project includes:

```text
mock_llm_server.py
```

This is a free local service used to test the Smart Assistant.

It provides predictable results without requiring a paid API or exposing a secret key.

The mock server is deliberately simple. It is designed to test:

- The request flow
- Product grounding
- Budget handling
- Loading states
- Error states

It is not intended to provide the same recommendation quality as a full language model.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Hacker794/Smart-Shopping-Assistant.git
```

### 2. Enter the project folder

```bash
cd Smart-Shopping-Assistant
```

### 3. Install the dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Start the mock Smart Assistant

Open the first terminal and run:

```bash
python3 mock_llm_server.py
```

The mock server should run on:

```text
http://127.0.0.1:5050
```

Check that it is running by opening:

```text
http://127.0.0.1:5050/health
```

### 5. Start the Flask API

Open a second terminal and run:

```bash
python3 app.py
```

The Flask API should run on:

```text
http://127.0.0.1:5000
```

### 6. Start the frontend

Open a third terminal and run:

```bash
python3 -m http.server 5500
```

Open the website at:

```text
http://127.0.0.1:5500
```

All three terminals must remain running for the local Smart Assistant feature to work.

## Testing the Smart Assistant

Try a request such as:

```text
I need breakfast for two people under £8.
```

Check that:

- The loading message appears
- Only products from the catalogue are suggested
- Product prices are displayed
- The total is calculated
- The total does not exceed £8
- The result appears without reloading the page

To test the failure state, stop the mock server using:

```text
Control + C
```

Then submit another request.

The application should display an error message instead of remaining stuck on a loading state.

## Testing Slow Connections

The loading state may disappear quickly on a fast connection.

To test it in Chrome:

1. Open Developer Tools.
2. Open the **Network** tab.
3. Change **No throttling** to **Slow 3G**.
4. Refresh the website.
5. Submit a Smart Assistant request.

This makes the loading state easier to observe.

Return the setting to **No throttling** after testing.

## Prompt Library

The file:

```text
prompt-library.md
```

contains three reusable prompts:

1. A general basket suggestion prompt
2. A budget-focused shopping prompt
3. A retry prompt for an over-budget response

Each prompt includes a short explanation of why it works.

The prompts use:

- A clear role
- Real product context
- A specific task
- Constraints
- A required output format

## Responsible AI

The project includes:

```text
RESPONSIBLE-AI.md
```

### Risk: hallucination

A language model may confidently suggest products that do not exist in the store.

This could mislead the user and create a basket that cannot actually be purchased.

### Mitigation

The assistant is grounded using the real product list.

In a production version, every returned product would also be checked against valid product IDs before the result was displayed.

Any invented or unavailable product would be rejected.

The assistant's result is treated as a suggestion rather than guaranteed factual information.

## Accessibility

The website includes:

- Semantic HTML
- Descriptive form labels
- Keyboard-accessible buttons
- Visible focus states
- ARIA labels
- `aria-live="polite"` on changing result areas
- Clear loading and error messages
- Text labels rather than colour-only meaning

The Smart Assistant result uses:

```html
aria-live="polite"
```

This allows screen readers to announce the result after it changes without immediately interrupting what they are already reading.

## Responsive Design

The desktop layout places content side by side where space is available.

On narrower screens:

- Sections stack vertically
- Product cards use fewer columns
- The basket moves below the catalogue
- The Smart Assistant form becomes one column
- Buttons remain easy to press
- Text areas use the available width

## Design Decision

The product cards were deliberately kept simple.

Each card contains only:

- Product icon
- Aisle
- Product name
- Price
- Add-to-basket button

This helps users scan the catalogue quickly and reduces unnecessary information, particularly on mobile screens.

## Deployment

### Frontend

The frontend is hosted using GitHub Pages:

```text
https://hacker794.github.io/Smart-Shopping-Assistant/
```

### Products API

The Flask products API is hosted using Render:

```text
https://smart-shopping-assistant-api.onrender.com
```

### Smart Assistant

The supplied mock Smart Assistant currently runs locally on port `5050`.

A future public version could use the Knull proxy or another deployed LLM service.

Any participant code or API key must be stored as an environment variable and must never be committed to GitHub.

## Limitations

- The mock assistant gives basic and predictable suggestions.
- The mock server must be running locally.
- The public GitHub Pages site cannot access a mock server running on a visitor's device.
- Recommendation quality is limited by the mock service.
- External services such as Render or Open-Meteo may occasionally be unavailable.
- A production version would need stronger validation of returned product IDs.

## Future Improvements

Possible improvements include:

- Connecting the assistant to the Knull proxy
- Deploying the Smart Assistant publicly
- Validating every suggested product against product IDs
- Adding dietary tags to the product data
- Adding quantities to basket suggestions
- Allowing suggested products to be added directly to the basket
- Saving the basket using `localStorage`
- Adding more detailed product descriptions
- Improving the assistant's recommendation quality

## Reflection

AI helped me build the Smart Assistant feature more quickly, but I remained responsible for understanding and reviewing the code.

The line between using AI as a tool and allowing it to do my thinking is whether I can explain the decisions, identify weaknesses and change the implementation myself.

I stayed the author by checking how the requests worked, reviewing the prompt, testing loading and failure states, and adding grounding and budget validation rather than trusting the assistant automatically.

I also learned the difference between something that works locally and something that works for every user. A service using `127.0.0.1` only exists on the user's own computer. A public application needs its backend services to be deployed somewhere that visitors can reach.

## Author

Created by Dominic as part of the Knull Work Experience Programme.






