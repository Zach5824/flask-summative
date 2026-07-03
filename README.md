# Flask Summative Inventory App

A small Flask-based inventory management API with CLI support and integration with the OpenFoodFacts public product database.

## Project Overview

This project provides:

- A Flask REST API for managing a local product inventory.
- CRUD operations for inventory items.
- OpenFoodFacts barcode lookup support to import real product details.
- A command-line interface for interacting with the API locally.

## Features

- `GET /inventory` to list all inventory items.
- `GET /inventory/<id>` to view a single item.
- `POST /inventory` to add a new product manually.
- `PATCH /inventory/<id>` to update price, stock, or product details.
- `DELETE /inventory/<id>` to remove an item.
- `POST /inventory/fetch/<barcode>` to import product data from OpenFoodFacts.

## Repository Structure

- `app.py` — Flask application with inventory routes.
- `cli.py` — Terminal-based user interface for inventory administration.
- `external_api.py` — Helper for querying the OpenFoodFacts API.
- `test_app.py` — Placeholder or tests for the Flask application.
- `.venv/` — Python virtual environment for dependencies.

## Dependencies

The project depends on:

- `Flask`
- `requests`

If you are using the provided virtual environment, activate it first.

## Setup

1. Open a terminal in the project folder.

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. Install dependencies if they are not already installed:

```bash
pip install flask requests
```

## Running the Flask API

Start the server by running:

```bash
python app.py
```

The API runs by default on `http://127.0.0.1:5000`.

## Using the CLI

With the Flask server running, open a new terminal and run:

```bash
python cli.py
```

The CLI provides these operations:

1. View all inventory.
2. View a single item.
3. Add a new inventory item.
4. Update an item price or stock.
5. Delete a product.
6. Find and import a product from OpenFoodFacts by barcode.
7. Exit.

## OpenFoodFacts Integration

The app can import real product data using the OpenFoodFacts API.

- CLI option 6 asks for a barcode.
- It sends a `POST` request to `POST /inventory/fetch/<barcode>`.
- The server fetches product details from `https://world.openfoodfacts.org/api/v0/product/<barcode>.json`.
- The fetched product name, brand, and ingredients are stored locally with the price and stock entered by the user.

### Example Barcode Import

1. Run the Flask app.
2. Run the CLI.
3. Choose option 6.
4. Enter a barcode such as `3017620425035`.
5. Provide a store price and stock quantity.

If the barcode is valid and OpenFoodFacts returns a product, the item is added to the local inventory.

## API Endpoints

### GET /inventory

Returns all inventory items.

### GET /inventory/<id>

Returns a single inventory item by ID.

### POST /inventory

Adds a new item.

Request body example:

```json
{
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar, ...",
  "price": 3.99,
  "stock": 45
}
```

### PATCH /inventory/<id>

Updates one or more fields on an existing item.

### DELETE /inventory/<id>

Deletes the specified item.

### POST /inventory/fetch/<barcode>

Fetches item details from OpenFoodFacts and stores the item locally.

Request body example:

```json
{
  "price": 2.99,
  "stock": 10
}
```

## Notes

- This project uses an in-memory inventory list, so data is lost when the server restarts.
- The OpenFoodFacts helper uses a public API and requires an internet connection.

## License

This repository does not include a license file. Use it for learning and local development.
