"""
Part A — E-Commerce Product Catalog System
============================================

"""

from collections import defaultdict, Counter
from typing import Optional


# ──────────────────────── DATA ────────────────────────

catalog: dict[str, dict] = {
    # ── Electronics (5) ──
    "SKU001": {
        "name": "Laptop",
        "price": 65000,
        "category": "electronics",
        "stock": 15,
        "rating": 4.5,
        "tags": ["computer", "work", "portable"],
    },
    "SKU002": {
        "name": "Wireless Mouse",
        "price": 1200,
        "category": "electronics",
        "stock": 50,
        "rating": 4.2,
        "tags": ["accessory", "computer", "wireless"],
    },
    "SKU003": {
        "name": "Bluetooth Speaker",
        "price": 3500,
        "category": "electronics",
        "stock": 0,
        "rating": 4.0,
        "tags": ["audio", "wireless", "portable"],
    },
    "SKU004": {
        "name": "USB-C Hub",
        "price": 2500,
        "category": "electronics",
        "stock": 30,
        "rating": 4.3,
        "tags": ["accessory", "computer", "hub"],
    },
    "SKU005": {
        "name": "Smartphone",
        "price": 28000,
        "category": "electronics",
        "stock": 20,
        "rating": 4.6,
        "tags": ["phone", "portable", "camera"],
    },

    # ── Clothing (4) ──
    "SKU006": {
        "name": "Cotton T-Shirt",
        "price": 799,
        "category": "clothing",
        "stock": 100,
        "rating": 3.8,
        "tags": ["casual", "cotton", "summer"],
    },
    "SKU007": {
        "name": "Denim Jeans",
        "price": 2200,
        "category": "clothing",
        "stock": 45,
        "rating": 4.1,
        "tags": ["casual", "denim", "winter"],
    },
    "SKU008": {
        "name": "Formal Shirt",
        "price": 1800,
        "category": "clothing",
        "stock": 0,
        "rating": 3.9,
        "tags": ["formal", "office", "cotton"],
    },
    "SKU009": {
        "name": "Running Shoes",
        "price": 3500,
        "category": "clothing",
        "stock": 25,
        "rating": 4.4,
        "tags": ["sports", "running", "fitness"],
    },

    # ── Books (4) ──
    "SKU010": {
        "name": "Python Crash Course",
        "price": 650,
        "category": "books",
        "stock": 60,
        "rating": 4.7,
        "tags": ["programming", "python", "beginner"],
    },
    "SKU011": {
        "name": "Clean Code",
        "price": 800,
        "category": "books",
        "stock": 35,
        "rating": 4.8,
        "tags": ["programming", "best-practices", "software"],
    },
    "SKU012": {
        "name": "Sapiens",
        "price": 550,
        "category": "books",
        "stock": 0,
        "rating": 4.6,
        "tags": ["history", "non-fiction", "bestseller"],
    },
    "SKU013": {
        "name": "Atomic Habits",
        "price": 499,
        "category": "books",
        "stock": 80,
        "rating": 4.9,
        "tags": ["self-help", "productivity", "bestseller"],
    },

    # ── Food (3) ──
    "SKU014": {
        "name": "Organic Green Tea",
        "price": 350,
        "category": "food",
        "stock": 200,
        "rating": 4.3,
        "tags": ["organic", "beverage", "health"],
    },
    "SKU015": {
        "name": "Dark Chocolate Bar",
        "price": 250,
        "category": "food",
        "stock": 150,
        "rating": 4.5,
        "tags": ["snack", "chocolate", "premium"],
    },
    "SKU016": {
        "name": "Mixed Nuts Pack",
        "price": 600,
        "category": "food",
        "stock": 0,
        "rating": 4.1,
        "tags": ["snack", "health", "protein"],
    },
}


# ─────────────────── FUNCTIONS ────────────────────────


