from collections import defaultdict

# Product catalog (16 products, 4 categories)
catalog = {
    "SKU001": {"name": "Laptop", "price": 65000, "category": "electronics", "stock": 15, "rating": 4.5, "tags": ["computer", "work"]},
    "SKU002": {"name": "Mouse", "price": 1200, "category": "electronics", "stock": 50, "rating": 4.2, "tags": ["computer", "accessory"]},
    "SKU003": {"name": "Speaker", "price": 3500, "category": "electronics", "stock": 0, "rating": 4.0, "tags": ["audio", "portable"]},
    "SKU004": {"name": "USB Hub", "price": 2500, "category": "electronics", "stock": 30, "rating": 4.3, "tags": ["computer", "hub"]},
    "SKU005": {"name": "Phone", "price": 28000, "category": "electronics", "stock": 20, "rating": 4.6, "tags": ["mobile", "camera"]},

    "SKU006": {"name": "T-Shirt", "price": 800, "category": "clothing", "stock": 100, "rating": 3.8, "tags": ["cotton", "summer"]},
    "SKU007": {"name": "Jeans", "price": 2200, "category": "clothing", "stock": 45, "rating": 4.1, "tags": ["denim", "casual"]},
    "SKU008": {"name": "Formal Shirt", "price": 1800, "category": "clothing", "stock": 0, "rating": 3.9, "tags": ["office", "formal"]},
    "SKU009": {"name": "Shoes", "price": 3500, "category": "clothing", "stock": 25, "rating": 4.4, "tags": ["sports", "running"]},

    "SKU010": {"name": "Python Book", "price": 650, "category": "books", "stock": 60, "rating": 4.7, "tags": ["programming"]},
    "SKU011": {"name": "Clean Code", "price": 800, "category": "books", "stock": 35, "rating": 4.8, "tags": ["programming"]},
    "SKU012": {"name": "Sapiens", "price": 550, "category": "books", "stock": 0, "rating": 4.6, "tags": ["history"]},
    "SKU013": {"name": "Atomic Habits", "price": 499, "category": "books", "stock": 80, "rating": 4.9, "tags": ["self-help"]},

    "SKU014": {"name": "Green Tea", "price": 350, "category": "food", "stock": 200, "rating": 4.3, "tags": ["health"]},
    "SKU015": {"name": "Dark Chocolate", "price": 250, "category": "food", "stock": 150, "rating": 4.5, "tags": ["snack"]},
    "SKU016": {"name": "Mixed Nuts", "price": 600, "category": "food", "stock": 0, "rating": 4.1, "tags": ["snack", "protein"]},
}

# search products by tag
def search_by_tag(tag):
    tag_map = defaultdict(list)

    for sku, product in catalog.items():
        for t in product.get("tags", []):
            tag_map[t].append(product.get("name"))

    return {tag: tag_map.get(tag, [])}

# products with zero stock
def out_of_stock():
    return {sku: p for sku, p in catalog.items() if p.get("stock") == 0}

# products in price range
def price_range(min_price, max_price):
    return {sku: p for sku, p in catalog.items()
            if min_price <= p.get("price", 0) <= max_price}

# summary by category
def category_summary():
    prices = defaultdict(list)
    ratings = defaultdict(list)

    for product in catalog.values():
        cat = product.get("category")
        prices[cat].append(product.get("price", 0))
        ratings[cat].append(product.get("rating", 0))

    result = {}
    for cat in prices:
        result[cat] = {
            "count": len(prices[cat]),
            "avg_price": sum(prices[cat]) / len(prices[cat]),
            "avg_rating": sum(ratings[cat]) / len(ratings[cat])
        }
    return result

# apply discount
def apply_discount(category, percent):
    factor = 1 - percent/100
    return {
        sku: {**p, "price": p.get("price", 0)*factor}
        if p.get("category") == category else p
        for sku, p in catalog.items()
    }

# merge catalogs
def merge_catalogs(c1, c2):
    return c1 | c2
