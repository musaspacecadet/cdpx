"""Utility functions."""

# We might add things like snake_case conversion here later if needed
# for consistency, but let's keep it minimal for pure parsing first.

def check_key(data: dict, key: str, context: str) -> None:
    """Raises an error if a required key is missing."""
    if key not in data:
        raise KeyError(f"Missing required key '{key}' in {context}")

