# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
Django REST Framework "Bookstore API" with two apps (`product`, `order`) and an SQLite database. Managed by Poetry.

### Prerequisites
- **Python 3.14** is required (`pyproject.toml` declares `requires-python = ">=3.14"`). Installed via the `deadsnakes` PPA on Ubuntu.
- **Poetry** for dependency management. Installed via `pip install poetry`.

### Running the dev server
```
poetry run python manage.py runserver 0.0.0.0:8000
```
The admin UI is at `/admin/`. Use `poetry run python manage.py createsuperuser` to create an admin account (or via shell: `echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin','admin@example.com','admin123')" | poetry run python manage.py shell`).

### Running tests
```
poetry run python manage.py test
poetry run pytest
```
Note: `pytest` currently collects 0 tests (test files are empty stubs). `manage.py test` will fail with an `ImportError` in `order/serializers/order_serializer.py` due to a pre-existing typo (`serializer.ModelSerializer` instead of `serializers.ModelSerializer`). This is a codebase bug, not an environment issue.

### Running migrations
```
poetry run python manage.py migrate
```

### Known issues
- `order/serializers/order_serializer.py` has a typo: uses `serializer.` instead of `serializers.` — this causes an import error at runtime if that module is loaded.
- Some `__pycache__/` bytecode files are tracked in git despite being in `.gitignore`.
- The `product/admin.py` and `order/admin.py` files import models but don't call `admin.site.register()`; models won't appear in the admin UI until registered.
