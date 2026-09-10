# AI Usage Documentation

## Tool used
Claude (Anthropic), via the claude.ai chat interface.

## What I used it for
- Getting a step-by-step walkthrough for setting up a Django project in VS Code (venv, project/app structure, admin registration).
- Designing the data model (Product, Box, Order, OrderItem) for a multi-product order.
- Designing the box-selection algorithm: weight check, volume check, and a
  longest-dimension sanity check as a documented simplification of true 3D
  bin-packing.
- Writing an initial DRF API endpoint (serializer, view, URL routing).
- Writing the initial automated test suite (shipping/tests.py).
- Debugging git issues (accidentally committing the venv folder and
  db.sqlite3 to version control; fixed with `git rm -r --cached`).
- Getting help drafting this README and AI_USAGE.md structure.

## What I accepted as-is
- The overall Django project structure (config/ + shipping app).
- The models.py structure, including using a through-model (OrderItem) for
  the order/product many-to-many relationship with quantity.
- The general shape of the box-selection algorithm (services.py).

## What I reviewed, tested, and fixed myself
- I ran the algorithm manually in the Django shell against real data
  (Order #1) and against a deliberately oversized "Giant Sofa" product to
  confirm both the success path and the NoSuitableBoxError failure path
  worked correctly.
- When I first ran the automated tests, one test failed:
  `test_recommends_cheapest_box_that_fits` expected the small box, but got
  the medium box. I checked the numbers by hand: the Book product is
  22x15x3cm, and its longest side (22cm) exceeds the small box's longest
  internal side (20cm) — so the small box was correctly rejected by the
  longest-dimension check. The bug was in my test's expected value, not
  in the algorithm. I corrected the test assertion to expect the medium
  box instead.
- I fixed a recurring git issue where the `venv/` folder and `db.sqlite3`
  kept getting tracked in commits despite being listed in `.gitignore`
  (because `.gitignore` only affects untracked files — I had to explicitly
  use `git rm -r --cached` to untrack them after they were already
  committed once).

## What I changed / would do differently
- I modified the error response in views.py to also include the order_id
  field, so API consumers get more context (which order failed) when a
  box recommendation fails, instead of just an error message alone.

## Limitations I'm aware of in the AI-assisted code
- The box-fit check is a simplification (volume + longest-dimension), not
  true 3D bin-packing — documented in the README as a known limitation.
- No support for splitting a large order across multiple boxes.
- No authentication/permissions on the API endpoint.