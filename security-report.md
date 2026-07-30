# Smart Shopping Assistant Security Report

## Overview

I reviewed the Flask API for my Smart Shopping Assistant and made several changes to reduce the risk of invalid input, exposed configuration and misuse of the public API.

## Changes Made

### Removed unrelated local file access

The Flask application contained a local path pointing to the separate Trolley Telemetry project. I removed this path and the telemetry route because the path would not exist on Render and should not be part of the Smart Shopping Assistant API.

### Restricted request size

I added a maximum request size of 16 KB. This helps prevent users from sending unnecessarily large request bodies that could waste server resources or affect availability.

### Improved input validation

The suggestions endpoint now checks that the request uses JSON, that the JSON body is an object and that the `need` field is text. Empty requests and requests longer than 300 characters are rejected.

This is important because input from the browser cannot be trusted. Server-side validation prevents unexpected values from causing errors or being passed to another service.

### Moved service configuration outside the code

The Smart Assistant URL is now read from the `ASSISTANT_URL` environment variable. A local development address is used only as a fallback.

This separates deployment configuration from the source code and follows the same approach that should be used for API keys and other secrets.

### Added security headers

I added headers that prevent content-type sniffing, block the API from being displayed inside a frame and reduce the amount of referrer information shared. API responses are also marked as not suitable for caching.

### Improved error handling

I added safe JSON responses for invalid requests, oversized requests, unsupported content types and unexpected server errors. The user receives a simple message rather than internal server details.

### Restricted cross-origin access

The application already limited API access to the deployed GitHub Pages website and local development addresses. I kept this restriction rather than allowing requests from every website.

## Remaining Risks

The API is public and does not currently require users to log in. An attacker could still repeatedly call the endpoints, so rate limiting should be added.

The project does not currently store passwords or process payments. If accounts are added later, passwords must be hashed and sensitive actions must require authentication and authorisation.

## Conclusion

The main improvements were stronger input validation, limited request sizes, safer error responses, restricted browser access and environment-based configuration. These changes make the API more resistant to malformed requests and reduce the amount of information exposed to an attacker.