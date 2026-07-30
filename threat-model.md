# Smart Shopping Assistant Threat Model

## System Overview

The Smart Shopping Assistant is a web application that allows shoppers to browse products, filter and sort items, add products to a basket and receive product suggestions from a Smart Assistant.

The system includes:

- A customer-facing website
- A Flask API
- Product and price data
- Basket information
- Smart Assistant requests
- A public deployment using GitHub Pages and Render

This threat model uses STRIDE to identify possible security risks and suitable mitigations. STRIDE stands for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service and Elevation of Privilege.

## Assets That Need Protection

The main assets are:

- Product names, prices and stock information
- Shopper basket data
- Smart Assistant prompts and responses
- Flask API endpoints
- API keys and other secret values
- Application source code
- Render deployment and configuration
- Any future shopper account or payment information

## Threats and Mitigations

| Asset or Area | STRIDE Category | Threat | Possible Impact | Mitigation |
|---|---|---|---|---|
| Flask API | Spoofing | An attacker could pretend to be a trusted user or administrator when making API requests. | The attacker could access restricted features or make unauthorised changes. | Add authentication and check the user’s role before allowing sensitive actions. |
| Product prices | Tampering | An attacker could change a product price by sending modified data to the API. | Products could be sold at incorrect prices and the business could lose money. | Validate price values on the server and allow only authorised users to change prices. |
| Product stock | Tampering | A user could alter stock information through an unprotected request. | Customers could see false availability or order products that are not in stock. | Protect stock-update routes and validate all incoming values. |
| Shopper basket | Tampering | A shopper could modify basket totals or item prices in the browser. | The displayed basket total could be lower than the correct price. | Recalculate prices and totals on the server rather than trusting browser data. |
| API activity | Repudiation | A user could deny making a request or changing data if no records exist. | It may be difficult to investigate misuse or identify who made a change. | Keep security logs containing timestamps, actions and user identifiers without logging passwords or secrets. |
| Smart Assistant prompts | Information Disclosure | Prompts may contain personal, private or sensitive information. | Sensitive information could be exposed through logs or external services. | Avoid collecting unnecessary personal data and remove sensitive values from logs. |
| API keys | Information Disclosure | A secret could be hard-coded in the source code or committed to GitHub. | An attacker could steal the key and use the connected service. | Store secrets in environment variables and immediately rotate any exposed key. |
| Flask errors | Information Disclosure | Detailed error messages could reveal file paths, code details or server configuration. | Attackers could use the information to plan further attacks. | Disable debug mode in production and return simple error messages to users. |
| Public API | Denial of Service | An attacker could send a very large number of requests. | The application could become slow, unavailable or exceed service limits. | Add rate limiting, request-size limits and monitoring. |
| Smart Assistant endpoint | Denial of Service | Repeated expensive assistant requests could overload the API or external service. | Genuine users may be unable to use the assistant and costs may increase. | Limit requests per IP address and reject unusually large prompts. |
| Input fields | Injection | Malicious input could be inserted into database queries or other commands. | An attacker could read, change or delete stored data. | Use parameterised queries and never build queries using string formatting. |
| Website output | Information Disclosure / Injection | User-controlled content could be displayed without being safely handled. | Malicious scripts could run in another shopper’s browser. | Validate input and use safe text rendering instead of inserting raw HTML. |
| Administrative functions | Elevation of Privilege | A normal shopper could gain access to an administrator-only feature. | They could change prices, stock or application settings. | Use role-based access control and check permissions on the server for every protected action. |
| Render account | Elevation of Privilege | An attacker who gains access to the deployment account could control the live API. | They could change code, steal environment variables or take the service offline. | Use a strong unique password, enable multi-factor authentication and restrict account access. |
| Dependencies | Elevation of Privilege | A vulnerable Python package could be exploited. | The attacker could affect the server or application data. | Keep dependencies updated and run tools such as `pip-audit` or Dependabot. |

## Main Entry Points

The main ways an attacker could interact with the system are:

- Search and filter inputs
- Smart Assistant prompt input
- Basket controls
- Public Flask API endpoints
- Query parameters and JSON request bodies
- GitHub repository
- Render deployment
- Third-party APIs used by the application

Every entry point should be treated as untrusted. Validation must happen on the server because browser-side checks can be changed or bypassed.

## Highest-Priority Risks

The highest-priority risks are exposed secrets, unauthorised changes to product data, unsafe user input and excessive requests to the public API.

These threats could lead to financial loss, service disruption or exposure of sensitive information. The first protections should therefore be environment variables for secrets, server-side validation, authorisation checks, parameterised queries and rate limiting.

## Conclusion

Thinking about the Smart Shopping Assistant using STRIDE shows that even a small application has several possible attack points.

The most important security principle is not to trust input from the browser. Sensitive actions should be validated and authorised on the server, secrets should remain outside the source code and public endpoints should be protected against misuse.