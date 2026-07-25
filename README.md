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

## Live API

The website uses the Open-Meteo API to display the current outside temperature.

The app sends a GET request using JavaScript's `fetch()` function. The response is returned as JSON, and the current temperature is displayed in the store conditions widget.

The API request handles three states:

- Loading while the request is running
- Success when weather data is returned
- Failure if the network or API is unavailable

The API does not require an API key.

Possible problems include a slow internet connection, the API being unavailable or the response not containing the expected data.

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






