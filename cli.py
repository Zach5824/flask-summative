import sys
import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

def print_menu():
    print("\n=== Inventory Admin Portal ===")
    print("1. View All Inventory")
    print("2. View Single Item Details")
    print("3. Add New Inventory Item")
    print("4. Update Item Price or Stock")
    print("5. Delete Product")
    print("6. Find & Import Item from OpenFoodFacts API")
    print("7. Exit")
    print("==============================")

def view_all():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            items = response.json()
            if not items:
                print("Inventory is currently empty.")
                return
            print(f"\n{'ID':<5} | {'Product Name':<25} | {'Brand':<15} | {'Price':<8} | {'Stock':<6}")
            print("-" * 68)
            for item in items:
                print(f"{item['id']:<5} | {item['product_name'][:25]:<25} | {item['brands'][:15]:<15} | ${item['price']:<7.2f} | {item['stock']:<6}")
        else:
            print(f"Failed to fetch inventory. Server returned code: {response.status_code}")
    except requests.RequestException:
        print("Error: Could not connect to the Flask API server. Ensure app.py is running.")

