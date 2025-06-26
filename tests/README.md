# Test Suite Organization

- `test_cli.py`: CLI command and integration tests
- `test_key.py`: Key validation and key-related logic
- `test_shred.py`: Secure deletion and shred logic
- `test_security.py`: Security features (key generation, hiding, etc.)
- `test_permissions.py`: Permission and error handling tests
- `test_all.py`: Legacy/integration tests (optional)
- `test_utils.py`: Utility/edge-case tests (optional)
- `conftest.py`: Shared pytest fixtures (if needed)
