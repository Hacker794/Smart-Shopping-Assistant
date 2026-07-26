# Smart Shopping Assistant

A responsive shopping web application built as part of the Knull Work Experience Programme.

The project allows users to search through products, add products to a basket and see the basket total update automatically.

## Live Website

[View the Smart Shopping Assistant](https://hacker794.github.io/Smart-Shopping-Assistant/)

## Project Overview

The aim of this project is to create the front end of a Smart Shopping Assistant using HTML, CSS and JavaScript.

The website is designed to work on both mobile and desktop screens. It includes a product search section, a product results grid and a shopping basket panel.

## Features

- Search and filter products
- Display products in a responsive grid
- Add products to a shopping basket
- Automatically update the basket total
- Responsive layout for mobile and desktop
- Clear and accessible page structure

## Stretch Features

- Keyboard navigation
- Visible focus states
- ARIA labels
- Product sorting and filtering
- Basket saved using localStorage
- Dark mode toggle

## APIs and Live Data

This project uses two APIs.

### Open-Meteo API

The Open-Meteo API provides live temperature data for the store conditions widget.

The request handles:

- A loading state while the weather is being fetched
- A success state when the temperature is returned
- An error state when the API or internet connection is unavailable

### Products API

The product catalogue is provided by a Flask REST API through the `/api/products` endpoint.

During development, the API ran locally at `127.0.0.1:5000`. This address only worked on my computer. The API was later deployed publicly so that visitors to the GitHub Pages website could also retrieve the product data.

The products request handles:

- Loading while the API request is running
- Success when product JSON is returned
- Failure if the server, internet connection or response is unavailable

The frontend is hosted on GitHub Pages, while the Flask API is hosted separately as a public web service.

## Technologies Used

- HTML
- CSS
- JavaScript
- Git and GitHub
- GitHub Pages

## Project Structure

```text
Smart-Shopping-Assistant/
│
├── index.html
├── style.css
├── script.js
├── app.py (backend)
├── README.md






