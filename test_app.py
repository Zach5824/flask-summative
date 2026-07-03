import pytest
from unittest.mock import patch
from app import app, inventory

@pytest.fixture
def client():
    """Configures the Flask app for testing and provides a test client."""
    app.config["TESTING"] = True
    # Reset the in-memory inventory array before each test to keep states isolated
    global inventory
    inventory.clear()
    inventory.append({
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, ...",
        "price": 3.99,
        "stock": 45
    })
    with app.test_client() as client:
        yield client

# === 1. API Endpoint Tests (GET, POST, PATCH, DELETE) ===

def test_get_inventory(client):
    """Test GET /inventory returns all elements."""
    response = client.get('/inventory')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["product_name"] == "Organic Almond Milk"

def test_get_single_item_success(client):
    """Test GET /inventory/<id> returns the exact requested item."""
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.get_json()["id"] == 1

def test_get_single_item_not_found(client):
    """Test GET /inventory/<id> returns 404 for missing items."""
    response = client.get('/inventory/999')
    assert response.status_code == 404

def test_post_inventory_success(client):
    """Test POST /inventory creates a new local record."""
    new_item = {
        "product_name": "Greek Yogurt",
        "brands": "Chobani",
        "ingredients_text": "Cultured nonfat milk",
        "price": 1.49,
        "stock": 20
    }
    response = client.post('/inventory', json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 2
    assert data["product_name"] == "Greek Yogurt"

def test_patch_inventory_success(client):
    """Test PATCH /inventory/<id> selectively updates details."""
    update_data = {"price": 4.25, "stock": 50}
    response = client.patch('/inventory/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 4.25
    assert data["stock"] == 50

def test_delete_inventory_success(client):
    """Test DELETE /inventory/<id> drops item from memory."""
    response = client.delete('/inventory/1')
    assert response.status_code == 200
    # Confirm it's gone
    get_response = client.get('/inventory/1')
    assert get_response.status_code == 404


# === 2. External API Interaction Mocks ===

@patch('app.fetch_openfoodfacts_data')
def test_fetch_and_add_external_success(mock_fetch, client):
    """Test external fetch successfully parses mock API payload into inventory."""
    # Set up simulated data matching valid API return schema
    mock_fetch.return_value = {
        "product_name": "Dark Chocolate 70%",
        "brands": "Lindt",
        "ingredients_text": "Cocoa mass, sugar, cocoa butter"
    }
    
    payload = {"price": 2.99, "stock": 15}
    response = client.post('/inventory/fetch/3046920022651', json=payload)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Dark Chocolate 70%"
    assert data["price"] == 2.99
    assert data["stock"] == 15

@patch('app.fetch_openfoodfacts_data')
def test_fetch_external_not_found(mock_fetch, client):
    """Test external fetch gracefully returns 404 when barcode doesn't exist."""
    mock_fetch.return_value = None
    
    response = client.post('/inventory/fetch/0000000000000', json={})
    assert response.status_code == 404
    assert "error" in response.get_json()


# === 3. CLI Input Flow Testing ===

@patch('requests.get')
def test_cli_view_all_interaction(mock_requests_get):
    """Validates CLI interaction parsing behavior using standard stdout prints."""
    from cli import view_all
    
    # Mock response format coming down from server onto client requests
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = [
        {"id": 1, "product_name": "Apples", "brands": "Gala", "price": 0.99, "stock": 100}
    ]
    
    # Executing function should print table layout out cleanly without crashing
    try:
        view_all()
        assert True
    except Exception as e:
        pytest.fail(f"CLI view_all failed unexpectedly: {e}")