def search_by_tag(
    tag: str, cat: Optional[dict[str, dict]] = None
) -> dict[str, list[str]]:
    """Return all products containing the given tag, grouped by tag.

    Uses ``defaultdict(list)`` to accumulate SKUs per tag, then filters
    for the requested tag.

    Args:
        tag: The tag string to search for (case-insensitive).
        cat: Catalog dict to search. Defaults to the global ``catalog``.

    Returns:
        A dict mapping the tag → list of product names that carry it.
        Returns an empty dict if the tag is not found.

    Example:
        >>> search_by_tag('portable')
        {'portable': ['Laptop', 'Bluetooth Speaker', 'Smartphone']}
    """
    cat = cat if cat is not None else catalog

    # Build a full tag → products index using defaultdict
    tag_index: defaultdict[str, list[str]] = defaultdict(list)
    for sku, product in cat.items():
        for t in product.get("tags", []):
            tag_index[t.lower()].append(product.get("name", sku))

    search_tag = tag.lower()
    if search_tag in tag_index:
        return {search_tag: tag_index[search_tag]}
    return {}


def out_of_stock(cat: Optional[dict[str, dict]] = None) -> dict[str, dict]:
    """Return products with stock == 0 using a dict comprehension.

    Args:
        cat: Catalog dict to search. Defaults to the global ``catalog``.

    Returns:
        A filtered catalog dict containing only out-of-stock products.

    Example:
        >>> out_of_stock()
        {'SKU003': {...}, 'SKU008': {...}, 'SKU012': {...}, 'SKU016': {...}}
    """
    cat = cat if cat is not None else catalog
    return {
        sku: details
        for sku, details in cat.items()
        if details.get("stock", 0) == 0
    }


def price_range(
    min_price: float,
    max_price: float,
    cat: Optional[dict[str, dict]] = None,
) -> dict[str, dict]:
    """Filter products whose price falls within [min_price, max_price].

    Args:
        min_price: Lower bound (inclusive).
        max_price: Upper bound (inclusive).
        cat: Catalog dict to search. Defaults to the global ``catalog``.

    Returns:
        Filtered catalog dict.

    Raises:
        ValueError: If min_price > max_price.

    Example:
        >>> price_range(500, 1000)
        {'SKU006': {...}, 'SKU010': {...}, ...}
    """
    if min_price > max_price:
        raise ValueError(
            f"min_price ({min_price}) must be <= max_price ({max_price})"
        )

    cat = cat if cat is not None else catalog
    return {
        sku: details
        for sku, details in cat.items()
        if min_price <= details.get("price", 0) <= max_price
    }


def category_summary(
    cat: Optional[dict[str, dict]] = None,
) -> dict[str, dict[str, float]]:
    """Produce per-category stats: count, avg_price, avg_rating.

    Uses ``defaultdict(list)`` to accumulate prices and ratings per
    category in a single pass, then computes averages.

    Args:
        cat: Catalog dict to summarise. Defaults to the global ``catalog``.

    Returns:
        A dict keyed by category name, each value being a dict with
        ``count``, ``avg_price``, and ``avg_rating``.

    Example:
        >>> category_summary()
        {'electronics': {'count': 5, 'avg_price': 20040.0, 'avg_rating': 4.32}, ...}
    """
    cat = cat if cat is not None else catalog

    prices: defaultdict[str, list[float]] = defaultdict(list)
    ratings: defaultdict[str, list[float]] = defaultdict(list)

    for product in cat.values():
        category = product.get("category", "unknown")
        prices[category].append(product.get("price", 0))
        ratings[category].append(product.get("rating", 0.0))

    return {
        category: {
            "count": len(prices[category]),
            "avg_price": round(sum(prices[category]) / len(prices[category]), 2),
            "avg_rating": round(
                sum(ratings[category]) / len(ratings[category]), 2
            ),
        }
        for category in prices
    }


def apply_discount(
    category: str,
    percent: float,
    cat: Optional[dict[str, dict]] = None,
) -> dict[str, dict]:
    """Reduce prices for all products in *category* by *percent*%.

    Returns a **new** catalog (does not mutate the original) built with
    a dict comprehension.

    Args:
        category: Target category (case-insensitive).
        percent: Discount percentage (0-100).
        cat: Catalog dict. Defaults to the global ``catalog``.

    Returns:
        A new catalog with updated prices for the target category.

    Raises:
        ValueError: If percent is not in the range 0-100.

    Example:
        >>> discounted = apply_discount('electronics', 10)
        >>> discounted['SKU001']['price']
        58500.0
    """
    if not 0 <= percent <= 100:
        raise ValueError(f"Discount percent must be 0-100, got {percent}")

    cat = cat if cat is not None else catalog
    factor = 1 - (percent / 100)
    target = category.lower()

    return {
        sku: (
            {**details, "price": round(details.get("price", 0) * factor, 2)}
            if details.get("category", "").lower() == target
            else details
        )
        for sku, details in cat.items()
    }


