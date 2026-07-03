import requests

def fetch_openfoodfacts_data(barcode):
    """
    Queries the external OpenFoodFacts API using a barcode.
    Returns a dictionary with formatted product details, or None if not found/error.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url, headers={"User-Agent": "InventoryManagerApp/1.0"})
        
        if response.status_code == 200:
            data = response.json()
            
            #the API returns a status code 
            # status = 1 means product found, status = 0 means not found
            if data.get("status") == 1:
                product_data = data.get("product", {})
                
                # Extract and format the fields required by the app
                return {
                    "product_name": product_data.get("product_name", "Unknown Product"),
                    "brands": product_data.get("brands", "Unknown Brand"),
                    "ingredients_text": product_data.get("ingredients_text", "No ingredients provided.")
                }
        return None
    except requests.RequestException:
        # Graceful error handling for API failures 
        return None