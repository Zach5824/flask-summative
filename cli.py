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

def view_item():
    item_id = input("Enter Item ID to view: ").strip()
    try:
        response = requests.get(f"{BASE_URL}/{item_id}")
        if response.status_code == 200:
            item = response.json()
            print(f"\n--- Item Details ---")
            print(f"ID: {item['id']}")
            print(f"Name: {item['product_name']}")
            print(f"Brand: {item['brands']}")
            print(f"Ingredients: {item['ingredients_text']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock Level: {item['stock']}")
        elif response.status_code == 404:
            print(f"Item with ID {item_id} not found.")
    except requests.RequestException:
        print("Error connecting to server.")

def add_item():
    name = input("Enter product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    brand = input("Enter brand name: ").strip()
    ingredients = input("Enter ingredients text: ").strip()
    
    try:
        price = float(input("Enter price: ") or 0.0)
        stock = int(input("Enter stock level: ") or 0)
    except ValueError:
        print("Invalid input. Price must be a decimal number and stock must be an integer.")
        return

    payload = {
        "product_name": name,
        "brands": brand if brand else "Unknown",
        "ingredients_text": ingredients if ingredients else "No data.",
        "price": price,
        "stock": stock
    }

    try:
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            print("Successfully added item!")
        else:
            print(f"Failed to add item. Server error: {response.json().get('error')}")
    except requests.RequestException:
        print("Error connecting to server.")

def update_item():
    item_id = input("Enter the ID of the item to update: ").strip()
    print("Leave fields blank if you do not want to update them.")
    
    payload = {}
    price_in = input("Enter new price: ").strip()
    stock_in = input("Enter new stock level: ").strip()
    
    try:
        if price_in:
            payload["price"] = float(price_in)
        if stock_in:
            payload["stock"] = int(stock_in)
    except ValueError:
        print("Invalid data types provided for price or stock.")
        return
        
    if not payload:
        print("No changes specified.")
        return

    try:
        response = requests.patch(f"{BASE_URL}/{item_id}", json=payload)
        if response.status_code == 200:
            print("Successfully updated item details.")
        elif response.status_code == 404:
            print(f"Item with ID {item_id} not found.")
    except requests.RequestException:
        print("Error connecting to server.")

def delete_item_cli():
    item_id = input("Enter Item ID to delete: ").strip()
    confirm = input(f"Are you sure you want to delete item {item_id}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Deletion canceled.")
        return
        
    try:
        response = requests.delete(f"{BASE_URL}/{item_id}")
        if response.status_code == 200:
            print(f"Item {item_id} successfully deleted.")
        elif response.status_code == 404:
            print("Item not found.")
    except requests.RequestException:
        print("Error connecting to server.")

def import_external():
    barcode = input("Enter barcode to fetch from OpenFoodFacts: ").strip()
    if not barcode:
        print("Barcode cannot be empty.")
        return
        
    try:
        price = float(input("Assign a store price: ") or 0.0)
        stock = int(input("Assign initial stock level: ") or 0)
    except ValueError:
        print("Invalid input. Defaulting price to 0.0 and stock to 0.")
        price, stock = 0.0, 0

    payload = {"price": price, "stock": stock}
    
    try:
        print("Querying external OpenFoodFacts API database via server...")
        response = requests.post(f"{BASE_URL}/fetch/{barcode}", json=payload)
        if response.status_code == 201:
            item = response.json()
            print(f"Success! Imported '{item['product_name']}' into your local inventory.")
        elif response.status_code == 404:
            print("Error: Barcode not found on OpenFoodFacts or external API failure.")
    except requests.RequestException:
        print("Error connecting to server.")

def main():
    while True:
        print_menu()
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            view_all()
        elif choice == "2":
            view_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item_cli()
        elif choice == "6":
            import_external()
        elif choice == "7":
            print("Exiting Admin Portal. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Please choose an option between 1 and 7.")

if __name__ == "__main__":
    main()