def merge_catalogs(
    catalog1: dict[str, dict],
    catalog2: dict[str, dict],
) -> dict[str, dict]:
    """Merge two catalogs, with catalog2 overriding duplicates.

    Uses the ``|`` merge operator (Python 3.9+).  For duplicate SKUs the
    entry from *catalog2* takes precedence (newer data wins).

    Args:
        catalog1: First (base) catalog.
        catalog2: Second catalog whose entries override duplicates.

    Returns:
        A new merged catalog.

    Example:
        >>> c1 = {'SKU001': {'name': 'Laptop', 'price': 65000}}
        >>> c2 = {'SKU001': {'name': 'Laptop Pro', 'price': 75000}}
        >>> merge_catalogs(c1, c2)['SKU001']['name']
        'Laptop Pro'
    """
    # Using the | merge operator (Python 3.9+); catalog2 wins on conflicts
    return catalog1 | catalog2


# ─────────────────── DEMO / MAIN ──────────────────────

def _separator(title: str) -> None:
    """Print a section separator for readability."""
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")


if __name__ == "__main__":

    # 1 ── Search by tag ──────────────────────────────────
    _separator("1. Search by Tag: 'portable'")
    results = search_by_tag("portable")
    for tag, products in results.items():
        print(f"  Tag '{tag}': {products}")

    _separator("   Search by Tag: 'bestseller'")
    results = search_by_tag("bestseller")
    for tag, products in results.items():
        print(f"  Tag '{tag}': {products}")

    # 2 ── Out of stock ───────────────────────────────────
    _separator("2. Out-of-Stock Products")
    oos = out_of_stock()
    for sku, details in oos.items():
        print(f"  {sku}: {details.get('name')} "
              f"(category: {details.get('category')})")

    # 3 ── Price range ────────────────────────────────────
    _separator("3. Products in Price Range ₹500 – ₹1000")
    filtered = price_range(500, 1000)
    for sku, details in filtered.items():
        print(f"  {sku}: {details.get('name')} — ₹{details.get('price')}")

    # 4 ── Category summary ───────────────────────────────
    _separator("4. Category Summary")
    summary = category_summary()
    for cat_name, stats in summary.items():
        print(f"  {cat_name:12s} → count: {stats['count']}, "
              f"avg_price: ₹{stats['avg_price']:,.2f}, "
              f"avg_rating: {stats['avg_rating']}")

    # 5 ── Apply discount ─────────────────────────────────
    _separator("5. Apply 10% Discount on Electronics")
    discounted = apply_discount("electronics", 10)
    for sku in ["SKU001", "SKU002", "SKU005"]:
        original = catalog[sku].get("price")
        new = discounted[sku].get("price")
        print(f"  {sku} ({catalog[sku].get('name')}): "
              f"₹{original} → ₹{new}")

    # 6 ── Merge catalogs ─────────────────────────────────
    _separator("6. Merge Catalogs")
    new_catalog = {
        "SKU001": {
            "name": "Laptop Pro",
            "price": 75000,
            "category": "electronics",
            "stock": 10,
            "rating": 4.8,
            "tags": ["computer", "work", "premium"],
        },
        "SKU017": {
            "name": "Yoga Mat",
            "price": 1200,
            "category": "fitness",
            "stock": 40,
            "rating": 4.3,
            "tags": ["fitness", "yoga", "health"],
        },
    }
    merged = merge_catalogs(catalog, new_catalog)
    print(f"  Original catalog size : {len(catalog)}")
    print(f"  New catalog size      : {len(new_catalog)}")
    print(f"  Merged catalog size   : {len(merged)}")
    print(f"  SKU001 after merge    : {merged['SKU001'].get('name')} "
          f"(₹{merged['SKU001'].get('price')})")
    print(f"  SKU017 (new)          : {merged.get('SKU017', {}).get('name')}")

    print(f"\n{'═' * 60}")
    print("  All Part A functions executed successfully ✓")
    print(f"{'═' * 60}\n")
