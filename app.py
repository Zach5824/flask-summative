from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated in-memory database array (as outlined in 1000257966.jpg)
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

# 1. GET /inventory -> Fetch all items (1000257969.jpg)
@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

# 2. GET /inventory/<id> -> Fetch a single item (1000257969.jpg)
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

# 3. POST /inventory -> Add a new item (1000257969.jpg)
