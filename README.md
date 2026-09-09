# Box Selection System

A Django-based system that recommends the cheapest shipping box that can hold a customer's order, based on product dimensions/weight and box internal dimensions/weight capacity/cost.

## Problem

Given an order containing one or more products (each with length, width, height, and weight), and a set of available boxes (each with internal dimensions, max weight capacity, and cost), recommend the cheapest box that can hold the entire order.

## Design decisions

- **Orders can contain multiple products** (via a many-to-many relationship with quantity), reflecting a realistic ecommerce order rather than a single-item simplification.
- **Box-fit check is a documented simplification, not true 3D bin-packing.** True bin-packing (deciding exact x/y/z placement and rotation of every item) is a hard computational problem, out of scope here. Instead, a box is considered suitable if:
  1. Total order weight ≤ box's max weight capacity
  2. Total order volume ≤ box's internal volume
  3. Every individual item's longest side fits within the box's longest internal side (a sanity check that catches cases a pure volume check would miss — e.g. one long thin item vs. a small cube-shaped box with equal volume)
- Among all boxes passing these checks, the **cheapest** one is recommended.
- This is documented as a known limitation: the system does not currently support splitting an order across multiple boxes, or true geometric packing verification.

## Tech stack

- Python 3.12, Django 6.1
- Django REST Framework (for the API endpoint)
- SQLite (default Django dev database)

## Setup

```bash
# Clone the repo
git clone https://github.com/Abhii16261/box-selection-system.git
cd box-selection-system

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Run the dev server
python manage.py runserver
```

Then visit:
- `http://127.0.0.1:8000/admin/` — add Products, Boxes, and Orders (with quantities) through the Django admin
- `http://127.0.0.1:8000/api/orders/<order_id>/recommend-box/` — get the recommended box for an order as JSON

## API

**`GET /api/orders/<order_id>/recommend-box/`**

Returns the cheapest box that fits the order:
```json
{
  "box": {
    "id": 1,
    "name": "small box",
    "internal_length_cm": "20.00",
    "internal_width_cm": "15.00",
    "internal_height_cm": "10.00",
    "max_weight_kg": "5.00",
    "cost": "30.00"
  },
  "reason": "Order weight 0.50kg <= box max 5.00kg; order volume 600.000000cm3 <= box volume 3000.000000cm3; cheapest suitable box."
}
```

If no box fits, returns HTTP 422 with an error message. If the order doesn't exist, returns HTTP 404.

## Running tests

```bash
python manage.py test shipping
```

See `TEST_OUTPUT.md` for a sample run.

## Project structure

```
config/          Django project settings and root URL config
shipping/
  models.py      Product, Box, Order, OrderItem
  services.py    Core box-recommendation algorithm
  serializers.py DRF serializers for the API
  views.py       API view
  urls.py        App-level URL routes
  admin.py       Django admin registration
  tests.py       Automated tests for the algorithm
```
