# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Django REST API (Bookstore) with endpoints for products, categories, and orders. It uses Poetry for dependency management and SQLite for local development (no external services required).

### Running the application

```bash
DEBUG=1 poetry run python manage.py runserver 0.0.0.0:8000
```

The `DEBUG=1` env var is required to enable debug mode and allow `localhost`/`127.0.0.1` in `ALLOWED_HOSTS`.

### Key gotchas

- **whitenoise not in lockfile**: The `pyproject.toml` has malformed trailing entries (duplicate `dj-database-url`, `whitenoise`, `psycopg2-binary` outside the proper `[tool.poetry.dependencies]` section). The lockfile does not include `whitenoise`, so it must be installed separately: `poetry run pip install whitenoise`.
- **Poetry install requires `--no-root`**: The project has no package source directory, so `poetry install --no-root` avoids the "No file/folder found" error.
- **Database**: Uses SQLite by default when `DATABASE_URL` is not set (falls back via `dj_database_url.config()`). No external database needed for development/testing.
- **Tests use Django's test runner**: Run with `poetry run python manage.py test`. Tests use `APITestCase` from DRF and factory_boy for fixtures.

### Commands reference

| Action | Command |
|--------|---------|
| Install deps | `poetry install --no-root && poetry run pip install whitenoise` |
| Run dev server | `DEBUG=1 poetry run python manage.py runserver 0.0.0.0:8000` |
| Run migrations | `poetry run python manage.py migrate` |
| Run tests | `poetry run python manage.py test` |
| Run linter | `poetry run flake8 .` |
| Get auth token | `curl -X POST http://127.0.0.1:8000/api-token-auth/ -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'` |

### API endpoints

- `POST /api-token-auth/` — obtain auth token
- `GET/POST /bookstore/v1/product/` — list/create products
- `GET/POST /bookstore/v1/category/` — list/create categories
- `GET/POST /bookstore/v1/order/` — list/create orders (requires `user` and `products_id` fields)
- `/admin/` — Django admin panel
