from flask import Flask, jsonify, request
from external_api import fetch_openfoodfacts_data

app = Flask(__name__)

# Simulated in-memory database array 
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, ...",
        "price": 3.99,
        "stock": 45
    }
]

# 1. GET /inventory -> Fetch all items 
@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

# 2. GET /inventory/<id> -> Fetch a single item 
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

# 3. POST /inventory -> Add a new item manually
@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    
    # Simple validation
    if not data or "product_name" not in data:
        return jsonify({"error": "Invalid data. 'product_name' is required."}), 400
        
    # Generate a unique ID 
    new_id = max([item["id"] for item in inventory], default=0) + 1
    
    new_item = {
        "id": new_id,
        "product_name": data.get("product_name"),
        "brands": data.get("brands", "Unknown"),
        "ingredients_text": data.get("ingredients_text", ""),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }
    
    inventory.append(new_item)
    return jsonify(new_item), 201

# 4. PATCH /inventory/<id> -> Update an item's details 
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    # Dynamically update only provided fields
    if "product_name" in data:
        item["product_name"] = data["product_name"]
    if "brands" in data:
        item["brands"] = data["brands"]
    if "ingredients_text" in data:
        item["ingredients_text"] = data["ingredients_text"]
    if "price" in data:
        item["price"] = data["price"]
    if "stock" in data:
        item["stock"] = data["stock"]
        
    return jsonify(item), 200

# 5. DELETE /inventory/<id> -> Remove an item 
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} successfully deleted"}), 200

# 6. POST /inventory/fetch/<barcode> -> Fetch from external API and store it 
@app.route('/inventory/fetch/<barcode>', methods=['POST'])
def fetch_and_add_item(barcode):
    # Query the external API helper function
    external_data = fetch_openfoodfacts_data(barcode)
    
    if not external_data:
        return jsonify({"error": "Product not found on OpenFoodFacts or external API failure"}), 404
        
    data = request.get_json() or {}
    
    # Generate a unique ID
    new_id = max([item["id"] for item in inventory], default=0) + 1
    
    # Combine external product specifications with the local price/stock entries
    new_item = {
        "id": new_id,
        "product_name": external_data["product_name"],
        "brands": external_data["brands"],
        "ingredients_text": external_data["ingredients_text"],
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }
    
    inventory.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    # Running in debug mode for active code validation and testing 
    app.run(debug=True, port=5000)